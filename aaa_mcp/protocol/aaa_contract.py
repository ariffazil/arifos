"""Shared AAA contract constants.

This module is the single source of truth for the active AAA MCP public
surface and its governance metadata. Public routers, internal routers, and
governance wrappers should import these constants instead of duplicating them.
"""

from __future__ import annotations

from typing import Any

MANIFEST_VERSION: int = 4

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL SURFACE TAXONOMY — L1 / L4 / L5
# ═══════════════════════════════════════════════════════════════════════════════
#
#   L1_PROMPTS     Transport scaffolding injected by FastMCP PromptsAsTools
#                  transform.  "Call in, call out" — NOT constitutional tools.
#                  They let tool-only clients (Copilot, etc.) access MCP prompts.
#
#   L4_TOOLS       The 13 canonical constitutional syscalls — the kernel surface.
#                  Each maps 1-to-1 to a governance stage (000-999).
#                  THIS IS THE SACRED COUNT: 13.
#
#   L5_COMPOSITE   Orchestration tools that sequence L4_TOOLS.
#                  Like a shell calling syscalls — real tools, but not atoms.
#
# ═══════════════════════════════════════════════════════════════════════════════

# L1: Transport-layer plumbing (auto-injected by FastMCP PromptsAsTools)
L1_PROMPTS: frozenset[str] = frozenset({"list_prompts", "get_prompt"})

