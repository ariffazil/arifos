from __future__ import annotations
import os

from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from arifosmcp.mcp_server import mcp
from arifosmcp.prompts import PROMPTS
from arifosmcp.resources import RESOURCES
from arifosmcp.runtime.verify_arifos_tools import PRIMARY_METRIC_NAME, JSONL_PATH as VITALITY_JSONL, TSV_PATH as VITALITY_TSV

mcp_http_app = mcp.http_app(stateless_http=True)
app = FastAPI(lifespan=mcp_http_app.lifespan, title="arifosmcp NEXT HORIZON")
app.mount("/mcp", mcp_http_app)


def _public_base_url(request: Request) -> str:
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    host = request.headers.get("x-forwarded-host", request.headers.get("host", request.url.netloc))
    return f"{proto}://{host}".rstrip("/")


def _health_payload() -> dict:
    return {
        "status": "healthy",
        "service": "arifosmcp-next-horizon",
        "tools_loaded": len(PRIMARY_METRIC_NAME),
        "prompts_loaded": len(PROMPTS),
        "resources_loaded": len(RESOURCES),
        "entrypoint": "arifosmcp.mcp_server",
        "vitality": {
            "jsonl": str(VITALITY_JSONL),
            "tsv": str(VITALITY_TSV),
            "jsonl_exists": os.path.exists(VITALITY_JSONL),
            "tsv_exists": os.path.exists(VITALITY_TSV),
        },
    }


def _tools_payload() -> dict:
    return {
        "tools": [
            {"name": name, "primary_metric": PRIMARY_METRIC_NAME[name]}
            for name in sorted(PRIMARY_METRIC_NAME)
        ]
    }


def _prompts_payload() -> dict:
    return {"prompts": [{"name": name} for name in sorted(PROMPTS)]}


def _resources_payload() -> dict:
    return {"resources": [{"uri": uri} for uri in sorted(RESOURCES)]}


def _status_payload(request: Request) -> dict:
    health_payload = _health_payload()
    ok = health_payload["status"] == "healthy"
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_ok": ok,
        "health": health_payload,
        "manifest": {
            "base_url": _public_base_url(request),
            "tools_count": len(PRIMARY_METRIC_NAME),
            "prompts_count": len(PROMPTS),
            "resources_count": len(RESOURCES),
        },
        "trinity_matrix": {
            "overall_ok": ok,
            "delta": {
                "state": "HIDUP" if ok else "LEBUR",
                "detail": "health_ok · 1 reachable_endpoint" if ok else "status_api_unreachable · 0 reachable_endpoints",
            },
            "psi": {
                "state": "SEAL" if ok else "GANTUNG",
                "detail": (
                    f"manifest_ok · {len(RESOURCES)} verified_domains"
                    if ok
                    else "status_api_unreachable · 0 verified_domains"
                ),
            },
            "omega": {
                "state": "SELARAS" if ok else "SESAT",
                "detail": f"tool_surface_ok · {len(PRIMARY_METRIC_NAME)} tools" if ok else "status_api_unreachable · 0 tau",
            },
        },
        "tools": _tools_payload()["tools"],
        "prompts": _prompts_payload()["prompts"],
        "resources": _resources_payload()["resources"],
    }


@app.get("/")
async def root() -> dict:
    return {
        "service": "arifosmcp-next-horizon",
        "entrypoint": "arifosmcp.runtime.server:app",
        "mcp_path": "/mcp",
    }


@app.get("/health")
async def health() -> dict:
    return _health_payload()


@app.get("/tools")
async def tools() -> dict:
    return _tools_payload()


@app.get("/prompts")
async def prompts() -> dict:
    return _prompts_payload()


@app.get("/resources")
async def resources() -> dict:
    return _resources_payload()


@app.get("/api/tools")
async def api_tools() -> dict:
    return _tools_payload()


@app.get("/api/telemetry")
async def api_telemetry(request: Request) -> dict:
    payload = _status_payload(request)
    return {"timestamp": payload["timestamp"], "health": payload["health"], "trinity_matrix": payload["trinity_matrix"]}


@app.get("/api/status")
@app.get("/status")
async def api_status(request: Request) -> dict:
    return _status_payload(request)


@app.get("/.well-known/mcp/server.json")
async def well_known(request: Request) -> JSONResponse:
    base_url = _public_base_url(request)
    payload = {
        "name": "arifosmcp-next-horizon",
        "description": (
        f"Constitutional governance server — {len(PRIMARY_METRIC_NAME)} live runtime tools "
        "with NEXT HORIZON prompts and organ resources."
        ),
        "version": "v2026.04.19-UNIFIED",
        "protocolVersion": "2025-03-26",
        "url": f"{base_url}/mcp",
        "toolsEndpoint": f"{base_url}/tools",
        "promptsEndpoint": f"{base_url}/prompts",
        "resourcesEndpoint": f"{base_url}/resources",
        "tools": _tools_payload()["tools"],
        "prompts": _prompts_payload()["prompts"],
        "resources": _resources_payload()["resources"],
    }
    return JSONResponse(payload)
