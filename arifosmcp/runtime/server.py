"""
arifosmcp/runtime/server.py — arifOS APEX-G MCP Hub

CANONICAL EXTERNAL ENTRYPOINT for the arifOS MCP surface.

Phase split:
  - Core constitutional stack (8 tools): the only tools used by the new
    constitutional kernel surface and deploy validation.
  - External capability tools (Phase 2 integration): legacy capability
    tools such as ACLIP sensors, reality search, evidence ingest.
    They stay enabled for compatibility.

Transport note:
  SSE transport was deprecated by the MCP spec (March 2025) and removed from
  Microsoft Copilot Studio support (August 2025). This server uses Streamable
  HTTP only via FastMCP http_app() with stateless_http=True.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os

from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from arifosmcp.runtime.fastmcp_ext.transports import (
    _build_http_middleware,
    _normalize_path,
    run_server,
)
from arifosmcp.runtime.orchestrator import metabolic_loop
from arifosmcp.runtime.phase2_tools import register_phase2_tools
from arifosmcp.runtime.prompts import register_prompts
from arifosmcp.runtime.public_registry import (
    is_public_profile,
    normalize_tool_profile,
    release_version_label,
)
from arifosmcp.runtime.resources import register_resources
from arifosmcp.runtime.rest_routes import register_rest_routes
from arifosmcp.runtime.tools import (
    audit_rules,
    check_vital,
    ingest_evidence,
    init_anchor_state,
    metabolic_loop_router,
    open_apex_dashboard,
    reality_atlas,
    reality_compass,
    register_tools,
    search_reality,
    session_memory,
    verify_vault_ledger,
)
from core.shared.manifest_loader import sync_runtime_floors

# ---------------------------------------------------------------------------
# Phase 1 — Canonical 7-Tool arifOS Stack
# ---------------------------------------------------------------------------

mcp = FastMCP("arifOS-APEX-G", version=release_version_label())
PUBLIC_TOOL_PROFILE = normalize_tool_profile(os.getenv("ARIFOS_PUBLIC_TOOL_PROFILE", "public"))
# SSE removed: deprecated by MCP spec (2025-03) and Copilot Studio (2025-08)
VALID_TRANSPORT_MODES = {"stdio", "http", "streamable-http"}

# ---------------------------------------------------------------------------
# Optional API key guard — activated when COPILOT_API_KEY is set in env.
# In Copilot Studio wizard: Authentication → API Key → Header → X-API-Key
# Leave COPILOT_API_KEY unset (or empty) to disable auth (development mode).
# ---------------------------------------------------------------------------
_COPILOT_API_KEY = os.getenv("COPILOT_API_KEY", "").strip()


class _APIKeyMiddleware(BaseHTTPMiddleware):
    """Optional API key guard for Copilot Studio and external MCP clients.

    Bypassed when COPILOT_API_KEY env var is not set, preserving
    zero-config development experience.
    """

    async def dispatch(self, request, call_next):  # type: ignore[override]
        if _COPILOT_API_KEY:
            incoming = request.headers.get("X-API-Key", "")
            if incoming != _COPILOT_API_KEY:
                return JSONResponse(
                    {"error": "Unauthorized", "hint": "Provide a valid X-API-Key header."},
                    status_code=401,
                )
        return await call_next(request)


def _validate_transport_mode(mode: str) -> str:
    normalized = mode.strip().lower()
    if normalized not in VALID_TRANSPORT_MODES:
        raise ValueError(
            f"Invalid AAA_MCP_TRANSPORT '{mode}'. Allowed: {sorted(VALID_TRANSPORT_MODES)}"
        )
    return normalized


def _parse_port(raw_port: str) -> int:
    port = int(raw_port)
    if port < 1024 or port > 65535:
        raise ValueError(f"PORT out of range (1024-65535): {port}")
    return port


register_tools(mcp, profile=PUBLIC_TOOL_PROFILE)
register_resources(mcp)
register_prompts(mcp)

# Sync Mind to Body (Dynamic Connection)
sync_runtime_floors()

CORE_TOOL_REGISTRY = {
    "arifOS_kernel": metabolic_loop_router,
    "arifOS-kernel": metabolic_loop_router,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "session_memory": session_memory,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
    "reality_compass": reality_compass,
    "reality_atlas": reality_atlas,
    "open_apex_dashboard": open_apex_dashboard,
    "init_anchor_state": init_anchor_state,
    "verify_vault_ledger": verify_vault_ledger,
}

register_rest_routes(mcp, CORE_TOOL_REGISTRY)


# ---------------------------------------------------------------------------
# Phase 2 — External Capability Tools (legacy-enabled, not in new loop)
# ---------------------------------------------------------------------------

if not is_public_profile(PUBLIC_TOOL_PROFILE):
    register_phase2_tools(mcp, profile=PUBLIC_TOOL_PROFILE)


# ---------------------------------------------------------------------------
# ASGI export for uvicorn/platform HTTP deployment
# ---------------------------------------------------------------------------

HTTP_PATH = _normalize_path(os.getenv("ARIFOS_MCP_PATH"), "/mcp")
# Enable stateless HTTP + JSON responses for agnostic/remote MCP compatibility.
_mcp_app = mcp.http_app(
    path=HTTP_PATH,
    json_response=True,
    middleware=_build_http_middleware(),
    stateless_http=True,
)

app = _mcp_app

# API key guard (no-op when COPILOT_API_KEY is unset)
app.add_middleware(_APIKeyMiddleware)

# Enable CORS for all origins (required for cross-site health/telemetry monitoring)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount APEX dashboard static files
_dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "apex-dashboard")
if os.path.isdir(_dashboard_dir):
    _mcp_app.mount("/dashboard", StaticFiles(directory=_dashboard_dir, html=True), name="dashboard")

# Mount H1 Developer Portal
_developer_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "developer")
if os.path.isdir(_developer_dir):
    _mcp_app.mount("/developer", StaticFiles(directory=_developer_dir, html=True), name="developer")


def create_aaa_mcp_server() -> FastMCP:
    """Return the fully configured arifOS MCP hub."""
    return mcp


__all__ = [
    "HTTP_PATH",
    "app",
    "audit_rules",
    "check_vital",
    "create_aaa_mcp_server",
    "ingest_evidence",
    "mcp",
    "metabolic_loop",
    "metabolic_loop_router",
    "open_apex_dashboard",
    "PUBLIC_TOOL_PROFILE",
    "register_tools",
    "search_reality",
    "session_memory",
]


if __name__ == "__main__":
    mode = _validate_transport_mode(os.getenv("AAA_MCP_TRANSPORT", "stdio"))
    host = os.getenv("HOST", "0.0.0.0")
    port = _parse_port(os.getenv("PORT", "8080"))
    run_server(mcp, mode=mode, host=host, port=port)
