"""
arifOS StreamableHTTP MCP Server
Dedicated POST endpoint for MCP 2024-11-05 spec
Runs alongside main SSE server
"""

import asyncio
import json
import os
import sys
import uuid

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


async def mcp_endpoint(request: Request) -> JSONResponse:
    """Handle MCP StreamableHTTP requests."""
    body = await request.json()
    method = body.get("method")
    request_id = body.get("id", 1)
    params = body.get("params", {})

    # Generate or use existing session ID
    session_id = request.headers.get("Mcp-Session-Id", str(uuid.uuid4()))

    if method == "initialize":
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}, "logging": {}, "prompts": {}, "resources": {}},
                    "serverInfo": {"name": "arifos-aaa-mcp", "version": "2026.02.15-FORGE-TRINITY-SEAL"},
                },
            },
            headers={"Mcp-Session-Id": session_id},
        )

    elif method == "tools/list":
        tools = [{"name": name, "description": desc} for name, desc in TOOL_DESCRIPTIONS.items()]
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
            if hasattr(tool, 'fn') and callable(tool.fn):
                # Use the underlying function
                func = tool.fn
            elif callable(tool):
                func = tool
            else:
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
    """Health check."""
    return JSONResponse(
        {
            "status": "healthy",
            "transport": "streamable-http",
            "version": "2026.02.15-FORGE-TRINITY-SEAL",
            "endpoints": ["/mcp", "/health"],
        }
    )


routes = [
    Route("/mcp", mcp_endpoint, methods=["POST"]),
    Route("/health", health, methods=["GET"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8889)
