"""Core MCP operation tests for arifOS AAA MCP.

Covers FastMCP client operations against the in-memory server transport:
- call_tool (structured + content access)
- call_tool options (timeout, progress_handler, meta)
- call_tool_mcp raw protocol access
- read_resource + read_resource_mcp
- get_prompt + get_prompt_mcp
"""

from __future__ import annotations

import json
from typing import Any

from fastmcp.client.client import Client as FastMCPClient


def _resource_text(items: list[Any]) -> str:
    assert items, "resource returned no content"
    first = items[0]
    if hasattr(first, "text"):
        return str(getattr(first, "text"))
    if hasattr(first, "blob"):
        blob = getattr(first, "blob")
        if isinstance(blob, (bytes, bytearray)):
            return blob.decode("utf-8", errors="replace")
    raise AssertionError(f"unexpected resource content type: {type(first)}")


async def test_call_tool_returns_structured_data_and_content(aaa_client: FastMCPClient) -> None:
    result = await aaa_client.call_tool(
        "anchor_session",
        {"query": "core ops test", "actor_id": "ops"},
        timeout=2.0,
        meta={"trace_id": "core-op-1", "request_source": "pytest"},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert result.data.get("tool") == "anchor_session"
    assert result.content, "Expected MCP content blocks to be present"


async def test_call_tool_supports_timeout_progress_and_meta(aaa_client: FastMCPClient) -> None:
    progress_events: list[dict[str, Any]] = []

    def _progress(event: Any) -> None:
        progress_events.append({"event": str(event)})

    result = await aaa_client.call_tool(
        "check_vital",
        {"include_swap": False, "include_io": False, "include_temp": False},
        timeout=30.0,
        progress_handler=_progress,
        meta={"trace_id": "core-op-2"},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert result.data.get("tool") == "check_vital"


async def test_call_tool_mcp_raw_protocol_access(aaa_client: FastMCPClient) -> None:
    raw = await aaa_client.call_tool_mcp(
        "search_reality",
        {"query": "arifOS"},
        timeout=2.0,
        meta={"trace_id": "core-op-3"},
    )

    assert hasattr(raw, "isError")
    assert hasattr(raw, "content")
    assert raw.isError is False


async def test_read_resource_and_read_resource_mcp(aaa_client: FastMCPClient) -> None:
    content = await aaa_client.read_resource("arifos://aaa/schemas")
    text = _resource_text(content)
    payload = json.loads(text)
    assert payload.get("tool_count") == 13

    raw = await aaa_client.read_resource_mcp("arifos://aaa/full-context-pack")
    assert hasattr(raw, "contents")
    assert raw.contents


async def test_get_prompt_and_get_prompt_mcp(aaa_client: FastMCPClient) -> None:
    prompt = await aaa_client.get_prompt(
        "arifos.prompt.aaa_chain",
        {"query": "hello", "actor_id": "ops"},
    )
    assert hasattr(prompt, "messages")
    assert prompt.messages
    first_text = prompt.messages[0].content.text
    assert "anchor_session" in first_text
    assert "seal_vault" in first_text

    raw = await aaa_client.get_prompt_mcp(
        "arifos.prompt.aaa_chain",
        {"query": "hello", "actor_id": "ops"},
    )
    assert hasattr(raw, "messages")
    assert raw.messages
