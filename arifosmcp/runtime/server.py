"""
arifosmcp/runtime/server.py — arifOS APEX-G MCP Hub

CANONICAL EXTERNAL ENTRYPOINT for the arifOS MCP surface.

Phase split:
  - Core constitutional stack (7 tools): the only tools used by the new
    constitutional kernel surface and deploy validation.
  - External capability tools (Phase 2 integration): legacy capability
    tools such as ACLIP sensors, reality search, evidence ingest.
    They stay enabled for compatibility.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os

from fastmcp import FastMCP
from starlette.staticfiles import StaticFiles

from arifosmcp.runtime.fastmcp_ext.transports import (
    _build_http_middleware,
    _normalize_path,
    run_server,
)
from arifosmcp.runtime.orchestrator import metabolic_loop
from arifosmcp.runtime.phase2_tools import register_phase2_tools
from arifosmcp.runtime.prompts import register_prompts
from arifosmcp.runtime.public_registry import release_version_label
from arifosmcp.runtime.resources import register_resources
from arifosmcp.runtime.rest_routes import register_rest_routes
from arifosmcp.runtime.tools import (
    audit_rules,
    check_vital,
    ingest_evidence,
    metabolic_loop_router,
    open_apex_dashboard,
    register_tools,
    search_reality,
    session_memory,
)

# ---------------------------------------------------------------------------
# Phase 1 — Canonical 7-Tool arifOS Stack
# ---------------------------------------------------------------------------

mcp = FastMCP("arifOS-APEX-G", version=release_version_label())
PUBLIC_TOOL_PROFILE = os.getenv("ARIFOS_PUBLIC_TOOL_PROFILE", "full").strip().lower() or "full"
VALID_TRANSPORT_MODES = {"stdio", "http", "sse", "streamable-http"}


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

CORE_TOOL_REGISTRY = {
    "arifOS.kernel": metabolic_loop_router,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "session_memory": session_memory,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
    "open_apex_dashboard": open_apex_dashboard,
}

register_rest_routes(mcp, CORE_TOOL_REGISTRY)


# ---------------------------------------------------------------------------
# Phase 2 — External Capability Tools (legacy-enabled, not in new loop)
# ---------------------------------------------------------------------------

if PUBLIC_TOOL_PROFILE not in ("chatgpt", "agnostic_public"):
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

# Mount APEX dashboard static files
_dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "apex-dashboard")
if os.path.isdir(_dashboard_dir):
    _mcp_app.mount("/dashboard", StaticFiles(directory=_dashboard_dir, html=True), name="dashboard")


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
