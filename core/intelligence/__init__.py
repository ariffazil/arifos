"""
core/intelligence/__init__.py — arifOS Intelligence Layer

3E Intelligence Architecture:
- Exploration: Gather candidate interpretations and hypotheses
- Entropy: Measure and metabolize uncertainty
- Eureka: Collapse confusion into coherent, decision-ready form

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from .vector_bridge import (
    QdrantVectorBridge,
    VectorEntry,
    IngestionResult,
    qdrant_bridge,
    vector_memory_embedding,
    vector_memory_search,
    ingest_from_evidence_bundle,
)

__all__ = [
    "QdrantVectorBridge",
    "VectorEntry",
    "IngestionResult",
    "qdrant_bridge",
    "vector_memory_embedding",
    "vector_memory_search",
    "ingest_from_evidence_bundle",
]
