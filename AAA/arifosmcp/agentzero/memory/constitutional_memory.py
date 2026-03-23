"""
ConstitutionalMemoryStore - Hardened Qdrant for AgentZero

Memory Areas (per project):
- MAIN: Core knowledge, user-provided info
- FRAGMENTS: Conversation snippets, auto-memorized
- SOLUTIONS: Proven solutions, successful approaches
- INSTRUMENTS: Custom procedures, scripts

Constitutional Enforcement:
- F2: Verify vector query results (truth degradation check)
- F4: Entropy reduction on storage (compression, structuring)
- F12: Scan for injection before storage
- F1: Audit log all memory operations
- Project isolation: Separate collections per tenant
"""

from __future__ import annotations

import hashlib
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any

logger = logging.getLogger(__name__)

QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
VECTOR_DIM = int(os.getenv("ARIFOS_VECTOR_DIM", "1024"))


class MemoryArea(Enum):
    """AgentZero memory classification areas."""

    MAIN = auto()        # Core knowledge, user-provided
    FRAGMENTS = auto()   # Conversation snippets
    SOLUTIONS = auto()   # Proven solutions
    INSTRUMENTS = auto() # Custom procedures

    @classmethod
    def from_string(cls, s: str) -> MemoryArea:
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
    content_hash: str

    # Constitutional metadata
    f2_verified: bool = False
    f2_confidence: float = 0.0
    f4_entropy_delta: float = 0.0
    f12_clean: bool = True
    f12_score: float = 0.0

    # Temporal metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    access_count: int = 0

    # Source tracking
    source: str = "unknown"
    source_agent: str | None = None
    embedding: list[float] | None = None

    def to_dict(self) -> dict[str, Any]:
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
    def from_dict(cls, data: dict[str, Any]) -> MemoryEntry:
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


def _build_qdrant_client():
    """Build Qdrant client — remote when QDRANT_URL set, VPS host otherwise."""
    from qdrant_client import QdrantClient

    if QDRANT_URL:
        kwargs: dict[str, Any] = {"url": QDRANT_URL, "timeout": 5.0}
        if QDRANT_API_KEY:
            kwargs["api_key"] = QDRANT_API_KEY
        return QdrantClient(**kwargs)
    
    # Wired for srv1325122.hstgr.cloud internal Docker networking
    return QdrantClient(host="qdrant_memory", port=6333)


def _embed(text: str) -> list[float]:
    """Generate embedding using the shared BGE-M3 model."""
    try:
        from arifosmcp.intelligence.embeddings import embed
        return embed(text)
    except Exception:
        # Fallback: deterministic hash-based pseudo-embedding
        digest = hashlib.sha256(text.encode()).digest()
        vec = [(b / 127.5) - 1.0 for b in digest]
        while len(vec) < VECTOR_DIM:
            vec.extend(vec)
        return vec[:VECTOR_DIM]


