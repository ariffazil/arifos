"""
AAA MCP REST Bridge — HTTP REST API for OpenAI Tool Adapter
Maps HTTP POST /tools/{name} → MCP tool calls

Endpoints:
  GET  /health              → Health check
  GET  /tools               → List available tools
  POST /tools/{tool_name}   → Call tool with JSON body
  
Usage:
  python -m aaa_mcp.rest
  
DITEMPA BUKAN DIBERI
"""

import os
import sys
import json
import asyncio
from typing import Any, AsyncGenerator

# Force local source priority
sys.path.insert(0, os.getcwd())

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route
from starlette.requests import Request

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

# Tool name aliases for backward compatibility (classic 5-tool schema)
TOOL_ALIASES = {
    "init_session": "anchor",      # 000_INIT → anchor
    "agi_cognition": "reason",     # 111-333_AGI → reason  
    "asi_empathy": "validate",     # 555-666_ASI → validate
    "apex_verdict": "audit",       # 888_APEX → audit
    "vault_seal": "seal",          # 999_VAULT → seal
}

# Tool metadata
TOOL_META = {
    "anchor": {"title": "1. ANCHOR", "description": "Init & Sense (Authority/F12)"},
    "reason": {"title": "2. REASON", "description": "Think & Hypothesize (Risk/Truth)"},
    "integrate": {"title": "3. INTEGRATE", "description": "Map & Ground (Facts)"},
    "respond": {"title": "4. RESPOND", "description": "Draft Response (Clarity)"},
    "validate": {"title": "5. VALIDATE", "description": "Check Impact (Stakeholders)"},
    "align": {"title": "6. ALIGN", "description": "Check Ethics (Anti-Hantu)"},
    "forge": {"title": "7. FORGE", "description": "Synthesize Solution (Code)"},
    "audit": {"title": "8. AUDIT", "description": "Verify & Judge (Consensus)"},
    "seal": {"title": "9. SEAL", "description": "Commit to Vault (Permanence)"},
}


async def route_info(request: Request):
    """Show all available routes for debugging."""
    return JSONResponse({
        "service": "aaa-mcp-rest",
        "version": "64.1.0",
        "routes": [
            {"method": "GET", "path": "/", "description": "This info"},
            {"method": "GET", "path": "/health", "description": "Health check"},
            {"method": "GET", "path": "/tools", "description": "List all tools"},
            {"method": "POST", "path": "/tools/{tool_name}", "description": "Call tool (new names)"},
            {"method": "POST", "path": "/{tool_name}", "description": "Call tool (root path)"},
            {"method": "POST", "path": "/mcp/{tool_name}", "description": "Call tool (MCP prefix)"},
            {"method": "POST", "path": "/api/{tool_name}", "description": "Call tool (API prefix)"},
        ],
        "example": "POST /tools/init_session or POST /init_session",
        "note": "Classic aliases work: init_session, agi_cognition, asi_empathy, apex_verdict, vault_seal"
    })


async def health(request: Request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "aaa-mcp-rest",
        "version": "64.1.0"
    })


