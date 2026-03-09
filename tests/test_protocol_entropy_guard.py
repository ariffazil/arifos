"""Entropy guards for protocol naming consistency and alias resolution."""

from __future__ import annotations

from core.schema import get_input_schema, get_output_schema
from arifosmcp.transport.protocol.tool_graph import validate_sequence
from arifosmcp.transport.protocol.tool_naming import (
    CANONICAL_PUBLIC_TO_LEGACY,
    MCP_VERB_TO_LEGACY,
    resolve_protocol_tool_name,
)
from arifosmcp.transport.protocol.tool_registry import get_tool_by_mcp_name, get_tool_spec


def test_canonical_public_names_resolve_to_protocol_keys() -> None:
    assert resolve_protocol_tool_name("init_session") == "init_gate"
    assert resolve_protocol_tool_name("agi_cognition") == "agi_reason"
    assert resolve_protocol_tool_name("phoenix_recall") == "phoenix_recall"
    assert resolve_protocol_tool_name("asi_empathy") == "asi_empathize"
    assert resolve_protocol_tool_name("apex_verdict") == "apex_verdict"
    assert resolve_protocol_tool_name("sovereign_actuator") == "sovereign_actuator"
    assert resolve_protocol_tool_name("vault_seal") == "vault_seal"
    assert resolve_protocol_tool_name("fetch") == "fetch"
    assert resolve_protocol_tool_name("analyze") == "analyze"
    assert resolve_protocol_tool_name("system_audit") == "system_audit"


def test_legacy_verbs_resolve_to_protocol_keys() -> None:
    assert resolve_protocol_tool_name("anchor") == "init_gate"
    assert resolve_protocol_tool_name("integrate") == "agi_reason"
    assert resolve_protocol_tool_name("validate") == "asi_empathize"
    assert resolve_protocol_tool_name("audit") == "apex_verdict"


def test_registry_accepts_canonical_and_verb_names() -> None:
    assert get_tool_spec("init_session").name == "init_gate"
    assert get_tool_spec("agi_cognition").name == "agi_reason"
    assert get_tool_by_mcp_name("anchor").name == "init_gate"
    assert get_tool_by_mcp_name("audit").name == "apex_verdict"


def test_schema_accessors_accept_canonical_names() -> None:
    init_schema = get_input_schema("init_session")
    reason_schema = get_input_schema("agi_cognition")
    empathy_schema = get_input_schema("asi_empathy")
    verdict_schema = get_output_schema("apex_verdict")
    phoenix_schema = get_input_schema("phoenix_recall")
    actuator_schema = get_input_schema("sovereign_actuator")
    audit_schema = get_input_schema("system_audit")

    assert init_schema is not None and "query" in init_schema["properties"]
    assert reason_schema is not None and "session_id" in reason_schema["properties"]
    assert empathy_schema is not None and "session_id" in empathy_schema["properties"]
    assert verdict_schema is not None and "verdict" in verdict_schema["properties"]
    assert phoenix_schema is not None and "query" in phoenix_schema["properties"]
    assert actuator_schema is not None and "command" in actuator_schema["properties"]
    assert audit_schema is not None and "audit_scope" in audit_schema["properties"]


def test_validate_sequence_accepts_canonical_public_names() -> None:
    ok, msg = validate_sequence(
        ["init_session", "agi_cognition", "asi_empathy", "apex_verdict", "vault_seal"]
    )
    assert ok, msg


def test_alias_maps_are_single_source_non_empty() -> None:
    assert CANONICAL_PUBLIC_TO_LEGACY
    assert MCP_VERB_TO_LEGACY
    assert len(set(CANONICAL_PUBLIC_TO_LEGACY.keys())) == len(CANONICAL_PUBLIC_TO_LEGACY)
    assert len(set(MCP_VERB_TO_LEGACY.keys())) == len(MCP_VERB_TO_LEGACY)
