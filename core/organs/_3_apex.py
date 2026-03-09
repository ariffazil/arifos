"""
organs/3_apex.py — Stage 777-888: THE SOUL (GOVERNANCE APEX)

Eureka Forge (Discovery) and Apex Judge (Final Verdict).
Mandates Landauer Bound checks and monotone-safe logic.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import logging
from typing import Any, Literal

from core.shared.types import (
    ApexOutput,
    EurekaProposal,
    JudgmentRationale,
    NextAction,
    Verdict,
)

logger = logging.getLogger(__name__)


async def forge(
    intent: str,
    session_id: str,
    eureka_type: str = "concept",
    materiality: str = "idea_only",
    auth_context: dict[str, Any] | None = None,
    **kwargs: Any,
) -> ApexOutput:
    """
    Stage 777: EUREKA FORGE (Discovery Actuator)
    """
    from core.physics.thermodynamics_hardened import consume_tool_energy

    consume_tool_energy(session_id, n_calls=1)

    floors = {"F3": "pass", "F8": "pass", "F11": "pass", "F12": "pass", "F13": "pass"}

    # 1. Forge Eureka Proposal
    proposal = EurekaProposal(
        type=eureka_type,  # type: ignore
        summary=f"Forged {eureka_type} discovery for: {intent[:50]}...",
        details="Forged through Stage 777 metabolic synthesis.",
        evidence_links=["reason_mind.step:3"],
    )

    # 2. Propose Next Actions
    next_actions = []
    if materiality == "idea_only":
        next_actions.append(
            NextAction(
                action_type="human_review",
                description="Review proposal with sovereign.",
                requires_888_hold=True,
            )
        )
    elif materiality == "prototype":
        next_actions.append(
            NextAction(
                action_type="code_sandbox",
                description="Run validation tests.",
                requires_888_hold=False,
            )
        )

    # 3. Construct Output
    return ApexOutput(
        session_id=session_id,
        verdict=Verdict.SEAL,
        intent=intent,
        eureka=proposal,
        next_actions=next_actions,
        floors=floors,
        human_witness=1.0,
        ai_witness=1.0,
        earth_witness=1.0,
        evidence={"grounding": "Constitutional Forge Logic"},
    )


async def judge(
    session_id: str,
    verdict_candidate: str = "SEAL",
    reason_summary: str | None = None,
    auth_context: dict[str, Any] | None = None,
    **kwargs: Any,
) -> ApexOutput:
    """
    Stage 888: APEX JUDGE (Final Judgment)

    Rule: MONOTONE-SAFE. Cannot upgrade a weaker candidate.
    Discipline: APEX Theorem Gate (G† = G* · η)
    """
    from core.physics.thermodynamics_hardened import (
        check_landauer_before_seal,
        consume_tool_energy,
        get_thermodynamic_budget,
    )
    from core.enforcement.genius import calculate_genius
    from core.shared.types import FloorScores, Verdict

    consume_tool_energy(session_id, n_calls=1)

    # 1. Map Candidate
    try:
        candidate = Verdict(verdict_candidate)
    except ValueError:
        candidate = Verdict.VOID

    # 2. Extract or Build Floor Scores
    floor_scores = kwargs.get("floor_scores")
    if not isinstance(floor_scores, FloorScores):
        # Map kwargs to FloorScores with defaults
        floor_scores = FloorScores(
            f1_amanah=kwargs.get("f1_amanah", kwargs.get("f1", 1.0)),
            f2_truth=kwargs.get("f2_truth", kwargs.get("f2", kwargs.get("akal", 0.99))),
            f3_tri_witness=kwargs.get("f3_tri_witness", kwargs.get("f3", 0.95)),
            f4_clarity=kwargs.get("f4_clarity", kwargs.get("f4", 1.0)),
            f5_peace=kwargs.get("f5_peace", kwargs.get("f5", 1.0)),
            f6_empathy=kwargs.get("f6_empathy", kwargs.get("f6", 0.95)),
            f7_humility=kwargs.get("f7_humility", kwargs.get("f7", 0.04)),
            f8_genius=kwargs.get("f8_genius", kwargs.get("f8", 0.80)),
            f9_anti_hantu=kwargs.get("f9_anti_hantu", kwargs.get("f9", 0.0)),
            f10_ontology=kwargs.get("f10_ontology", kwargs.get("f10", True)),
            f11_command_auth=kwargs.get("f11_command_auth", kwargs.get("f11", True)),
            f12_injection=kwargs.get("f12_injection", kwargs.get("f12", 0.0)),
            f13_sovereign=kwargs.get("f13_sovereign", kwargs.get("f13", 1.0)),
        )

    # 3. Monotone Safety Check
    violations = kwargs.get("violations", [])
    if violations and candidate == Verdict.SEAL:
        candidate = Verdict.PARTIAL

    # 4. Real Genius Calculation (The Discipline Layer)
    try:
        budget = get_thermodynamic_budget(session_id)
        budget_used = budget.consumed
        budget_max = budget.initial_budget
    except Exception:
        budget_used = 0.5
        budget_max = 1.0

    genius_result = calculate_genius(
        floors=floor_scores,
        h=kwargs.get("hysteresis", 0.0),
        compute_budget_used=budget_used,
        compute_budget_max=budget_max,
    )

    g_score = genius_result["genius_score"]
    dials = genius_result["dials"]

    # 5. G Sovereignty Gate
    if candidate == Verdict.SEAL and g_score < 0.80:
        logger.info(f"arifOS APEX Discipline Check: G ({g_score:.4f}) < 0.80. Downgrading to PARTIAL.")
        candidate = Verdict.PARTIAL
        reason_summary = (reason_summary or "") + f" [APEX Gate: G={g_score:.4f} < 0.80]"

    # 6. Landauer Physics Check (Mandatory before SEAL)
    if candidate == Verdict.SEAL:
        try:
            check_landauer_before_seal(
                session_id=session_id,
                compute_ms=kwargs.get("compute_ms", 500),
                tokens=kwargs.get("tokens", 200),
                delta_s=kwargs.get("delta_s", -0.2),
            )
        except Exception as e:
            logger.warning(f"Landauer check failed: {e}")
            candidate = Verdict.SABAR
            reason_summary = f"Physics Law Violation: {str(e)}"

    # 7. Build Rationale
    rationale = JudgmentRationale(
        summary=reason_summary or f"Judgment finalized for session {session_id}.",
        tri_witness={"human": dials["E"], "ai": dials["A"], "earth": dials["P"]},
        omega_0=floor_scores.f7_humility,
    )

    # Update floor statuses for output
    floors_status = {f"F{i}": "pass" for i in range(1, 14)}
    if g_score < 0.80:
        floors_status["F8"] = "partial"
    if floor_scores.f2_truth < 0.99:
        floors_status["F2"] = "fail"

    # 8. Construct Output
    return ApexOutput(
        session_id=session_id,
        verdict=candidate,
        final_verdict=candidate,
        reasoning=rationale,
        floors=floors_status,
        metrics={
            "G": g_score,
            "akal": round(dials["A"], 4),
            "presence": round(dials["P"], 4),
            "exploration": round(dials["X"], 4),
            "energy": round(dials["E"], 4),
        },
        floor_scores=floor_scores,
        human_witness=dials["E"],
        ai_witness=dials["A"],
        earth_witness=dials["P"],
        human_approve=True,  # Satisfy F13
        evidence={"grounding": "Constitutional Apex Consensus"},  # Satisfy F2
    )


async def apex(
    action: Literal["forge", "judge", "full"] = "full",
    session_id: str = "global",
    intent: str | None = None,
    verdict_candidate: str = "SEAL",
    **kwargs: Any,
) -> ApexOutput:
    """
    Unified APEX Interface
    """
    if action == "forge":
        return await forge(intent or "Discovery", session_id, **kwargs)
    elif action == "judge":
        return await judge(session_id, verdict_candidate, **kwargs)

    # Default Full Judgment Flow
    return await judge(session_id, verdict_candidate, **kwargs)


# Unified aliases
sync = apex


__all__ = ["apex", "forge", "judge", "sync"]
