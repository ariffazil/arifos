"""
arifOS MCP Server — Canonical Entry Point
═══════════════════════════════════════════

13-tool capability surface | internal ping/selftest | 13 Floors (F1–F13) | Trinity ΔΩΨ
FastMCP 3.2.0 + MCP Apps + Streamable HTTP
DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import asyncio
import inspect
import logging
import os
import sys
import traceback
from typing import Any


# ─── Path prioritization (runs before arifOS imports below) ─────────────────
# Defined at module level so ruff sees it as top-level; executed inside the
# _apply_path_priority() helper which is called after all stdlib imports.
def _prioritize_paths(*paths: str) -> None:
    for path in reversed(paths):
        if path in sys.path:
            sys.path.remove(path)
    for path in reversed(paths):
        sys.path.insert(0, path)


def _apply_path_priority() -> None:
    """Run path prioritization before arifOS package imports."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(project_root)
    parent_idx = sys.path.index(parent) if parent in sys.path else len(sys.path)
    project_root_idx = sys.path.index(project_root) if project_root in sys.path else len(sys.path)
    if parent not in sys.path or project_root not in sys.path or parent_idx > project_root_idx:
        _prioritize_paths(parent, project_root)


from dotenv import load_dotenv  # noqa: E402

_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(_env_path):
    load_dotenv(_env_path, override=True)

# Fix sys.path so arifOS packages resolve correctly inside Docker
_apply_path_priority()

import fastmcp  # noqa: E402
from arifosmcp.constitutional_map import (  # noqa: E402
    CANONICAL_TOOLS,
    list_authenticated_tools,
    list_canonical_tools,
    list_constitutional_tools,
    list_probe_tools,
    list_public_tools,
    list_sovereign_tools,
)
from fastmcp import FastMCP  # noqa: E402
from starlette.middleware.base import BaseHTTPMiddleware  # noqa: E402
from starlette.middleware.cors import CORSMiddleware  # noqa: E402
from starlette.requests import Request  # noqa: E402
from starlette.responses import JSONResponse, Response  # noqa: E402

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


# ─── Deployment Identity ─────────────────────────────────────────────────────
# Resolved at import time:
#   1. From environment variables (set at docker build via --build-arg)
#   2. Fallback to git commands (host/developer)
# These are the single source of truth for what code is actually running.
# All /health responses MUST agree.
def _get_git_info() -> tuple[str, str, str]:
    import subprocess

    # 1. Try env vars first (container runtime — set by docker build)
    commit = os.environ.get("DEPLOY_GIT_COMMIT", "").strip()
    branch = os.environ.get("DEPLOY_GIT_BRANCH", "").strip()
    build_time = os.environ.get("DEPLOY_BUILD_TIME", "").strip()
    if commit:
        return commit, branch, build_time
    # 2. Fallback: run git commands (host/developer)
    try:
        cwd = os.path.dirname(os.path.abspath(__file__))
        commit = (
            subprocess.check_output(  # nosec: B603 -- git is intentional, no user input
                ["git", "describe", "--always", "--long"],
                stderr=subprocess.DEVNULL,
                cwd=cwd,
            )
            .decode()
            .strip()
        )
        branch = (
            subprocess.check_output(  # nosec: B603 -- git is intentional, no user input
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL,
                cwd=cwd,
            )
            .decode()
            .strip()
        )
        build_time = (
            subprocess.check_output(  # nosec: B603 -- git is intentional, no user input
                ["git", "log", "-1", "--format=%ci"],
                stderr=subprocess.DEVNULL,
                cwd=cwd,
            )
            .decode()
            .strip()
        )
        return commit, branch, build_time
    except Exception:
        return "unknown", "unknown", "unknown"


_DEPLOY_GIT_COMMIT, _DEPLOY_GIT_BRANCH, _DEPLOY_BUILD_TIME = _get_git_info()
_DEPLOY_VERSION = f"kanon-{_DEPLOY_GIT_COMMIT}"


mcp = FastMCP(
    "ARIFOS MCP",
    version=f"kanon-{_DEPLOY_GIT_COMMIT}",
    website_url="https://arifosmcp.arif-fazil.com",
    instructions=(
        "Constitutional AI orchestration kernel — arifOS.\n\n"
        "Golden path: init → sense → mind → heart → judge → vault\n\n"
        "Runtime surface: 13 public capability tools.\n"
        f"Tools (arif_noun_verb):\n  {_canonical_tool_names_text}\n\n"
        "DITEMPA BUKAN DIBERI — Forged, Not Given"
    ),
)

