"""
arifOS AAA MCP Server — Constitutional AI Gateway
9 Canonical Tools | Trinity Architecture (AGI/ASI/APEX)

Provides constitutional governance layer for MCP-compatible AI platforms.
"""

from .core.constitutional_decorator import constitutional_floor, get_tool_floors
from .mcp_config import MCP_SERVERS, TrinityComponent, get_server_config
from .mcp_integration import MCPIntegrationLayer, get_mcp_layer
from .server import (
    agi_reason,
    agi_sense,
    agi_think,
    apex_verdict,
    asi_align,
    asi_empathize,
    init_gate,
    mcp,
    reality_search,
    vault_seal,
)

__version__ = "55.5.0"
__all__ = [
    # FastMCP server instance
    "mcp",
    # 9 Canonical Tools (000-999 Metabolic Loop)
    "init_gate",  # 000-111: Session gate + security
    "agi_sense",  # 111: Perception (F2, F4)
    "agi_think",  # 222: Cognition (F2, F4, F7)
    "agi_reason",  # 333: Logic (F2, F4, F7)
    "asi_empathize",  # 444-555: Care (F5, F6)
    "asi_align",  # 666: Alignment (F5, F6, F9)
    "apex_verdict",  # 777-888: Judgment (F3, F8)
    "reality_search",  # F7: External fact-checking
    "vault_seal",  # 999: Immutable ledger (F1, F3)
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
