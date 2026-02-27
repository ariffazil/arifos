"""Shared public-surface constants for arifOS AAA MCP.

This module is the source of truth for client-facing aliases, resources,
and prompts that must stay aligned across the internal and public FastMCP
instances.
"""

from __future__ import annotations

PUBLIC_CANONICAL_TOOLS: tuple[str, ...] = (
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
)

PUBLIC_TOOL_ALIASES: dict[str, str] = {
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "recall_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "apex_judge",
    "judge_soul": "apex_judge",
    "sovereign_actuator": "eureka_forge",
    "vault_seal": "seal_vault",
    "search": "search_reality",
    "fetch": "fetch_content",
    "analyze": "inspect_file",
    "system_audit": "audit_rules",
    "anchor": "anchor_session",
    "reason": "reason_mind",
    "integrate": "reason_mind",
    "respond": "reason_mind",
    "validate": "simulate_heart",
    "align": "simulate_heart",
    "forge": "apex_judge",
    "audit": "apex_judge",
    "seal": "seal_vault",
}

PUBLIC_RESOURCE_URIS: dict[str, str] = {
    "schemas": "arifos://aaa/schemas",
    "full_context_pack": "arifos://aaa/full-context-pack",
}

PUBLIC_PROMPT_NAMES: dict[str, str] = {
    "aaa_chain": "arifos.prompt.aaa_chain",
}

__all__ = [
    "PUBLIC_CANONICAL_TOOLS",
    "PUBLIC_PROMPT_NAMES",
    "PUBLIC_RESOURCE_URIS",
    "PUBLIC_TOOL_ALIASES",
]
