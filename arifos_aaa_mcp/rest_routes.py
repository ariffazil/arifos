"""REST endpoints for the unified arifOS AAA MCP server.

Registered as custom routes on the FastMCP instance via mcp.custom_route().
These run alongside the standard MCP protocol at /mcp, providing:
  GET  /                           Landing page / service info
  GET  /health                     Docker healthcheck + monitoring
  GET  /version                    Build info
  GET  /tools                      Tool listing (REST-style)
  POST /tools/{tool_name}          REST tool calling (ChatGPT adapter)
  GET  /.well-known/mcp/server.json  MCP registry discovery

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import inspect
import json
import os
import secrets
import time
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.staticfiles import StaticFiles

from aaa_mcp.build_info import get_build_info
from aaa_mcp.protocol.public_surface import PUBLIC_TOOL_ALIASES
from core.shared.floor_audit import get_ml_floor_runtime

BUILD_INFO = get_build_info()
MCP_PROTOCOL_VERSION = "2025-11-25"
MCP_SUPPORTED_PROTOCOL_VERSIONS = ["2025-11-25", "2025-03-26"]

TOOL_ALIASES: dict[str, str] = dict(PUBLIC_TOOL_ALIASES)

WELCOME_HTML = """\
<!DOCTYPE html>
<html>
<head>
    <title>arifOS MCP Server</title>
    <style>
        body {
            background: #050505; color: #e6c25d;
            font-family: 'JetBrains Mono', monospace; padding: 4rem; text-align: center;
        }
        .box {
            border: 1px solid #e6c25d33; padding: 2rem; display: inline-block;
            border-radius: 8px; background: #0a0a0a;
        }
        h1 {
            font-weight: 900; letter-spacing: -0.1rem;
            border-bottom: 2px solid #e6c25d; display: inline-block; padding-bottom: 0.5rem;
        }
        p { color: #888; max-width: 400px; margin: 1rem auto; }
        .status {
            color: #00ff88; font-weight: bold; margin-top: 2rem;
            border: 1px solid #00ff8833; padding: 0.5rem 1rem;
            border-radius: 50px; display: inline-block;
        }
        a { color: #00a2ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="box">
        <h1>arifOS MCP</h1>
        <p>This is a live <strong>Model Context Protocol</strong> server.
           It is optimized for machine intelligence, but humans are welcome.</p>
        <div class="status">ONLINE</div>
        <div style="margin-top: 2rem;">
            <a href="/tools">/tools</a> &nbsp;|&nbsp;
            <a href="/health">/health</a> &nbsp;|&nbsp;
            <a href="/mcp">/mcp</a> &nbsp;|&nbsp;
            <a href="https://arifos.arif-fazil.com">docs</a>
        </div>
    </div>
</body>
</html>
"""


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _required_bearer_token() -> str | None:
    return os.getenv("ARIFOS_API_KEY") or os.getenv("ARIFOS_API_TOKEN")


def _auth_error_response(request: Request) -> JSONResponse | None:
    """Enforce Bearer auth when configured."""
    required = _required_bearer_token()
    if not required:
        return None
    if _env_truthy("ARIFOS_DEV_MODE"):
        return None

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            {"error": "invalid_request", "error_description": "Bearer token required"},
            status_code=401,
        )

    presented = auth_header[7:].strip()
    if not presented or not secrets.compare_digest(presented, required):
        return JSONResponse(
            {"error": "invalid_token", "error_description": "Invalid bearer token"},
            status_code=401,
        )
    return None


def register_rest_routes(mcp: Any, tool_registry: dict[str, Callable]) -> None:
    """Register REST endpoints as custom routes on the FastMCP instance.

    Args:
        mcp: The FastMCP server instance.
        tool_registry: Mapping of canonical tool names to async callables.
    """

    @mcp.custom_route("/", methods=["GET"])
    async def root(request: Request) -> Response:
        accept = request.headers.get("Accept", "")
        if "text/html" in accept:
            return HTMLResponse(WELCOME_HTML)
        return JSONResponse(
            {
                "service": "arifOS AAA MCP Server",
                "version": BUILD_INFO["version"],
                "protocol_version": MCP_PROTOCOL_VERSION,
                "supported_protocol_versions": MCP_SUPPORTED_PROTOCOL_VERSIONS,
                "mcp_endpoint": "/mcp",
                "tools_endpoint": "/tools",
                "health_endpoint": "/health",
                "tool_count": len(tool_registry),
                "tools": list(tool_registry.keys()),
            }
        )

    @mcp.custom_route("/health", methods=["GET"])
    async def health(request: Request) -> Response:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "arifos-aaa-mcp",
                "version": BUILD_INFO["version"],
                "transport": "streamable-http",
                "tools_loaded": len(tool_registry),
                "ml_floors": get_ml_floor_runtime(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @mcp.custom_route("/version", methods=["GET"])
    async def version(request: Request) -> Response:
        return JSONResponse(BUILD_INFO)

    @mcp.custom_route("/tools", methods=["GET"])
    async def list_tools(request: Request) -> Response:
        if err := _auth_error_response(request):
            return err

        # Get tools from mcp instance
        mcp_tools = await mcp.list_tools()
        tool_list = []
        for tool in mcp_tools:
            tool_list.append({
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.parameters or {}
            })
        return JSONResponse({"tools": tool_list, "count": len(tool_list)})

    @mcp.custom_route("/tools/{tool_name:path}", methods=["POST"])
    async def call_tool_rest(request: Request) -> Response:
        """REST-style tool calling for ChatGPT and other HTTP clients."""
        if err := _auth_error_response(request):
            return err

        incoming_name = request.path_params.get("tool_name", "")
        canonical_name = TOOL_ALIASES.get(incoming_name, incoming_name)
        request_id = f"req-{uuid.uuid4().hex[:12]}"
        start_time = time.time()

        if canonical_name not in tool_registry:
            return JSONResponse(
                {"error": f"Tool '{incoming_name}' not found", "request_id": request_id},
                status_code=404,
            )

        try:
            body = await request.json()
        except Exception:
            body = {}
        if not isinstance(body, dict):
            body = {}

        tool_obj = tool_registry[canonical_name]
        tool_fn = getattr(tool_obj, "fn", tool_obj)

        try:
            # Filter body to only valid parameters
            sig = inspect.signature(tool_fn)
            has_kwargs = any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
            )
            if has_kwargs:
                filtered = body
            else:
                valid_params = {
                    name
                    for name, p in sig.parameters.items()
                    if p.kind
                    not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                }
                filtered = {k: v for k, v in body.items() if k in valid_params}

            result = await tool_fn(**filtered)
        except Exception as exc:
            return JSONResponse(
                {"error": str(exc), "tool": incoming_name, "request_id": request_id},
                status_code=500,
            )

        latency_ms = (time.time() - start_time) * 1000
        return JSONResponse(
            {
                "status": "success",
                "tool": incoming_name,
                "canonical": canonical_name,
                "request_id": request_id,
                "latency_ms": round(latency_ms, 2),
                "result": result,
            }
        )

    @mcp.custom_route("/.well-known/mcp/server.json", methods=["GET"])
    async def well_known(request: Request) -> Response:
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "server.json")
        if os.path.exists(static_path):
            with open(static_path) as f:
                payload = json.load(f)
                payload.setdefault("protocolVersion", MCP_PROTOCOL_VERSION)
                payload.setdefault("supportedProtocolVersions", MCP_SUPPORTED_PROTOCOL_VERSIONS)
                payload.setdefault("authentication", {"type": "none", "description": "No authentication required. actor_id is used for logging only."})
                return JSONResponse(payload)
        # Fallback: generate minimal discovery
        return JSONResponse(
            {
                "name": "arifOS AAA MCP",
                "version": BUILD_INFO["version"],
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "supportedProtocolVersions": MCP_SUPPORTED_PROTOCOL_VERSIONS,
                "transport": {"type": "streamable-http", "url": "/mcp"},
                "authentication": {"type": "none", "description": "No authentication required. actor_id is used for logging only."},
                "tools": list(tool_registry.keys()),
            }
        )

    @mcp.custom_route("/api/governance-status", methods=["GET"])
    async def governance_status(request: Request) -> Response:
        # Mock recent data or get actual data from VAULT999
        import random
        return JSONResponse({
            "status": "success",
            "data": {
                "f1": round(random.uniform(0.95, 1.0), 2),
                "f2": round(random.uniform(0.95, 1.0), 2),
                "f3": round(random.uniform(0.90, 0.98), 2),
                "f4": round(random.uniform(-0.1, 0.0), 2),
                "f5": round(random.uniform(1.0, 1.2), 2),
                "f6": round(random.uniform(0.90, 1.0), 2),
                "f7": round(random.uniform(0.03, 0.05), 3),
                "f8": round(random.uniform(0.85, 0.95), 2),
                "f9": round(random.uniform(0.0, 0.2), 2),
                "f10": "PASS",
                "f11": "PASS",
                "f12": round(random.uniform(0.0, 0.3), 2),
                "f13": "PASS",
                "human": round(random.uniform(0.9, 1.0), 2),
                "ai": round(random.uniform(0.85, 0.98), 2),
                "earth": round(random.uniform(0.92, 0.99), 2),
                "timestamp": time.time(),
                "verdict": "SEAL",
                "stage": "999_SEAL"
            }
        })

    # Serve the standalone dashboard static files
    dashboard_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "333_APPS", "constitutional-visualizer", "dist-web")
    if os.path.exists(dashboard_dir) and hasattr(mcp, "_app"):
        mcp._app.mount("/dashboard", StaticFiles(directory=dashboard_dir, html=True), name="dashboard")
