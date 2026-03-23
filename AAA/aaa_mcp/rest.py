"""
aaa_mcp.rest — REST compatibility layer for arifOS MCP

Re-exports the FastMCP http_app for legacy REST integrations.
"""

from __future__ import annotations

from arifosmcp.runtime.server import (
    app,
    create_aaa_mcp_server,
    mcp,
)

__all__ = ["app", "create_aaa_mcp_server", "mcp"]
