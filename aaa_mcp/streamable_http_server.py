"""
arifOS StreamableHTTP MCP Server
Dedicated POST endpoint for MCP 2024-11-05 spec
Runs alongside main SSE server

Identity Policy: "Guest book only, no bouncer"
- Transport auth: none (by design)
- Identity: mandatory to log, optional to enforce
- Required fields: user_id, session_id (clientInfo and/or headers)
- No request rejection if IDs missing
- Log "null" for missing fields
"""

import asyncio
import inspect
import json
import os
import sys
import uuid
from datetime import datetime
from typing import Any, get_args, get_origin

# Force local source priority (same as rest.py)
sys.path.insert(0, os.getcwd())

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Import tools directly from server module (avoid mcp wrapper issues)
from aaa_mcp.server import anchor, reason, integrate, respond, validate, align, forge, audit, seal

# Tool registry mapping names to functions
TOOLS = {
    "anchor": anchor,
    "reason": reason,
    "integrate": integrate,
    "respond": respond,
    "validate": validate,
    "align": align,
    "forge": forge,
    "audit": audit,
    "seal": seal,
}

# Tool descriptions for listing
TOOL_DESCRIPTIONS = {
    "anchor": "1. ANCHOR (000) - Init & Sense",
    "reason": "2. REASON (222) - Think & Hypothesize",
    "integrate": "3. INTEGRATE (333) - Map & Ground",
    "respond": "4. RESPOND (444) - Draft Plan",
    "validate": "5. VALIDATE (555) - Safety & Impact",
    "align": "6. ALIGN (666) - Ethics & Constitution",
    "forge": "7. FORGE (777) - Synthesize Solution",
    "audit": "8. AUDIT (888) - Verify & Judge",
    "seal": "9. SEAL (999) - Commit to Vault",
}


async def log_identity(
    user_id: str | None,
    session_id: str | None,
    client_name: str | None,
    client_version: str | None,
    timestamp: datetime,
    method: str,
) -> None:
    """
    Log identity metadata to cooling ledger (guest book).

    Path A: Logging only, no enforcement.
    Logs to /tmp/arifos-identity.log for now (append-only).
    """
    log_entry = {
        "timestamp": timestamp.isoformat(),
        "method": method,
        "user_id": user_id,
        "session_id": session_id,
        "client_name": client_name,
        "client_version": client_version,
    }

    # Simple append-only log file (cooling ledger stub)
    log_file = "/tmp/arifos-identity.log"
    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        # Don't fail the request if logging fails
        print(f"Identity logging failed: {e}")

    # Also print to console for debugging
    print(f"IDENTITY: {json.dumps(log_entry)}")


def _resolve_tool_callable(tool: Any):
    """Resolve FastMCP FunctionTool wrappers to raw callables."""
    if hasattr(tool, "fn") and callable(tool.fn):
        return tool.fn
    if callable(tool):
        return tool
    return None


def _annotation_to_json_type(annotation: Any) -> str:
    """Convert Python annotation to a coarse JSON Schema type."""
    if annotation is inspect._empty:
        return "string"

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is None:
        if annotation in (str,):
            return "string"
        if annotation in (int, float):
            return "number"
        if annotation is bool:
            return "boolean"
        if annotation in (list, tuple, set):
            return "array"
        if annotation is dict:
            return "object"
        return "string"

    if origin in (list, tuple, set):
        return "array"
    if origin is dict:
        return "object"
    if origin is Any:
        return "object"

    # Optional[T] / Union[T, None]
    if str(origin).endswith("Union") and args:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return _annotation_to_json_type(non_none[0])
        return "string"

    return "string"


def _build_input_schema(tool: Any) -> dict:
    """Build MCP-compliant inputSchema from tool signature."""
    func = _resolve_tool_callable(tool)
    if func is None:
        return {"type": "object", "properties": {}, "additionalProperties": True}

    sig = inspect.signature(func)
    properties: dict[str, dict] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        prop = {"type": _annotation_to_json_type(param.annotation)}
        if param.default is not inspect._empty:
            prop["default"] = param.default
        else:
            required.append(name)
        properties[name] = prop

    schema = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
    }
    if required:
        schema["required"] = required
    return schema


