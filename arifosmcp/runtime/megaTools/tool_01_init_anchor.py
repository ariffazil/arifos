"""
arifosmcp/runtime/megaTools/01_init_anchor.py

🔥 THE IGNITION STATE OF INTELLIGENCE (Unified)
Stage: 000_INIT | Trinity: PSI Ψ | Floors: F11, F12, F13

Modes: init, revoke, refresh, state, status
"""

from __future__ import annotations

from typing import Any
from fastmcp.dependencies import CurrentContext

from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
from arifosmcp.runtime.tools_internal import init_anchor_impl
from arifosmcp.runtime.tools_hardened_dispatch import HARDENED_DISPATCH_MAP


async def init_anchor(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    human_approved: bool | None = None,
    risk_tier: str = "low",
    dry_run: bool = True,
    allow_execution: bool = False,
    caller_context: dict[str, Any] | None = None,
    auth_context: dict | None = None,
    debug: bool = False,
    request_id: str | None = None,
    timestamp: str | None = None,
    raw_input: str | None = None,
    pns_shield: Any | None = None,
    proof: str | None = None,
    ctx: Any | None = None,
    reason: str | None = None,
    use_memory: bool = True,
    use_heart: bool = True,
    use_critique: bool = True,
    context: Any | None = None,
) -> RuntimeEnvelope:
    payload = dict(payload or {})
    if human_approved is not None and human_approval is False:
        human_approval = human_approved
    if "human_approved" in payload and "human_approval" not in payload:
        payload["human_approval"] = payload.pop("human_approved")
    if raw_input:
        payload.setdefault("query", raw_input)
    if caller_context:
        payload.setdefault("caller_context", caller_context)
    if auth_context:
        payload.setdefault("auth_context", auth_context)
    if query:
        payload.setdefault("query", query)
    if raw_input:
        payload.setdefault("raw_input", raw_input)
    if session_id:
        payload.setdefault("session_id", session_id)
    if actor_id:
        payload.setdefault("actor_id", actor_id)
    if declared_name:
        payload.setdefault("declared_name", declared_name)
    if intent:
        payload.setdefault("intent", intent)
    if "human_approval" not in payload:
        payload["human_approval"] = human_approval
    if risk_tier:
        payload.setdefault("risk_tier", risk_tier)
    if raw_input:
        payload.setdefault("raw_input", raw_input)
    if pns_shield:
        payload.setdefault("pns_shield", pns_shield)
    if proof:
        payload.setdefault("proof", proof)
    if reason:
        payload.setdefault("reason", reason)
    payload.setdefault("use_memory", use_memory)
    payload.setdefault("use_heart", use_heart)
    payload.setdefault("use_critique", use_critique)
    if context:
        payload.setdefault("context", context)

    if "init_anchor" in HARDENED_DISPATCH_MAP:
        if mode is None:
            mode = "init"
        res = await HARDENED_DISPATCH_MAP["init_anchor"](mode=mode, payload=payload)
        if isinstance(res, dict):
            ok = res.get("ok", res.get("status") not in ("HOLD", "ERROR", "VOID", None))
            _next_tools = res.get("next_allowed_tools", [])
            _payload = res.get("payload", res) if isinstance(res.get("payload"), dict) else res
            _hold_reason = res.get("warnings", [""])[0] if res.get("warnings") else ""
            _next_action = None
            if not ok and _hold_reason:
                _next_action = {
                    "reason": _hold_reason,
                    "missing_requirements": _payload.get("missing_requirements", [])
                    if isinstance(_payload, dict)
                    else [],
                    "next_allowed_tools": _next_tools,
                    "suggested_canonical_call": _payload.get("suggested_canonical_call")
                    if isinstance(_payload, dict)
                    else None,
                }
            return RuntimeEnvelope(
                tool=res.get("tool", "unknown"),
                stage=res.get("stage", "444_ROUTER"),
                status=RuntimeStatus.SUCCESS if ok else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if ok else Verdict.VOID,
                allowed_next_tools=_next_tools,
                next_action=_next_action,
                payload=res,
            )
        return res

    effective_mode = mode or (payload.get("mode") if payload else "init")
    effective_intent = intent or raw_input or (payload.get("intent") if payload else None)
    effective_session = session_id or (payload.get("session_id") if payload else None)
    effective_human_approval = human_approval or (
        payload.get("human_approval") if payload else False
    )
    effective_proof = proof or (payload.get("proof") if payload else None)
    if effective_mode == "revoke" or (reason and "revoke" in str(reason).lower()):
        effective_mode = "revoke"
        effective_intent = effective_intent or reason or "User requested revocation"
    elif effective_mode == "status":
        effective_mode = "status"
    elif effective_mode == "state":
        effective_mode = "state"
    elif effective_mode == "refresh":
        effective_mode = "refresh"

    return await init_anchor_impl(
        actor_id=actor_id or declared_name,
        intent=effective_intent,
        session_id=effective_session,
        human_approval=effective_human_approval,
        ctx=ctx or CurrentContext(),
        mode=effective_mode,
        proof=effective_proof,
        reason=reason,
        payload=payload,
    )
