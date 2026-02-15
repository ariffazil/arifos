"""
arifOS StreamableHTTP MCP Server
Dedicated POST endpoint for MCP 2024-11-05 spec
Runs alongside main SSE server
"""

import json
import uuid
from typing import Any, Dict

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn


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
                    "capabilities": {
                        "tools": {},
                        "logging": {},
                        "prompts": {},
                        "resources": {}
                    },
                    "serverInfo": {
                        "name": "arifos-aaa-mcp",
                        "version": "64.2-FORGE-TRINITY-SEAL"
                    }
                }
            },
            headers={"Mcp-Session-Id": session_id}
        )
    
    elif method == "tools/list":
        tools = [
            {"name": "anchor", "description": "1. ANCHOR (000) - Init & Sense"},
            {"name": "reason", "description": "2. REASON (222) - Think & Hypothesize"},
            {"name": "integrate", "description": "3. INTEGRATE (333) - Map & Ground"},
            {"name": "respond", "description": "4. RESPOND (444) - Draft Plan"},
            {"name": "validate", "description": "5. VALIDATE (555) - Safety & Impact"},
            {"name": "align", "description": "6. ALIGN (666) - Ethics & Constitution"},
            {"name": "forge", "description": "7. FORGE (777) - Synthesize Solution"},
            {"name": "audit", "description": "8. AUDIT (888) - Verify & Judge"},
            {"name": "seal", "description": "9. SEAL (999) - Commit to Vault"}
        ]
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}},
            headers={"Mcp-Session-Id": session_id}
        )
    
    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        
        # Simple passthrough for now
        result = {"status": "called", "tool": tool_name, "args": tool_args}
        
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
            },
            headers={"Mcp-Session-Id": session_id}
        )
    
    else:
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            },
            headers={"Mcp-Session-Id": session_id}
        )


async def health(request: Request) -> JSONResponse:
    """Health check."""
    return JSONResponse({
        "status": "healthy",
        "transport": "streamable-http",
        "version": "64.2-FORGE-TRINITY-SEAL",
        "endpoints": ["/mcp", "/health"]
    })


routes = [
    Route("/mcp", mcp_endpoint, methods=["POST"]),
    Route("/health", health, methods=["GET"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8889)
