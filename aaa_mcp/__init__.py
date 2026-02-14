"""
arifOS AAA MCP Server — 5-Core Constitutional Architecture (v64.1-GAGI)
5 Canonical Tools | Trinity Pipeline (INIT → AGI → ASI → APEX → SEAL)

Provides constitutional governance layer for MCP-compatible AI platforms.
"""

from .core.constitutional_decorator import constitutional_floor, get_tool_floors
from .mcp_config import MCP_SERVERS, TrinityComponent, get_server_config
from .mcp_integration import MCPIntegrationLayer, get_mcp_layer
from .server import agi_cognition, apex_verdict, asi_empathy, init_session, mcp, vault_seal

__version__ = "64.1.0"
__all__ = [
    # FastMCP server instance
    "mcp",
    # 5 Canonical Tools (000-999 Trinity Pipeline)
    "init_session",  # 000_INIT: Session ignition (F11, F12)
    "agi_cognition",  # 111-333_AGI: Mind - sense/think/reason (F2, F4, F7, F8, F10)
    "asi_empathy",  # 555-666_ASI: Heart - empathize/align (F1, F5, F6, F9)
    "apex_verdict",  # 888_APEX: Soul - judgment (F2, F3, F8, F10, F11, F12, F13)
    "vault_seal",  # 999_VAULT: Memory - seal (F1, F3)
    # Integration layer
    "MCPIntegrationLayer",
    "get_mcp_layer",
    # Config
    "MCP_SERVERS",
    "get_server_config",
    "TrinityComponent",
    # Decorators
    "constitutional_floor",
    "get_tool_floors",
]
# CACHE BUST: 1770989689 - v61 forced rebuild
# v62 CACHE BUST: 1770992292 - SystemState exposure deployed
# v62.1 CACHE BUST: 1770992489 - Improved heuristics
# v62.2 CACHE BUST: 1770993431 - Real Brave Search evidence
# v62.3 CACHE BUST: 1770993875 - Relevance-based grounding
