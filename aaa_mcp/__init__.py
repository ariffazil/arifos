"""
arifOS AAA MCP Server — 9-Skill Constitutional Architecture (v64.1-GAGI)
9 Canonical Verbs | Trinity Pipeline (ANCHOR → REASON → INTEGRATE → RESPOND → VALIDATE → ALIGN → FORGE → AUDIT → SEAL)

Provides constitutional governance layer for MCP-compatible AI platforms.
"""

from .core.constitutional_decorator import constitutional_floor, get_tool_floors
from .mcp_config import MCP_SERVERS, TrinityComponent, get_server_config
from .mcp_integration import MCPIntegrationLayer, get_mcp_layer
from .server import align, anchor, audit, forge, integrate, mcp, reason, respond, seal, validate

__version__ = "64.1.0"
__all__ = [
    # FastMCP server instance
    "mcp",
    # 9 Canonical Skills (Verbs)
    "anchor",  # 1. ANCHOR (000/111)
    "reason",  # 2. REASON (222)
    "integrate",  # 3. INTEGRATE (333)
    "respond",  # 4. RESPOND (444)
    "validate",  # 5. VALIDATE (555)
    "align",  # 6. ALIGN (666)
    "forge",  # 7. FORGE (777)
    "audit",  # 8. AUDIT (888)
    "seal",  # 9. SEAL (999)
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
# CACHE BUST: 1770989689 - v64.1 GAGI Refactor
