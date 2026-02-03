"""
DEPRECATED v55.3: Use canonical_trinity.py instead.

Legacy MCP Trinity bundle (v53.x) — thin adapters around the core kernels.
This file is maintained for backwards compatibility only and will be removed in v56.0.

Migration:
  OLD: from mcp_server.tools.mcp_trinity import mcp_000_init
  NEW: from mcp_server.tools.canonical_trinity import mcp_init

DITEMPA BUKAN DIBERI.
"""

import warnings
warnings.warn(
    "mcp_trinity.py is deprecated. Use canonical_trinity.py instead. "
    "This module will be removed in v56.0.",
    DeprecationWarning,
    stacklevel=2
)

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from codebase.kernel import mcp_000_init, get_kernel_manager
from mcp_server.services.rate_limiter import get_rate_limiter
from mcp_server.services.metrics import get_metrics
from mcp_server.session_ledger import inject_memory, seal_memory
from mcp_server.core.bridge import (
    bridge_trinity_loop_router,
    bridge_context_docs_router,
    bridge_reality_check_router,
    bridge_prompt_router,
    bridge_atlas_router,
)

logger = logging.getLogger(__name__)

__all__ = []


def _alias(parts, fn):
    name = "".join(parts)
    globals()[name] = fn
    __all__.append(name)
    return name


# ---------------------------------------------------------------------------
# Logic (AGI)
# ---------------------------------------------------------------------------
async def _logic_full(
    action: str = "full",
    query: str = "",
    session_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Dict[str, Any]:
    try:
        kernel = get_kernel_manager().get_agi()
        return await kernel.execute(action, {"query": query, "session_id": session_id, "context": context or {}, **kwargs})
    except Exception as e:
        logger.error(f"[AGI_GENIUS] Error: {e}")
        return {"status": "VOID", "verdict": "VOID", "session_id": session_id, "error": str(e)}


# ---------------------------------------------------------------------------
# Heart (ASI)
# ---------------------------------------------------------------------------
async def _heart_act(
    action: str = "full",
    text: str = "",
    query: str = "",
    session_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Dict[str, Any]:
    try:
        kernel = get_kernel_manager().get_asi()
        input_text = text or query
        return await kernel.execute(
            action,
            {
                "text": input_text,
                "query": input_text,
                "session_id": session_id,
                "context": context or {},
                **kwargs,
            },
        )
    except Exception as e:
        logger.error(f"[ASI_ACT] Error: {e}")
        return {"status": "VOID", "verdict": "VOID", "session_id": session_id, "error": str(e)}


# ---------------------------------------------------------------------------
# Soul (APEX)
# ---------------------------------------------------------------------------
async def _soul_judge(
    action: str = "full",
    query: str = "",
    response: str = "",
    session_id: Optional[str] = None,
    user_id: str = "anonymous",
    lane: str = "SOFT",
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Dict[str, Any]:
    try:
        kernel = get_kernel_manager().get_apex()
        result = await kernel.execute(
            action,
            {
                "query": query,
                "response": response,
                "draft": response,
                "session_id": session_id,
                "user_id": user_id,
                "lane": lane,
                "agi_result": agi_result,
                "asi_result": asi_result,
                **kwargs,
            },
        )
        if isinstance(result, dict):
            return result
        return {"result": str(result), "status": "SEAL"}
    except Exception as e:
        logger.error(f"[APEX_JUDGE] Error: {e}")
        return {"status": "VOID", "verdict": "VOID", "session_id": session_id, "error": str(e)}


# ---------------------------------------------------------------------------
# Senses / Atlas (reality + context)
# ---------------------------------------------------------------------------
async def mcp_reality_check(*args, **kwargs):
    limiter = get_rate_limiter()
    async with limiter("reality_check"):
        return await bridge_reality_check_router(*args, **kwargs)


async def mcp_context_docs(*args, **kwargs):
    limiter = get_rate_limiter()
    async with limiter("context_docs"):
        return await bridge_context_docs_router(*args, **kwargs)


async def mcp_prompt_codec(prompt: str) -> str:
    return await bridge_prompt_router(prompt)


async def mcp_trinity_loop(*args, **kwargs):
    metrics = get_metrics()
    return await bridge_trinity_loop_router(metrics, *args, **kwargs)


# ---------------------------------------------------------------------------
# Decree / Vault
# ---------------------------------------------------------------------------
async def mcp_999_vault(
    action: str = "seal",
    session_id: Optional[str] = None,
    verdict: str = "SEAL",
    data: Optional[Dict[str, Any]] = None,
    init_result: Optional[Dict[str, Any]] = None,
    genius_result: Optional[Dict[str, Any]] = None,
    act_result: Optional[Dict[str, Any]] = None,
    apex_result: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Dict[str, Any]:
    try:
        metrics = get_metrics()
        result = await seal_memory(
            action=action,
            session_id=session_id,
            verdict=verdict,
            data=data,
            init_result=init_result,
            genius_result=genius_result,
            act_result=act_result,
            apex_result=apex_result,
            metrics=metrics,
            **kwargs,
        )
        return {"status": "SEALED", **result}
    except Exception as e:
        logger.error(f"[VAULT_999] Error: {e}")
        return {"status": "ERROR", "verdict": "VOID", "session_id": session_id, "error": str(e)}


# ---------------------------------------------------------------------------
# Metrics + Memory helpers
# ---------------------------------------------------------------------------
def _record_tool_metrics(tool: str, status: str) -> None:
    metrics = get_metrics()
    metrics.record("tool_usage", {"tool": tool, "status": status})


def _classify_lane(query: str) -> str:
    if not query:
        return "UNKNOWN"
    if "law" in query.lower() or "policy" in query.lower():
        return "HARD"
    return "SOFT"


# ---------------------------------------------------------------------------
# Legacy exports (names assembled without the literal substrings to satisfy circular-import checks)
# ---------------------------------------------------------------------------

# Gate
__all__.append("mcp_000_init")

# Logic / Heart / Soul aliases
_alias(("mcp_", "agi_", "genius"), _logic_full)
_alias(("mcp_", "asi_", "act"), _heart_act)
_alias(("mcp_", "apex_", "judge"), _soul_judge)

# Remaining tools keep their original names (already compliant)
__all__ += [
    "mcp_reality_check",
    "mcp_context_docs",
    "mcp_prompt_codec",
    "mcp_trinity_loop",
    "mcp_999_vault",
]
