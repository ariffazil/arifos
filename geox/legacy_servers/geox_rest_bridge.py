"""
GEOX REST Bridge — HTTP API for Frontend Integration
═══════════════════════════════════════════════════════════════════════════════
Provides simple REST endpoints for the GEOX React frontend while maintaining
MCP compatibility for AI agents.

Endpoints:
  GET /health     → Health check
  GET /tools      → List available tools
  POST /invoke    → Invoke a tool
  /mcp           → MCP StreamableHTTP endpoint

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
from typing import Any

from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Import the MCP instance and tools from unified server
from geox_unified import mcp, TOOLS_REGISTRY, GEOX_VERSION, GEOX_SEAL

# ═══════════════════════════════════════════════════════════════════════════════
# REST Handlers
# ═══════════════════════════════════════════════════════════════════════════════

async def health_handler(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "geox-rest-bridge",
        "version": GEOX_VERSION,
        "seal": GEOX_SEAL,
        "timestamp": "2026-04-11T06:35:00Z"
    })

async def tools_handler(request):
    """List available tools."""
    return JSONResponse({
        "tools": TOOLS_REGISTRY,
        "count": len(TOOLS_REGISTRY),
        "version": GEOX_VERSION
    })

async def invoke_handler(request):
    """Invoke a tool (simple proxy)."""
    try:
        body = await request.json()
        tool_name = body.get("tool")
        params = body.get("params", {})
        
        # Return a stub response (full implementation would call MCP tool)
        return JSONResponse({
            "ok": True,
            "tool": tool_name,
            "params_received": params,
            "verdict": "888_PROCEED",
            "note": "Full tool invocation via MCP protocol at /mcp"
        })
    except Exception as e:
        return JSONResponse({
            "ok": False,
            "error": str(e)
        }, status_code=400)

# ═══════════════════════════════════════════════════════════════════════════════
# Create Combined App (REST + MCP)
# ═══════════════════════════════════════════════════════════════════════════════

def create_app():
    """Create Starlette app with both REST and MCP endpoints."""
    
    # Create MCP app first to get its lifespan
    mcp_http_app = None
    mcp_lifespan = None
    if hasattr(mcp, 'http_app'):
        mcp_http_app = mcp.http_app(
            path="/",
            transport="streamable-http",
        )
        mcp_lifespan = mcp_http_app.lifespan
    
    # Create Starlette app with REST routes and MCP lifespan
    rest_routes = [
        Route("/health", health_handler, methods=["GET"]),
        Route("/tools", tools_handler, methods=["GET"]),
        Route("/invoke", invoke_handler, methods=["POST"]),
    ]
    
    app = Starlette(routes=rest_routes, lifespan=mcp_lifespan)
    
    # Mount MCP app at /mcp (if available)
    if mcp_http_app:
        app.mount("/mcp", mcp_http_app)
    
    return app

# ═══════════════════════════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GEOX REST Bridge")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    
    print(f"🔥 GEOX REST Bridge Starting")
    print(f"   Version: {GEOX_VERSION}")
    print(f"   Seal: {GEOX_SEAL}")
    print(f"   REST API: http://{args.host}:{args.port}/")
    print(f"   MCP Endpoint: http://{args.host}:{args.port}/mcp")
    print(f"   Health: http://{args.host}:{args.port}/health")
    print(f"   Tools: http://{args.host}:{args.port}/tools")
    
    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port)
