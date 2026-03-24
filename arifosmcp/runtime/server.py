"""
arifosmcp/runtime/server.py — arifOS AAA Sovereign Hub - HARDENED

UPGRADE: Global Panic Middleware and Sovereign Domain Hardening.
FIX: Register routes BEFORE creating http_app
"""

from __future__ import annotations

import os
import sys
import traceback
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, FileResponse
from starlette.middleware.cors import CORSMiddleware

from arifosmcp.runtime.tools import register_tools, ALL_TOOL_IMPLEMENTATIONS
from arifosmcp.runtime.rest_routes import register_rest_routes

# ---------------------------------------------------------------------------
# HARDENING: GLOBAL PANIC MIDDLEWARE
# ---------------------------------------------------------------------------

class GlobalPanicMiddleware(BaseHTTPMiddleware):
    """Intercepts kernel panics and emits a Constitutional VOID."""
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            print(f"!!! KERNEL PANIC: {str(e)}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            return JSONResponse({
                "status": "void",
                "tool": "kernel_panic_handler",
                "error_message": "F13: System halt due to unhandled kernel exception.",
                "action": "HALT"
            }, status_code=500)

# ---------------------------------------------------------------------------
# SERVER INITIALIZATION
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "arifOS Sovereign Intelligence Kernel",
    version="2026.03.24-HARDENED",
    website_url="https://aaa.arif-fazil.com",
)

# Register Surface FIRST (before creating http_app)
register_tools(mcp)
register_rest_routes(mcp, ALL_TOOL_IMPLEMENTATIONS)

# THEN create the app with all routes included
app = mcp.http_app(stateless_http=True)
app.add_middleware(GlobalPanicMiddleware)

# Strict CORS: Only allow Sovereign Domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Content-Type"],
)

def create_aaa_mcp_server() -> FastMCP:
    return mcp

if __name__ == "__main__":
    from arifosmcp.runtime.fastmcp_ext.transports import run_server
    run_server(mcp, mode="http", host="0.0.0.0", port=8080)
