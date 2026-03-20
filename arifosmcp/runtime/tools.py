from __future__ import annotations

import asyncio
import logging
import os
import uuid
from typing import Any, Callable

from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context
from fastmcp.tools import Tool
from fastmcp.tools import tool as make_tool
from fastmcp.tools.tool_transform import ArgTransform

from arifosmcp.runtime.models import (
    ArifOSError,
    AuthContext,
    CanonicalAuthority,
    ClaimStatus,
    RuntimeEnvelope,
    UserModelField,
    UserModelSource,
    Stage,
    Verdict,
    RuntimeStatus,
    CanonicalError,
    CallerContext,
    UserModel,
    PersonaId,
    BudgetTier,
    OverflowPolicy,
)
from arifosmcp.runtime.public_registry import (
    public_tool_names,
    public_tool_specs,
    public_tool_spec_by_name,
)
from arifosmcp.runtime.sessions import (
    _resolve_session_id,
    get_session_identity,
    resolve_runtime_context,
    set_active_session,
)
from arifosmcp.runtime.bridge import call_kernel
from arifosmcp.capability_map import CAPABILITY_MAP
from arifosmcp.runtime.reality_handlers import handler as reality_handler
from arifosmcp.runtime.reality_models import BundleInput
from arifosmcp.tools.agentzero_tools import (
    agentzero_validate as _az_validate,
    agentzero_engineer as _az_engineer,
    agentzero_hold_check as _az_hold_check,
    agentzero_memory_query as _az_memory_query,
    agentzero_armor_scan as _az_armor_scan,
)

# High-level dispatcher imports
from arifosmcp.runtime.tools_internal import (
    init_anchor_impl,
    revoke_anchor_state_impl,
    refresh_anchor_impl,
    arifos_kernel_impl,
    get_caller_status_impl,
    apex_soul_dispatch_impl,
    vault_ledger_dispatch_impl,
    agi_mind_dispatch_impl,
    asi_heart_dispatch_impl,
    engineering_memory_dispatch_impl,
    physics_reality_dispatch_impl,
    math_estimator_dispatch_impl,
    code_engine_dispatch_impl,
    architect_registry_dispatch_impl,
)

logger = logging.getLogger(__name__)

_public_tool_names_fn = public_tool_names
_public_tool_specs_fn = public_tool_specs

PUBLIC_KERNEL_TOOL_NAME = "arifOS_kernel"
LEGACY_KERNEL_TOOL_NAME = "metabolic_loop_router"

try:
    from core.telemetry import check_adaptation_status, get_current_hysteresis
except Exception:  # pragma: no cover
    def check_adaptation_status() -> dict[str, Any]:
        return {"status": "unavailable"}

    def get_current_hysteresis() -> float:
        return 0.0

try:
    from core.physics.thermodynamics_hardened import get_thermodynamic_report
except Exception:  # pragma: no cover
    def get_thermodynamic_report(session_id: str) -> dict[str, Any]:
        return {"status": "unavailable", "session_id": session_id}

def _normalize_session_id(session_id: str | None) -> str:
    """Resolve or mint a session id for compatibility callers."""
    resolved = _resolve_session_id(session_id)
    if resolved and str(resolved).strip():
        return str(resolved).strip()
    minted = f"session-{uuid.uuid4().hex[:8]}"
    set_active_session(minted)
    return minted

# =============================================================================
# ⚖️ GOVERNANCE LAYER (G-1 to G-4)
# =============================================================================

