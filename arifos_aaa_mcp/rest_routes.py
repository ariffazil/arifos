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
import time
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response

BUILD_INFO = {
    "version": "2026.02.23",
    "git_sha": os.environ.get("GIT_SHA", "unknown"),
    "build_time": os.environ.get("BUILD_TIME", datetime.now(timezone.utc).isoformat()),
}

# Canonical aliases — legacy and mid-gen names → current UX names.
TOOL_ALIASES: dict[str, str] = {
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "recall_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "judge_soul",
    "sovereign_actuator": "forge_hand",
    "vault_seal": "seal_vault",
    "search": "search_reality",
    "fetch": "fetch_content",
    "analyze": "inspect_file",
    "system_audit": "audit_rules",
    # Legacy 9-verb surface
    "anchor": "anchor_session",
    "reason": "reason_mind",
    "integrate": "reason_mind",
    "respond": "reason_mind",
    "validate": "simulate_heart",
    "align": "simulate_heart",
    "forge": "judge_soul",
    "audit": "judge_soul",
    "seal": "seal_vault",
}

WELCOME_HTML = """\
<!DOCTYPE html>
<html>
<head>
    <title>arifOS MCP Server</title>
    <style>
        body { background: #050505; color: #e6c25d; font-family: 'JetBrains Mono', monospace; padding: 4rem; text-align: center; }
        .box { border: 1px solid #e6c25d33; padding: 2rem; display: inline-block; border-radius: 8px; background: #0a0a0a; }
        h1 { font-weight: 900; letter-spacing: -0.1rem; border-bottom: 2px solid #e6c25d; display: inline-block; padding-bottom: 0.5rem; }
        p { color: #888; max-width: 400px; margin: 1rem auto; }
        .status { color: #00ff88; font-weight: bold; margin-top: 2rem; border: 1px solid #00ff8833; padding: 0.5rem 1rem; border-radius: 50px; display: inline-block; }
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
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @mcp.custom_route("/version", methods=["GET"])
    async def version(request: Request) -> Response:
        return JSONResponse(BUILD_INFO)

    @mcp.custom_route("/tools", methods=["GET"])
    async def list_tools(request: Request) -> Response:
        tool_list = []
        for name, fn in tool_registry.items():
            doc = inspect.getdoc(fn) or ""
            sig = inspect.signature(fn)
            params = {
                p_name: {
                    "required": p.default is inspect.Parameter.empty,
                    "default": None if p.default is inspect.Parameter.empty else repr(p.default),
                }
                for p_name, p in sig.parameters.items()
            }
            tool_list.append({"name": name, "description": doc, "parameters": params})
        return JSONResponse({"tools": tool_list, "count": len(tool_list)})

    @mcp.custom_route("/tools/{tool_name:path}", methods=["POST"])
    async def call_tool_rest(request: Request) -> Response:
        """REST-style tool calling for ChatGPT and other HTTP clients."""
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

        tool_fn = tool_registry[canonical_name]

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
                return JSONResponse(json.load(f))
        # Fallback: generate minimal discovery
        return JSONResponse(
            {
                "name": "arifOS AAA MCP",
                "version": BUILD_INFO["version"],
                "transport": {"type": "streamable-http", "url": "/mcp"},
                "tools": list(tool_registry.keys()),
            }
        )
