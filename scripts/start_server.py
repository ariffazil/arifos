"""
arifOS MCP Server — Railway Production Entry Point

Starts the constitutional MCP server with all 10 tools on network transports.
Health endpoint at /health for Railway healthchecks.
Tool list at / for service discovery.

DITEMPA BUKAN DIBERI
"""

import os

import uvicorn
from starlette.responses import JSONResponse
from starlette.routing import Route

from fastmcp.server.http import create_sse_app, create_streamable_http_app

# Railway provides PORT and HOST via environment
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")
transport = os.environ.get("AAA_MCP_TRANSPORT", "sse").strip().lower()

from aaa_mcp.server import mcp  # noqa: E402 — env must be set before import

async def health(_request):
    return JSONResponse({"status": "ok"})


# Build the transport app and add an explicit /health endpoint for Railway.
if transport in {"http", "streamable-http", "mcp"}:
    app = create_streamable_http_app(
        mcp,
        streamable_http_path="/mcp",
        routes=[Route("/health", endpoint=health, methods=["GET"])],
    )
else:
    app = create_sse_app(
        mcp,
        message_path="/messages",
        sse_path="/sse",
        routes=[Route("/health", endpoint=health, methods=["GET"])],
    )

# Disable redirect_slashes to prevent 307 redirects on POST /messages
# This fixes the SSE transport issue where clients POST to /messages?session_id=xxx
# but Starlette redirects to /messages/?session_id=xxx with 307
app.router.redirect_slashes = False

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
