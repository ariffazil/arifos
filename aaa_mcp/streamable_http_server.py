"""arifOS Streamable HTTP MCP transport endpoint.

Aligns transport behavior to MCP 2025-11-25 Streamable HTTP requirements:
- JSON-RPC 2.0 payloads over POST
- MCP endpoint supports POST, GET, DELETE
- Session header management via MCP-Session-Id
- Protocol version handling via MCP-Protocol-Version
- Origin validation guard for DNS rebinding mitigation
"""

import asyncio
import inspect
import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Any, get_args, get_origin

# Force local source priority (same as rest.py)
sys.path.insert(0, os.getcwd())

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

# Import canonical tools from public 13-tool surface.
from arifos_aaa_mcp.server import (
    anchor_session,
    audit_rules,
    check_vital,
    critique_thought,
    fetch_content,
    forge_hand,
    inspect_file,
    judge_soul,
    reason_mind,
    recall_memory,
    seal_vault,
    search_reality,
    simulate_heart,
)

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = "2025-11-25"
SUPPORTED_PROTOCOL_VERSIONS = {"2025-11-25", "2025-03-26"}
SESSION_HEADER = "MCP-Session-Id"
PROTOCOL_HEADER = "MCP-Protocol-Version"
_ACTIVE_SESSIONS: set[str] = set()

# Tool registry — canonical UX names as primary keys.
TOOLS = {
    "anchor_session": anchor_session,
    "reason_mind": reason_mind,
    "recall_memory": recall_memory,
    "simulate_heart": simulate_heart,
    "critique_thought": critique_thought,
    "judge_soul": judge_soul,
    "forge_hand": forge_hand,
    "seal_vault": seal_vault,
    "search_reality": search_reality,
    "fetch_content": fetch_content,
    "inspect_file": inspect_file,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
}

# Tool descriptions for MCP tools/list.
TOOL_DESCRIPTIONS = {
    "anchor_session": "[Lane: Delta] 000_INIT — Session ignition + injection scan",
    "reason_mind": "[Lane: Delta] 111-444_AGI — SENSE→THINK→REASON with grounding",
    "recall_memory": "[Lane: Omega] 555_RECALL — Associative memory retrieval",
    "simulate_heart": "[Lane: Omega] 555-666_ASI — Stakeholder impact + care",
    "critique_thought": "[Lane: Omega] 666_ALIGN — 7-model bias critique",
    "judge_soul": "[Lane: Psi] 888_APEX_JUDGE — Sovereign verdict synthesis",
    "forge_hand": "[Lane: Psi] 777_EUREKA_FORGE — Sandboxed action execution",
    "seal_vault": "[Lane: Psi] 999_VAULT — Immutable ledger seal",
    "search_reality": "[Lane: Delta] Web grounding search (Perplexity/Brave)",
    "fetch_content": "[Lane: Delta] Raw evidence content retrieval",
    "inspect_file": "[Lane: Delta] Filesystem inspection (read-only)",
    "audit_rules": "[Lane: Delta] Rule & governance audit checks",
    "check_vital": "[Lane: Omega] System health & vital signs",
}

# All aliases resolve to canonical names.
TOOL_ALIASES = {
    # Mid-gen kernel names
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "recall_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "judge_soul",
    "sovereign_actuator": "forge_hand",
    "vault_seal": "seal_vault",
    "search": "search_reality",
    "fetch": "fetch_content",
    "system_audit": "audit_rules",
    # Legacy 9-verb surface
    "anchor": "anchor_session",
    "reason": "reason_mind",
    "integrate": "reason_mind",
    "respond": "reason_mind",
    "validate": "simulate_heart",
    "align": "simulate_heart",
    "forge": "forge_hand",
    "audit": "judge_soul",
    "seal": "seal_vault",
}


async def log_identity(
    user_id: str | None,
    session_id: str | None,
    client_name: str | None,
    client_version: str | None,
    timestamp: datetime,
    method: str,
) -> None:
    """
    Log identity metadata to cooling ledger (guest book).

    Path A: Logging only, no enforcement.
    Logs to /tmp/arifos-identity.log for now (append-only).
    """
    log_entry = {
        "timestamp": timestamp.isoformat(),
        "method": method,
        "user_id": user_id,
        "session_id": session_id,
        "client_name": client_name,
        "client_version": client_version,
    }

    # Simple append-only log file (cooling ledger stub)
    log_file = "/tmp/arifos-identity.log"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=True) + "\n")
    except Exception as e:
        # Never fail request due to audit logging path.
        logger.warning("Identity logging failed: %s", e)

    logger.debug("IDENTITY %s", json.dumps(log_entry, ensure_ascii=True))


def _resolve_tool_callable(tool: Any):
    """Resolve FastMCP FunctionTool wrappers to raw callables."""
    if hasattr(tool, "fn") and callable(tool.fn):
        return tool.fn
    if callable(tool):
        return tool
    return None


