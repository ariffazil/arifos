"""
arifOS REST API Transport Layer
Exposes MCP tools as REST endpoints alongside MCP transport.

Policy-based exposure:
- OPEN: agi_sense, agi_think, agi_reason, asi_empathize, asi_align
- GUARDED: apex_verdict, reality_search, vault_seal, _trinity_
- MCP_ONLY: init_gate (and any other sensitive tools)

Routes:
- GET  /routes              -> List all registered routes
- GET  /api/tools           -> List tools with schemas (respects exposure policy)
- POST /api/tools/{name}    -> Execute tool (respects exposure policy)
- POST /api/vault/*         -> Vault convenience endpoints with redaction
"""

import os
import json
import logging
import hashlib
import time
from typing import Any, Dict, Optional, List, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Security configuration
# Strip quotes from API_KEY in case Railway includes them
API_KEY = os.environ.get("API_KEY", "").strip().strip('"').strip("'") or None
ALLOW_RAW_VAULT_READ = os.environ.get("ALLOW_RAW_VAULT_READ", "false").lower() == "true"
ALLOW_INTERNAL_TOOLS = os.environ.get("ALLOW_INTERNAL_TOOLS", "false").lower() == "true"
MAX_BODY_SIZE = 256 * 1024  # 256KB
MAX_RESPONSE_SIZE = 256 * 1024  # 256KB

# Tool exposure policy
TOOL_EXPOSURE = {
    # OPEN: Safe to expose
    "agi_sense": "OPEN",
    "agi_think": "OPEN",
    "agi_reason": "OPEN",
    "asi_empathize": "OPEN",
    "asi_align": "OPEN",
    
    # GUARDED: Exposed with restrictions
    "apex_verdict": "GUARDED",
    "reality_search": "GUARDED",
    "vault_seal": "GUARDED",
    "_trinity_": "GUARDED",
    
    # MCP_ONLY: Not exposed via REST
    "init_gate": "MCP_ONLY",
}

# Keys to always remove from vault_read (deep scrub)
VAULT_REDACT_KEYS: Set[str] = {
    "kernel_result",
    "proof",
    "leaves",
    "signature_ed25519",
    "public_key_ed25519",
    "vault_location",
    "filesystem",
    "stage",
    "status",
}

# Pattern-based redaction
VAULT_REDACT_PATTERNS = ["_key", "signature", "private", "secret"]


@dataclass
class RateLimiter:
    """Simple in-memory rate limiter per IP."""
    window: int = 60  # seconds
    max_requests: int = 30  # per window
    
    def __post_init__(self):
        self._requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, client_ip: str) -> tuple[bool, Optional[str]]:
        now = time.time()
        
        # Clean old entries
        if client_ip in self._requests:
            self._requests[client_ip] = [
                t for t in self._requests[client_ip] 
                if now - t < self.window
            ]
        else:
            self._requests[client_ip] = []
        
        # Check limit
        if len(self._requests[client_ip]) >= self.max_requests:
            return False, f"Rate limit exceeded: {self.max_requests} requests per {self.window}s"
        
        # Record request
        self._requests[client_ip].append(now)
        return True, None


# Global rate limiter instance
rate_limiter = RateLimiter()


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


def check_rate_limit(client_ip: str) -> tuple[bool, Optional[str]]:
    """Check rate limiting."""
    return rate_limiter.is_allowed(client_ip)


def validate_body_size(body: bytes) -> tuple[bool, Optional[str]]:
    """Check if body size is within limits."""
    if len(body) > MAX_BODY_SIZE:
        return False, f"Request body too large: {len(body)} bytes (max {MAX_BODY_SIZE})"
    return True, None


def truncate_response(data: dict, max_bytes: int = MAX_RESPONSE_SIZE) -> dict:
    """Truncate response if it exceeds max size."""
    json_str = json.dumps(data)
    if len(json_str.encode('utf-8')) <= max_bytes:
        return data
    
    # Start truncating fields
    result = {"_truncated": True}
    
    # Keep essential fields
    for key in ["ok", "tool", "verdict"]:
        if key in data:
            result[key] = data[key]
    
    # Truncate result
    if "result" in data:
        result["result"] = "[TRUNCATED: response too large]"
    
    return result


def deep_redact(obj: Any, redact_keys: Set[str], patterns: List[str]) -> Any:
    """Deep redact sensitive keys from nested objects."""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            # Check exact key match
            if k in redact_keys:
                continue
            # Check pattern match
            if any(pattern in k.lower() for pattern in patterns):
                continue
            # Recurse
            result[k] = deep_redact(v, redact_keys, patterns)
        return result
    elif isinstance(obj, list):
        return [deep_redact(item, redact_keys, patterns) for item in obj]
    else:
        return obj


