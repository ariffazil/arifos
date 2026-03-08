"""Public arifOS AAA MCP package (canonical 13-tool surface)."""

from .server import create_aaa_mcp_server, mcp

__all__ = ["mcp", "create_aaa_mcp_server"]
