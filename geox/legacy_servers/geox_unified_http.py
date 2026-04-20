"""
GEOX Dimension-Native MCP Server — HTTP Transport Wrapper
═══════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI

Wraps the unified MCP server with HTTP/SSE transport for web integration.
"""

from __future__ import annotations

import os
import sys
import logging
from datetime import datetime, timezone

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from mcp.server.sse import SseServerTransport

# Import the unified server MCP instance
from geox_unified_mcp_server import mcp, GEOX_PROFILE, ENABLED_DIMENSIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geox.http")

GEOX_VERSION = "v2026.04.11-DIMENSION-NATIVE"
GEOX_SEAL = "DITEMPA BUKAN DIBERI"


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

async def health_handler(request):
    """Health check endpoint for Docker/Traefik."""
    return JSONResponse({
        "status": "healthy",
        "service": "geox-dimension-native",
        "version": GEOX_VERSION,
        "seal": GEOX_SEAL,
        "profile": GEOX_PROFILE,
        "enabled_dimensions": ENABLED_DIMENSIONS,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


async def profile_handler(request):
    """Return current profile and dimension status."""
    return JSONResponse({
        "profile": GEOX_PROFILE,
        "enabled_dimensions": ENABLED_DIMENSIONS,
        "version": GEOX_VERSION,
        "seal": GEOX_SEAL
    })


# ═══════════════════════════════════════════════════════════════════════════════
# SSE TRANSPORT SETUP
# ═══════════════════════════════════════════════════════════════════════════════

sse = SseServerTransport("/mcp/")


async def sse_handler(request):
    """SSE endpoint for MCP clients."""
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# STARLETTE APP
# ═══════════════════════════════════════════════════════════════════════════════

routes = [
    Route("/health", health_handler),
    Route("/profile", profile_handler),
    Route("/mcp/", endpoint=sse_handler),
]

app = Starlette(
    debug=os.getenv("GEOX_DEBUG", "false").lower() == "true",
    routes=routes,
)

# CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import uvicorn
    
    host = os.getenv("GEOX_HOST", "0.0.0.0")
    port = int(os.getenv("GEOX_PORT", "8000"))
    
    logger.info(f"Starting GEOX Dimension-Native HTTP Server")
    logger.info(f"  Version: {GEOX_VERSION}")
    logger.info(f"  Profile: {GEOX_PROFILE}")
    logger.info(f"  Dimensions: {', '.join(ENABLED_DIMENSIONS)}")
    logger.info(f"  Host: {host}:{port}")
    logger.info(f"  Seal: {GEOX_SEAL}")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
