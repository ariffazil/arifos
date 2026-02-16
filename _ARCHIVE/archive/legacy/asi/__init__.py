"""
arifOS ASI Module - v53.4.0 HARDENED

Unified Heart Engine with 3-Trinity Architecture:
- Trinity I (Self): Empathy Flow (κᵣ), Bias Mirror, Reversibility (F1)
- Trinity II (System): Power-Care (Peace²), Accountability Loop, Consent (F11)
- Trinity III (Society): Stakeholder Protection, Thermodynamic Justice, Ecology

Fractal Geometry: Self-similar stakeholder recursion
Ω = κᵣ · Peace² · Justice

Exports:
- ASIEngineHardened: Main hardened ASI engine
- OmegaBundle: ASI output structure
- TrinitySelf, TrinitySystem, TrinitySociety: Individual Trinity components
- Stakeholder: Stakeholder representation

DITEMPA BUKAN DIBERI
"""

# v55.5: Consolidated - all hardened exports now from engine.py
from .engine import (
    ASIEngineHardened,
    ASIEngine,
    OmegaBundle,
    EmpathyFlow,
    SystemIntegrity,
    SocietalImpact,
    Stakeholder,
    TrinitySelf,
    TrinitySystem,
    TrinitySociety,
    EngineVote,
    StakeholderType,
    execute_asi_hardened,
    execute_asi,
    cleanup_expired_sessions,
    get_asi_engine,
)

__version__ = "v53.4.0-HARDENED"
__all__ = [
    "ASIEngineHardened",
    "ASIEngine",
    "OmegaBundle",
    "EmpathyFlow",
    "SystemIntegrity",
    "SocietalImpact",
    "Stakeholder",
    "TrinitySelf",
    "TrinitySystem",
    "TrinitySociety",
    "EngineVote",
    "StakeholderType",
    "execute_asi_hardened",
    "execute_asi",
]
