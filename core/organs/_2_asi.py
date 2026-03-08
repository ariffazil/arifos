"""
core/organs/_2_asi.py — The Heart (Stage 555-666)

ASI Engine: Empathy, Stakeholder Care, Peace Preservation with ST Integration

DOMAIN ISOLATION (P2):
    - ASI handles EMPATHY, STAKEHOLDERS, HARM only
    - ASI does NOT assess truth (F2) — that's AGI
    - ASI does NOT issue final verdicts — that's APEX
    - ASI passes care assessment to APEX for synthesis

Floors:
    F5: Peace² (stability)
    F6: Empathy (κᵣ ≥ 0.95)
    F9: Anti-Hantu (no consciousness claims)

QT QUAD INTEGRATION:
    - Extracts stakeholders from ST Synthesis tags
    - Populates stakeholders[] from "stakeholder:{name}" tags
    - Calculates κᵣ with quantum uncertainty
"""

from __future__ import annotations

from typing import Any

from core.shared.physics import (
    ConstitutionalTensor,
    Peace2,
    Stakeholder,
    # QT Quad Integration (NEW)
    extract_stakeholders_from_tags,
    harm_score,
    identify_stakeholders,
    kappa_r,
)
from core.shared.sbert_floors import classify_asi_floors
from core.shared.types import AsiOutput, FloorScores, Verdict

# ═══════════════════════════════════════════════════════
# P2 HARDENING: Domain Isolation Enforcement
# ═══════════════════════════════════════════════════════


class AsiDomainViolation(Exception):
    """P2: ASI attempted to operate outside its domain (Heart only)."""

    pass


def enforce_asi_domain(action_type: str) -> None:
    """
    P2 HARDENING: ASI domain isolation.

    ASI (Heart) is restricted to:
    - Empathy, stakeholder impact
    - Peace preservation
    - Harm assessment

    ASI is NOT allowed to:
    - Assess truth (F2) — that's AGI
    - Evaluate evidence — that's AGI
    - Issue final verdicts — that's APEX
    """
    AGI_FUNCTIONS = ["truth", "evidence", "reason", "logic", "ground"]
    APEX_FUNCTIONS = ["judge", "verdict", "seal", "forge", "audit", "sync"]

    action_lower = action_type.lower()

    for func in AGI_FUNCTIONS:
        if func in action_lower:
            raise AsiDomainViolation(
                f"ASI_DOMAIN_VIOLATION: ASI attempted AGI function '{action_type}'. "
                f"Heart cannot assess truth/evidence. Pass to AGI (Mind)."
            )

    for func in APEX_FUNCTIONS:
        if func in action_lower:
            raise AsiDomainViolation(
                f"ASI_DOMAIN_VIOLATION: ASI attempted APEX function '{action_type}'. "
                f"Heart cannot issue verdicts. Pass to APEX (Soul)."
            )


