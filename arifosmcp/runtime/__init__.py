"""arifOS Runtime — The Sovereign FastMCP Instance.

Provides the primary Model Context Protocol (MCP) server for the arifOS ecosystem.
"""

from __future__ import annotations

from .server import create_aaa_mcp_server, mcp

__all__ = ["mcp", "create_aaa_mcp_server"]
