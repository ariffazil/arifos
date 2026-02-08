"""
codebase/constants.py — Constitutional Floor Thresholds

This module provides the canonical threshold values for constitutional floors.
Source: 000_THEORY/000_LAW.md and constitutional_floors.py

DITEMPA BUKAN DIBERI
"""

from codebase.constitutional_floors import THRESHOLDS

# Floor Thresholds (Canonical - Imported from SSOT)
TRUTH_THRESHOLD = THRESHOLDS["F2_Truth"]["threshold"]
DELTA_S_THRESHOLD = THRESHOLDS["F4_Clarity"]["threshold"]
PEACE_SQUARED_THRESHOLD = THRESHOLDS["F5_Peace2"]["threshold"]
KAPPA_R_THRESHOLD = THRESHOLDS["F6_Empathy"]["threshold"]
OMEGA_0_MIN = THRESHOLDS["F7_Humility"]["range"][0]
OMEGA_0_MAX = THRESHOLDS["F7_Humility"]["range"][1]
TRI_WITNESS_THRESHOLD = THRESHOLDS["F3_TriWitness"]["threshold"]
GENIUS_THRESHOLD = THRESHOLDS["F8_Genius"]["threshold"]
DARK_CLEVERNESS_CEILING = THRESHOLDS["F9_AntiHantu"]["threshold"]
INJECTION_THRESHOLD = THRESHOLDS["F12_Injection"]["threshold"]
AUTH_STRICTNESS = THRESHOLDS["F11_CommandAuth"]["threshold"]
ONTOLOGY_SCORE = THRESHOLDS["F10_Ontology"]["threshold"]
CURIOSITY_MIN_PATHS = 3         # F13: Minimum explored paths

# Floor Types
# HARD: Must pass or VOID/SABAR
# SOFT: Warning/PARTIAL if failed
# DERIVED: Calculated from other metrics
FLOOR_TYPES = {
    key.split("_")[0]: val["type"] 
    for key, val in THRESHOLDS.items()
}
# Ensure F13 is present if not in THRESHOLDS main dict yet
if "F13" not in FLOOR_TYPES:
    FLOOR_TYPES["F13"] = "SOFT"


def get_lane_truth_threshold(lane: str = "SOFT") -> float:
    """
    Get truth threshold for a specific lane.
    
    Args:
        lane: Governance lane ("HARD" or "SOFT")
        
    Returns:
        Truth threshold for the lane
    """
    # HARD lane requires higher truth
    if lane.upper() == "HARD":
        return TRUTH_THRESHOLD  # 0.99
    else:
        return 0.90  # SOFT lane allows 90% truth


# Dataclass for floors verdict (simplified version)
class FloorsVerdict:
    """Result of floor checking."""
    
    def __init__(self, verdict: str, passed_floors: list, failed_floors: list, reason: str = ""):
        self.verdict = verdict
        self.passed_floors = passed_floors
        self.failed_floors = failed_floors
        self.reason = reason
        self.all_passed = len(failed_floors) == 0
