"""Contract checks for ChatGPT Actions deployment surface."""

from __future__ import annotations

from arifos_aaa_mcp.fastmcp_ext.transports import _build_http_middleware
from arifos_aaa_mcp.rest_routes import _openapi_schema
from arifos_aaa_mcp.server import create_aaa_mcp_server


def test_actions_routes_are_registered() -> None:
    mcp = create_aaa_mcp_server()
    routes = getattr(mcp, "_additional_http_routes", [])
    route_map = {getattr(route, "path", ""): set(getattr(route, "methods", set())) for route in routes}

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