def _annotation_to_json_type(annotation: Any) -> str:
    """Convert Python annotation to a coarse JSON Schema type."""
    if annotation is inspect._empty:
        return "string"

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is None:
        if annotation in (str,):
            return "string"
        if annotation in (int, float):
            return "number"
        if annotation is bool:
            return "boolean"
        if annotation in (list, tuple, set):
            return "array"
        if annotation is dict:
            return "object"
        return "string"

    if origin in (list, tuple, set):
        return "array"
    if origin is dict:
        return "object"
    if origin is Any:
        return "object"

    # Optional[T] / Union[T, None]
    if str(origin).endswith("Union") and args:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            return _annotation_to_json_type(non_none[0])
        return "string"

    return "string"


def _build_input_schema(tool: Any) -> dict:
    """Build MCP-compliant inputSchema from tool signature."""
    func = _resolve_tool_callable(tool)
    if func is None:
        return {"type": "object", "properties": {}, "additionalProperties": True}

    sig = inspect.signature(func)
    properties: dict[str, dict] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        prop = {"type": _annotation_to_json_type(param.annotation)}
        if param.default is not inspect._empty:
            prop["default"] = param.default
        else:
            required.append(name)
        properties[name] = prop

    schema = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
    }
    if required:
        schema["required"] = required
    return schema


async def mcp_endpoint(request: Request) -> Response:
    """Handle MCP Streamable HTTP endpoint (POST/GET/DELETE)."""

    def _allowed_origins() -> set[str]:
        raw = os.getenv(
            "ARIFOS_ALLOWED_ORIGINS",
            "http://localhost,http://127.0.0.1,https://localhost,https://127.0.0.1",
        )
        return {v.strip() for v in raw.split(",") if v.strip()}

    def _transport_headers(session_id: str | None = None) -> dict[str, str]:
        headers = {PROTOCOL_HEADER: PROTOCOL_VERSION}
        if session_id:
            headers[SESSION_HEADER] = session_id
        return headers

    def _jsonrpc_error(
        *,
        code: int,
        message: str,
        request_id: Any = None,
        http_status: int = 400,
        session_id: str | None = None,
    ) -> JSONResponse:
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "error": {"code": code, "message": message},
        }
        if request_id is not None:
            payload["id"] = request_id
        return JSONResponse(payload, status_code=http_status, headers=_transport_headers(session_id))

    # Security: origin validation to mitigate DNS rebinding.
    origin = request.headers.get("origin")
    if origin and origin not in _allowed_origins():
        return _jsonrpc_error(code=-32600, message="Forbidden origin", http_status=403)

    if request.method == "GET":
        accept = request.headers.get("accept", "")
        if "text/event-stream" not in accept:
            return Response(status_code=406, headers=_transport_headers())
        # This server does not expose an unsolicited SSE stream.
        return Response(status_code=405, headers=_transport_headers())

    if request.method == "DELETE":
        session_id = request.headers.get(SESSION_HEADER, "")
        if not session_id:
            return Response(status_code=400, headers=_transport_headers())
        _ACTIVE_SESSIONS.discard(session_id)
        return Response(status_code=204, headers=_transport_headers())

    # POST rules
    accept = request.headers.get("accept", "")
    if "application/json" not in accept or "text/event-stream" not in accept:
        return Response(status_code=406, headers=_transport_headers())

    try:
        body = await request.json()
    except Exception:
        return _jsonrpc_error(code=-32700, message="Invalid JSON", http_status=400)

    if not isinstance(body, dict) or body.get("jsonrpc") != "2.0":
        return _jsonrpc_error(code=-32600, message="Invalid JSON-RPC 2.0 payload", http_status=400)

    request_id = body.get("id")
    method = body.get("method")
    params = body.get("params") if isinstance(body.get("params"), dict) else {}

    # Client notifications and responses are acknowledged with 202.
    if method is None:
        is_response = ("result" in body or "error" in body) and request_id is not None
        if is_response:
            return Response(status_code=202, headers=_transport_headers())
        return _jsonrpc_error(code=-32600, message="Method is required", http_status=400)

    # Initialization can open a new session.
    if method == "initialize":
        session_id = str(uuid.uuid4())
        _ACTIVE_SESSIONS.add(session_id)
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}, "logging": {}},
            "serverInfo": {
                "name": "arifos-aaa-mcp",
                "version": "2026.02.23-CANONICAL-13",
            },
        }
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": result},
            headers=_transport_headers(session_id),
        )

    session_id = request.headers.get(SESSION_HEADER, "")
    if not session_id:
        return _jsonrpc_error(
            code=-32600,
            message=f"Missing {SESSION_HEADER} header",
            request_id=request_id,
            http_status=400,
        )
    if session_id not in _ACTIVE_SESSIONS:
        return _jsonrpc_error(
            code=-32001,
            message="Session not found",
            request_id=request_id,
            http_status=404,
            session_id=session_id,
        )

    protocol_version = request.headers.get(PROTOCOL_HEADER)
    if protocol_version and protocol_version not in SUPPORTED_PROTOCOL_VERSIONS:
        return _jsonrpc_error(
            code=-32600,
            message=f"Unsupported {PROTOCOL_HEADER}: {protocol_version}",
            request_id=request_id,
            http_status=400,
            session_id=session_id,
        )

    # Capture identity metadata for audit trail.
    client_info = params.get("clientInfo", {}) if isinstance(params, dict) else {}
    user_id = (
        client_info.get("user_id")
        if isinstance(client_info, dict)
        else None
    ) or request.headers.get("x-arifos-user-id")
    await log_identity(
        user_id=user_id,
        session_id=session_id,
        client_name=client_info.get("name") if isinstance(client_info, dict) else None,
        client_version=client_info.get("version") if isinstance(client_info, dict) else None,
        timestamp=datetime.now(timezone.utc),
        method=str(method),
    )

    if method == "notifications/initialized":
        return Response(status_code=202, headers=_transport_headers(session_id))

    if method == "resources/list":
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"resources": []}},
            headers=_transport_headers(session_id),
        )

    if method == "prompts/list":
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"prompts": []}},
            headers=_transport_headers(session_id),
        )

    if method == "tools/list":
        tools = [
            {
                "name": name,
                "description": desc,
                "inputSchema": _build_input_schema(TOOLS[name]),
            }
            for name, desc in TOOL_DESCRIPTIONS.items()
        ]
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}},
            headers=_transport_headers(session_id),
        )

    if method == "tools/call":
        if not isinstance(params, dict):
            return _jsonrpc_error(
                code=-32602,
                message="Invalid params",
                request_id=request_id,
                session_id=session_id,
            )

        tool_name = TOOL_ALIASES.get(str(params.get("name", "")), str(params.get("name", "")))
        tool_args = params.get("arguments", {})
        if not isinstance(tool_args, dict):
            return _jsonrpc_error(
                code=-32602,
                message="Tool arguments must be object",
                request_id=request_id,
                session_id=session_id,
            )

        if tool_name not in TOOLS:
            return _jsonrpc_error(
                code=-32601,
                message=f"Tool not found: {tool_name}",
                request_id=request_id,
                session_id=session_id,
            )

        func = _resolve_tool_callable(TOOLS[tool_name])
        if func is None:
            return _jsonrpc_error(
                code=-32000,
                message=f"Tool not callable: {tool_name}",
                request_id=request_id,
                session_id=session_id,
            )

        try:
            maybe_result = func(**tool_args)
            if inspect.isawaitable(maybe_result):
                result = await asyncio.wait_for(maybe_result, timeout=10.0)
            else:
                result = maybe_result
            response_payload = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=True)}]
                },
            }
            return JSONResponse(response_payload, headers=_transport_headers(session_id))
        except asyncio.TimeoutError:
            return _jsonrpc_error(
                code=-32000,
                message="Tool execution timeout",
                request_id=request_id,
                session_id=session_id,
            )
        except Exception as e:
            return _jsonrpc_error(
                code=-32000,
                message=f"Tool execution error: {e}",
                request_id=request_id,
                session_id=session_id,
            )

    return _jsonrpc_error(
        code=-32601,
        message=f"Method not found: {method}",
        request_id=request_id,
        session_id=session_id,
    )


