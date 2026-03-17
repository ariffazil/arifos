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
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.transforms import ResourcesAsTools, Visibility
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

try:
    from arifosmcp.apps.apex_score import _register as _register_apex_score_app
    from arifosmcp.apps.stage_pipeline import _register as _register_stage_pipeline_app

    _PREFAB_APPS_AVAILABLE = True
except ImportError:
    _PREFAB_APPS_AVAILABLE = False
from arifosmcp.runtime.tools import (
    agi_reason,
    agi_reflect,
    asi_critique,
    asi_simulate,
    apex_judge,
    audit_rules,
    agentzero_armor_scan,
    agentzero_engineer,
    agentzero_hold_check,
    agentzero_memory_query,
    agentzero_validate,
    check_vital,
    forge,
    ingest_evidence,
    init_anchor,
    arifos_kernel,
    open_apex_dashboard,
    reality_atlas,
    reality_compass,
    register_tools,
    revoke_anchor_state,
    search_reality,
    vault_seal,
    verify_vault_ledger,
)
from arifosmcp.intelligence import console_tools as aclip_tools
from core.shared.manifest_loader import sync_runtime_floors

# ---------------------------------------------------------------------------
# Phase 1 — arifOS APEX-G Sovereign Hub (2026-03-14 Epoch)
# ---------------------------------------------------------------------------

CONSTITUTIONAL_INSTRUCTIONS = """
You are interacting with arifOS, a Constitutional AGI Governance System.
All actions must pass the 13 Constitutional Floors:
F1 Amanah, F2 Truth, F3 Tri-Witness, F4 ΔS Clarity, F5 Peace², F6 kr Empathy, 
F7 Omega Humility, F8 G Genius, F9 C_dark, F10 Ontology, F11 Command Auth, 
F12 Injection, F13 Sovereign.

The architecture is a Double Helix:
- Inner Ring: 8 Sacred Constitutional Organs (init_anchor, agi_reason, etc.)
- Outer Ring: 7 Peripheral Nervous System (PNS) Organs (shield, search, etc.)

Strictly follow the Sacred Chain loop: INIT -> REASON -> REFLECT -> SIMULATE -> CRITIQUE -> FORGE -> JUDGE -> SEAL.
"""


@asynccontextmanager
async def arifos_lifespan(server: FastMCP):
    """Lifecycle management for the arifOS Double Helix organs."""
    # INIT Stage: Ignition — sync Mind to Body
    sync_runtime_floors()
    yield


mcp = FastMCP(
    "arifOS-APEX-G",
    version="2026.03.14-VALIDATED",
    instructions=CONSTITUTIONAL_INSTRUCTIONS,
    lifespan=arifos_lifespan,
)
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

# ── FastMCP Prefab UI Apps (Human Interface) ─────────────────────────────────
if _PREFAB_APPS_AVAILABLE:
    _register_apex_score_app(mcp)  # APEX G-Score card: metrics + philosophy + verdict
    _register_stage_pipeline_app(mcp)  # 000→999 Sacred Chain pipeline visualiser

# Hide internal tools from public clients (untested/mock-auth AgentZero tools)
if is_public_profile(PUBLIC_TOOL_PROFILE):
    mcp.add_transform(Visibility(False, tags={"internal"}))

# Expose resources as tools for tool-only clients (ChatGPT, REST adapters)
mcp.add_transform(ResourcesAsTools(mcp))

# Sync Mind to Body (Dynamic Connection)
sync_runtime_floors()

