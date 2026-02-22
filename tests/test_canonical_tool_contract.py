"""Strict contract tests for canonical arifOS MCP tools."""

from __future__ import annotations

import inspect

from aaa_mcp import (
    agi_cognition,
    analyze,
    apex_verdict,
    asi_empathy,
    fetch,
    init_session,
    search,
    system_audit,
    vault_seal,
)
from aaa_mcp.server import ORGAN_ANNOTATIONS, UTILITY_ANNOTATIONS


CANONICAL_TOOLS = {
    "init_session": init_session,
    "agi_cognition": agi_cognition,
    "asi_empathy": asi_empathy,
    "apex_verdict": apex_verdict,
    "vault_seal": vault_seal,
    "search": search,
    "fetch": fetch,
    "analyze": analyze,
    "system_audit": system_audit,
}


def test_canonical_tool_names_are_exact() -> None:
    assert set(CANONICAL_TOOLS.keys()) == {
        "init_session",
        "agi_cognition",
        "asi_empathy",
        "apex_verdict",
        "vault_seal",
        "search",
        "fetch",
        "analyze",
        "system_audit",
    }


def test_canonical_signatures_are_stable() -> None:
    expected = {
        "init_session": ["query", "actor_id", "auth_token", "platform", "stakeholders"],
        "agi_cognition": ["query", "session_id", "hypotheses", "grounding", "plan_scope"],
        "asi_empathy": ["query", "session_id", "stakeholders", "ethical_rules", "scope"],
        "apex_verdict": [
            "session_id",
            "query",
            "implementation_details",
            "proposed_verdict",
            "human_approve",
        ],
        "vault_seal": ["session_id", "summary", "verdict"],
        "search": ["query"],
        "fetch": ["id"],
        "analyze": ["data", "analysis_type"],
        "system_audit": ["audit_scope", "verify_floors"],
    }

    for name, tool in CANONICAL_TOOLS.items():
        params = list(inspect.signature(tool.fn).parameters.keys())
        assert params == expected[name], f"{name} signature drifted: {params}"


def test_floor_metadata_matches_declared_contract() -> None:
    expected_floors = {
        "init_session": ("F11", "F12", "F5", "F6"),
        "agi_cognition": ("F2", "F4", "F7", "F8", "F10"),
        "asi_empathy": ("F5", "F6", "F9"),
        "apex_verdict": ("F2", "F3", "F4", "F11", "F13"),
        "vault_seal": ("F1", "F3"),
        "analyze": ("F4",),
        "system_audit": ("F2", "F3"),
    }

    for name, floors in expected_floors.items():
        tool = CANONICAL_TOOLS[name]
        actual = getattr(tool.fn, "_constitutional_floors", ())
        assert tuple(actual) == floors, f"{name} floor metadata mismatch: {actual}"

    # Read-only utilities intentionally have no constitutional decorator floors.
    assert getattr(search.fn, "_constitutional_floors", ()) == ()
    assert getattr(fetch.fn, "_constitutional_floors", ()) == ()


def test_server_annotations_cover_canonical_surface() -> None:
    assert set(ORGAN_ANNOTATIONS.keys()) == {
        "init_session",
        "agi_cognition",
        "asi_empathy",
        "apex_verdict",
        "vault_seal",
    }
    assert set(UTILITY_ANNOTATIONS.keys()) == {"search", "fetch", "analyze", "system_audit"}

    for name, meta in ORGAN_ANNOTATIONS.items():
        assert meta["title"]
        assert meta["description"]
        assert meta["floors"]
