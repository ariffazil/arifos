from __future__ import annotations

import pytest

from arifosmcp.runtime import phase2_tools
from arifosmcp.runtime import tools as runtime_tools


@pytest.mark.asyncio
async def test_session_memory_tool_routes_payload(monkeypatch):
    captured: dict[str, object] = {}

    async def _fake_call_kernel(tool_name: str, session_id: str, payload: dict[str, object]):
        captured["tool_name"] = tool_name
        captured["session_id"] = session_id
        captured["payload"] = payload
        return {"status": "SUCCESS"}

    monkeypatch.setattr(phase2_tools, "call_kernel", _fake_call_kernel)

    response = await phase2_tools.session_memory(
        session_id="s1",
        operation="store",
        content="remember this",
        top_k=3,
    )

    assert response["status"] == "SUCCESS"
    assert captured["tool_name"] == "session_memory"
    assert captured["session_id"] == "s1"
    assert captured["payload"] == {
        "operation": "store",
        "content": "remember this",
        "top_k": 3,
        "memory_ids": None,
    }


@pytest.mark.asyncio
async def test_runtime_session_memory_uses_public_canonical_tool(monkeypatch):
    captured: dict[str, object] = {}

    async def _fake_wrap_call(
        tool_name: str,
        stage: object,
        session_id: str,
        payload: dict[str, object],
        ctx: object = None,
    ):
        captured["tool_name"] = tool_name
        captured["stage"] = stage
        captured["session_id"] = session_id
        captured["payload"] = payload
        return {"status": "SUCCESS"}

    monkeypatch.setattr(runtime_tools, "_wrap_call", _fake_wrap_call)

    response = await runtime_tools.session_memory(
        session_id="s1",
        operation="retrieve",
        content="remember this",
        top_k=3,
    )

    assert response["status"] == "SUCCESS"
    assert captured["tool_name"] == "session_memory"
    assert captured["session_id"] == "s1"
    assert captured["payload"] == {
        "operation": "retrieve",
        "content": "remember this",
        "memory_ids": None,
        "top_k": 3,
        "auth_context": {},
    }