async def mcp_endpoint(request: Request) -> JSONResponse:
    """Handle MCP StreamableHTTP requests."""
    body = await request.json()
    method = body.get("method")
    request_id = body.get("id", 1)
    params = body.get("params", {})

    # Capture identity metadata (Path A: guest book only)
    client_info = params.get("clientInfo", {})

    # Extract user_id from clientInfo or headers
    user_id = client_info.get("user_id") or request.headers.get("x-arifos-user-id")

    # Extract session_id with fallback chain:
    # 1. clientInfo.session_id
    # 2. x-arifos-session-id header
    # 3. mcp-session-id header (standard MCP)
    # 4. Generate new UUID (last resort)
    session_id = (
        client_info.get("session_id")
        or request.headers.get("x-arifos-session-id")
        or request.headers.get("mcp-session-id")
        or str(uuid.uuid4())
    )

    # Log identity (guest book entry)
    await log_identity(
        user_id=user_id,
        session_id=session_id,
        client_name=client_info.get("name"),
        client_version=client_info.get("version"),
        timestamp=datetime.utcnow(),
        method=method or "unknown",
    )

    if method == "initialize":
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}, "logging": {}, "prompts": {}, "resources": {}},
                    "serverInfo": {
                        "name": "arifos-aaa-mcp",
                        "version": "2026.02.17-FORGE-VPS-SEAL",
                    },
                },
            },
            headers={"Mcp-Session-Id": session_id},
        )

    elif method == "tools/list":
        tools = []
        for name, desc in TOOL_DESCRIPTIONS.items():
            tools.append(
                {
                    "name": name,
                    "description": desc,
                    "inputSchema": _build_input_schema(TOOLS[name]),
                }
            )
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}},
            headers={"Mcp-Session-Id": session_id},
        )

    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})

        if tool_name not in TOOLS:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Tool not found: {tool_name}"},
                },
                headers={"Mcp-Session-Id": session_id},
            )

        tool = TOOLS[tool_name]

        try:
            # Call tool with timeout protection (10 seconds)
            # FastMCP 2.x tools are FunctionTool objects with fn attribute
            func = _resolve_tool_callable(tool)
            if func is None:
                raise ValueError(f"Tool {tool_name} is not callable")

            result = await asyncio.wait_for(func(**tool_args), timeout=10.0)
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                },
                headers={"Mcp-Session-Id": session_id},
            )
        except asyncio.TimeoutError:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": "Tool execution timeout"},
                },
                headers={"Mcp-Session-Id": session_id},
            )
        except Exception as e:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32000, "message": f"Tool execution error: {str(e)}"},
                },
                headers={"Mcp-Session-Id": session_id},
            )

    else:
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            },
            headers={"Mcp-Session-Id": session_id},
        )


async def health(request: Request) -> JSONResponse:
    """Health check with governance metrics."""
    from aaa_mcp.infrastructure.monitoring import get_health_monitor, get_metrics_collector

    monitor = get_health_monitor()
    collector = get_metrics_collector()

    health_results = await monitor.check_all()
    stats = collector.get_stats()

    return JSONResponse(
        {
            "status": "healthy" if monitor.is_healthy() else "degraded",
            "transport": "streamable-http",
            "version": "2026.02.17-FORGE-VPS-SEAL",
            "governance_metrics": stats,
            "health_checks": health_results,
            "endpoints": ["/mcp", "/health"],
        }
    )


routes = [
    Route("/mcp", mcp_endpoint, methods=["POST"]),
    Route("/health", health, methods=["GET"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    # Initialize monitoring
    from aaa_mcp.infrastructure.monitoring import init_monitoring

    asyncio.run(init_monitoring())

    uvicorn.run(app, host="0.0.0.0", port=8889)
