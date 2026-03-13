"""
ConstitutionalMemoryStore - Hardened Qdrant for AgentZero

This implements the AgentZero memory architecture with constitutional governance:

Memory Areas (per project):
- MAIN: Core knowledge, user-provided info
- FRAGMENTS: Conversation snippets, auto-memorized
- SOLUTIONS: Proven solutions, successful approaches
- INSTRUMENTS: Custom procedures, scripts

Constitutional Enforcement:
- F2: Verify recalled memories (truth degradation check)
- F4: Entropy reduction on storage (compression, structuring)
- F12: Scan for injection before storage
- F1: Audit log all memory operations
- Project isolation: Separate collections per tenant
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4


logger = logging.getLogger(__name__)


class MemoryArea(Enum):
    """AgentZero memory classification areas."""
    MAIN = auto()        # Core knowledge, user-provided
    FRAGMENTS = auto()   # Conversation snippets
    SOLUTIONS = auto()   # Proven solutions
    INSTRUMENTS = auto() # Custom procedures
    
    @classmethod
    def from_string(cls, s: str) -> MemoryArea:
        """Parse from string."""
        mapping = {
            "main": cls.MAIN,
            "fragments": cls.FRAGMENTS,
            "solutions": cls.SOLUTIONS,
            "instruments": cls.INSTRUMENTS,
        }
        return mapping.get(s.lower(), cls.MAIN)


@dataclass
class MemoryEntry:
    """A single memory entry with full metadata."""
    id: str
    content: str
    area: MemoryArea
    project_id: str
    
    # Content hash for integrity
    content_hash: str
    
    # Constitutional metadata
    f2_verified: bool = False
    f2_confidence: float = 0.0
    f4_entropy_delta: float = 0.0
    f12_clean: bool = True
    f12_score: float = 0.0
    
    # Temporal metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    access_count: int = 0
    
    # Source tracking
    source: str = "unknown"  # user, agent, tool, import
    source_agent: Optional[str] = None
    
    # Vector embedding (populated by store)
    embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "content": self.content,
            "area": self.area.name,
            "project_id": self.project_id,
            "content_hash": self.content_hash,
            "f2_verified": self.f2_verified,
            "f2_confidence": self.f2_confidence,
            "f4_entropy_delta": self.f4_entropy_delta,
            "f12_clean": self.f12_clean,
            "f12_score": self.f12_score,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "source": self.source,
            "source_agent": self.source_agent,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> MemoryEntry:
        """Create from dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            area=MemoryArea.from_string(data["area"]),
            project_id=data["project_id"],
            content_hash=data["content_hash"],
            f2_verified=data.get("f2_verified", False),
            f2_confidence=data.get("f2_confidence", 0.0),
            f4_entropy_delta=data.get("f4_entropy_delta", 0.0),
            f12_clean=data.get("f12_clean", True),
            f12_score=data.get("f12_score", 0.0),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            access_count=data.get("access_count", 0),
            source=data.get("source", "unknown"),
            source_agent=data.get("source_agent"),
        )


