"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""
arifosmcp.transport/core — Core module for MCP Server

Constitutional decorators, engine adapters, and mode selection.
"""

from .constitutional_decorator import constitutional_floor, get_tool_floors
from .engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from .mode_selector import MCPMode, get_mcp_mode, get_mode_config

__all__ = [
    "constitutional_floor",
    "get_tool_floors",
    "AGIEngine",
    "ASIEngine",
    "APEXEngine",
    "InitEngine",
    "MCPMode",
    "get_mcp_mode",
    "get_mode_config",
]
