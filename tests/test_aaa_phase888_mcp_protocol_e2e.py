"""888 APEX TEST — MCP protocol E2E for arifOS AAA MCP.

Verifies via FastMCP Client (MCP protocol path):
- tools list includes canonical 13
- prompts/resources are discoverable and readable
- each tool is callable with minimal arguments
- responses contain governance envelope fields
"""

from __future__ import annotations

from typing import Any, Dict
import json

from fastmcp.client.client import Client as FastMCPClient

EXPECTED_13 = {
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


def _unwrap(obj: Any) -> Any:
    if hasattr(obj, "data"):
        return getattr(obj, "data")
    return obj


def _resource_text(contents: Any) -> str:
    """FastMCP resources return a list of ResourceContents objects."""
    if isinstance(contents, list) and contents:
        first = contents[0]
        if hasattr(first, "text"):
            return str(getattr(first, "text"))
        if hasattr(first, "blob"):
            blob = getattr(first, "blob")
            if isinstance(blob, (bytes, bytearray)):
                return blob.decode("utf-8", errors="replace")
    if isinstance(contents, bytes):
        return contents.decode("utf-8", errors="replace")
    if isinstance(contents, str):
        return contents
    raise AssertionError(f"Unexpected resource contents type: {type(contents)}")


def _assert_envelope(payload: Dict[str, Any]) -> None:
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
    messages = getattr(prompt_obj, "messages")
    assert messages
    content = getattr(messages[0], "content")
    text = getattr(content, "text")
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
            "judge_soul",
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
            "forge_hand",
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