async def health(request: Request) -> JSONResponse:
    """Health check with governance metrics."""
    from aaa_mcp.infrastructure.monitoring import get_health_monitor, get_metrics_collector

    monitor = get_health_monitor()
    collector = get_metrics_collector()

    health_results = await monitor.check_all()
    stats = collector.get_stats()

    return JSONResponse(
        {
            "status": "healthy" if monitor.is_healthy() else "degraded",
            "transport": "streamable-http",
            "version": "2026.02.23-CANONICAL-13",
            "governance_metrics": stats,
            "health_checks": health_results,
            "endpoints": ["/mcp", "/health"],
        }
    )


async def well_known_mcp_server_json(request: Request) -> JSONResponse:
    """Serve MCP discovery document for clients and registries."""
    try:
        static_path = os.path.join(
            os.path.dirname(__file__), "..", "static", ".well-known", "mcp", "server.json"
        )
        root_path = os.path.join(os.path.dirname(__file__), "..", "server.json")

        file_path = static_path if os.path.exists(static_path) else root_path
        if not os.path.exists(file_path):
            return JSONResponse({"error": "server.json not found"}, status_code=404)

        with open(file_path, encoding="utf-8") as f:
            payload = json.load(f)
        return JSONResponse(payload)
    except Exception as e:
        return JSONResponse({"error": f"failed to load server.json: {str(e)}"}, status_code=500)


routes = [
    Route("/mcp", mcp_endpoint, methods=["POST", "GET", "DELETE"]),
    Route("/messages", mcp_endpoint, methods=["POST"]),
    Route("/messages/", mcp_endpoint, methods=["POST"]),
    Route("/health", health, methods=["GET"]),
    Route("/.well-known/mcp/server.json", well_known_mcp_server_json, methods=["GET"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    # Initialize monitoring
    from aaa_mcp.infrastructure.monitoring import init_monitoring

    asyncio.run(init_monitoring())

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8889"))
    uvicorn.run(app, host=host, port=port)
