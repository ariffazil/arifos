"""
Phase 2 external capability tools for the arifOS runtime.

These tools remain enabled for compatibility, but they are intentionally kept
outside the new 10-tool APEX-G metabolic loop. They are the integration seam
for stricter future governance at Stages 777/888.
"""

from __future__ import annotations

import logging
from typing import Any

from fastmcp import FastMCP

from arifosmcp.bridge import call_kernel

logger = logging.getLogger(__name__)


async def search_reality(query: str) -> dict[str, Any]:
    """Legacy external capability: web grounding before making claims."""
    return await call_kernel("search_reality", "global", {"query": query})


async def ingest_evidence(source_url: str) -> dict[str, Any]:
    """Legacy external capability: extract evidence from a source URL."""
    return await call_kernel("ingest_evidence", "global", {"source_url": source_url})


async def audit_rules(session_id: str = "global") -> dict[str, Any]:
    """Legacy external capability: verify current state against the Floors."""
    return await call_kernel("audit_rules", session_id, {})


async def check_vital(session_id: str = "global") -> dict[str, Any]:
    """Legacy external capability: system health and constitutional vitality."""
    return await call_kernel("check_vital", session_id, {})


async def metabolic_loop(session_id: str = "global") -> dict[str, Any]:
    """Legacy orchestration tool preserved for compatibility only."""
    return await call_kernel("metabolic_loop", session_id, {})


def _register_local_phase2_tools(mcp: FastMCP, profile: str = "full") -> None:
    normalized_profile = profile.strip().lower() or "full"

    mcp.tool(
        description=(
            "Use this when you need web grounding or source discovery before making claims. "
            "This tool is read-only."
        ),
        annotations={"readOnlyHint": True},
    )(search_reality)
    mcp.tool(
        description=(
            "Use this when you need to fetch or inspect evidence from a URL or file path "
            "without mutating state. This tool is read-only."
        ),
        annotations={"readOnlyHint": True},
    )(ingest_evidence)
    mcp.tool(
        description=(
            "Use this when you need a read-only governance or floor audit. This tool is "
            "read-only."
        ),
        annotations={"readOnlyHint": True},
    )(audit_rules)
    mcp.tool(
        description=(
            "Use this when you need a read-only system health snapshot. This tool is "
            "read-only."
        ),
        annotations={"readOnlyHint": True},
    )(check_vital)
    if normalized_profile != "chatgpt":
        mcp.tool(
            description=(
                "Use this only for legacy compatibility. For ChatGPT and remote MCP clients, "
                "prefer `metabolic_loop_router` from the core runtime tool surface."
            ),
        )(metabolic_loop)


def _register_aclip_tools(mcp: FastMCP) -> None:
    try:
        from arifosmcp.intelligence.mcp_bridge import register_aclip_tools

        register_aclip_tools(mcp)
    except Exception as exc:
        logger.warning("Phase 2 ACLIP tools unavailable: %s", exc)


def register_phase2_tools(mcp: FastMCP, profile: str = "full") -> None:
    """Register legacy capability tools without wiring them into the new loop."""
    normalized_profile = profile.strip().lower() or "full"
    _register_local_phase2_tools(mcp, profile=normalized_profile)
    if normalized_profile != "chatgpt":
        _register_aclip_tools(mcp)


__all__ = [
    "audit_rules",
    "check_vital",
    "ingest_evidence",
    "metabolic_loop",
    "register_phase2_tools",
    "search_reality",
]
