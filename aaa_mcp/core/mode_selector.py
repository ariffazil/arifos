"""
Mode Selector for arifOS MCP Server (v55.5-HARDENED)

Determines transport mode based on environment and context.
Supports stdio (local/CLI) and SSE (remote/web).
"""

import os
from enum import Enum
from typing import Optional


class MCPMode(Enum):
    """MCP transport modes."""

    STDIO = "stdio"  # stdin/stdout for local CLI
    SSE = "sse"  # Server-Sent Events for web/remote


# Environment variable for mode override
MODE_ENV_VAR = "ARIF_MCP_MODE"

# Default mode by environment
DEFAULT_MODES = {
    "local": MCPMode.STDIO,
    "development": MCPMode.SSE,
    "production": MCPMode.SSE,
    "railway": MCPMode.SSE,
    "cloudflare": MCPMode.SSE,
}


def detect_environment() -> str:
    """
    Detect current execution environment.

    Returns:
        Environment name: 'railway', 'cloudflare', 'development', 'local', 'production'
    """
    # Railway detection
    if os.getenv("RAILWAY_ENVIRONMENT"):
        return "railway"

    # Cloudflare Workers detection
    if os.getenv("CF_WORKER"):
        return "cloudflare"

    # Development detection
    if os.getenv("DEBUG") or os.getenv("DEV"):
        return "development"

    # Production detection
    if os.getenv("PRODUCTION") or os.getenv("PROD"):
        return "production"

    # Check for TTY (local terminal)
    import sys

    if sys.stdin.isatty():
        return "local"

    return "production"


def get_mcp_mode() -> MCPMode:
    """
    Get the appropriate MCP transport mode.

    Priority:
        1. ARIF_MCP_MODE environment variable
        2. Auto-detect based on environment
        3. Default to SSE

    Returns:
        MCPMode enum value
    """
    # Check for explicit mode override
    mode_override = os.getenv(MODE_ENV_VAR)
    if mode_override:
        mode_upper = mode_override.upper()
        if mode_upper in [m.name for m in MCPMode]:
            return MCPMode[mode_upper]

    # Auto-detect environment
    env = detect_environment()
    return DEFAULT_MODES.get(env, MCPMode.SSE)


def get_port() -> int:
    """
    Get the server port from environment.

    Returns:
        Port number (default: 6274 for arifOS)
    """
    return int(os.getenv("PORT", "6274"))


def get_host() -> str:
    """
    Get the server host from environment.

    Returns:
        Host address (default: 0.0.0.0 for production, 127.0.0.1 for local)
    """
    env = detect_environment()
    default_host = "0.0.0.0" if env in ("production", "railway", "cloudflare") else "127.0.0.1"
    return os.getenv("HOST", default_host)


def get_mode_config() -> dict:
    """
    Get full configuration for current mode.

    Returns:
        Dict with mode, port, host, and environment info
    """
    mode = get_mcp_mode()
    return {
        "mode": mode.value,
        "port": get_port(),
        "host": get_host(),
        "environment": detect_environment(),
        "version": "v55.5-HARDENED",
    }
