"""Contract checks for arifOS AAA MCP 13-tool surface.

These tests are static (AST/text) to avoid requiring runtime MCP dependencies.
"""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_FILE = ROOT / "arifos_aaa_mcp" / "server.py"
GOV_FILE = ROOT / "arifos_aaa_mcp" / "governance.py"


EXPECTED_TOOLS = {
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "judge_soul",
    "forge_hand",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
}


def _tool_names_from_server(path: Path) -> set[str]:
    mod = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in mod.body:
        if not isinstance(node, ast.AsyncFunctionDef):
            continue
        for dec in node.decorator_list:
            if (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Attribute)
                and dec.func.attr == "tool"
            ):
                names.add(node.name)
    return names


def test_aaa_server_exposes_exactly_13_tools() -> None:
    names = _tool_names_from_server(SERVER_FILE)
    assert names == EXPECTED_TOOLS


def test_governance_has_333_axioms_catalog() -> None:
    text = GOV_FILE.read_text(encoding="utf-8")
    assert "AXIOMS_333" in text
    assert "A1_TRUTH_COST" in text
    assert "A2_SCAR_WEIGHT" in text
    assert "A3_ENTROPY_WORK" in text


def test_governance_has_13_law_catalog() -> None:
    text = GOV_FILE.read_text(encoding="utf-8")
    assert "LAW_13_CATALOG" in text
    for marker in (
        "F1_AMANAH",
        "F2_TRUTH",
        "F4_CLARITY",
        "F5_PEACE2",
        "F6_EMPATHY",
        "F7_HUMILITY",
        "F9_ANTI_HANTU",
        "F11_AUTHORITY",
        "F12_DEFENSE",
        "F3_TRI_WITNESS",
        "F8_GENIUS",
        "F10_ONTOLOGY_LOCK",
        "F13_SOVEREIGNTY",
    ):
        assert marker in text


def test_governance_embeds_apex_dials_mapping() -> None:
    text = GOV_FILE.read_text(encoding="utf-8")
    assert "tool_dials_map.json" in text
    assert "_derive_apex_dials" in text
    assert '"G_star"' in text


def test_governance_embeds_ditempa_motto_bookends() -> None:
    text = GOV_FILE.read_text(encoding="utf-8")
    assert "MOTTO_000_INIT_HEADER" in text
    assert "MOTTO_999_SEAL_HEADER" in text
    assert '"anchor_session"' in text
    assert '"seal_vault"' in text


def test_no_legacy_public_tool_names_in_aaa_surface() -> None:
    text = SERVER_FILE.read_text(encoding="utf-8")
    legacy_names = [
        'name="init_session"',
        'name="agi_cognition"',
        'name="asi_empathy"',
        'name="apex_verdict"',
        'name="vault_seal"',
        'name="search"',
        'name="fetch"',
        'name="analyze"',
        'name="system_audit"',
    ]
    for marker in legacy_names:
        assert marker not in text
