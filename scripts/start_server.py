"""
arifOS MCP Server — Railway Production Entry Point (v61.0-FORGE)

Starts the constitutional MCP server with SSE transport.
Uses FastMCP's native mounting for proper tool registration.

DITEMPA BUKAN DIBERI
"""

import sys

print("=== RAILWAY STARTUP: BEGIN ===", file=sys.stderr, flush=True)

import asyncio
import os

# Environment setup
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")

print(f"[startup] Port: {port}, Host: {host}", file=sys.stderr, flush=True)

# Import dependencies
try:
    import uvicorn
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    print("[startup] Dependencies imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[startup] ERROR: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

# Import MCP server - this triggers tool registration
try:
    # Import server module first (registers all tools)
    from aaa_mcp import server as mcp_module
    from aaa_mcp.server import mcp as mcp_server
    from aaa_mcp import __version__
    
    print(f"[startup] MCP v{__version__} loaded", file=sys.stderr, flush=True)
    
except Exception as e:
    print(f"[startup] ERROR importing MCP: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)


# Health endpoint
async def health(request):
    """Health check endpoint for Railway."""
    try:
        tools = await mcp_server.get_tools()
        tool_count = len(tools)
        tool_names = list(tools.keys())
    except Exception as e:
        print(f"[health] Error: {e}", file=sys.stderr, flush=True)
        tool_count = 0
        tool_names = []
    
    return JSONResponse({
        "status": "ok",
        "version": __version__,
        "mcp_tools": tool_count,
        "tool_names": tool_names,
    })


async def root(request):
    """Root endpoint with server info."""
    return JSONResponse({
        "service": "arifOS MCP Server",
        "version": __version__,
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "mcp_sse": "/mcp/sse",
        },
    })


async def startup():
    """Startup tasks."""
    print("=" * 60, file=sys.stderr, flush=True)
    print("arifOS MCP Server Starting", file=sys.stderr, flush=True)
    print("=" * 60, file=sys.stderr, flush=True)
    print(f"Version: {__version__}", file=sys.stderr, flush=True)
    print(f"Host: {host}:{port}", file=sys.stderr, flush=True)
    
    # Verify tool registration
    try:
        tools = await mcp_server.get_tools()
        print(f"[startup] Tools: {list(tools.keys())}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[startup] WARNING: {e}", file=sys.stderr, flush=True)
    
    print(file=sys.stderr, flush=True)
    print("DITEMPA BUKAN DIBERI - Forged, Not Given", file=sys.stderr, flush=True)
    print("=" * 60, file=sys.stderr, flush=True)


# Create the Starlette app
# FastMCP v2+ uses a different pattern - let it handle its own mounting
try:
    # Try to get the underlying server and create SSE endpoint manually
    # This is the most reliable method for FastMCP 2.x
    from mcp.server.sse import SseServerTransport
    
    sse = SseServerTransport("/messages")
    
    async def sse_endpoint(request):
        """SSE endpoint for MCP clients."""
        print("[sse] Connection initiated", file=sys.stderr, flush=True)
        try:
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as (read_stream, write_stream):
                print("[sse] Streams connected", file=sys.stderr, flush=True)
                
                # Get the LowLevelServer from FastMCP
                server = mcp_server._mcp_server
                if server is None:
                    raise RuntimeError("MCP server not initialized")
                
                # Run the server
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options(),
                )
                print("[sse] Server run completed", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"[sse] ERROR: {e}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    
    async def messages_endpoint(request):
        """Handle POST messages."""
        print("[messages] POST received", file=sys.stderr, flush=True)
        try:
            await sse.handle_post_message(
                request.scope, request.receive, request._send
            )
            print("[messages] Handled successfully", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"[messages] ERROR: {e}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    
    # Create app with all routes
    routes = [
        Route("/", root, methods=["GET"]),
        Route("/health", health, methods=["GET"]),
        Route("/sse", sse_endpoint, methods=["GET"]),
        Route("/messages", messages_endpoint, methods=["POST"]),
    ]
    
    app = Starlette(routes=routes, debug=False)
    print("[startup] Starlette app created with custom SSE routes", file=sys.stderr, flush=True)
    
except Exception as e:
    print(f"[startup] ERROR creating app: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    asyncio.run(startup())
    print(f"[startup] Starting uvicorn on {host}:{port}", file=sys.stderr, flush=True)
    uvicorn.run(app, host=host, port=port, log_level="info")
