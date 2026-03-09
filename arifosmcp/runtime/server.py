"""
arifosmcp/runtime/server.py — arifOS APEX-G MCP Hub

CANONICAL EXTERNAL ENTRYPOINT for the arifOS MCP surface.

Phase split:
  - Core constitutional stack (10 tools): the only tools used by the new
    APEX-G metabolic loop and deploy validation.
  - External capability tools (Phase 2 integration): legacy capability
    tools such as ACLIP sensors, reality search, evidence ingest, and the
    old metabolic loop. They stay enabled for compatibility, but are not
    wired into the new orchestrated path.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os

from fastmcp import FastMCP
from starlette.staticfiles import StaticFiles

from arifosmcp.runtime.fastmcp_ext.transports import _build_http_middleware, run_server
from arifosmcp.runtime.orchestrator import metabolic_loop
from arifosmcp.runtime.phase2_tools import register_phase2_tools
from arifosmcp.runtime.prompts import register_prompts
from arifosmcp.runtime.resources import register_resources
from arifosmcp.runtime.rest_routes import register_rest_routes
from arifosmcp.runtime.tools import (
    apex_judge_verdict,
    assess_heart_impact,
    critique_thought_audit,
    init_anchor_state,
    integrate_analyze_reflect,
    metabolic_loop_router,
    quantum_eureka_forge,
    reason_mind_synthesis,
    register_tools,
    seal_vault_commit,
    vector_memory_store,
)

# ---------------------------------------------------------------------------
# Phase 1 — Core Constitutional Stack (10 tools)
# ---------------------------------------------------------------------------

mcp = FastMCP("arifOS-APEX-G", version="2026.03.08-SEAL")

register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)

CORE_TOOL_REGISTRY = {
    "init_anchor_state": init_anchor_state,
    "integrate_analyze_reflect": integrate_analyze_reflect,
    "reason_mind_synthesis": reason_mind_synthesis,
    "metabolic_loop_router": metabolic_loop_router,
    "vector_memory_store": vector_memory_store,
    "assess_heart_impact": assess_heart_impact,
    "critique_thought_audit": critique_thought_audit,
    "quantum_eureka_forge": quantum_eureka_forge,
    "apex_judge_verdict": apex_judge_verdict,
    "seal_vault_commit": seal_vault_commit,
}

register_rest_routes(mcp, CORE_TOOL_REGISTRY)


# ---------------------------------------------------------------------------
# Phase 2 — External Capability Tools (legacy-enabled, not in new loop)
# ---------------------------------------------------------------------------

register_phase2_tools(mcp)


# ---------------------------------------------------------------------------
# ASGI export for uvicorn/platform HTTP deployment
# ---------------------------------------------------------------------------

HTTP_PATH = os.getenv("ARIFOS_MCP_PATH", "/mcp/")
# Enable stateless HTTP for Cloudflare compatibility (no session persistence needed)
app = mcp.http_app(
    path=HTTP_PATH, 
    middleware=_build_http_middleware(),
    stateless_http=True
)

# Mount APEX dashboard static files
_dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "apex-dashboard")
if os.path.isdir(_dashboard_dir):
    app.mount("/dashboard", StaticFiles(directory=_dashboard_dir, html=True), name="dashboard")


def create_aaa_mcp_server() -> FastMCP:
    """Return the fully configured arifOS MCP hub."""
    return mcp


__all__ = [
    "HTTP_PATH",
    "app",
    "apex_judge_verdict",
    "assess_heart_impact",
    "create_aaa_mcp_server",
    "critique_thought_audit",
    "init_anchor_state",
    "integrate_analyze_reflect",
    "mcp",
    "metabolic_loop",
    "metabolic_loop_router",
    "quantum_eureka_forge",
    "reason_mind_synthesis",
    "seal_vault_commit",
    "vector_memory_store",
]


if __name__ == "__main__":
    mode = os.getenv("AAA_MCP_TRANSPORT", "stdio")
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    run_server(mcp, mode=mode, host=host, port=port)