CORE_TOOL_REGISTRY = {
    # ── Orchestration entry point ────────────────────────────────────────────
    "arifOS_kernel": arifos_kernel,
    # ── 8 Sacred Constitutional Organs (Inner Ring) ──────────────────────────
    "init_anchor": init_anchor,
    "agi_reason": agi_reason,
    "agi_reflect": agi_reflect,
    "asi_simulate": asi_simulate,
    "asi_critique": asi_critique,
    "forge": forge,
    "apex_judge": apex_judge,
    "vault_seal": vault_seal,
    # ── Reality / Evidence layer ─────────────────────────────────────────────
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "reality_compass": reality_compass,
    "reality_atlas": reality_atlas,
    # ── Constitutional utilities ─────────────────────────────────────────────
    "audit_rules": audit_rules,
    "check_vital": check_vital,
    "open_apex_dashboard": open_apex_dashboard,
    "verify_vault_ledger": verify_vault_ledger,
    # ── AgentZero Parliament Tools (Outer Ring) ──────────────────────────────
    "agentzero_validate": agentzero_validate,
    "agentzero_engineer": agentzero_engineer,
    "agentzero_hold_check": agentzero_hold_check,
    "agentzero_memory_query": agentzero_memory_query,
    "agentzero_armor_scan": agentzero_armor_scan,
    # ── Session lifecycle ────────────────────────────────────────────────────
    "revoke_anchor_state": revoke_anchor_state,
    # ── ACLIP Nervous System Tools (Operational) ───────────────────────────────
    "system_health": aclip_tools.system_health,
    "process_list": aclip_tools.process_list,
    "fs_inspect": aclip_tools.fs_inspect,
    "log_tail": aclip_tools.log_tail,
    "net_status": aclip_tools.net_status,
    "chroma_query": aclip_tools.chroma_query,
    "arifos_list_resources": aclip_tools.arifos_list_resources,
    "arifos_read_resource": aclip_tools.arifos_read_resource,
    "cost_estimator": aclip_tools.cost_estimator,
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

# Session middleware required for WebMCP (F11 Command Auth)
# Must be added before WebMCP mounts
import os
from starlette.middleware.sessions import SessionMiddleware

_session_secret = os.getenv("SESSION_SECRET") or os.urandom(32).hex()
app.add_middleware(
    SessionMiddleware,
    secret_key=_session_secret,
    max_age=3600,
    same_site="strict",
    https_only=os.getenv("SESSION_SECURE", "true").lower() == "true",
    session_cookie="arifos_session",
)

# Additional middleware can be added here if needed,
# but CORS and Auth are already handled by _build_http_middleware()

# Mount APEX dashboard static files (v2.1 - Real-time governance dashboard)
_dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "dashboard")
if os.path.isdir(_dashboard_dir):
    # Add redirect for /dashboard → /dashboard/ before mount
    from starlette.responses import RedirectResponse
    from starlette.routing import Route

    async def _dashboard_slash_redirect(request):
        return RedirectResponse(url="/dashboard/", status_code=307)

    _mcp_app.routes.insert(0, Route("/dashboard", _dashboard_slash_redirect))
    _mcp_app.mount("/dashboard", StaticFiles(directory=_dashboard_dir, html=True), name="dashboard")

# Legacy dashboard (fallback)
_apex_dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "apex-dashboard")
if os.path.isdir(_apex_dashboard_dir):
    _mcp_app.mount(
        "/apex-dashboard",
        StaticFiles(directory=_apex_dashboard_dir, html=True),
        name="apex-dashboard",
    )

# Mount H1 Developer Portal
_developer_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "developer")
if os.path.isdir(_developer_dir):
    _mcp_app.mount("/developer", StaticFiles(directory=_developer_dir, html=True), name="developer")

# ---------------------------------------------------------------------------
# WebMCP Integration - AI-Governed Web Environment
# ---------------------------------------------------------------------------
# WebMCP extends MCP to browsers with constitutional enforcement (F1-F13)
# Every HTTP request passes through the 000→999 metabolic loop.
# ---------------------------------------------------------------------------

_WEBMCP_ENABLED = os.getenv("ARIFOS_WEBMCP_ENABLED", "true").lower() in ("true", "1", "yes")

if _WEBMCP_ENABLED:
    try:
        from .webmcp import WebMCPGateway

        # Create WebMCP gateway mounted at /webmcp
        _webmcp_gateway = WebMCPGateway(mcp)
        _webmcp_app = _webmcp_gateway.app

        # Mount WebMCP routes into main app
        # WebMCP app already has /webmcp, /api/live, /governance prefixes
        _mcp_app.mount("/", _webmcp_app, name="webmcp")

        print("✅ WebMCP gateway integrated at /webmcp, /api/live, /governance")

    except ImportError as e:
        print(f"⚠️ WebMCP not available: {e}. Run: pip install itsdangerous fastapi uvicorn redis")
    except Exception as e:
        print(f"❌ WebMCP integration failed: {e}")

# Serve trinity-nav.js globally
_sites_dir = os.path.join(os.path.dirname(__file__), "..", "sites")
if os.path.isdir(_sites_dir):
    _mcp_app.mount("/static-sites", StaticFiles(directory=_sites_dir), name="static-sites")

    # Root-level discovery files
    from starlette.responses import FileResponse
    from starlette.routing import Route

    async def get_llms_txt(request):
        return FileResponse(os.path.join(_sites_dir, "llms.txt"))

    async def get_ai_json(request):
        return FileResponse(os.path.join(_sites_dir, "ai.json"))

    async def get_robots_txt(request):
        return FileResponse(os.path.join(_sites_dir, "robots.txt"))

    async def get_openapi_json(request):
        return FileResponse(os.path.join(_sites_dir, "openapi.json"))

    async def get_rag_context(request):
        return FileResponse(os.path.join(_sites_dir, "RAG_CONTEXT.md"))

    async def get_delegation_protocol(request):
        return FileResponse(os.path.join(_sites_dir, "DELEGATION_PROTOCOL.md"))


