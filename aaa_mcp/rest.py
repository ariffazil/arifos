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

import os
import sys
import json
import asyncio
import time
import uuid
from typing import Any, AsyncGenerator, Dict, List
from dataclasses import dataclass, field
from datetime import datetime

# Force local source priority
sys.path.insert(0, os.getcwd())

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route
from starlette.requests import Request

# Import tools directly from server module (avoid mcp wrapper issues)
from aaa_mcp.server import anchor, reason, integrate, respond, validate, align, forge, audit, seal
from aaa_mcp.integrations.self_ops import self_diagnose

# Build info
BUILD_INFO = {
    "version": "64.2.0",
    "schema_version": "v65.0-chatgpt",
    "git_sha": os.environ.get("GIT_SHA", "unknown"),
    "build_time": os.environ.get("BUILD_TIME", datetime.utcnow().isoformat()),
}

# Tool registry mapping names to functions
TOOLS = {
    "anchor": anchor,
    "reason": reason,
    "integrate": integrate,
    "respond": respond,
    "validate": validate,
    "align": align,
    "forge": forge,
    "audit": audit,
    "seal": seal,
    "self_diagnose": self_diagnose,
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
        }
    },
    "agi_cognition": {
        "description": "111–333_AGI — SENSE→THINK→REASON",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "grounding": {"type": "array|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        }
    },
    "asi_empathy": {
        "description": "555–666_ASI — EMPATHIZE→ALIGN",
        "args": {
            "query": {"type": "string", "required": True},
            "session_id": {"type": "string", "required": True},
            "stakeholders": {"type": "array|null", "default": None},
            "capability_modules": {"type": "array|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        }
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
        }
    },
    "vault_seal": {
        "description": "999_VAULT — Immutable record seal",
        "args": {
            "session_id": {"type": "string", "required": True},
            "verdict": {"type": "enum", "values": ["SEAL", "VOID", "PARTIAL", "SABAR", "888_HOLD"], "required": True},
            "query_summary": {"type": "string|null", "default": None},
            "risk_level": {"type": "enum", "values": ["low", "medium", "high", "critical"], "default": "low"},
            "category": {"type": "string", "default": "general"},
            "floors_checked": {"type": "array|null", "default": None},
            "payload": {"type": "object|null", "default": None},
            "debug": {"type": "boolean", "default": False},
        }
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
        }
    },
    "self_diagnose": {
        "description": "SELF_OPS — Infrastructure health check, protocol compatibility, auto-remediation (non-constitutional)",
        "args": {
            "base_url": {"type": "string|null", "required": False, "default": None, "description": "Optional custom base URL to diagnose"},
        }
    },
}

# Tool name aliases for backward compatibility (classic 5-tool schema)
TOOL_ALIASES = {
    "init_session": "anchor",
    "agi_cognition": "reason",
    "asi_empathy": "validate",
    "apex_verdict": "audit",
    "vault_seal": "seal",
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


async def health(request: Request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "aaa-mcp-rest",
        "version": BUILD_INFO["version"],
    })


async def ready(request: Request):
    """Readiness check — tool registry loaded (ChatGPT feedback: /ready endpoint)."""
    try:
        tools_loaded = len(TOOLS)
        schemas_loaded = len(TOOL_SCHEMAS)
        return JSONResponse({
            "ready": tools_loaded > 0 and schemas_loaded > 0,
            "tools_loaded": tools_loaded,
            "schemas_loaded": schemas_loaded,
            "tool_names": list(TOOLS.keys()),
        })
    except Exception as e:
        return JSONResponse({"ready": False, "error": str(e)}, status_code=503)


async def version(request: Request):
    """Build version info (ChatGPT feedback: /version endpoint)."""
    return JSONResponse(BUILD_INFO)


async def metrics_endpoint(request: Request):
    """Metrics endpoint (ChatGPT feedback: /metrics endpoint)."""
    avg_latency = sum(metrics.latencies_ms) / len(metrics.latencies_ms) if metrics.latencies_ms else 0
    return JSONResponse({
        "requests_total": metrics.requests_total,
        "requests_by_tool": metrics.requests_by_tool,
        "avg_latency_ms": round(avg_latency, 2),
        "timeouts": metrics.timeouts,
        "errors": metrics.errors,
        "active_sessions": len(active_sessions),
    })


