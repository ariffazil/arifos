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
from types import UnionType
from typing import Any, Union, get_args, get_origin, get_type_hints

# Force local source priority (same as rest.py)
sys.path.insert(0, os.getcwd())

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from aaa_mcp.protocol.public_surface import (
    PUBLIC_PROMPT_NAMES,
    PUBLIC_RESOURCE_URIS,
    PUBLIC_TOOL_ALIASES,
)
from aaa_mcp.protocol.aaa_contract import AAA_CANONICAL_TOOLS, CANONICAL_TOOL_COUNT

# Import canonical tools from public 13-tool surface.
from arifos_aaa_mcp.server import (
    aaa_chain_prompt,
    aaa_full_context_pack,
    aaa_tool_schemas,
    anchor_session,
    apex_judge,
    audit_rules,
    check_vital,
    critique_thought,
    eureka_forge,
    ingest_evidence,
    metabolic_loop,
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
_ACTIVE_SESSIONS: dict[str, str] = {}

RESOURCE_DESCRIPTORS = [
    {
        "uri": PUBLIC_RESOURCE_URIS["schemas"],
        "name": "arifos_aaa_tool_schemas",
        "description": "Canonical AAA MCP 13-tool schema/contract overview.",
        "mimeType": "application/json",
    },
    {
        "uri": PUBLIC_RESOURCE_URIS["full_context_pack"],
        "name": "arifos_aaa_full_context_pack",
        "description": "Full-context orchestration metadata (stage spine, prompts, resources).",
        "mimeType": "application/json",
    },
]

PROMPT_DESCRIPTORS = [
    {
        "name": PUBLIC_PROMPT_NAMES["aaa_chain"],
        "title": "AAA Chain Prompt",
        "description": "Run canonical 13-tool continuity chain from anchor to seal.",
        "arguments": [
            {"name": "query", "required": True},
            {"name": "actor_id", "required": False},
        ],
    }
]

PROMPT_ARGUMENT_COMPLETIONS: dict[str, dict[str, list[str]]] = {
    PUBLIC_PROMPT_NAMES["aaa_chain"]: {
        "actor_id": ["user", "ops", "anonymous"],
    }
}

# Tool registry — exactly 13 canonical tools, keyed by canonical name.
# Sourced from AAA_CANONICAL_TOOLS; no archived or internal tools present.
TOOLS = {
    "anchor_session": anchor_session,
    "reason_mind": reason_mind,
    "recall_memory": recall_memory,
    "simulate_heart": simulate_heart,
    "critique_thought": critique_thought,
    "eureka_forge": eureka_forge,
    "apex_judge": apex_judge,
    "seal_vault": seal_vault,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
    "metabolic_loop": metabolic_loop,
}

# Tool descriptions for MCP tools/list — 13 canonical tools only.
TOOL_DESCRIPTIONS = {
    "anchor_session": "[Lane: Delta] 000_INIT — Session ignition + injection scan",
    "reason_mind": "[Lane: Delta] 111-444_AGI — SENSE→THINK→REASON with grounding",
    "recall_memory": "[Lane: Omega] 555_RECALL — Associative memory retrieval",
    "simulate_heart": "[Lane: Omega] 555-666_ASI — Stakeholder impact + care",
    "critique_thought": "[Lane: Omega] 666_ALIGN — 7-model bias critique",
    "eureka_forge": "[Lane: Psi] 777_EUREKA_FORGE — Sandboxed action execution",
    "apex_judge": "[Lane: Psi] 888_APEX_JUDGE — Sovereign verdict synthesis",
    "seal_vault": "[Lane: Psi] 999_VAULT — Immutable ledger seal",
    "search_reality": "[Lane: Delta] Web grounding search (Perplexity/Brave)",
    "ingest_evidence": "[Lane: Delta] Unified evidence ingestion — URL fetch or file inspect",
    "audit_rules": "[Lane: Delta] Rule & governance audit checks",
    "check_vital": "[Lane: Omega] System health & vital signs",
    "metabolic_loop": "[Lane: ALL] 000→999 full constitutional cycle orchestration",
}

# All aliases resolve to canonical names.
TOOL_ALIASES = dict(PUBLIC_TOOL_ALIASES)


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
    if origin in (Union, UnionType) and args:
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
    try:
        type_hints = get_type_hints(func)
    except Exception:
        type_hints = {}
    properties: dict[str, dict] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        annotation = type_hints.get(name, param.annotation)
        prop = {"type": _annotation_to_json_type(annotation)}
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


def _complete_prompt_argument(prompt_name: str, arg_name: str, value: str) -> list[str]:
    """Return deterministic completion values for known prompt arguments."""
    args = PROMPT_ARGUMENT_COMPLETIONS.get(prompt_name, {})
    candidates = args.get(arg_name, [])
    if not candidates:
        return []

    needle = value.lower().strip()
    if not needle:
        return candidates
    return [candidate for candidate in candidates if candidate.lower().startswith(needle)]


async def mcp_endpoint(request: Request) -> Response:
    """Handle MCP Streamable HTTP endpoint (POST/GET/DELETE)."""

    def _allowed_origins() -> set[str]:
        raw = os.getenv(
            "ARIFOS_ALLOWED_ORIGINS",
            "http://localhost,http://127.0.0.1,https://localhost,https://127.0.0.1",
        )
        return {v.strip() for v in raw.split(",") if v.strip()}

    def _transport_headers(
        session_id: str | None = None,
        protocol_version: str | None = None,
    ) -> dict[str, str]:
        negotiated = protocol_version
        if negotiated is None and session_id:
            negotiated = _ACTIVE_SESSIONS.get(session_id)
        headers = {PROTOCOL_HEADER: negotiated or PROTOCOL_VERSION}
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
        return JSONResponse(
            payload, status_code=http_status, headers=_transport_headers(session_id)
        )

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
        _ACTIVE_SESSIONS.pop(session_id, None)
        return Response(status_code=204, headers=_transport_headers())

    # POST rules
    accept = request.headers.get("accept", "")
    if "application/json" not in accept and "text/event-stream" not in accept:
        return Response(status_code=406, headers=_transport_headers())

    try:
        body = await request.json()
    except Exception:
        return _jsonrpc_error(code=-32700, message="Invalid JSON", http_status=400)

    if not isinstance(body, dict) or body.get("jsonrpc") != "2.0":
        return _jsonrpc_error(code=-32600, message="Invalid JSON-RPC 2.0 payload", http_status=400)

    request_id = body.get("id")
    method = body.get("method")
    raw_params: Any = body.get("params")
    params: dict[str, Any] = raw_params if isinstance(raw_params, dict) else {}

    # Client notifications and responses are acknowledged with 202.
    if method is None:
        is_response = ("result" in body or "error" in body) and request_id is not None
        if is_response:
            return Response(status_code=202, headers=_transport_headers())
        return _jsonrpc_error(code=-32600, message="Method is required", http_status=400)

    # Initialization can open a new session.
    if method == "initialize":
        requested_version = str(params.get("protocolVersion", "")).strip()
        if requested_version and requested_version not in SUPPORTED_PROTOCOL_VERSIONS:
            supported = ", ".join(sorted(SUPPORTED_PROTOCOL_VERSIONS))
            return _jsonrpc_error(
                code=-32602,
                message=f"Unsupported protocolVersion: {requested_version}. Supported: {supported}",
                request_id=request_id,
                http_status=400,
            )

        negotiated_version = requested_version or PROTOCOL_VERSION
        session_id = str(uuid.uuid4())
        _ACTIVE_SESSIONS[session_id] = negotiated_version
        result = {
            "protocolVersion": negotiated_version,
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False},
                "prompts": {"listChanged": False},
                "completion": {},
                "logging": {},
            },
            "serverInfo": {
                "name": "arifos-aaa-mcp",
                "version": "2026.02.27-CANONICAL-13",
            },
        }
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": result},
            headers=_transport_headers(session_id, negotiated_version),
        )

    session_id = request.headers.get(SESSION_HEADER, "")

    is_anchor = False
    if method == "tools/call" and isinstance(params, dict):
        tool_n = str(params.get("name", ""))
        # Resolve alias if used
        target_tool = TOOL_ALIASES.get(tool_n, tool_n)
        if target_tool == "anchor_session":
            is_anchor = True

    if not session_id:
        if is_anchor:
            session_id = str(uuid.uuid4())
            _ACTIVE_SESSIONS[session_id] = PROTOCOL_VERSION
        else:
            return _jsonrpc_error(
                code=-32600,
                message=f"Missing {SESSION_HEADER} header",
                request_id=request_id,
                http_status=400,
            )
    if session_id not in _ACTIVE_SESSIONS:
        if is_anchor:
            _ACTIVE_SESSIONS[session_id] = PROTOCOL_VERSION
        else:
            return _jsonrpc_error(
                code=-32001,
                message="Session not found",
                request_id=request_id,
                http_status=404,
                session_id=session_id,
            )

    negotiated_version = _ACTIVE_SESSIONS[session_id]

    protocol_version = request.headers.get(PROTOCOL_HEADER)
    if protocol_version and protocol_version not in SUPPORTED_PROTOCOL_VERSIONS:
        return _jsonrpc_error(
            code=-32600,
            message=f"Unsupported {PROTOCOL_HEADER}: {protocol_version}",
            request_id=request_id,
            http_status=400,
            session_id=session_id,
        )
    if protocol_version and protocol_version != negotiated_version:
        return _jsonrpc_error(
            code=-32600,
            message=(
                f"Protocol version mismatch for session. "
                f"Expected: {negotiated_version}, got: {protocol_version}"
            ),
            request_id=request_id,
            http_status=400,
            session_id=session_id,
        )

    # Capture identity metadata for audit trail.
    client_info = params.get("clientInfo", {}) if isinstance(params, dict) else {}
    user_id = (
        client_info.get("user_id") if isinstance(client_info, dict) else None
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

    if method in {
        "notifications/tools/list_changed",
        "notifications/resources/list_changed",
        "notifications/prompts/list_changed",
    }:
        return Response(status_code=202, headers=_transport_headers(session_id))

    if method == "resources/list":
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"resources": RESOURCE_DESCRIPTORS}},
            headers=_transport_headers(session_id),
        )

    if method == "resources/templates/list":
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"resourceTemplates": []}},
            headers=_transport_headers(session_id),
        )

    if method in {"resources/subscribe", "resources/unsubscribe"}:
        return _jsonrpc_error(
            code=-32601,
            message="Resource subscriptions are not supported by this transport",
            request_id=request_id,
            session_id=session_id,
        )

    if method == "resources/read":
        uri = str(params.get("uri", "")).strip()
        if uri == PUBLIC_RESOURCE_URIS["schemas"]:
            content_text = aaa_tool_schemas()
        elif uri == PUBLIC_RESOURCE_URIS["full_context_pack"]:
            content_text = aaa_full_context_pack()
        else:
            return _jsonrpc_error(
                code=-32602,
                message=f"Unknown resource URI: {uri}",
                request_id=request_id,
                session_id=session_id,
            )
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": content_text,
                        }
                    ]
                },
            },
            headers=_transport_headers(session_id),
        )

    if method == "prompts/list":
        return JSONResponse(
            {"jsonrpc": "2.0", "id": request_id, "result": {"prompts": PROMPT_DESCRIPTORS}},
            headers=_transport_headers(session_id),
        )

    if method == "prompts/get":
        prompt_name = str(params.get("name", "")).strip()
        if prompt_name != PUBLIC_PROMPT_NAMES["aaa_chain"]:
            return _jsonrpc_error(
                code=-32602,
                message=f"Unknown prompt: {prompt_name}",
                request_id=request_id,
                session_id=session_id,
            )

        raw_arguments: Any = params.get("arguments")
        arguments: dict[str, Any] = raw_arguments if isinstance(raw_arguments, dict) else {}
        query = str(arguments.get("query", "")).strip() or ""
        actor_id = str(arguments.get("actor_id", "user")).strip() or "user"
        prompt_text = aaa_chain_prompt(query=query, actor_id=actor_id)
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "name": PUBLIC_PROMPT_NAMES["aaa_chain"],
                    "description": "Run canonical 13-tool continuity chain from anchor to seal.",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": prompt_text,
                            },
                        }
                    ],
                },
            },
            headers=_transport_headers(session_id),
        )

    if method == "completion/complete":
        ref = params.get("ref", {}) if isinstance(params, dict) else {}
        argument = params.get("argument", {}) if isinstance(params, dict) else {}

        if not isinstance(ref, dict) or not isinstance(argument, dict):
            return _jsonrpc_error(
                code=-32602,
                message="Invalid completion params",
                request_id=request_id,
                session_id=session_id,
            )

        ref_type = str(ref.get("type", "")).strip()
        if ref_type == "prompt":
            prompt_name = str(ref.get("name", "")).strip()
            arg_name = str(argument.get("name", "")).strip()
            arg_value = str(argument.get("value", ""))

            if prompt_name != PUBLIC_PROMPT_NAMES["aaa_chain"]:
                return _jsonrpc_error(
                    code=-32602,
                    message=f"Unknown prompt for completion: {prompt_name}",
                    request_id=request_id,
                    session_id=session_id,
                )

            values = _complete_prompt_argument(prompt_name, arg_name, arg_value)
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "completion": {
                            "values": values,
                            "total": len(values),
                            "hasMore": False,
                        }
                    },
                },
                headers=_transport_headers(session_id),
            )

        if ref_type == "resource":
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "completion": {
                            "values": [],
                            "total": 0,
                            "hasMore": False,
                        }
                    },
                },
                headers=_transport_headers(session_id),
            )

        return _jsonrpc_error(
            code=-32602,
            message=f"Unsupported completion ref type: {ref_type}",
            request_id=request_id,
            session_id=session_id,
        )

    if method == "tools/list":
        # MCP 2025-11-25: tools/list supports cursor-based pagination.
        # All 13 canonical tools fit in one page, so nextCursor is omitted.
        # Null/missing cursor is treated as "first page" per spec §3.3.
        tools = [
            {
                "name": name,
                "description": TOOL_DESCRIPTIONS[name],
                "inputSchema": _build_input_schema(TOOLS[name]),
            }
            for name in AAA_CANONICAL_TOOLS
            if name in TOOLS and name in TOOL_DESCRIPTIONS
        ]
        # Invariant check — surface must never exceed the sacred 13.
        assert len(tools) == CANONICAL_TOOL_COUNT, (
            f"tools/list surface violation: got {len(tools)}, expected {CANONICAL_TOOL_COUNT}"
        )
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools,
                    # nextCursor omitted when all tools fit on one page (MCP 2025-11-25 §3.3)
                },
            },
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
    """Health check with governance metrics — reports exactly 13 canonical tools."""
    from aaa_mcp.infrastructure.monitoring import get_health_monitor, get_metrics_collector
    from aaa_mcp.protocol.aaa_contract import ARCHIVED_TOOLS

    monitor = get_health_monitor()
    collector = get_metrics_collector()

    health_results = await monitor.check_all()
    stats = collector.get_stats()

    return JSONResponse(
        {
            "status": "healthy" if monitor.is_healthy() else "degraded",
            "transport": "streamable-http",
            "version": "2026.02.27-CANONICAL-13",
            "tools": {
                "canonical_tools_count": CANONICAL_TOOL_COUNT,
                "public": list(AAA_CANONICAL_TOOLS),
                "archived": sorted(ARCHIVED_TOOLS),
            },
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
