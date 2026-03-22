from __future__ import annotations
from arifosmcp.runtime.tools_hardened_dispatch import HARDENED_DISPATCH_MAP
import asyncio
import logging
import uuid
from typing import Any, Callable, Dict, Union
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context
from arifosmcp.capability_map import CAPABILITY_MAP
from arifosmcp.runtime.bridge import call_kernel
from arifosmcp.runtime.governance_identities import (
    PROTECTED_SOVEREIGN_IDS,
    is_protected_sovereign_id,
    validate_sovereign_proof,
)
from arifosmcp.runtime.models import (
    ArifOSError,
    CallerContext,
    CanonicalError,
    RuntimeEnvelope,
    RuntimeStatus,
    Stage,
    UserModel,
    UserModelField,
    UserModelSource,
    Verdict,
    PersonaId,
    ClaimStatus,
    AuthorityLevel,
)
from arifosmcp.runtime.public_registry import (
    public_tool_names as _registry_tool_names,
    public_tool_spec_by_name as _registry_tool_spec_by_name,
    public_tool_specs as _registry_tool_specs,
)
from arifosmcp.runtime.tool_specs import (
    MegaToolName,
    ToolSpec,
)
from arifosmcp.runtime.reality_handlers import handler as reality_handler
from arifosmcp.runtime.reality_models import BundleInput
from arifosmcp.runtime.sessions import (
    _resolve_session_id,
    get_session_identity,
    resolve_runtime_context,
    set_active_session,
)
from arifosmcp.runtime.schemas import IntentType
from arifosmcp.runtime.tools_internal import (
    agi_mind_dispatch_impl,
    apex_soul_dispatch_impl,
    architect_registry_dispatch_impl,
    arifos_kernel_impl,
    asi_heart_dispatch_impl,
    code_engine_dispatch_impl,
    engineering_memory_dispatch_impl,
    get_caller_status_impl,
    init_anchor_impl,
    math_estimator_dispatch_impl,
    physics_reality_dispatch_impl,
    refresh_anchor_impl,
    revoke_anchor_state_impl,
    vault_ledger_dispatch_impl,
)
logger = logging.getLogger(__name__)
# P0: Helper function to check for valid cryptographic proof
def _has_valid_proof(payload: dict[str, Any], actor_id: str) -> bool:
    """Check if payload contains valid cryptographic proof for protected ID."""
    proof = payload.get("auth_token") or payload.get("proof") or payload.get("signature")
    if isinstance(proof, dict):
        return validate_sovereign_proof(actor_id, proof)
    return False
def select_governed_philosophy(
    context: str,
    *,
    stage: str,
    verdict: str,
    g_score: float = 1.0,
    failed_floors: list[str] = None,
    session_id: str = "global",
) -> dict[str, Any]:
    """Provides a constitutional philosophy snippet for any stage result."""
    from arifosmcp.runtime.philosophy import select_governed_philosophy as _select
    return _select(
        context=context,
        stage=stage,
        verdict=verdict,
        g_score=g_score,
        failed_floors=failed_floors,
        session_id=session_id,
    )
_public_tool_names_fn = _registry_tool_names
_public_tool_specs_fn = _registry_tool_specs
_public_tool_spec_by_name_fn = _registry_tool_spec_by_name
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
    resolved = _resolve_session_id(session_id)
    if resolved and str(resolved).strip():
        return str(resolved).strip()
    minted = f"session-{uuid.uuid4().hex[:8]}"
    set_active_session(minted)
    return minted
