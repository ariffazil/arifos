"""
arifOS MCP Server — Railway Production Entry Point

Starts the constitutional MCP server with all 13 tools on network transports.
Health endpoint at /health for Railway healthchecks.
Tool list at / for service discovery.
Monitoring at /metrics for Prometheus.

DITEMPA BUKAN DIBERI
"""

import sys

print("=== RAILWAY STARTUP: BEGIN ===", file=sys.stderr, flush=True)

import asyncio
import os

import uvicorn
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

# Railway provides PORT and HOST via environment
port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")
transport = os.environ.get("AAA_MCP_TRANSPORT", "sse").strip().lower()

print(
    f"=== RAILWAY STARTUP: CONFIG PORT={port} HOST={host} TRANSPORT={transport} ===",
    file=sys.stderr,
    flush=True,
)

try:
    print("=== RAILWAY STARTUP: IMPORTING MCP SERVER ===", file=sys.stderr, flush=True)
    from aaa_mcp.server import mcp  # noqa: E402 — env must be set before import

    print("=== RAILWAY STARTUP: IMPORT SUCCESS ===", file=sys.stderr, flush=True)
except Exception as e:
    print(f"=== RAILWAY STARTUP: CRITICAL IMPORT ERROR: {e} ===", file=sys.stderr, flush=True)
    import traceback

    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

# Try to import monitoring
try:
    from aaa_mcp.infrastructure.monitoring import (
        get_health_monitor,
        get_metrics_collector,
        startup_health_check,
    )

    MONITORING_AVAILABLE = True
except Exception as e:
    print(f"[WARN] Monitoring not available: {e}")
    MONITORING_AVAILABLE = False


async def health(request):
    """Health check endpoint for Railway."""
    # Always return 200 for Railway healthchecks - server is running
    # Internal component health is logged but doesn't block deployment
    return JSONResponse(
        {
            "status": "healthy",
            "service": "arifOS MCP Server",
            "version": "60.0-FORGE",
            "mcp_tools": 14,
        }
    )


async def root(request):
    """Root endpoint with service info."""
    return JSONResponse(
        {
            "service": "arifOS MCP Server",
            "version": "60.0-FORGE",
            "status": "operational",
            "endpoints": {
                "health": "/health",
                "metrics": "/metrics",
            },
            "repository": "https://github.com/ariffazil/arifOS",
            "documentation": "https://arifos.arif-fazil.com",
            "motto": "DITEMPA BUKAN DIBERI",
        }
    )


async def metrics(request):
    """Prometheus metrics endpoint."""
    if MONITORING_AVAILABLE:
        collector = get_metrics_collector()
        prometheus_data = collector.export_prometheus()
        return PlainTextResponse(prometheus_data)
    else:
        return PlainTextResponse("# Monitoring not available")


async def stats(request):
    """JSON stats endpoint."""
    if MONITORING_AVAILABLE:
        collector = get_metrics_collector()
        stats_data = collector.get_stats()
        return JSONResponse(
            {
                "service": "arifOS MCP",
                "stats": stats_data,
            }
        )
    else:
        return JSONResponse({"error": "Monitoring not available"})


# =============================================================================
# OAuth 2.1 Endpoints (MCP 2025-11-25 Authorization)
# https://modelcontextprotocol.io/specification/2025-11-25/server/authorization
# =============================================================================

OAUTH_ISSUER = os.environ.get("AAA_ISSUER", "https://aaamcp.arif-fazil.com")
OAUTH_AUTH_ENDPOINT = os.environ.get(
    "OAUTH_AUTHORIZATION_ENDPOINT", f"{OAUTH_ISSUER}/oauth/authorize"
)
OAUTH_TOKEN_ENDPOINT = os.environ.get("OAUTH_TOKEN_ENDPOINT", f"{OAUTH_ISSUER}/oauth/token")


async def oauth_authorization_server(request):
    """OAuth 2.1 Authorization Server Metadata (RFC 8414)."""
    return JSONResponse(
        {
            "issuer": OAUTH_ISSUER,
            "authorization_endpoint": OAUTH_AUTH_ENDPOINT,
            "token_endpoint": OAUTH_TOKEN_ENDPOINT,
            "registration_endpoint": f"{OAUTH_ISSUER}/oauth/register",
            "scopes_supported": ["mcp:read", "mcp:execute", "aaa:audit"],
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token", "client_credentials"],
            "code_challenge_methods_supported": ["S256"],
            "token_endpoint_auth_methods_supported": ["client_secret_basic", "client_secret_post"],
            "revocation_endpoint": f"{OAUTH_ISSUER}/oauth/revoke",
            "introspection_endpoint": f"{OAUTH_ISSUER}/oauth/introspect",
        }
    )


async def oauth_protected_resource(request):
    """OAuth 2.1 Protected Resource Metadata."""
    return JSONResponse(
        {
            "resource": OAUTH_ISSUER,
            "authorization_servers": [OAUTH_ISSUER],
            "scopes_supported": ["mcp:read", "mcp:execute", "aaa:audit"],
            "bearer_methods_supported": ["header"],
        }
    )


