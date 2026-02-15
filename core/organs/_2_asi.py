from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.shared.physics import (
    ConstitutionalTensor,
    Peace2,
    PeaceSquared,
    Stakeholder,
    identify_stakeholders,
    kappa_r,
)
from core.shared.types import AsiOutput, FloorScores, Verdict
from core.asi.sbert_floors import classify_asi_floors, SbertFloorScores


async def empathize(
    query: str, agi_tensor: ConstitutionalTensor, session_id: str, context: Optional[str] = None
) -> AsiOutput:
    sbert_scores = classify_asi_floors(query)
    stakeholders = identify_stakeholders(query, context=context)
    
    # Use SBERT for F5, F6, F9
    f5_peace_score = sbert_scores.f5_peace
    f6_empathy_score = sbert_scores.f6_empathy
    f9_anti_hantu_score = sbert_scores.f9_anti_hantu
    
    # Peace2 expects Dict[str, float] based on perceived harms
    # For simplicity, map SBERT-based peace score to stakeholder harms
    harms = {s.name: (1.0 - f5_peace_score) for s in stakeholders}
    peace_obj = Peace2(harms)
    
    weakest = (
        min(stakeholders, key=lambda s: s.vulnerability_score)
        if stakeholders
        else Stakeholder("System", 1.0) # Assume 1.0 for now
    )
    care_recs = [f"Monitor impact on {s.name}" for s in stakeholders if s.vulnerability_score < 0.5]
    
    return AsiOutput(
        session_id=session_id,
        floor_scores=FloorScores(f5_peace=f5_peace_score, f6_empathy=f6_empathy_score, f9_anti_hantu=f9_anti_hantu_score),
        verdict=Verdict.SEAL, # Default to SEAL, align() will change if violations
        stakeholder_impact={s.name: s.vulnerability_score for s in stakeholders},
        metrics={
            "stage": 555,
            "action": "empathize",
            "weakest": weakest.name,
            "recommendations": care_recs,
            "sbert_confidence": sbert_scores.confidence,
            "sbert_method": sbert_scores.method,
        },
    )


async def align(
    query: str, empathy_output: Any, agi_tensor: ConstitutionalTensor, session_id: str
) -> AsiOutput:
    emp_data = (
        empathy_output.model_dump() if hasattr(empathy_output, "model_dump") else empathy_output
    )
    
    # Use SBERT scores from empathize output, or re-classify if not present
    if "sbert_method" in emp_data.get("metrics", {}):
        f5_peace_score = emp_data["floor_scores"]["f5_peace"]
        f6_empathy_score = emp_data["floor_scores"]["f6_empathy"]
        f9_anti_hantu_score = emp_data["floor_scores"]["f9_anti_hantu"]
    else:
        # Fallback: re-classify if SBERT scores weren't propagated from empathize
        sbert_scores = classify_asi_floors(query)
        f5_peace_score = sbert_scores.f5_peace
        f6_empathy_score = sbert_scores.f6_empathy
        f9_anti_hantu_score = sbert_scores.f9_anti_hantu
    
    stakeholders = emp_data.get("stakeholder_impact", {})
    is_reversible = not any(
        word in query.lower() for word in ["delete", "remove", "wipe", "format", "reset"]
    )

    harms = {name: (1.0 - f5_peace_score) for name in stakeholders}
    p2_score = Peace2(harms).P2()

    violations = []
    if not is_reversible:
        violations.append("F1_AMANAH_LOW_REVERSIBILITY")
    if f5_peace_score < 0.5: # F5 Peace² violation threshold
        violations.append("F5_PEACE_UNSTABLE")
    if f6_empathy_score < 0.5: # F6 Empathy violation threshold
        violations.append("F6_EMPATHY_LOW")
    if f9_anti_hantu_score < 0.5: # F9 Anti-Hantu violation threshold
        violations.append("F9_ANTI_HANTU_VIOLATION")

    # HARD floor violations = VOID, not SABAR
    hard_violations = [
        v for v in violations if v.startswith(("F1_", "F6_", "F9_", "F10_", "F11_", "F12_")) # Added F9
    ]
    if hard_violations:
        verdict_str = "VOID"
    elif violations:
        verdict_str = "SABAR"
    else:
        verdict_str = "SEAL"
    stakeholder_harms = {
        name: (1.0 - score) if score < 0.5 else 0.0 for name, score in stakeholders.items()
    }
    return AsiOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f1_amanah=1.0 if is_reversible else 0.0,
            f5_peace=f5_peace_score,
            f6_empathy=f6_empathy_score,
            f9_anti_hantu=f9_anti_hantu_score, # Use SBERT F9 score
        ),
        verdict=Verdict(verdict_str),
        violations=violations,
        stakeholder_impact=stakeholder_harms,
        metrics={
            "stage": 666,
            "action": "align",
            "is_reversible": is_reversible,
            "sbert_confidence": emp_data.get("metrics", {}).get("sbert_confidence", sbert_scores.confidence), # Propagate or use new
            "sbert_method": emp_data.get("metrics", {}).get("sbert_method", sbert_scores.method), # Propagate or use new
        },
    )


async def asi(
    action: str, agi_tensor: ConstitutionalTensor, session_id: str, query: str = ""
) -> Any:
    if action == "empathize":
        return await empathize(query, agi_tensor, session_id)
    elif action == "align":
        emp_out = await empathize(query, agi_tensor, session_id)
        return await align(query, emp_out, agi_tensor, session_id)
    elif action == "full":
        emp_res = await empathize(query, agi_tensor, session_id)
        return await align(query, emp_res, agi_tensor, session_id)
    else:
        raise ValueError(f"Unknown: {action}")