async def init_anchor(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    raw_input: str | None = None,
    session_id: str | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """000_INIT: Dispatcher for identity operations."""
    ctx = ctx or CurrentContext()
    if mode is None:
        mode = "init"
        payload = {
            "actor_id": actor_id or declared_name or "anonymous",
            "intent": intent or raw_input,
            "session_id": session_id,
        }
    
    # Ensure payload has session_id
    if payload is None: payload = {}
    sid = payload.get("session_id") or session_id
    payload["session_id"] = _normalize_session_id(sid)

    if mode == "init":
        return await init_anchor_impl(
            actor_id=payload.get("actor_id", "anonymous"),
            intent=payload.get("intent"),
            session_id=payload.get("session_id"),
            ctx=ctx
        )
    elif mode == "revoke":
        return await revoke_anchor_state_impl(
            session_id=payload.get("session_id"),
            reason=payload.get("reason") or "Unspecified",
            ctx=ctx
        )
    elif mode == "refresh":
        refreshed_session = payload.get("session_id")
        return RuntimeEnvelope(
            tool="init_anchor",
            session_id=refreshed_session,
            stage=Stage.INIT_000.value,
            verdict=Verdict.SEAL,
            status=RuntimeStatus.SUCCESS,
            payload={"refreshed": True, "session_id": refreshed_session},
        )
    raise ValueError(f"Invalid mode for init_anchor: {mode}")

async def arifOS_kernel(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    query: str | None = None,
    session_id: str | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """444_ROUTER: Dispatcher for kernel and status."""
    ctx = ctx or CurrentContext()
    if mode is None:
        mode = "kernel"
        payload = {"query": query or "", "session_id": session_id}
    
    # Ensure payload has session_id
    if payload is None: payload = {}
    sid = payload.get("session_id") or session_id
    payload["session_id"] = _normalize_session_id(sid)

    if mode == "kernel":
        return await arifos_kernel_impl(
            query=payload.get("query", ""),
            risk_tier=risk_tier,
            auth_context=auth_context,
            dry_run=dry_run,
            allow_execution=allow_execution,
            session_id=payload.get("session_id"),
            ctx=ctx
        )
    elif mode == "status":
        return await get_caller_status_impl(session_id=payload.get("session_id"), ctx=ctx)
    raise ValueError(f"Invalid mode for arifOS_kernel: {mode}")

async def apex_soul(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """888_JUDGE: Dispatcher for soul/verdict functions."""
    ctx = ctx or CurrentContext()
    return await apex_soul_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def vault_ledger(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """999_VAULT: Dispatcher for immutable persistence."""
    ctx = ctx or CurrentContext()
    return await vault_ledger_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

# =============================================================================
# 🧠 INTELLIGENCE LAYER (I-1 to I-3)
# =============================================================================

async def agi_mind(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """333_MIND: Dispatcher for reasoning and reflection."""
    ctx = ctx or CurrentContext()
    return await agi_mind_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def asi_heart(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """666_HEART: Dispatcher for empathy and ethics."""
    ctx = ctx or CurrentContext()
    return await asi_heart_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def engineering_memory(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
) -> RuntimeEnvelope:
    """555_MEMORY: Dispatcher for technical execution."""
    return await engineering_memory_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run
    )

# =============================================================================
# ⚙️ MACHINE LAYER (M-1 to M-4)
# =============================================================================

async def physics_reality(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """111_SENSE: Dispatcher for grounding."""
    ctx = ctx or CurrentContext()
    return await physics_reality_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def math_estimator(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Dispatcher for quantitative estimation."""
    ctx = ctx or CurrentContext()
    return await math_estimator_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def code_engine(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Dispatcher for computational execution."""
    ctx = ctx or CurrentContext()
    return await code_engine_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def architect_registry(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """Dispatcher for system definition."""
    ctx = ctx or CurrentContext()
    return await architect_registry_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

# -----------------------------------------------------------------------------
# INTERNAL HELPERS
# -----------------------------------------------------------------------------

def _build_user_model(
    tool_name: str,
    stage_value: str,
    payload: dict[str, Any],
    envelope_data: dict[str, Any],
) -> UserModel:
    """Helper to build User Model for legacy callers."""
    query = str(payload.get("query") or payload.get("intent") or payload.get("content") or "").strip()
    context = str(payload.get("context") or "").strip()
    output_constraints: list[UserModelField] = []
    lowered = f"{query} {context}".lower()
    if "concise" in lowered:
        output_constraints.append(
            UserModelField(value="keep_response_concise", source=UserModelSource.EXPLICIT)
        )
    if envelope_data.get("meta", {}).get("dry_run") or payload.get("dry_run"):
        output_constraints.append(
            UserModelField(
                value="state_that_execution_is_simulated",
                source=UserModelSource.OBSERVABLE,
            )
        )
    return UserModel(
        stated_goal=UserModelField(
            value=query or context or f"{tool_name}:{stage_value}",
            source=UserModelSource.EXPLICIT,
        ),
        output_constraints=output_constraints,
    )

def _resolve_caller_context(
    caller_context: CallerContext | None,
    requested_persona: str | None,
) -> CallerContext:
    """Helper to resolve caller context for legacy callers."""
    base = caller_context or CallerContext()
    if requested_persona:
        try:
            base.persona_id = PersonaId(requested_persona.lower())
        except (ValueError, AttributeError):
            pass
    return base


def _resolve_caller_state(
    session_id: str,
    authority: Any,
) -> tuple[str, list[str], list[dict[str, str]]]:
    if session_id == "global":
        caller_state = "anonymous"
    elif stored := get_session_identity(session_id):
        caller_state = "verified" if stored.get("authority_level") in {"sovereign", "operator"} else "anchored"
    else:
        if isinstance(authority, dict):
            claim_status = authority.get("claim_status", "anonymous")
            actor_id = authority.get("actor_id", "anonymous")
        else:
            claim_status = getattr(authority, "claim_status", "anonymous") if authority is not None else "anonymous"
            actor_id = getattr(authority, "actor_id", "anonymous") if authority is not None else "anonymous"
        claim_status_value = getattr(claim_status, "value", claim_status)
        if str(claim_status_value).lower() == "verified":
            caller_state = "verified"
        elif str(claim_status_value).lower() == "anchored":
            caller_state = "anchored"
        elif actor_id != "anonymous":
            caller_state = "claimed"
        else:
            caller_state = "anonymous"

    allowed = {
        "anonymous": ["get_caller_status", "init_anchor", "init_anchor_state", "register_tools", "audit_rules", "check_vital"],
        "claimed": ["get_caller_status", "init_anchor", "init_anchor_state", "register_tools", "audit_rules", "check_vital"],
        "anchored": ["get_caller_status", "check_vital", "audit_rules", "agi_reason", "search_reality", "reality_compass", "asi_critique"],
        "verified": ["get_caller_status", "check_vital", "audit_rules", "agi_reason", "search_reality", "reality_compass", "asi_critique", "arifOS_kernel", "forge", "vault_seal"],
    }
    blocked = {
        "anonymous": [
            {"tool": "arifOS_kernel", "reason": "Session anchor required."},
            {"tool": "agentzero_engineer", "reason": "Execution requires anchored authority."},
        ],
        "claimed": [
            {"tool": "arifOS_kernel", "reason": "Anchor identity before kernel execution."},
            {"tool": "agentzero_engineer", "reason": "Execution requires anchored authority."},
        ],
        "anchored": [{"tool": "agentzero_engineer", "reason": "High-risk execution remains gated."}],
        "verified": [],
    }
    return caller_state, allowed.get(caller_state, allowed["anonymous"]), blocked.get(caller_state, blocked["anonymous"])

async def _wrap_call(
    tool_name: str,
    stage: Stage,
    session_id: str | None,
    payload: dict[str, Any],
    ctx: Context | None = None,
    caller_context: CallerContext | None = None,
) -> RuntimeEnvelope:
    """Unified internal wrapper for metabolic loop dispatch."""
    if not isinstance(payload, dict):
        raise TypeError("Payload must be a dict")

    normalized_session = _normalize_session_id(session_id)
    payload = dict(payload)
    payload["session_id"] = normalized_session
    payload["tool"] = tool_name
    payload["stage"] = stage.value
    if caller_context is not None:
        payload["caller_context"] = caller_context.model_dump(mode="json", exclude_none=True)

    try:
        kernel_res = await call_kernel(tool_name, normalized_session, payload)
        envelope = RuntimeEnvelope(**kernel_res)
    except ArifOSError:
        raise
    except Exception as e:
        logger.error(f"wrap_call failure: {e}", exc_info=True)
        envelope = RuntimeEnvelope(
            ok=False, tool=tool_name, session_id=normalized_session, stage=stage.value,
            verdict=Verdict.SABAR, status=RuntimeStatus.ERROR,
            errors=[CanonicalError(code="RUNTIME_FAILURE", message=str(e), stage=stage.value)]
        )

    if envelope.user_model is None:
        envelope.user_model = _build_user_model(tool_name, envelope.stage, payload, envelope.model_dump(mode="json"))

    envelope.tool = tool_name
    envelope.session_id = normalized_session
    envelope.caller_state, envelope.allowed_next_tools, envelope.blocked_tools = _resolve_caller_state(
        normalized_session,
        getattr(envelope, "authority", None),
    )
    
    return envelope

# -----------------------------------------------------------------------------
# LEGACY COMPATIBILITY WRAPPERS
# -----------------------------------------------------------------------------

async def metabolic_loop_router(
    query: str,
    session_id: str | None = None,
    risk_tier: str = "medium",
    caller_context: CallerContext | None = None,
    requested_persona: str | None = None,
    **kwargs
) -> RuntimeEnvelope:
    resolved_caller = _resolve_caller_context(caller_context, requested_persona)
    payload = {"query": query, "session_id": session_id, "risk_tier": risk_tier, "caller_context": resolved_caller, **kwargs}
    return await _wrap_call("arifOS_kernel", Stage.ROUTER_444, session_id, payload, caller_context=resolved_caller)

async def check_vital(session_id: str = "global", **kwargs) -> RuntimeEnvelope:
    envelope = await _wrap_call("check_vital", Stage.INIT_000, session_id, {"session_id": session_id, **kwargs})
    try:
        envelope.payload["thermodynamic_vitality"] = get_thermodynamic_report(session_id)
        envelope.payload["constitutional_telemetry"] = {
            "adaptation_status": check_adaptation_status(),
            "hysteresis_penalty": get_current_hysteresis(),
        }
    except Exception as exc:
        envelope.payload["vital_error"] = str(exc)
    envelope.payload["intelligence_services"] = await _probe_intelligence_services()
    return envelope


async def _probe_intelligence_services() -> dict[str, dict[str, Any]]:
    return {}

async def audit_rules(session_id: str = "global", **kwargs) -> RuntimeEnvelope:
    return await _wrap_call("audit_rules", Stage.JUDGE_888, session_id, {"session_id": session_id, **kwargs})

async def init_anchor_state(
    declared_name: str = "anonymous",
    session_id: str | None = None,
    auth_context: dict[str, Any] | None = None,
    human_approval: bool = False,
    intent: Any | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
    **kwargs
) -> RuntimeEnvelope:
    return await init_anchor(
        actor_id=declared_name,
        session_id=session_id,
        auth_context=auth_context,
        intent=intent,
        caller_context=caller_context,
        ctx=ctx,
        **kwargs
    )

async def get_caller_status(
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    envelope = await _wrap_call("get_caller_status", Stage.INIT_000, session_id, {}, ctx)
    envelope.tool = "get_caller_status"

    auth_ctx_dict = (
        envelope.auth_context.model_dump(mode="json")
        if envelope.auth_context is not None and hasattr(envelope.auth_context, "model_dump")
        else None
    )
    resolved = resolve_runtime_context(
        incoming_session_id=session_id,
        auth_context=auth_ctx_dict,
        actor_id=envelope.authority.actor_id if getattr(envelope, "authority", None) else None,
        declared_name=None,
    )
    envelope.session_id = resolved["resolved_session_id"]
    envelope.payload.update(
        {
            "transport_session_id": resolved["transport_session_id"],
            "resolved_session_id": resolved["resolved_session_id"],
            "session_id": resolved["resolved_session_id"],
            "canonical_actor_id": resolved["canonical_actor_id"],
            "display_name": resolved["display_name"],
            "authority_source": resolved["authority_source"],
            "caller_state": envelope.caller_state,
            "bootstrap_sequence": [
                "1. check_vital - System health and vitals (no auth required)",
                "2. audit_rules - Constitutional floors and tool contracts (no auth required)",
                "3. init_anchor - Establish identity (creates session anchor)",
                "4. arifOS_kernel - Primary metabolic loop for governed execution",
            ],
            "system_motto": "DITEMPA BUKAN DIBERI — Forged, Not Given",
        }
    )
    envelope.diagnostics_only = envelope.caller_state == "anonymous"
    return envelope

async def forge_legacy(spec: str, session_id: str = "global", dry_run: bool = False, **kwargs) -> RuntimeEnvelope:
    return await agi_mind(mode="forge", payload={"query": spec, "session_id": session_id, "dry_run": dry_run, **kwargs})


async def arifos_kernel(
    query: str = "",
    session_id: str | None = None,
    risk_tier: str = "medium",
    dry_run: bool = False,
    debug: bool = False,
    **kwargs,
) -> RuntimeEnvelope:
    return await metabolic_loop_router(
        query=query,
        session_id=session_id,
        risk_tier=risk_tier,
        dry_run=dry_run,
        debug=debug,
        **kwargs,
    )


async def forge(
    spec: str,
    session_id: str = "global",
    dry_run: bool = False,
    risk_tier: str = "medium",
    **kwargs,
) -> RuntimeEnvelope:
    return await metabolic_loop_router(
        query=spec,
        session_id=session_id,
        dry_run=dry_run,
        risk_tier=risk_tier,
        **kwargs,
    )


async def agi_reason(
    query: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    facts: list[str] | None = None,
    causal_interventions: list[dict[str, Any]] | None = None,
    auth_context: dict[str, Any] | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    payload = {
        "query": query,
        "facts": facts or [],
        "causal_interventions": causal_interventions or [],
        "auth_context": auth_context,
        **kwargs,
    }
    return await _wrap_call("agi_reason", Stage.MIND_333, session_id, payload, ctx)


async def agi_reflect(
    topic: str = "",
    session_id: str | None = None,
    ctx: Context | None = None,
    content: str | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    payload = {"topic": topic, "content": content or topic, **kwargs}
    return await _wrap_call("agi_reflect", Stage.MEMORY_555, session_id, payload, ctx)


async def asi_simulate(
    scenario: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("asi_simulate", Stage.HEART_666, session_id, {"scenario": scenario, **kwargs}, ctx)


async def asi_critique(
    draft_output: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("asi_critique", Stage.CRITIQUE_666, session_id, {"draft_output": draft_output, **kwargs}, ctx)


async def apex_judge(
    candidate_output: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("apex_judge", Stage.JUDGE_888, session_id, {"candidate_output": candidate_output, **kwargs}, ctx)


async def vault_seal(
    verdict: str = "SEAL",
    evidence: Any | None = None,
    summary: str | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    payload = {"verdict": verdict, "evidence": evidence or summary, **kwargs}
    return await _wrap_call("vault_seal", Stage.VAULT_999, session_id, payload, ctx)


async def verify_vault_ledger(
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("verify_vault_ledger", Stage.VAULT_999, session_id, kwargs, ctx)


async def reality_compass(
    input: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    mode: str = "compass",
    policy: dict[str, Any] | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    if mode == "search":
        result = await reality_handler.handle_compass(BundleInput(type="query", value=input, mode="search"), {})
    elif mode == "fetch":
        result = await reality_handler.handle_compass(BundleInput(type="url", value=input, mode="fetch"), {})
    else:
        result = await reality_handler.handle_compass(
            BundleInput(type="query", value=input),
            {"session_id": session_id, "policy": policy or {}, **kwargs},
        )
    if isinstance(result, RuntimeEnvelope):
        return result
    if hasattr(result, "model_dump"):
        dumped = result.model_dump()
        if asyncio.iscoroutine(dumped):
            dumped = await dumped
        if "tool" not in dumped or "stage" not in dumped:
            dumped = {
                "ok": True,
                "tool": "reality_compass",
                "session_id": session_id,
                "stage": Stage.REALITY_222.value,
                "verdict": getattr(getattr(result, "status", None), "verdict", "SEAL"),
                "status": getattr(getattr(result, "status", None), "state", "SUCCESS"),
                "payload": dumped,
            }
        return RuntimeEnvelope(**dumped)
    return RuntimeEnvelope(**result)


async def search_reality(
    query: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await reality_compass(input=query, mode="search", session_id=session_id, ctx=ctx, **kwargs)


async def ingest_evidence(
    url: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await reality_compass(input=url, mode="fetch", session_id=session_id, ctx=ctx, **kwargs)


async def agentzero_engineer(
    task: str | None = None,
    task_description: str | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    payload = {"task": task or task_description or "", **kwargs}
    return await _wrap_call("agentzero_engineer", Stage.MEMORY_555, session_id, payload, ctx)


async def agentzero_validate(
    input_to_validate: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    payload = {"input_to_validate": input_to_validate, **kwargs}
    return await _wrap_call("agentzero_validate", Stage.JUDGE_888, session_id, payload, ctx)


async def agentzero_armor_scan(
    content: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("agentzero_armor_scan", Stage.JUDGE_888, session_id, {"content": content, **kwargs}, ctx)


async def agentzero_hold_check(
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("agentzero_hold_check", Stage.JUDGE_888, session_id, kwargs, ctx)


async def agentzero_memory_query(
    query: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await _wrap_call("agentzero_memory_query", Stage.MEMORY_555, session_id, {"query": query, **kwargs}, ctx)


async def reality_atlas(
    operation: str = "merge",
    session_id: str | None = None,
    bundles: list[dict[str, Any]] | None = None,
    query: dict[str, Any] | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    payload = {"operation": operation, "bundles": bundles or [], "query": query or {}, **kwargs}
    return await _wrap_call("reality_atlas", Stage.REALITY_222, session_id, payload, ctx)


async def seal_vault_commit(
    verdict: str = "SEAL",
    evidence: Any | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
    **kwargs,
) -> RuntimeEnvelope:
    return await vault_seal(verdict=verdict, evidence=evidence, session_id=session_id, ctx=ctx, **kwargs)


INIT_ANCHOR = init_anchor
AGI_REASON = agi_reason
AGI_REFLECT = agi_reflect
ASI_CRITIQUE = asi_critique
ASI_SIMULATE = asi_simulate
APEX_JUDGE = apex_judge
VAULT_SEAL = vault_seal

# ─── Mapping ───
FINAL_TOOL_IMPLEMENTATIONS: dict[str, Callable] = {
    "init_anchor": init_anchor,
    "arifOS_kernel": arifOS_kernel,
    "apex_soul": apex_soul,
    "vault_ledger": vault_ledger,
    "agi_mind": agi_mind,
    "asi_heart": asi_heart,
    "engineering_memory": engineering_memory,
    "physics_reality": physics_reality,
    "math_estimator": math_estimator,
    "code_engine": code_engine,
    "architect_registry": architect_registry,
}

LEGACY_COMPAT_MAP: dict[str, Callable] = {
    "metabolic_loop_router": metabolic_loop_router,
    "arifos_kernel": arifos_kernel,
    "check_vital": check_vital,
    "audit_rules": audit_rules,
    "init_anchor_state": init_anchor_state,
    "get_caller_status": get_caller_status,
    "agi_reason": agi_reason,
    "agi_reflect": agi_reflect,
    "asi_critique": asi_critique,
    "asi_simulate": asi_simulate,
    "apex_judge": apex_judge,
    "vault_seal": vault_seal,
    "verify_vault_ledger": verify_vault_ledger,
    "reality_compass": reality_compass,
    "reality_atlas": reality_atlas,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "agentzero_engineer": agentzero_engineer,
    "agentzero_validate": agentzero_validate,
    "agentzero_armor_scan": agentzero_armor_scan,
    "agentzero_hold_check": agentzero_hold_check,
    "agentzero_memory_query": agentzero_memory_query,
    "seal_vault_commit": seal_vault_commit,
    "forge": forge_legacy,
}

ALL_TOOL_IMPLEMENTATIONS = {**FINAL_TOOL_IMPLEMENTATIONS, **LEGACY_COMPAT_MAP}

def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register canonical mega-tools and deprecated legacy aliases."""
    specs = {spec.name: spec for spec in _public_tool_specs_fn()}

    for name, handler in FINAL_TOOL_IMPLEMENTATIONS.items():
        spec = specs.get(name)
        mcp.tool(
            name=name,
            description=spec.description if spec else name,
        )(handler)

    def _make_legacy_shim(alias: str, mega_tool: str, mode: str) -> Callable[..., Any]:
        async def _shim(
            query: str | None = None,
            session_id: str | None = None,
            actor_id: str | None = None,
            intent: Any | None = None,
            url: str | None = None,
            content: str | None = None,
            spec: str | None = None,
            path: str | None = None,
            uri: str | None = None,
            verdict: str | None = None,
            evidence: Any | None = None,
            auth_context: dict[str, Any] | None = None,
            risk_tier: str = "medium",
            dry_run: bool = True,
            allow_execution: bool = False,
            ctx: Context | None = None,
        ) -> RuntimeEnvelope:
            payload = {
                "query": query,
                "session_id": session_id,
                "actor_id": actor_id,
                "intent": intent,
                "url": url,
                "content": content,
                "spec": spec,
                "path": path,
                "uri": uri,
                "verdict": verdict,
                "evidence": evidence,
            }
            payload = {key: value for key, value in payload.items() if value is not None}
            handler = FINAL_TOOL_IMPLEMENTATIONS[mega_tool]
            if mega_tool == "arifOS_kernel":
                return await handler(
                    mode=mode,
                    payload=payload,
                    auth_context=auth_context,
                    risk_tier=risk_tier,
                    dry_run=dry_run,
                    allow_execution=allow_execution,
                    ctx=ctx,
                )
            return await handler(
                mode=mode,
                payload=payload,
                auth_context=auth_context,
                risk_tier=risk_tier,
                dry_run=dry_run,
                ctx=ctx,
            )

        _shim.__name__ = f"{alias}_shim"
        return _shim

    for legacy_name, target in CAPABILITY_MAP.items():
        if legacy_name in FINAL_TOOL_IMPLEMENTATIONS:
            continue
        shim = _make_legacy_shim(legacy_name, target.mega_tool, target.mode)
        note = f" {target.note}" if target.note else ""
        mcp.tool(
            name=legacy_name,
            description=f"[DEPRECATED] Routes to {target.mega_tool} mode='{target.mode}'.{note}",
        )(shim)


class _CallableList(list):
    def __call__(self) -> list[Any]:
        return list(self)


public_tool_names = _CallableList(_public_tool_names_fn())
public_tool_specs = _CallableList(_public_tool_specs_fn())
