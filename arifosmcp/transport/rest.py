"""
AAA MCP REST Bridge — HTTP REST API for OpenAI Tool Adapter
Maps HTTP POST /tools/{name} → MCP tool calls

Endpoints:
  GET  /                    → Service info (JSON) / landing page (HTML)
  GET  /health              → Health check with governance metrics
  GET  /ready               → Tool registry + dependencies ready
  GET  /version             → Build info (git sha, schema version)
  GET  /metrics             → Latency, timeouts, active sessions
  GET  /tools               → List available tools with schemas
  POST /tools/{tool_name}   → Call tool with JSON body (canonical + aliases)
  POST /apex_judge          → Full pipeline wrapper (000→333→666→888→999)
  GET/POST /mcp             → Unified Sovereign Connector alias

Usage:
  python -m arifosmcp.transport rest

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import asyncio
import inspect
import json
import os
import secrets
import sys
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route

from arifosmcp.transport.build_info import get_build_info
from arifosmcp.transport.integrations.self_ops import self_diagnose
from arifosmcp.transport.protocol.public_surface import PUBLIC_TOOL_ALIASES
from arifosmcp.transport.server import (
    anchor_session,
    apex_judge,
    audit_rules,
    check_vital,
    critique_thought,
    eureka_forge,
    fetch_content,
    ingest_evidence,
    inspect_file,
    metabolic_loop,
    reason_mind,
    seal_vault,
    search_reality,
    simulate_heart,
    vector_memory,
)
from core.shared.floor_audit import get_ml_floor_runtime

# Import tools from transport layer to keep REST bridge core-facing and adapter-agnostic.

# Build info
BUILD_INFO = get_build_info()

# Tool registry — exactly 13 canonical (L4) constitutional tools, sourced from AAA_CANONICAL_TOOLS.
TOOLS = {
    "anchor_session": anchor_session,
    "reason_mind": reason_mind,
    "vector_memory": vector_memory,
    "simulate_heart": simulate_heart,
    "critique_thought": critique_thought,
    "eureka_forge": eureka_forge,
    "apex_judge": apex_judge,
    "seal_vault": seal_vault,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "fetch_content": fetch_content,
    "inspect_file": inspect_file,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
    "metabolic_loop": metabolic_loop,
}

# Auxiliary (non-constitutional) tools — not part of the canonical 13.
# Dispatchable via /tools/{name} but excluded from the /tools listing.
AUXILIARY_TOOLS = {
    "self_diagnose": self_diagnose,
}

# Tool schemas with canonical UX names.
TOOL_SCHEMAS = {
    "anchor_session": {
        "description": "[Lane: Delta] 000_INIT — Session ignition + injection scan + authority check",
        "args": {
            "query": {"type": "string", "required": True},
            "actor_id": {"type": "string", "required": False, "default": "anonymous"},
            "auth_token": {"type": "string|null", "required": False, "default": None},
            "mode": {"type": "enum", "values": ["conscience", "ghost"], "default": "conscience"},
            "grounding_required": {"type": "boolean", "default": True},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "reason_mind": {
        "description": "[Lane: Delta] 111-444_AGI — SENSE→THINK→REASON with grounding",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "grounding": {"type": "array|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "vector_memory": {
        "description": "[Lane: Omega] 555_RECALL — Associative hybrid memory retrieval",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "depth": {"type": "integer", "default": 3},
            "domain": {
                "type": "enum",
                "values": ["canon", "manifesto", "docs", "all"],
                "default": "canon",
            },
            "debug": {"type": "boolean", "default": False},
        },
    },
    "simulate_heart": {
        "description": "[Lane: Omega] 555-666_ASI — Stakeholder impact + care constraints",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "stakeholders": {"type": "array|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "critique_thought": {
        "description": "[Lane: Omega] 666_ALIGN — 7-model bias critique",
        "args": {
            "session_id": {"type": "string", "required": True},
            "plan": {"type": "object", "required": True},
            "context": {"type": "string", "required": False, "default": ""},
        },
    },
    "apex_judge": {
        "description": "[Lane: Psi] 888_APEX_JUDGE — Sovereign verdict synthesis",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "agi_result": {"type": "object|null", "default": None},
            "asi_result": {"type": "object|null", "default": None},
            "proposed_verdict": {
                "type": "enum",
                "values": ["SEAL", "VOID", "PARTIAL", "SABAR", "888_HOLD"],
                "default": "SEAL",
            },
            "human_approve": {"type": "boolean", "default": False},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "eureka_forge": {
        "description": "[Lane: Psi] 777_EUREKA_FORGE — Sandboxed command execution with metabolic logging",
        "args": {
            "session_id": {"type": "string", "required": True},
            "command": {"type": "string", "required": True},
            "agent_id": {"type": "string", "default": "unknown"},
            "purpose": {"type": "string", "default": ""},
            "working_dir": {"type": "string", "default": "/root"},
            "timeout": {"type": "integer", "default": 60},
            "confirm_dangerous": {"type": "boolean", "default": False},
        },
    },
    "seal_vault": {
        "description": "[Lane: Psi] 999_VAULT — Immutable ledger seal with Amanah handshake",
        "args": {
            "session_id": {"type": "string", "required": True},
            "summary": {"type": "string", "required": True},
            "governance_token": {"type": "string", "required": True},
        },
    },
    "search_reality": {
        "description": "[Lane: Delta] Web grounding search (Perplexity/Brave)",
        "args": {
            "query": {"type": "string", "required": True},
            "intent": {"type": "string", "default": "general"},
        },
    },
    "ingest_evidence": {
        "description": "[Lane: Delta] Unified evidence ingestion — URL fetch or file inspect",
        "args": {
            "source_type": {"type": "enum", "values": ["url", "file"], "required": True},
            "target": {"type": "string", "required": True},
            "mode": {"type": "enum", "values": ["raw", "summary", "chunks"], "default": "raw"},
            "max_chars": {"type": "integer", "required": False, "default": 4000},
            "session_id": {"type": "string|null", "required": False, "default": None},
            "depth": {"type": "integer", "required": False, "default": 1},
            "include_hidden": {"type": "boolean", "required": False, "default": False},
            "pattern": {"type": "string", "required": False, "default": "*"},
            "min_size_bytes": {"type": "integer", "required": False, "default": 0},
            "max_files": {"type": "integer", "required": False, "default": 100},
        },
    },
    "fetch_content": {
        "description": "[Lane: Delta] Fetch URL content (legacy alias of ingest_evidence)",
        "args": {
            "id": {"type": "string", "required": True},
            "max_chars": {"type": "integer", "required": False, "default": 4000},
        },
    },
    "inspect_file": {
        "description": "[Lane: Delta] Inspect local files (legacy alias of ingest_evidence)",
        "args": {
            "path": {"type": "string", "required": False, "default": "."},
            "depth": {"type": "integer", "required": False, "default": 1},
            "include_hidden": {"type": "boolean", "required": False, "default": False},
            "pattern": {"type": "string", "required": False, "default": "*"},
            "min_size_bytes": {"type": "integer", "required": False, "default": 0},
            "max_files": {"type": "integer", "required": False, "default": 100},
        },
    },
    "audit_rules": {
        "description": "[Lane: Delta] Rule & governance audit checks",
        "args": {
            "audit_scope": {"type": "string", "default": "quick"},
            "verify_floors": {"type": "boolean", "default": True},
        },
    },
    "check_vital": {
        "description": "[Lane: Omega] System health & vital signs",
        "args": {
            "include_swap": {"type": "boolean", "required": False, "default": True},
            "include_io": {"type": "boolean", "required": False, "default": False},
            "include_temp": {"type": "boolean", "required": False, "default": False},
        },
    },
    "metabolic_loop": {
        "description": "[Lane: ALL] 000-999_LOOP — Full constitutional metabolic cycle (11-stage orchestration)",
        "args": {
            "query": {"type": "string", "required": True},
            "context": {"type": "string", "required": False, "default": ""},
            "risk_tier": {
                "type": "enum",
                "values": ["low", "medium", "high", "critical"],
                "default": "medium",
            },
            "actor_id": {"type": "string", "required": False, "default": "anonymous"},
            "use_sampling": {"type": "boolean", "default": True},
            "debug": {"type": "boolean", "default": False},
        },
    },
}

# Auxiliary tool schemas — non-constitutional tools excluded from the canonical /tools listing.
AUXILIARY_TOOL_SCHEMAS = {
    "self_diagnose": {
        "description": "SELF_OPS — Infrastructure health check (non-constitutional)",
        "args": {
            "base_url": {"type": "string|null", "required": False, "default": None},
        },
    },
}

TOOL_ALIASES = dict(PUBLIC_TOOL_ALIASES)

# ═══════════════════════════════════════════════════════
# AUTH (OPTIONAL) — Bearer token gate for REST bridge
# ═══════════════════════════════════════════════════════


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _required_bearer_token() -> str | None:
    # Prefer the canonical name used in docs.
    return os.getenv("ARIFOS_API_KEY") or os.getenv("ARIFOS_API_TOKEN")


def _auth_error_response(request: Request) -> JSONResponse | None:
    """
    Enforce Bearer auth when configured.
    """
    required = _required_bearer_token()
    if not required:
        return None
    if _env_truthy("ARIFOS_DEV_MODE"):
        return None

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            {"error": "invalid_request", "error_description": "Bearer token required"},
            status_code=401,
        )

    presented = auth_header[7:].strip()
    if not presented or not secrets.compare_digest(presented, required):
        return JSONResponse(
            {"error": "invalid_token", "error_description": "Invalid bearer token"},
            status_code=401,
        )
    return None


# ═══════════════════════════════════════════════════════
# TOOL DISPATCH
# ═══════════════════════════════════════════════════════


def _normalize_tool_name(raw_name: str | None) -> str:
    """Normalize tool path names to tolerate trailing slashes."""
    return (raw_name or "").strip().strip("/")


async def _execute_tool_call(
    incoming_tool_name: str,
    body: dict[str, Any],
    *,
    request_id: str,
    start_time: float,
) -> JSONResponse:
    original_name = incoming_tool_name
    tool_name = TOOL_ALIASES.get(incoming_tool_name, incoming_tool_name)

    # Add request_id for tracing
    body["request_id"] = request_id

    # Track metrics
    metrics.requests_total += 1
    metrics.requests_by_tool[original_name] = metrics.requests_by_tool.get(original_name, 0) + 1

    # Fast ACK logic
    if tool_name == "init_session" and body.get("fast_ack", False):
        session_id = body.get("actor_id", "anon") + "-" + uuid.uuid4().hex[:8]
        active_sessions[session_id] = {
            "started": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "status": "initializing",
        }
        return JSONResponse(
            {
                "status": "ack",
                "tool": original_name,
                "session_id": session_id,
                "request_id": request_id,
                "message": "Session initializing async",
            }
        )

    if tool_name not in TOOLS and tool_name not in AUXILIARY_TOOLS:
        metrics.errors += 1
        return JSONResponse(
            {"error": f"Tool '{original_name}' not found", "request_id": request_id},
            status_code=404,
        )

    tool = TOOLS.get(tool_name) or AUXILIARY_TOOLS[tool_name]

    try:
        actual_fn = getattr(tool, "fn", tool)
        sig = inspect.signature(actual_fn)
        param_names: list[str] = []
        has_kwargs = False
        for name, param in sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                has_kwargs = True
            else:
                param_names.append(name)

        filtered_body: dict[str, Any]
        if has_kwargs:
            filtered_body = body
        else:
            filtered_body = {k: v for k, v in body.items() if k in param_names}

        result = await asyncio.wait_for(actual_fn(**filtered_body), timeout=15.0)
    except asyncio.TimeoutError:
        metrics.timeouts += 1
        return JSONResponse(
            {
                "error": "INIT_TIMEOUT",
                "stage": "tool_execution",
                "request_id": request_id,
                "tool": original_name,
            },
            status_code=504,
        )

    latency_ms = (time.time() - start_time) * 1000
    metrics.latencies_ms.append(latency_ms)
    return JSONResponse(
        {
            "status": "success",
            "tool": original_name,
            "request_id": request_id,
            "latency_ms": round(latency_ms, 2),
            "result": result,
        }
    )


@dataclass
class Metrics:
    requests_total: int = 0
    requests_by_tool: dict[str, int] = field(default_factory=dict)
    latencies_ms: list[float] = field(default_factory=list)
    timeouts: int = 0
    errors: int = 0
    active_sessions: int = 0


metrics = Metrics()
active_sessions: dict[str, dict] = {}


def generate_request_id() -> str:
    return f"req-{uuid.uuid4().hex[:12]}"


WELCOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>arifOS MCP Server</title>
    <style>
        body { background: #050505; color: #e6c25d; font-family: 'JetBrains Mono', monospace; padding: 4rem; text-align: center; }
        .box { border: 1px solid #e6c25d33; padding: 2rem; display: inline-block; border-radius: 8px; background: #0a0a0a; }
        h1 { font-weight: 900; letter-spacing: -0.1rem; border-bottom: 2px solid #e6c25d; display: inline-block; padding-bottom: 0.5rem; }
        p { color: #888; max-width: 400px; margin: 1rem auto; }
        .status { color: #00ff88; font-weight: bold; margin-top: 2rem; border: 1px solid #00ff8833; padding: 0.5rem 1rem; border-radius: 50px; display: inline-block; }
        a { color: #00a2ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="box">
        <h1>arifOS MCP</h1>
        <p>This is a live <strong>Model Context Protocol</strong> server. 
           It is optimized for machine intelligence, but humans are welcome.</p>
        <div class="status">● ONLINE</div>
        <div style="margin-top: 2rem;">
            <a href="/tools">/tools</a> &nbsp;|&nbsp; 
            <a href="/health">/health</a> &nbsp;|&nbsp; 
            <a href="https://arifos.arif-fazil.com">documentation</a>
        </div>
    </div>
</body>
</html>
"""


