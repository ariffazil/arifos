"""
arifOS MCP Server — Railway Production Entry Point (v60.0-FORGE)

Starts the constitutional MCP server with SSE transport.
Health endpoint at /health for Railway healthchecks.

DITEMPA BUKAN DIBERI
"""

import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from mcp.server.sse import SseServerTransport
from mcp.server import Server
import uvicorn

# Environment
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")

# Import the MCP server instance
from aaa_mcp.server import mcp as mcp_server

# Health and root endpoints
async def health(request):
    return JSONResponse({
        "status": "ok",
        "version": "60.0.0-FORGE",
        "mcp_tools": 10
    })

async def root(request):
    return JSONResponse({
        "service": "arifOS MCP Server",
        "version": "60.0.0-FORGE",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "sse": "/sse",
            "messages": "/messages"
        },
        "repository": "https://github.com/ariffazil/arifOS",
        "documentation": "https://arifos.arif-fazil.com",
        "motto": "DITEMPA BUKAN DIBERI"
    })

# Create SSE transport
sse = SseServerTransport("/messages")

# Handler for SSE connections (FastMCP v2+ API)
async def sse_endpoint(request):
    """SSE endpoint for MCP clients.

    Uses SseServerTransport.connect_sse, which wraps the underlying
    MCP server with a streaming transport. This replaces the older
    connect_session() API.
    """
    return await sse.connect_sse(
        request.scope,
        request.receive,
        request.send,
        mcp_server._mcp_server,
    )

# Handler for POST messages
async def messages_endpoint(request):
    return await sse.handle_post_message(request.scope, request.receive, request.send)

# Create Starlette app with routes
app = Starlette(
    routes=[
        Route("/", root, methods=["GET"]),
        Route("/health", health, methods=["GET"]),
        Route("/sse", sse_endpoint, methods=["GET"]),
        Route("/messages", messages_endpoint, methods=["POST"]),
    ],
    debug=False
)

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