def redact_vault_entry(entry: dict, redact: bool = True) -> tuple[dict, dict]:
    """
    Redact vault entry for REST-safe output.
    Returns: (redacted_entry, redaction_info)
    """
    if not redact:
        return entry, {"applied": False}
    
    # Allowlist of safe fields
    safe_fields = {
        "sequence", "session_id", "seal_id", "timestamp",
        "authority", "verdict", "entry_hash", "prev_hash",
        "merkle_root", "vault_backend", "created_at"
    }
    
    # Start with safe fields
    redacted = {k: v for k, v in entry.items() if k in safe_fields}
    
    # Extract note if present in seal_data
    if "seal_data" in entry and isinstance(entry["seal_data"], dict):
        seal_data = entry["seal_data"]
        if "note" in seal_data:
            redacted["note"] = seal_data["note"]
        elif "payload" in seal_data and isinstance(seal_data["payload"], dict):
            if "note" in seal_data["payload"]:
                redacted["note"] = seal_data["payload"]["note"]
    
    # Deep redact anything else
    redacted = deep_redact(redacted, VAULT_REDACT_KEYS, VAULT_REDACT_PATTERNS)
    
    # Track what was removed
    removed = [k for k in entry.keys() if k not in redacted]
    removed.extend(VAULT_REDACT_KEYS)
    
    redaction_info = {
        "applied": True,
        "removed_keys": list(set(removed)),
        "truncated": False
    }
    
    return redacted, redaction_info


def create_json_response(data: dict, status_code: int = 200) -> Any:
    """Create a JSON response compatible with Starlette."""
    from starlette.responses import JSONResponse
    
    # Truncate if needed
    data = truncate_response(data)
    
    return JSONResponse(data, status_code=status_code)


def get_client_ip(request) -> str:
    """Extract client IP from request."""
    # Check X-Forwarded-For header (for proxies)
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    # Fall back to direct connection
    if hasattr(request, 'client') and request.client:
        return request.client.host
    
    return "unknown"


