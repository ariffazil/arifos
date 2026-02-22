"""
AAA MCP REST Bridge — HTTP REST API for OpenAI Tool Adapter
Maps HTTP POST /tools/{name} → MCP tool calls
Implements ChatGPT feedback: fast ACK, apex_judge wrapper, observability

Endpoints:
  GET  /health              → Health check
  GET  /ready               → Tool registry + dependencies ready
  GET  /version             → Build info (git sha, schema version)
  GET  /metrics             → Latency, timeouts, active sessions
  GET  /tools               → List available tools with schemas
  POST /tools/{tool_name}   → Call tool with JSON body
  POST /apex_judge          → Full pipeline wrapper (000→333→666→888→999)
  GET  /sse                 → MCP SSE transport
  POST /messages            → MCP JSON-RPC messages

Usage:
  python -m aaa_mcp.rest

DITEMPA BUKAN DIBERI
"""

import asyncio
import inspect
import json
import os
import sys
import time
import uuid
"""
AAA MCP REST Bridge — HTTP REST API for OpenAI Tool Adapter
Maps HTTP POST /tools/{name} → MCP tool calls
Implements ChatGPT feedback: fast ACK, apex_judge wrapper, observability

Endpoints:
  GET  /health              → Health check
  GET  /ready               → Tool registry + dependencies ready
  GET  /version             → Build info (git sha, schema version)
  GET/POST /mcp             → Unified Sovereign Connector alias

Usage:
  python -m aaa_mcp.rest

DITEMPA BUKAN DIBERI
"""

import asyncio
import inspect
import json
import os
import sys
import time
import uuid
import uvicorn
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, List, Any, Optional

from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse, HTMLResponse
from starlette.routing import Route
from starlette.requests import Request

# Import canonical 5-organ tools directly from server module.
# Legacy verbs are supported via HTTP aliases only.
from aaa_mcp.server import (
    agi_cognition,
    apex_verdict,
    asi_empathy,
    init_session,
    vault_seal,
    search,
    fetch,
)
from aaa_mcp.integrations.self_ops import self_diagnose

# Build info
BUILD_INFO = {
    "version": "2026.02.22-FORGE-VPS-SEAL",
    "schema_version": "2026.02.22-FORGE-VPS-SEAL",
    "git_sha": os.environ.get("GIT_SHA", "unknown"),
    "build_time": os.environ.get("BUILD_TIME", datetime.now(timezone.utc).isoformat()),
}

# Tool registry mapping names to functions
TOOLS = {
    "init_session": init_session,
    "agi_cognition": agi_cognition,
    "asi_empathy": asi_empathy,
    "apex_verdict": apex_verdict,
    "vault_seal": vault_seal,
    "self_diagnose": self_diagnose,
    "search": search,
    "fetch": fetch,
}