async def oauth_authorize(request):
    """OAuth 2.1 Authorization Endpoint (stub - requires full OAuth implementation)."""
    # This is a placeholder - full OAuth 2.1 implementation requires:
    # - User authentication/ consent
    # - Authorization code generation
    # - PKCE validation
    # - Client validation
    return JSONResponse(
        {
            "error": "not_implemented",
            "error_description": "OAuth 2.1 authorization endpoint requires external IdP integration",
            "hint": "Configure AAA_ISSUER to point to your OAuth provider (e.g., Auth0, Keycloak)",
        },
        status_code=501,
    )


async def oauth_token(request):
    """OAuth 2.1 Token Endpoint (stub - requires full OAuth implementation)."""
    # This is a placeholder - full OAuth 2.1 implementation requires:
    # - Authorization code exchange
    # - Client authentication
    # - Token generation (JWT)
    # - Refresh token handling
    return JSONResponse(
        {
            "error": "not_implemented",
            "error_description": "OAuth 2.1 token endpoint requires external IdP integration",
            "hint": "Configure AAA_ISSUER to point to your OAuth provider (e.g., Auth0, Keycloak)",
        },
        status_code=501,
    )


# Setup routes
routes = [
    Route("/", endpoint=root, methods=["GET"]),
    Route("/health", endpoint=health, methods=["GET"]),
    Route("/metrics", endpoint=metrics, methods=["GET"]),
    Route("/stats", endpoint=stats, methods=["GET"]),
    # OAuth 2.1 endpoints (MCP 2025-11-25)
    Route(
        "/.well-known/oauth-authorization-server",
        endpoint=oauth_authorization_server,
        methods=["GET"],
    ),
    Route(
        "/.well-known/oauth-protected-resource", endpoint=oauth_protected_resource, methods=["GET"]
    ),
    Route("/oauth/authorize", endpoint=oauth_authorize, methods=["GET", "POST"]),
    Route("/oauth/token", endpoint=oauth_token, methods=["POST"]),
]

# Build the transport app based on FastMCP version
try:
    # Try FastMCP 2.0+ style
    from fastmcp.server.http import create_sse_app, create_streamable_http_app

    if transport in {"http", "streamable-http", "mcp"}:
        app = create_streamable_http_app(
            mcp,
            streamable_http_path="/mcp",
            routes=routes,
        )
    else:
        app = create_sse_app(
            mcp,
            message_path="/messages/",
            sse_path="/sse",
            routes=routes,
        )
except ImportError:
    # Fallback to FastMCP 1.0 style
    from fastmcp.server import SseServerTransport
    from starlette.applications import Starlette

    sse_transport = SseServerTransport("/messages/")

    async def sse_endpoint(request):
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp.run(streams[0], streams[1], mcp.create_initialization_options())

    starlette_routes = [
        Route("/", endpoint=root, methods=["GET"]),
        Route("/health", endpoint=health, methods=["GET"]),
        Route("/metrics", endpoint=metrics, methods=["GET"]),
        Route("/stats", endpoint=stats, methods=["GET"]),
        # OAuth 2.1 endpoints (MCP 2025-11-25)
        Route(
            "/.well-known/oauth-authorization-server",
            endpoint=oauth_authorization_server,
            methods=["GET"],
        ),
        Route(
            "/.well-known/oauth-protected-resource",
            endpoint=oauth_protected_resource,
            methods=["GET"],
        ),
        Route("/oauth/authorize", endpoint=oauth_authorize, methods=["GET", "POST"]),
        Route("/oauth/token", endpoint=oauth_token, methods=["POST"]),
        Route("/sse", endpoint=sse_endpoint),
    ]

    app = Starlette(routes=starlette_routes)

# Disable redirect_slashes to prevent 307 redirects
app.router.redirect_slashes = False


async def startup():
    """Startup tasks."""
    print("=" * 60)
    print("arifOS MCP Server Starting")
    print("=" * 60)
    print(f"Transport: {transport}")
    print(f"Host: {host}:{port}")
    print(f"Monitoring: {'Available' if MONITORING_AVAILABLE else 'Basic'}")
    print()

    if MONITORING_AVAILABLE:
        print("Running startup health checks...")
        try:
            startup_status = await startup_health_check()
            print(f"Status: {startup_status['status']}")
            for check_name, check_result in startup_status["checks"].items():
                status = check_result.get("status", "unknown")
                symbol = "[OK]" if status == "healthy" else "[WARN]"
                print(f"  {symbol} {check_name}: {status}")
        except Exception as e:
            print(f"[WARN] Health check error: {e}")

    print()
    print("=" * 60)
    print("DITEMPA BUKAN DIBERI - Forged, Not Given")
    print("=" * 60)
    print()


if __name__ == "__main__":
    # Run startup check
    asyncio.run(startup())

    # Start server
    uvicorn.run(app, host=host, port=port)
