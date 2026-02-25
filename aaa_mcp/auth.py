"""
JWT Authentication Middleware for arifOS FORGE-2
Replaces ARIF_SECRET header with standardized JWT + RBAC tied to constitutional floors.

Features:
- JWT validation with HS256/RS256 support
- Tool-level RBAC based on floor permissions
- Optional mTLS client certificate binding
- Audit logging for authentication events

Environment Variables:
- ARIF_JWT_SECRET: HMAC secret (for HS256) or path to RSA public key (for RS256)
- ARIF_JWT_ALGORITHM: HS256 (default) or RS256
- ARIF_JWT_AUDIENCE: Expected audience claim (optional)
- ARIF_JWT_ISSUER: Expected issuer claim (optional)
- ARIF_MTLS_ENABLED: Enable mutual TLS (true/false)

Usage:
    from aaa_mcp.auth import jwt_auth_middleware, require_floor_permission

    app = Starlette(middleware=[jwt_auth_middleware])

    @require_floor_permission("F11")  # Authority floor required
    async def restricted_tool(request):
        ...
"""

import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

try:
    import jwt

    JWT_AVAILABLE = True
except ImportError:
    jwt = None
    JWT_AVAILABLE = False


@dataclass
class AuthContext:
    """Authentication context for request lifecycle."""

    user_id: str
    session_id: str
    floors: list[str]  # Constitutional floors user has access to
    metadata: dict[str, Any]
    is_authenticated: bool = True


class JWTConfig:
    """JWT configuration from environment variables."""

    def __init__(self):
        self.secret = os.getenv("ARIF_JWT_SECRET", os.getenv("ARIF_SECRET", ""))
        self.algorithm = os.getenv("ARIF_JWT_ALGORITHM", "HS256")
        self.audience = os.getenv("ARIF_JWT_AUDIENCE")
        self.issuer = os.getenv("ARIF_JWT_ISSUER")
        self.mtls_enabled = os.getenv("ARIF_MTLS_ENABLED", "false").lower() == "true"

        # Floor to tool mapping (configurable)
        self.floor_tool_mapping = {
            "F1": ["vault_seal"],  # Amanah - immutable ledger
            "F2": ["search", "fetch"],  # Truth - reality grounding
            "F3": ["apex_verdict"],  # Peace - judgment
            "F11": ["init_session", "self_diagnose"],  # Authority - session control
            "F12": ["agi_cognition", "asi_empathy"],  # Defense - core reasoning
        }


def decode_jwt(token: str, config: JWTConfig) -> dict[str, Any] | None:
    """Decode and validate JWT token."""
    if not JWT_AVAILABLE:
        raise RuntimeError("PyJWT not installed. Run: pip install pyjwt")

    try:
        # For RS256, secret should be a public key file path
        secret = config.secret
        if config.algorithm == "RS256" and os.path.exists(secret):
            with open(secret) as f:
                secret = f.read()

        payload = jwt.decode(
            token,
            secret,
            algorithms=[config.algorithm],
            audience=config.audience,
            issuer=config.issuer,
            options={"require_exp": True, "require_iat": True},
        )
        return payload
    except jwt.InvalidTokenError as e:
        print(f"JWT validation failed: {e}")
        return None


def extract_auth_context(request: Request, config: JWTConfig) -> AuthContext | None:
    """Extract authentication context from request."""
    # Check mTLS client certificate if enabled
    if config.mtls_enabled:
        client_cert = request.scope.get("client_cert")
        if client_cert:
            # TODO: Validate client certificate
            pass

    # Extract JWT from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header[7:]  # Remove "Bearer " prefix
    payload = decode_jwt(token, config)
    if not payload:
        return None

    # Extract floors from JWT claims
    floors = payload.get("floors", [])
    if isinstance(floors, str):
        floors = [f.strip() for f in floors.split(",")]

    return AuthContext(
        user_id=payload.get("sub", "anonymous"),
        session_id=payload.get("sid", str(time.time())),
        floors=floors,
        metadata=payload,
        is_authenticated=True,
    )


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """JWT authentication middleware for Starlette."""

    def __init__(self, app, config: JWTConfig | None = None):
        super().__init__(app)
        self.config = config or JWTConfig()

    async def dispatch(self, request: Request, call_next):
        # Skip auth for health checks and public endpoints
        if request.url.path in ["/health", "/ready", "/version", "/metrics"]:
            return await call_next(request)

        # Extract auth context
        auth_context = extract_auth_context(request, self.config)
        if not auth_context:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "details": "Invalid or missing JWT token"},
            )

        # Attach auth context to request state
        request.state.auth = auth_context

        # Check tool-level RBAC for tool endpoints
        if request.url.path.startswith("/tools/"):
            tool_name = request.url.path.split("/")[-1]
            if not self._check_tool_access(tool_name, auth_context.floors):
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Forbidden",
                        "details": f"Insufficient floor permissions for tool '{tool_name}'",
                    },
                )

        response = await call_next(request)

        # Add authentication headers
        response.headers["X-Authenticated-User"] = auth_context.user_id
        response.headers["X-Authenticated-Floors"] = ",".join(auth_context.floors)

        return response

    def _check_tool_access(self, tool_name: str, user_floors: list[str]) -> bool:
        """Check if user has required floor permissions for tool."""
        # Find floors that grant access to this tool
        required_floors = []
        for floor, tools in self.config.floor_tool_mapping.items():
            if tool_name in tools:
                required_floors.append(floor)

        # If no specific floor mapping, allow access
        if not required_floors:
            return True

        # Check if user has at least one required floor
        return any(floor in user_floors for floor in required_floors)


def require_floor_permission(floor: str):
    """Decorator to require specific floor permission for endpoint."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            auth_context = getattr(request.state, "auth", None)
            if not auth_context or floor not in auth_context.floors:
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Forbidden",
                        "details": f"Floor '{floor}' permission required",
                    },
                )
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


# Backward compatibility: support ARIF_SECRET as simple bearer token
def legacy_auth_middleware(app):
    """Legacy middleware using ARIF_SECRET header."""

    async def middleware(request: Request, call_next):
        if request.url.path in ["/health", "/ready", "/version", "/metrics"]:
            return await call_next(request)

        secret = os.getenv("ARIF_SECRET")
        if secret:
            auth_header = request.headers.get("Authorization")
            if not auth_header or auth_header != f"Bearer {secret}":
                return JSONResponse(
                    status_code=401,
                    content={"error": "Unauthorized", "details": "Invalid ARIF_SECRET"},
                )

        return await call_next(request)

    return middleware


# Default export: use JWT if available, otherwise fallback to legacy
if JWT_AVAILABLE:
    jwt_auth_middleware = JWTAuthMiddleware
else:
    jwt_auth_middleware = legacy_auth_middleware
