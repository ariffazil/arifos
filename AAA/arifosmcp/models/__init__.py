"""
arifosmcp.models - Pydantic models for the Canon-13 Regime.

This module contains all data models used across the arifOS MCP architecture,
including MGI envelopes, 3E cycle structures, and verdict enumerations.
"""

from .mgi import (
    MachineLayer,
    GovernanceLayer,
    IntelligenceLayer,
    MGIEnvelope,
    MGIBaseResponse,
)

from .cycle3e import (
    ExplorationPhase,
    EntropyPhase,
    EurekaPhase,
    Cycle3E,
    EvidenceBundle,
    SourceAttribution,
)

from .verdicts import (
    VerdictState,
    FloorState,
    SealType,
    ThermodynamicBudget,
)

__all__ = [
    # MGI Envelope
    "MachineLayer",
    "GovernanceLayer",
    "IntelligenceLayer",
    "MGIEnvelope",
    "MGIBaseResponse",
    # 3E Cycle
    "ExplorationPhase",
    "EntropyPhase",
    "EurekaPhase",
    "Cycle3E",
    "EvidenceBundle",
    "SourceAttribution",
    # Verdicts
    "VerdictState",
    "FloorState",
    "SealType",
    "ThermodynamicBudget",
]
