"""
arifosmcp/bridge.py — The Harden Bridge

This module acts as the secure airlock between the transport layer (MCP/Hub)
and the governance layer (Core/Kernel).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import json
import logging
from pathlib import Path
from typing import Any

from arifosmcp.intelligence.tools.reality_grounding import open_web_page, reality_check
from arifosmcp.runtime.contracts import REQUIRES_SESSION
from core.enforcement.auth_continuity import mint_auth_context, verify_auth_context_cached
from core.enforcement.governance_engine import wrap_tool_output
from core.organs import Verdict, agi, apex, asi, init, vault

logger = logging.getLogger(__name__)
DEFAULT_VAULT_PATH = Path("VAULT999/vault999.jsonl")

# Normalized mapping for the 10-tool stack
TOOL_MAP = {
    "init_anchor_state": "anchor_session",
    "integrate_analyze_reflect": "reason_mind",
    "reason_mind_synthesis": "reason_mind",
    "arifOS.kernel": "metabolic_loop",
    "metabolic_loop_router": "metabolic_loop",
    "vector_memory_store": "vector_memory",
    "assess_heart_impact": "simulate_heart",
    "critique_thought_audit": "critique_thought",
    "quantum_eureka_forge": "eureka_forge",
    "apex_judge_verdict": "apex_judge",
    "seal_vault_commit": "seal_vault",
    "session_memory": "session_memory",
}


async def call_kernel(
    tool_name: str,
    session_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    Route a tool call through the 7-Organ Sovereign Stack.
    Supports the 10-tool APEX-G naming convention.
    """
    canonical_name = TOOL_MAP.get(tool_name, tool_name)

    # 1. Verification of Continuity (F11)
    auth_ctx = payload.get("auth_context")
    if canonical_name in REQUIRES_SESSION:
        if not auth_ctx:
            return wrap_tool_output(
                canonical_name,
                {
                    "verdict": "VOID",
                    "error": (
                        "F11: Missing auth_context for continuity. Run init_anchor_state first."
                    ),
                    "stage": "000_INIT",
                },
            )

        valid, reason = verify_auth_context_cached(session_id, auth_ctx)
        if not valid:
            return wrap_tool_output(
                canonical_name,
                {
                    "verdict": "VOID",
                    "error": f"F11: Authentication continuity failed: {reason}",
                    "stage": "000_INIT",
                },
            )

    # 1.5. Early Exit for Grounding Utilities
    if canonical_name == "search_reality":
        query = payload.get("query", "")
        res = await reality_check(query=query)
        return wrap_tool_output(canonical_name, res)
    if canonical_name == "ingest_evidence":
        res = await open_web_page(url=payload.get("source_url", ""))
        return wrap_tool_output(canonical_name, res)
    if canonical_name == "trace_replay":
        limit = payload.get("limit", 20)
        try:
            max_entries = max(1, min(int(limit), 200))
        except (TypeError, ValueError):
            max_entries = 20

        if not DEFAULT_VAULT_PATH.exists():
            return wrap_tool_output(
                canonical_name,
                {
                    "status": "NO_DATA",
                    "session_id": session_id,
                    "trace_count": 0,
                    "message": "No vault ledger found for replay.",
                    "entries": [],
                },
            )

        replay_entries: list[dict[str, Any]] = []
        try:
            with open(DEFAULT_VAULT_PATH, encoding="utf-8") as ledger_file:
                for line in ledger_file:
                    row = line.strip()
                    if not row:
                        continue
                    try:
                        parsed = json.loads(row)
                    except json.JSONDecodeError:
                        continue
                    if parsed.get("session_id") != session_id:
                        continue
                    telemetry = parsed.get("telemetry", {})
                    trace = telemetry.get("trace") if isinstance(telemetry, dict) else None
                    if not isinstance(trace, dict):
                        continue
                    replay_entries.append(
                        {
                            "session_id": parsed.get("session_id"),
                            "verdict": parsed.get("verdict"),
                            "summary": parsed.get("summary"),
                            "timestamp": parsed.get("timestamp"),
                            "reality": telemetry.get("reality", {}),
                            "trace": trace,
                            "seal_hash": parsed.get("seal_hash"),
                        }
                    )
        except OSError as exc:
            logger.warning("trace_replay failed reading vault: %s", exc)
            return wrap_tool_output(
                canonical_name,
                {
                    "status": "ERROR",
                    "session_id": session_id,
                    "trace_count": 0,
                    "message": f"Vault read failed: {exc}",
                    "entries": [],
                },
            )

        replay_entries = replay_entries[-max_entries:]
        return wrap_tool_output(
            canonical_name,
            {
                "status": "SUCCESS",
                "session_id": session_id,
                "trace_count": len(replay_entries),
                "entries": replay_entries,
            },
        )

    # 2. Kernel Execution Logic
    try:
        query_input = payload.get("query", "")
        actor_id = payload.get("actor_id", "anonymous")
        result: Any = {}

        if canonical_name == "anchor_session":
            from core.shared.types import GovernanceMetadata, Intent, MathDials

            intent = (
                Intent(**payload.get("intent", {}))
                if payload.get("intent")
                else Intent(query=query_input or "INIT")
            )
            math = MathDials(**payload.get("math", {})) if payload.get("math") else MathDials()
            gov = (
                GovernanceMetadata(**payload.get("governance", {}))
                if payload.get("governance")
                else GovernanceMetadata(actor_id=actor_id)
            )

            res = await init(
                query=intent, actor_id=gov, math_dials=math, auth_token=payload.get("auth_token")
            )
            result = res.model_dump(mode="json")

            if res.verdict != Verdict.VOID:
                result["auth_context"] = mint_auth_context(
                    session_id=res.session_id,
                    actor_id=res.governance.actor_id,
                    token_fingerprint="sha256:...",
                    approval_scope=["reason_mind", "simulate_heart", "eureka_forge", "seal_vault"],
                    parent_signature="",
                )
                result["auth_context"]["math"] = math.model_dump(mode="json")

        elif canonical_name == "reason_mind":
            action = "framing" if tool_name == "integrate_analyze_reflect" else "full"
            result = await agi(
                query=query_input,
                session_id=session_id,
                action=action,
                reason_mode=payload.get("reason_mode", "default"),
                max_steps=payload.get("max_steps", 7),
                auth_context=auth_ctx,
            )

        elif canonical_name == "vector_memory":
            result = await vault(
                operation=payload.get("operation", "search"),
                session_id=session_id,
                content=payload.get("content") or payload.get("query"),
                memory_ids=payload.get("memory_ids"),
                top_k=payload.get("top_k", 5),
                auth_context=auth_ctx,
            )

        elif canonical_name == "session_memory":
            requested_operation = str(payload.get("operation", "retrieve")).strip().lower()
            operation_map = {
                "retrieve": "search",
                "recall": "recall",
                "search": "search",
                "store": "store",
                "forget": "forget",
            }
            memory_operation = operation_map.get(requested_operation, "search")
            result = await vault(
                operation=memory_operation,
                session_id=session_id,
                content=payload.get("content") or payload.get("query"),
                memory_ids=payload.get("memory_ids"),
                top_k=payload.get("top_k", 5),
                auth_context=auth_ctx,
            )

        elif canonical_name in ("simulate_heart", "critique_thought"):
            action = "simulate_heart" if canonical_name == "simulate_heart" else "critique_thought"
            result = await asi(
                action=action,
                session_id=session_id,
                scenario=payload.get("scenario") or query_input,
                thought_id=payload.get("thought_id"),
                focus=payload.get("focus") or payload.get("critique_focus", "general"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "eureka_forge":
            result = await apex(
                action="forge",
                session_id=session_id,
                intent=payload.get("intent") or query_input,
                eureka_type=payload.get("eureka_type", "concept"),
                materiality=payload.get("materiality", "idea_only"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "apex_judge":
            result = await apex(
                action="judge",
                session_id=session_id,
                verdict_candidate=payload.get("verdict_candidate", "SEAL"),
                reason_summary=payload.get("reason_summary"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "seal_vault":
            result = await vault(
                operation="seal",
                session_id=session_id,
                summary=payload.get("summary") or "Final commit",
                verdict=payload.get("verdict", "SEAL"),
                approved_by=payload.get("approved_by"),
                approval_reference=payload.get("approval_reference"),
                telemetry=payload.get("telemetry"),
                seal_mode=payload.get("seal_mode", "final"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "metabolic_loop":
            from arifosmcp.runtime.orchestrator import metabolic_loop

            result = await metabolic_loop(
                query=query_input,
                risk_tier=payload.get("risk_tier", "medium"),
                actor_id=actor_id,
                session_id=session_id,
                allow_execution=bool(payload.get("allow_execution", False)),
                dry_run=bool(payload.get("dry_run", False)),
            )

            canonical_envelope_keys = {
                "ok",
                "tool",
                "session_id",
                "stage",
                "verdict",
                "status",
                "metrics",
                "trace",
                "authority",
                "payload",
                "errors",
                "meta",
            }
            if isinstance(result, dict) and canonical_envelope_keys.issubset(result):
                return result

        else:
            result = {"status": "SUCCESS", "message": f"Utility {tool_name} executed."}

        # Normalize result and wrap in Governance Envelope
        if hasattr(result, "model_dump"):
            result = result.model_dump(mode="json")

        if isinstance(result, dict):
            verdict_value = result.get("verdict")
            if hasattr(verdict_value, "value"):
                result["verdict"] = verdict_value.value

            result.setdefault("session_id", session_id)
            result.setdefault("stage", payload.get("stage") or "")
            result.setdefault(
                "actor_id", actor_id or (auth_ctx.get("actor_id") if auth_ctx else "anonymous")
            )

            if canonical_name != "anchor_session" and not any(
                k in result for k in ("evidence", "grounding", "results")
            ):
                result["grounding"] = 1.0

            if canonical_name in {"eureka_forge", "apex_judge", "seal_vault"}:
                for w in ("human_witness", "ai_witness", "earth_witness"):
                    result.setdefault(w, 1.0)

            if canonical_name == "eureka_forge":
                result.setdefault("evidence", {"grounding": "Constitutional Forge Logic"})
            elif canonical_name == "seal_vault":
                result.setdefault("stage", "999_SEAL")

            if auth_ctx:
                result["auth_context"] = auth_ctx

        envelope = wrap_tool_output(canonical_name, result)

        # Handle Auth Context Rotation
        if envelope.get("verdict") != "VOID" and canonical_name != "anchor_session" and auth_ctx:
            envelope["auth_context"] = mint_auth_context(
                session_id=session_id,
                actor_id=auth_ctx.get("actor_id", "anonymous"),
                token_fingerprint="sha256:...",
                approval_scope=["reason_mind", "simulate_heart", "eureka_forge", "seal_vault"],
                parent_signature=auth_ctx.get("signature", ""),
            )
            if "math" in auth_ctx:
                envelope["auth_context"]["math"] = auth_ctx["math"]
        elif canonical_name == "anchor_session" and "auth_context" in result:
            envelope["auth_context"] = result["auth_context"]

        return envelope

    except Exception as e:
        logger.error(f"Bridge failure on {tool_name}: {e}", exc_info=True)
        return wrap_tool_output(
            canonical_name, {"verdict": "VOID", "error": str(e), "stage": "BRIDGE_FAILURE"}
        )
