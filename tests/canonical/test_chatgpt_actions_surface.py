"""Contract checks for ChatGPT Actions deployment surface."""

from __future__ import annotations

import importlib
from pathlib import Path

from fastmcp import Client
from starlette.testclient import TestClient

from arifosmcp.runtime.fastmcp_ext.transports import _build_http_middleware
from arifosmcp.runtime.rest_routes import _openapi_schema
from arifosmcp.runtime.server import app as runtime_http_app
from arifosmcp.runtime.server import create_aaa_mcp_server


def test_actions_routes_are_registered() -> None:
    mcp = create_aaa_mcp_server()
    routes = getattr(mcp, "_additional_http_routes", [])
    route_map = {
        getattr(route, "path", ""): set(getattr(route, "methods", set())) for route in routes
    }

    assert "/openapi.json" in route_map
    assert "GET" in route_map["/openapi.json"]
    assert "/checkpoint" in route_map
    assert "POST" in route_map["/checkpoint"]


def test_openapi_schema_contains_checkpoint_contract() -> None:
    schema = _openapi_schema("https://arifosmcp.arif-fazil.com")

    assert schema["openapi"] == "3.1.0"
    assert "/checkpoint" in schema["paths"]
    assert "post" in schema["paths"]["/checkpoint"]
    op = schema["paths"]["/checkpoint"]["post"]
    assert op["operationId"] == "evaluateCheckpoint"
    assert op["requestBody"]["required"] is True
    assert "CheckpointRequest" in schema["components"]["schemas"]
    assert "CheckpointResponse" in schema["components"]["schemas"]


def test_default_cors_allows_chatgpt_origins() -> None:
    middleware = _build_http_middleware()
    cors_layers = [m for m in middleware if getattr(m, "cls", None).__name__ == "CORSMiddleware"]
    assert cors_layers, "CORSMiddleware must be enabled in HTTP transport by default"

    allow_origins = cors_layers[0].kwargs.get("allow_origins", [])
    assert "https://chat.openai.com" in allow_origins
    assert "https://chatgpt.com" in allow_origins


async def test_dashboard_app_surface_is_registered() -> None:
    mcp = create_aaa_mcp_server()

    async with Client(mcp) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()

    tool_names = {tool.name for tool in tools}
    tool_meta = {tool.name: (tool.meta or {}) for tool in tools}
    resource_uris = {str(resource.uri) for resource in resources}

    assert "open_apex_dashboard" in tool_names
    assert "ui://apex/dashboard.html" in resource_uris
    assert tool_meta["open_apex_dashboard"]["ui"]["resourceUri"] == "ui://apex/dashboard.html"


async def test_metabolic_loop_router_is_described_as_chatgpt_entrypoint() -> None:
    mcp = create_aaa_mcp_server()

    async with Client(mcp) as client:
        tools = await client.list_tools()

    descriptions = {tool.name: (tool.description or "") for tool in tools}
    router_description = descriptions["metabolic_loop_router"].lower()

    assert "preferred entrypoint" in router_description
    assert "chatgpt" in router_description


def test_dashboard_assets_are_packaged_for_deployment() -> None:
    manifest = Path("MANIFEST.in").read_text(encoding="utf-8")
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert "recursive-include arifosmcp/sites" in manifest
    assert 'sites/apex-dashboard/*.html' in pyproject


def test_auth_continuity_secret_prefers_stable_env(monkeypatch) -> None:
    import core.enforcement.auth_continuity as auth_continuity

    sample = {
        "session_id": "sess-1",
        "actor_id": "actor-1",
        "token_fingerprint": "sha256:test",
        "nonce": "nonce-1",
        "iat": 1,
        "exp": 2,
        "approval_scope": ["reason_mind"],
        "parent_signature": "",
    }

    monkeypatch.setenv("ARIFOS_GOVERNANCE_SECRET", "stable-shared-secret")
    reloaded = importlib.reload(auth_continuity)
    sig_one = reloaded.sign_auth_context(sample)
    sig_two = importlib.reload(reloaded).sign_auth_context(sample)
    assert sig_one == sig_two

    monkeypatch.delenv("ARIFOS_GOVERNANCE_SECRET", raising=False)
    monkeypatch.delenv("ARIFOS_GOVERNANCE_TOKEN_SECRET", raising=False)
    fallback_one = importlib.reload(reloaded).sign_auth_context(sample)
    fallback_two = importlib.reload(reloaded).sign_auth_context(sample)
    assert fallback_one != fallback_two


async def test_chatgpt_profile_exposes_orchestrator_first_surface(monkeypatch) -> None:
    import arifosmcp.runtime.server as runtime_server

    monkeypatch.setenv("ARIFOS_PUBLIC_TOOL_PROFILE", "chatgpt")
    reloaded = importlib.reload(runtime_server)

    try:
        async with Client(reloaded.create_aaa_mcp_server()) as client:
            tools = await client.list_tools()
    finally:
        monkeypatch.delenv("ARIFOS_PUBLIC_TOOL_PROFILE", raising=False)
        importlib.reload(reloaded)

    tool_names = {tool.name for tool in tools}

    assert "metabolic_loop_router" in tool_names
    assert "init_anchor_state" not in tool_names
    assert "reason_mind_synthesis" not in tool_names
    assert "assess_heart_impact" not in tool_names


def _runtime_initialize_payload() -> dict[str, object]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "pytest", "version": "1.0"},
        },
    }


def test_runtime_http_initialize_accepts_json_only() -> None:
    with TestClient(runtime_http_app) as client:
        response = client.post(
            "/mcp",
            json=_runtime_initialize_payload(),
            headers={"accept": "application/json"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["protocolVersion"] == "2025-11-25"


def test_runtime_http_init_anchor_state_calls_with_json_only() -> None:
    with TestClient(runtime_http_app) as client:
        init_response = client.post(
            "/mcp",
            json=_runtime_initialize_payload(),
            headers={"accept": "application/json"},
        )
        assert init_response.status_code == 200

        call_response = client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "init_anchor_state",
                    "arguments": {
                        "intent": {"query": "hello"},
                        "governance": {"actor_id": "ops"},
                    },
                },
            },
            headers={
                "accept": "application/json",
                "MCP-Protocol-Version": "2025-11-25",
            },
        )

    assert call_response.status_code == 200
    payload = call_response.json()
    assert payload["jsonrpc"] == "2.0"
    assert "result" in payload
