"""Contract tests for current canonical arifOS MCP tools."""

from __future__ import annotations

import inspect

from aaa_mcp import (
    agi_cognition,
    analyze,
    apex_verdict,
    asi_empathy,
    fetch,
    init_session,
    phoenix_recall,
    search,
    sovereign_actuator,
    system_audit,
    vault_seal,
)

CANONICAL_TOOLS = {
    "init_session": init_session,
    "agi_cognition": agi_cognition,
    "phoenix_recall": phoenix_recall,
    "asi_empathy": asi_empathy,
    "apex_verdict": apex_verdict,
    "sovereign_actuator": sovereign_actuator,
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
        "phoenix_recall",
        "asi_empathy",
        "apex_verdict",
        "sovereign_actuator",
        "vault_seal",
        "search",
        "fetch",
        "analyze",
        "system_audit",
    }


def test_canonical_signatures_are_stable() -> None:
    expected = {
        "init_session": [
            "query",
            "actor_id",
            "auth_token",
            "mode",
            "grounding_required",
            "debug",
            "inject_kernel",
            "compact_kernel",
            "template_id",
            "auth_context",
        ],
        "agi_cognition": [
            "query",
            "session_id",
            "grounding",
            "capability_modules",
            "debug",
            "actor_id",
            "auth_token",
            "parent_session_id",
            "auth_context",
            "inference_budget",
            "risk_mode",
        ],
        "phoenix_recall": ["current_thought_vector", "session_id", "depth", "domain", "debug"],
        "asi_empathy": [
            "query",
            "session_id",
            "stakeholders",
            "capability_modules",
            "debug",
            "actor_id",
            "auth_token",
            "parent_session_id",
            "auth_context",
            "risk_mode",
        ],
        "apex_verdict": [
            "session_id",
            "query",
            "agi_result",
            "asi_result",
            "capability_modules",
            "implementation_details",
            "proposed_verdict",
            "human_approve",
            "debug",
            "actor_id",
            "auth_token",
            "parent_session_id",
            "auth_context",
            "risk_mode",
        ],
        "sovereign_actuator": [
            "session_id",
            "command",
            "working_dir",
            "timeout",
            "confirm_dangerous",
            "agent_id",
            "purpose",
        ],
        "vault_seal": ["session_id", "summary", "governance_token"],
        "search": ["query", "intent"],
        "fetch": ["id", "max_chars"],
        "analyze": ["session_id", "path", "depth", "include_hidden", "pattern", "min_size_bytes", "max_files"],
        "system_audit": ["audit_scope", "verify_floors"],
    }

    for name, tool in CANONICAL_TOOLS.items():
        params = list(inspect.signature(tool.fn).parameters.keys())
        assert params == expected[name], f"{name} signature drifted: {params}"
