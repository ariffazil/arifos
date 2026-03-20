from __future__ import annotations

import logging
from typing import Any, Callable

try:
    from fastmcp.dependencies import CurrentContext
    _has_ctx = True
except ImportError:
    _has_ctx = False
    def CurrentContext(): return None

from arifosmcp.runtime.models import (
    RuntimeEnvelope,
    Stage,
    Verdict,
    RuntimeStatus,
    CanonicalError,
    CallerContext,
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

def _normalize_session_id(session_id: str | None) -> str:
    if session_id and str(session_id).strip():
        return str(session_id).strip()
    return "global"

# =============================================================================
# ⚖️ THE 11 GOVERNED MEGA-TOOLS (STRICT SIGNATURES)
# =============================================================================

async def init_anchor(
    mode: str = "init",
    payload: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """000_INIT: Establish, revoke, or refresh a governed session identity."""
    p = payload or {}
    sid = _normalize_session_id(p.get("session_id"))
    ctx = CurrentContext()
    if mode == "init": return await init_anchor_impl(p.get("actor_id", "anonymous"), p.get("intent"), sid, ctx)
    elif mode == "revoke": return await revoke_anchor_state_impl(sid, p.get("reason") or "Unspecified", ctx)
    elif mode == "refresh": return await refresh_anchor_impl(sid, ctx)
    raise ValueError(f"Invalid mode for init_anchor: {mode}")

async def arifOS_kernel(
    mode: str = "kernel",
    payload: dict[str, Any] | None = None,
) -> RuntimeEnvelope:
    """444_ROUTER: One canonical orchestration path for reasoning and routed execution."""
    p = payload or {}
    sid = _normalize_session_id(p.get("session_id"))
    ctx = CurrentContext()
    if mode == "kernel": return await arifos_kernel_impl(p.get("query", ""), p.get("risk_tier", "medium"), p.get("auth_context"), bool(p.get("dry_run", True)), bool(p.get("allow_execution", False)), sid, ctx)
    elif mode == "status": return await get_caller_status_impl(sid, ctx)
    raise ValueError(f"Invalid mode for arifOS_kernel: {mode}")

async def apex_soul(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await apex_soul_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def vault_ledger(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await vault_ledger_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def agi_mind(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await agi_mind_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def asi_heart(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await asi_heart_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def engineering_memory(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await engineering_memory_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)))

async def physics_reality(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await physics_reality_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def math_estimator(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await math_estimator_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def code_engine(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await code_engine_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

async def architect_registry(mode: str, payload: dict[str, Any]) -> RuntimeEnvelope:
    return await architect_registry_dispatch_impl(mode, payload, payload.get("auth_context"), payload.get("risk_tier", "medium"), bool(payload.get("dry_run", True)), CurrentContext())

# -----------------------------------------------------------------------------
# LEGACY COMPATIBILITY SHIMS (Exported for tests)
# -----------------------------------------------------------------------------

async def arifos_kernel(**kwargs) -> RuntimeEnvelope: return await arifOS_kernel(mode="kernel", payload=kwargs)
async def check_vital(**kwargs) -> RuntimeEnvelope: return await math_estimator(mode="vitals", payload=kwargs)
async def audit_rules(**kwargs) -> RuntimeEnvelope: return await apex_soul(mode="rules", payload=kwargs)
async def anchor_session(**kwargs) -> RuntimeEnvelope: return await init_anchor(mode="init", payload=kwargs)
async def init_anchor_state(**kwargs) -> RuntimeEnvelope: return await init_anchor(mode="init", payload=kwargs)
async def revoke_anchor_state(**kwargs) -> RuntimeEnvelope: return await init_anchor(mode="revoke", payload=kwargs)
async def get_caller_status(**kwargs) -> RuntimeEnvelope: return await arifOS_kernel(mode="status", payload=kwargs)
async def metabolic_loop(**kwargs) -> RuntimeEnvelope: return await arifOS_kernel(mode="kernel", payload=kwargs)

async def agi_reason(**kwargs) -> RuntimeEnvelope: return await agi_mind(mode="reason", payload=kwargs)
async def agi_reflect(**kwargs) -> RuntimeEnvelope: return await agi_mind(mode="reflect", payload=kwargs)
async def forge(**kwargs) -> RuntimeEnvelope: return await agi_mind(mode="forge", payload=kwargs)
async def reason_mind(**kwargs) -> RuntimeEnvelope: return await agi_mind(mode="reason", payload=kwargs)
async def reason_mind_synthesis(**kwargs) -> RuntimeEnvelope: return await agi_mind(mode="reason", payload=kwargs)
async def integrate_analyze_reflect(**kwargs) -> RuntimeEnvelope: return await agi_mind(mode="reason", payload=kwargs)

async def asi_critique(**kwargs) -> RuntimeEnvelope: return await asi_heart(mode="critique", payload=kwargs)
async def asi_simulate(**kwargs) -> RuntimeEnvelope: return await asi_heart(mode="simulate", payload=kwargs)
async def search_reality(**kwargs) -> RuntimeEnvelope: return await physics_reality(mode="search", payload=kwargs)
async def ingest_evidence(**kwargs) -> RuntimeEnvelope: return await physics_reality(mode="ingest", payload=kwargs)
async def reality_compass(**kwargs) -> RuntimeEnvelope: return await physics_reality(mode="compass", payload=kwargs)
async def reality_atlas(**kwargs) -> RuntimeEnvelope: return await physics_reality(mode="atlas", payload=kwargs)
async def system_health(**kwargs) -> RuntimeEnvelope: return await math_estimator(mode="health", payload=kwargs)
async def cost_estimator(**kwargs) -> RuntimeEnvelope: return await math_estimator(mode="cost", payload=kwargs)
async def fs_inspect(**kwargs) -> RuntimeEnvelope: return await code_engine(mode="fs", payload=kwargs)
async def process_list(**kwargs) -> RuntimeEnvelope: return await code_engine(mode="process", payload=kwargs)
async def net_status(**kwargs) -> RuntimeEnvelope: return await code_engine(mode="net", payload=kwargs)
async def log_tail(**kwargs) -> RuntimeEnvelope: return await code_engine(mode="tail", payload=kwargs)
async def trace_replay(**kwargs) -> RuntimeEnvelope: return await code_engine(mode="replay", payload=kwargs)
async def agentzero_engineer(**kwargs) -> RuntimeEnvelope: return await engineering_memory(mode="engineer", payload=kwargs)
async def agentzero_memory_query(**kwargs) -> RuntimeEnvelope: return await engineering_memory(mode="query", payload=kwargs)
async def chroma_query(**kwargs) -> RuntimeEnvelope: return await engineering_memory(mode="query", payload=kwargs)
async def apex_judge(**kwargs) -> RuntimeEnvelope: return await apex_soul(mode="judge", payload=kwargs)
async def agentzero_validate(**kwargs) -> RuntimeEnvelope: return await apex_soul(mode="validate", payload=kwargs)
async def agentzero_hold_check(**kwargs) -> RuntimeEnvelope: return await apex_soul(mode="hold", payload=kwargs)
async def agentzero_armor_scan(**kwargs) -> RuntimeEnvelope: return await apex_soul(mode="armor", payload=kwargs)
async def open_apex_dashboard(**kwargs) -> RuntimeEnvelope: return await apex_soul(mode="rules", payload=kwargs)
async def vault_seal(**kwargs) -> RuntimeEnvelope: return await vault_ledger(mode="seal", payload=kwargs)
async def verify_vault_ledger(**kwargs) -> RuntimeEnvelope: return await vault_ledger(mode="verify", payload=kwargs)

async def metabolic_loop_router(query: str, session_id: str | None = None, **kwargs) -> RuntimeEnvelope:
    return await arifOS_kernel(mode="kernel", payload={"query": query, "session_id": session_id, **kwargs})

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

def register_tools(mcp: Any, profile: str = "full") -> None:
    for handler in FINAL_TOOL_IMPLEMENTATIONS.values():
        mcp.tool()(handler)