async def list_tools(request: Request):
    """List available MCP tools."""
    try:
        tool_list = []
        for name, meta in TOOL_META.items():
            tool_list.append({
                "name": name,
                "description": meta["description"],
            })
        # Also list classic aliases for backward compatibility
        classic_tools = [
            {"name": "init_session", "description": "000_INIT - Session ignition (alias for anchor)", "alias_for": "anchor"},
            {"name": "agi_cognition", "description": "111-333_AGI - Mind/Reasoning (alias for reason)", "alias_for": "reason"},
            {"name": "asi_empathy", "description": "555-666_ASI - Heart/Empathy (alias for validate)", "alias_for": "validate"},
            {"name": "apex_verdict", "description": "888_APEX - Soul/Judgment (alias for audit)", "alias_for": "audit"},
            {"name": "vault_seal", "description": "999_VAULT - Seal/Commit (alias for seal)", "alias_for": "seal"},
        ]
        return JSONResponse({
            "tools": tool_list,
            "classic_aliases": classic_tools,
            "note": "Use classic names (init_session, agi_cognition, etc.) for ChatGPT compatibility"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def call_tool_get(request: Request):
    """Handle GET requests to tool endpoints - explain to use POST."""
    tool_name = request.path_params.get("tool_name")
    return JSONResponse({
        "error": "Method not allowed",
        "message": f"Tool '{tool_name}' requires POST, not GET",
        "hint": "Use POST with JSON body",
        "example": {
            "method": "POST",
            "url": f"/tools/{tool_name}",
            "body": {"session_id": "your-session-id"}
        },
        "available_methods": ["POST"]
    }, status_code=405)


async def call_tool(request: Request):
    """Call an MCP tool via HTTP POST."""
    tool_name = request.path_params.get("tool_name")
    
    # Map classic tool names to new names
    original_name = tool_name
    if tool_name in TOOL_ALIASES:
        tool_name = TOOL_ALIASES[tool_name]
    
    try:
        body = await request.json()
    except Exception:
        body = {}
    
    try:
        # Get tool from registry
        if tool_name not in TOOLS:
            return JSONResponse(
                {"error": f"Tool '{original_name}' (mapped to '{tool_name}') not found"}, 
                status_code=404
            )
        
        tool = TOOLS[tool_name]
        
        # Call the tool with provided arguments
        result = await tool(**body)
        
        return JSONResponse({
            "status": "success",
            "tool": original_name,
            "mapped_to": tool_name,
            "result": result
        })
    except Exception as e:
        return JSONResponse(
            {"error": str(e), "tool": original_name}, 
            status_code=500
        )


async def mcp_jsonrpc(request: Request):
    """JSON-RPC compatible endpoint for MCP protocol."""
    try:
        body = await request.json()
        method = body.get("method", "")
        params = body.get("params", {})
        
        # Extract tool name from method (e.g., "init_session" or "tools/init_session")
        tool_name = method.split("/")[-1] if "/" in method else method
        
        # Map classic tool names
        if tool_name in TOOL_ALIASES:
            tool_name = TOOL_ALIASES[tool_name]
        
        # Get tool from registry
        if tool_name not in TOOLS:
            return JSONResponse({
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method '{method}' not found"},
                "id": body.get("id")
            })
        
        tool = TOOLS[tool_name]
        result = await tool(**params)
        
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": result,
            "id": body.get("id")
        })
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": str(e)},
            "id": body.get("id") if body else None
        })


async def sse_endpoint(request: Request):
    """MCP SSE transport endpoint."""
    async def event_generator() -> AsyncGenerator[str, None]:
        # Send initial endpoint event with message URL
        msg_url = f"{request.url.scheme}://{request.url.netloc}/messages"
        yield f"event: endpoint\ndata: {msg_url}\n\n"

        # Keep connection alive with periodic pings
        while True:
            if await request.is_disconnected():
                break
            yield ": ping\n\n"  # SSE comment (heartbeat)
            await asyncio.sleep(30)  # Ping every 30 seconds

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


async def messages_endpoint(request: Request):
    """MCP messages endpoint for client to server communication."""
    try:
        body = await request.json()
        method = body.get("method", "")
        params = body.get("params", {})
        msg_id = body.get("id")

        # Map classic tool names
        tool_name = method.split("/")[-1] if "/" in method else method
        if tool_name in TOOL_ALIASES:
            tool_name = TOOL_ALIASES[tool_name]

        # Execute tool
        if tool_name not in TOOLS:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })

        tool = TOOLS[tool_name]
        result = await tool(**params)

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": result
        })
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in dir() else None,
            "error": {"code": -32603, "message": str(e)}
        })


# Create Starlette app with REST routes
routes = [
    Route("/", route_info, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
    Route("/tools", list_tools, methods=["GET"]),
    Route("/tools/{tool_name}", call_tool, methods=["POST"]),
    Route("/tools/{tool_name}", call_tool_get, methods=["GET"]),  # Helpful 405
    # MCP SSE transport endpoints
    Route("/sse", sse_endpoint, methods=["GET"]),
    Route("/messages", messages_endpoint, methods=["POST"]),
    # JSON-RPC endpoint (MCP standard)
    Route("/mcp", mcp_jsonrpc, methods=["POST"]),
    # Additional routes for different path conventions
    Route("/{tool_name}", call_tool, methods=["POST"]),  # Root path
    Route("/{tool_name}", call_tool_get, methods=["GET"]),  # Helpful 405
    Route("/mcp/{tool_name}", call_tool, methods=["POST"]),  # MCP prefix
    Route("/mcp/{tool_name}", call_tool_get, methods=["GET"]),  # Helpful 405
    Route("/api/{tool_name}", call_tool, methods=["POST"]),  # API prefix
    Route("/api/{tool_name}", call_tool_get, methods=["GET"]),  # Helpful 405
]

app = Starlette(routes=routes, debug=False)


def main():
    """Start REST API server."""
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"[rest] AAA MCP REST Bridge starting on {host}:{port}", file=sys.stderr)
    print(f"[rest] Endpoints: /health, /tools, /tools/{{name}}", file=sys.stderr)
    
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