# L4: The 13 canonical constitutional tool surface
AAA_CANONICAL_TOOLS: tuple[str, ...] = (
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
L4_TOOLS: frozenset[str] = frozenset(AAA_CANONICAL_TOOLS)

# L5: Composite orchestration (sequences L4 tools)
L5_COMPOSITE: frozenset[str] = frozenset({"metabolic_loop"})

# Full MCP tools/list surface = L1 + L4 + L5 (but canonical count stays 13)
MCP_FULL_SURFACE: frozenset[str] = L1_PROMPTS | L4_TOOLS | L5_COMPOSITE

# Test assertion helpers
CANONICAL_TOOL_COUNT: int = 13  # Sacred count — L4 only
MCP_GOVERNED_TOOLS: frozenset[str] = L4_TOOLS | L5_COMPOSITE  # Tools with envelopes

AAA_TOOL_ALIASES: dict[str, str] = {
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

AAA_RESOURCE_URIS: dict[str, str] = {
    "schemas": "arifos://aaa/schemas",
    "full_context_pack": "arifos://aaa/full-context-pack",
}

AAA_PROMPT_NAMES: dict[str, str] = {
    "aaa_chain": "arifos.prompt.aaa_chain",
}

AXIOMS_333: dict[str, dict[str, Any]] = {
    "A1_TRUTH_COST": {
        "statement": "Truth has thermodynamic cost; evidence must be explicit for claims.",
        "source": "000_THEORY/000_LAW.md#Axiom-1",
    },
    "A2_SCAR_WEIGHT": {
        "statement": "Authority requires accountability; AI proposes, human disposes.",
        "source": "000_THEORY/000_LAW.md#Axiom-2",
    },
    "A3_ENTROPY_WORK": {
        "statement": "Clarity requires work; governance must reduce confusion entropy.",
        "source": "000_THEORY/000_LAW.md#Axiom-3",
    },
}

TRINITY_BY_TOOL: dict[str, str] = {
    "anchor_session": "Delta",
    "reason_mind": "Delta",
    "recall_memory": "Omega",
    "simulate_heart": "Omega",
    "critique_thought": "Omega",
    "apex_judge": "Psi",
    "judge_soul": "Psi",
    "eureka_forge": "Psi",
    "seal_vault": "Psi",
    "search_reality": "Delta",
    "fetch_content": "Delta",
    "inspect_file": "Delta",
    "audit_rules": "Delta",
    "check_vital": "Omega",
}

LAW_13_CATALOG: dict[str, dict[str, str]] = {
    "F1_AMANAH": {"type": "floor", "threshold": "reversible"},
    "F2_TRUTH": {"type": "floor", "threshold": ">=0.99 (adaptive)"},
    "F4_CLARITY": {"type": "floor", "threshold": "dS<=0"},
    "F5_PEACE2": {"type": "floor", "threshold": ">=1.0"},
    "F6_EMPATHY": {"type": "floor", "threshold": ">=0.95"},
    "F7_HUMILITY": {"type": "floor", "threshold": "omega0 in [0.03,0.05]"},
    "F9_ANTI_HANTU": {"type": "floor", "threshold": "c_dark<0.30"},
    "F11_AUTHORITY": {"type": "floor", "threshold": "valid auth continuity"},
    "F12_DEFENSE": {"type": "floor", "threshold": "risk<0.85"},
    "F3_TRI_WITNESS": {"type": "mirror", "threshold": "cross-check present"},
    "F8_GENIUS": {"type": "mirror", "threshold": "coherence >= 0.80"},
    "F10_ONTOLOGY_LOCK": {"type": "wall", "threshold": "lock engaged"},
    "F13_SOVEREIGNTY": {"type": "wall", "threshold": "human veto preserved"},
}

AAA_TOOL_LAW_BINDINGS: dict[str, list[str]] = {
    "anchor_session": ["F11_AUTHORITY", "F12_DEFENSE", "F13_SOVEREIGNTY", "F3_TRI_WITNESS"],
    "reason_mind": ["F2_TRUTH", "F4_CLARITY", "F7_HUMILITY", "F8_GENIUS", "F3_TRI_WITNESS"],
    "recall_memory": ["F4_CLARITY", "F7_HUMILITY", "F3_TRI_WITNESS", "F13_SOVEREIGNTY"],
    "simulate_heart": ["F5_PEACE2", "F6_EMPATHY", "F4_CLARITY", "F3_TRI_WITNESS"],
    "critique_thought": ["F4_CLARITY", "F7_HUMILITY", "F8_GENIUS", "F12_DEFENSE", "F3_TRI_WITNESS"],
    "apex_judge": [
        "F1_AMANAH",
        "F2_TRUTH",
        "F3_TRI_WITNESS",
        "F8_GENIUS",
        "F9_ANTI_HANTU",
        "F10_ONTOLOGY_LOCK",
        "F11_AUTHORITY",
        "F13_SOVEREIGNTY",
    ],
    "judge_soul": [
        "F1_AMANAH",
        "F2_TRUTH",
        "F3_TRI_WITNESS",
        "F8_GENIUS",
        "F9_ANTI_HANTU",
        "F10_ONTOLOGY_LOCK",
        "F11_AUTHORITY",
        "F13_SOVEREIGNTY",
    ],
    "eureka_forge": [
        "F5_PEACE2",       # Safe defaults (working_dir validation)
        "F6_EMPATHY",      # Error handling with clear messages
        "F7_HUMILITY",     # Risk classification, admit uncertainty
        "F9_ANTI_HANTU",   # Transparent logging
        "F13_SOVEREIGNTY", # Human veto via confirm_dangerous
    ],
    "seal_vault": ["F1_AMANAH", "F3_TRI_WITNESS", "F10_ONTOLOGY_LOCK", "F13_SOVEREIGNTY"],
    "search_reality": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "fetch_content": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "inspect_file": ["F1_AMANAH", "F4_CLARITY", "F11_AUTHORITY", "F12_DEFENSE"],
    "audit_rules": ["F2_TRUTH", "F8_GENIUS", "F10_ONTOLOGY_LOCK", "F12_DEFENSE"],
    "check_vital": ["F4_CLARITY", "F5_PEACE2", "F7_HUMILITY", "F3_TRI_WITNESS"],
}

AAA_TOOL_STAGE_MAP: dict[str, str] = {
    "anchor_session": "000_INIT",
    "reason_mind": "333_REASON",
    "recall_memory": "444_SYNC",
    "simulate_heart": "555_EMPATHY",
    "critique_thought": "666_ALIGN",
    "apex_judge": "888_JUDGE",
    "judge_soul": "888_JUDGE",
    "eureka_forge": "777_FORGE",
    "seal_vault": "999_SEAL",
    "search_reality": "111_SENSE",
    "fetch_content": "444_SYNC",
    "inspect_file": "111_SENSE",
    "audit_rules": "333_REASON",
    "check_vital": "555_EMPATHY",
}

READ_ONLY_TOOLS: set[str] = {
    "search_reality",
    "fetch_content",
    "inspect_file",
    "audit_rules",
    "check_vital",
}

__all__ = [
    "AAA_CANONICAL_TOOLS",
    "AAA_PROMPT_NAMES",
    "AAA_RESOURCE_URIS",
    "AAA_TOOL_ALIASES",
    "AAA_TOOL_LAW_BINDINGS",
    "AAA_TOOL_STAGE_MAP",
    "AXIOMS_333",
    "CANONICAL_TOOL_COUNT",
    "L1_PROMPTS",
    "L4_TOOLS",
    "L5_COMPOSITE",
    "LAW_13_CATALOG",
    "MANIFEST_VERSION",
    "MCP_FULL_SURFACE",
    "MCP_GOVERNED_TOOLS",
    "READ_ONLY_TOOLS",
    "TRINITY_BY_TOOL",
]
