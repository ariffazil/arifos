"""
core/enforcement/genius.py — Constitutional Genius & Dial Derivation

This module implements the "Real Scoring" system for arifOS.
It derives the 4 APEX Dials (A/P/X/E) from the 13 Constitutional Floors
via geometric projection (Eigendecomposition approximation).

G = A × P × X × E²

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import math
import logging
from typing import Any

from pydantic import BaseModel, Field
from core.shared.types import FloorScores
from core.shared.floor_audit import AuditResult

logger = logging.getLogger(__name__)

class APEXDials(BaseModel):
    """
    The 4 APEX dials derived from floor scores.
    Each dial represents a dimension of constitutional compliance.
    """
    A: float = Field(ge=0.0, le=1.0, description="Akal: Mind/Clarity cluster (F2, F4, F7, F10)")
    P: float = Field(ge=0.0, le=1.0, description="Presence: Stability/Trust cluster (F1, F5, F11)")
    X: float = Field(ge=0.0, le=1.0, description="Exploration: Heart/Navigation cluster (F3, F6, F8_prev, F9)")
    E: float = Field(ge=0.0, le=1.0, description="Energy: Vitality/Boundary cluster (F12, F13 + Budget)")

    def to_dict(self) -> dict[str, float]:
        return {"A": self.A, "P": self.P, "X": self.X, "E": self.E}


def audit_result_to_floor_scores(audit_result: Any) -> FloorScores:
    """
    Convert a FloorAuditor AuditResult or a raw dict of results to a FloorScores object.
    """
    if isinstance(audit_result, AuditResult):
        results = audit_result.floor_results
    elif isinstance(audit_result, dict):
        # Could be a dict of FloorResult objects or a dict from build_governance_proof
        results = audit_result.get("floor_results", audit_result)
    else:
        return FloorScores()

    def get_score(fid: str, default: float = 1.0) -> float:
        res = results.get(fid)
        if hasattr(res, "score"):
            return res.score
        if isinstance(res, dict) and "score" in res:
            return res["score"]
        # Fallback for simple "pass"/"fail" strings
        if res == "pass": return 1.0
        if res == "fail": return 0.0
        return default

    def get_bool(fid: str, default: bool = True) -> bool:
        res = results.get(fid)
        if hasattr(res, "passed"):
            return res.passed
        if isinstance(res, dict) and "passed" in res:
            return res["passed"]
        if res == "pass": return True
        if res == "fail": return False
        return default

    return FloorScores(
        f1_amanah=get_score("F1"),
        f2_truth=get_score("F2", 0.99),
        f3_tri_witness=get_score("F3", 0.95),
        f4_clarity=get_score("F4", 1.0),
        f5_peace=get_score("F5", 1.0),
        f6_empathy=get_score("F6", 0.95),
        f7_humility=get_score("F7", 0.04),
        f8_genius=get_score("F8", 0.80),
        f9_anti_hantu=1.0 - get_score("F9", 1.0),
        f10_ontology=get_bool("F10"),
        f11_command_auth=get_bool("F11"),
        f12_injection=1.0 - get_score("F12", 1.0),
        f13_sovereign=get_score("F13"),
    )


def geometric_mean(values: list[float]) -> float:
    """
    Compute geometric mean of values.
    Returns 0.0 if any value is <= 0.0 to enforce HARD floor logic.
    """
    if not values:
        return 0.0
    
    # Constitutional Enforcement: If any floor is 0, the cluster is 0.
    if any(v <= 0 for v in values):
        return 0.0
        
    try:
        product = 1.0
        for v in values:
            product *= v
        return product ** (1.0 / len(values))
    except Exception as e:
        logger.error(f"Error calculating geometric mean: {e}")
        return 0.0


def floors_to_dials(
    floors: FloorScores,
    compute_budget_used: float = 0.5,
    compute_budget_max: float = 1.0
) -> APEXDials:
    """
    Project 13 Floors onto 4 Dials (A/P/X/E).
    """
    # 1. Helper to convert bool floors to floats
    f10 = 1.0 if floors.f10_ontology else 0.0
    f11 = 1.0 if floors.f11_command_auth else 0.0
    
    # 2. A = AKAL (Mind/Structure)
    f7_norm = 1.0 if 0.03 <= floors.f7_humility <= 0.05 else (
        1.0 - min(abs(floors.f7_humility - 0.04) * 10, 1.0)
    )
    
    akal = geometric_mean([
        floors.f2_truth,
        floors.f4_clarity,
        f7_norm,
        f10
    ])
    
    # 3. P = PRESENCE (Stability/Trust)
    presence = geometric_mean([
        floors.f1_amanah,
        floors.f5_peace,
        f11
    ])
    
    # 4. X = EXPLORATION (Navigation/Heart)
    anti_hantu_compliance = 1.0 - floors.f9_anti_hantu
    
    exploration = geometric_mean([
        floors.f3_tri_witness,
        floors.f6_empathy,
        floors.f8_genius,
        anti_hantu_compliance
    ])
    
    # 5. E = ENERGY (Vitality/System)
    injection_compliance = 1.0 - floors.f12_injection
    
    energy_from_floors = geometric_mean([
        injection_compliance,
        floors.f13_sovereign
    ])
    
    energy_ratio = 1.0 - (compute_budget_used / max(compute_budget_max, 1e-6))
    energy_ratio = max(0.0, min(1.0, energy_ratio))
    
    energy = (energy_from_floors + energy_ratio) / 2.0
    
    return APEXDials(A=akal, P=presence, X=exploration, E=energy)


def calculate_genius(
    floors: FloorScores,
    h: float = 0.0,
    compute_budget_used: float = 0.5,
    compute_budget_max: float = 1.0
) -> dict[str, Any]:
    """
    The Unified Genius Equation: G = (A × P × X × E²) × (1 - h)
    """
    dials = floors_to_dials(floors, compute_budget_used, compute_budget_max)
    
    akal = dials.A
    presence = dials.P
    exploration = dials.X
    energy = dials.E
    
    base_g = akal * presence * exploration * (energy ** 2)
    G = base_g * (1.0 - h)
    
    return {
        "genius_score": round(G, 4),
        "dials": dials.to_dict(),
        "hysteresis": h,
        "passed": G >= 0.80,
        "verdict": "SEAL" if G >= 0.80 else "PARTIAL" if G >= 0.60 else "VOID"
    }

__all__ = ["APEXDials", "floors_to_dials", "calculate_genius", "audit_result_to_floor_scores"]
