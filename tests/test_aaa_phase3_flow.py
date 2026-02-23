"""Phase 3 static flow checks for AAA MCP.

Focus:
- session continuity guard present on governed tools
- 000->999 tool names exist for orchestrated flow
"""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_FILE = ROOT / "arifos_aaa_mcp" / "server.py"


def test_phase3_server_references_session_guard() -> None:
    text = SERVER_FILE.read_text(encoding="utf-8")
    assert "require_session(" in text
    assert "validate_input(" in text


def test_phase3_contains_000_to_999_public_tools() -> None:
    mod = ast.parse(SERVER_FILE.read_text(encoding="utf-8"))
    names = set()
    for node in mod.body:
        if not isinstance(node, ast.AsyncFunctionDef):
            continue
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and dec.func.attr == "tool":
                names.add(node.name)

    for required in ("anchor_session", "reason_mind", "simulate_heart", "judge_soul", "seal_vault"):
        assert required in names