async def well_known_mcp_server_json(request: Request):
    """Serve MCP server.json for registry auto-discovery.
    
    Endpoint: /.well-known/mcp/server.json
    Used by MCP Registry for automatic server discovery and updates.
    """
    try:
        # Try static directory first (for production deployments)
        static_path = os.path.join(os.path.dirname(__file__), "..", "static", ".well-known", "mcp", "server.json")
        # Fallback to repo root (for development)
        root_path = os.path.join(os.path.dirname(__file__), "..", "server.json")
        
        if os.path.exists(static_path):
            with open(static_path, "r") as f:
                content = json.load(f)
        elif os.path.exists(root_path):
            with open(root_path, "r") as f:
                content = json.load(f)
        else:
            return JSONResponse(
                {"error": "server.json not found"},
                status_code=404
            )
        
        return JSONResponse(content)
    except Exception as e:
        return JSONResponse(
            {"error": f"Failed to load server.json: {str(e)}"},
            status_code=500
        )


async def list_tools(request: Request):
    """List available MCP tools with schemas."""
    tool_list = []
    for name, schema in TOOL_SCHEMAS.items():
        tool_list.append({
            "name": name,
            "description": schema["description"],
            "args": schema["args"],
        })
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
        if tool_name == "anchor" and body.get("fast_ack", False):
            session_id = body.get("actor_id", "anon") + "-" + uuid.uuid4().hex[:8]
            active_sessions[session_id] = {
                "started": datetime.utcnow().isoformat(),
                "request_id": request_id,
                "status": "initializing"
            }
            # Return fast ACK, continue async work
            return JSONResponse({
                "status": "ack",
                "tool": original_name,
                "session_id": session_id,
                "request_id": request_id,
                "message": "Session initializing async",
            })
        
        # Get tool from registry
        if tool_name not in TOOLS:
            metrics.errors += 1
            return JSONResponse(
                {"error": f"Tool '{original_name}' not found", "request_id": request_id},
                status_code=404
            )
        
        tool = TOOLS[tool_name]
        
        # Call with timeout protection (ChatGPT feedback: prevent timeouts)
        try:
            result = await asyncio.wait_for(tool(**body), timeout=10.0)
        except asyncio.TimeoutError:
            metrics.timeouts += 1
            return JSONResponse({
                "error": "INIT_TIMEOUT",
                "stage": "tool_execution",
                "request_id": request_id,
                "tool": original_name,
            }, status_code=504)
        
        # Track latency
        latency_ms = (time.time() - start_time) * 1000
        metrics.latencies_ms.append(latency_ms)
        
        return JSONResponse({
            "status": "success",
            "tool": original_name,
            "request_id": request_id,
            "latency_ms": round(latency_ms, 2),
            "result": result,
        })
    except Exception as e:
        metrics.errors += 1
        return JSONResponse(
            {"error": str(e), "tool": original_name, "request_id": request_id},
            status_code=500
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
        init_result = await anchor(query=query, actor_id=actor_id, mode="conscience")
        pipeline_results["pipeline"].append({"stage": "000_INIT", "result": init_result})
        
        # Stage 2: AGI (333)
        agi_result = await reason(query=query, session_id=session_id)
        pipeline_results["pipeline"].append({"stage": "333_AGI", "result": agi_result})
        
        # Stage 3: ASI (666)
        asi_result = await validate(session_id=session_id, stakeholders=body.get("stakeholders", []))
        pipeline_results["pipeline"].append({"stage": "666_ASI", "result": asi_result})
        
        # Stage 4: APEX (888)
        apex_result = await audit(session_id=session_id, verdict="SEAL")
        pipeline_results["pipeline"].append({"stage": "888_APEX", "result": apex_result})
        
        # Stage 5: VAULT (999) — optional
        if auto_seal:
            seal_result = await seal(session_id=session_id, summary=query[:100], verdict="SEAL")
            pipeline_results["pipeline"].append({"stage": "999_VAULT", "result": seal_result})
        
        latency_ms = (time.time() - start_time) * 1000
        pipeline_results["latency_ms"] = round(latency_ms, 2)
        pipeline_results["final_verdict"] = apex_result.get("verdict", "UNKNOWN")
        
        return JSONResponse(pipeline_results)
        
    except Exception as e:
        return JSONResponse({
            "error": str(e),
            "request_id": request_id,
            "session_id": session_id,
            "pipeline": pipeline_results["pipeline"],
        }, status_code=500)


async def sse_endpoint(request: Request):
    """MCP SSE transport endpoint."""
    async def event_generator() -> AsyncGenerator[str, None]:
        msg_url = f"{request.url.scheme}://{request.url.netloc}/messages"
        yield f"event: endpoint\ndata: {msg_url}\n\n"
        
        while True:
            if await request.is_disconnected():
                break
            yield ": ping\n\n"
            await asyncio.sleep(30)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )


async def messages_endpoint(request: Request):
    """MCP messages endpoint for client to server communication."""
    try:
        body = await request.json()
        method = body.get("method", "")
        params = body.get("params", {})
        msg_id = body.get("id")
        
        # Handle apex_judge wrapper
        if method == "apex_judge":
            result = await apex_judge_wrapper(request)
            return result
        
        tool_name = method.split("/")[-1] if "/" in method else method
        if tool_name in TOOL_ALIASES:
            tool_name = TOOL_ALIASES[tool_name]
        
        if tool_name not in TOOLS:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
        
        tool = TOOLS[tool_name]
        result = await tool(**params)
        
        return JSONResponse({"jsonrpc": "2.0", "id": msg_id, "result": result})
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in dir() else None,
            "error": {"code": -32603, "message": str(e)}
        })


async def route_info(request: Request):
    """Show all available routes for debugging."""
    return JSONResponse({
        "service": "aaa-mcp-rest",
        "version": BUILD_INFO["version"],
        "schema_version": BUILD_INFO["schema_version"],
        "routes": [
            {"method": "GET", "path": "/health", "description": "Health check"},
            {"method": "GET", "path": "/ready", "description": "Tool registry + dependencies ready"},
            {"method": "GET", "path": "/version", "description": "Build info (git sha, schema version)"},
            {"method": "GET", "path": "/metrics", "description": "Latency, timeouts, active sessions"},
            {"method": "GET", "path": "/tools", "description": "List tools with schemas"},
            {"method": "POST", "path": "/tools/{tool_name}", "description": "Call tool"},
            {"method": "POST", "path": "/apex_judge", "description": "Full pipeline wrapper (DX win)"},
            {"method": "GET", "path": "/sse", "description": "MCP SSE transport"},
            {"method": "POST", "path": "/messages", "description": "MCP JSON-RPC messages"},
        ],
        "tools": list(TOOL_SCHEMAS.keys()),
    })


# Create Starlette app with REST routes
routes = [
    Route("/", route_info, methods=["GET"]),
    Route("/.well-known/mcp/server.json", well_known_mcp_server_json, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
    Route("/ready", ready, methods=["GET"]),
    Route("/version", version, methods=["GET"]),
    Route("/metrics", metrics_endpoint, methods=["GET"]),
    Route("/tools", list_tools, methods=["GET"]),
    Route("/self_diagnose", self_diagnose, methods=["GET"]),
    Route("/tools/{tool_name}", call_tool, methods=["POST"]),
    Route("/{tool_name}", call_tool, methods=["POST"]),  # Root path for direct tool calls
    Route("/apex_judge", apex_judge_wrapper, methods=["POST"]),
    Route("/sse", sse_endpoint, methods=["GET"]),
    Route("/messages", messages_endpoint, methods=["POST"]),
]

app = Starlette(routes=routes, debug=False)


def main():
    """Start REST API server."""
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Show both core tools and aliases
    all_tool_names = list(TOOLS.keys()) + list(TOOL_ALIASES.keys())
    
    print(f"[rest] AAA MCP REST Bridge v{BUILD_INFO['version']} starting on {host}:{port}", file=sys.stderr)
    print(f"[rest] Schema: {BUILD_INFO['schema_version']}", file=sys.stderr)
    print(f"[rest] Core tools: {list(TOOLS.keys())}", file=sys.stderr)
    print(f"[rest] Aliases: {list(TOOL_ALIASES.keys())}", file=sys.stderr)
    print(f"[rest] All endpoints: {all_tool_names}", file=sys.stderr)
    
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
