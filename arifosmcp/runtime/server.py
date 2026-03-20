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
import sys
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.transforms import ResourcesAsTools, Visibility
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from arifosmcp.runtime.fastmcp_ext.transports import (
    _build_http_middleware,
    _normalize_path,
    run_server,
)
from arifosmcp.runtime.orchestrator import metabolic_loop
from arifosmcp.runtime.prompts import register_prompts
from arifosmcp.runtime.public_registry import (
    is_public_profile,
    normalize_tool_profile,
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
    register_tools,
    ALL_TOOL_IMPLEMENTATIONS,
)
from arifosmcp.runtime.contracts import verify_contract
from arifosmcp.runtime.public_registry import verify_no_drift
from core.shared.manifest_loader import sync_runtime_floors

# ---------------------------------------------------------------------------
# Phase 1 — arifOS APEX-G Sovereign Hub (2026-03-14 Epoch)
# ---------------------------------------------------------------------------

CONSTITUTIONAL_INSTRUCTIONS = """
You are interacting with arifOS, a Constitutional AGI Governance System.
All actions must pass the 13 Constitutional Floors (F1-F13).

The architecture is consolidated into 11 Final Mega-Tools across three layers:
- ⚖️ GOVERNANCE: init_anchor, arifOS_kernel, apex_soul, vault_ledger
- 🧠 INTELLIGENCE: agi_mind, asi_heart, engineering_memory
- ⚙️ MACHINE: physics_reality, math_estimator, code_engine, architect_registry

Always use the appropriate 'mode' for each mega-tool to access underlying functions.
"""


@asynccontextmanager
async def arifos_lifespan(server: FastMCP):
    """Lifecycle management for the arifOS Double Helix organs."""
    # Register arifOS-specific Prometheus metrics
    from arifosmcp.runtime.metrics import FLOOR_VIOLATIONS, VERDICT_TOTAL, GENIUS_SCORE, ENTROPY_DELTA, HUMILITY_BAND, PEACE_SQUARED, Counter
    
    # Custom metric for registry panic monitoring
    DRIFT_PANICS = Counter(
        "arifos_registry_drift_panics_total",
        "Total number of server start-up failures due to registry drift."
    )

    # CRITICAL: Verify 11-tool contract on startup
    drift_check = verify_no_drift()
    if not drift_check["ok"]:
        DRIFT_PANICS.inc()
        raise RuntimeError(
            f"arifOS FATAL: Tool registry drift detected!\n"
            f"Expected {drift_check['expected_count']} tools, got {drift_check['actual_count']}\n"
            f"Missing: {drift_check.get('missing', [])}\n"
            f"Extra: {drift_check.get('extra', [])}"
        )

    contract_check = verify_contract()
    if not contract_check["ok"]:
        raise RuntimeError(
            f"arifOS FATAL: Contract verification failed!\nChecks: {contract_check['checks']}"
        )

    sync_runtime_floors()
    yield


mcp = FastMCP(
    "arifOS-APEX-G",
    version="2026.03.20-CONSOLIDATION",
    instructions=CONSTITUTIONAL_INSTRUCTIONS,
    website_url="https://arifosmcp.arif-fazil.com",
    lifespan=arifos_lifespan,
    strict_input_validation=True,
    list_page_size=20,
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

register_rest_routes(mcp, ALL_TOOL_IMPLEMENTATIONS)


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
_session_secret = os.getenv("SESSION_SECRET") or os.urandom(32).hex()
app.add_middleware(
    SessionMiddleware,
    secret_key=_session_secret,
    max_age=3600,
    same_site="strict",
    https_only=os.getenv("SESSION_SECURE", "true").lower() == "true",
    session_cookie="arifos_session",
)

# Root-level discovery configuration
_sites_dir = os.path.join(os.path.dirname(__file__), "..", "sites")


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


async def well_known_agent(request):
    """A2A Agent Card discovery endpoint (Google Protocol - April 2025)."""
    return JSONResponse(
        {
            "name": "arifOS Constitutional Kernel",
            "description": "AI governance system with 13 constitutional floors (F1-F13)",
            "url": "https://arifosmcp.arif-fazil.com",
            "version": "2026.03.20-CONSOLIDATION",
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
                "execute": "/a2a/execute",
                "status": "/a2a/status",
                "cancel": "/a2a/cancel",
                "subscribe": "/a2a/subscribe",
            },
        }
    )