# Mount REAL WebMCP Gateway (W3C Standard - Feb 2026)
# This provides browser-native MCP with navigator.modelContext API
try:
    from arifosmcp.runtime.webmcp.real_webmcp import create_real_webmcp, WebMCPConfig

    _webmcp_config = WebMCPConfig(
        site_name="arifOS Constitutional AI",
        site_url="https://arifosmcp.arif-fazil.com",
        version="2026.03.14-VALIDATED",
        enable_declarative=True,
        enable_imperative=True,
        require_human_confirmation=True,  # F13 Sovereign
    )

    _webmcp_gateway = create_real_webmcp(mcp, _webmcp_config)

    # Mount WebMCP at /webmcp
    _mcp_app.mount("/webmcp", _webmcp_gateway.app, name="webmcp")

    print("✅ Real WebMCP Gateway mounted at /webmcp (W3C Standard)")

except ImportError as e:
    print(f"⚠️ WebMCP not available: {e}")

    _mcp_app.router.add_route("/llms.txt", get_llms_txt, methods=["GET"], include_in_schema=False)
    _mcp_app.router.add_route("/ai.json", get_ai_json, methods=["GET"], include_in_schema=False)
    _mcp_app.router.add_route(
        "/robots.txt", get_robots_txt, methods=["GET"], include_in_schema=False
    )
    _mcp_app.router.add_route(
        "/openapi.json", get_openapi_json, methods=["GET"], include_in_schema=False
    )
    _mcp_app.router.add_route(
        "/RAG_CONTEXT.md", get_rag_context, methods=["GET"], include_in_schema=False
    )
    _mcp_app.router.add_route(
        "/DELEGATION_PROTOCOL.md", get_delegation_protocol, methods=["GET"], include_in_schema=False
    )

# Mount REAL A2A Server (Google Protocol - April 2025)
# This provides Agent-to-Agent protocol for multi-agent collaboration
try:
    from arifosmcp.runtime.a2a import create_a2a_server

    _a2a_server = create_a2a_server(mcp)

    # Mount A2A at /a2a
    _mcp_app.mount("/a2a", _a2a_server.app, name="a2a")

    # Also mount at root for /.well-known/agent.json
    from starlette.responses import JSONResponse

    async def well_known_agent(request):
        """A2A Agent Card discovery endpoint."""
        return JSONResponse(
            {
                "name": "arifOS Constitutional Kernel",
                "description": "AI governance system with 13 constitutional floors (F1-F13)",
                "url": "https://arifosmcp.arif-fazil.com",
                "version": "2026.03.14-VALIDATED",
                "authentication": {"schemes": ["none", "api_key"]},
                "capabilities": {
                    "streaming": True,
                    "pushNotifications": False,
                },
                "skills": [
                    {
                        "id": "constitutional_review",
                        "name": "Constitutional Review",
                        "description": "Review actions against 13 constitutional floors",
                    },
                    {
                        "id": "task_execution",
                        "name": "Governed Task Execution",
                        "description": "Execute tasks with full constitutional oversight",
                    },
                ],
                "endpoints": {
                    "task": "/a2a/task",
                    "status": "/a2a/status",
                    "cancel": "/a2a/cancel",
                    "subscribe": "/a2a/subscribe",
                },
            }
        )

    # Register the route using Starlette's router
    _mcp_app.router.add_route("/.well-known/agent.json", well_known_agent, methods=["GET"])

    print("✅ Real A2A Server mounted at /a2a (Google Protocol)")
    print("✅ Agent Card available at /.well-known/agent.json")

except ImportError as e:
    print(f"⚠️ A2A not available: {e}")


def create_aaa_mcp_server() -> FastMCP:
    """Return the fully configured arifOS MCP hub."""
    return mcp


__all__ = [
    "app",
    "arifos_kernel",
    "audit_rules",
    "check_vital",
    "create_aaa_mcp_server",
    "ingest_evidence",
    "mcp",
    "open_apex_dashboard",
    "PUBLIC_TOOL_PROFILE",
    "register_tools",
    "search_reality",
    # FastMCP Apps
    "apex_score_app",
    "stage_pipeline_app",
]


if __name__ == "__main__":
    mode = _validate_transport_mode(os.getenv("AAA_MCP_TRANSPORT", "stdio"))
    host = os.getenv("HOST", "0.0.0.0")
    port = _parse_port(os.getenv("PORT", "8080"))
    run_server(mcp, mode=mode, host=host, port=port)
