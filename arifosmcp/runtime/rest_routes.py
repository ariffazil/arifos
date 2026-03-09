"""REST endpoints for the unified arifOS AAA MCP server.

Registered as custom routes on the FastMCP instance via mcp.custom_route().
These run alongside the standard MCP protocol at /mcp, providing:
  GET  /                           Landing page / service info
  GET  /health                     Docker healthcheck + monitoring
  GET  /version                    Build info
  GET  /tools                      Tool listing (REST-style)
  POST /tools/{tool_name}          REST tool calling (ChatGPT adapter)
  GET  /.well-known/mcp/server.json  MCP registry discovery

DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import inspect
import json
import logging
import os
import secrets
import time
import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.staticfiles import StaticFiles

from arifosmcp.runtime.resources import apex_tools_html_rows, apex_tools_markdown_table
from arifosmcp.transport.build_info import get_build_info
from arifosmcp.transport.protocol.aaa_contract import AAA_TOOL_STAGE_MAP, TRINITY_BY_TOOL
from arifosmcp.transport.protocol.public_surface import PUBLIC_TOOL_ALIASES
from core.shared.floor_audit import get_ml_floor_runtime
from core.shared.floors import (
    FLOOR_SPEC_KEYS,
    get_floor_comparator,
    get_floor_spec,
    get_floor_threshold,
)

BUILD_INFO = get_build_info()
MCP_PROTOCOL_VERSION = "2025-11-25"
MCP_SUPPORTED_PROTOCOL_VERSIONS = ["2025-11-25", "2025-03-26"]

TOOL_ALIASES: dict[str, str] = dict(PUBLIC_TOOL_ALIASES)

logger = logging.getLogger(__name__)


def _representative_floor_score(floor_id: str) -> float:
    """
    Build a visualizer-friendly fallback score from canonical core floor specs.

    This intentionally stays transport-agnostic by deriving from core as source-of-truth.
    """
    comparator = get_floor_comparator(floor_id)
    threshold = float(get_floor_threshold(floor_id))
    spec = get_floor_spec(floor_id)

    if floor_id == "F7" and "range" in spec:
        low, _high = spec["range"]
        return float(low) + 0.01  # representative in-band humility value

    if comparator in {">", ">="}:
        return threshold
    if comparator == "<=":
        return threshold
    # "<" comparators (e.g., risk-style floors) — choose conservative passing value
    return threshold * 0.5


def _canonical_floor_defaults() -> dict[str, float]:
    return {fid: _representative_floor_score(fid) for fid in FLOOR_SPEC_KEYS}


# Fallback floor defaults used only when live governance kernel state is unavailable.
_FLOOR_DEFAULTS: dict[str, float] = _canonical_floor_defaults()

# Fallback Tri-Witness weights (normalised to sum to 1.0).
# Reflects approximate sovereign split: Human 42%, AI 32%, Earth 26%.
_WITNESS_DEFAULTS: dict[str, float] = {"human": 0.42, "ai": 0.32, "earth": 0.26}

# Default QDF (Quantum Decision Field) baseline — target ≥ 0.83 per APEX solver spec.
_DEFAULT_QDF: float = 0.83

# Default metabolic stage returned when kernel state is unavailable.
# 333 = REASON stage, the last full AGI reasoning stage before TRINITY_SYNC.
_DEFAULT_METABOLIC_STAGE: int = 333

WELCOME_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>arifOS MCP Server</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0d0d0d;color:#d4d4d4;font-family:ui-monospace,monospace;
         font-size:14px;line-height:1.6;padding:2rem 1rem;max-width:860px;margin:auto}
    h1{color:#e6c25d;font-size:1.5rem;margin-bottom:.25rem}
    h2{color:#aaa;font-size:.85rem;font-weight:normal;margin-bottom:2rem;
       letter-spacing:.08em;text-transform:uppercase}
    .pill{display:inline-block;background:#00ff8822;color:#00ff88;
          border:1px solid #00ff8855;border-radius:99px;
          padding:.1rem .75rem;font-size:.75rem;margin-bottom:2rem}
    section{margin-bottom:2.5rem}
    h3{color:#e6c25d;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;
       border-bottom:1px solid #333;padding-bottom:.4rem;margin-bottom:.75rem}
    table{width:100%;border-collapse:collapse}
    td,th{padding:.4rem .6rem;text-align:left}
    th{color:#888;font-weight:normal;font-size:.75rem;text-transform:uppercase}
    tr:nth-child(odd){background:#ffffff06}
    .stage{color:#e6c25d;font-size:.75rem;min-width:3.5rem;display:inline-block}
    .name{color:#7dd3fc}
    .role{color:#aaa}
    .url{color:#7dd3fc}
    a{color:#7dd3fc;text-decoration:none}
    a:hover{text-decoration:underline}
    .nav{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2rem}
    .nav a{background:#1a1a1a;border:1px solid #333;padding:.3rem .8rem;
           border-radius:4px;font-size:.8rem;color:#aaa}
    .nav a:hover{border-color:#7dd3fc;color:#7dd3fc}
    .motto{color:#555;font-size:.75rem;margin-top:2rem;text-align:center}
  </style>
</head>
<body>
  <h1>arifOS MCP</h1>
  <h2>APEX-G Constitutional Intelligence Kernel</h2>
  <div class="pill">&#9679; ONLINE</div>

  <div class="nav">
    <a href="/tools">/tools</a>
    <a href="/health">/health</a>
    <a href="/version">/version</a>
    <a href="/openapi.json">/openapi.json</a>
    <a href="/llms.txt">/llms.txt</a>
    <a href="/.well-known/mcp/server.json">/.well-known/mcp/server.json</a>
    <a href="https://arifos.arif-fazil.com" target="_blank">docs</a>
  </div>

  <section>
    <h3>10-Tool APEX-G Stack (Phase 1 Core)</h3>
    <table>
      <tr><th>Stage</th><th>Runtime Tool</th><th>Canonical Handle</th><th>Label</th><th>Role</th></tr>
      __APEX_HTML_ROWS__
    </table>
  </section>

  <section>
    <h3>Endpoints</h3>
    <table>
      <tr><th>Method</th><th>Path</th><th>Description</th></tr>
      <tr><td>GET</td><td class="url">/mcp</td><td>MCP protocol endpoint (SSE / JSON-RPC)</td></tr>
      <tr><td>GET</td><td class="url">/tools</td><td>Tool listing (REST)</td></tr>
      <tr><td>POST</td><td class="url">/tools/{name}</td><td>Call a tool via HTTP</td></tr>
      <tr><td>POST</td><td class="url">/checkpoint</td><td>Single-call constitutional evaluation</td></tr>
      <tr><td>GET</td><td class="url">/health</td><td>Docker / uptime health check</td></tr>
      <tr><td>GET</td><td class="url">/openapi.json</td><td>OpenAPI 3.1 schema</td></tr>
      <tr><td>GET</td><td class="url">/llms.txt</td><td>LLM-readable server description</td></tr>
      <tr><td>GET</td><td class="url">/.well-known/mcp/server.json</td><td>MCP registry discovery</td></tr>
    </table>
  </section>

  <section>
    <h3>Governance</h3>
    <p style="color:#888">
      Every tool call passes through 13 constitutional floors (F1&ndash;F13).<br>
      Verdicts: <strong style="color:#00ff88">SEAL</strong> &nbsp;
                <strong style="color:#e6c25d">PARTIAL</strong> &nbsp;
                <strong style="color:#ff8800">HOLD-888</strong> &nbsp;
                <strong style="color:#ff4444">VOID</strong> &nbsp;
                <strong style="color:#ff4444">SABAR</strong><br>
      Protocol: <a href="https://modelcontextprotocol.io" target="_blank">MCP 2025-11-25</a>
    </p>
  </section>

  <div class="motto">DITEMPA BUKAN DIBERI &mdash; Forged, not given.</div>
</body>
</html>
"""

