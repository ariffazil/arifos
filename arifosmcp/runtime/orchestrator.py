"""
arifosmcp/runtime/orchestrator.py — The arifOS Metabolic Loop Orchestrator

This module implements the Stage 444 logic, coordinating the 10-tool APEX-G kernel.
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import asyncio
import logging
import os
from typing import Any

from arifosmcp.runtime.models import RuntimeEnvelope, Verdict

logger = logging.getLogger(__name__)


async def metabolic_loop(
    query: str,
    risk_tier: str = "medium",
    actor_id: str = "anonymous",
    session_id: str | None = None,
    allow_execution: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Orchestrate the 10-tool constitutional loop (000-999).
    This function acts as the internal logic for the Stage 444 metabolic_loop_router.
    """
    from arifosmcp.runtime.tools import (
        _normalize_session_id,
        apex_judge_verdict,
        assess_heart_impact,
        critique_thought_audit,
        init_anchor_state,
        integrate_analyze_reflect,
        quantum_eureka_forge,
        reason_mind_synthesis,
        seal_vault_commit,
    )
    from arifosmcp.transport.server import _adapt_human_command

    # Apply Human Command Adapter (Repair Directive Priority 2)
    query = _adapt_human_command(query)

    phase2_hooks = {
        "search_reality": os.getenv("ARIFOS_ENABLE_PHASE2_SEARCH", "0") == "1",
        "ingest_evidence": os.getenv("ARIFOS_ENABLE_PHASE2_INGEST", "0") == "1",
    }
    trace: dict[str, Any] = {"phase2_hooks": phase2_hooks}
    reality_summary: dict[str, Any] = {
        "required": False,
        "executed": False,
        "status": "SKIPPED",
        "score": 0.0,
        "results_count": 0,
        "needs_check": False,
    }

    # Resolve/Mint Session (Repair Directive Priority 1 & 3)
    effective_session_id = _normalize_session_id(session_id)

    # P5: Improved Ergonomics (Coercion)
    from core.organs._0_init import coerce_authority_level, coerce_stakes_class

    auth_coerced = coerce_authority_level(actor_id)
    stakes_coerced = coerce_stakes_class(risk_tier)

    actor_id = auth_coerced["value"]
    effective_risk_tier = stakes_coerced["value"]
    authority_level = {
        "user": "human",
        "agent": "agent",
        "system": "system",
        "anonymous": "anonymous",
        "operator": "operator",
        "sovereign": "sovereign",
    }.get(actor_id, "anonymous")

    # 1. Stage 000: INIT (Auto-Anchor for low-risk)
    init_res: RuntimeEnvelope = await init_anchor_state(
        intent={"query": query, "task_type": "ask"},
        governance={
            "actor_id": actor_id,
            "authority_level": authority_level,
            "stakes_class": effective_risk_tier,
        },
        session_id=effective_session_id,
    )
    trace["000_INIT"] = init_res.verdict.value

    # SHADOW EVALUATION & AUTO-ANCHOR (P0):
    init_failed = init_res.verdict == Verdict.VOID
    auth_ctx = init_res.auth_context.model_dump(exclude_none=True)

    auth_state = init_res.auth_state

    if init_failed and effective_risk_tier == "C" and not allow_execution:
        # F11 Auto-Anchor Bypass for low-risk reads (P0)
        from core.enforcement.auth_continuity import mint_auth_context

        logger.info(f"[arifOS] Auto-anchoring low-risk read-only session: {effective_session_id}")

        # Mint a guest context so subsequent tools can pass the bridge
        guest_ctx = mint_auth_context(
            session_id=effective_session_id,
            actor_id="anonymous",
            token_fingerprint="guest-auto-anchor",
            approval_scope=["reason_mind", "simulate_heart", "critique_thought"],
            parent_signature="AUTO_ANCHOR_BYPASS",
        )
        auth_ctx = guest_ctx
        auth_state = "bootstrap_readonly"
        trace["000_INIT"] = "AUTO_ANCHOR"

    # Invariant: Maintain consistency for shadow evaluation
    if not (init_failed and trace["000_INIT"] == "AUTO_ANCHOR"):
        session_id = init_res.session_id
    else:
        session_id = effective_session_id

    # 2. Stage 111: FRAMING
    frame_res: RuntimeEnvelope = await integrate_analyze_reflect(
        session_id=session_id, query=query, auth_context=auth_ctx
    )
    trace["111_MIND"] = frame_res.verdict.value
    auth_ctx = frame_res.auth_context.model_dump(exclude_none=True)

    # 3. Stage 333: REASONING
    mind_res: RuntimeEnvelope = await reason_mind_synthesis(
        session_id=session_id, query=query, auth_context=auth_ctx
    )
    trace["333_MIND"] = mind_res.verdict.value
    auth_ctx = mind_res.auth_context.model_dump(exclude_none=True)

    # 3.5 Stage 222: REALITY VERIFICATION (Epistemic grounding)
    reality_gate_verdict = Verdict.SEAL
    reality_required_tiers = {
        token.strip().upper()
        for token in os.getenv("ARIFOS_REALITY_REQUIRED_TIERS", "A,B").split(",")
        if token.strip()
    }
    reality_required = effective_risk_tier in reality_required_tiers
    reality_summary["required"] = reality_required

    if phase2_hooks["search_reality"] or reality_required:
        from arifosmcp.intelligence.tools.reality_grounding import (
            reality_check,
            should_reality_check,
        )

        needs_check, check_reason = should_reality_check(query)
        reality_summary["needs_check"] = needs_check
        reality_summary["check_reason"] = check_reason
        reality_timeout = float(os.getenv("ARIFOS_REALITY_TIMEOUT_SECONDS", "20"))

        try:
            reality_res = await asyncio.wait_for(
                reality_check(query=query, max_results=5, fetch_sources=False),
                timeout=reality_timeout,
            )
            results_count = int(reality_res.get("results_count", 0))
            uncertainty = float(reality_res.get("uncertainty_aggregate", 1.0))
            status = str(reality_res.get("status", "UNKNOWN"))

            score = (
                min(results_count, 5) / 5.0 * 0.5
                + max(0.0, 1.0 - min(1.0, uncertainty)) * 0.3
                + (0.2 if status.upper() == "OK" else 0.0)
            )
            score = max(0.0, min(1.0, score))

            reality_summary.update(
                {
                    "executed": True,
                    "status": status,
                    "score": score,
                    "results_count": results_count,
                    "uncertainty": uncertainty,
                    "engines_used": reality_res.get("engines_used", []),
                    "engines_failed": reality_res.get("engines_failed", []),
                }
            )

            if reality_required and (results_count == 0 or score < 0.40):
                reality_gate_verdict = Verdict.PARTIAL
                reality_summary["gate_reason"] = "insufficient_grounding"
        except Exception as exc:
            reality_gate_verdict = Verdict.PARTIAL if reality_required else Verdict.SEAL
            reality_summary.update(
                {
                    "executed": True,
                    "status": "ERROR",
                    "score": 0.0,
                    "gate_reason": "reality_stage_error",
                    "error": str(exc),
                }
            )

    trace["222_REALITY"] = {
        "required": reality_summary["required"],
        "status": reality_summary["status"],
        "score": reality_summary["score"],
        "results_count": reality_summary["results_count"],
        "gate_verdict": reality_gate_verdict.value,
    }

    # 4. Stage 666A & 666B: HEART & AUDIT
    # Run in parallel from the same authenticated context, then continue with
    # a deterministic merged context for downstream stages.
    parallel_timeout_seconds = float(os.getenv("ARIFOS_PARALLEL_STAGE_TIMEOUT", "30"))
    parallel_failed = False
    heart_res: RuntimeEnvelope | None = None
    critique_res: RuntimeEnvelope | None = None
    try:
        heart_res, critique_res = await asyncio.wait_for(
            asyncio.gather(
                assess_heart_impact(session_id=session_id, scenario=query, auth_context=auth_ctx),
                critique_thought_audit(
                    session_id=session_id,
                    thought_id="current_thought",
                    auth_context=auth_ctx,
                ),
            ),
            timeout=parallel_timeout_seconds,
        )
    except Exception as exc:
        parallel_failed = True
        logger.warning("[arifOS] Parallel 666 stages failed, falling back to sequential: %s", exc)

    if parallel_failed:
        heart_res = await assess_heart_impact(
            session_id=session_id, scenario=query, auth_context=auth_ctx
        )
        critique_res = await critique_thought_audit(
            session_id=session_id,
            thought_id="current_thought",
            auth_context=heart_res.auth_context.model_dump(exclude_none=True),
        )

    if heart_res is None or critique_res is None:
        raise RuntimeError(
            "Stage 666 parallel/sequential execution did not produce required results"
        )

    trace["666A_HEART"] = heart_res.verdict.value
    trace["666B_HEART"] = critique_res.verdict.value
    auth_ctx = critique_res.auth_context.model_dump(exclude_none=True)

    # 5. Stage 777: FORGE (Discovery)
    forge_res: RuntimeEnvelope = await quantum_eureka_forge(
        session_id=session_id, intent=query, auth_context=auth_ctx
    )
    trace["777_APEX"] = forge_res.verdict.value
    auth_ctx = forge_res.auth_context.model_dump(exclude_none=True)

    # 6. Stage 888: JUDGE
    verdicts = [
        init_res.verdict,
        frame_res.verdict,
        mind_res.verdict,
        reality_gate_verdict,
        heart_res.verdict,
        critique_res.verdict,
    ]

    if dry_run:
        # P4: Dry-run support. Return state without judgment or commit.
        return {
            "status": "DRY_RUN",
            "verdict": "DRY_RUN",
            "final_verdict": "DRY_RUN",
            "auth_state": auth_state,
            "session_id": session_id,
            "trace": trace,
            "remediation_notes": [
                "Constitutional dry-run completed. No judgment or vault commit performed."
            ],
            "next_best_action": "Set dry_run=False to execute formal governance judgment.",
        }

    # Final Verdict Gating
    if init_failed:
        # Auth failed, loop continues for visibility, but JUDGE must BLOCK.
        candidate = Verdict.VOID
    elif Verdict.VOID in verdicts:
        candidate = Verdict.VOID
    elif Verdict.HOLD_888 in verdicts:
        candidate = Verdict.HOLD_888
    elif Verdict.SABAR in verdicts:
        candidate = Verdict.SABAR
    else:
        candidate = Verdict.SEAL

    judge_res: RuntimeEnvelope = await apex_judge_verdict(
        session_id=session_id,
        verdict_candidate=candidate.value,
        auth_context=auth_ctx,
        reason_summary=(
            f"Metabolic loop synthesis for: {query[:50]}... | "
            f"reality_status={reality_summary['status']} "
            f"score={reality_summary['score']:.2f} "
            f"results={reality_summary['results_count']}"
        ),
    )
    trace["888_JUDGE"] = judge_res.verdict.value
    auth_ctx = judge_res.auth_context.model_dump(exclude_none=True)

    # 7. Stage 999: VAULT
    vault_res: RuntimeEnvelope = await seal_vault_commit(
        session_id=session_id,
        verdict=judge_res.verdict.value,
        auth_context=auth_ctx,
        telemetry={"trace": trace, "reality": reality_summary},
    )
    trace["999_VAULT"] = vault_res.verdict.value

    # Final result construction
    final_output = judge_res.model_dump(mode="json")

    # P1/P2 Unification
    final_output["final_verdict"] = "AUTH_FAIL" if init_failed else judge_res.verdict.value
    final_output["status"] = (
        "SUCCESS" if judge_res.verdict not in (Verdict.VOID, Verdict.SABAR) else "ERROR"
    )
    final_output["auth_state"] = auth_state
    final_output["grounding"] = reality_summary

    if init_failed:
        final_output["failure_origin"] = "AUTH"
        final_output["failure_stage"] = "000_INIT"
        final_output["blocked_because"] = "F11: Command Authority failure during session bootstrap"
        final_output["block_class"] = "auth_only"
        final_output["safe_alternative"] = (
            "Use allow_execution=False and risk_tier=low for auto-anchor"
        )
        final_output["next_best_action"] = "Anchor session with valid actor_id and auth_token"

    final_output["trace"] = trace
    final_output["session_id"] = session_id
    final_output["vault_seal"] = vault_res.verdict == Verdict.SEAL
    final_output["auth_context"] = auth_ctx

    return final_output
