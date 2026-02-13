"""
arifOS MCP Server — Railway Production Entry Point (v61.0-FORGE)

Starts the constitutional MCP server with SSE transport.
Health endpoint at /health for Railway healthchecks.

DITEMPA BUKAN DIBERI
"""

import sys

print("=== RAILWAY STARTUP: BEGIN ===", file=sys.stderr, flush=True)

import asyncio
import os

# Environment setup first
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")

print(f"[startup] Port: {port}, Host: {host}", file=sys.stderr, flush=True)

# Import dependencies
try:
    import uvicorn
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route, Mount
    from mcp.server.sse import SseServerTransport
    print("[startup] Dependencies imported successfully", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[startup] ERROR importing dependencies: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

# Import the MCP server instance
try:
    from aaa_mcp.server import mcp as mcp_server
    from aaa_mcp import __version__
    print(f"[startup] MCP server imported: {__version__}", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[startup] ERROR importing MCP server: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)


# Health and root endpoints
async def health(request):
    """Health check endpoint for Railway."""
    try:
        tools = await mcp_server.get_tools()
        tool_count = len(tools)
    except Exception as e:
        print(f"[health] Error counting tools: {e}", file=sys.stderr, flush=True)
        tool_count = 5  # Fallback
    
    return JSONResponse({
        "status": "ok",
        "version": __version__,
        "mcp_tools": tool_count
    })


async def root(request):
    return JSONResponse({
        "service": "arifOS MCP Server",
        "version": __version__,
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "sse": "/sse",
            "messages": "/messages"
        },
    })


# Create SSE transport
sse = SseServerTransport("/messages")


async def sse_endpoint(request):
    """SSE endpoint for MCP clients using FastMCP's native SSE support."""
    print("[sse] Connection initiated", file=sys.stderr, flush=True)
    try:
        # Use FastMCP's built-in SSE handling
        # The correct pattern for FastMCP v2+ is to use the sse_response context manager
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            print("[sse] Streams connected, starting MCP server", file=sys.stderr, flush=True)
            
            # Get the underlying MCP server and run it with the streams
            # FastMCP stores the server in _mcp_server attribute
            if hasattr(mcp_server, '_mcp_server') and mcp_server._mcp_server is not None:
                server = mcp_server._mcp_server
                # Run the server with the streams
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options(),
                )
            else:
                # Fallback: use FastMCP's run method directly if available
                print("[sse] Using FastMCP direct run", file=sys.stderr, flush=True)
                await mcp_server.run(
                    read_stream,
                    write_stream,
                    mcp_server.create_initialization_options(),
                )
            
            print("[sse] Server run completed", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[sse] ERROR: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise


async def messages_endpoint(request):
    """Handle JSON-RPC POST messages for MCP tools."""
    print("[messages] POST received", file=sys.stderr, flush=True)
    try:
        await sse.handle_post_message(
            request.scope,
            request.receive,
            request._send,
        )
        print("[messages] Handled successfully", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[messages] ERROR: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise


# Create Starlette app with routes
routes = [
    Route("/", root, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
    Route("/sse", sse_endpoint, methods=["GET"]),
    Route("/messages", messages_endpoint, methods=["POST"]),
]

app = Starlette(
    routes=routes,
    debug=False,
)


async def startup():
    """Startup tasks."""
    print("=" * 60, file=sys.stderr, flush=True)
    print("arifOS MCP Server Starting", file=sys.stderr, flush=True)
    print("=" * 60, file=sys.stderr, flush=True)
    print(f"Version: {__version__}", file=sys.stderr, flush=True)
    print(f"Host: {host}:{port}", file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)
    print("DITEMPA BUKAN DIBERI - Forged, Not Given", file=sys.stderr, flush=True)
    print("=" * 60, file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)


if __name__ == "__main__":
    # Run startup check
    asyncio.run(startup())
    
    # Start server
    print(f"[startup] Starting uvicorn on {host}:{port}", file=sys.stderr, flush=True)
    uvicorn.run(app, host=host, port=port, log_level="info")