ROBOTS_TXT = """\
User-agent: *
Allow: /

# LLM-readable description of this service
# See: https://llmstxt.org
Sitemap: https://arifosmcp.arif-fazil.com/llms.txt
"""

LLMS_TXT = """\
# arifOS MCP Server

> APEX-G Constitutional Intelligence Kernel — a governed Model Context Protocol (MCP) server.
> Motto: DITEMPA BUKAN DIBERI — Forged, not given.

## What this server does

arifOS is an MCP server exposing a 10-tool constitutional AI pipeline.
Every tool call passes through 13 governance floors (F1-F13) and returns
a structured RuntimeEnvelope with verdict, telemetry, and Tri-Witness scores.

## MCP connection

- Protocol: Model Context Protocol (MCP) 2025-11-25
- Endpoint: /mcp  (SSE + JSON-RPC)
- Tool listing: GET /tools
- Single call: POST /checkpoint

## The 10-tool APEX-G stack

__APEX_MD_TABLE__

## Common RuntimeEnvelope (returned by every tool)

```json
{
  "verdict": "SEAL | PARTIAL | SABAR | VOID | HOLD-888 | UNSET",
  "stage": "000_INIT | 111_MIND | 333_MIND | 444_ROUTER | 555_MEMORY | 666_HEART | 777_APEX | 888_JUDGE | 999_VAULT",
  "session_id": "string",
  "telemetry": { "dS": -0.7, "peace2": 1.1, "confidence": 0.9, "verdict": "Alive" },
  "witness": { "human": 0.0, "ai": 0.0, "earth": 0.0 },
  "auth_context": { "actor_id": "string", "authority_level": "human|agent|system|anonymous", "stakes_class": "A|B|C|UNKNOWN" },
  "data": {}
}
```

## Governance floors summary

- Hard floors (fail -> VOID): F1 Amanah, F2 Truth, F4 Clarity, F7 Humility, F9 Anti-dark, F10 Ontology, F11 Command Auth, F12 Injection Defense
- Soft floors (fail -> PARTIAL): F3 Tri-Witness, F5 Peace, F6 Empathy, F8 Genius
- Veto: F13 Sovereign — human final authority

## Key endpoints

- GET  /tools                        — list all tools with schemas
- POST /tools/{tool_name}            — call a tool via REST
- POST /checkpoint                   — single-call constitutional evaluation
- GET  /health                       — health check
- GET  /openapi.json                 — OpenAPI 3.1 schema
- GET  /.well-known/mcp/server.json  — MCP registry discovery
- GET  /llms.txt                     — this file

## Optional: quick test

```
POST /checkpoint
Content-Type: application/json

{ "query": "Should I deploy this to production?", "risk_tier": "high" }
```

## Links

- Docs: https://arifos.arif-fazil.com
- Protocol: https://modelcontextprotocol.io
"""