async def get_health_reentry(request):
    """Re-entry point for /health to avoid shadowing."""
    from arifosmcp.runtime.rest_routes import BUILD_INFO
    from core.shared.floor_audit import get_ml_floor_runtime
    from arifosmcp.runtime.capability_map import build_runtime_capability_map
    from datetime import datetime, timezone

    return JSONResponse(
        {
            "status": "healthy",
            "service": "arifos-aaa-mcp",
            "version": BUILD_INFO["version"],
            "transport": "streamable-http",
            "tools_loaded": len(ALL_TOOL_IMPLEMENTATIONS),
            "ml_floors": get_ml_floor_runtime(),
            "capability_map": build_runtime_capability_map(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        headers={"Access-Control-Allow-Origin": "*"},
    )


# Register all root-level discovery routes at the beginning to avoid shadowing
_mcp_app.routes.insert(0, Route("/health", get_health_reentry, methods=["GET"]))
_mcp_app.routes.insert(0, Route("/.well-known/agent.json", well_known_agent, methods=["GET"]))
_mcp_app.routes.insert(0, Route("/llms.txt", get_llms_txt, methods=["GET"]))
_mcp_app.routes.insert(0, Route("/ai.json", get_ai_json, methods=["GET"]))
_mcp_app.routes.insert(0, Route("/robots.txt", get_robots_txt, methods=["GET"]))
_mcp_app.routes.insert(0, Route("/openapi.json", get_openapi_json, methods=["GET"]))
_mcp_app.routes.insert(0, Route("/RAG_CONTEXT.md", get_rag_context, methods=["GET"]))
_mcp_app.routes.insert(
    0, Route("/DELEGATION_PROTOCOL.md", get_delegation_protocol, methods=["GET"])
)

# Mount Static sites
if os.path.isdir(_sites_dir):
    _mcp_app.routes.insert(
        0, Mount("/static-sites", StaticFiles(directory=_sites_dir, html=True), name="static-sites")
    )

# Mount APEX dashboard static files
_dashboard_dir = os.path.join(os.path.dirname(__file__), "..", "sites", "dashboard")
if os.path.isdir(_dashboard_dir):

    async def _dashboard_slash_redirect(request):
        from starlette.responses import RedirectResponse

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

# Mount REAL A2A Server (Google Protocol - April 2025)
try:
    from arifosmcp.runtime.a2a import create_a2a_server

    _a2a_server = create_a2a_server(mcp)

    # Mount A2A at /a2a
    _mcp_app.mount("/a2a", _a2a_server.app, name="a2a")

    print("✅ Real A2A Server mounted at /a2a (Google Protocol)", file=sys.stderr)

except ImportError as e:
    print(f"⚠️ A2A not available: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# WebMCP Integration - AI-Governed Web Environment
# ---------------------------------------------------------------------------

_WEBMCP_ENABLED = os.getenv("ARIFOS_WEBMCP_ENABLED", "true").lower() in ("true", "1", "yes")

if _WEBMCP_ENABLED:
    try:
        from .webmcp import WebMCPGateway

        # Mount the legacy WebMCP gateway last so its root mount does not
        # swallow more specific protocol routes such as /a2a/*.
        _webmcp_gateway = WebMCPGateway(mcp)
        _webmcp_app = _webmcp_gateway.app
        _mcp_app.mount("/", _webmcp_app, name="webmcp_root")

        print("✅ WebMCP gateway integrated at root", file=sys.stderr)

    except ImportError as e:
        print(f"⚠️ WebMCP not available: {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ WebMCP integration failed: {e}", file=sys.stderr)


def create_aaa_mcp_server() -> FastMCP:
    """Return the fully configured arifOS MCP hub."""
    return mcp


__all__ = [
    "app",
    "mcp",
    "create_aaa_mcp_server",
    "PUBLIC_TOOL_PROFILE",
    "register_tools",
    # 11 MEGA-TOOLS
    "init_anchor",
    "arifOS_kernel",
    "apex_soul",
    "vault_ledger",
    "agi_mind",
    "asi_heart",
    "engineering_memory",
    "physics_reality",
    "math_estimator",
    "code_engine",
    "architect_registry",
]


if __name__ == "__main__":
    t_mode = os.getenv("AAA_MCP_TRANSPORT", "stdio").strip().lower()
    mode = _validate_transport_mode(t_mode)
    host = os.getenv("HOST", "0.0.0.0")
    port = _parse_port(os.getenv("PORT", "8080"))
    run_server(mcp, mode=mode, host=host, port=port)
