"""888 APEX TEST — MCP protocol E2E for arifOS AAA MCP.

Verifies via FastMCP Client (MCP protocol path):
- tools list includes canonical 13
- prompts/resources are discoverable and readable
- each tool is callable with minimal arguments
- responses contain governance envelope fields
"""

from __future__ import annotations

import json
from typing import Any

from fastmcp.client.client import Client as FastMCPClient
from starlette.testclient import TestClient

from aaa_mcp.streamable_http_server import PROTOCOL_HEADER, SESSION_HEADER
from aaa_mcp.streamable_http_server import app as streamable_app

EXPECTED_13 = {
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
}


def _unwrap(obj: Any) -> Any:
    if hasattr(obj, "data"):
        return obj.data
    return obj


def _resource_text(contents: Any) -> str:
    """FastMCP resources return a list of ResourceContents objects."""
    if isinstance(contents, list) and contents:
        first = contents[0]
        if hasattr(first, "text"):
            return str(first.text)
        if hasattr(first, "blob"):
            blob = first.blob
            if isinstance(blob, (bytes, bytearray)):
                return blob.decode("utf-8", errors="replace")
    if isinstance(contents, bytes):
        return contents.decode("utf-8", errors="replace")
    if isinstance(contents, str):
        return contents
    raise AssertionError(f"Unexpected resource contents type: {type(contents)}")


def _assert_envelope(payload: dict[str, Any]) -> None:
    assert isinstance(payload, dict)
    assert "verdict" in payload
    assert "tool" in payload
    assert "axioms_333" in payload
    assert "laws_13" in payload
    assert "apex_dials" in payload
    assert "motto" in payload
    assert "data" in payload


async def test_phase888_mcp_lists_tools_prompts_resources_and_calls_all_13(
    aaa_client: FastMCPClient,
) -> None:
    client = aaa_client
    tools = await client.list_tools()
    tool_names = {t.name for t in tools}
    assert tool_names == EXPECTED_13

    prompts = await client.list_prompts()
    prompt_names = {p.name for p in prompts}
    assert "arifos.prompt.aaa_chain" in prompt_names

    resources = await client.list_resources()
    resource_uris = {str(r.uri) for r in resources}
    assert "arifos://aaa/schemas" in resource_uris
    assert "arifos://aaa/full-context-pack" in resource_uris

    schemas_contents = _unwrap(await client.read_resource("arifos://aaa/schemas"))
    schemas = json.loads(_resource_text(schemas_contents))
    assert schemas.get("tool_count") == 13
    assert set(schemas.get("surface", [])) == EXPECTED_13

    full_context_contents = _unwrap(await client.read_resource("arifos://aaa/full-context-pack"))
    full_context = json.loads(_resource_text(full_context_contents))
    assert "stage_spine" in full_context
    assert "continuity" in full_context

    prompt_obj = await client.get_prompt(
        "arifos.prompt.aaa_chain", arguments={"query": "hello", "actor_id": "ops"}
    )
    # FastMCP returns GetPromptResult with `messages`.
    assert hasattr(prompt_obj, "messages")
    messages = prompt_obj.messages
    assert messages
    content = messages[0].content
    text = content.text
    assert "anchor_session" in text
    assert "seal_vault" in text

    init_res = await client.call_tool(
        "anchor_session", arguments={"query": "phase888", "actor_id": "ops"}
    )
    init = _unwrap(init_res)
    _assert_envelope(init)
    session_id = init["data"].get("session_id", "")
    assert session_id

    reason = _unwrap(
        await client.call_tool(
            "reason_mind", arguments={"query": "verify", "session_id": session_id}
        )
    )
    _assert_envelope(reason)

    recall = _unwrap(
        await client.call_tool(
            "recall_memory",
            arguments={"current_thought_vector": "vector", "session_id": session_id},
        )
    )
    _assert_envelope(recall)

    heart = _unwrap(
        await client.call_tool(
            "simulate_heart", arguments={"query": "impact", "session_id": session_id}
        )
    )
    _assert_envelope(heart)

    critique = _unwrap(
        await client.call_tool(
            "critique_thought",
            arguments={"plan": {"step": "x", "risk": "low"}, "session_id": session_id},
        )
    )
    _assert_envelope(critique)

    judge = _unwrap(
        await client.call_tool(
            "apex_judge",
            arguments={
                "session_id": session_id,
                "query": "verdict",
                "agi_result": reason.get("data", {}),
                "asi_result": heart.get("data", {}),
                "critique_result": critique.get("data", {}),
            },
        )
    )
    _assert_envelope(judge)

    forge = _unwrap(
        await client.call_tool(
            "eureka_forge",
            arguments={
                "action_payload": {"action": "noop"},
                "session_id": session_id,
                "signature": "phase888",
            },
        )
    )
    _assert_envelope(forge)

    seal = _unwrap(
        await client.call_tool(
            "seal_vault",
            arguments={"session_id": session_id, "summary": "phase888", "verdict": "SEAL"},
        )
    )
    _assert_envelope(seal)

    search = _unwrap(await client.call_tool("search_reality", arguments={"query": "arifOS"}))
    _assert_envelope(search)

    fetch = _unwrap(
        await client.call_tool(
            "fetch_content", arguments={"id": "https://example.com", "max_chars": 200}
        )
    )
    _assert_envelope(fetch)

    fs = _unwrap(
        await client.call_tool("inspect_file", arguments={"path": ".", "depth": 1, "max_files": 5})
    )
    _assert_envelope(fs)

    audit = _unwrap(await client.call_tool("audit_rules", arguments={"audit_scope": "quick"}))
    _assert_envelope(audit)

    vital = _unwrap(await client.call_tool("check_vital", arguments={"include_swap": False}))
    _assert_envelope(vital)


