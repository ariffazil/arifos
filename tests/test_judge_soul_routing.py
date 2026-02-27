"""Router parity test: judge_soul must be registered and callable.

Acceptance criteria from the kernel ABI mismatch diagnosis:
  1. 'judge_soul' appears in the FastMCP tool names at runtime.
  2. 'apex_judge' still works as a backward-compat alias.
  3. Calling judge_soul returns a structured verdict (not "Unknown tool").
  4. MANIFEST_VERSION is consistent between layers.

Run:
    pytest tests/test_judge_soul_routing.py -v
"""

from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# Layer 1: internal transport adapter (aaa_mcp)
# ---------------------------------------------------------------------------


def test_aaa_mcp_registers_judge_soul() -> None:
    """FastMCP must have 'judge_soul' in its internal tool registry."""
    from aaa_mcp.server import mcp

    tool_names = {t.name for t in mcp.get_tools().values()} if hasattr(mcp, "get_tools") else set()
    # Fallback: inspect _tool_manager or tools attribute (FastMCP internals vary by version)
    if not tool_names:
        tools = getattr(mcp, "_tools", None) or getattr(mcp, "tools", {})
        tool_names = set(tools.keys()) if isinstance(tools, dict) else set()

    assert "judge_soul" in tool_names, (
        f"'judge_soul' not found in FastMCP tool registry. "
        f"Registered tools: {sorted(tool_names)}"
    )


def test_aaa_mcp_apex_judge_compat_alias_exists() -> None:
    """apex_judge ToolHandle must still be accessible for backward compat."""
    from aaa_mcp import server as s

    assert hasattr(s, "apex_judge"), "apex_judge ToolHandle removed — breaks existing clients"
    assert hasattr(s, "judge_soul"), "judge_soul ToolHandle missing"


# ---------------------------------------------------------------------------
# Layer 2: canonical external surface (arifos_aaa_mcp)
# ---------------------------------------------------------------------------


def test_arifos_aaa_tool_list_contains_judge_soul() -> None:
    """AAA_TOOLS manifest must declare judge_soul, not apex_judge."""
    from arifos_aaa_mcp.server import AAA_TOOLS

    assert "judge_soul" in AAA_TOOLS, (
        f"'judge_soul' absent from AAA_TOOLS. Current list: {AAA_TOOLS}"
    )


def test_tool_registry_has_judge_soul() -> None:
    """_TOOL_REGISTRY used by REST layer must map 'judge_soul' to a callable."""
    from arifos_aaa_mcp.server import _TOOL_REGISTRY

    assert "judge_soul" in _TOOL_REGISTRY, (
        f"'judge_soul' not in _TOOL_REGISTRY. Keys: {sorted(_TOOL_REGISTRY)}"
    )
    # apex_judge backward compat
    assert "apex_judge" in _TOOL_REGISTRY, "'apex_judge' compat alias missing from _TOOL_REGISTRY"
    # Both must point to the same callable
    assert _TOOL_REGISTRY["judge_soul"] is _TOOL_REGISTRY["apex_judge"], (
        "judge_soul and apex_judge must point to the same handler"
    )


def test_rest_aliases_route_apex_judge_to_judge_soul() -> None:
    """REST TOOL_ALIASES must map legacy 'apex_judge' to 'judge_soul'."""
    from arifos_aaa_mcp.rest_routes import TOOL_ALIASES

    assert TOOL_ALIASES.get("apex_judge") == "judge_soul", (
        f"REST alias apex_judge -> judge_soul missing. Got: {TOOL_ALIASES.get('apex_judge')!r}"
    )
    assert TOOL_ALIASES.get("apex_verdict") == "judge_soul", (
        f"REST alias apex_verdict -> judge_soul missing. Got: {TOOL_ALIASES.get('apex_verdict')!r}"
    )


# ---------------------------------------------------------------------------
# Layer 3: governance metadata
# ---------------------------------------------------------------------------


def test_governance_maps_include_judge_soul() -> None:
    """TRINITY_BY_TOOL, TOOL_LAW_BINDINGS, TOOL_STAGE_MAP must all have judge_soul."""
    from arifos_aaa_mcp.governance import TOOL_LAW_BINDINGS, TOOL_STAGE_MAP, TRINITY_BY_TOOL

    assert TRINITY_BY_TOOL.get("judge_soul") == "Psi", "judge_soul lane must be Psi"
    assert TOOL_STAGE_MAP.get("judge_soul") == "888_JUDGE", "judge_soul stage must be 888_JUDGE"
    assert "F1_AMANAH" in TOOL_LAW_BINDINGS.get("judge_soul", []), (
        "judge_soul must bind F1_AMANAH floor"
    )


# ---------------------------------------------------------------------------
# Layer 4: protocol naming
# ---------------------------------------------------------------------------


def test_protocol_naming_resolves_judge_soul() -> None:
    """resolve_protocol_tool_name('judge_soul') must return 'apex_verdict'."""
    from aaa_mcp.protocol.tool_naming import resolve_protocol_tool_name

    assert resolve_protocol_tool_name("judge_soul") == "apex_verdict"
    assert resolve_protocol_tool_name("apex_judge") == "apex_verdict"  # compat still works


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
# Layer 6: acceptance test — call judge_soul with dummy payload
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_judge_soul_callable_returns_verdict() -> None:
    """judge_soul must return a structured verdict dict, not an error."""
    from arifos_aaa_mcp.server import apex_judge as judge_soul_fn

    result = await judge_soul_fn.fn(
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
