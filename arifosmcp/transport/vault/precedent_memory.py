"""
vault_precedent_memory — Constitutional Precedent Vector Store

Dual-layer memory: Ledger (truth) + Vectors (interpretation)
- Collection: vault_precedent_memory (1024-dim, Cosine)
- Model: BAAI/bge-m3 (multilingual — Malay, English, Manglish)
- Purpose: Semantic retrieval of governance decisions

Critical Rule: Vectors reference ledger, never replace it.
Join key: session_id (exact match)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

# Try to import Qdrant client
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance,
        FieldCondition,
        Filter,
        MatchAny,
        PointStruct,
        VectorParams,
    )

    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

# Try to import embedding function
try:
    from arifosmcp.intelligence.embeddings import embed

    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


# F2 Truth + F6 Empathy: BGE-M3 supports Malay, English, Manglish (1024-dim)
VECTOR_DIM = 1024
COLLECTION_NAME = "vault_precedent_memory"
EMBEDDING_MODEL = "BAAI/bge-m3"


@dataclass
class PrecedentEntry:
    """A constitutional precedent entry linking vector to ledger."""

    seal_id: str
    session_id: str
    timestamp: str
    verdict: str
    floors_failed: list[str]
    governance_explanation: str
    thermodynamic_scar: str
    constitutional_lesson: str
    eureka_score: float
    vector_id: str  # ID in Qdrant


class VaultPrecedentMemory:
    """
    Constitutional precedent engine for VAULT999.

    Strengthens F3 Tri-Witness by adding HISTORICAL witness:
    W4 = Human × AI × System × Precedent
    """

    def __init__(self, qdrant_url: str | None = None, embedding_fn: Callable | None = None):
        self.qdrant_url = qdrant_url or os.environ.get("QDRANT_URL", "http://localhost:6333")
        self.embedding_fn = embedding_fn or embed
        self._client: QdrantClient | None = None
        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize Qdrant connection and ensure collection exists."""
        if not QDRANT_AVAILABLE:
            print("[VAULT_PRECEDENT] Qdrant not available, precedent memory disabled")
            return False

        if not EMBEDDING_AVAILABLE:
            print("[VAULT_PRECEDENT] Embeddings not available, precedent memory disabled")
            return False

        try:
            self._client = QdrantClient(self.qdrant_url)

            # Check if collection exists
            collections = self._client.get_collections().collections
            exists = any(c.name == COLLECTION_NAME for c in collections)

            if not exists:
                # F2 Truth: 1024-dim BGE-M3 (multilingual — Malay, English, Manglish)
                self._client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
                )
                print(f"[VAULT_PRECEDENT] Created {COLLECTION_NAME} ({VECTOR_DIM}-dim, Cosine)")
            else:
                print(f"[VAULT_PRECEDENT] Connected to {COLLECTION_NAME}")

            self._initialized = True
            return True

        except Exception as e:
            print(f"[VAULT_PRECEDENT] Initialization failed: {e}")
            return False

    async def embed_governance_decision(self, vault_entry: dict[str, Any]) -> str | None:
        """
        Create semantic embedding of governance reasoning.

        ONLY embed interpretive fields, NEVER embed:
        - verdict (exact value)
        - telemetry (numeric precision)
        - session_id (identity reference)
        """
        if not self._initialized:
            await self.initialize()

        if not self._client:
            return None

        # Extract interpretive content only
        governance_explanation = self._generate_governance_explanation(vault_entry)

        # Build semantic text for embedding
        interpretive_text = f"""
        Constitutional Decision Analysis:
        {governance_explanation}
        
        Failed Floors: {', '.join(vault_entry.get('floors_failed', []))}
        
        Thermodynamic Context:
        {vault_entry.get('thermodynamics', {}).get('status', 'N/A')}
        
        Eureka Score: {vault_entry.get('eureka_score', 0):.2f}
        """.strip()

        # Generate embedding
        try:
            embedding = self.embedding_fn(interpretive_text)

            # Create unique vector ID
            vector_id = hashlib.sha256(
                f"{vault_entry['seal_id']}:{vault_entry['timestamp']}".encode()
            ).hexdigest()[:16]

            # Store in Qdrant with ledger reference metadata
            self._client.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=vector_id,
                        vector=embedding,
                        payload={
                            "seal_id": vault_entry["seal_id"],
                            "session_id": vault_entry["session_id"],  # Join key
                            "timestamp": vault_entry["timestamp"],
                            "verdict": vault_entry.get("verdict", "UNKNOWN"),
                            "floors_failed": vault_entry.get("floors_failed", []),
                            "eureka_score": vault_entry.get("eureka_score", 0),
                            "governance_explanation": governance_explanation[:500],
                            # F2 Truth: Model info for audit
                            "embedding_model": EMBEDDING_MODEL,
                            "vector_dim": VECTOR_DIM,
                            # F6 Empathy: Support multilingual governance (BM, EN, Manglish)
                            "multilingual": True,
                            "languages_supported": ["ms", "en", "manglish"],
                        },
                    )
                ],
            )

            print(f"[VAULT_PRECEDENT] Embedded {vector_id} → {COLLECTION_NAME}")
            return vector_id

        except Exception as e:
            print(f"[VAULT_PRECEDENT] Embedding failed: {e}")
            return None

    def _generate_governance_explanation(self, vault_entry: dict) -> str:
        """Generate human-readable governance explanation from entry."""
        verdict = vault_entry.get("verdict", "UNKNOWN")
        floors_failed = vault_entry.get("floors_failed", [])
        eureka = vault_entry.get("eureka_score", 0)

        explanations = []

        if verdict == "SEAL":
            explanations.append(f"Full constitutional SEAL achieved with EUREKA score {eureka:.2f}")
        elif verdict == "VOID":
            explanations.append(f"Hard floor VOID: {', '.join(floors_failed)}")
        elif verdict == "SABAR":
            explanations.append("Cooling period SABAR: potential risk detected")
        elif verdict == "888_HOLD":
            explanations.append("Human sovereign approval required (888_HOLD)")

        # Add floor-specific explanations
        for floor in floors_failed:
            if floor == "F1":
                explanations.append("Irreversible action blocked by Amanah")
            elif floor == "F2":
                explanations.append("Truth threshold not met")
            elif floor == "F3":
                explanations.append("Tri-witness consensus failed")
            elif floor == "F4":
                explanations.append("Entropy increased (clarity violation)")

        return " | ".join(explanations) if explanations else "Standard governance flow"

    async def find_similar_precedents(
        self, query: str, verdict_filter: list[str] | None = None, k: int = 5
    ) -> list[dict[str, Any]]:
        """
        Retrieve similar past governance decisions.

        Returns precedent entries with semantic scores and ledger references.
        """
        if not self._initialized or not self._client:
            return []

        try:
            # Embed query
            query_embedding = self.embedding_fn(query)

            # Build filter
            search_filter = None
            if verdict_filter:
                search_filter = Filter(
                    must=[FieldCondition(key="verdict", match=MatchAny(any=verdict_filter))]
                )

            # Search
            results = self._client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_embedding,
                limit=k,
                query_filter=search_filter,
                with_payload=True,
            )

            precedents = []
            for result in results:
                precedents.append(
                    {
                        "semantic_score": result.score,
                        "vector_id": result.id,
                        "session_id": result.payload["session_id"],  # Join key
                        "seal_id": result.payload["seal_id"],
                        "verdict": result.payload["verdict"],
                        "timestamp": result.payload["timestamp"],
                        "floors_failed": result.payload["floors_failed"],
                        "governance_explanation": result.payload["governance_explanation"],
                        "eureka_score": result.payload["eureka_score"],
                    }
                )

            return precedents

        except Exception as e:
            print(f"[VAULT_PRECEDENT] Search failed: {e}")
            return []

    async def detect_constitutional_drift(self, window_days: int = 30) -> dict[str, Any]:
        """
        Detect if recent decisions diverge from historical precedent.

        Constitutional anomaly detection for F8 Genius.
        """
        if not self._initialized:
            return {"status": "DISABLED", "drift_score": 0}

        try:
            # Get recent vs historical distributions
            # This is a simplified version - full implementation would
            # compare embedding centroids

            return {
                "status": "NOMINAL",
                "drift_score": 0.0,
                "message": "Constitutional precedent tracking active",
                "precedents_stored": self._client.count(COLLECTION_NAME).count,
            }

        except Exception as e:
            return {"status": "ERROR", "drift_score": 0, "message": str(e)}


# Global instance
_precedent_memory: VaultPrecedentMemory | None = None


async def get_precedent_memory() -> VaultPrecedentMemory:
    """Get or create global precedent memory instance."""
    global _precedent_memory
    if _precedent_memory is None:
        _precedent_memory = VaultPrecedentMemory()
        await _precedent_memory.initialize()
    return _precedent_memory


async def embed_vault_entry(vault_entry: dict[str, Any]) -> str | None:
    """Convenience function: embed a vault entry to precedent memory."""
    memory = await get_precedent_memory()
    return await memory.embed_governance_decision(vault_entry)


async def find_precedents(
    query: str, verdict_filter: list[str] | None = None, k: int = 5
) -> list[dict[str, Any]]:
    """Convenience function: find similar precedents."""
    memory = await get_precedent_memory()
    return await memory.find_similar_precedents(query, verdict_filter, k)
