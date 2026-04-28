"""
arifOS MCP Server — Canonical Entry Point
═══════════════════════════════════════════

13-tool capability surface | internal ping/selftest | 13 Floors (F1–F13) | Trinity ΔΩΨ
FastMCP 3.2.0 + MCP Apps + Streamable HTTP
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import traceback
from typing import Any


# Ensure project root is on path — /app before /app/arifosmcp
# so "from core.shared" resolves to /app/core/shared/ (correct)
# not /app/arifosmcp/core/ (stub package — wrong)
def _prioritize_paths(*paths: str) -> None:
    for path in reversed(paths):
        if path in sys.path:
            sys.path.remove(path)
    for path in reversed(paths):
        sys.path.insert(0, path)


_project_root = os.path.dirname(os.path.abspath(__file__))  # /usr/src/app/arifosmcp
_parent = os.path.dirname(_project_root)  # /usr/src/app
_parent_idx = sys.path.index(_parent) if _parent in sys.path else len(sys.path)
_project_root_idx = sys.path.index(_project_root) if _project_root in sys.path else len(sys.path)
if _parent not in sys.path or _project_root not in sys.path or _parent_idx > _project_root_idx:
    _prioritize_paths(_parent, _project_root)

from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(_project_root), ".env")
if os.path.exists(_env_path):
    load_dotenv(_env_path, override=True)

import fastmcp
from arifosmcp.constitutional_map import (
    CANONICAL_TOOLS,
    list_authenticated_tools,
    list_canonical_tools,
    list_constitutional_tools,
    list_probe_tools,
    list_public_tools,
    list_sovereign_tools,
)
from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)

_canonical_tool_names = list_canonical_tools()
_canonical_tool_names_text = ", ".join(_canonical_tool_names)
_constitutional_tool_names = list_constitutional_tools()
_probe_tool_names = list_probe_tools()


class GlobalPanicMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            print(f"!!! KERNEL PANIC: {e}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            return JSONResponse(
                {
                    "status": "void",
                    "tool": "kernel_panic_handler",
                    "error_message": "F13: System halt due to unhandled kernel exception.",
                    "action": "HALT",
                },
                status_code=500,
            )


mcp = FastMCP(
    "ARIFOS MCP",
    version="2026.04.26-KANON",
    website_url="https://arifosmcp.arif-fazil.com",
    instructions=(
        "Constitutional AI orchestration kernel — arifOS.\n\n"
        "Golden path: init → sense → mind → heart → judge → vault\n\n"
        "Runtime surface: 13 public capability tools.\n"
        f"Tools (arif_noun_verb):\n  {_canonical_tool_names_text}\n\n"
        "DITEMPA BUKAN DIBERI — Forged, Not Given"
    ),
)

_engineering_lock_path = os.path.join(os.path.dirname(_project_root), ".ENGINEERING_LOCK")
if not os.path.exists(_engineering_lock_path):
    logger.warning("Engineering lock missing at startup: %s", _engineering_lock_path)


def create_arifos_mcp_server() -> FastMCP:
    return mcp


# CC tool names — registered via mcp.tool(name=...) in server.py, NOT via _register_tools()
_CC_TOOL_NAMES: frozenset[str] = frozenset({
    "session_status", "ops_vitals", "judge_action", "forge_dry_run",
    "gateway_handshake", "vault_list", "vault_dry_seal",
})

def _assert_registered_surface(registered_names: list[str]) -> None:
    registered_set = set(registered_names)
    # _register_tools() registers only the 13 non-CC canonical handlers.
    # The 7 CC tools are registered separately via mcp.tool(name=...) below.
    expected_non_cc = {name for name in CANONICAL_TOOLS if name not in _CC_TOOL_NAMES}

    if registered_set != expected_non_cc:
        missing = sorted(expected_non_cc - registered_set)
        extra = sorted(registered_set - expected_non_cc)
        raise RuntimeError(
            f"Ontology mismatch: missing={missing} extra={extra}"
        )

    if any(name.startswith("arifos_") for name in registered_names):
        raise RuntimeError("Legacy surface detected in registered MCP tools")


v2_tools_registered: list[str] = []
v2_prompts_registered: list[str] = []
v2_resources_registered: list[str] = []
v2_apps_registered: list[str] = []

IS_FASTMCP_3 = fastmcp.__version__.startswith("3")

try:
    from arifosmcp.prompts import CANONICAL_PROMPTS, register_prompts
    from arifosmcp.resources import CANONICAL_RESOURCES, register_resources
    from arifosmcp.runtime.tools import register_tools

    v2_tools_registered = register_tools(mcp)
    _assert_registered_surface(v2_tools_registered)
    v2_prompts_registered = register_prompts(mcp)
    if tuple(v2_prompts_registered) != CANONICAL_PROMPTS:
        raise RuntimeError(
            f"Prompt drift detected: expected {list(CANONICAL_PROMPTS)}, got {v2_prompts_registered}"
        )
    v2_resources_registered = register_resources(mcp)
    if tuple(v2_resources_registered) != CANONICAL_RESOURCES:
        raise RuntimeError(
            "Resource drift detected: "
            f"expected {list(CANONICAL_RESOURCES)}, got {v2_resources_registered}"
        )
    logger.info(
        f"ARIFOS MCP KANON Phase 1: {len(v2_tools_registered)} tools, "
        f"{len(v2_prompts_registered)} prompts, {len(v2_resources_registered)} resources"
    )
except Exception as e:
    logger.error(f"Failed to initialize runtime components: {e}")
    raise


# ── MCP Apps registration ───────────────────────────────────────────────────
# Each app in its own try block so one failure doesn't cascade
def _safe_register(mcp, module_path: str, name: str) -> None:
    import sys

    try:
        import importlib

        mod = importlib.import_module(module_path)
        print(f"[arif-register] Importing {module_path}...", flush=True)
        mod._register(mcp)
        v2_apps_registered.append(name)
        print(f"[arif-register] Registered: {name} OK", flush=True)
        logger.info(f"  Registered app: {name}")
    except Exception as e:
        import traceback

        print(f"[arif-register] FAILED {name}: {e}", flush=True)
        traceback.print_exc(file=sys.stdout)
        logger.warning(f"  Skipped app {name} ({module_path}): {e}")


# ── MCP Apps registration ───────────────────────────────────────────────────
# command_center FastMCPApp (UI layer) is DISABLED — its tools have
# visibility=["app"] and do NOT appear in MCP tools/list for clients.
#
# The 7 command_center tools are wired HERE as direct MCP tool handlers
# pointing to real canonical backends. This makes them proper MCP tools
# visible to all clients, while keeping command_center as the logical owner.
#
# Tool wiring:
#   session_status      → internal session state panel
#   ops_vitals          → arif_ops_measure(mode="vitals")
#   judge_action        → arif_judge_deliberate via governed wrapper
#   forge_dry_run       → arif_forge_execute(mode="dry_run") via governed wrapper
#   vault_list          → VAULT999 ledger read
#   vault_dry_seal      → arif_vault_seal(mode="dry_run") via governed wrapper
#   gateway_handshake   → arif_gateway_connect
# ─────────────────────────────────────────────────────────────────────────────
try:
    from arifosmcp.apps.command_center.governance import classify_risk
    from arifosmcp.apps.command_center.interceptor import governance_guard
    from arifosmcp.apps.command_center.judge_app import governed_judge_deliberate
    from arifosmcp.apps.command_center.forge_app import governed_forge_execute
    from arifosmcp.apps.command_center.state import get_state
    from arifosmcp.apps.command_center.vault_audit import get_vault_audit
    from arifosmcp.apps.command_center.vault_chain import append_vault_record
    from arifosmcp.tools.forge import arif_forge_execute as _cc_forge
    from arifosmcp.tools.gateway import arif_gateway_connect as _cc_gateway
    from arifosmcp.tools.ops import arif_ops_measure as _cc_ops
    from arifosmcp.schemas.forge import ForgeOutput
    from arifosmcp.schemas.verdict import VerdictOutput
    _CC_WIRING_OK = True
except Exception as e:
    logger.warning(f"command_center wiring incomplete: {e}")
    _CC_WIRING_OK = False


def _cc_session_status() -> dict:
    """UI panel: live constitutional session state. Read-only diagnostic."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    state = get_state()
    local = state.get_session()
    if not local:
        return {"session_id": None, "status": "no_session"}
    from arifosmcp.apps.command_center.models import SessionStatus
    return SessionStatus(
        session_id=local.session_id,
        actor_id=local.actor_id,
        constitution_id="arifos-constitution-v2026.04.26",
        stage="000",
        lane="AGI",
        sealed=False,
        authority="human_judge_required",
        plan_state="draft",
        token=getattr(local, "token", None),
        floor_audit=getattr(local, "floor_audit", {}),
        created_at=getattr(local, "created_at", None),
        expires_at=getattr(local, "expires_at", None),
    ).model_dump()


