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
    public_names = tool_names_for_profile("public")
    internal_names = tool_names_for_profile("internal")

    assert "lsp_query_tool" not in public_names
    assert "forge_office_document" not in public_names
    assert "ollama_local_generate" not in public_names
    assert "lsp_query_tool" in internal_names
    assert "forge_office_document" in internal_names
    assert "ollama_local_generate" in internal_names


def test_internal_server_json_declares_internal_capabilities() -> None:
    server_json = build_internal_server_json()
    tool_names = {tool["name"] for tool in server_json["tools"]}

    assert server_json["capabilities"]["profile"] == "internal"
    assert "lsp_query_tool" in tool_names
    assert "forge_office_document" in tool_names
    assert "ollama_local_generate" in tool_names