# Tool schemas with enums (ChatGPT feedback: schema hardening)
TOOL_SCHEMAS = {
    "init_session": {
        "description": "000_INIT — Session ignition + authority checks + injection scan",
        "args": {
            "query": {"type": "string", "required": True},
            "actor_id": {"type": "string", "required": False, "default": "user"},
            "auth_token": {"type": "string|null", "required": False, "default": None},
            "mode": {"type": "enum", "values": ["conscience", "ghost"], "default": "conscience"},
            "grounding_required": {"type": "boolean", "default": True},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "agi_cognition": {
        "description": "111–333_AGI — SENSE→THINK→REASON",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "grounding": {"type": "array|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "asi_empathy": {
        "description": "555–666_ASI — EMPATHIZE→ALIGN",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "stakeholders": {"type": "array|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "apex_verdict": {
        "description": "888_APEX — Final judgment synthesis + tri-witness scoring",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "agi_result": {"type": "object|null", "default": None},
            "asi_result": {"type": "object|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "vault_seal": {
        "description": "999_VAULT — Immutable record seal",
        "args": {
            "session_id": {"type": "string", "required": True},
            "verdict": {
                "type": "enum",
                "values": ["SEAL", "VOID", "PARTIAL", "SABAR", "888_HOLD"],
                "required": True,
            },
            "query_summary": {"type": "string|null", "default": None},
            "risk_level": {
                "type": "enum",
                "values": ["low", "medium", "high", "critical"],
                "default": "low",
            },
            "category": {"type": "string", "default": "general"},
            "floors_checked": {"type": "array|null", "default": None},
            "payload": {"type": "object|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "apex_judge": {
        "description": "Full pipeline wrapper — 000→333→666→888→999 (ChatGPT DX win)",
        "args": {
            "query": {"type": "string", "required": True},
            "actor_id": {"type": "string", "required": False, "default": "user"},
            "auth_token": {"type": "string|null", "default": None},
            "stakeholders": {"type": "array|null", "default": None},
            "grounding": {"type": "array|null", "default": None},
            "auto_seal": {"type": "boolean", "default": False},
            "debug": {"type": "boolean", "default": False},
        },
    },
    "self_diagnose": {
        "description": "SELF_OPS — Infrastructure health check, protocol compatibility, auto-remediation (non-constitutional)",
        "args": {
            "base_url": {
                "type": "string|null",
                "required": False,
                "default": None,
                "description": "Optional custom base URL to diagnose",
            },
        },
    },
    "search": {
        "description": "ChatGPT Deep Research: Search for records matching the query.",
        "args": {
            "query": {"type": "string", "required": True},
        },
    },
    "fetch": {
        "description": "ChatGPT Deep Research: Fetch a complete record by ID.",
        "args": {
            "id": {"type": "string", "required": True},
        },
    },
}

# Tool name aliases for backward compatibility.
# Canonical names remain 5-organ; legacy 9-verbs are HTTP-only aliases.
TOOL_ALIASES = {
    # Legacy 9-verb surface
    "anchor": "init_session",
    "reason": "agi_cognition",
    "integrate": "agi_cognition",
    "respond": "agi_cognition",
    "validate": "asi_empathy",
    "align": "asi_empathy",
    "forge": "apex_verdict",
    "audit": "apex_verdict",
    "seal": "vault_seal",
    # Prior alias surface
    "apex_judge": "apex_verdict",
}


# Metrics tracking (ChatGPT feedback: observability)
@dataclass
class Metrics:
    requests_total: int = 0
    requests_by_tool: Dict[str, int] = field(default_factory=dict)
    latencies_ms: List[float] = field(default_factory=list)
    timeouts: int = 0
    errors: int = 0
    active_sessions: int = 0


metrics = Metrics()

# Active sessions tracking
active_sessions: Dict[str, dict] = {}


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
                {"method": "GET", "path": "/", "description": "Service info (JSON) / landing page (HTML)"},
                {
                    "method": "GET",
                    "path": "/.well-known/mcp/server.json",
                    "description": "MCP discovery (optional)",
                },
                {"method": "GET", "path": "/health", "description": "Health check"},
                {"method": "GET", "path": "/ready", "description": "Readiness (tools + schemas loaded)"},
                {"method": "GET", "path": "/version", "description": "Build info"},
                {"method": "GET", "path": "/metrics", "description": "Operational metrics"},
                {"method": "GET", "path": "/tools", "description": "List tools with schemas"},
                {"method": "POST", "path": "/tools/{tool_name}", "description": "Call tool (canonical + aliases)"},
                {"method": "POST", "path": "/apex_judge", "description": "Full pipeline wrapper"},
                {"method": "GET", "path": "/sse", "description": "MCP SSE transport"},
                {"method": "POST", "path": "/mcp", "description": "Unified MCP alias (Sovereign Connector)"},
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
            with open(static_path, "r") as f:
                content = json.load(f)
        elif os.path.exists(root_path):
            with open(root_path, "r") as f:
                content = json.load(f)
        else:
            return JSONResponse({"error": "server.json not found"}, status_code=404)

        return JSONResponse(content)
    except Exception as e:
        return JSONResponse({"error": f"Failed to load server.json: {str(e)}"}, status_code=500)


async def list_tools(request: Request):
    """List available MCP tools with schemas."""
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
    request_id = generate_request_id()
    tool_name = request.path_params.get("tool_name")
    start_time = time.time()

    # Map classic tool names
    original_name = tool_name
    if tool_name in TOOL_ALIASES:
        tool_name = TOOL_ALIASES[tool_name]

    try:
        body = await request.json()
    except Exception:
        body = {}

    # Add request_id for tracing (ChatGPT feedback: request_id correlation)
    body["request_id"] = request_id

    # Track metrics
    metrics.requests_total += 1
    metrics.requests_by_tool[original_name] = metrics.requests_by_tool.get(original_name, 0) + 1

    try:
        # Fast ACK for init_session (ChatGPT feedback: return fast ACK <200ms)
        if tool_name == "init_session" and body.get("fast_ack", False):
            session_id = body.get("actor_id", "anon") + "-" + uuid.uuid4().hex[:8]
            active_sessions[session_id] = {
                "started": datetime.utcnow().isoformat(),
                "request_id": request_id,
                "status": "initializing",
            }
            # Return fast ACK, continue async work
            return JSONResponse(
                {
                    "status": "ack",
                    "tool": original_name,
                    "session_id": session_id,
                    "request_id": request_id,
                    "message": "Session initializing async",
                }
            )

        # Get tool from registry
        if tool_name not in TOOLS:
            metrics.errors += 1
            return JSONResponse(
                {"error": f"Tool '{original_name}' not found", "request_id": request_id},
                status_code=404,
            )

        tool = TOOLS[tool_name]

        # Call with timeout protection (ChatGPT feedback: prevent timeouts)
        # Note: FastMCP FunctionTool has .fn attribute with the actual function
        try:
            actual_fn = getattr(tool, "fn", tool)
            # Get function parameters and filter body
            sig = inspect.signature(actual_fn)
            param_names = []
            has_kwargs = False
            for name, param in sig.parameters.items():
                if param.kind == inspect.Parameter.VAR_KEYWORD:
                    has_kwargs = True
                else:
                    param_names.append(name)

            if has_kwargs:
                # Function accepts **kwargs, pass all body parameters
                filtered_body = body
            else:
                # Filter to only valid parameters
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

        # Track latency
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
        init_tool = TOOLS["init_session"]
        init_fn = getattr(init_tool, "fn", init_tool)
        init_result = await init_fn(query=query, actor_id=actor_id)
        pipeline_results["pipeline"].append({"stage": "000_INIT", "result": init_result})

        canonical_session_id = init_result.get("session_id", session_id)
        pipeline_results["session_id"] = canonical_session_id

        # Stage 2: AGI (333)
        agi_tool = TOOLS["agi_cognition"]
        agi_fn = getattr(agi_tool, "fn", agi_tool)
        agi_result = await agi_fn(
            query=query,
            session_id=canonical_session_id,
            grounding=body.get("grounding"),
        )
        pipeline_results["pipeline"].append({"stage": "333_AGI", "result": agi_result})

        # Stage 3: ASI (666)
        asi_tool = TOOLS["asi_empathy"]
        asi_fn = getattr(asi_tool, "fn", asi_tool)
        asi_result = await asi_fn(
            query=query, session_id=canonical_session_id, stakeholders=body.get("stakeholders", [])
        )
        pipeline_results["pipeline"].append({"stage": "666_ASI", "result": asi_result})

        # Stage 4: APEX (888)
        apex_tool = TOOLS["apex_verdict"]
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

        # Stage 5: VAULT (999) — optional
        if auto_seal:
            seal_tool = TOOLS["vault_seal"]
            seal_fn = getattr(seal_tool, "fn", seal_tool)
            seal_result = await seal_fn(
                session_id=canonical_session_id,
                summary=query[:100],
                verdict=apex_result.get("verdict", "SEAL"),
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
    Route("/{tool_name}", call_tool, methods=["POST"]),  # Root path for direct tool calls — MUST BE LAST
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