async def route_info(request: Request):
    accept = request.headers.get("Accept", "")
    if "text/html" in accept:
        return HTMLResponse(WELCOME_HTML)

    return JSONResponse(
        {
            "service": "arifOS MCP Server",
            "version": BUILD_INFO["version"],
            "endpoints": [
                {"method": "GET", "path": "/", "description": "Service info"},
                {"method": "GET", "path": "/health", "description": "Health check"},
                {"method": "GET", "path": "/tools", "description": "List tools"},
                {"method": "POST", "path": "/tools/{tool_name}", "description": "Call tool"},
                {"method": "POST", "path": "/apex_judge", "description": "Full pipeline wrapper"},
            ],
            "tools": list(TOOL_SCHEMAS.keys()),
            "aliases": TOOL_ALIASES,
        }
    )


async def health(request: Request):
    from arifosmcp.transport.infrastructure.monitoring import (
        get_health_monitor,
        get_metrics_collector,
    )
    from arifosmcp.transport.protocol.aaa_contract import (
        AAA_CANONICAL_TOOLS,
        ARCHIVED_TOOLS,
        CANONICAL_TOOL_COUNT,
    )

    monitor = get_health_monitor()
    collector = get_metrics_collector()
    health_results = await monitor.check_all()
    stats = collector.get_stats()
    return JSONResponse(
        {
            "status": "healthy" if monitor.is_healthy() else "degraded",
            "version": BUILD_INFO["version"],
            "tools": {
                "canonical_tools_count": CANONICAL_TOOL_COUNT,
                "public": list(AAA_CANONICAL_TOOLS),
                "archived": sorted(ARCHIVED_TOOLS),
            },
            "ml_floors": get_ml_floor_runtime(),
            "governance_metrics": stats,
            "health_checks": health_results,
        }
    )


