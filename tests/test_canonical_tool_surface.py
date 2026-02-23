"""Tool-surface hardening tests for external MCP exposure."""

from __future__ import annotations

from aclip_cai.mcp_server import mcp


CANONICAL_EXPOSED_TOOLS = {
    "init_session",
    "agi_cognition",
    "phoenix_recall",
    "asi_empathy",
    "apex_verdict",
    "sovereign_actuator",
    "vault_seal",
    "search",
    "fetch",
    "analyze",
    "system_audit",
    "sense_health",
    "sense_fs",
}

LEGACY_TRIAD_TOOLS = {
    "triad_anchor",
    "triad_reason",
    "triad_integrate",
    "triad_respond",
    "triad_validate",
    "triad_align",
    "triad_forge",
    "triad_audit",
    "triad_seal",
}


async def test_external_mcp_surface_exposes_only_canonical_and_aux_tools() -> None:
    # Import side effect: hardens tool surface by removing legacy triad aliases.
    import aaa_mcp.server  # noqa: F401

    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}

    assert names == CANONICAL_EXPOSED_TOOLS


async def test_legacy_triad_tool_aliases_not_externally_exposed() -> None:
    import aaa_mcp.server  # noqa: F401

    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}

    assert LEGACY_TRIAD_TOOLS.isdisjoint(names)
