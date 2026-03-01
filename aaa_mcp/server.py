"""
aaa_mcp/server.py — Thin compatibility shim

This module re-exports the canonical 13-tool surface from arifos_aaa_mcp.
The canonical implementation has been consolidated to arifos_aaa_mcp/server.py
to eliminate circular dependencies and reduce entropy.

Migration path:
- Use `arifos_aaa_mcp` for new code (canonical)
- Use `aaa_mcp` for backward compatibility (this shim)
- Both expose identical 13-tool MCP surface

Ditempa Bukan Diberi — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

# Re-export all canonical tools and surface from arifos_aaa_mcp
from arifos_aaa_mcp.server import (
    anchor_session,
    apex_judge,
    audit_rules,
    check_vital,
    create_aaa_mcp_server,
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
    # Prompts
    aaa_chain_prompt,
    arifos_governance_brief_prompt,
    prompt_trinity_forge,
    prompt_anchor_reason,
    prompt_audit_then_seal,
    # Resources
    aaa_tool_schemas,
    aaa_full_context_pack,
    full_context_template_v2,
)

# Keep MANIFEST_VERSION import from original location for compatibility
from aaa_mcp.protocol.aaa_contract import MANIFEST_VERSION

# Backward compatibility aliases (deprecated, use canonical names)
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


def create_unified_mcp_server() -> Any:
    """Backward compatible alias for create_aaa_mcp_server()."""
    return create_aaa_mcp_server()


__all__ = [
    # Core
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
    # Prompts
    "aaa_chain_prompt",
    "arifos_governance_brief_prompt",
    "prompt_trinity_forge",
    "prompt_anchor_reason",
    "prompt_audit_then_seal",
    # Resources
    "aaa_tool_schemas",
    "aaa_full_context_pack",
    "full_context_template_v2",
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
