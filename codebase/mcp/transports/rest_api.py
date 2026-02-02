"""
arifOS REST API Transport Layer
Exposes MCP tools as REST endpoints alongside MCP transport.

Routes:
- GET  /routes              -> List all registered routes
- GET  /api/tools           -> List tools with schemas
- POST /api/tools/{name}    -> Execute tool
- POST /api/vault           -> Vault compatibility endpoint
"""

import os
import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Security configuration
API_KEY = os.environ.get("API_KEY")
MAX_BODY_SIZE = 256 * 1024  # 256KB


def check_auth(request_headers: dict) -> tuple[bool, Optional[str]]:
    """Check API key authentication if configured."""
    if not API_KEY:
        return True, None
    
    provided_key = request_headers.get("x-api-key") or request_headers.get("X-API-Key")
    if not provided_key:
        return False, "Missing x-api-key header"
    
    # Use constant-time comparison to prevent timing attacks
    import hmac
    if not hmac.compare_digest(provided_key, API_KEY):
        return False, "Invalid API key"
    
    return True, None


def create_json_response(data: dict, status_code: int = 200) -> Any:
    """Create a JSON response compatible with Starlette."""
    from starlette.responses import JSONResponse
    return JSONResponse(data, status_code=status_code)


def validate_body_size(body: bytes) -> tuple[bool, Optional[str]]:
    """Check if body size is within limits."""
    if len(body) > MAX_BODY_SIZE:
        return False, f"Request body too large: {len(body)} bytes (max {MAX_BODY_SIZE})"
    return True, None


