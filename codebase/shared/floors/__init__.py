"""
codebase/floors/__init__.py
Constitutional Floor Modules (F1-F13)
v55.5: Exports Canonical Floors, Metrics, and Eigendecomposition
"""

# Genius Calculator with Eigendecomposition (v55.5)
from codebase.floors.genius import (
    GeniusCalculator,
    GeniusMetrics,
    FloorScores,
    extract_dials,
    Verdict,
    OntologyLock,
)

# F1: Amanah (Sacred Trust)
from codebase.floors.amanah import F1_Amanah, AmanahCovenant

# F10: Ontology (Category Lock)
from codebase.floors.ontology import F10_OntologyGate, OntologyResult

# F12: Injection Defense
from codebase.floors.injection import F12_InjectionDefense, InjectionDefenseResult

# F11: Command Authority
from codebase.floors.authority import AuthorityVerifier, verify_authority

# Floor Registry for health checks
class FloorRegistry:
    """Registry of all constitutional floors F1-F13."""
    
    _floors = {
        1: "F1_Amanah",
        2: "F2_Truth",
        3: "F3_TriWitness",
        4: "F4_Clarity",
        5: "F5_Equilibrium",
        6: "F6_AntiPollution",
        7: "F7_Humility",
        8: "F8_Genius",
        9: "F9_AntiClever",
        10: "F10_Ontology",
        11: "F11_Command",
        12: "F12_Injection",
        13: "F13_Sovereign",
    }
    
    @classmethod
    def list_floors(cls) -> list:
        """Return list of all floor names."""
        return list(cls._floors.values())
    
    @classmethod
    def get_floor(cls, number: int) -> str:
        """Get floor name by number."""
        return cls._floors.get(number, "Unknown")


__all__ = [
    # Genius with Eigendecomposition
    "GeniusCalculator",
    "GeniusMetrics",
    "FloorScores",
    "extract_dials",
    "Verdict",
    "OntologyLock",
    # F1
    "F1_Amanah",
    "AmanahCovenant",
    # F10
    "F10_OntologyGate",
    "OntologyResult",
    # F12
    "F12_InjectionDefense",
    "InjectionDefenseResult",
    # F11
    "AuthorityVerifier",
    "verify_authority",
    # Registry
    "FloorRegistry",
]