def _jsonrpc_initialize_payload(protocol_version: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": protocol_version,
            "capabilities": {},
            "clientInfo": {"name": "pytest", "version": "1.0"},
        },
    }


def test_streamable_initialize_negotiates_supported_older_version() -> None:
    client = TestClient(streamable_app)
    resp = client.post(
        "/mcp",
        json=_jsonrpc_initialize_payload("2025-03-26"),
        headers={"accept": "application/json"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["result"]["protocolVersion"] == "2025-03-26"
    assert resp.headers.get(PROTOCOL_HEADER) == "2025-03-26"
    assert resp.headers.get(SESSION_HEADER)


def test_streamable_initialize_rejects_unsupported_version() -> None:
    client = TestClient(streamable_app)
    resp = client.post(
        "/mcp",
        json=_jsonrpc_initialize_payload("2099-01-01"),
        headers={"accept": "application/json"},
    )
    assert resp.status_code == 400
    body = resp.json()
    assert body["error"]["code"] == -32602
    assert "Unsupported protocolVersion" in body["error"]["message"]


def test_streamable_session_rejects_protocol_mismatch_after_initialize() -> None:
    client = TestClient(streamable_app)
    init_resp = client.post(
        "/mcp",
        json=_jsonrpc_initialize_payload("2025-03-26"),
        headers={"accept": "application/json"},
    )
    assert init_resp.status_code == 200
    session_id = init_resp.headers.get(SESSION_HEADER)
    assert session_id

    tools_list_resp = client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        headers={
            "accept": "application/json",
            SESSION_HEADER: session_id,
            PROTOCOL_HEADER: "2025-11-25",
        },
    )
    assert tools_list_resp.status_code == 400
    payload = tools_list_resp.json()
    assert payload["error"]["code"] == -32600
    assert "Protocol version mismatch" in payload["error"]["message"]


def test_streamable_initialize_advertises_capabilities() -> None:
    client = TestClient(streamable_app)
    resp = client.post(
        "/mcp",
        json=_jsonrpc_initialize_payload("2025-11-25"),
        headers={"accept": "application/json"},
    )
    assert resp.status_code == 200
    capabilities = resp.json()["result"]["capabilities"]
    assert capabilities["completion"] == {}
    assert capabilities["tools"]["listChanged"] is False
    assert capabilities["resources"]["listChanged"] is False
    assert capabilities["resources"]["subscribe"] is False
    assert capabilities["prompts"]["listChanged"] is False


def test_streamable_completion_complete_prompt_actor_id() -> None:
    client = TestClient(streamable_app)
    init_resp = client.post(
        "/mcp",
        json=_jsonrpc_initialize_payload("2025-11-25"),
        headers={"accept": "application/json"},
    )
    assert init_resp.status_code == 200
    session_id = init_resp.headers.get(SESSION_HEADER)
    assert session_id

    complete_resp = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "completion/complete",
            "params": {
                "ref": {"type": "prompt", "name": "arifos.prompt.aaa_chain"},
                "argument": {"name": "actor_id", "value": "o"},
            },
        },
        headers={
            "accept": "application/json",
            SESSION_HEADER: session_id,
            PROTOCOL_HEADER: "2025-11-25",
        },
    )
    assert complete_resp.status_code == 200
    completion = complete_resp.json()["result"]["completion"]
    assert completion["values"] == ["ops"]
    assert completion["total"] == 1
    assert completion["hasMore"] is False


def test_streamable_resources_subscribe_returns_method_not_found() -> None:
    client = TestClient(streamable_app)
    init_resp = client.post(
        "/mcp",
        json=_jsonrpc_initialize_payload("2025-11-25"),
        headers={"accept": "application/json"},
    )
    assert init_resp.status_code == 200
    session_id = init_resp.headers.get(SESSION_HEADER)
    assert session_id

    subscribe_resp = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/subscribe",
            "params": {"uri": "arifos://aaa/schemas"},
        },
        headers={
            "accept": "application/json",
            SESSION_HEADER: session_id,
            PROTOCOL_HEADER: "2025-11-25",
        },
    )
    assert subscribe_resp.status_code == 400
    payload = subscribe_resp.json()
    assert payload["error"]["code"] == -32601