class RESTAPIRouter:
    """Router for REST API endpoints. Integrates with FastMCP/Starlette."""
    
    def __init__(self, tool_registry, mcp_server):
        self.tool_registry = tool_registry
        self.mcp = mcp_server
        self.routes = []
        
        if not API_KEY:
            logger.warning("API_KEY not set - REST API is open (dev mode). Set API_KEY env var for production.")
        else:
            logger.info("REST API authentication enabled")
        
        # Log exposure policy
        logger.info("REST API tool exposure policy:")
        for tool, exposure in TOOL_EXPOSURE.items():
            logger.info(f"  {tool}: {exposure}")
    
    def register_all_routes(self):
        """Register all REST API routes."""
        self._register_routes_endpoint()
        self._register_tools_list_endpoint()
        self._register_tool_execute_endpoint()
        self._register_vault_compat_endpoints()
        
        # Phase 1: API v1 observability endpoints (constitutional debugging)
        from ..api_routes import register_api_v1_routes
        register_api_v1_routes(self)
        
        logger.info(f"Registered {len(self.routes)} REST API routes")
    
    def _add_route(self, path: str, methods: list, handler_name: str):
        """Track registered routes for introspection."""
        for method in methods:
            self.routes.append({"method": method, "path": path, "handler": handler_name})
    
    def _get_exposure_level(self, tool_name: str) -> str:
        """Get exposure level for a tool."""
        return TOOL_EXPOSURE.get(tool_name, "MCP_ONLY")  # Default to safe
    
    def _is_rest_exposed(self, tool_name: str) -> bool:
        """Check if tool is exposed via REST."""
        exposure = self._get_exposure_level(tool_name)
        if exposure == "MCP_ONLY":
            return False
        if exposure == "GUARDED":
            return True
        if exposure == "OPEN":
            return True
        return False
    
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
            
            return create_json_response({
                "ok": True,
                "routes": self.routes,
                "count": len(self.routes)
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
                exposure = self._get_exposure_level(name)
                
                # Skip MCP_ONLY tools unless explicitly allowed
                if exposure == "MCP_ONLY" and not ALLOW_INTERNAL_TOOLS:
                    continue
                
                tool_info = {
                    "name": name,
                    "exposure": exposure,
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
            client_ip = get_client_ip(request)
            
            # Check rate limit
            ok, error = check_rate_limit(client_ip)
            if not ok:
                return create_json_response({
                    "ok": False,
                    "tool": None,
                    "error": {"type": "rate_limit", "message": error, "details": None}
                }, 429)
            
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
            
            # Check if tool is exposed via REST
            if not self._is_rest_exposed(tool_name):
                return create_json_response({
                    "ok": False,
                    "tool": tool_name,
                    "error": {
                        "type": "not_found",
                        "message": f"Tool '{tool_name}' not found or not available via REST",
                        "details": None
                    }
                }, 404)
            
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
                        "details": None
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
            
            # Extract args, kwargs, and confirm
            args = data.get("args", [])
            kwargs = data.get("kwargs", {})
            confirm = data.get("confirm", False)
            authority = data.get("authority", "api")
            
            # If no args/kwargs wrapper, treat entire body as kwargs (for simpler usage)
            if not args and not kwargs and data and not any(k in data for k in ["confirm", "authority"]):
                kwargs = {k: v for k, v in data.items() if k not in ["confirm", "authority"]}
            
            # GUARDED tools: require confirm=true for SEAL verdicts
            exposure = self._get_exposure_level(tool_name)
            if exposure == "GUARDED":
                if not confirm or authority != "human":
                    # Force SABAR verdict instead of SEAL
                    if tool_name in ["apex_verdict", "_trinity_"]:
                        return create_json_response({
                            "ok": True,
                            "tool": tool_name,
                            "verdict": "SABAR",
                            "result": {
                                "message": "GUARDED tool requires confirm=true and authority='human' to return SEAL",
                                "hint": "Add {\"confirm\": true, \"authority\": \"human\"} to request"
                            },
                            "audit": {
                                "request_id": hashlib.sha256(f"{tool_name}{time.time()}".encode()).hexdigest()[:16],
                                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                            }
                        })
            
            # Execute tool
            try:
                # Add authority to kwargs for GUARDED tools
                if exposure == "GUARDED":
                    kwargs["authority"] = authority
                
                if args:
                    result = await tool_def.handler(*args, **kwargs)
                else:
                    result = await tool_def.handler(**kwargs)
                
                # Determine verdict from result
                verdict = "SEAL"  # Default
                if isinstance(result, dict):
                    if "verdict" in result:
                        verdict = result["verdict"]
                    elif "operation" in result and result["operation"] == "sealed":
                        verdict = result.get("verdict", "SEAL")
                
                return create_json_response({
                    "ok": True,
                    "tool": tool_name,
                    "verdict": verdict,
                    "result": result,
                    "audit": {
                        "request_id": hashlib.sha256(f"{tool_name}{time.time()}".encode()).hexdigest()[:16],
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    }
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
    
    def _register_vault_compat_endpoints(self):
        """Register /api/vault/* convenience endpoints."""
        from starlette.requests import Request
        
        @self.mcp.custom_route("/api/vault/list", methods=["POST"])
        async def vault_list_endpoint(request: Request):
            return await self._handle_vault_action(request, "list")
        
        @self.mcp.custom_route("/api/vault/read", methods=["POST"])
        async def vault_read_endpoint(request: Request):
            return await self._handle_vault_action(request, "read", redact_default=True)
        
        @self.mcp.custom_route("/api/vault/seal", methods=["POST"])
        async def vault_seal_endpoint(request: Request):
            return await self._handle_vault_action(request, "seal", require_confirm=True)
        
        self._add_route("/api/vault/list", ["POST"], "vault_list_endpoint")
        self._add_route("/api/vault/read", ["POST"], "vault_read_endpoint")
        self._add_route("/api/vault/seal", ["POST"], "vault_seal_endpoint")
    
    async def _handle_vault_action(self, request, action: str, redact_default: bool = False, require_confirm: bool = False):
        """Handle vault actions with proper guards."""
        client_ip = get_client_ip(request)
        
        # Check rate limit
        ok, error = check_rate_limit(client_ip)
        if not ok:
            return create_json_response({
                "ok": False,
                "tool": "vault_seal",
                "error": {"type": "rate_limit", "message": error, "details": None}
            }, 429)
        
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
        
        # Check confirm requirement for seal
        if require_confirm:
            confirm = data.get("confirm", False)
            authority = data.get("authority", "api")
            if not confirm or authority != "human":
                return create_json_response({
                    "ok": False,
                    "tool": "vault_seal",
                    "verdict": "SABAR",
                    "error": {
                        "type": "confirm_required",
                        "message": "Vault seal requires confirm=true and authority='human' for irreversible actions",
                        "details": {"provided_confirm": confirm, "provided_authority": authority}
                    }
                }, 403)
        
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
        
        # Prepare kwargs
        kwargs = {"action": action, **data}
        
        # Handle redaction for read
        redact = data.get("redact", redact_default)
        allow_raw = ALLOW_RAW_VAULT_READ and API_KEY and dict(request.headers).get("x-api-key")
        if redact_default and not allow_raw:
            redact = True
        
        # Execute
        try:
            result = await tool_def.handler(**kwargs)
            
            # Redact if needed
            if action == "read" and redact and "entry" in result:
                entry = result["entry"]
                redacted_entry, redaction_info = redact_vault_entry(entry, redact=True)
                result["entry"] = redacted_entry
                result["redaction"] = redaction_info
            
            return create_json_response({
                "ok": True,
                "tool": "vault_seal",
                "operation": action,
                "result": result,
                "audit": {
                    "request_id": hashlib.sha256(f"vault_{action}{time.time()}".encode()).hexdigest()[:16],
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
            })
        
        except Exception as e:
            logger.error(f"Vault {action} error: {e}")
            return create_json_response({
                "ok": False,
                "tool": "vault_seal",
                "error": {
                    "type": "execution",
                    "message": str(e),
                    "details": {"exception_type": type(e).__name__}
                }
            }, 500)
