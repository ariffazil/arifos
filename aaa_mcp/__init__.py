"""
arifOS AAA MCP package exports.

Public contract:
- 5-organ tools (`init_session`, `agi_cognition`, `asi_empathy`, `apex_verdict`, `vault_seal`)
- 4 utility tools (`search`, `fetch`, `analyze`, `system_audit`)

Legacy verb aliases are kept for backward compatibility.
"""

from .core.constitutional_decorator import constitutional_floor, get_tool_floors
from .mcp_config import MCP_SERVERS, TrinityComponent, get_server_config
from .mcp_integration import MCPIntegrationLayer, get_mcp_layer
from .server import (
    agi_cognition,
    analyze,
    apex_verdict,
    asi_empathy,
    fetch,
    init_session,
    mcp,
    search,
    system_audit,
    vault_seal,
)

# Backward-compatible aliases (legacy 9-verb naming)
anchor = init_session
reason = agi_cognition
integrate = agi_cognition
respond = agi_cognition
validate = asi_empathy
align = asi_empathy
forge = apex_verdict
audit = apex_verdict
seal = vault_seal

__version__ = "2026.02.22-FORGE-VPS-SEAL"
__all__ = [
    # FastMCP server instance
    "mcp",
    # Canonical 5-organ + 4-utility surface
    "init_session",
    "agi_cognition",
    "asi_empathy",
    "apex_verdict",
    "vault_seal",
    "search",
    "fetch",
    "analyze",
    "system_audit",
    # Legacy aliases
    "anchor",
    "reason",
    "integrate",
    "respond",
    "validate",
    "align",
    "forge",
    "audit",
    "seal",
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
# CACHE BUST: 1771142400 - T000 FORGE-TRINITY SEAL