async def init_anchor(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "init_anchor" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "init_anchor" == "init_anchor" else "init_anchor"
        res = await HARDENED_DISPATCH_MAP["init_anchor"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    # P0: Unification Dispatch — The Ignition State of Intelligence
    # Consolidates: init, state, status, revoke, refresh into ONE tool
    effective_mode = mode or (payload.get("mode") if payload else "init")
    effective_intent = intent or raw_input or (payload.get("intent") if payload else None)
    effective_session = session_id or (payload.get("session_id") if payload else None)
    effective_human_approval = human_approval or (payload.get("human_approval") if payload else False)
    effective_proof = proof or (payload.get("proof") if payload else None)
    # Handle legacy tool routing through capability_map
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
        payload=payload
    )
async def arifOS_kernel(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "arifOS_kernel" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "arifOS_kernel" == "init_anchor" else "arifOS_kernel"
        res = await HARDENED_DISPATCH_MAP["arifOS_kernel"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    del caller_context
    ctx = ctx or CurrentContext()
    if mode is None:
        mode = "kernel"
        payload = {"query": query or "", "session_id": session_id, "intent": intent}
    payload = dict(payload or {})
    payload["session_id"] = _normalize_session_id(payload.get("session_id") or session_id)
    if intent and not payload.get("intent"):
        payload["intent"] = intent
    if mode == "kernel":
        return await arifos_kernel_impl(
            query=payload.get("query", query or ""),
            risk_tier=payload.get("risk_tier", risk_tier),
            auth_context=payload.get("auth_context", auth_context),
            dry_run=bool(payload.get("dry_run", dry_run)),
            allow_execution=bool(payload.get("allow_execution", allow_execution)),
            session_id=payload.get("session_id"),
            ctx=ctx,
            intent=payload.get("intent"),
        )
    if mode == "status":
        return await get_caller_status_impl(session_id=payload.get("session_id"), ctx=ctx)
    raise ValueError(f"Invalid mode for arifOS_kernel: {mode}")
async def apex_soul(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "apex_soul" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "apex_soul" == "init_anchor" else "apex_soul"
        res = await HARDENED_DISPATCH_MAP["apex_soul"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await apex_soul_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def vault_ledger(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "vault_ledger" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "vault_ledger" == "init_anchor" else "vault_ledger"
        res = await HARDENED_DISPATCH_MAP["vault_ledger"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await vault_ledger_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def agi_mind(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "agi_mind" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "agi_mind" == "init_anchor" else "agi_mind"
        res = await HARDENED_DISPATCH_MAP["agi_mind"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await agi_mind_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def asi_heart(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "asi_heart" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "asi_heart" == "init_anchor" else "asi_heart"
        res = await HARDENED_DISPATCH_MAP["asi_heart"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await asi_heart_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def engineering_memory(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "engineering_memory" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "engineering_memory" == "init_anchor" else "engineering_memory"
        res = await HARDENED_DISPATCH_MAP["engineering_memory"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await engineering_memory_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def physics_reality(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "physics_reality" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "physics_reality" == "init_anchor" else "physics_reality"
        res = await HARDENED_DISPATCH_MAP["physics_reality"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await physics_reality_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def math_estimator(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "math_estimator" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "math_estimator" == "init_anchor" else "math_estimator"
        res = await HARDENED_DISPATCH_MAP["math_estimator"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await math_estimator_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def code_engine(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "code_engine" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "code_engine" == "init_anchor" else "code_engine"
        res = await HARDENED_DISPATCH_MAP["code_engine"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await code_engine_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
async def architect_registry(
    mode: str | None = None,
    payload: dict[str, Any] | None = None,
    query: str | None = None,
    session_id: str | None = None,
    actor_id: str | None = None,
    declared_name: str | None = None,
    intent: Any | None = None,
    human_approval: bool = False,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Any | None = None,
) -> RuntimeEnvelope:
    # P0: Unified ABI Adapter (Hardened)
    payload = dict(payload or {})

    if query: payload.setdefault("query", query)
    if session_id: payload.setdefault("session_id", session_id)
    if actor_id: payload.setdefault("actor_id", actor_id)
    if intent: payload.setdefault("intent", intent)
    if human_approval: payload.setdefault("human_approval", human_approval)
    # Hardened Dispatch
    if "architect_registry" in HARDENED_DISPATCH_MAP:
        if mode is None: mode = "init" if "architect_registry" == "init_anchor" else "architect_registry"
        res = await HARDENED_DISPATCH_MAP["architect_registry"](mode=mode, payload=payload)
        # Wrap in envelope if not already (legacy compatibility)
        if isinstance(res, dict) and "ok" in res:
            from arifosmcp.runtime.models import RuntimeEnvelope, RuntimeStatus, Verdict
            return RuntimeEnvelope(
                status=RuntimeStatus.SUCCESS if res.get("ok") else RuntimeStatus.ERROR,
                verdict=Verdict.SEAL if res.get("ok") else Verdict.VOID,
                payload=res
            )
        return res
    resolved_payload = dict(payload or {})
    return await architect_registry_dispatch_impl(
        mode=mode,
        payload=resolved_payload,
        auth_context=resolved_payload.get("auth_context", auth_context),
        risk_tier=resolved_payload.get("risk_tier", risk_tier),
        dry_run=bool(resolved_payload.get("dry_run", dry_run)),
        ctx=ctx or CurrentContext(),
    )
def _build_user_model(
    tool_name: str, stage_value: str, payload: dict[str, Any], envelope_data: dict[str, Any]
) -> UserModel:
    query = str(
        payload.get("query") or payload.get("intent") or payload.get("content") or ""
    ).strip()
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
                value="state_that_execution_is_simulated", source=UserModelSource.OBSERVABLE
            )
        )
    return UserModel(
        stated_goal=UserModelField(
            value=query or context or f"{tool_name}:{stage_value}", source=UserModelSource.EXPLICIT
        ),
        output_constraints=output_constraints,
    )
def _resolve_caller_context(
    caller_context: CallerContext | None, requested_persona: str | None
) -> CallerContext:
    base = caller_context or CallerContext()
    if requested_persona:
        try:
            base.persona_id = PersonaId(requested_persona.lower())
        except (ValueError, AttributeError):
            pass
    return base
def _resolve_caller_state(session_id: str, authority: Any) -> tuple[str, list[str], list[dict[str, str]]]:
    """Single source of truth for caller state resolution."""
    from .tools_internal import _resolve_caller_state as _resolve
    return _resolve(session_id, authority)
async def _wrap_call(
    tool_name: str,
    stage: Stage,
    session_id: str | None,
    payload: dict[str, Any],
    ctx: Context | None = None,
    caller_context: CallerContext | None = None,
) -> RuntimeEnvelope:
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
    except Exception as exc:
        logger.error("wrap_call failure: %s", exc, exc_info=True)
        envelope = RuntimeEnvelope(
            ok=False,
            tool=tool_name,
            session_id=normalized_session,
            stage=stage.value,
            verdict=Verdict.SABAR,
            status=RuntimeStatus.ERROR,
            errors=[CanonicalError(code="RUNTIME_FAILURE", message=str(exc), stage=stage.value)],
        )
    if envelope.user_model is None:
        envelope.user_model = _build_user_model(
            tool_name, envelope.stage, payload, envelope.model_dump(mode="json")
        )
    envelope.tool = tool_name
    envelope.session_id = normalized_session
    envelope.caller_state, envelope.allowed_next_tools, envelope.blocked_tools = (
        _resolve_caller_state(
            normalized_session,
            getattr(envelope, "authority", None),
        )
    )
    # ── Philosophy Injection (APEX-G) ──
    # Wire the 33-quote rich wisdom layer to every tool output.
    g_score = 1.0
    if envelope.metrics and envelope.metrics.telemetry:
        g_score = envelope.metrics.telemetry.G_star
    failed_codes = [e.code for e in envelope.errors if str(e.code).startswith("F")]
    # If this is an init call, we want to reflect the resolve status in the philosophy
    effective_stage = envelope.stage
    effective_verdict = str(envelope.verdict.value) if hasattr(envelope.verdict, "value") else str(envelope.verdict)
    # Force deep contrast for 000_INIT failures
    if effective_stage == "000_INIT" and envelope.verdict == Verdict.VOID:
        g_score = 0.33 # Force humility quote
    envelope.philosophy = select_governed_philosophy(
        context=str(
            payload.get("query")
            or payload.get("intent")
            or payload.get("content")
            or payload.get("spec")
            or tool_name
        ),
        stage=effective_stage,
        verdict=effective_verdict,
        g_score=g_score,
        failed_floors=failed_codes,
        session_id=normalized_session,
    )
    # Final ABI Alignment: Sync flags from payload to authority if they were explicitly confirmed
    if envelope.authority:
        envelope.authority.human_required = not bool(envelope.payload.get("human_approval_persisted", False))
    return envelope
async def metabolic_loop_router(
    query: str,
    session_id: str | None = None,
    risk_tier: str = "medium",
    caller_context: CallerContext | None = None,
    requested_persona: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    resolved_caller = _resolve_caller_context(caller_context, requested_persona)
    payload = {
        "query": query,
        "session_id": session_id,
        "risk_tier": risk_tier,
        "caller_context": resolved_caller,
        "auth_context": auth_context,
        **kwargs,
    }
    return await _wrap_call(
        "arifOS_kernel", Stage.ROUTER_444, session_id, payload, caller_context=resolved_caller
    )
async def check_vital(session_id: str = "global", **kwargs: Any) -> RuntimeEnvelope:
    envelope = await _wrap_call(
        "check_vital", Stage.INIT_000, session_id, {"session_id": session_id, **kwargs}
    )
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
async def audit_rules(session_id: str = "global", **kwargs: Any) -> RuntimeEnvelope:
    return await _wrap_call(
        "audit_rules", Stage.JUDGE_888, session_id, {"session_id": session_id, **kwargs}
    )
async def anchor_session(**kwargs: Any) -> RuntimeEnvelope:
    return await init_anchor(mode="init", payload=kwargs)
async def init_anchor_state(**kwargs: Any) -> RuntimeEnvelope:
    """Legacy wrapper for unified init_anchor(mode='state')"""
    return await init_anchor(mode="state", **kwargs)
async def revoke_anchor_state(**kwargs: Any) -> RuntimeEnvelope:
    """Legacy wrapper for unified init_anchor(mode='revoke')"""
    return await init_anchor(mode="revoke", **kwargs)
async def get_caller_status(**kwargs: Any) -> RuntimeEnvelope:
    """Legacy wrapper for unified init_anchor(mode='status')"""
    return await init_anchor(mode="status", **kwargs)
async def arifos_kernel(
    query: str = "",
    session_id: str | None = None,
    risk_tier: str = "medium",
    dry_run: bool = False,
    debug: bool = False,
) -> RuntimeEnvelope:
    return await metabolic_loop_router(
        query=query,
        session_id=session_id,
        risk_tier=risk_tier,
        dry_run=dry_run,
        debug=debug,
        **kwargs,
    )
async def forge_legacy(
    spec: str, session_id: str = "global", dry_run: bool = False, **kwargs: Any
) -> RuntimeEnvelope:
    return await agi_mind(
        mode="forge",
        payload={"query": spec, "session_id": session_id, "dry_run": dry_run, **kwargs},
    )
async def forge(
    spec: str,
    session_id: str = "global",
    dry_run: bool = False,
    risk_tier: str = "medium",
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
) -> RuntimeEnvelope:
    payload = {"topic": topic, "content": content or topic, **kwargs}
    return await _wrap_call("agi_reflect", Stage.MEMORY_555, session_id, payload, ctx)
async def reason_mind(**kwargs: Any) -> RuntimeEnvelope:
    return await agi_reason(**kwargs)
async def reason_mind_synthesis(**kwargs: Any) -> RuntimeEnvelope:
    return await agi_reason(**kwargs)
async def integrate_analyze_reflect(**kwargs: Any) -> RuntimeEnvelope:
    return await agi_reason(**kwargs)
async def agi_asi_forge_handler(
    spec: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    payload = {"spec": spec, **kwargs}
    return await _wrap_call("agi_asi_forge_handler", Stage.FORGE_777, session_id, payload, ctx)
async def asi_simulate(
    scenario: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call(
        "asi_simulate", Stage.HEART_666, session_id, {"scenario": scenario, **kwargs}, ctx
    )
async def asi_critique(
    draft_output: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call(
        "asi_critique",
        Stage.CRITIQUE_666,
        session_id,
        {"draft_output": draft_output, **kwargs},
        ctx,
    )
async def apex_judge(
    candidate_output: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call(
        "apex_judge",
        Stage.JUDGE_888,
        session_id,
        {"candidate_output": candidate_output, **kwargs},
        ctx,
    )
async def vault_seal(
    verdict: str = "SEAL",
    evidence: Any | None = None,
    summary: str | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    payload = {"verdict": verdict, "evidence": evidence or summary, **kwargs}
    return await _wrap_call("vault_seal", Stage.VAULT_999, session_id, payload, ctx)
async def verify_vault_ledger(
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call("verify_vault_ledger", Stage.VAULT_999, session_id, kwargs, ctx)
async def reality_compass(
    input: str,
    session_id: str | None = None,
    ctx: Context | None = None,
    mode: str = "compass",
    policy: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    if mode == "search":
        result = await reality_handler.handle_compass(
            BundleInput(type="query", value=input, mode="search"), {}
        )
    elif mode == "fetch":
        result = await reality_handler.handle_compass(
            BundleInput(type="url", value=input, mode="fetch"), {}
        )
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
) -> RuntimeEnvelope:
    return await reality_compass(
        input=query, mode="search", session_id=session_id, ctx=ctx, **kwargs
    )
async def ingest_evidence(
    url: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await reality_compass(input=url, mode="fetch", session_id=session_id, ctx=ctx, **kwargs)
async def system_health(**kwargs: Any) -> RuntimeEnvelope:
    return await math_estimator(mode="health", payload=kwargs)
async def cost_estimator(**kwargs: Any) -> RuntimeEnvelope:
    return await math_estimator(mode="cost", payload=kwargs)
async def fs_inspect(**kwargs: Any) -> RuntimeEnvelope:
    return await code_engine(mode="fs", payload=kwargs)
async def process_list(**kwargs: Any) -> RuntimeEnvelope:
    return await code_engine(mode="process", payload=kwargs)
async def net_status(**kwargs: Any) -> RuntimeEnvelope:
    return await code_engine(mode="net", payload=kwargs)
async def log_tail(**kwargs: Any) -> RuntimeEnvelope:
    return await code_engine(mode="tail", payload=kwargs)
async def trace_replay(**kwargs: Any) -> RuntimeEnvelope:
    return await code_engine(mode="replay", payload=kwargs)
async def agentzero_engineer(
    task: str | None = None,
    task_description: str | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    payload = {"task": task or task_description or "", **kwargs}
    return await _wrap_call("agentzero_engineer", Stage.MEMORY_555, session_id, payload, ctx)
async def agentzero_validate(
    input_to_validate: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    payload = {"input_to_validate": input_to_validate, **kwargs}
    return await _wrap_call("agentzero_validate", Stage.JUDGE_888, session_id, payload, ctx)
async def agentzero_armor_scan(
    content: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call(
        "agentzero_armor_scan", Stage.JUDGE_888, session_id, {"content": content, **kwargs}, ctx
    )
async def agentzero_hold_check(
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call("agentzero_hold_check", Stage.JUDGE_888, session_id, kwargs, ctx)
async def agentzero_memory_query(
    query: str,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await _wrap_call(
        "agentzero_memory_query", Stage.MEMORY_555, session_id, {"query": query, **kwargs}, ctx
    )
async def chroma_query(**kwargs: Any) -> RuntimeEnvelope:
    return await agentzero_memory_query(**kwargs)
async def reality_atlas(
    operation: str = "merge",
    session_id: str | None = None,
    bundles: list[dict[str, Any]] | None = None,
    query: dict[str, Any] | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    payload = {"operation": operation, "bundles": bundles or [], "query": query or {}, **kwargs}
    return await _wrap_call("reality_atlas", Stage.REALITY_222, session_id, payload, ctx)
async def seal_vault_commit(
    verdict: str = "SEAL",
    evidence: Any | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    return await vault_seal(
        verdict=verdict, evidence=evidence, session_id=session_id, ctx=ctx, **kwargs
    )
async def open_apex_dashboard(**kwargs: Any) -> RuntimeEnvelope:
    return await apex_soul(mode="rules", payload=kwargs)
INIT_ANCHOR = init_anchor
AGI_REASON = agi_reason
AGI_REFLECT = agi_reflect
ASI_CRITIQUE = asi_critique
ASI_SIMULATE = asi_simulate
APEX_JUDGE = apex_judge
VAULT_SEAL = vault_seal
FINAL_TOOL_IMPLEMENTATIONS: dict[str, Callable[..., Any]] = {
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
LEGACY_COMPAT_MAP: dict[str, Callable[..., Any]] = {
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
    "reason_mind_synthesis": reason_mind_synthesis,
    "agi_asi_forge_handler": agi_asi_forge_handler,
}
ALL_TOOL_IMPLEMENTATIONS = {**FINAL_TOOL_IMPLEMENTATIONS, **LEGACY_COMPAT_MAP}
def _build_legacy_payload(mega_tool: str, mode: str, values: dict[str, Any]) -> dict[str, Any]:
    payload = {key: value for key, value in values.items() if value is not None}
    if mega_tool == "apex_soul":
        candidate = (
            payload.get("candidate")
            or payload.get("candidate_output")
            or payload.get("input_to_validate")
            or payload.get("content")
            or payload.get("query")
        )
        if candidate is not None:
            payload.setdefault("candidate", candidate)
    elif mega_tool == "asi_heart":
        content = (
            payload.get("content")
            or payload.get("draft_output")
            or payload.get("scenario")
            or payload.get("query")
        )
        if content is not None:
            payload.setdefault("content", content)
    elif mega_tool == "physics_reality":
        input_value = payload.get("input")
        if input_value is None:
            if mode == "ingest":
                input_value = payload.get("url") or payload.get("query") or payload.get("content")
            else:
                input_value = payload.get("query") or payload.get("content") or payload.get("url")
        if input_value is not None:
            payload.setdefault("input", input_value)
    elif mega_tool == "engineering_memory":
        task = payload.get("task") or payload.get("task_description")
        if task is not None:
            payload.setdefault("task", task)
    elif mega_tool == "vault_ledger":
        if payload.get("summary") is not None and payload.get("evidence") is None:
            payload["evidence"] = payload["summary"]
    elif mega_tool == "arifOS_kernel":
        payload.setdefault("query", "")
    return payload
def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    del profile
    specs = {spec.name: spec for spec in _public_tool_specs_fn()}
    for name, handler in FINAL_TOOL_IMPLEMENTATIONS.items():
        spec = specs.get(name)
        mcp.tool(name=name, description=spec.description if spec else name)(handler)
    def _make_legacy_shim(alias: str, mega_tool: str, mode: str) -> Callable[..., Any]:
        async def _shim(
            query: str | None = None,
            session_id: str | None = None,
            actor_id: str | None = None,
            declared_name: str | None = None,  # P0: ABI v1.0 Identity
            intent: IntentType = None,         # P0: ABI v1.0 Structured Intent
            human_approval: bool = False,      # P0: ABI v1.0 Sovereign Flag
            url: str | None = None,
            content: str | None = None,
            spec: str | None = None,
            path: str | None = None,
            uri: str | None = None,
            verdict: str | None = None,
            evidence: Any | None = None,
            summary: str | None = None,
            task: str | None = None,
            task_description: str | None = None,
            input_to_validate: str | None = None,
            candidate_output: str | None = None,
            draft_output: str | None = None,
            scenario: str | None = None,
            operation: str | None = None,
            bundles: list[dict[str, Any]] | None = None,
            hold_id: str | None = None,
            full_scan: bool | None = None,
            auth_context: dict[str, Any] | None = None,
            caller_context: dict[str, Any] | None = None,  # P0: ABI v1.0 Context
            risk_tier: str = "medium",
            dry_run: bool = True,
            allow_execution: bool = False,
            ctx: Context | None = None,
        ) -> RuntimeEnvelope:
            payload = _build_legacy_payload(
                mega_tool,
                mode,
                {
                    "query": query,
                    "session_id": session_id,
                    "actor_id": actor_id,
                    "declared_name": declared_name,
                    "intent": intent,
                    "human_approval": human_approval,
                    "url": url,
                    "content": content,
                    "spec": spec,
                    "path": path,
                    "uri": uri,
                    "verdict": verdict,
                    "evidence": evidence,
                    "summary": summary,
                    "task": task,
                    "task_description": task_description,
                    "input_to_validate": input_to_validate,
                    "candidate_output": candidate_output,
                    "draft_output": draft_output,
                    "scenario": scenario,
                    "operation": operation,
                    "bundles": bundles,
                    "hold_id": hold_id,
                    "full_scan": full_scan,
                },
            )
            handler = FINAL_TOOL_IMPLEMENTATIONS[mega_tool]
            # P0: Hardened Dispatch Integration
            if mega_tool in HARDENED_DISPATCH_MAP:
                hardened_handler = HARDENED_DISPATCH_MAP[mega_tool]
                # Combine gov_params if needed, but for now we dispatch directly
                return await hardened_handler(mode=mode, payload=payload)
            # P0: Governance Parameter Extraction
            # Ensure governance flags are passed explicitly if the handler accepts them
            gov_params = {}
            if mega_tool == "init_anchor":
                gov_params = {
                    "actor_id": actor_id or declared_name,
                    "declared_name": declared_name,
                    "intent": intent,
                    "human_approval": human_approval,
                    "session_id": session_id,
                    # CallerContext expects a model, but we might receive a dict from MCP
                    "caller_context": caller_context,
                }
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
            if mega_tool == "init_anchor" and mode == "init":
                return await handler(
                    mode=mode,
                    auth_context=auth_context,
                    risk_tier=risk_tier,
                    dry_run=dry_run,
                    ctx=ctx,
                    **gov_params,
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
    # P0: DEPRECATED TOOLS REMOVED FROM PUBLIC REGISTRY
    # Legacy shims remain available for internal routing via CAPABILITY_MAP
    # but are no longer registered as public MCP tools to clean up the surface.
    pass
class _CallableList(list):
    def __call__(self) -> list[Any]:
        return list(self)
public_tool_names = _CallableList(_public_tool_names_fn())
public_tool_specs = _CallableList(_public_tool_specs_fn())
public_tool_spec_by_name = _public_tool_spec_by_name_fn