async def ready(request: Request):
    return JSONResponse({"ready": len(TOOLS) > 0})


async def version(request: Request):
    return JSONResponse(BUILD_INFO)


async def metrics_endpoint(request: Request):
    return JSONResponse({"requests_total": metrics.requests_total, "errors": metrics.errors})


async def well_known_mcp_server_json(request: Request):
    root_path = os.path.join(os.path.dirname(__file__), "..", "server.json")
    if os.path.exists(root_path):
        with open(root_path) as f:
            return JSONResponse(json.load(f))
    return JSONResponse({"error": "server.json not found"}, status_code=404)


async def list_tools(request: Request):
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    tool_list = [
        {"name": n, "description": s["description"], "args": s["args"]}
        for n, s in TOOL_SCHEMAS.items()
    ]
    return JSONResponse({"tools": tool_list, "count": len(tool_list)})


async def call_tool(request: Request):
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    request_id = generate_request_id()
    tool_name = _normalize_tool_name(request.path_params.get("tool_name"))
    start_time = time.time()
    try:
        body = await request.json()
    except:
        body = {}
    return await _execute_tool_call(tool_name, body, request_id=request_id, start_time=start_time)


async def sse_endpoint(request: Request):
    return JSONResponse({"error": "SSE_NOT_ENABLED"}, status_code=501)


