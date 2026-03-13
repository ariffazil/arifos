"""
Phase 2 external capability tools for the arifOS runtime.

These tools remain enabled for compatibility, but they are intentionally kept
outside the public arifOS_kernel surface. They are the integration seam
for stricter future governance at Stages 777/888.
"""

from __future__ import annotations

import logging
from typing import Any

from fastmcp import FastMCP

from .bridge import call_kernel
from .public_registry import is_public_profile, normalize_tool_profile

logger = logging.getLogger(__name__)


# Tools moved to core are no longer defined here.


async def trace_replay(session_id: str = "global", limit: int = 20) -> dict[str, Any]:
    """Read-only replay of sealed trace history for a session."""
    return await call_kernel("trace_replay", session_id, {"limit": limit})


async def metabolic_loop(session_id: str = "global") -> dict[str, Any]:
    """Legacy orchestration tool preserved for compatibility only."""
    return await call_kernel("metabolic_loop", session_id, {})


def _register_local_phase2_tools(mcp: FastMCP, profile: str = "full") -> None:
    normalized_profile = normalize_tool_profile(profile)

    # search_reality, ingest_evidence, audit_rules, check_vital, session_memory
    # have all been moved to the primary arifOS core tool surface.

    if not is_public_profile(normalized_profile):
        mcp.tool(
            description=(
                "Use this when you need to replay sealed stage traces for a given session_id "
                "from VAULT999 for explainability or audit. This tool is read-only."
            ),
            annotations={"readOnlyHint": True},
        )(trace_replay)
        mcp.tool(
            description=(
                "Use this only for legacy compatibility. For ChatGPT and remote MCP clients, "
                "prefer `arifOS_kernel` from the core runtime tool surface."
            ),
        )(metabolic_loop)


def _register_aclip_tools(mcp: FastMCP) -> None:
    # ACLIP legacy tools are currently disabled or migrated to the primary surface.
    pass


def register_phase2_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register legacy capability tools without wiring them into the new loop."""
    normalized_profile = normalize_tool_profile(profile)
    _register_local_phase2_tools(mcp, profile=normalized_profile)
    if not is_public_profile(normalized_profile):
        _register_aclip_tools(mcp)


__all__ = [
    "metabolic_loop",
    "register_phase2_tools",
    "trace_replay",
]
