"""
arifosmcp.core - Core system components.

This module contains the foundational components of the arifOS system:
- floors: F1-F13 metabolic loop implementation
- constitution: Canon-13 constitutional validation
- merkle: Merkle chain for provenance verification
"""

from .floors import (
    Floor,
    FloorRegistry,
    MetabolicLoop,
    F1_AnchorFloor,
    F2_QueryFloor,
    F3_ExploreFloor,
    F4_MetabolizeFloor,
    F5_SynthesizeFloor,
    F6_CalculateFloor,
    F7_ConstituteFloor,
    F8_RatifyFloor,
    F9_SealFloor,
    F10_PersistFloor,
    F11_ReportFloor,
    F12_MonitorFloor,
    F13_CloseFloor,
)

from .constitution import (
    Canon13Constitution,
    ConstitutionalValidator,
    ArticleViolation,
)

from .merkle import (
    MerkleNode,
    MerkleTree,
    MerkleChain,
)

__all__ = [
    # Floors
    "Floor",
    "FloorRegistry",
    "MetabolicLoop",
    "F1_AnchorFloor",
    "F2_QueryFloor",
    "F3_ExploreFloor",
    "F4_MetabolizeFloor",
    "F5_SynthesizeFloor",
    "F6_CalculateFloor",
    "F7_ConstituteFloor",
    "F8_RatifyFloor",
    "F9_SealFloor",
    "F10_PersistFloor",
    "F11_ReportFloor",
    "F12_MonitorFloor",
    "F13_CloseFloor",
    # Constitution
    "Canon13Constitution",
    "ConstitutionalValidator",
    "ArticleViolation",
    # Merkle
    "MerkleNode",
    "MerkleTree",
    "MerkleChain",
]
