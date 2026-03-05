"""Tool-surface hardening tests for external MCP exposure."""

from __future__ import annotations

import inspect

from aaa_mcp.server import mcp

CANONICAL_EXPOSED_TOOLS = {
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
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


async def _tool_names() -> set[str]:
    get_tools = getattr(mcp, "get_tools", None)
    if callable(get_tools):
        tools = get_tools()
    else:
        list_tools = getattr(mcp, "list_tools", None)
        if not callable(list_tools):
            return set()
        tools = list_tools()
    if inspect.isawaitable(tools):
        tools = await tools

    if isinstance(tools, dict):
        return set(tools.keys())
    if not isinstance(tools, (list, tuple, set)):
        return set()

    names: set[str] = set()
    for tool in tools:
        name = getattr(tool, "name", None)
        if isinstance(name, str):
            names.add(name)
    return names


async def test_external_mcp_surface_exposes_only_canonical_and_aux_tools() -> None:
    names = await _tool_names()

    assert names == CANONICAL_EXPOSED_TOOLS


async def test_legacy_triad_tool_aliases_not_externally_exposed() -> None:
    names = await _tool_names()

    assert LEGACY_TRIAD_TOOLS.isdisjoint(names)
