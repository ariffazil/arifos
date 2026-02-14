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
from typing import Any

# Force local source priority
sys.path.insert(0, os.getcwd())

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

# Import MCP server to get tools
from aaa_mcp.server import mcp as mcp_server


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
        tools = await mcp_server.get_tools()
        tool_list = []
        for name, tool in tools.items():
            tool_list.append({
                "name": name,
                "description": getattr(tool, 'description', 'No description'),
            })
        return JSONResponse({"tools": tool_list})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def call_tool(request: Request):
    """Call an MCP tool via HTTP POST."""
    tool_name = request.path_params.get("tool_name")
    
    try:
        body = await request.json()
    except Exception:
        body = {}
    
    try:
        # Get tool from MCP server
        tools = await mcp_server.get_tools()
        if tool_name not in tools:
            return JSONResponse(
                {"error": f"Tool '{tool_name}' not found"}, 
                status_code=404
            )
        
        tool = tools[tool_name]
        
        # Call the tool with provided arguments
        result = await tool(**body)
        
        return JSONResponse({
            "status": "success",
            "tool": tool_name,
            "result": result
        })
    except Exception as e:
        return JSONResponse(
            {"error": str(e), "tool": tool_name}, 
            status_code=500
        )


# Create Starlette app with REST routes
routes = [
    Route("/health", health, methods=["GET"]),
    Route("/tools", list_tools, methods=["GET"]),
    Route("/tools/{tool_name}", call_tool, methods=["POST"]),
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
