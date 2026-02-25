"""
aaa_mcp/asgi.py — ASGI entrypoint for FastMCP HTTP hosting (Prefect Horizon, Railway, etc.)

Exports:
  - `app`: Starlette ASGI application with MCP mounted at `/mcp` and health at `/health`.

Notes:
  - Uses the existing unified registry in `aaa_mcp.server` (tools/resources/prompts/templates).
  - No stdout writes here (safe for stdio-based tooling).
"""

from __future__ import annotations

from datetime import datetime, timezone

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from arifos_aaa_mcp.server import create_aaa_mcp_server


async def health(_: Request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "healthy",
            "service": "arifOS",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


_mcp = create_aaa_mcp_server()
_mcp_app = _mcp.http_app(path="/")

app = Starlette(
    routes=[
        Route("/health", health, methods=["GET"]),
        Mount("/mcp", app=_mcp_app),
    ],
    lifespan=_mcp_app.lifespan,
)

__all__ = ["app"]