_engineering_lock_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".ENGINEERING_LOCK"
)
if not os.path.exists(_engineering_lock_path):
    logger.warning("Engineering lock missing at startup: %s", _engineering_lock_path)


def create_arifos_mcp_server() -> FastMCP:
    return mcp


def _assert_registered_surface(registered_names: list[str]) -> None:
    registered_set = set(registered_names)
    expected_set = set(CANONICAL_TOOLS)

    if len(registered_names) != len(expected_set):
        raise RuntimeError(
            f"Surface drift: expected {len(expected_set)} tools, got {len(registered_names)}"
        )

    if any(name.startswith("arifos_") for name in registered_names):
        raise RuntimeError("Legacy surface detected in registered MCP tools")

    if registered_set != expected_set:
        missing = sorted(expected_set - registered_set)
        extra = sorted(registered_set - expected_set)
        raise RuntimeError(
            f"Ontology mismatch detected: missing={missing or '[]'} extra={extra or '[]'}"
        )


v2_tools_registered: list[str] = []
v2_prompts_registered: list[str] = []
v2_resources_registered: list[str] = []
v2_apps_registered: list[str] = []

IS_FASTMCP_3 = fastmcp.__version__.startswith("3")


# ── FAIL-CLOSED HARDENED DISPATCH ───────────────────────────────────────────
def _wrap_hardened_dispatch(tool_name: str, original_handler: Any) -> Any:
    """Wrap a tool handler with transport-level floor enforcement."""
    import functools

    async def _invoke_original(arguments: dict[str, Any]) -> Any:
        result = original_handler(**arguments)
        if inspect.isawaitable(result):
            result = await result
        if hasattr(result, "model_dump"):
            return result.model_dump(mode="json")
        return result

    try:
        sig = inspect.signature(original_handler)
    except Exception:

        async def fallback_handler(req: dict[str, Any]):
            return await _invoke_original(req)

        return fallback_handler

    @functools.wraps(original_handler)
    async def wrapper(**kwargs):
        from arifosmcp.core.floors import check_floors

        bound = sig.bind(**kwargs)
        bound.apply_defaults()
        args = dict(bound.arguments)

        session_id = args.get("session_id") or os.environ.get("ARIFOS_SESSION_ID")  # noqa: F841
        actor_id = args.get("actor_id") or os.environ.get("ARIFOS_ACTOR_ID")

        floor_result = check_floors(
            tool_name=tool_name,
            params=args,
            actor_id=actor_id,
        )
        if floor_result["verdict"] != "SEAL":
            return {
                "verdict": floor_result["verdict"],
                "tool": tool_name,
                "failed_floors": floor_result.get("failed_floors", []),
                "reason": floor_result.get("reason", "Floor breach"),
                "action": "HOLD" if floor_result["verdict"] == "HOLD" else "VOID",
            }

        return await _invoke_original(args)

    return wrapper


