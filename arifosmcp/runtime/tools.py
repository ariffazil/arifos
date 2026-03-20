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
)
from arifosmcp.runtime.public_registry import (
    public_tool_names,
    public_tool_specs,
)
from arifosmcp.runtime.sessions import (
    _resolve_session_id,
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

# =============================================================================
# ⚖️ GOVERNANCE LAYER (G-1 to G-4)
# =============================================================================

async def init_anchor(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """000_INIT: Dispatcher for identity operations."""
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
        return await refresh_anchor_impl(
            session_id=payload.get("session_id"),
            ctx=ctx
        )
    raise ValueError(f"Invalid mode for init_anchor: {mode}")

async def arifOS_kernel(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    allow_execution: bool = False,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """444_ROUTER: Dispatcher for kernel and status."""
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
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """888_JUDGE: Dispatcher for soul/verdict functions."""
    return await apex_soul_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def vault_ledger(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """999_VAULT: Dispatcher for immutable persistence."""
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
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """333_MIND: Dispatcher for reasoning and reflection."""
    return await agi_mind_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def asi_heart(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """666_HEART: Dispatcher for empathy and ethics."""
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
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """111_SENSE: Dispatcher for grounding."""
    return await physics_reality_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def math_estimator(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """Dispatcher for quantitative estimation."""
    return await math_estimator_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def code_engine(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """Dispatcher for computational execution."""
    return await code_engine_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

async def architect_registry(
    mode: str,
    payload: dict[str, Any],
    auth_context: dict[str, Any] | None = None,
    risk_tier: str = "medium",
    dry_run: bool = True,
    ctx: Context = CurrentContext(),
) -> RuntimeEnvelope:
    """Dispatcher for system definition."""
    return await architect_registry_dispatch_impl(
        mode=mode, payload=payload, auth_context=auth_context, risk_tier=risk_tier, dry_run=dry_run, ctx=ctx
    )

# -----------------------------------------------------------------------------
# LEGACY COMPATIBILITY WRAPPERS (FOR E2E/E3E TESTS)
# -----------------------------------------------------------------------------

async def metabolic_loop_router(**kwargs) -> RuntimeEnvelope:
    return await arifOS_kernel(mode="kernel", payload=kwargs)

async def check_vital(**kwargs) -> RuntimeEnvelope:
    return await math_estimator(mode="vitals", payload=kwargs)

async def audit_rules(**kwargs) -> RuntimeEnvelope:
    return await apex_soul(mode="rules", payload=kwargs)

async def init_anchor_state(**kwargs) -> RuntimeEnvelope:
    # Handle legacy 'declared_name' mapping to 'actor_id'
    actor_id = kwargs.get("declared_name") or kwargs.get("actor_id", "anonymous")
    return await init_anchor(mode="init", payload={"actor_id": actor_id, "intent": "Legacy init"})

async def get_caller_status(**kwargs) -> RuntimeEnvelope:
    return await arifOS_kernel(mode="status", payload=kwargs)

async def vault_seal(**kwargs) -> RuntimeEnvelope:
    return await vault_ledger(mode="seal", payload=kwargs)

async def verify_vault_ledger(**kwargs) -> RuntimeEnvelope:
    return await vault_ledger(mode="verify", payload=kwargs)

async def search_reality(**kwargs) -> RuntimeEnvelope:
    return await physics_reality(mode="search", payload={"input": kwargs.get("query", "")})

async def ingest_evidence(**kwargs) -> RuntimeEnvelope:
    return await physics_reality(mode="ingest", payload={"input": kwargs.get("url", "")})

async def forge_legacy(**kwargs) -> RuntimeEnvelope:
    return await agi_mind(mode="forge", payload={"query": kwargs.get("spec", "")})

async def agentzero_armor_scan(**kwargs) -> RuntimeEnvelope:
    return await apex_soul(mode="armor", payload={"candidate": kwargs.get("content", "")})

async def register_tools_legacy(**kwargs) -> dict[str, Any]:
    return {"status": "SUCCESS", "tools": public_tool_names()}

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
    "metabolic_loop": metabolic_loop_router,
    "check_vital": check_vital,
    "audit_rules": audit_rules,
    "init_anchor_state": init_anchor_state,
    "get_caller_status": get_caller_status,
    "vault_seal": vault_seal,
    "verify_vault_ledger": verify_vault_ledger,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "forge": forge_legacy,
    "agentzero_armor_scan": agentzero_armor_scan,
    "register_tools": register_tools_legacy,
}

ALL_TOOL_IMPLEMENTATIONS = {**FINAL_TOOL_IMPLEMENTATIONS, **LEGACY_COMPAT_MAP}

def register_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register exactly 11 Mega-Tools with safety profiles and versioning."""
    from .build_info import get_build_info
    build_info = get_build_info()
    version = build_info.get("version", "1.0.0")
    
    specs = {spec.name: spec for spec in public_tool_specs()}
    
    for name, handler in FINAL_TOOL_IMPLEMENTATIONS.items():
        spec = specs.get(name)
        
        # Build FastMCP safety profile annotations based on layer and function
        annotations = {}
        tags = set()
        if spec:
            tags.add(spec.layer.lower())
            tags.add(spec.trinity.split()[0].lower()) # Add e.g. 'psi', 'delta'
            
            if spec.layer == "MACHINE" and name not in {"code_engine"}:
                annotations["readOnlyHint"] = True
                annotations["idempotentHint"] = True
            elif name == "code_engine" or name == "engineering_memory":
                annotations["destructiveHint"] = True
                annotations["idempotentHint"] = False
            elif spec.layer == "GOVERNANCE" and name != "vault_ledger":
                annotations["readOnlyHint"] = True
                annotations["idempotentHint"] = False
            elif spec.layer == "INTELLIGENCE":
                annotations["idempotentHint"] = True

        # Register tool with versioning and tags for better client discoverability
        mcp.tool(
            name=name, 
            description=spec.description if spec else None, 
            annotations=annotations,
            version=version,
            tags=tags if tags else None
        )(handler)

__all__ = list(ALL_TOOL_IMPLEMENTATIONS.keys()) + [
    "register_tools", 
    "FINAL_TOOL_IMPLEMENTATIONS", 
    "ALL_TOOL_IMPLEMENTATIONS",
    "Stage",
    "Verdict",
    "RuntimeStatus",
]
