"""Contract tests for canonical tool/alias adapter profile.

This file validates current canonical sources directly and avoids removed
legacy schema paths.
"""

from __future__ import annotations

import ast
from pathlib import Path

from arifosmcp.transport.protocol.aaa_contract import (
    AAA_CANONICAL_TOOLS,
    AAA_TOOL_ALIASES,
    ARCHIVED_TOOLS,
)

ROOT = Path(__file__).resolve().parents[2]
SERVER_FILE = ROOT / "arifosmcp.runtime" / "server.py"


def _tool_names_in_server() -> set[str]:
    module = ast.parse(SERVER_FILE.read_text(encoding="utf-8"))
    names: set[str] = set()

    for node in ast.walk(module):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for deco in node.decorator_list:
            if not isinstance(deco, ast.Call):
                continue
            func = deco.func
            if not isinstance(func, ast.Attribute):
                continue
            if not isinstance(func.value, ast.Name) or func.value.id != "mcp":
                continue
            if func.attr != "tool":
                continue

            explicit_name = None
            for kw in deco.keywords:
                if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                    if isinstance(kw.value.value, str):
                        explicit_name = kw.value.value
                        break
            names.add(explicit_name or node.name)

    return names


def test_server_registration_matches_canonical_contract() -> None:
    canonical = set(AAA_CANONICAL_TOOLS)
    registered = _tool_names_in_server()
    assert registered == canonical


def test_alias_targets_resolve_to_canonical_tools() -> None:
    canonical = set(AAA_CANONICAL_TOOLS)
    for alias, target in AAA_TOOL_ALIASES.items():
        assert target in canonical, f"Alias '{alias}' maps to non-canonical target '{target}'"


def test_archived_aliases_map_to_canonical_replacements() -> None:
    assert "fetch_content" in ARCHIVED_TOOLS
    assert "inspect_file" in ARCHIVED_TOOLS
    assert "system_audit" in ARCHIVED_TOOLS

    assert AAA_TOOL_ALIASES["fetch_content"] == "ingest_evidence"
    assert AAA_TOOL_ALIASES["inspect_file"] == "ingest_evidence"
    assert AAA_TOOL_ALIASES["system_audit"] == "audit_rules"