def _cc_ops_vitals() -> dict:
    """UI panel: thermodynamic health vitals. Read-only."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    result = _cc_ops(mode="vitals")
    from arifosmcp.apps.command_center.models import OpsVitals
    return OpsVitals(
        g_score=result.g_score,
        delta_S=result.delta_S,
        omega=result.omega,
        psi_le=result.psi_le,
        status=result.meta.get("status", "OK"),
    ).model_dump()


def _cc_judge_action(candidate: str) -> dict:
    """Submit a candidate action for constitutional verdict."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    if not isinstance(candidate, str):
        candidate = str(candidate) if candidate is not None else ""
    live = get_state().get_session()
    session_id = live.get("session_id", "uninitialized") if live else "uninitialized"
    plan_id = live.get("plan_id") if live else None
    plan_state = live.get("caller_state", "draft") if live else "draft"
    return governed_judge_deliberate(
        candidate=candidate,
        actor_id="arif",
        session_id=session_id,
        plan_id=plan_id,
        plan_state=plan_state,
    )


def _cc_forge_dry_run(manifest: str) -> dict:
    """Simulate a forge execution. No gates checked, no vault written."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    if not isinstance(manifest, str):
        manifest = str(manifest) if manifest is not None else ""
    risk = classify_risk(manifest)
    reversibility = "uncertain" if risk in {"high", "critical"} else "reversible"
    result = _cc_forge(mode="dry_run", manifest=manifest)
    forge_result = result.result if hasattr(result, "result") else {}
    from arifosmcp.apps.command_center.models import ForgeDryRun
    return ForgeDryRun(
        routing_path=["init", "sense", "mind"],
        mode="dry_run",
        would_execute=False,
        manifest_summary=manifest[:120] + ("..." if len(manifest) > 120 else ""),
        reversibility=reversibility,
        required_verdict="SEAL",
        status="simulated",
        plan_state="draft",
    ).model_dump()


def _cc_gateway_handshake(target_agent: str) -> dict:
    """Initiate cross-agent A2A handshake with federation agent."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    if not isinstance(target_agent, str):
        target_agent = str(target_agent) if target_agent is not None else ""
    result = _cc_gateway(mode="connect", target=target_agent)
    from arifosmcp.apps.command_center.models import GatewayHandshake
    return GatewayHandshake(
        target_agent=target_agent,
        handshake="connected" if result.get("status") == "ok" else "failed",
        constitution_hash_required=True,
        rogue_agent_protection=True,
    ).model_dump()