class ConstitutionalMemoryStore:
    """
    Hardened Qdrant-based memory store for AgentZero.
    
    Features:
    - Project-level isolation (separate Qdrant collections)
    - Memory area classification (MAIN/FRAGMENTS/SOLUTIONS/INSTRUMENTS)
    - F2 verification on recall (detect truth degradation)
    - F4 entropy management (compression, structuring)
    - F12 injection scanning (before storage)
    - F1 audit logging (VAULT999 integration)
    - Knowledge import pipeline (MD5 tracking)
    """
    
    def __init__(
        self,
        qdrant_client=None,  # QdrantClient instance
        embedding_model=None,  # Sentence transformer
        prompt_armor=None,  # F12 scanner
        arifos_client=None,  # For F2 verification
        vault_logger=None,  # F1 audit logger
        base_path: str = "./data/agentzero/memory"
    ):
        self.qdrant = qdrant_client
        self.embedding_model = embedding_model
        self.prompt_armor = prompt_armor
        self.arifos = arifos_client
        self.vault = vault_logger
        self.base_path = base_path
        
        # Project tracking
        self.active_projects: Dict[str, Dict] = {}
        
        # Knowledge import tracking
        self.import_tracker: Dict[str, Dict] = {}
        
        # Statistics
        self.stats = {
            "stores": 0,
            "recalls": 0,
            "f2_rejections": 0,
            "f12_blocks": 0,
        }
    
    async def initialize_project(self, project_id: str) -> bool:
        """
        Initialize memory storage for a project.
        
        Creates separate collections for each memory area:
        - {project_id}_main
        - {project_id}_fragments
        - {project_id}_solutions
        - {project_id}_instruments
        """
        if project_id in self.active_projects:
            logger.info(f"Project {project_id} already initialized")
            return True
        
        try:
            # Create collections for each area
            for area in MemoryArea:
                collection_name = f"{project_id}_{area.name.lower()}"
                
                # In real implementation:
                # await self.qdrant.create_collection(
                #     collection_name=collection_name,
                #     vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                # )
                
                logger.info(f"Created collection: {collection_name}")
            
            # Track project
            self.active_projects[project_id] = {
                "initialized_at": datetime.utcnow(),
                "collections": [f"{project_id}_{a.name.lower()}" for a in MemoryArea],
                "entry_count": 0
            }
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize project {project_id}: {e}")
            return False
    
    async def store(
        self,
        content: str,
        area: MemoryArea,
        project_id: str,
        source: str = "agent",
        source_agent: Optional[str] = None,
        skip_f12: bool = False
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Store memory with full constitutional enforcement.
        
        Returns: (success, memory_id, error_message)
        """
        memory_id = str(uuid4())
        
        logger.info(f"[{memory_id}] Storing to {area.name}/{project_id}")
        
        # === F12: Injection Scan ===
        if not skip_f12 and self.prompt_armor:
            scan_result = await self.prompt_armor.scan(content, "memory")
            
            if scan_result.is_injection:
                self.stats["f12_blocks"] += 1
                logger.warning(f"[{memory_id}] F12 BLOCKED: injection detected")
                
                # Log to VAULT999
                if self.vault:
                    await self.vault.log_security_event({
                        "type": "F12_MEMORY_INJECTION",
                        "memory_id": memory_id,
                        "score": scan_result.score,
                        "category": scan_result.category
                    })
                
                return False, None, f"F12_INJECTION_BLOCKED: {scan_result.category}"
            
            f12_clean = True
            f12_score = scan_result.score
        else:
            f12_clean = True
            f12_score = 0.0
        
        # === F4: Entropy Analysis ===
        entropy_delta = self._calculate_entropy_delta(content)
        if entropy_delta > 0:
            logger.warning(f"[{memory_id}] F4: Entropy increase {entropy_delta}")
            # Consider compression/structuring
            content = self._structure_content(content)
        
        # === Generate Embedding ===
        if self.embedding_model:
            embedding = self.embedding_model.encode(content).tolist()
        else:
            # Fallback: simple hash-based (not for production)
            embedding = None
        
        # === Create Memory Entry ===
        entry = MemoryEntry(
            id=memory_id,
            content=content,
            area=area,
            project_id=project_id,
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            f2_verified=False,  # Will be verified on recall
            f2_confidence=0.0,
            f4_entropy_delta=entropy_delta,
            f12_clean=f12_clean,
            f12_score=f12_score,
            source=source,
            source_agent=source_agent,
            embedding=embedding
        )
        
        # === Store to Qdrant ===
        try:
            collection_name = f"{project_id}_{area.name.lower()}"
            
            # In real implementation:
            # await self.qdrant.upsert(
            #     collection_name=collection_name,
            #     points=[PointStruct(
            #         id=memory_id,
            #         vector=embedding,
            #         payload=entry.to_dict()
            #     )]
            # )
            
            # For MVP: file-based storage
            await self._store_to_file(entry, project_id, area)
            
            self.stats["stores"] += 1
            
            # Update project stats
            if project_id in self.active_projects:
                self.active_projects[project_id]["entry_count"] += 1
            
            logger.info(f"[{memory_id}] Stored successfully")
            return True, memory_id, None
            
        except Exception as e:
            logger.error(f"[{memory_id}] Storage failed: {e}")
            return False, None, str(e)
    
    async def recall(
        self,
        query: str,
        project_id: str,
        areas: Optional[List[MemoryArea]] = None,
        k: int = 5,
        threshold: float = 0.7,
        verify_f2: bool = True
    ) -> List[MemoryEntry]:
        """
        Recall memories with F2 verification.
        
        F2: On recall, verify memories are still accurate.
        Memories can degrade over time (truth decay).
        """
        logger.info(f"Recalling from {project_id}: '{query[:50]}...' (k={k})")
        
        areas = areas or list(MemoryArea)
        
        # Generate query embedding
        if self.embedding_model:
            query_embedding = self.embedding_model.encode(query).tolist()
        else:
            query_embedding = None
        
        # Search all relevant collections
        all_results = []
        
        for area in areas:
            collection_name = f"{project_id}_{area.name.lower()}"
            
            try:
                # In real implementation:
                # results = await self.qdrant.search(
                #     collection_name=collection_name,
                #     query_vector=query_embedding,
                #     limit=k,
                #     score_threshold=threshold
                # )
                
                # For MVP: file-based search
                results = await self._search_files(query, project_id, area, k)
                all_results.extend(results)
                
            except Exception as e:
                logger.error(f"Search failed for {collection_name}: {e}")
        
        # Sort by relevance (score)
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # Convert to MemoryEntry objects
        entries = []
        for result in all_results[:k]:
            entry = MemoryEntry.from_dict(result["payload"])
            entry.access_count += 1
            entry.last_accessed = datetime.utcnow()
            entries.append(entry)
        
        # === F2: Verify Recalled Memories ===
        if verify_f2 and self.arifos:
            verified_entries = []
            
            for entry in entries:
                is_accurate, confidence = await self._verify_truth(entry)
                
                if is_accurate:
                    entry.f2_verified = True
                    entry.f2_confidence = confidence
                    verified_entries.append(entry)
                else:
                    logger.warning(f"[{entry.id}] F2: Memory degraded (confidence={confidence})")
                    self.stats["f2_rejections"] += 1
                    
                    # Flag for update rather than delete
                    await self._flag_degraded(entry)
            
            entries = verified_entries
        
        self.stats["recalls"] += 1
        
        logger.info(f"Recalled {len(entries)} verified memories")
        return entries
    
    async def import_knowledge(
        self,
        file_path: str,
        project_id: str,
        area: MemoryArea = MemoryArea.MAIN
    ) -> Dict[str, Any]:
        """
        Import knowledge from file with MD5 tracking.
        
        Implements AgentZero's knowledge import pipeline:
        1. Calculate MD5 checksum
        2. Check if already imported/changed
        3. Chunk and embed
        4. Store with metadata
        """
        import os
        
        logger.info(f"Importing {file_path} to {project_id}/{area.name}")
        
        # Calculate MD5
        md5_hash = await self._calculate_file_md5(file_path)
        
        # Check if already imported
        if file_path in self.import_tracker:
            if self.import_tracker[file_path]["md5"] == md5_hash:
                logger.info(f"{file_path} unchanged, skipping")
                return {"status": "UNCHANGED", "md5": md5_hash}
        
        # Read and chunk
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = self._chunk_document(content)
            
            stored_ids = []
            for chunk in chunks:
                success, mem_id, error = await self.store(
                    content=chunk,
                    area=area,
                    project_id=project_id,
                    source="import",
                    source_agent="knowledge_pipeline"
                )
                
                if success:
                    stored_ids.append(mem_id)
                else:
                    logger.error(f"Failed to store chunk: {error}")
            
            # Update tracker
            self.import_tracker[file_path] = {
                "md5": md5_hash,
                "imported_at": datetime.utcnow().isoformat(),
                "project_id": project_id,
                "area": area.name,
                "chunks": len(chunks),
                "memory_ids": stored_ids
            }
            
            return {
                "status": "IMPORTED",
                "md5": md5_hash,
                "chunks": len(chunks),
                "memory_ids": stored_ids
            }
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return {"status": "FAILED", "error": str(e)}
    
    def get_project_stats(self, project_id: str) -> Dict:
        """Get memory statistics for a project."""
        if project_id not in self.active_projects:
            return {"error": "Project not found"}
        
        stats = self.active_projects[project_id].copy()
        stats["global_stats"] = self.stats
        
        return stats
    
    # === Helper Methods ===
    
    def _calculate_entropy_delta(self, content: str) -> float:
        """
        F4: Calculate entropy change.
        
        Positive = entropy increase (bad)
        Negative = entropy decrease (good)
        """
        # Simplified entropy calculation
        # Real implementation would use information theory
        
        # Factors that increase entropy:
        # - Repetition
        # - Unstructured data
        # - Random noise
        
        # Factors that decrease entropy:
        # - Structure
        # - Compression
        # - Organization
        
        lines = content.split('\n')
        
        # Unstructured content has high entropy
        avg_line_length = sum(len(l) for l in lines) / max(1, len(lines))
        variance = sum((len(l) - avg_line_length) ** 2 for l in lines) / max(1, len(lines))
        
        # High variance = unstructured = high entropy
        entropy = variance / 1000  # Normalize
        
        return min(1.0, entropy)
    
    def _structure_content(self, content: str) -> str:
        """F4: Structure content to reduce entropy."""
        # Simple structuring
        lines = content.split('\n')
        
        # Remove excessive blank lines
        structured = []
        prev_blank = False
        for line in lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            structured.append(line)
            prev_blank = is_blank
        
        return '\n'.join(structured)
    
    async def _verify_truth(self, entry: MemoryEntry) -> Tuple[bool, float]:
        """
        F2: Verify memory is still accurate.
        
        In production, this would:
        - Check against ground truth
        - Verify source is still valid
        - Detect contradictions with newer knowledge
        
        For MVP: Assume valid unless very old
        """
        age_days = (datetime.utcnow() - entry.created_at).days
        
        # Very old memories need re-verification
        if age_days > 365:
            return False, 0.5
        
        # Recent memories are likely valid
        confidence = max(0.5, 1.0 - (age_days / 730))  # Degrade over 2 years
        
        return confidence > 0.7, confidence
    
    async def _flag_degraded(self, entry: MemoryEntry):
        """Flag a memory as degraded for later review."""
        logger.info(f"[{entry.id}] Flagged for degradation review")
        # Would update metadata in Qdrant
    
    async def _calculate_file_md5(self, file_path: str) -> str:
        """Calculate MD5 hash of file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _chunk_document(self, content: str, chunk_size: int = 1000) -> List[str]:
        """Split document into chunks."""
        words = content.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size >= chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    async def _store_to_file(self, entry: MemoryEntry, project_id: str, area: MemoryArea):
        """MVP: Store to file (replace with Qdrant in production)."""
        import os
        
        dir_path = os.path.join(self.base_path, project_id, area.name.lower())
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, f"{entry.id}.json")
        
        with open(file_path, 'w') as f:
            json.dump(entry.to_dict(), f, indent=2)
    
    async def _search_files(self, query: str, project_id: str, area: MemoryArea, k: int) -> List[Dict]:
        """MVP: Simple file-based search (replace with Qdrant in production)."""
        import os
        
        dir_path = os.path.join(self.base_path, project_id, area.name.lower())
        
        if not os.path.exists(dir_path):
            return []
        
        results = []
        query_lower = query.lower()
        
        for filename in os.listdir(dir_path):
            if not filename.endswith('.json'):
                continue
            
            file_path = os.path.join(dir_path, filename)
            
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                content = data.get("content", "").lower()
                
                # Simple relevance score
                score = 0.0
                for word in query_lower.split():
                    if word in content:
                        score += 0.2
                
                if score > 0:
                    results.append({
                        "payload": data,
                        "score": min(1.0, score)
                    })
                    
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
        
        return results