async def empathize(
    query: str, agi_tensor: ConstitutionalTensor, session_id: str, context: str | None = None
) -> AsiOutput:
    sbert_scores = classify_asi_floors(query)
    
    # ═══════════════════════════════════════════════════════════════════
    # QT QUAD: Extract stakeholders from ST thought chain
    # ═══════════════════════════════════════════════════════════════════
    
    # Try to get ST chain from AGI tensor
    st_stakeholders: list[Stakeholder] = []
    if hasattr(agi_tensor, "st_chain") and agi_tensor.st_chain:
        st_stakeholders = extract_stakeholders_from_tags(agi_tensor.st_chain)
    
    # Fallback: heuristic stakeholder detection
    heuristic_stakeholders = identify_stakeholders(query, context=context)
    
    # Merge: ST stakeholders take precedence, heuristic fills gaps
    stakeholder_map = {s.name: s for s in st_stakeholders}
    for s in heuristic_stakeholders:
        if s.name not in stakeholder_map:
            stakeholder_map[s.name] = s
    
    stakeholders = list(stakeholder_map.values())
    
    # Ensure minimum stakeholders (prevent empty list)
    if len(stakeholders) < 2:
        stakeholders.extend([
            Stakeholder("User", "user", 0.3),
            Stakeholder("System", "system", 0.1),
        ])

    # Use SBERT for F6, F9; compute F5 from harm score
    f6_empathy_score = sbert_scores.f6_empathy
    f9_anti_hantu_score = sbert_scores.f9_anti_hantu
    
    # QT QUAD: Calculate κᵣ with full stakeholder list
    kappa_r_score = kappa_r(query, stakeholders)
    # Blend SBERT and κᵣ for final F6
    f6_empathy_score = max(f6_empathy_score, kappa_r_score)

    # Compute harm score based on similarity to harm archetypes
    query_harm = harm_score(query)
    # Map harm to stakeholders weighted by vulnerability
    harms = {s.name: query_harm * s.vulnerability_score for s in stakeholders}
    peace_obj = Peace2(harms)
    f5_peace_score = peace_obj.P2()

    weakest = (
        min(stakeholders, key=lambda s: s.vulnerability_score)
        if stakeholders
        else Stakeholder("System", "system", 1.0)
    )
    care_recs = [f"Monitor impact on {s.name}" for s in stakeholders if s.vulnerability_score < 0.5]

    return AsiOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f5_peace=f5_peace_score, f6_empathy=f6_empathy_score, f9_anti_hantu=f9_anti_hantu_score
        ),
        verdict=Verdict.SEAL,  # Default to SEAL, align() will change if violations
        stakeholder_impact={s.name: s.vulnerability_score for s in stakeholders},
        metrics={
            "stage": 555,
            "action": "empathize",
            "weakest": weakest.name,
            "recommendations": care_recs,
            "sbert_confidence": sbert_scores.confidence,
            "sbert_method": sbert_scores.method,
            # QT Quad additions
            "stakeholder_count": len(stakeholders),
            "stakeholder_sources": ["st_chain" if s in st_stakeholders else "heuristic" for s in stakeholders],
            "kappa_r": kappa_r_score,
        },
    )


async def align(
    query: str, empathy_output: Any, agi_tensor: ConstitutionalTensor, session_id: str
) -> AsiOutput:
    emp_data = (
        empathy_output.model_dump() if hasattr(empathy_output, "model_dump") else empathy_output
    )

    # Use SBERT scores from empathize output, or re-classify if not present
    sbert_scores = None
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
    # Determine confidence and method for metrics
    if sbert_scores is not None:
        sbert_confidence = sbert_scores.confidence
        sbert_method = sbert_scores.method
    else:
        sbert_confidence = emp_data.get("metrics", {}).get("sbert_confidence", 0.5)
        sbert_method = emp_data.get("metrics", {}).get("sbert_method", "unknown")

    stakeholders = emp_data.get("stakeholder_impact", {})
    is_reversible = not any(
        word in query.lower() for word in ["delete", "remove", "wipe", "format", "reset"]
    )

    query_harm = harm_score(query)
    harms = {name: query_harm * score for name, score in stakeholders.items()}

    violations = []
    if not is_reversible:
        violations.append("F1_AMANAH_LOW_REVERSIBILITY")
    if f5_peace_score < 0.5:  # F5 Peace² violation threshold
        violations.append("F5_PEACE_UNSTABLE")
    if f6_empathy_score < 0.5:  # F6 Empathy violation threshold
        violations.append("F6_EMPATHY_LOW")
    if f9_anti_hantu_score < 0.5:  # F9 Anti-Hantu violation threshold
        violations.append("F9_ANTI_HANTU_VIOLATION")

    # HARD floor violations = VOID, not SABAR
    hard_violations = [
        v
        for v in violations
        if v.startswith(("F1_", "F6_", "F9_", "F10_", "F11_", "F12_"))  # Added F9
    ]
    if hard_violations:
        verdict_str = "VOID"
    elif violations:
        verdict_str = "SABAR"
    else:
        verdict_str = "SEAL"
    stakeholder_harms = harms
    return AsiOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f1_amanah=1.0 if is_reversible else 0.0,
            f5_peace=f5_peace_score,
            f6_empathy=f6_empathy_score,
            f9_anti_hantu=f9_anti_hantu_score,  # Use SBERT F9 score
        ),
        verdict=Verdict(verdict_str),
        violations=violations,
        stakeholder_impact=stakeholder_harms,
        metrics={
            "stage": 666,
            "action": "align",
            "is_reversible": is_reversible,
            "sbert_confidence": sbert_confidence,
            "sbert_method": sbert_method,
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