def _cc_vault_list() -> dict:
    """Read last 20 entries from VAULT999 ledger. Read-only."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    audit = get_vault_audit(limit=20)
    from arifosmcp.apps.command_center.models import VaultEntry, VaultList
    entries = [
        VaultEntry(
            id=e.get("entry_id", "unknown"),
            type=e.get("type", "seal"),
            permanent=e.get("permanent", False),
            note=e.get("note", "")[:80],
            timestamp=e.get("timestamp", ""),
            prev_hash=e.get("prev_hash", ""),
        )
        for e in audit.get("entries", [])
    ]
    return VaultList(
        entries=entries,
        total_count=audit.get("total", 0),
        chain_valid=audit.get("chain_valid", False),
    ).model_dump()


def _cc_vault_dry_seal(payload: str) -> dict:
    """Preview a vault seal without writing to ledger."""
    if not _CC_WIRING_OK:
        return {"error": "command_center not fully wired"}
    if not isinstance(payload, str):
        payload = str(payload) if payload is not None else ""
    result = governed_forge_execute(
        manifest=payload,
        actor_id="arif",
        session_id="cc_dry_seal",
        plan_id=None,
        mode="dry_run",
    )
    from arifosmcp.apps.command_center.models import VaultDrySeal
    return VaultDrySeal(
        routing_path=["init", "sense", "vault"],
        mode="dry_seal",
        permanent=False,
        payload_preview=payload[:120],
        seal_result=result,
    ).model_dump()


# Register the 7 command_center tools on the main MCP server
if _CC_WIRING_OK:
    mcp.tool(name="session_status")(_cc_session_status)
    mcp.tool(name="ops_vitals")(_cc_ops_vitals)
    mcp.tool(name="judge_action")(_cc_judge_action)
    mcp.tool(name="forge_dry_run")(_cc_forge_dry_run)
    mcp.tool(name="gateway_handshake")(_cc_gateway_handshake)
    mcp.tool(name="vault_list")(_cc_vault_list)
    mcp.tool(name="vault_dry_seal")(_cc_vault_dry_seal)
    print("[arif-register] command_center 7 tools wired to canonical backends ✅", flush=True)
    logger.info("ARIFOS MCP KANON Phase 2: command_center 7 tools wired to canonical backends")
else:
    print("[arif-register] command_center wiring FAILED — see warnings above", flush=True)
    logger.warning("ARIFOS MCP KANON Phase 2: command_center wiring incomplete")

PUBLIC_TOOLS = list_public_tools()
AUTHENTICATED_TOOLS = list_authenticated_tools()
SOVEREIGN_TOOLS = list_sovereign_tools()


async def horizon_health(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "healthy",
            "service": "arifos-mcp-kanon",
            "version": "2026.04.26-KANON",
            "gateway": "unified",
            "tools": len(v2_tools_registered),
            "prompts": len(v2_prompts_registered),
            "resources": len(v2_resources_registered),
            "apps": len(v2_apps_registered),
            "canonical_surface": len(_constitutional_tool_names),
            "probe_surface": len(_probe_tool_names),
            "registered_surface": len(v2_tools_registered),
            "timestamp": __import__("datetime")
            .datetime.now(__import__("datetime").timezone.utc)
            .isoformat(),
        }
    )


async def horizon_ready(request: Request) -> JSONResponse:
    from arifosmcp.runtime.tools import _runtime_selftest

    readiness = _runtime_selftest()
    verdict = str(readiness.get("verdict", "FAIL")).lower()
    return JSONResponse(
        {
            "status": verdict,
            "checks": readiness.get("checks", {}),
            "failures": readiness.get("failed_checks", []),
            "warnings": readiness.get("warnings", []),
            "timestamp": readiness.get("timestamp"),
        },
        status_code=200 if verdict in {"pass", "partial"} else 503,
    )


async def horizon_metadata(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "name": "ARIFOS MCP",
            "version": "2026.04.26-KANON",
            "protocol": "MCP 2025-03-26",
            "gateway": {
                "type": "unified",
                "capabilities": ["tools", "prompts", "resources", "apps", "webmcp"],
                "surface": {
                    "registered": len(v2_tools_registered),
                    "constitutional": len(_constitutional_tool_names),
                    "probes": len(_probe_tool_names),
                },
                "tool_access": {
                    "public": PUBLIC_TOOLS,
                    "authenticated": AUTHENTICATED_TOOLS,
                    "sovereign_only": SOVEREIGN_TOOLS,
                },
            },
            "endpoints": {
                "mcp": "/mcp",
                "health": "/health",
                "ready": "/ready",
                "metadata": "/metadata",
                "tools": "/tools",
                "webmcp_discovery": "/.well-known/mcp",
            },
            "motto": "DITEMPA BUKAN DIBERI — Forged, Not Given",
        }
    )


async def webmcp_discovery(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "name": "arifOS WebMCP Gateway",
            "version": "v2026.04.26",
            "endpoints": {
                "health": "/health",
                "tools": "/tools",
                "execute": "/mcp",
                "metadata": "/metadata",
            },
            "capabilities": ["tools:list", "execute", "metadata"],
        }
    )


async def serve_humans_txt(request: Request) -> Response:
    content = (
        "/* TEAM */\n"
        "Sovereign: Arif Fazil\n"
        "Contact: arif@arif-fazil.com\n"
        "Site: https://arif-fazil.com\n\n"
        "/* THANKS */\n"
        "All contributors to the arifOS project\n\n"
        "/* SITE */\n"
        "Standards: MCP, FastMCP, Constitutional AI\n"
        "Components: FastAPI, Starlette, Pydantic\n\n"
        "DITEMPA BUKAN DIBERI — Forged, Not Given\n"
    )
    return Response(content=content, media_type="text/plain")


app: Any = None

try:
    if IS_FASTMCP_3:
        app = mcp.http_app(stateless_http=True)
    else:
        app = mcp._mcp_server.app

    if app is not None:
        # Define tools_with_meta before registration
        async def tools_with_meta(request: Request) -> JSONResponse:
            from arifosmcp.tool_manifest import TOOL_MANIFEST

            tool_summaries = []
            try:
                # Iterate over all providers (LocalProvider, AppProvider, etc.)
                for provider in mcp.providers:
                    # Access the internal _components map
                    # Some providers have it at the top level, others (like FastMCPApp) have it in _local
                    raw_components = getattr(provider, "_components", None)
                    if raw_components is None:
                        local = getattr(provider, "_local", None)
                        if local:
                            raw_components = getattr(local, "_components", None)

                    if not raw_components:
                        continue

                    raw_tools = {k: v for k, v in raw_components.items() if k.startswith("tool:")}

                    for name, tool in raw_tools.items():
                        tool_name = name.replace("tool:", "").rstrip("@")
                        base = {
                            "description": tool.description or "",
                            "parameters": tool.parameters or {},
                        }
                        manifest = TOOL_MANIFEST.get(tool_name, {})
                        meta_dict = getattr(tool, "meta", None) or {}
                        arifos_m = meta_dict.get("arifos_manifest", {}) or manifest
                        entry = {
                            "name": tool_name,
                            "description": base["description"],
                            "parameters": base["parameters"],
                            "stage": arifos_m.get("stage_code", ""),
                            "lane": arifos_m.get("lane", ""),
                            "meta": {
                                "arifos_manifest": arifos_m,
                                "stage_code": meta_dict.get(
                                    "stage_code", arifos_m.get("stage_code", "")
                                ),
                                "stage_name": meta_dict.get(
                                    "stage_name", arifos_m.get("stage_name", "")
                                ),
                                "risk_tier": meta_dict.get(
                                    "risk_tier", arifos_m.get("risk", {}).get("tier", "low")
                                ),
                                "irreversible": meta_dict.get(
                                    "irreversible",
                                    arifos_m.get("risk", {}).get("irreversible", False),
                                ),
                                "requires_human_ack": meta_dict.get(
                                    "requires_human_ack",
                                    arifos_m.get("risk", {}).get("requires_human_ack", False),
                                ),
                                "use_when": arifos_m.get("use_when", []),
                                "do_not_use_when": arifos_m.get("do_not_use_when", []),
                                "next_recommended_tools": arifos_m.get(
                                    "next_recommended_tools", []
                                ),
                                "authority_boundary": arifos_m.get("authority_boundary", {}),
                                "privacy_scope": arifos_m.get("privacy_scope", []),
                                "canonical_order": meta_dict.get(
                                    "canonical_order", arifos_m.get("canonical_order", [])
                                ),
                                "ui": meta_dict.get("ui", {}),
                            },
                        }
                        tool_summaries.append(entry)
            except Exception as e:
                logger.warning(f"Failed to build meta-enriched tools response: {e}")
                tool_summaries = []
            return JSONResponse({"tools": tool_summaries, "count": len(tool_summaries)})

        # Register REST routes: landing page (/), dashboard, developer, llms.txt, /status.json
        try:
            from arifosmcp.runtime.rest_routes import register_rest_routes
            from arifosmcp.runtime.tools import CANONICAL_TOOL_HANDLERS

            register_rest_routes(mcp, CANONICAL_TOOL_HANDLERS)
            logger.info(
                "REST routes registered: /, /dashboard, /developer, /llms.txt, /status.json"
            )
        except Exception:
            logger.exception(
                "REST route registration failed; /status.json unavailable — observability spine is DOWN"
            )

        # Federation Status Spine — added directly to avoid register_rest_routes import chain
        async def federation_status_json(request: Request) -> JSONResponse:
            """GET /status.json — Federation visibility spine.

            Probes arifOS, GEOX, WEALTH concurrently and returns a public-safe
            aggregated status payload. Shallow fields only — no latency_ms,
            exceptions, container names, env vars, or vault state.
            """
            from datetime import datetime, timezone

            import httpx

            _results: dict[str, Any] = {}
            _overall = "ok"

            async def _mcp_initialize(host: str, port: int, path: str = "/mcp") -> dict[str, Any]:
                url = f"http://{host}:{port}{path}"
                result: dict[str, Any] = {"ok": False, "error": None, "tools_count": None}
                try:
                    async with httpx.AsyncClient(timeout=6.0, follow_redirects=False) as client:
                        init_resp = await client.post(
                            url,
                            json={
                                "jsonrpc": "2.0",
                                "id": 1,
                                "method": "initialize",
                                "params": {
                                    "protocolVersion": "2025-03-26",
                                    "capabilities": {},
                                    "clientInfo": {"name": "arifOS-status-probe", "version": "1.0"},
                                },
                            },
                            headers={
                                "Content-Type": "application/json",
                                "Accept": "application/json, text/event-stream",
                            },
                        )
                        if init_resp.status_code == 200:
                            session_id = init_resp.headers.get("mcp-session-id", "")
                            result["ok"] = True
                            result["session_id"] = session_id[:16] + "..." if session_id else None
                            if session_id:
                                try:
                                    tools_resp = await client.post(
                                        url,
                                        json={
                                            "jsonrpc": "2.0",
                                            "id": 2,
                                            "method": "tools/list",
                                            "params": {},
                                        },
                                        headers={
                                            "Content-Type": "application/json",
                                            "Accept": "application/json",
                                            "mcp-session-id": session_id,
                                        },
                                        timeout=5.0,
                                    )
                                    if tools_resp.status_code == 200:
                                        td = tools_resp.json()
                                        if "result" in td and "tools" in td["result"]:
                                            result["tools_count"] = len(td["result"]["tools"])
                                except Exception:
                                    pass
                        else:
                            result["error"] = f"http_{init_resp.status_code}"
                except Exception as e:
                    result["error"] = type(e).__name__
                return result

            try:
                async with httpx.AsyncClient(timeout=8.0) as client:
                    probes = await asyncio.gather(
                        client.get("http://arifosmcp:8080/health", timeout=5.0),
                        client.get("http://arifosmcp:8080/ready", timeout=5.0),
                        client.get("http://wealth-organ:8000/health", timeout=5.0),
                        client.post(
                            "http://geox:8081/mcp",
                            json={
                                "jsonrpc": "2.0",
                                "id": 1,
                                "method": "initialize",
                                "params": {
                                    "protocolVersion": "2025-03-26",
                                    "capabilities": {},
                                    "clientInfo": {"name": "arifOS-status-probe", "version": "1.0"},
                                },
                            },
                            headers={
                                "Content-Type": "application/json",
                                "Accept": "application/json, text/event-stream",
                            },
                            timeout=6.0,
                        ),
                        return_exceptions=True,
                    )
                    arifos_h, arifos_r, wealth_h, geox_mcp = (
                        probes[0],
                        probes[1],
                        probes[2],
                        probes[3],
                    )

                    # arifOS
                    if isinstance(arifos_h, Exception):
                        _results["arifos"] = {"status": "down"}
                        _overall = "degraded"
                    elif arifos_h.status_code == 200:
                        _results["arifos"] = {
                            "status": "ok",
                            "health": "ok",
                            "ready": (
                                "ok"
                                if not isinstance(arifos_r, Exception)
                                and arifos_r.status_code == 200
                                else "unknown"
                            ),
                        }
                    else:
                        _results["arifos"] = {"status": "degraded"}
                        _overall = "degraded"

                    # WEALTH
                    if isinstance(wealth_h, Exception):
                        _results["wealth"] = {"status": "down"}
                        _overall = "degraded"
                    elif wealth_h.status_code == 200:
                        _results["wealth"] = {"status": "ok", "health": "ok"}
                    else:
                        _results["wealth"] = {"status": "degraded"}
                        _overall = "degraded"

                    # GEOX — MCP probe
                    if isinstance(geox_mcp, Exception):
                        _results["geox"] = {"status": "down"}
                        _overall = "degraded"
                    elif isinstance(geox_mcp, httpx.Response) and geox_mcp.status_code == 200:
                        sid = geox_mcp.headers.get("mcp-session-id", "")
                        tools = None
                        if sid:
                            try:
                                t = await client.post(
                                    "http://geox:8081/mcp",
                                    json={
                                        "jsonrpc": "2.0",
                                        "id": 2,
                                        "method": "tools/list",
                                        "params": {},
                                    },
                                    headers={
                                        "Content-Type": "application/json",
                                        "Accept": "application/json",
                                        "mcp-session-id": sid,
                                    },
                                    timeout=5.0,
                                )
                                if t.status_code == 200:
                                    td = t.json()
                                    if "result" in td and "tools" in td["result"]:
                                        tools = len(td["result"]["tools"])
                            except Exception:
                                pass
                        _results["geox"] = {
                            "status": "ok",
                            "mcp_probe": "ok",
                            "session_id": sid[:16] + "..." if sid else None,
                            "tools_count": tools,
                        }
                    else:
                        code = (
                            geox_mcp.status_code
                            if isinstance(geox_mcp, httpx.Response)
                            else "exception"
                        )
                        _results["geox"] = {"status": "degraded", "mcp_code": code}
                        _overall = "degraded"
            except Exception:
                _overall = "degraded"

            # Import here to avoid module-level import chain issues
            from arifosmcp.runtime.public_surface import public_surface

            ps = public_surface()
            payload = {
                "system": ps["system"],
                "status": _overall,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "canonical": ps["canonical"],
                "version": ps["version"],
                "commit": ps["commit"],
                "protocol_version": ps["protocol_version"],
                "services": {
                    "arifos": {
                        "role": "constitutional_kernel",
                        "mcp": True,
                        "endpoint": ps["canonical"]["mcp"],
                        "status": _results.get("arifos", {}).get("status", "unknown"),
                        "health": _results.get("arifos", {}).get("health", "unknown"),
                        "ready": _results.get("arifos", {}).get("ready", "unknown"),
                        "tools": 13,
                        "prompts": 8,
                        "resources": 5,
                    },
                    "geox": {
                        "role": "earth_intelligence_processor",
                        "mcp": True,
                        "endpoint": ps["canonical"]["mcp"].replace(
                            "mcp.arif-fazil.com", "geox.arif-fazil.com"
                        ),
                        "status": _results.get("geox", {}).get("status", "unknown"),
                        "mcp_probe": _results.get("geox", {}).get("mcp_probe", "unknown"),
                        "tools_count": _results.get("geox", {}).get("tools_count"),
                    },
                    "wealth": {
                        "role": "capital_intelligence_processor",
                        "mcp": True,
                        "endpoint": "https://wealth.arif-fazil.com/mcp",
                        "status": _results.get("wealth", {}).get("status", "unknown"),
                        "health": _results.get("wealth", {}).get("health", "unknown"),
                    },
                },
                "visibility": {"llms_txt": "ok", "well_known": "ok"},
                "seal": "DITEMPA BUKAN DIBERI",
            }
            return JSONResponse(payload, media_type="application/json")

        app.add_route("/status.json", federation_status_json, methods=["GET"])
        logger.info("/status.json route registered via app.add_route")

        app.add_middleware(GlobalPanicMiddleware)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=["X-API-Key", "Content-Type", "Authorization", "X-MCP-Protocol"],
        )
        app.add_route("/health", horizon_health, methods=["GET"])
        app.add_route("/ready", horizon_ready, methods=["GET"])
        app.add_route("/metadata", horizon_metadata, methods=["GET"])
        app.add_route("/humans.txt", serve_humans_txt, methods=["GET"])
        app.add_route("/.well-known/mcp", webmcp_discovery, methods=["GET"])

        # WebMCP Aliases
        app.add_route("/webmcp/health", horizon_health, methods=["GET"])
        app.add_route("/webmcp/tools", tools_with_meta, methods=["GET"])
        app.add_route("/webmcp/metadata", horizon_metadata, methods=["GET"])
        app.add_route("/webmcp/.well-known/mcp", webmcp_discovery, methods=["GET"])

        # Overwrite Starlette routes list with our prioritized meta-enriched /tools
        app.add_route("/tools", tools_with_meta, methods=["GET"])
        app.add_route("/health", horizon_health, methods=["GET"])
        app.add_route("/ready", horizon_ready, methods=["GET"])
        app.add_route("/metadata", horizon_metadata, methods=["GET"])
        app.add_route("/humans.txt", serve_humans_txt, methods=["GET"])
        app.add_route("/.well-known/mcp", webmcp_discovery, methods=["GET"])

        # WebMCP Aliases
        app.add_route("/webmcp/health", horizon_health, methods=["GET"])
        app.add_route("/webmcp/tools", tools_with_meta, methods=["GET"])
        app.add_route("/webmcp/metadata", horizon_metadata, methods=["GET"])
        app.add_route("/webmcp/.well-known/mcp", webmcp_discovery, methods=["GET"])
        logger.info("HTTP app configured with gateway endpoints + meta-enriched /tools")
    else:
        logger.warning("HTTP app is None")
except Exception as e:
    logger.error(f"Failed to setup HTTP app: {e}")


__all__ = ["mcp", "create_arifos_mcp_server", "app", "v2_tools_registered"]


def main() -> None:
    import asyncio

    import uvicorn

    async def run_server():
        print("=" * 60)
        print("ARIFOS MCP v2026.04.26-KANON — CANONICAL SURFACE")
        print("=" * 60)
        print(f"   Server: {mcp.name}")
        print(f"   Version: {mcp.version}")
        print(f"   Tools: {len(v2_tools_registered)}")
        print(f"   Prompts: {len(v2_prompts_registered)}")
        print(f"   Resources: {len(v2_resources_registered)}")
        print(f"   Apps: {len(v2_apps_registered)}")
        print("=" * 60)

        if app is None:
            print("HTTP app not available — falling back to mcp.run()")
            mcp.run()
            return

        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=int(os.getenv("ARIFOS_PORT", "8080")),
            timeout_graceful_shutdown=2,
            lifespan="on",
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
