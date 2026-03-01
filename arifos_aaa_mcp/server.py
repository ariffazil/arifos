"""arifOS AAA MCP public 13-tool surface — Canonical Package.

This module re-exports the 13-tool MCP surface from aaa_mcp.server.
The actual implementations remain in aaa_mcp for backward compatibility.

Ditempa Bukan Diberi — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

# Import all canonical tools from aaa_mcp (where actual implementations live)
from aaa_mcp.server import (
    anchor_session,
    apex_judge,
    audit_rules,
    check_vital,
    create_unified_mcp_server,
    critique_thought,
    eureka_forge,
    fetch_content,
    inspect_file,
    mcp,
    reason_mind,
    recall_memory,
    seal_vault,
    search_reality,
    simulate_heart,
)

# Re-export with canonical naming
create_aaa_mcp_server = create_unified_mcp_server

# Backward compatibility aliases
init_session = anchor_session
agi_cognition = reason_mind
phoenix_recall = recall_memory
asi_empathy = simulate_heart
apex_verdict = apex_judge
sovereign_actuator = eureka_forge
vault_seal_tool = seal_vault
search = search_reality
fetch = fetch_content
analyze = inspect_file

# Import manifest version
from aaa_mcp.protocol.aaa_contract import MANIFEST_VERSION

# Register REST routes (health, version, tools, etc.)
from . import rest_routes
rest_routes.register_rest_routes(mcp, {})

__all__ = [
    "mcp",
    "create_aaa_mcp_server",
    "create_unified_mcp_server",
    "MANIFEST_VERSION",
    # 13 Canonical Tools
    "anchor_session",
    "reason_mind",
    "recall_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
    # Backward compatibility aliases
    "init_session",
    "agi_cognition",
    "phoenix_recall",
    "asi_empathy",
    "apex_verdict",
    "sovereign_actuator",
    "vault_seal_tool",
    "search",
    "fetch",
    "analyze",
]
