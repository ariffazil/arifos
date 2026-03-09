"""
arifosmcp/runtime/orchestrator.py — The arifOS Metabolic Loop Orchestrator

This module implements the Stage 444 logic, coordinating the 10-tool APEX-G kernel.
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import os
import logging
from typing import Any

from arifosmcp.runtime.models import RuntimeEnvelope, Verdict

logger = logging.getLogger(__name__)


async def metabolic_loop(
    query: str,
    risk_tier: str = "medium",
    actor_id: str = "anonymous",
) -> dict[str, Any]:
    """
    Orchestrate the 10-tool constitutional loop (000-999).
    This function acts as the internal logic for the Stage 444 metabolic_loop_router.
    """
    from arifosmcp.runtime.tools import (
        apex_judge_verdict,
        assess_heart_impact,
        critique_thought_audit,
        init_anchor_state,
        integrate_analyze_reflect,
        quantum_eureka_forge,
        reason_mind_synthesis,
        seal_vault_commit,
    )

    phase2_hooks = {
        "search_reality": os.getenv("ARIFOS_ENABLE_PHASE2_SEARCH", "0") == "1",
        "ingest_evidence": os.getenv("ARIFOS_ENABLE_PHASE2_INGEST", "0") == "1",
    }
    trace = {"phase2_hooks": phase2_hooks}

    # 1. Stage 000: INIT
    init_res: RuntimeEnvelope = await init_anchor_state(
        intent={"query": query, "task_type": "ask"},
        governance={"actor_id": actor_id, "stakes_class": "C"},
    )
    trace["000_INIT"] = init_res.verdict
    if init_res.verdict == Verdict.VOID:
        output = init_res.model_dump()
        output["trace"] = trace
        return output

    session_id = init_res.session_id
    auth_ctx = init_res.auth_context.model_dump()

    # 2. Stage 111: FRAMING
    frame_res: RuntimeEnvelope = await integrate_analyze_reflect(
        session_id=session_id, query=query, auth_context=auth_ctx
    )
    trace["111_MIND"] = frame_res.verdict
    auth_ctx = frame_res.auth_context.model_dump()

    # 3. Stage 333: REASONING
    mind_res: RuntimeEnvelope = await reason_mind_synthesis(
        session_id=session_id, query=query, auth_context=auth_ctx
    )
    trace["333_MIND"] = mind_res.verdict
    auth_ctx = mind_res.auth_context.model_dump()

    # 4. Stage 666A & 666B: HEART & AUDIT
    heart_res: RuntimeEnvelope = await assess_heart_impact(
        session_id=session_id, scenario=query, auth_context=auth_ctx
    )
    trace["666A_HEART"] = heart_res.verdict
    auth_ctx = heart_res.auth_context.model_dump()

    critique_res: RuntimeEnvelope = await critique_thought_audit(
        session_id=session_id, thought_id="current_thought", auth_context=auth_ctx
    )
    trace["666B_HEART"] = critique_res.verdict
    auth_ctx = critique_res.auth_context.model_dump()

    # 5. Stage 777: FORGE (Discovery)
    # Phase 2 hooks are intentionally not dispatched here yet. Future work may
    # allow 777/888 to invoke search_reality / ingest_evidence behind stricter
    # Floors and HOLD-888 gating.
    forge_res: RuntimeEnvelope = await quantum_eureka_forge(
        session_id=session_id, intent=query, auth_context=auth_ctx
    )
    trace["777_APEX"] = forge_res.verdict
    auth_ctx = forge_res.auth_context.model_dump()

    # 6. Stage 888: JUDGE
    # Aggregate verdicts for the candidate
    verdicts = [
        init_res.verdict,
        frame_res.verdict,
        mind_res.verdict,
        heart_res.verdict,
        critique_res.verdict,
    ]
    candidate = Verdict.SEAL
    if Verdict.VOID in verdicts:
        candidate = Verdict.VOID
    elif Verdict.HOLD_888 in verdicts:
        candidate = Verdict.HOLD_888
    elif Verdict.SABAR in verdicts:
        candidate = Verdict.SABAR

    judge_res: RuntimeEnvelope = await apex_judge_verdict(
        session_id=session_id,
        verdict_candidate=candidate.value,
        auth_context=auth_ctx,
        reason_summary=f"Metabolic loop synthesis for: {query[:50]}...",
    )
    trace["888_JUDGE"] = judge_res.verdict
    auth_ctx = judge_res.auth_context.model_dump()

    # 7. Stage 999: VAULT
    vault_res: RuntimeEnvelope = await seal_vault_commit(
        session_id=session_id, verdict=judge_res.verdict.value, auth_context=auth_ctx
    )
    trace["999_VAULT"] = vault_res.verdict

    # Final result construction
    final_output = judge_res.model_dump()
    final_output["trace"] = trace
    final_output["vault_seal"] = vault_res.verdict == Verdict.SEAL

    return final_output