async def messages_endpoint(request: Request):
    return JSONResponse({"error": "MESSAGES_NOT_ENABLED"}, status_code=501)


async def apex_judge_wrapper(request: Request):
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    request_id = generate_request_id()
    start_time = time.time()
    try:
        body = await request.json()
    except:
        body = {}

    query = body.get("query", "")
    actor_id = body.get("actor_id", "user")
    session_id = f"{actor_id}-{uuid.uuid4().hex[:8]}"

    # Minimal wrapper for DX
    try:
        res0 = await TOOLS["anchor_session"](query=query, actor_id=actor_id)
        cid = res0.get("session_id", session_id)
        res1 = await TOOLS["reason_mind"](query=query, session_id=cid)
        res2 = await TOOLS["simulate_heart"](query=query, session_id=cid)
        res3 = await TOOLS["apex_judge"](
            session_id=cid, query=query, agi_result=res1, asi_result=res2
        )

        return JSONResponse(
            {
                "status": "success",
                "request_id": request_id,
                "session_id": cid,
                "verdict": res3.get("verdict"),
                "pipeline": [
                    {"stage": "000_INIT", "result": res0},
                    {"stage": "111-333_AGI", "result": res1},
                    {"stage": "555-666_ASI", "result": res2},
                    {"stage": "888_APEX", "result": res3},
                ],
            }
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def mcp_alias(request: Request):
    if request.method == "GET":
        return await list_tools(request)
    return await call_tool(request)


routes = [
    Route("/", route_info, methods=["GET"]),
    Route("/.well-known/mcp/server.json", well_known_mcp_server_json, methods=["GET"]),
    Route("/mcp", mcp_alias, methods=["GET", "POST"]),
    Route("/mcp/", mcp_alias, methods=["GET", "POST"]),
    Route("/health", health, methods=["GET"]),
    Route("/ready", ready, methods=["GET"]),
    Route("/version", version, methods=["GET"]),
    Route("/metrics", metrics_endpoint, methods=["GET"]),
    Route("/tools", list_tools, methods=["GET"]),
    Route("/tools/", list_tools, methods=["GET"]),
    Route("/tools/{tool_name:path}", call_tool, methods=["POST"]),
    Route("/apex_judge", apex_judge_wrapper, methods=["POST"]),
    Route("/sse", sse_endpoint, methods=["GET", "POST"]),
    Route("/sse/", sse_endpoint, methods=["GET", "POST"]),
    Route("/messages", messages_endpoint, methods=["POST"]),
    Route("/{tool_name}", call_tool, methods=["POST"]),
]


@asynccontextmanager
async def lifespan(app):
    yield


app = Starlette(routes=routes, debug=False, lifespan=lifespan)


def main():
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"[rest] AAA MCP REST Bridge starting on {host}:{port}", file=sys.stderr)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
