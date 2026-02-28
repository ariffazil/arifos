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
  python -m aaa_mcp rest

DITEMPA BUKAN DIBERI
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
from starlette.responses import HTMLResponse, JSONResponse, StreamingResponse
from starlette.routing import Route

from aaa_mcp.integrations.self_ops import self_diagnose
from aaa_mcp.protocol.public_surface import PUBLIC_TOOL_ALIASES

# Import all 13 canonical tools from server module.
# Legacy verbs are supported via HTTP aliases only.
from arifos_aaa_mcp.server import (
    anchor_session,
    audit_rules,
    check_vital,
    critique_thought,
    fetch_content,
    eureka_forge,
    inspect_file,
    apex_judge,
    reason_mind,
    recall_memory,
    seal_vault,
    search_reality,
    simulate_heart,
)

# Build info
BUILD_INFO = {
    "version": "2026.02.23-CANONICAL-13",
    "schema_version": "2026.02.23-CANONICAL-13",
    "git_sha": os.environ.get("GIT_SHA", "unknown"),
    "build_time": os.environ.get("BUILD_TIME", datetime.now(timezone.utc).isoformat()),
}

# Tool registry — canonical UX names as primary keys.
TOOLS = {
    "anchor_session": anchor_session,
    "reason_mind": reason_mind,
    "recall_memory": recall_memory,
    "simulate_heart": simulate_heart,
    "critique_thought": critique_thought,
    "apex_judge": apex_judge,
    "eureka_forge": eureka_forge,
    "seal_vault": seal_vault,
    "search_reality": search_reality,
    "fetch_content": fetch_content,
    "inspect_file": inspect_file,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
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
    "recall_memory": {
        "description": "[Lane: Omega] 555_RECALL — Associative memory retrieval",
        "args": {
            "current_thought_vector": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
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
        "description": "[Lane: Psi] 777_EUREKA_FORGE — Sandboxed action execution with sovereign gating",
        "args": {
            "action_payload": {"type": "object", "required": True},
            "signed_tensor": {"type": "object", "required": True},
            "execution_context": {"type": "object", "required": True},
            "signature": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "idempotency_key": {"type": "string", "required": True},
            "ratification_token": {"type": "string|null", "required": False, "default": None},
        },
    },
    "seal_vault": {
        "description": "[Lane: Psi] 999_VAULT — Immutable ledger seal",
        "args": {
            "session_id": {"type": "string", "required": True},
            "summary": {"type": "string", "required": True},
            "verdict": {
                "type": "enum",
                "values": ["SEAL", "VOID", "PARTIAL", "SABAR", "888_HOLD"],
                "default": "SEAL",
            },
        },
    },
    "search_reality": {
        "description": "[Lane: Delta] Web grounding search (Perplexity/Brave)",
        "args": {
            "query": {"type": "string", "required": True},
            "intent": {"type": "string", "default": "general"},
        },
    },
    "fetch_content": {
        "description": "[Lane: Delta] Raw evidence content retrieval by URL",
        "args": {
            "id": {"type": "string", "required": True},
            "max_chars": {"type": "integer", "default": 4000},
        },
    },
    "inspect_file": {
        "description": "[Lane: Delta] Filesystem inspection (read-only)",
        "args": {
            "session_id": {"type": "string", "required": True},
            "path": {"type": "string", "required": True},
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
            "session_id": {"type": "string", "required": True},
        },
    },
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

    - If `ARIFOS_API_KEY` (or `ARIFOS_API_TOKEN`) is unset → allow all (local dev default).
    - If `ARIFOS_DEV_MODE=true` → bypass (explicit local-only override).
    - Otherwise require `Authorization: Bearer <token>` matching the configured token.
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


async def _execute_tool_call(
    incoming_tool_name: str,
    body: dict[str, Any],
    *,
    request_id: str,
    start_time: float,
) -> JSONResponse:
    original_name = incoming_tool_name
    tool_name = TOOL_ALIASES.get(incoming_tool_name, incoming_tool_name)

    # Add request_id for tracing (ChatGPT feedback: request_id correlation)
    body["request_id"] = request_id

    # Track metrics
    metrics.requests_total += 1
    metrics.requests_by_tool[original_name] = metrics.requests_by_tool.get(original_name, 0) + 1

    # Fast ACK for init_session (ChatGPT feedback: return fast ACK <200ms)
    if tool_name == "init_session" and body.get("fast_ack", False):
        session_id = body.get("actor_id", "anon") + "-" + uuid.uuid4().hex[:8]
        active_sessions[session_id] = {
            "started": datetime.utcnow().isoformat(),
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

    if tool_name not in TOOLS:
        metrics.errors += 1
        return JSONResponse(
            {"error": f"Tool '{original_name}' not found", "request_id": request_id},
            status_code=404,
        )

    tool = TOOLS[tool_name]

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

        result = await asyncio.wait_for(actual_fn(**filtered_body), timeout=10.0)
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


# Metrics tracking (ChatGPT feedback: observability)
@dataclass
class Metrics:
    requests_total: int = 0
    requests_by_tool: dict[str, int] = field(default_factory=dict)
    latencies_ms: list[float] = field(default_factory=list)
    timeouts: int = 0
    errors: int = 0
    active_sessions: int = 0


metrics = Metrics()

# Active sessions tracking
active_sessions: dict[str, dict] = {}


def generate_request_id() -> str:
    """Generate unique request ID for tracing (ChatGPT feedback: request_id correlation)."""
    return f"req-{uuid.uuid4().hex[:12]}"


# --- HUMANS WELCOME ---
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
    """Root landing: HTML for humans, JSON for operators."""
    accept = request.headers.get("Accept", "")
    if "text/html" in accept:
        return HTMLResponse(WELCOME_HTML)

    return JSONResponse(
        {
            "service": "arifOS MCP Server",
            "version": BUILD_INFO["version"],
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/",
                    "description": "Service info (JSON) / landing page (HTML)",
                },
                {
                    "method": "GET",
                    "path": "/.well-known/mcp/server.json",
                    "description": "MCP discovery (optional)",
                },
                {"method": "GET", "path": "/health", "description": "Health check"},
                {
                    "method": "GET",
                    "path": "/ready",
                    "description": "Readiness (tools + schemas loaded)",
                },
                {"method": "GET", "path": "/version", "description": "Build info"},
                {"method": "GET", "path": "/metrics", "description": "Operational metrics"},
                {"method": "GET", "path": "/tools", "description": "List tools with schemas"},
                {
                    "method": "POST",
                    "path": "/tools/{tool_name}",
                    "description": "Call tool (canonical + aliases)",
                },
                {"method": "POST", "path": "/apex_judge", "description": "Full pipeline wrapper"},
                {"method": "GET", "path": "/sse", "description": "MCP SSE transport"},
                {
                    "method": "POST",
                    "path": "/mcp",
                    "description": "Unified MCP alias (Sovereign Connector)",
                },
            ],
            "tools": list(TOOL_SCHEMAS.keys()),
            "aliases": TOOL_ALIASES,
        }
    )


async def health(request: Request):
    """Health check endpoint with governance metrics."""
    from aaa_mcp.infrastructure.monitoring import get_health_monitor, get_metrics_collector

    monitor = get_health_monitor()
    collector = get_metrics_collector()

    health_results = await monitor.check_all()
    stats = collector.get_stats()

    return JSONResponse(
        {
            "status": "healthy" if monitor.is_healthy() else "degraded",
            "service": "aaa-mcp-rest",
            "version": BUILD_INFO["version"],
            "governance_metrics": stats,
            "health_checks": health_results,
        }
    )


async def ready(request: Request):
    """Readiness check — tool registry loaded (ChatGPT feedback: /ready endpoint)."""
    try:
        tools_loaded = len(TOOLS)
        schemas_loaded = len(TOOL_SCHEMAS)
        return JSONResponse(
            {
                "ready": tools_loaded > 0 and schemas_loaded > 0,
                "tools_loaded": tools_loaded,
                "schemas_loaded": schemas_loaded,
                "tool_names": list(TOOLS.keys()),
            }
        )
    except Exception as e:
        return JSONResponse({"ready": False, "error": str(e)}, status_code=503)


async def version(request: Request):
    """Build version info (ChatGPT feedback: /version endpoint)."""
    return JSONResponse(BUILD_INFO)


async def metrics_endpoint(request: Request):
    """Metrics endpoint with v65.0 governance support."""
    from aaa_mcp.infrastructure.monitoring import get_metrics_collector

    collector = get_metrics_collector()
    stats = collector.get_stats()

    # Legacy compatibility
    avg_latency = (
        sum(metrics.latencies_ms) / len(metrics.latencies_ms) if metrics.latencies_ms else 0
    )

    return JSONResponse(
        {
            "requests_total": stats.get("total_executions", 0) + metrics.requests_total,
            "avg_latency_ms": stats.get("avg_latency_ms", round(avg_latency, 2)),
            "governance_stats": stats,
            "legacy_stats": {
                "requests_by_tool": metrics.requests_by_tool,
                "timeouts": metrics.timeouts,
                "errors": metrics.errors,
                "active_sessions": len(active_sessions),
            },
        }
    )


async def well_known_mcp_server_json(request: Request):
    """Serve MCP server.json for registry auto-discovery.

    Endpoint: /.well-known/mcp/server.json
    Used by MCP Registry for automatic server discovery and updates.
    """
    try:
        # Try static directory first (for production deployments)
        static_path = os.path.join(
            os.path.dirname(__file__), "..", "static", ".well-known", "mcp", "server.json"
        )
        # Fallback to repo root (for development)
        root_path = os.path.join(os.path.dirname(__file__), "..", "server.json")

        if os.path.exists(static_path):
            with open(static_path) as f:
                content = json.load(f)
        elif os.path.exists(root_path):
            with open(root_path) as f:
                content = json.load(f)
        else:
            return JSONResponse({"error": "server.json not found"}, status_code=404)

        return JSONResponse(content)
    except Exception as e:
        return JSONResponse({"error": f"Failed to load server.json: {str(e)}"}, status_code=500)


async def list_tools(request: Request):
    """List available MCP tools with schemas."""
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    tool_list = []
    for name, schema in TOOL_SCHEMAS.items():
        tool_list.append(
            {
                "name": name,
                "description": schema["description"],
                "args": schema["args"],
            }
        )
    return JSONResponse({"tools": tool_list, "count": len(tool_list)})


async def call_tool(request: Request):
    """Call an MCP tool via HTTP POST with fast ACK pattern (ChatGPT feedback)."""
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    request_id = generate_request_id()
    tool_name = request.path_params.get("tool_name")
    start_time = time.time()

    # Map classic tool names
    original_name = tool_name

    try:
        body = await request.json()
    except Exception:
        body = {}

    try:
        if not isinstance(original_name, str) or not original_name.strip():
            metrics.errors += 1
            return JSONResponse(
                {"error": "Tool name required", "request_id": request_id},
                status_code=400,
            )

        if not isinstance(body, dict):
            body = {}

        return await _execute_tool_call(
            original_name,
            body,
            request_id=request_id,
            start_time=start_time,
        )
    except Exception as e:
        metrics.errors += 1
        return JSONResponse(
            {"error": str(e), "tool": original_name, "request_id": request_id}, status_code=500
        )


async def sse_endpoint(request: Request):
    """
    Compatibility SSE endpoint for the REST bridge.

    Production SSE transport is provided by FastMCP (`python -m aaa_mcp sse`) and should be
    routed directly (e.g., via Traefik/Nginx) when needed.
    """
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    accept = request.headers.get("Accept", "")
    if "text/event-stream" in accept:

        async def _stream():
            yield "event: error\ndata: REST bridge SSE not enabled; use FastMCP SSE transport\n\n"

        return StreamingResponse(_stream(), media_type="text/event-stream")

    return JSONResponse(
        {
            "error": "SSE_NOT_ENABLED",
            "message": "REST bridge SSE is a compatibility stub. Use FastMCP SSE transport instead.",
        },
        status_code=501,
    )


async def messages_endpoint(request: Request):
    """Compatibility JSON-RPC endpoint stub for MCP clients."""
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    return JSONResponse(
        {
            "error": "MESSAGES_NOT_ENABLED",
            "message": "Use POST /mcp for the unified connector, or FastMCP HTTP transport.",
        },
        status_code=501,
    )


async def apex_judge_wrapper(request: Request):
    """
    Full pipeline wrapper — 000→333→666→888→999 (ChatGPT feedback: DX win).
    Orchestrates complete Trinity pipeline in one call.
    """
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    request_id = generate_request_id()
    start_time = time.time()

    try:
        body = await request.json()
    except Exception:
        body = {}

    query = body.get("query", "")
    actor_id = body.get("actor_id", "user")
    auto_seal = body.get("auto_seal", False)

    session_id = f"{actor_id}-{uuid.uuid4().hex[:8]}"

    pipeline_results = {
        "request_id": request_id,
        "session_id": session_id,
        "pipeline": [],
    }

    try:
        # Stage 1: INIT (000)
        init_tool = TOOLS["anchor_session"]
        init_fn = getattr(init_tool, "fn", init_tool)
        init_result = await init_fn(query=query, actor_id=actor_id)
        pipeline_results["pipeline"].append({"stage": "000_INIT", "result": init_result})

        canonical_session_id = init_result.get("session_id", session_id)
        pipeline_results["session_id"] = canonical_session_id

        # Stage 2: AGI (111-444)
        agi_tool = TOOLS["reason_mind"]
        agi_fn = getattr(agi_tool, "fn", agi_tool)
        agi_result = await agi_fn(
            query=query,
            session_id=canonical_session_id,
            grounding=body.get("grounding"),
        )
        pipeline_results["pipeline"].append({"stage": "111-444_AGI", "result": agi_result})

        # Stage 2.5: PHOENIX (555)
        phoenix_tool = TOOLS["recall_memory"]
        phoenix_fn = getattr(phoenix_tool, "fn", phoenix_tool)
        phoenix_result = await phoenix_fn(
            current_thought_vector=query,
            session_id=canonical_session_id,
        )
        pipeline_results["pipeline"].append({"stage": "555_RECALL", "result": phoenix_result})

        # Stage 3: ASI (666)
        asi_tool = TOOLS["simulate_heart"]
        asi_fn = getattr(asi_tool, "fn", asi_tool)
        asi_result = await asi_fn(
            query=query, session_id=canonical_session_id, stakeholders=body.get("stakeholders", [])
        )
        pipeline_results["pipeline"].append({"stage": "666_ASI", "result": asi_result})

        # Stage 4: APEX (888)
        apex_tool = TOOLS["apex_judge"]
        apex_fn = getattr(apex_tool, "fn", apex_tool)
        apex_result = await apex_fn(
            session_id=canonical_session_id,
            query=query,
            implementation_details={
                "source": "rest_apex_judge",
                "agi": agi_result,
                "asi": asi_result,
            },
            proposed_verdict="SEAL",
            human_approve=body.get("human_approve", False),
        )
        pipeline_results["pipeline"].append({"stage": "888_APEX", "result": apex_result})

        # Stage 4.5: FORGE (888_ACTUATE)
        if apex_result.get("verdict") == "SEAL":
            forge_tool = TOOLS["eureka_forge"]
            forge_fn = getattr(forge_tool, "fn", forge_tool)
            forge_result = await forge_fn(
                action_payload=body.get("action_payload", {}),
                signed_tensor=apex_result.get("payload", {}),
                execution_context=body.get("execution_context", {}),
                signature=body.get("signature", ""),
                session_id=canonical_session_id,
                idempotency_key=request_id,
            )
            pipeline_results["pipeline"].append(
                {"stage": "777_EUREKA_FORGE", "result": forge_result}
            )

        # Stage 5: VAULT (999) — optional
        if auto_seal:
            seal_tool = TOOLS["seal_vault"]
            seal_fn = getattr(seal_tool, "fn", seal_tool)
            governance_token = str(apex_result.get("governance_token", ""))
            seal_result = await seal_fn(
                session_id=canonical_session_id,
                summary=query[:100],
                governance_token=governance_token,
            )
            pipeline_results["pipeline"].append({"stage": "999_VAULT", "result": seal_result})
        latency_ms = (time.time() - start_time) * 1000
        pipeline_results["latency_ms"] = round(latency_ms, 2)
        pipeline_results["verdict"] = apex_result.get("verdict", init_result.get("verdict", "SEAL"))

        return JSONResponse(
            {
                "status": "success",
                "tool": "apex_judge",
                "request_id": request_id,
                "result": pipeline_results,
            }
        )
    except Exception as e:
        metrics.errors += 1
        return JSONResponse(
            {"error": str(e), "tool": "apex_judge", "request_id": request_id}, status_code=500
        )


async def mcp_alias(request: Request):
    """
    Unified /mcp endpoint (ChatGPT Sovereign Connector).
    Handles both direct tool calls and MCP protocol detection.
    """
    auth_error = _auth_error_response(request)
    if auth_error:
        return auth_error
    # Detect if it's an MCP SSE request
    accept = request.headers.get("Accept", "")
    if request.method == "GET" and ("text/event-stream" in accept or "application/json" in accept):
        # If it's a GET, return tool list or SSE entry based on Accept header
        if "text/event-stream" in accept:
            from aaa_mcp.rest import sse_endpoint

            return await sse_endpoint(request)
        return await list_tools(request)

    # If it's a POST, it might be an MCP message or a direct tool call
    try:
        body = await request.json()
        if isinstance(body, dict) and "tool" in body:
            request_id = generate_request_id()
            start_time = time.time()
            tool = str(body.get("tool", "")).strip()
            args = body.get("arguments") or {}
            if not tool:
                metrics.errors += 1
                return JSONResponse(
                    {"error": "Tool name required", "request_id": request_id},
                    status_code=400,
                )
            if not isinstance(args, dict):
                metrics.errors += 1
                return JSONResponse(
                    {"error": "Tool arguments must be an object", "request_id": request_id},
                    status_code=400,
                )
            return await _execute_tool_call(
                tool,
                args,
                request_id=request_id,
                start_time=start_time,
            )
        if "method" in body and "params" in body:
            from aaa_mcp.rest import messages_endpoint

            return await messages_endpoint(request)
    except Exception:
        pass

    # Default to direct tool call if it's a POST to /mcp
    return await call_tool(request)


# Create Starlette app with REST routes
routes = [
    Route("/", route_info, methods=["GET"]),
    Route("/.well-known/mcp/server.json", well_known_mcp_server_json, methods=["GET"]),
    Route("/mcp", mcp_alias, methods=["GET", "POST"]),
    Route("/health", health, methods=["GET"]),
    Route("/ready", ready, methods=["GET"]),
    Route("/version", version, methods=["GET"]),
    Route("/metrics", metrics_endpoint, methods=["GET"]),
    Route("/tools", list_tools, methods=["GET"]),
    Route("/self_diagnose", self_diagnose, methods=["GET"]),
    Route("/tools/{tool_name}", call_tool, methods=["POST"]),
    Route("/apex_judge", apex_judge_wrapper, methods=["POST"]),
    Route("/sse", sse_endpoint, methods=["GET", "POST"]),
    Route("/messages", sse_endpoint, methods=["GET"]),
    Route("/messages", messages_endpoint, methods=["POST"]),
    Route(
        "/{tool_name}", call_tool, methods=["POST"]
    ),  # Root path for direct tool calls — MUST BE LAST
]


@asynccontextmanager
async def lifespan(app):
    """Initialize app resources."""
    if os.getenv("ARIFOS_SKIP_MONITORING") != "1":
        try:
            from aaa_mcp.infrastructure.monitoring import init_monitoring

            await init_monitoring()
        except Exception as e:
            print(f"[rest] ⚠️ Lifespan monitoring init failed: {e} - continuing", file=sys.stderr)
    yield


app = Starlette(routes=routes, debug=False, lifespan=lifespan)


def main():
    """Start REST API server."""
    # Initialize monitoring with timeout and error tolerance
    try:
        from aaa_mcp.infrastructure.monitoring import init_monitoring

        # Timeout after 5 seconds to avoid blocking startup
        asyncio.run(asyncio.wait_for(init_monitoring(), timeout=5.0))
        print("[rest] Monitoring initialized successfully", file=sys.stderr)
    except asyncio.TimeoutError:
        print(
            "[rest] ⚠️ Monitoring initialization timeout - continuing without monitoring",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"[rest] ⚠️ Monitoring initialization failed: {e} - continuing without monitoring",
            file=sys.stderr,
        )

    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")

    # Show both core tools and aliases
    all_tool_names = list(TOOLS.keys()) + list(TOOL_ALIASES.keys())

    print(
        f"[rest] AAA MCP REST Bridge v{BUILD_INFO['version']} starting on {host}:{port}",
        file=sys.stderr,
    )
    print(f"[rest] Schema: {BUILD_INFO['schema_version']}", file=sys.stderr)
    print(f"[rest] Core tools: {list(TOOLS.keys())}", file=sys.stderr)
    print(f"[rest] Aliases: {list(TOOL_ALIASES.keys())}", file=sys.stderr)
    print(f"[rest] All endpoints: {all_tool_names}", file=sys.stderr)

    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
