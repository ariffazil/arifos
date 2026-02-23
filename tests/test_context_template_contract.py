"""Contracts for full-context resources, prompts, and schema continuity."""

from __future__ import annotations

from aaa_mcp.protocol import export_full_context_pack, get_input_schema
from aaa_mcp.server import (
    _prompt_anchor_reason,
    _prompt_audit_then_seal,
    _prompt_trinity_forge,
    _resource_full_context_template,
    _resource_tool_schemas,
)
from core.shared.context_template import build_full_context_template


def test_full_context_template_shape() -> None:
    payload = build_full_context_template()
    assert payload["template_id"] == "arifos.full_context.v1"
    assert payload["schema_version"] == "1.0.0"
    assert payload["stage_spine"] == ["000", "222", "333", "444", "666", "888", "999"]
    assert "required_inputs" in payload and "session_id" in payload["required_inputs"]


def test_server_resources_expose_template_and_schemas() -> None:
    template = _resource_full_context_template()
    schemas = _resource_tool_schemas()
    assert template["template_id"] == "arifos.full_context.v1"
    assert schemas["schema_version"] == "2026.02.23-context-forge"
    assert "init_session" in schemas["inputs"]


def test_prompts_include_continuity_context() -> None:
    prompt_forge = _prompt_trinity_forge("ship production safely", actor_id="arif")
    prompt_chain = _prompt_anchor_reason("should we deploy?", actor_id="arif")
    prompt_seal = _prompt_audit_then_seal("sess-1", "deployment approved", "SEAL")

    assert "000 -> 222 -> 333 -> 444 -> 666 -> 888 -> 999" in prompt_forge
    assert "session continuity" in prompt_chain.lower()
    assert "session_id=sess-1" in prompt_seal


def test_protocol_schemas_expose_auth_and_session_continuity() -> None:
    init_schema = get_input_schema("init_session")
    agi_schema = get_input_schema("agi_cognition")

    assert init_schema is not None and "actor_id" in init_schema["properties"]
    assert init_schema is not None and "auth_token" in init_schema["properties"]
    assert agi_schema is not None and "session_id" in agi_schema["properties"]
    assert agi_schema is not None and "auth_token" in agi_schema["properties"]


def test_full_context_pack_export_includes_resources_and_prompts() -> None:
    pack = export_full_context_pack()
    assert "arifos://templates/full-context" in pack["resources"]
    assert "arifos.prompt.trinity_forge" in pack["prompts"]
