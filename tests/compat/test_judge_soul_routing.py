"""Router parity test: apex_judge is canonical and judge_soul is alias-only.

Acceptance criteria from the kernel ABI mismatch diagnosis:
  1. 'apex_judge' appears in the FastMCP tool names at runtime.
  2. 'judge_soul' still works as a backward-compat alias.
  3. Alias names do not leak into public tool discovery.
  4. Calling apex_judge returns a structured verdict (not "Unknown tool").
  5. MANIFEST_VERSION is consistent between layers.

Run:
    pytest tests/compat/test_judge_soul_routing.py -v
"""

from __future__ import annotations

import pytest


def _tool_fn(tool):
    return getattr(tool, "fn", tool)


# ---------------------------------------------------------------------------
# Layer 1: internal transport adapter (aaa_mcp)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_aaa_mcp_registers_apex_judge() -> None:
    """FastMCP must have 'apex_judge' in its internal tool registry."""
    from fastmcp import Client

    from aaa_mcp.server import create_unified_mcp_server

    async with Client(create_unified_mcp_server()) as client:
        tools = await client.list_tools()
    tool_names = {tool.name for tool in tools}

    assert "apex_judge" in tool_names, (
        f"'apex_judge' not found in FastMCP tool registry. "
        f"Registered tools: {sorted(tool_names)}"
    )


def test_aaa_mcp_apex_judge_compat_alias_exists() -> None:
    """apex_judge is canonical and judge_soul remains a compat alias."""
    from aaa_mcp import server as s

    assert hasattr(s, "apex_judge"), "apex_judge ToolHandle removed — breaks existing clients"
    assert hasattr(s, "judge_soul"), "judge_soul ToolHandle missing"


# ---------------------------------------------------------------------------
# Layer 2: canonical external surface (arifos_aaa_mcp)
# ---------------------------------------------------------------------------


def test_arifos_aaa_tool_list_contains_apex_judge() -> None:
    """AAA_TOOLS manifest must declare apex_judge as canonical."""
    from arifos_aaa_mcp.server import AAA_TOOLS

    assert "apex_judge" in AAA_TOOLS, (
        f"'apex_judge' absent from AAA_TOOLS. Current list: {AAA_TOOLS}"
    )


def test_tool_registry_has_only_canonical_apex_judge() -> None:
    """_TOOL_REGISTRY must expose only the canonical public tool name."""
    from arifos_aaa_mcp.server import _TOOL_REGISTRY

    assert "apex_judge" in _TOOL_REGISTRY, (
        f"'apex_judge' not in _TOOL_REGISTRY. Keys: {sorted(_TOOL_REGISTRY)}"
    )
    assert "judge_soul" not in _TOOL_REGISTRY, (
        "judge_soul alias leaked into the public tool registry"
    )


def test_rest_aliases_route_legacy_names_to_apex_judge() -> None:
    """REST TOOL_ALIASES must route legacy names to apex_judge canon."""
    from arifos_aaa_mcp.rest_routes import TOOL_ALIASES

    assert TOOL_ALIASES.get("judge_soul") == "apex_judge", (
        f"REST alias judge_soul -> apex_judge missing. Got: {TOOL_ALIASES.get('judge_soul')!r}"
    )
    assert TOOL_ALIASES.get("apex_verdict") == "apex_judge", (
        f"REST alias apex_verdict -> apex_judge missing. Got: {TOOL_ALIASES.get('apex_verdict')!r}"
    )


@pytest.mark.anyio
async def test_public_tool_listing_hides_judge_soul_alias() -> None:
    """FastMCP public discovery must list only the canonical apex_judge name."""
    from fastmcp import Client

    from arifos_aaa_mcp.server import create_aaa_mcp_server

    async with Client(create_aaa_mcp_server()) as client:
        tools = await client.list_tools()
    tool_names = {tool.name for tool in tools}

    assert "apex_judge" in tool_names
    assert "judge_soul" not in tool_names


# ---------------------------------------------------------------------------
# Layer 3: governance metadata
# ---------------------------------------------------------------------------


def test_governance_maps_include_apex_judge() -> None:
    """TRINITY_BY_TOOL, TOOL_LAW_BINDINGS, TOOL_STAGE_MAP must all have apex_judge."""
    from arifos_aaa_mcp.governance import TOOL_LAW_BINDINGS, TOOL_STAGE_MAP, TRINITY_BY_TOOL

    assert TRINITY_BY_TOOL.get("apex_judge") == "Psi", "apex_judge lane must be Psi"
    assert TOOL_STAGE_MAP.get("apex_judge") == "888_JUDGE", "apex_judge stage must be 888_JUDGE"
    assert "F1_AMANAH" in TOOL_LAW_BINDINGS.get("apex_judge", []), (
        "apex_judge must bind F1_AMANAH floor"
    )


# ---------------------------------------------------------------------------
# Layer 4: protocol naming
# ---------------------------------------------------------------------------


def test_protocol_naming_resolves_apex_and_judge_soul() -> None:
    """resolve_protocol_tool_name() must route both apex_judge and judge_soul."""
    from aaa_mcp.protocol.tool_naming import resolve_protocol_tool_name

    assert resolve_protocol_tool_name("apex_judge") == "apex_verdict"
    assert resolve_protocol_tool_name("judge_soul") == "apex_verdict"  # compat still works


# ---------------------------------------------------------------------------
# Layer 5: manifest ABI version parity
# ---------------------------------------------------------------------------


def test_manifest_version_parity() -> None:
    """Both layers must declare the same MANIFEST_VERSION."""
    from aaa_mcp.server import MANIFEST_VERSION as inner
    from arifos_aaa_mcp.server import MANIFEST_VERSION as outer

    assert inner == outer, (
        f"MANIFEST_VERSION mismatch: aaa_mcp={inner}, arifos_aaa_mcp={outer}. "
        "Restart the server — half-upgrade detected."
    )


# ---------------------------------------------------------------------------
# Layer 6: acceptance test — call apex_judge with dummy payload
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_apex_judge_callable_returns_verdict() -> None:
    """apex_judge must return a structured verdict dict, not an error."""
    from arifos_aaa_mcp.server import apex_judge

    result = await _tool_fn(apex_judge)(
        session_id="arif-5c6623cb",
        query="APEX ping",
        agi_result={},
        asi_result={},
        critique_result={},
    )

    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    assert "verdict" in result, f"No 'verdict' key in result: {result}"
    # Must be a known verdict, not an error string
    known_verdicts = {"SEAL", "PARTIAL", "SABAR", "VOID", "888_HOLD", "HOLD"}
    assert result["verdict"] in known_verdicts, (
        f"Unexpected verdict '{result['verdict']}' — tool may have errored: {result}"
    )