class RESTAPIRouter:
    """Router for REST API endpoints. Integrates with FastMCP/Starlette."""
    
    def __init__(self, tool_registry, mcp_server):
        self.tool_registry = tool_registry
        self.mcp = mcp_server
        self.routes = []  # Track registered routes for introspection
        
        if not API_KEY:
            logger.warning("API_KEY not set - REST API is open (dev mode). Set API_KEY env var for production.")
        else:
            logger.info("REST API authentication enabled")
    
    def register_all_routes(self):
        """Register all REST API routes."""
        self._register_routes_endpoint()
        self._register_tools_list_endpoint()
        self._register_tool_execute_endpoint()
        self._register_vault_compat_endpoint()
        logger.info(f"Registered {len(self.routes)} REST API routes")
    
    def _add_route(self, path: str, methods: list, handler_name: str):
        """Track registered routes for introspection."""
        for method in methods:
            self.routes.append({"method": method, "path": path, "handler": handler_name})
    
    def _register_routes_endpoint(self):
        """GET /routes - List all registered routes."""
        @self.mcp.custom_route("/routes", methods=["GET"])
        async def routes_endpoint(request):
            # Check auth
            ok, error = check_auth(dict(request.headers))
            if not ok:
                return create_json_response({
                    "ok": False,
                    "error": {"type": "auth", "message": error, "details": None}
                }, 401)
            
            # Get MCP tool routes too
            tools = self.tool_registry.list_tools()
            tool_routes = [{"method": "TOOL", "path": f"mcp://{name}", "handler": "mcp_tool"} 
                          for name in tools.keys()]
            
            return create_json_response({
                "ok": True,
                "routes": self.routes + tool_routes,
                "count": len(self.routes) + len(tool_routes)
            })
        
        self._add_route("/routes", ["GET"], "routes_endpoint")
    
    def _register_tools_list_endpoint(self):
        """GET /api/tools - List all tools with their schemas."""
        @self.mcp.custom_route("/api/tools", methods=["GET"])
        async def tools_list_endpoint(request):
            # Check auth
            ok, error = check_auth(dict(request.headers))
            if not ok:
                return create_json_response({
                    "ok": False,
                    "error": {"type": "auth", "message": error, "details": None}
                }, 401)
            
            tools = self.tool_registry.list_tools()
            tools_list = []
            
            for name, tool_def in tools.items():
                tool_info = {
                    "name": name,
                    "title": tool_def.title,
                    "description": tool_def.description,
                    "input_schema": tool_def.input_schema,
                }
                if tool_def.output_schema:
                    tool_info["output_schema"] = tool_def.output_schema
                if tool_def.annotations:
                    tool_info["annotations"] = tool_def.annotations
                tools_list.append(tool_info)
            
            return create_json_response({
                "ok": True,
                "tools": tools_list,
                "count": len(tools_list)
            })
        
        self._add_route("/api/tools", ["GET"], "tools_list_endpoint")
    
    def _register_tool_execute_endpoint(self):
        """POST /api/tools/{tool_name} - Execute a tool."""
        @self.mcp.custom_route("/api/tools/{tool_name}", methods=["POST"])
        async def tool_execute_endpoint(request):
            from starlette.requests import Request
            
            # Check auth
            ok, error = check_auth(dict(request.headers))
            if not ok:
                return create_json_response({
                    "ok": False,
                    "tool": None,
                    "error": {"type": "auth", "message": error, "details": None}
                }, 401)
            
            # Get tool name from path
            tool_name = request.path_params.get("tool_name")
            
            # Check body size first
            body = await request.body()
            ok, error = validate_body_size(body)
            if not ok:
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {"type": "size", "message": error, "details": None}
                }, 413)
            
            # Get tool definition
            tool_def = self.tool_registry.get(tool_name)
            if not tool_def:
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {
                        "type": "not_found",
                        "message": f"Tool '{tool_name}' not found",
                        "details": {"available_tools": list(self.tool_registry.list_tools().keys())}
                    }
                }, 404)
            
            # Check handler exists
            if not tool_def.handler:
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {
                        "type": "config",
                        "message": f"Tool '{tool_name}' has no handler",
                        "details": None
                    }
                }, 500)
            
            # Parse request body
            try:
                if body:
                    data = json.loads(body.decode('utf-8'))
                else:
                    data = {}
            except json.JSONDecodeError as e:
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {
                        "type": "json",
                        "message": f"Invalid JSON in request body: {str(e)}",
                        "details": None
                    }
                }, 400)
            
            # Extract args and kwargs
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            
            # If no args/kwargs wrapper, treat entire body as kwargs (for simpler usage)
            if not args and not kwargs and data:
                kwargs = data
            
            # Execute tool
            try:
                # Tools are async, so we need to await
                import asyncio
                if args:
                    result = await tool_def.handler(*args, **kwargs)
                else:
                    result = await tool_def.handler(**kwargs)
                
                return create_json_response({
                    "ok": True,
                    "tool": tool_name,
                    "result": result
                })
            
            except TypeError as e:
                # Likely wrong arguments
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {
                        "type": "args",
                        "message": f"Invalid arguments: {str(e)}",
                        "details": {
                            "provided_args": args,
                            "provided_kwargs": list(kwargs.keys()),
                            "expected_schema": tool_def.input_schema
                        }
                    }
                }, 400)
            
            except Exception as e:
                logger.error(f"Tool execution error for {tool_name}: {e}")
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {
                        "type": "execution",
                        "message": str(e),
                        "details": {"exception_type": type(e).__name__}
                    }
                }, 500)
        
        self._add_route("/api/tools/{tool_name}", ["POST"], "tool_execute_endpoint")
    
    def _register_vault_compat_endpoint(self):
        """POST /api/vault - Compatibility endpoint for vault operations."""
        @self.mcp.custom_route("/api/vault", methods=["POST"])
        async def vault_compat_endpoint(request):
            # Check auth
            ok, error = check_auth(dict(request.headers))
            if not ok:
                return create_json_response({
                    "ok": False,
                    "tool": "vault_seal",
                    "error": {"type": "auth", "message": error, "details": None}
                }, 401)
            
            # Check body size
            body = await request.body()
            ok, error = validate_body_size(body)
            if not ok:
                return create_json_response({
                    "ok": False,
                    "tool": "vault_seal",
                    "error": {"type": "size", "message": error, "details": None}
                }, 413)
            
            # Parse body
            try:
                if body:
                    data = json.loads(body.decode('utf-8'))
                else:
                    data = {}
            except json.JSONDecodeError as e:
                return create_json_response({
                    "ok": False,
                    "tool": "vault_seal",
                    "error": {
                        "type": "json",
                        "message": f"Invalid JSON: {str(e)}",
                        "details": None
                    }
                }, 400)
            
            # Get vault_seal tool
            tool_def = self.tool_registry.get("vault_seal")
            if not tool_def or not tool_def.handler:
                return create_json_response({
                    "ok": False,
                    "tool": "vault_seal",
                    "error": {
                        "type": "config",
                        "message": "vault_seal tool not available",
                        "details": None
                    }
                }, 500)
            
            # Execute vault_seal with the entire body as kwargs
            try:
                result = await tool_def.handler(**data)
                return create_json_response({
                    "ok": True,
                    "tool": "vault_seal",
                    "result": result
                })
            
            except Exception as e:
                logger.error(f"Vault compat endpoint error: {e}")
                return create_json_response({
                    "ok": False,
                    "tool": "vault_seal",
                    "error": {
                        "type": "execution",
                        "message": str(e),
                        "details": {"exception_type": type(e).__name__}
                    }
                }, 500)
        
        self._add_route("/api/vault", ["POST"], "vault_compat_endpoint")
