"""
arifOS MCP Streamable HTTP Transport (FastMCP)
HTTP transport for remote clients and production deployment.

v55.1: Streamable HTTP (spec 2025-03-26+), stateless mode,
       localhost binding for local dev.
       Fixed resource/prompt registration to use FastMCP types.
"""

import logging
import os

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import Prompt as FastMCPPrompt
from mcp.server.fastmcp.resources import FunctionResource
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ..core.session_context import get_current_session_id, set_current_session_id
from ..core.tool_registry import ToolRegistry
from ..services.constitutional_metrics import get_full_metrics
from ..services.rate_limiter import rate_limited
from .base import BaseTransport
from .rest_api import RESTAPIRouter

logger = logging.getLogger(__name__)

# Security: bind to localhost for local dev, 0.0.0.0 only when HOST env is set
_DEFAULT_HOST = os.getenv("HOST", "127.0.0.1")
_DEFAULT_PORT = int(os.getenv("PORT", 8080))


class SSETransport(BaseTransport):
    """Streamable HTTP Transport implementation using FastMCP."""

    def __init__(self, tool_registry: ToolRegistry):
        super().__init__(tool_registry)
        self.mcp = FastMCP(
            "AAA-MCP-CODEBASE",
            host=_DEFAULT_HOST,
            port=_DEFAULT_PORT,
            stateless_http=True,
            json_response=True,
        )
        self.rest_router = RESTAPIRouter(tool_registry, self.mcp)
        self._register_routes()
        self.rest_router.register_all_routes()

    @property
    def name(self) -> str:
        return "streamable-http"

    async def start(self) -> None:
        """Start the FastMCP server with Streamable HTTP transport."""
        # Register tools dynamically
        for tool_name, tool_def in self.tool_registry.list_tools().items():
            # Apply constitutionally mandated rate limiting
            base_handler = tool_def.handler

            # Wrap handler for implicit session binding
            async def session_wrapped_handler(*args, **kwargs):
                # 1. Capture session from header if available (via starlette request if FastMCP exposes it)
                # Note: FastMCP tool handlers can optionally take a 'request' arg

                # 2. Check explicit session_id in kwargs
                session_id = kwargs.get("session_id") or get_current_session_id()
                if session_id:
                    set_current_session_id(session_id)
                    if "session_id" not in kwargs:
                        kwargs["session_id"] = session_id

                # 3. Execute
                result = await base_handler(*args, **kwargs)

                # 4. Update implicit context if result contains a new session_id
                new_session_id = result.get("session_id")
                if new_session_id:
                    set_current_session_id(new_session_id)

                return result

            handler = rate_limited(tool_name)(session_wrapped_handler)

            # FastMCP tool registration with annotations
            tool_kwargs = {
                "name": tool_def.name,
                "description": tool_def.description,
            }
            if tool_def.annotations:
                tool_kwargs["annotations"] = tool_def.annotations
            self.mcp.add_tool(handler, **tool_kwargs)
            logger.info(f"Registered HTTP tool: {tool_name}")

        # Register MCP Resources and Prompts
        self._register_resources()
        self._register_prompts()

        logger.info(f"Starting Streamable HTTP Transport on {_DEFAULT_HOST}:{_DEFAULT_PORT}")

        # Run using uvicorn programmatically
        asgi_app = self.mcp.streamable_http_app()

        # Add implicit session binding middleware
        @asgi_app.middleware("http")
        async def session_binding_middleware(request, call_next):
            session_id = request.headers.get("X-arifOS-Session")
            if session_id:
                set_current_session_id(session_id)
            return await call_next(request)

        config = uvicorn.Config(
            asgi_app,
            host=_DEFAULT_HOST,
            port=_DEFAULT_PORT,
            log_level="info",
            loop="asyncio",
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def stop(self) -> None:
        # Uvicorn handles shutdown on signal
        pass

    async def send_response(self, request_id: str, response: dict) -> None:
        pass  # Handled internally

    def _register_routes(self):
        """Register custom routes (Health, Metrics, Dashboard)."""

        @self.mcp.custom_route("/health", methods=["GET"])
        async def health_check(request):
            from codebase.mcp.maintenance import health_check as deep_health_check

            health = deep_health_check()
            health["transport"] = "streamable-http"
            health["mode"] = "CODEBASE"
            health["tools"] = len(self.tool_registry.list_tools())
            return JSONResponse(health)

        @self.mcp.custom_route("/metrics/json", methods=["GET"])
        async def metrics_endpoint(request):
            return JSONResponse(get_full_metrics())

        @self.mcp.custom_route("/", methods=["GET"])
        async def root(request):
            """Root endpoint - serve MIND Layer Engine status."""
            return JSONResponse(
                {
                    "layer": "MIND",
                    "engine": "arifOS Metabolic Kernel",
                    "status": "ONLINE",
                    "version": "v55.2-AAA",
                    "message": "DITEMPA BUKAN DIBERI",
                    "endpoints": {
                        "health": "/health",
                        "metrics": "/metrics/json",
                        "mcp": "/mcp",
                        "routes": "/routes",
                        "api_tools": "/api/tools",
                        "api_vault": "/api/vault",
                        "vault_legacy": "/vault",
                    },
                }
            )

        # VAULT999 REST Endpoints
        self._register_vault_routes()

    def _register_vault_routes(self):
        """Register VAULT999 REST API endpoints."""
        from starlette.requests import Request

        @self.mcp.custom_route("/vault", methods=["POST"])
        async def vault_endpoint(request: Request):
            """
            VAULT999 REST API - Direct vault access.

            Actions:
            - seal: Create a new seal
            - read: Read a specific seal by sequence
            - list: List seals with pagination
            - verify: Verify chain integrity
            - proof: Get Merkle proof for a sequence
            """
            try:
                from codebase.vault import get_vault_ledger
                from codebase.vault.migrations.run_migrations import ensure_vault_tables

                body = await request.json()
                action = body.get("action", "list")

                # Ensure tables exist
                await ensure_vault_tables()

                ledger = get_vault_ledger()
                await ledger.connect()

                try:
                    if action == "seal":
                        session_id = body.get("session_id", "rest-api")
                        verdict = body.get("verdict", "SEAL")
                        authority = body.get("authority", "api")
                        payload = body.get("payload", {})

                        receipt = await ledger.append(
                            session_id=session_id,
                            verdict=verdict,
                            seal_data=payload,
                            authority=authority,
                        )
                        return JSONResponse(
                            {
                                "operation": "sealed",
                                "verdict": verdict,
                                "sealed": receipt,
                                "vault_backend": "postgres",
                                "authority_notice": "This seal is generated by arifOS infrastructure. ChatGPT/LLM is only the caller, not the authority.",
                            }
                        )

                    elif action == "read":
                        sequence = body.get("sequence")
                        if sequence is None:
                            return JSONResponse({"error": "sequence required"}, status_code=400)

                        entry = await ledger.get_entry_by_sequence(sequence)
                        if entry:
                            return JSONResponse(
                                {"operation": "read", "entry": entry, "vault_backend": "postgres"}
                            )
                        return JSONResponse({"error": "Seal not found"}, status_code=404)

                    elif action == "list":
                        cursor = body.get("cursor")
                        limit = body.get("limit", 50)

                        result = await ledger.list_entries(cursor=cursor, limit=limit)
                        return JSONResponse(
                            {
                                "operation": "list",
                                "entries": result["entries"],
                                "next_cursor": result.get("next_cursor"),
                                "has_more": result.get("has_more"),
                                "vault_backend": "postgres",
                            }
                        )

                    elif action == "verify":
                        result = await ledger.verify_chain()
                        return JSONResponse(
                            {"operation": "verify", "result": result, "vault_backend": "postgres"}
                        )

                    elif action == "proof":
                        sequence = body.get("sequence")
                        if sequence is None:
                            return JSONResponse({"error": "sequence required"}, status_code=400)

                        proof = await ledger.get_merkle_proof(sequence)
                        if proof:
                            return JSONResponse(
                                {"operation": "proof", "proof": proof, "vault_backend": "postgres"}
                            )
                        return JSONResponse({"error": "Proof not found"}, status_code=404)

                    else:
                        return JSONResponse({"error": f"Unknown action: {action}"}, status_code=400)

                finally:
                    await ledger.close()

            except Exception as e:
                logger.error(f"Vault endpoint error: {e}")
                return JSONResponse({"error": str(e)}, status_code=500)

        @self.mcp.custom_route("/vault/health", methods=["GET"])
        async def vault_health(request):
            """VAULT999 health check."""
            try:
                from codebase.vault import get_vault_dsn, should_use_postgres
                from codebase.vault.migrations.run_migrations import ensure_vault_tables

                if not should_use_postgres():
                    return JSONResponse(
                        {
                            "status": "filesystem",
                            "message": "Using filesystem backend (not PostgreSQL)",
                        }
                    )

                # Try to connect and check tables
                from codebase.vault import get_vault_ledger

                ledger = get_vault_ledger()
                await ledger.connect()

                try:
                    await ensure_vault_tables()
                    entries = await ledger.list_entries(limit=1)

                    return JSONResponse(
                        {
                            "status": "healthy",
                            "backend": "postgres",
                            "entries": len(entries["entries"]),
                            "has_more": entries.get("has_more", False),
                        }
                    )
                finally:
                    await ledger.close()

            except Exception as e:
                return JSONResponse({"status": "error", "error": str(e)}, status_code=503)

    def _register_resources(self):
        """Register MCP Resources using FastMCP FunctionResource."""
        for res_def in self.resource_registry.list_resources():
            # Capture uri in closure to avoid late-binding bug
            uri = res_def.uri
            resource = FunctionResource(
                uri=uri,
                name=res_def.name,
                description=res_def.description,
                mime_type=res_def.mime_type,
                fn=lambda _uri=uri: self.resource_registry.read_resource(_uri),
            )
            self.mcp.add_resource(resource)
            logger.info(f"Registered resource: {uri}")

    def _register_prompts(self):
        """Register MCP Prompts using FastMCP Prompt type."""
        for prompt_def in self.prompt_registry.list_prompts():
            # Capture name in closure
            pname = prompt_def.name
            prompt = FastMCPPrompt(
                name=pname,
                description=prompt_def.description,
                fn=lambda _name=pname, **kwargs: self.prompt_registry.render_prompt(
                    _name, kwargs if kwargs else None
                ),
            )
            self.mcp.add_prompt(prompt)
            logger.info(f"Registered prompt: {pname}")
            logger.info(f"Registered prompt: {pname}")
