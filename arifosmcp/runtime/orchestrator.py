"""
arifosmcp/runtime/orchestrator.py — The arifOS Metabolic Loop Orchestrator

This module implements the Stage 444 logic, coordinating the routed 000-999 flow.
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

from arifosmcp.runtime.models import CallerContext, RuntimeEnvelope, Stage, Verdict


def _extract_auth_context(
    envelope: RuntimeEnvelope | None, fallback: dict[str, Any] | None = None
) -> dict[str, Any]:
    if envelope is None:
        return dict(fallback or {})

    auth_context = getattr(envelope, "auth_context", None)
    if isinstance(auth_context, dict):
        return dict(auth_context)

    return dict(fallback or {})


def _extract_caller_context(
    envelope: RuntimeEnvelope | None, fallback: CallerContext | None = None
) -> CallerContext | None:
    """Carry the caller_context forward through the metabolic loop."""
    if envelope is None:
        return fallback

    ctx = getattr(envelope, "caller_context", None)
    if isinstance(ctx, CallerContext):
        return ctx

    return fallback


def _dump_caller_context(caller_ctx: CallerContext | None) -> dict[str, Any] | None:
    """Serialize CallerContext for embedding in output dicts."""
    if caller_ctx is None:
        return None
    return caller_ctx.model_dump(mode="json", exclude_none=True)


async def run_stage(
    stage_id: str,
    query: str,
    session_id: str,
    auth_ctx: dict[str, Any],
    verdicts: list[Verdict],
    trace: dict[str, Any],
    reality_summary: dict[str, Any],
    caller_ctx: CallerContext | None = None,
) -> RuntimeEnvelope:
    """Execute one routed stage for the metabolic loop."""
    from arifosmcp.runtime.tools import (
        apex_judge_verdict,
        assess_heart_impact,
        critique_thought_audit,
        integrate_analyze_reflect,
        quantum_eureka_forge,
        reason_mind_synthesis,
        seal_vault_commit,
        session_memory,
    )

    if stage_id == Stage.SENSE_111.value:
        return await integrate_analyze_reflect(
            session_id=session_id, query=query, auth_context=auth_ctx, caller_context=caller_ctx
        )

    if stage_id == Stage.REALITY_222.value:
        from arifosmcp.intelligence.tools.reality_grounding import reality_check

        reality_timeout = float(os.getenv("ARIFOS_REALITY_TIMEOUT_SECONDS", "15"))
        try:
            reality_res = await asyncio.wait_for(
                reality_check(query=query), timeout=reality_timeout
            )
            score = float(reality_res.get("score", 0.0))
            results_count = int(reality_res.get("results_count", 0))
            status = str(reality_res.get("status", "OK"))
            reality_summary.update(
                {
                    "executed": True,
                    "status": status,
                    "score": score,
                    "results_count": results_count,
                }
            )
            verdict = Verdict.SEAL if score >= 0.5 else Verdict.PARTIAL
        except Exception as exc:
            verdict = Verdict.PARTIAL
            reality_summary.update({"status": "ERROR", "error": str(exc), "executed": True})

        return RuntimeEnvelope(
            tool="search_reality",
            session_id=session_id,
            stage=Stage.REALITY_222.value,
            verdict=verdict,
            payload={"reality": dict(reality_summary)},
            auth_context=auth_ctx,
            caller_context=caller_ctx,
        )

    if stage_id == Stage.MIND_333.value:
        return await reason_mind_synthesis(
            session_id=session_id, query=query, auth_context=auth_ctx, caller_context=caller_ctx
        )

    if stage_id == Stage.MEMORY_555.value:
        return await session_memory(
            session_id=session_id,
            operation="search",
            auth_context=auth_ctx,
            content=query,
            caller_context=caller_ctx,
        )

    if stage_id == Stage.HEART_666.value:
        return await assess_heart_impact(
            session_id=session_id, scenario=query, auth_context=auth_ctx, caller_context=caller_ctx
        )

    if stage_id == Stage.CRITIQUE_666.value:
        return await critique_thought_audit(
            session_id=session_id,
            thought_id="current_thought",
            auth_context=auth_ctx,
            caller_context=caller_ctx,
        )

    if stage_id == Stage.FORGE_777.value:
        return await quantum_eureka_forge(
            session_id=session_id, intent=query, auth_context=auth_ctx, caller_context=caller_ctx
        )

    if stage_id == Stage.JUDGE_888.value:
        candidate = Verdict.SEAL
        if Verdict.VOID in verdicts:
            candidate = Verdict.VOID
        elif Verdict.HOLD_888 in verdicts or Verdict.HOLD in verdicts:
            candidate = Verdict.HOLD_888
        elif Verdict.SABAR in verdicts:
            candidate = Verdict.SABAR

        return await apex_judge_verdict(
            session_id=session_id,
            verdict_candidate=candidate.value,
            auth_context=auth_ctx,
            reason_summary=(
                f"Metabolic loop synthesis for: {query[:50]}... | "
                f"reality_status={reality_summary.get('status', 'SKIPPED')} "
                f"score={reality_summary.get('score', 0.0):.2f}"
            ),
            caller_context=caller_ctx,
        )

    if stage_id == Stage.VAULT_999.value:
        last_verdict = verdicts[-1] if verdicts else Verdict.SABAR
        return await seal_vault_commit(
            session_id=session_id,
            verdict=last_verdict.value,
            auth_context=auth_ctx,
            telemetry={"trace": trace, "reality": reality_summary},
            caller_context=caller_ctx,
        )

    return RuntimeEnvelope(
        tool="arifOS.kernel",
        session_id=session_id,
        stage=stage_id,
        verdict=Verdict.SABAR,
        payload={"warning": f"Unknown routed stage: {stage_id}"},
        auth_context=auth_ctx,
        caller_context=caller_ctx,
    )


async def metabolic_loop(
    query: str,
    risk_tier: str = "medium",
    actor_id: str = "anonymous",
    session_id: str | None = None,
    allow_execution: bool = False,
    dry_run: bool = False,
    caller_context: CallerContext | None = None,
) -> dict[str, Any]:
    """Run the routed constitutional loop and return the canonical kernel envelope."""
    from arifosmcp.runtime.tools import _normalize_session_id, init_anchor_state, seal_vault_commit
    from core.governance_kernel import route_pipeline
    from core.organs._0_init import coerce_stakes_class

    current_session_id = _normalize_session_id(session_id)
    stakes_class = coerce_stakes_class(risk_tier).get("value", "C")
    init_res = await init_anchor_state(
        {"query": query},
        session_id=current_session_id,
        governance={"actor_id": actor_id, "stakes_class": stakes_class},
        caller_context=caller_context,
    )
    auth_ctx = _extract_auth_context(init_res)
    caller_ctx = _extract_caller_context(init_res, caller_context)
    auth_state = init_res.authority.auth_state
    init_failed = init_res.verdict == Verdict.VOID

    reality_summary = {
        "status": "SKIPPED",
        "required": False,
        "executed": False,
        "score": 0.0,
        "results_count": 0,
    }
    trace = {Stage.INIT_000.value: init_res.verdict.value}

    plan = route_pipeline(query, {"human_required": allow_execution})
    if Stage.VAULT_999.value not in plan:
        plan.append(Stage.VAULT_999.value)

    if dry_run:
        return {
            "ok": True,
            "tool": "arifOS.kernel",
            "session_id": current_session_id,
            "stage": Stage.ROUTER_444.value,
            "verdict": Verdict.PARTIAL.value,
            "status": "DRY_RUN",
            "metrics": {},
            "trace": trace,
            "authority": {"actor_id": actor_id, "auth_state": auth_state},
            "payload": {"plan": plan},
            "errors": [],
            "meta": {"schema_version": "1.0.0", "debug": False, "dry_run": True},
            "final_verdict": "DRY_RUN",
            "auth_state": auth_state,
            "caller_context": _dump_caller_context(caller_ctx),
            "remediation_notes": ["Constitutional dry-run completed."],
        }

    verdicts: list[Verdict] = [init_res.verdict]
    policy_res: RuntimeEnvelope = init_res
    policy_verdict = init_res.verdict

    for stage_id in plan:
        res = await run_stage(
            stage_id=stage_id,
            query=query,
            session_id=current_session_id,
            auth_ctx=auth_ctx,
            verdicts=verdicts,
            trace=trace,
            reality_summary=reality_summary,
            caller_ctx=caller_ctx,
        )
        verdict = res.verdict

        if stage_id < Stage.JUDGE_888.value and verdict == Verdict.VOID:
            verdict = Verdict.SABAR
            res = res.model_copy(update={"verdict": verdict})

        trace[stage_id] = verdict.value
        verdicts.append(verdict)
        auth_ctx = _extract_auth_context(res, auth_ctx)
        caller_ctx = _extract_caller_context(res, caller_ctx)

        if stage_id != Stage.VAULT_999.value:
            policy_res = res
            policy_verdict = verdict

        should_break = (
            stage_id in {Stage.JUDGE_888.value, Stage.VAULT_999.value}
            and verdict in {Verdict.SEAL, Verdict.HOLD_888, Verdict.VOID}
        )
        if should_break and stage_id != Stage.VAULT_999.value:
            vault_res = await seal_vault_commit(
                session_id=current_session_id,
                verdict=policy_verdict.value,
                auth_context=auth_ctx,
                telemetry={"trace": trace, "reality": reality_summary},
                caller_context=caller_ctx,
            )
            trace[Stage.VAULT_999.value] = vault_res.verdict.value
            auth_ctx = _extract_auth_context(vault_res, auth_ctx)
            caller_ctx = _extract_caller_context(vault_res, caller_ctx)
            break

    out = policy_res.model_dump(mode="json")
    out.update(
        {
            "tool": "arifOS.kernel",
            "session_id": current_session_id,
            "stage": policy_res.stage,
            "verdict": policy_verdict.value,
            "status": "SUCCESS" if policy_verdict not in (Verdict.VOID, Verdict.SABAR) else "ERROR",
            "trace": trace,
            "authority": policy_res.authority.model_dump(mode="json"),
            "final_verdict": "AUTH_FAIL" if init_failed else policy_verdict.value,
            "auth_state": auth_state,
            "grounding": reality_summary,
            "vault_seal": trace.get(Stage.VAULT_999.value) == Verdict.SEAL.value,
            "caller_context": _dump_caller_context(caller_ctx),
        }
    )
    return out