WELCOME_HTML = WELCOME_HTML.replace("__APEX_HTML_ROWS__", apex_tools_html_rows())
LLMS_TXT = LLMS_TXT.replace("__APEX_MD_TABLE__", apex_tools_markdown_table())

CHECKPOINT_MODES = {"quick", "full", "audit_only"}
RISK_TIER_BY_MODE = {
    "quick": "low",
    "full": "medium",
    "audit_only": "medium",
}


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _required_bearer_token() -> str | None:
    return os.getenv("ARIFOS_API_KEY") or os.getenv("ARIFOS_API_TOKEN")


def _auth_error_response(request: Request) -> JSONResponse | None:
    """Enforce Bearer auth when configured."""
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


def _normalize_tool_name(raw_name: str) -> str:
    """Normalize tool path params so trailing slashes do not break alias resolution."""
    return (raw_name or "").strip().strip("/")


def _public_base_url(request: Request) -> str:
    explicit = os.getenv("ARIFOS_PUBLIC_BASE_URL", "").strip().rstrip("/")
    if explicit:
        return explicit
    scheme = request.headers.get("x-forwarded-proto") or request.url.scheme or "https"
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or "localhost"
    return f"{scheme}://{host}".rstrip("/")


def _openapi_schema(base_url: str) -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "arifOS Checkpoint REST API",
            "version": BUILD_INFO["version"],
            "description": (
                "Minimal REST/OpenAPI compatibility surface for arifOS constitutional "
                "evaluation. Primary endpoint: POST /checkpoint. This is not the MCP "
                "transport; remote MCP clients should connect to `/mcp`."
            ),
        },
        "servers": [{"url": base_url}],
        "paths": {
            "/checkpoint": {
                "post": {
                    "operationId": "evaluateCheckpoint",
                    "summary": "Constitutional checkpoint evaluation",
                    "description": (
                        "Runs governed evaluation through arifOS and returns verdict + telemetry."
                    ),
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CheckpointRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Checkpoint completed",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/CheckpointResponse"}
                                }
                            },
                        },
                        "400": {
                            "description": "Invalid request",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                        "401": {
                            "description": "Unauthorized",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                        "500": {
                            "description": "Internal error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                    },
                }
            },
            "/health": {
                "get": {
                    "operationId": "getHealth",
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "Service healthy",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "CheckpointRequest": {
                    "type": "object",
                    "required": ["task"],
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "User query/task to evaluate constitutionally.",
                        },
                        "mode": {
                            "type": "string",
                            "enum": sorted(CHECKPOINT_MODES),
                            "default": "full",
                            "description": "Execution profile for checkpoint evaluation.",
                        },
                        "actor_id": {
                            "type": "string",
                            "default": "chatgpt-action",
                            "description": "Caller identity for audit trail.",
                        },
                        "context": {
                            "description": "Optional context payload.",
                            "oneOf": [{"type": "string"}, {"type": "object"}, {"type": "array"}],
                        },
                        "risk_tier": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Optional risk override. If omitted, derived from mode.",
                        },
                        "debug": {"type": "boolean", "default": False},
                    },
                },
                "CheckpointResponse": {
                    "type": "object",
                    "properties": {
                        "verdict": {"type": "string"},
                        "session_id": {"type": "string"},
                        "request_id": {"type": "string"},
                        "latency_ms": {"type": "number"},
                        "mode": {"type": "string"},
                        "risk_tier": {"type": "string"},
                        "metrics": {"type": "object"},
                        "floors": {"type": "object"},
                        "result": {"type": "object"},
                    },
                    "required": ["verdict", "request_id", "latency_ms"],
                },
                "HealthResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "service": {"type": "string"},
                        "version": {"type": "string"},
                        "transport": {"type": "string"},
                        "tools_loaded": {"type": "integer"},
                        "timestamp": {"type": "string"},
                    },
                    "required": ["status", "service", "version", "transport"],
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                        "error_description": {"type": "string"},
                        "request_id": {"type": "string"},
                    },
                    "required": ["error"],
                },
            }
        },
    }


