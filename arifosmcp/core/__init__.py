"""
arifosmcp.core - Core system components.

This module contains the foundational components of the arifOS system:
- ontology: Unified terminology and ontology definitions
- merkle: Merkle chain for provenance verification
"""

from .ontology import (
    TrinityEngine,
    MetabolicStage,
    ConstitutionalFloor,
    VerdictState,
    OntologyRegistry,
)

from .merkle import (
    MerkleNode,
    MerkleTree,
    MerkleChain,
)

__all__ = [
    # Ontology
    "TrinityEngine",
    "MetabolicStage", 
    "ConstitutionalFloor",
    "VerdictState",
    "OntologyRegistry",
    # Merkle
    "MerkleNode",
    "MerkleTree",
    "MerkleChain",
]
