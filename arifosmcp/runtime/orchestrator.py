"""
arifosmcp/runtime/orchestrator.py — The arifOS Metabolic Loop Orchestrator

This module implements the Stage 444 logic, coordinating the 10-tool APEX-G kernel.
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import asyncio
import logging
import os
from typing import Any

from arifosmcp.runtime.models import RuntimeEnvelope, Stage, Verdict

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
    Refined Stage 444 Orchestrator (~33 lines core logic).
    Enforces the Constitutional State Machine.
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
    from core.governance_kernel import route_pipeline

    # 1. INIT & Routing
    current_session_id = _normalize_session_id(session_id)
    init_res = await init_anchor_state(
        {"query": query},
        session_id=current_session_id,
        governance={"actor_id": actor_id, "stakes_class": risk_tier},
    )
    auth_ctx = init_res.auth_context.model_dump(exclude_none=True)
    auth_state = init_res.auth_state
    init_failed = init_res.verdict == Verdict.VOID
    reality_summary = {
        "status": "SKIPPED",
        "required": False,
        "executed": False,
        "score": 0.0,
        "results_count": 0,
    }
    trace = {"000_INIT": init_res.verdict.value}

    # Use the context-aware router
    plan = route_pipeline(query, {"human_required": allow_execution})

    # Always ensure Vault is in the final persistence path
    if "999_VAULT" not in plan:
        plan.append("999_VAULT")

    if dry_run:
        return {
            "status": "DRY_RUN",
            "verdict": "DRY_RUN",
            "final_verdict": "DRY_RUN",
            "auth_state": auth_state,
            "session_id": current_session_id,
            "trace": trace,
            "plan": plan,
            "remediation_notes": ["Constitutional dry-run completed."],
        }

    # 2. Sequential Execution (The Metabolic Loop)
    verdicts: list[Verdict] = [init_res.verdict]
    last_res: RuntimeEnvelope = init_res

    for stage_id in plan:
        res: RuntimeEnvelope | None = None

        if stage_id == "111_SENSE":
            res = await integrate_analyze_reflect(
                session_id=current_session_id, query=query, auth_context=auth_ctx
            )
        elif stage_id == "222_REALITY":
            # Reality Verification Logic (Grounding)
            from arifosmcp.intelligence.tools.reality_grounding import reality_check

            reality_timeout = float(os.getenv("ARIFOS_REALITY_TIMEOUT_SECONDS", "15"))
            try:
                reality_res = await asyncio.wait_for(
                    reality_check(query=query), timeout=reality_timeout
                )
                score = float(reality_res.get("score", 0.0))
                results_count = int(reality_res.get("results_count", 0))
                status = reality_res.get("status", "OK")
                reality_summary.update(
                    {
                        "executed": True,
                        "status": status,
                        "score": score,
                        "results_count": results_count,
                    }
                )
                v = Verdict.SEAL if score >= 0.5 else Verdict.PARTIAL
            except Exception as e:
                v = Verdict.PARTIAL
                reality_summary.update({"status": "ERROR", "error": str(e), "executed": True})
            res = RuntimeEnvelope(verdict=v, stage=Stage.SENSE_111, session_id=current_session_id)

        elif stage_id == "333_MIND":
            res = await reason_mind_synthesis(
                session_id=current_session_id, query=query, auth_context=auth_ctx
            )
        elif stage_id == "555_HEART":
            res = await assess_heart_impact(
                session_id=current_session_id, scenario=query, auth_context=auth_ctx
            )
        elif stage_id == "666_CRITIQUE":
            res = await critique_thought_audit(
                session_id=current_session_id, thought_id="current", auth_context=auth_ctx
            )
        elif stage_id == "777_FORGE":
            res = await quantum_eureka_forge(
                session_id=current_session_id, intent=query, auth_context=auth_ctx
            )
        elif stage_id == "888_JUDGE":
            # Final Verdict Gating
            candidate = Verdict.SEAL
            if init_failed or Verdict.VOID in verdicts:
                candidate = Verdict.VOID
            elif Verdict.HOLD_888 in verdicts:
                candidate = Verdict.HOLD_888
            elif Verdict.SABAR in verdicts:
                candidate = Verdict.SABAR
            elif Verdict.HOLD in verdicts:
                candidate = Verdict.HOLD

            res = await apex_judge_verdict(
                session_id=current_session_id,
                verdict_candidate=candidate.value,
                auth_context=auth_ctx,
                reason_summary=f"Metabolic loop for: {query[:50]}...",
            )
        elif stage_id == "999_VAULT":
            # VAULT is always the final seal
            res = await seal_vault_commit(
                session_id=current_session_id,
                verdict=last_res.verdict.value,
                auth_context=auth_ctx,
                telemetry={"trace": trace, "reality": reality_summary},
            )

        # Process stage result
        if res:
            last_res = res
            verdict = res.verdict

            # Constitutional Normalization Safeguard (Exploration stages cannot kill ideas)
            if stage_id < "888_JUDGE" and verdict == Verdict.VOID:
                verdict = Verdict.SABAR

            trace[stage_id] = verdict.value
            verdicts.append(verdict)

            if res.auth_context:
                auth_ctx = res.auth_context.model_dump(exclude_none=True)

            # Terminal check: Stop exploration on final or blocked states
            if verdict in [Verdict.SEAL, Verdict.HOLD, Verdict.HOLD_888, Verdict.VOID]:
                # Seal vault with whatever we have before breaking
                if stage_id != "999_VAULT" and "999_VAULT" in plan:
                    await seal_vault_commit(
                        session_id=current_session_id,
                        verdict=verdict.value,
                        auth_context=auth_ctx,
                        telemetry={"trace": trace, "reality": reality_summary},
                    )
                break

    # 3. Build Final Production Output
    out = last_res.model_dump(mode="json")
    out.update(
        {
            "final_verdict": verdicts[-1].value,
            "status": "SUCCESS" if verdicts[-1] not in (Verdict.VOID, Verdict.SABAR) else "ERROR",
            "auth_state": auth_state,
            "trace": trace,
            "grounding": reality_summary,
            "session_id": current_session_id,
            "vault_seal": "999_VAULT" in trace,
        }
    )
    return out