def register_rest_routes(mcp: Any, tool_registry: dict[str, Callable]) -> None:
    """Register REST endpoints as custom routes on the FastMCP instance.

    Args:
        mcp: The FastMCP server instance.
        tool_registry: Mapping of canonical tool names to async callables.
    """

    @mcp.custom_route("/", methods=["GET"])
    async def root(request: Request) -> Response:
        accept = request.headers.get("Accept", "")
        if "text/html" in accept:
            return HTMLResponse(WELCOME_HTML)
        return JSONResponse(
            {
                "service": "arifOS AAA MCP Server",
                "version": BUILD_INFO["version"],
                "protocol_version": MCP_PROTOCOL_VERSION,
                "supported_protocol_versions": MCP_SUPPORTED_PROTOCOL_VERSIONS,
                "mcp_endpoint": "/mcp",
                "tools_endpoint": "/tools",
                "health_endpoint": "/health",
                "tool_count": len(tool_registry),
                "tools": list(tool_registry.keys()),
            }
        )

    @mcp.custom_route("/health", methods=["GET"])
    async def health(request: Request) -> Response:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "arifos-aaa-mcp",
                "version": BUILD_INFO["version"],
                "transport": "streamable-http",
                "tools_loaded": len(tool_registry),
                "ml_floors": get_ml_floor_runtime(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @mcp.custom_route("/version", methods=["GET"])
    async def version(request: Request) -> Response:
        return JSONResponse(BUILD_INFO)

    @mcp.custom_route("/tools", methods=["GET"])
    async def list_tools(request: Request) -> Response:
        if err := _auth_error_response(request):
            return err

        # Get tools from mcp instance
        mcp_tools = await mcp.list_tools()
        tool_list = []
        for tool in mcp_tools:
            tool_list.append(
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.parameters or {},
                    "stage": AAA_TOOL_STAGE_MAP.get(tool.name),
                    "lane": TRINITY_BY_TOOL.get(tool.name),
                }
            )
        return JSONResponse({"tools": tool_list, "count": len(tool_list)})

    @mcp.custom_route("/tools/", methods=["GET"])
    async def list_tools_slash(request: Request) -> Response:
        return await list_tools(request)

    @mcp.custom_route("/openapi.json", methods=["GET"])
    async def openapi_json(request: Request) -> Response:
        schema = _openapi_schema(_public_base_url(request))
        return JSONResponse(schema)

    @mcp.custom_route("/tools/{tool_name:path}", methods=["POST"])
    async def call_tool_rest(request: Request) -> Response:
        """REST-style tool calling for ChatGPT and other HTTP clients."""
        if err := _auth_error_response(request):
            return err

        incoming_name = _normalize_tool_name(request.path_params.get("tool_name", ""))
        canonical_name = TOOL_ALIASES.get(incoming_name, incoming_name)
        request_id = f"req-{uuid.uuid4().hex[:12]}"
        start_time = time.time()

        if canonical_name not in tool_registry:
            return JSONResponse(
                {"error": f"Tool '{incoming_name}' not found", "request_id": request_id},
                status_code=404,
            )

        try:
            body = await request.json()
        except Exception:
            body = {}
        if not isinstance(body, dict):
            body = {}

        tool_obj = tool_registry[canonical_name]
        tool_fn = getattr(tool_obj, "fn", tool_obj)

        try:
            # Filter body to only valid parameters
            sig = inspect.signature(tool_fn)
            has_kwargs = any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
            )
            if has_kwargs:
                filtered = body
            else:
                valid_params = {
                    name
                    for name, p in sig.parameters.items()
                    if p.kind
                    not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                }
                filtered = {k: v for k, v in body.items() if k in valid_params}

            result = await tool_fn(**filtered)
        except Exception as exc:
            return JSONResponse(
                {"error": str(exc), "tool": incoming_name, "request_id": request_id},
                status_code=500,
            )

        latency_ms = (time.time() - start_time) * 1000
        
        # Handle RuntimeEnvelope and other Pydantic models serialization
        if hasattr(result, "model_dump"):
            # Pydantic v2
            result_dict = result.model_dump()
        elif hasattr(result, "dict"):
            # Pydantic v1
            result_dict = result.dict()
        else:
            result_dict = result
        
        return JSONResponse(
            {
                "status": "success",
                "tool": incoming_name,
                "canonical": canonical_name,
                "request_id": request_id,
                "latency_ms": round(latency_ms, 2),
                "result": result_dict,
            }
        )

    @mcp.custom_route("/.well-known/mcp/server.json", methods=["GET"])
    async def well_known(request: Request) -> Response:
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "server.json")
        if os.path.exists(static_path):
            with open(static_path) as f:
                payload = json.load(f)
                payload.setdefault("protocolVersion", MCP_PROTOCOL_VERSION)
                payload.setdefault("supportedProtocolVersions", MCP_SUPPORTED_PROTOCOL_VERSIONS)
                payload.setdefault(
                    "authentication",
                    {
                        "type": "none",
                        "description": "No authentication required. actor_id is used for logging only.",
                    },
                )
                return JSONResponse(payload)
        # Fallback: generate minimal discovery
        return JSONResponse(
            {
                "name": "arifOS AAA MCP",
                "version": BUILD_INFO["version"],
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "supportedProtocolVersions": MCP_SUPPORTED_PROTOCOL_VERSIONS,
                "transport": {"type": "streamable-http", "url": "/mcp"},
                "authentication": {
                    "type": "none",
                    "description": "No authentication required. actor_id is used for logging only.",
                },
                "tools": list(tool_registry.keys()),
            }
        )

    @mcp.custom_route("/api/governance-status", methods=["GET"])
    async def governance_status(request: Request) -> Response:
        """Return current governance telemetry for the Constitutional Visualizer."""
        try:
            session_id: str | None = None
            floors: dict[str, Any] = {}
            telemetry: dict[str, Any] = {}
            witness: dict[str, float] = {}
            qdf: float = 0.0
            metabolic_stage: int = 0
            verdict: str = "SEAL"

            # Attempt to load live session data from the governance kernel
            try:
                from core.governance_kernel import get_governance_kernel

                kernel = get_governance_kernel()
                state = kernel.get_current_state() if hasattr(kernel, "get_current_state") else {}
                if state:
                    session_id = state.get("session_id")
                    floors = state.get("floors", {})
                    telemetry = state.get("telemetry", {})
                    witness = state.get("witness", {})
                    qdf = float(state.get("qdf", 0.0))
                    metabolic_stage = int(state.get("metabolic_stage", 0))
                    verdict = state.get("verdict", "SEAL")
            except (ImportError, AttributeError):
                logger.debug("Governance kernel unavailable — using default telemetry values")
            except Exception:
                logger.exception("Unexpected error loading governance kernel state")

            # Build normalised floor map (F1–F13) using canonical defaults
            resolved_floors = {k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}

            resolved_witness = {k: witness.get(k, v) for k, v in _WITNESS_DEFAULTS.items()}

            resolved_telemetry = {
                "dS": telemetry.get("dS", -0.35),
                "peace2": telemetry.get("peace2", 1.04),
                "kappa_r": telemetry.get("kappa_r", 0.97),
                "echoDebt": telemetry.get("echoDebt", 0.4),
                "shadow": telemetry.get("shadow", 0.3),
                "confidence": telemetry.get("confidence", 0.88),
                "psi_le": telemetry.get("psi_le", 0.82),
                "verdict": verdict,
            }

            return JSONResponse(
                {
                    "telemetry": resolved_telemetry,
                    "witness": resolved_witness,
                    "qdf": qdf or _DEFAULT_QDF,
                    "floors": resolved_floors,
                    "session_id": session_id or f"sess_{uuid.uuid4().hex[:8]}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "metabolic_stage": metabolic_stage or _DEFAULT_METABOLIC_STAGE,
                }
            )
        except Exception as exc:
            logger.exception("governance_status endpoint failed")
            return JSONResponse(
                {"error": "governance_status_failed", "detail": str(exc)},
                status_code=500,
            )

    @mcp.custom_route("/api/governance-history", methods=["GET"])
    async def governance_history(request: Request) -> Response:
        """Return recent VAULT999 session history for the Constitutional Visualizer."""
        try:
            limit_raw = request.query_params.get("limit", "20")
            try:
                limit = max(1, min(int(limit_raw), 100))
            except (ValueError, TypeError):
                limit = 20

            sessions: list[dict[str, Any]] = []

            # Attempt to query VAULT999 for real session history
            try:
                from arifosmcp.transport.vault_sqlite import VaultSQLite

                vault = VaultSQLite()
                raw = vault.query_recent(limit=limit) if hasattr(vault, "query_recent") else []
                for entry in raw:
                    sessions.append(
                        {
                            "session_id": entry.get("session_id", ""),
                            "verdict": entry.get("verdict", "UNKNOWN"),
                            "stage": entry.get("stage", ""),
                            "timestamp": entry.get("timestamp", ""),
                            "floors": entry.get("floors", {}),
                        }
                    )
            except (ImportError, AttributeError):
                logger.debug("VAULT999 SQLite unavailable — returning empty session history")
            except Exception:
                logger.exception("Unexpected error querying VAULT999 history")

            return JSONResponse(
                {
                    "sessions": sessions,
                    "count": len(sessions),
                    "limit": limit,
                }
            )
        except Exception as exc:
            logger.exception("governance_history endpoint failed")
            return JSONResponse(
                {"error": "governance_history_failed", "detail": str(exc)},
                status_code=500,
            )

    # ═══════════════════════════════════════════════════════
    # CHECKPOINT REST COMPATIBILITY — OpenAPI / action-style integration
    # ═══════════════════════════════════════════════════════

    @mcp.custom_route("/checkpoint", methods=["POST"])
    async def checkpoint_endpoint(request: Request) -> Response:
        """
        REST/OpenAPI compatibility entry point for constitutional validation.
        Simplified 000→888 pipeline for non-MCP clients.
        """
        if err := _auth_error_response(request):
            return err

        try:
            body = await request.json()
        except Exception:
            body = {}

        # Support both 'query' and 'task' parameters for compatibility
        query = body.get("query") or body.get("task", "")
        body.get("stakeholders", ["user"])
        actor_id = body.get("actor_id", "chatgpt")
        mode = body.get("mode", "full")

        if not query or not isinstance(query, str):
            return JSONResponse(
                {"error": "Missing required field: query (or task)"}, status_code=400
            )

        session_id = f"gpt-{actor_id}-{uuid.uuid4().hex[:8]}"
        start_time = time.time()

        try:
            # Get tools from registry (using canonical APEX-G tool names)
            anchor_tool = tool_registry.get("init_anchor_state")
            reason_tool = tool_registry.get("reason_mind_synthesis")
            heart_tool = tool_registry.get("assess_heart_impact")
            judge_tool = tool_registry.get("apex_judge_verdict")

            if not all([anchor_tool, reason_tool, heart_tool, judge_tool]):
                return JSONResponse(
                    {"error": "Required tools not available", "verdict": "VOID"}, status_code=500
                )

            # 000_INIT
            anchor_fn = getattr(anchor_tool, "fn", anchor_tool)
            anchor_res = await anchor_fn(
                intent={"query": query, "purpose": "checkpoint", "actor_id": actor_id}
            )
            anchor_data = anchor_res.model_dump() if hasattr(anchor_res, "model_dump") else anchor_res
            cid = anchor_data.get("session_id", session_id)

            # 111-444_AGI
            reason_fn = getattr(reason_tool, "fn", reason_tool)
            await reason_fn(
                query=query, 
                session_id=cid,
                auth_context={"actor_id": actor_id, "authority_level": "agent"}
            )

            # 555-666_ASI
            heart_fn = getattr(heart_tool, "fn", heart_tool)
            await heart_fn(
                scenario=query, 
                session_id=cid,
                auth_context={"actor_id": actor_id, "authority_level": "agent"}
            )

            # 777-888_APEX
            judge_fn = getattr(judge_tool, "fn", judge_tool)
            judge_res = await judge_fn(
                session_id=cid, 
                verdict_candidate="checkpoint_evaluation",
                reason_summary=query,
                auth_context={"actor_id": actor_id, "authority_level": "agent"}
            )

            # Extract data from RuntimeEnvelope responses
            judge_data = judge_res.model_dump() if hasattr(judge_res, "model_dump") else judge_res
            verdict = judge_data.get("verdict", "VOID")
            
            # Extract floors from nested data structure
            floors_passed = []
            floors_failed = []
            truth_score = None
            truth_threshold = None
            
            if "data" in judge_data and isinstance(judge_data["data"], dict):
                data = judge_data["data"]
                # Try nested apex_output structure
                if "apex_output" in data:
                    apex = data["apex_output"]
                    if "governance_layer" in apex:
                        gov = apex["governance_layer"]
                        floors_passed = [k for k, v in gov.items() if v == "pass"]
                        floors_failed = [k for k, v in gov.items() if v != "pass" and k != "vitality_index"]
                    if "governed_intelligence" in apex:
                        gi = apex["governed_intelligence"]
                        truth_score = gi.get("G_star")
                        truth_threshold = 0.5
                # Also check for direct floors/truth
                if not floors_passed and not floors_failed:
                    floors_passed = data.get("floors", {}).get("passed", [])
                    floors_failed = data.get("floors", {}).get("failed", [])
                if truth_score is None:
                    truth_score = data.get("truth", {}).get("score")
                    truth_threshold = data.get("truth", {}).get("threshold", 0.5)
            
            floors = {"passed": floors_passed, "failed": floors_failed}
            truth = {"score": truth_score, "threshold": truth_threshold}

            # Build human-readable summary
            if verdict == "SEAL":
                summary = "✓ All constitutional floors passed. Safe to proceed."
            elif verdict == "PARTIAL":
                summary = "⚠ Soft floor warning. Proceed with caution."
            elif verdict == "VOID":
                if floors_failed:
                    summary = f"✗ Constitutional violation: {', '.join(floors_failed[:3])}. Action blocked."
                else:
                    summary = "✗ Constitutional evaluation returned VOID. Action blocked."
            elif verdict == "888_HOLD":
                summary = "⏸ High-stakes decision. Requires explicit human confirmation."
            else:
                summary = f"Status: {verdict}"

            latency_ms = (time.time() - start_time) * 1000

            return JSONResponse(
                {
                    "verdict": verdict,
                    "summary": summary,
                    "mode": mode,
                    "floors": {
                        "passed": floors.get("passed", []),
                        "failed": floors.get("failed", []),
                    },
                    "metrics": {"truth": truth.get("score"), "threshold": truth.get("threshold")},
                    "session_id": cid,
                    "latency_ms": round(latency_ms, 2),
                    "version": BUILD_INFO.get("version", "2026.3.1"),
                }
            )

        except Exception as exc:
            logger.exception("checkpoint_endpoint failed")
            return JSONResponse({"error": str(exc), "verdict": "VOID"}, status_code=500)

    @mcp.custom_route("/openapi.yaml", methods=["GET"])
    async def openapi_schema(request: Request) -> Response:
        """Serve OpenAPI schema for the REST compatibility surface."""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "333_APPS",
            "L4_TOOLS",
            "chatgpt-actions",
            "chatgpt_openapi.yaml",
        )
        if os.path.exists(schema_path):
            content = open(schema_path).read()
            return Response(content, media_type="application/yaml")
        return JSONResponse({"error": "Schema not found"}, status_code=404)

    @mcp.custom_route("/robots.txt", methods=["GET"])
    async def robots_txt(_request: Request) -> Response:
        return Response(ROBOTS_TXT, media_type="text/plain")

    @mcp.custom_route("/llms.txt", methods=["GET"])
    async def llms_txt(_request: Request) -> Response:
        return Response(LLMS_TXT, media_type="text/plain")

    # Serve the APEX Sovereign Dashboard at /dashboard/
    dashboard_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "sites",
        "apex-dashboard",
    )
    if os.path.exists(dashboard_dir) and hasattr(mcp, "_app"):
        mcp._app.mount(
            "/dashboard", StaticFiles(directory=dashboard_dir, html=True), name="dashboard"
        )
