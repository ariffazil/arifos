"""
codebase/floors/__init__.py
Constitutional Floor Modules (F1-F13)
v55.1: Exports Canonical Floors, Metrics, and Eigendecomposition
"""

# Genius Calculator with Eigendecomposition (v55.1)
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

__all__ = [
    # Genius with Eigendecomposition
    "GeniusCalculator",
    "GeniusMetrics",
    "FloorScores",  # NEW: 13 floor measurements
    "extract_dials",  # NEW: floor → dial projection
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
]