try:
    from arifosmcp.prompts import CANONICAL_PROMPTS, register_prompts
    from arifosmcp.resources import CANONICAL_RESOURCES, register_resources
    from arifosmcp.runtime.tools import _CANONICAL_HANDLERS, register_tools

    HARDENED_HANDLERS = {
        name: _wrap_hardened_dispatch(name, handler)
        for name, handler in _CANONICAL_HANDLERS.items()
    }
    _CANONICAL_HANDLERS.clear()
    _CANONICAL_HANDLERS.update(HARDENED_HANDLERS)

    v2_tools_registered = register_tools(mcp)
    _assert_registered_surface(v2_tools_registered)
    v2_prompts_registered = register_prompts(mcp)
    if tuple(v2_prompts_registered) != CANONICAL_PROMPTS:
        raise RuntimeError(
            f"Prompt drift: expected {list(CANONICAL_PROMPTS)}, got {v2_prompts_registered}"
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


# ── MCP Apps registration — STABILIZED ──────────────────────────────────────
_safe_register(mcp, "arifosmcp.apps.command_center.app", "command_center")
# ─────────────────────────────────────────────────────────────────────────────

PUBLIC_TOOLS = list_public_tools()
AUTHENTICATED_TOOLS = list_authenticated_tools()
SOVEREIGN_TOOLS = list_sovereign_tools()


async def horizon_health(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "healthy",
            "service": "arifos-mcp-kanon",
            "version": _DEPLOY_VERSION,
            "git_commit": _DEPLOY_GIT_COMMIT,
            "git_branch": _DEPLOY_GIT_BRANCH,
            "build_time": _DEPLOY_BUILD_TIME,
            "gateway": "unified",
            "tools": len(_constitutional_tool_names),  # canonical pipeline only
            "prompts": len(v2_prompts_registered),
            "resources": len(v2_resources_registered),
            "apps": len(v2_apps_registered),
            "canonical_surface": len(_constitutional_tool_names),
            "probe_surface": len(_probe_tool_names),
            "registered_surface": len(v2_tools_registered),  # includes infra
            "infra_tools": [t for t in v2_tools_registered if t not in _constitutional_tool_names],
            "timestamp": __import__("datetime")
            .datetime.now(__import__("datetime").timezone.utc)
            .isoformat(),
        },
        headers={
            "X-Deployment-Hash": _DEPLOY_GIT_COMMIT,
            "X-Build-Time": _DEPLOY_BUILD_TIME,
            "X-Git-Branch": _DEPLOY_GIT_BRANCH,
        },
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
            "version": f"kanon-{_DEPLOY_GIT_COMMIT}",
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
            "version": f"kanon-{_DEPLOY_GIT_COMMIT}",
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
        # stateless_http=True causes FastMCP 3.2 to return None here.
        # mcp.http_app() (no args) correctly returns StarletteWithLifespan.
        app = mcp.http_app()
        if app is None:
            raise RuntimeError(
                "FastMCP HTTP app unavailable — refusing mcp.run() fallback "
                "because custom REST routes would be bypassed."
            )
    else:
        app = mcp._mcp_server.app
        if app is None:
            raise RuntimeError("FastMCP ASGI app unavailable and _mcp_server.app is None.")

    # Register custom REST routes onto the ASGI app — always, not conditionally
    # mcp.http_app() returns a separate StarletteWithLifespan instance (the Uvicorn app).
    # Routes must be registered on THAT app, not on the mcp object.
    try:
        from arifosmcp.runtime.rest_routes import register_rest_routes
        from arifosmcp.runtime.tools import CANONICAL_TOOL_HANDLERS

        register_rest_routes(app, CANONICAL_TOOL_HANDLERS)
        logger.info(
            "REST routes registered on ASGI app: /, /dashboard, /tools, /tools.json, "
            "/constitution -> /api/constitution, /mcp/*"
        )

        # Mount /constitution as public path (redirect to /api/constitution)
        from starlette.responses import RedirectResponse as _ConstitutionRedirect

        @app.route("/constitution", methods=["GET"])
        async def constitution_public(_request: Request) -> _ConstitutionRedirect:
            return _ConstitutionRedirect(url="/api/constitution", status_code=307)

    except Exception:
        logger.exception("REST route registration failed — observability spine DOWN")
        raise  # fail closed — do not silently continue

        # Define tools_with_meta before registration
        async def tools_with_meta(request: Request) -> JSONResponse:
            from arifosmcp.constitutional_map import CANONICAL_TOOLS
            from arifosmcp.tool_manifest import TOOL_MANIFEST

            tool_summaries = []
            try:
                # Iterate over all providers (LocalProvider, AppProvider, etc.)
                for provider in mcp.providers:
                    # Access internal _components map — top-level or _local depending on provider
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
                        # ── Surface lock: only 13 canonical tools + command_center app ──
                        # arif_cc_* aliases are internal CC compat tools — exclude entirely
                        # command_center is the app surface — include
                        if tool_name.startswith("arif_cc_"):
                            continue
                        if tool_name not in CANONICAL_TOOLS and tool_name != "command_center":
                            continue
                        tool_summaries.append(entry)
            except Exception as e:
                logger.warning(f"Failed to build meta-enriched tools response: {e}")
                tool_summaries = []
            return JSONResponse({"tools": tool_summaries, "count": len(tool_summaries)})

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
        print(f"ARIFOS MCP kanon-{_DEPLOY_GIT_COMMIT} — CANONICAL SURFACE")
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
            host="0.0.0.0",  # noqa: B104 — intentional: Docker service must bind all interfaces
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
