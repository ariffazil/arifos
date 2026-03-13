from __future__ import annotations

import json
from pathlib import Path

from arifosmcp.runtime.public_registry import (
    build_internal_server_json,
    build_mcp_manifest,
    build_server_json,
    tool_names_for_profile,
)

ROOT = Path(__file__).resolve().parents[1]


def test_server_json_matches_registry() -> None:
    server_json = json.loads((ROOT / "spec" / "server.json").read_text(encoding="utf-8"))
    assert server_json == build_server_json()


def test_mcp_manifest_matches_registry() -> None:
    manifest_json = json.loads((ROOT / "spec" / "mcp-manifest.json").read_text(encoding="utf-8"))
    assert manifest_json == build_mcp_manifest()


def test_public_profile_stays_minimal_and_internal_profile_includes_internal_tools() -> None:
    """Canonical 24 tools are all public - internal profile adds legacy aliases only."""
    public_names = tool_names_for_profile("public")
    internal_names = tool_names_for_profile("internal")

    # Canonical 24 are public
    assert "init_anchor" in public_names
    assert "apex_judge" in public_names
    assert "vault_seal" in public_names

    # Internal profile includes all public tools (no hidden tier in canonical 24)
    assert set(public_names).issubset(set(internal_names))


def test_internal_server_json_declares_internal_capabilities() -> None:
    """Internal server JSON marks profile but includes same 24 canonical tools."""
    server_json = build_internal_server_json()
    tool_names = {tool["name"] for tool in server_json["tools"]}

    assert server_json["capabilities"]["profile"] == "internal"
    # All 24 canonical tools present
    assert "init_anchor" in tool_names
    assert "forge" in tool_names
    assert "apex_judge" in tool_names
    assert "vault_seal" in tool_names
