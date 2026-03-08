"""Public surface contract tests for shared aliases/resources/prompts."""

from __future__ import annotations

import json

import pytest
from fastmcp import Client

from arifosmcp.transport.protocol.public_surface import (
    PUBLIC_PROMPT_NAMES,
    PUBLIC_RESOURCE_URIS,
    PUBLIC_TOOL_ALIASES,
)


def test_public_rest_aliases_use_shared_source() -> None:
    from arifosmcp.runtime.rest_routes import TOOL_ALIASES

    assert TOOL_ALIASES == PUBLIC_TOOL_ALIASES
    assert TOOL_ALIASES["apex_verdict"] == "apex_judge"
    assert TOOL_ALIASES["judge_soul"] == "apex_judge"


def test_streamable_aliases_use_shared_source() -> None:
    from arifosmcp.transport.streamable_http_server import TOOL_ALIASES

    assert TOOL_ALIASES == PUBLIC_TOOL_ALIASES
    assert TOOL_ALIASES["audit"] == "apex_judge"
    assert TOOL_ALIASES["forge"] == "apex_judge"


def test_legacy_rest_aliases_use_shared_source() -> None:
    from arifosmcp.transport.rest import TOOL_ALIASES

    assert TOOL_ALIASES == PUBLIC_TOOL_ALIASES
    assert TOOL_ALIASES["apex_verdict"] == "apex_judge"
    assert TOOL_ALIASES["judge_soul"] == "apex_judge"


@pytest.mark.anyio
async def test_internal_server_mirrors_public_resources_and_prompt() -> None:
    from arifosmcp.transport.server import create_unified_mcp_server

    async with Client(create_unified_mcp_server()) as client:
        resources = await client.list_resources()
        resource_uris = {str(r.uri) for r in resources}
        assert PUBLIC_RESOURCE_URIS["schemas"] in resource_uris
        assert PUBLIC_RESOURCE_URIS["full_context_pack"] in resource_uris

        prompts = await client.list_prompts()
        prompt_names = {p.name for p in prompts}
        assert PUBLIC_PROMPT_NAMES["aaa_chain"] in prompt_names

        prompt = await client.get_prompt(
            PUBLIC_PROMPT_NAMES["aaa_chain"],
            {"query": "hello", "actor_id": "ops"},
        )
        assert prompt.messages
        assert "apex_judge" in prompt.messages[0].content.text

        contents = await client.read_resource(PUBLIC_RESOURCE_URIS["schemas"])
        first = contents[0]
        text = first.text if hasattr(first, "text") else first.blob.decode("utf-8")
        payload = json.loads(text if isinstance(text, str) else str(text))
        assert "inputs" in payload
        assert "outputs" in payload
