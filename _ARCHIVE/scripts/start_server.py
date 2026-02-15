"""
arifOS MCP Server — Railway Production Entry Point (v64.1-GAGI)

Starts the constitutional MCP server with SSE transport.
Uses FastMCP's native mounting for proper tool registration.

v64.1 GAGI Features:
- Uncertainty Engine: 5-dim vector with harmonic/geometric mean
- Governance Kernel: Synchronous AWAITING_888 (conditional)
- Telemetry: 30-day locked adaptation
- Irreversibility Index: impact × recovery × time

DITEMPA BUKAN DIBERI
"""

import os

# 🔥 CRITICAL FIX: Force local source priority over site-packages
# Prevents Docker from loading old installed package instead of fresh source
import sys

sys.path.insert(0, os.getcwd())
print(f"[startup] sys.path[0] = {sys.path[0]}", file=sys.stderr, flush=True)

print("=== RAILWAY STARTUP: BEGIN ===", file=sys.stderr, flush=True)

import asyncio
import os

# Environment setup
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")

print(f"[startup] Port: {port}, Host: {host}", file=sys.stderr, flush=True)

# Import dependencies
try:
    import inspect  # For module path verification

    import uvicorn
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse, Response
    from starlette.routing import Route

    print("[startup] Dependencies imported", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[startup] ERROR: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

# Import MCP server - this triggers tool registration
try:
    # Import server module first (registers all tools)
    from aaa_mcp import __version__
    from aaa_mcp import server as mcp_module
    from aaa_mcp.server import mcp as mcp_server

    print(f"[startup] MCP v{__version__} loaded", file=sys.stderr, flush=True)

    # =============================================================================
    # ACLIP-CAI INTEGRATION (Sensory Tools C0-C9)
    # =============================================================================
    try:
        from aclip_cai.server import chroma_query as _chroma_query
        from aclip_cai.server import config_flags as _config_flags
        from aclip_cai.server import cost_estimator as _cost_estimator
        from aclip_cai.server import financial_cost as _financial_cost
        from aclip_cai.server import forge_guard as _forge_guard
        from aclip_cai.server import fs_inspect as _fs_inspect
        from aclip_cai.server import log_tail as _log_tail
        from aclip_cai.server import net_status as _net_status
        from aclip_cai.server import system_health as _system_health

        print(
            "[startup] ACLIP-CAI module loaded, registering tools...", file=sys.stderr, flush=True
        )

        @mcp_server.tool(
            name="aclip_system_health", description="[C0] System Health - CPU/RAM/Processes"
        )
        async def aclip_system_health(
            mode: str = "full", filter_process: str = "", top_n: int = 15
        ) -> dict:
            return await _system_health(mode, filter_process, top_n)

        @mcp_server.tool(
            name="aclip_fs_inspect", description="[C2] Filesystem Inspector - Read-only"
        )
        async def aclip_fs_inspect(
            path: str = ".", depth: int = 1, include_hidden: bool = False
        ) -> dict:
            return await _fs_inspect(path, depth, include_hidden)

        @mcp_server.tool(name="aclip_log_tail", description="[C3] Log Tail - View recent logs")
        async def aclip_log_tail(
            log_file: str = "aaa_mcp.log", lines: int = 50, pattern: str = ""
        ) -> dict:
            return await _log_tail(log_file, lines, pattern)

        @mcp_server.tool(name="aclip_net_status", description="[C4] Network Status - Ports/Conns")
        async def aclip_net_status(
            check_ports: bool = True, check_connections: bool = True
        ) -> dict:
            return await _net_status(check_ports, check_connections)

        @mcp_server.tool(name="aclip_config_flags", description="[C5] Config Flags - Env check")
        async def aclip_config_flags() -> dict:
            return await _config_flags()

        @mcp_server.tool(name="aclip_chroma_query", description="[C6] Chroma Query - Vector DB")
        async def aclip_chroma_query(
            query: str, collection: str = "default", top_k: int = 5, list_only: bool = False
        ) -> dict:
            return await _chroma_query(query, collection, top_k, list_only)

        @mcp_server.tool(
            name="aclip_cost_estimator", description="[C7] Cost Estimator - Thermodynamic"
        )
        async def aclip_cost_estimator(
            action_description: str,
            estimated_cpu_percent: float = 0,
            estimated_ram_mb: float = 0,
            estimated_io_mb: float = 0,
        ) -> dict:
            return await _cost_estimator(
                action_description, estimated_cpu_percent, estimated_ram_mb, estimated_io_mb
            )

        @mcp_server.tool(name="aclip_financial_cost", description="[C9] Financial Cost - Monetary")
        async def aclip_financial_cost(
            service: str, action: str, resource_id: str = "", period_days: int = 1
        ) -> dict:
            return await _financial_cost(service, action, resource_id, period_days)

        @mcp_server.tool(name="aclip_forge_guard", description="[C8] Forge Guard - Circuit Breaker")
        async def aclip_forge_guard(
            check_system_health: bool = True,
            cost_score_threshold: float = 0.8,
            cost_score_to_check: float = 0.0,
        ) -> dict:
            return await _forge_guard(
                check_system_health, cost_score_threshold, cost_score_to_check
            )

        print("[startup] ACLIP-CAI tools registered (C0-C9)", file=sys.stderr, flush=True)

    except ImportError:
        print(
            "[startup] ACLIP-CAI module not found. Skipping sensory tools.",
            file=sys.stderr,
            flush=True,
        )

except Exception as e:
    print(f"[startup] ERROR importing MCP: {e}", file=sys.stderr, flush=True)
    import traceback

    traceback.print_exc(file=sys.stderr)
    sys.exit(1)


# Health endpoint
async def health(request):
    """Health check endpoint for Railway with full truth probe."""
    try:
        tools = await mcp_server.get_tools()
        tool_count = len(tools)
        tool_names = list(tools.keys())
    except Exception as e:
        print(f"[health] Error: {e}", file=sys.stderr, flush=True)
        tool_count = 0
        tool_names = []

    # v64.1: TRUTH PROBE — Full version diagnostics
    import subprocess
    from importlib.metadata import version as pkg_version

    # 1. Package version (from pyproject.toml metadata)
    try:
        arifos_pkg_version = pkg_version("arifos")
    except:
        arifos_pkg_version = "unknown"

    # 2. Runtime version (from aaa_mcp.__version__)
    runtime_version = __version__

    # 3. Git SHA
    try:
        git_sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=5
        ).stdout.strip()
    except:
        git_sha = "unknown"

    # 4. Module path (where aaa_mcp is actually loaded from)
    module_path = inspect.getfile(mcp_module)

    # 5. sys.path[0] (local source priority verification)
    sys_path_0 = sys.path[0] if sys.path else "empty"

    # Version consistency check
    versions_match = arifos_pkg_version == runtime_version

    return JSONResponse(
        {
            "status": "ok" if versions_match else "version_mismatch",
            "versions": {
                "package": arifos_pkg_version,  # From pyproject.toml
                "runtime": runtime_version,  # From aaa_mcp.__version__
                "match": versions_match,
            },
            "git_sha": git_sha,
            "runtime_id": os.environ.get("RAILWAY_REPLICA_ID", "local"),
            "module_path": module_path,  # Physical file location
            "sys_path_0": sys_path_0,  # Python path priority
            "mcp_tools": tool_count,
            "tool_names": tool_names,
        }
    )