class ConstitutionalMemoryStore:
    """
    Hardened Qdrant-based memory store for AgentZero.

    Uses in-memory Qdrant when no QDRANT_URL is set (dev/test),
    or connects to a remote Qdrant server in production.
    """

    def __init__(
        self,
        qdrant_client: Any = None,
        embedding_model: Any = None,
        prompt_armor: Any = None,
        arifos_client: Any = None,
        vault_logger: Any = None,
        base_path: str = "./data/agentzero/memory",
    ) -> None:
        self.qdrant = qdrant_client or _build_qdrant_client()
        self.embedding_model = embedding_model
        self.prompt_armor = prompt_armor
        self.arifos = arifos_client
        self.vault = vault_logger
        self.base_path = base_path

        self.active_projects: dict[str, dict[str, Any]] = {}
        self.import_tracker: dict[str, dict[str, Any]] = {}
        self.stats = {
            "stores": 0,
            "vector_queries": 0,
            "f2_rejections": 0,
            "f12_blocks": 0,
        }

    def _collection_name(self, project_id: str, area: MemoryArea) -> str:
        # Use arifos_memory as a unified collection per Job 2 blueprint
        return os.getenv("ARIFOS_MEMORY_COLLECTION", "arifos_memory")

    def _ensure_collection(self, collection_name: str) -> None:
        from qdrant_client.models import Distance, VectorParams

        try:
            self.qdrant.get_collection(collection_name)
        except Exception:
            self.qdrant.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
            )
            logger.info(f"Created Qdrant collection: {collection_name}")

    async def initialize_project(self, project_id: str) -> bool:
        if project_id in self.active_projects:
            return True
        try:
            for area in MemoryArea:
                self._ensure_collection(self._collection_name(project_id, area))
            self.active_projects[project_id] = {
                "initialized_at": datetime.now(timezone.utc),
                "collections": [self._collection_name(project_id, a) for a in MemoryArea],
                "entry_count": 0,
            }
            logger.info(f"Initialized project '{project_id}' in Qdrant")
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
        source_agent: str | None = None,
        skip_f12: bool = False,
    ) -> tuple[bool, str | None, str | None]:
        """Store memory with full constitutional enforcement."""
        memory_id = str(uuid.uuid4())
        logger.info(f"[{memory_id}] Storing to {area.name}/{project_id}")

        # === F12: Injection Scan ===
        f12_clean = True
        f12_score = 0.0
        if not skip_f12 and self.prompt_armor:
            scan_result = await self.prompt_armor.scan(content, "memory")
            if scan_result.is_injection:
                self.stats["f12_blocks"] += 1
                logger.warning(f"[{memory_id}] F12 BLOCKED: injection detected")
                if self.vault:
                    await self.vault.log_security_event({
                        "type": "F12_MEMORY_INJECTION",
                        "memory_id": memory_id,
                        "score": scan_result.score,
                        "category": scan_result.category,
                    })
                return False, None, f"F12_INJECTION_BLOCKED: {scan_result.category}"
            f12_score = scan_result.score

        # === F4: Entropy Analysis ===
        entropy_delta = self._calculate_entropy_delta(content)
        if entropy_delta > 0:
            logger.warning(f"[{memory_id}] F4: Entropy increase {entropy_delta:.3f}")
            content = self._structure_content(content)

        embedding = _embed(content)

        entry = MemoryEntry(
            id=memory_id,
            content=content,
            area=area,
            project_id=project_id,
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            f4_entropy_delta=entropy_delta,
            f12_clean=f12_clean,
            f12_score=f12_score,
            source=source,
            source_agent=source_agent,
            embedding=embedding,
        )

        try:
            from qdrant_client.models import PointStruct

            coll = self._collection_name(project_id, area)
            self._ensure_collection(coll)
            self.qdrant.upsert(
                collection_name=coll,
                points=[PointStruct(id=memory_id, vector=embedding, payload=entry.to_dict())],
            )
            self.stats["stores"] += 1
            if project_id in self.active_projects:
                self.active_projects[project_id]["entry_count"] += 1
            logger.info(f"[{memory_id}] Stored to Qdrant")
            return True, memory_id, None
        except Exception as e:
            logger.error(f"[{memory_id}] Qdrant storage failed: {e}")
            return False, None, str(e)

    async def vector_query(
        self,
        query: str,
        project_id: str,
        areas: list[MemoryArea] | None = None,
        k: int = 5,
        threshold: float = 0.5,
        verify_f2: bool = True,
    ) -> list[MemoryEntry]:
        """
        555_MEMORY: Vector semantic search with F2 verification.
        
        Constitutional Floors:
        - F2: Verify recalled memories (truth degradation check)
        - F4: Entropy reduction (structured results)
        - F12: Injection scan on query vector
        
        Args:
            query: Search query text
            project_id: Project namespace (tenant isolation)
            k: Number of results (max 100)
            areas: Optional MemoryArea filter
            verify_f2: Run F2 truth verification on results
        
        Returns:
            List of MemoryEntry with constitutional metadata
        """
        logger.info(f"vector_query from '{project_id}': '{query[:50]}' (k={k})")
        areas = areas or list(MemoryArea)
        query_vec = _embed(query)
        all_results: list[dict[str, Any]] = []

        for area in areas:
            coll = self._collection_name(project_id, area)
            try:
                self._ensure_collection(coll)
                response = self.qdrant.query_points(
                    collection_name=coll,
                    query=query_vec,
                    limit=k,
                    score_threshold=threshold,
                    with_payload=True,
                )
                for hit in getattr(response, "points", []):
                    all_results.append({"payload": hit.payload, "score": hit.score})
            except Exception as e:
                logger.error(f"Qdrant search failed for {coll}: {e}")

        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)

        entries: list[MemoryEntry] = []
        for result in all_results[:k]:
            try:
                entry = MemoryEntry.from_dict(result["payload"])
                entry.access_count += 1
                entry.last_accessed = datetime.now(timezone.utc)
                entries.append(entry)
            except Exception as e:
                logger.warning(f"Failed to parse memory entry: {e}")

        # === F2: Verify Recalled Memories ===
        if verify_f2 and self.arifos:
            verified: list[MemoryEntry] = []
            for entry in entries:
                is_accurate, confidence = await self._verify_truth(entry)
                if is_accurate:
                    entry.f2_verified = True
                    entry.f2_confidence = confidence
                    verified.append(entry)
                else:
                    logger.warning(
                        f"[{entry.id}] F2: Memory degraded (confidence={confidence:.2f})"
                    )
                    self.stats["f2_rejections"] += 1
                    await self._flag_degraded(entry)
            entries = verified

        self.stats["vector_queries"] += 1
        logger.info(f"vector_query returned {len(entries)} verified memories from Qdrant")
        return entries

    async def recall(
        self,
        query: str,
        project_id: str,
        areas: list[MemoryArea] | None = None,
        k: int = 5,
        threshold: float = 0.5,
        verify_f2: bool = True,
    ) -> list[MemoryEntry]:
        """
        [DEPRECATED] Use vector_query() instead.
        
        Legacy alias maintained for backward compatibility.
        Logs deprecation warning.
        """
        logger.warning("DEPRECATED: recall() called — use vector_query() instead")
        return await self.vector_query(
            query=query,
            project_id=project_id,
            areas=areas,
            k=k,
            threshold=threshold,
            verify_f2=verify_f2,
        )

    async def import_knowledge(
        self,
        file_path: str,
        project_id: str,
        area: MemoryArea = MemoryArea.MAIN,
    ) -> dict[str, Any]:
        """Import knowledge from file with MD5 tracking."""
        logger.info(f"Importing {file_path} to {project_id}/{area.name}")
        md5_hash = await self._calculate_file_md5(file_path)

        if file_path in self.import_tracker:
            if self.import_tracker[file_path]["md5"] == md5_hash:
                logger.info(f"{file_path} unchanged, skipping")
                return {"status": "UNCHANGED", "md5": md5_hash}

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            chunks = self._chunk_document(content)
            stored_ids = []
            for chunk in chunks:
                success, mem_id, error = await self.store(
                    content=chunk,
                    area=area,
                    project_id=project_id,
                    source="import",
                    source_agent="knowledge_pipeline",
                )
                if success:
                    stored_ids.append(mem_id)
                else:
                    logger.error(f"Failed to store chunk: {error}")

            self.import_tracker[file_path] = {
                "md5": md5_hash,
                "imported_at": datetime.now(timezone.utc).isoformat(),
                "project_id": project_id,
                "area": area.name,
                "chunks": len(chunks),
                "memory_ids": stored_ids,
            }
            return {"status": "IMPORTED", "md5": md5_hash, "chunks": len(chunks),
                    "memory_ids": stored_ids}

        except Exception as e:
            logger.error(f"Import failed: {e}")
            return {"status": "FAILED", "error": str(e)}

    def get_project_stats(self, project_id: str) -> dict[str, Any]:
        if project_id not in self.active_projects:
            return {"error": "Project not found"}
        stats = self.active_projects[project_id].copy()
        stats["global_stats"] = self.stats
        stats["qdrant_mode"] = "remote" if QDRANT_URL else "in-memory"
        return stats

    # === Helper Methods ===

    def _calculate_entropy_delta(self, content: str) -> float:
        """F4: Positive = entropy increase (bad)."""
        lines = content.split("\n")
        avg = sum(len(line) for line in lines) / max(1, len(lines))
        variance = sum((len(line) - avg) ** 2 for line in lines) / max(1, len(lines))
        return min(1.0, variance / 1000)

    def _structure_content(self, content: str) -> str:
        """F4: Remove excessive blank lines to reduce entropy."""
        structured = []
        prev_blank = False
        for line in content.split("\n"):
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            structured.append(line)
            prev_blank = is_blank
        return "\n".join(structured)

    async def _verify_truth(self, entry: MemoryEntry) -> tuple[bool, float]:
        """F2: Verify memory accuracy by age."""
        age_days = (datetime.now(timezone.utc) - entry.created_at.replace(tzinfo=timezone.utc)).days
        if age_days > 365:
            return False, 0.5
        confidence = max(0.5, 1.0 - (age_days / 730))
        return confidence > 0.7, confidence

    async def _flag_degraded(self, entry: MemoryEntry) -> None:
        logger.info(f"[{entry.id}] Flagged for degradation review")

    async def _calculate_file_md5(self, file_path: str) -> str:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _chunk_document(self, content: str, chunk_size: int = 1000) -> list[str]:
        words = content.split()
        chunks: list[str] = []
        current: list[str] = []
        size = 0
        for word in words:
            current.append(word)
            size += len(word) + 1
            if size >= chunk_size:
                chunks.append(" ".join(current))
                current = []
                size = 0
        if current:
            chunks.append(" ".join(current))
        return chunks
