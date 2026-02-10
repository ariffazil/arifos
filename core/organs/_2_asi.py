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


async def empathize(query: str, agi_tensor: ConstitutionalTensor, session_id: str) -> AsiOutput:
    stakeholders = identify_stakeholders(query)
    # Peace2 expects Dict[str, float]
    harms = {s.name: (1.0 - agi_tensor.truth_score) for s in stakeholders}
    peace_obj = Peace2(harms)
    kappa = kappa_r(query, stakeholders)  # Fixed: requires query and stakeholders
    weakest = (
        min(stakeholders, key=lambda s: s.vulnerability_score)
        if stakeholders
        else Stakeholder("System", 1.0)
    )
    care_recs = [f"Monitor impact on {s.name}" for s in stakeholders if s.vulnerability_score < 0.5]
    return AsiOutput(
        session_id=session_id,
        floor_scores=FloorScores(f5_peace=peace_obj.P2(), f6_empathy=kappa),
        verdict=Verdict.SEAL,
        stakeholder_impact={s.name: s.vulnerability_score for s in stakeholders},
        metrics={
            "stage": 555,
            "action": "empathize",
            "weakest": weakest.name,
            "recommendations": care_recs,
        },
    )


async def align(
    query: str, empathy_output: Any, agi_tensor: ConstitutionalTensor, session_id: str
) -> AsiOutput:
    emp_data = (
        empathy_output.model_dump() if hasattr(empathy_output, "model_dump") else empathy_output
    )
    kappa = emp_data.get("floor_scores", {}).get("f6_empathy", 0.0)
    stakeholders = emp_data.get("stakeholder_impact", {})
    is_reversible = not any(
        word in query.lower() for word in ["delete", "remove", "wipe", "format", "reset"]
    )

    harms = {name: (1.0 - agi_tensor.truth_score) for name in stakeholders}
    p2_score = Peace2(harms).P2()

    violations = []
    if not is_reversible:
        violations.append("F1_AMANAH_LOW_REVERSIBILITY")
    if p2_score < 1.0:
        violations.append("F5_PEACE_UNSTABLE")
    if kappa < 0.70:
        violations.append("F6_EMPATHY_LOW")
    verdict_str = "SEAL" if not violations else "SABAR"
    stakeholder_harms = {
        name: (1.0 - score) if score < 0.5 else 0.0 for name, score in stakeholders.items()
    }
    return AsiOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f1_amanah=1.0 if is_reversible else 0.0, f5_peace=p2_score, f6_empathy=kappa
        ),
        verdict=Verdict(verdict_str),
        violations=violations,
        stakeholder_impact=stakeholder_harms,
        metrics={"stage": 666, "action": "align", "is_reversible": is_reversible},
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
