"""
arifOS MCP Server — Railway Production Entry Point

Starts the constitutional MCP server with all 9 tools on SSE transport.
Health endpoint at /health for Railway healthchecks.
Tool list at / for service discovery.

DITEMPA BUKAN DIBERI
"""

import os

import uvicorn
from starlette.responses import JSONResponse
from starlette.routing import Route

from fastmcp.server.http import create_sse_app

# Railway provides PORT and HOST via environment
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")

from aaa_mcp.server import mcp  # noqa: E402 — env must be set before import

async def health(_request):
    return JSONResponse({"status": "ok"})


# Build an SSE app and add an explicit /health endpoint for Railway.
app = create_sse_app(
    mcp,
    message_path="/messages",
    sse_path="/sse",
    routes=[Route("/health", endpoint=health, methods=["GET"])],
)

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