async def root(request):
    """Root endpoint with server info."""
    return JSONResponse(
        {
            "service": "arifOS MCP Server",
            "version": __version__,
            "status": "operational",
            "endpoints": {
                "health": "/health",
                "mcp_sse": "/sse",
                "mcp_messages": "/messages",
            },
        }
    )


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
        from starlette.responses import Response

        print("[sse] Connection initiated", file=sys.stderr, flush=True)
        try:
            async with sse.connect_sse(request.scope, request.receive, request._send) as (
                read_stream,
                write_stream,
            ):
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

            # Return empty response - SSE handled by transport
            return Response(status_code=200)

        except Exception as e:
            print(f"[sse] ERROR: {e}", file=sys.stderr, flush=True)
            import traceback

            traceback.print_exc(file=sys.stderr)
            raise

    async def messages_endpoint(request):
        """Handle POST messages."""
        print("[messages] POST received", file=sys.stderr, flush=True)
        try:
            await sse.handle_post_message(request.scope, request.receive, request._send)
            print("[messages] Handled successfully", file=sys.stderr, flush=True)
            from starlette.responses import Response

            return Response(status_code=202)  # ✅ F4 COMPLIANT
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
    print(f"[startup] Starting uvicorn on {host}:{port}", file=sys.stderr, flush=True)
    uvicorn.run(app, host=host, port=port, log_level="info")
