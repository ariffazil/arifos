"""
arifosmcp/runtime/contracts.py — Unified arifOS MCP Contracts

Public/main contract:
  - the 8-tool surface generated from arifosmcp.runtime.public_registry

Internal/dev compatibility:
  - stage tools and legacy aliases retained for orchestration and transition

This module keeps governance metadata and input validation aligned with that
split. It is not the hand-authored public contract page.
"""

from __future__ import annotations

from typing import Any

from .public_registry import public_tool_input_contracts, public_tool_names

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL SURFACES
# ═══════════════════════════════════════════════════════════════════════════════

AAA_PUBLIC_TOOLS: tuple[str, ...] = public_tool_names()

AAA_INTERNAL_STAGE_TOOLS: tuple[str, ...] = (
    "anchor_session",
    "reason_mind",
    "vector_memory",
    "simulate_heart",
    "critique_thought",
    "eureka_forge",
    "apex_judge",
    "seal_vault",
    "metabolic_loop",
    "trace_replay",
    "office_forge_audit",
    "forge_office_document",
    "ollama_local_generate",
    "lsp_query_tool",
    "lsp_get_symbols_tool",
    "lsp_get_diagnostics_tool",
    "lsp_go_to_definition_tool",
    "lsp_find_references_tool",
    "lsp_rename_tool",
)

AAA_CANONICAL_TOOLS: tuple[str, ...] = (
    *AAA_PUBLIC_TOOLS,
    *AAA_INTERNAL_STAGE_TOOLS,
)

REQUIRES_SESSION: set[str] = {
    "reason_mind",
    "vector_memory",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
    "forge_office_document",
    "ollama_local_generate",
}

READ_ONLY_TOOLS: set[str] = {
    "reality_compass",
    "ingest_evidence",
    "audit_rules",
    "check_vital",
    "verify_vault_ledger",
}

# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE METADATA
# ═══════════════════════════════════════════════════════════════════════════════

AAA_TOOL_STAGE_MAP: dict[str, str] = {
    "anchor_session": "000_INIT",
    "reason_mind": "333_MIND",
    "vector_memory": "555_MEMORY",
    "simulate_heart": "666_HEART",
    "critique_thought": "666_HEART",
    "eureka_forge": "777_FORGE",
    "apex_judge": "888_JUDGE",
    "judge_soul": "888_JUDGE",
    "seal_vault": "999_VAULT",
    "reality_compass": "111_SENSE",
    "reality_atlas": "222_REALITY",
    "search_reality": "111_SENSE",
    "ingest_evidence": "222_REALITY",
    "audit_rules": "333_MIND",
    "check_vital": "000_INIT",
    "metabolic_loop": "444_ROUTER",
    "verify_vault_ledger": "999_VAULT",
    "trace_replay": "999_VAULT",
    "office_forge_audit": "777_FORGE",
    "forge_office_document": "777_FORGE",
    "ollama_local_generate": "333_MIND",
    "lsp_query_tool": "111_SENSE",
    "lsp_get_symbols_tool": "111_SENSE",
    "lsp_get_diagnostics_tool": "111_SENSE",
    "lsp_go_to_definition_tool": "111_SENSE",
    "lsp_find_references_tool": "111_SENSE",
    "lsp_rename_tool": "111_SENSE",
}

TRINITY_BY_TOOL: dict[str, str] = {
    "anchor_session": "Delta",
    "reason_mind": "Delta",
    "vector_memory": "Omega",
    "simulate_heart": "Omega",
    "critique_thought": "Omega",
    "apex_judge": "Psi",
    "judge_soul": "Psi",
    "eureka_forge": "Psi",
    "seal_vault": "Psi",
    "reality_compass": "Delta",
    "reality_atlas": "Delta",
    "search_reality": "Delta",
    "ingest_evidence": "Delta",
    "audit_rules": "Delta",
    "check_vital": "Omega",
    "metabolic_loop": "ALL",
    "verify_vault_ledger": "Psi",
    "trace_replay": "Psi",
    "office_forge_audit": "Psi",
    "forge_office_document": "Psi",
    "ollama_local_generate": "Delta",
    "lsp_query_tool": "Delta",
    "lsp_get_symbols_tool": "Delta",
    "lsp_get_diagnostics_tool": "Delta",
    "lsp_go_to_definition_tool": "Delta",
    "lsp_find_references_tool": "Delta",
    "lsp_rename_tool": "Delta",
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
    "reason_mind": [
        "F2_TRUTH",
        "F4_CLARITY",
        "F7_HUMILITY",
        "F8_GENIUS",
        "F3_TRI_WITNESS",
        "F11_AUTHORITY",
    ],
    "vector_memory": [
        "F4_CLARITY",
        "F7_HUMILITY",
        "F3_TRI_WITNESS",
        "F13_SOVEREIGNTY",
        "F11_AUTHORITY",
    ],
    "simulate_heart": ["F5_PEACE2", "F6_EMPATHY", "F4_CLARITY", "F3_TRI_WITNESS", "F11_AUTHORITY"],
    "critique_thought": [
        "F4_CLARITY",
        "F7_HUMILITY",
        "F8_GENIUS",
        "F12_DEFENSE",
        "F3_TRI_WITNESS",
        "F11_AUTHORITY",
    ],
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
    "eureka_forge": [
        "F5_PEACE2",
        "F6_EMPATHY",
        "F7_HUMILITY",
        "F9_ANTI_HANTU",
        "F13_SOVEREIGNTY",
    ],
    "seal_vault": ["F1_AMANAH", "F3_TRI_WITNESS", "F10_ONTOLOGY_LOCK", "F13_SOVEREIGNTY"],
    "reality_compass": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "reality_atlas": ["F2_TRUTH", "F4_CLARITY", "F11_AUTHORITY"],
    "search_reality": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "ingest_evidence": ["F1_AMANAH", "F2_TRUTH", "F4_CLARITY", "F11_AUTHORITY", "F12_DEFENSE"],
    "audit_rules": ["F2_TRUTH", "F8_GENIUS", "F10_ONTOLOGY_LOCK", "F12_DEFENSE"],
    "check_vital": ["F4_CLARITY", "F5_PEACE2", "F7_HUMILITY", "F3_TRI_WITNESS"],
    "metabolic_loop": ["F1_AMANAH", "F2_TRUTH", "F3_TRI_WITNESS", "F4_CLARITY", "F13_SOVEREIGNTY"],
    "verify_vault_ledger": ["F13_SOVEREIGNTY"],
    "trace_replay": ["F2_TRUTH", "F3_TRI_WITNESS", "F13_SOVEREIGNTY"],
    "office_forge_audit": ["F4_CLARITY", "F7_HUMILITY", "F12_DEFENSE"],
    "forge_office_document": [
        "F1_AMANAH",
        "F4_CLARITY",
        "F11_AUTHORITY",
        "F12_DEFENSE",
        "F13_SOVEREIGNTY",
    ],
    "ollama_local_generate": [
        "F2_TRUTH",
        "F4_CLARITY",
        "F7_HUMILITY",
        "F11_AUTHORITY",
        "F12_DEFENSE",
    ],
    "lsp_query_tool": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "lsp_get_symbols_tool": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "lsp_get_diagnostics_tool": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "lsp_go_to_definition_tool": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "lsp_find_references_tool": ["F2_TRUTH", "F4_CLARITY", "F12_DEFENSE"],
    "lsp_rename_tool": ["F1_AMANAH", "F2_TRUTH", "F11_AUTHORITY", "F12_DEFENSE", "F13_SOVEREIGNTY"],
}

AAA_TOOL_ALIASES: dict[str, str] = {
    "metabolicloop": "metabolic_loop",
    "init_session": "anchor_session",
    "agi_cognition": "reason_mind",
    "phoenix_recall": "vector_memory",
    "recall_memory": "vector_memory",
    "memory_search": "vector_memory",
    "asi_empathy": "simulate_heart",
    "apex_verdict": "apex_judge",
    "judge_soul": "apex_judge",
    "sovereign_actuator": "eureka_forge",
    "vault_seal": "seal_vault",
    "search": "reality_compass",
    "compass": "reality_compass",
    "atlas": "reality_atlas",
    "reality_atlas": "reality_atlas",
    "search_reality": "reality_compass",
    "fetch": "ingest_evidence",
    "fetch_content": "ingest_evidence",
    "inspect_file": "ingest_evidence",
    "analyze": "ingest_evidence",
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

TOOL_INPUT_CONTRACTS: dict[str, dict[str, str]] = {
    **public_tool_input_contracts(),
    "anchor_session": {"query": "str", "actor_id": "str", "session_id": "str"},
    "reason_mind": {"query": "str", "session_id": "str"},
    "vector_memory": {"query": "str", "session_id": "str"},
    "simulate_heart": {"query": "str", "session_id": "str"},
    "critique_thought": {"thought_id": "str", "session_id": "str"},
    "apex_judge": {"session_id": "str", "verdict_candidate": "str"},
    "eureka_forge": {
        "session_id": "str",
        "intent": "str",
    },
    "seal_vault": {"session_id": "str", "verdict": "str"},
    "trace_replay": {},
    "metabolic_loop": {"query": "str"},
    "office_forge_audit": {"markdown": "str"},
    "forge_office_document": {
        "session_id": "str",
        "markdown": "str",
        "output_mode": "str",
    },
    "ollama_local_generate": {"prompt": "str", "model": "str"},
    "lsp_query_tool": {"file_path": "str", "query_type": "str"},
    "lsp_get_symbols_tool": {"file_path": "str"},
    "lsp_get_diagnostics_tool": {"file_path": "str"},
    "lsp_go_to_definition_tool": {"file_path": "str", "line": "int", "character": "int"},
    "lsp_find_references_tool": {"file_path": "str", "line": "int", "character": "int"},
    "lsp_rename_tool": {
        "file_path": "str",
        "line": "int",
        "character": "int",
        "new_name": "str",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# TWO-LAYER IDENTITY ENVELOPE (F9/F10 compliant)
#
# Every tool call envelope must carry two identity layers, auto-populated by
# the MCP server:
#   1. auth_context  — Human authority layer (never AI)
#   2. caller_context — AI execution identity layer (instrument, not sovereign)
#
# The LLM may provide a `requested_persona` hint (advisory only); the server
# governs the final caller_context.persona_id.
# ═══════════════════════════════════════════════════════════════════════════════

#: JSON Schema for the human authority layer.
AUTH_CONTEXT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": "Human authority layer. Populated by MCP server. Never the AI model.",
    "properties": {
        "actor_id": {
            "type": "string",
            "description": "Human or org identity (e.g. 'arif', 'petronas_ciso').",
        },
        "token_fingerprint": {
            "type": "string",
            "description": "Cryptographic session fingerprint.",
        },
        "authority_level": {
            "type": "string",
            "enum": ["anonymous", "user", "admin", "apex"],
            "description": "Permission or approval scope.",
        },
        "continuity": {
            "type": "string",
            "enum": ["session", "thread", "case", "none"],
            "description": "Continuity anchor for audit/logging.",
        },
    },
    "required": ["actor_id", "authority_level", "token_fingerprint"],
}

#: JSON Schema for the AI runtime identity layer.
CALLER_CONTEXT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "description": (
        "AI execution identity layer. Instrument only — never inherits human sovereignty (F9/F10). "
        "Populated by the MCP server from transport metadata. The LLM may supply a "
        "`requested_persona` hint but the server governs the final persona_id."
    ),
    "properties": {
        "agent_id": {
            "type": "string",
            "description": "Stable runtime instance ID (e.g. 'gpt-runtime-01').",
        },
        "model_id": {
            "type": "string",
            "description": "Model/version string (e.g. 'claude-3-5-sonnet').",
        },
        "persona_id": {
            "type": "string",
            "enum": ["architect", "engineer", "auditor", "validator"],
            "description": (
                "Governed operational persona. Server-assigned; LLM hint via "
                "`requested_persona` field is advisory only."
            ),
        },
        "runtime_role": {
            "type": "string",
            "enum": ["assistant", "router", "tool_broker", "evaluator"],
            "description": "Operational role for this call.",
        },
        "toolchain_role": {
            "type": "string",
            "enum": ["orchestrator", "leaf", "subagent"],
            "description": "Position in multi-agent/tool chain.",
        },
        "extra": {
            "type": "object",
            "description": "Forward-compatible extension slot for future fields.",
        },
    },
    "required": ["persona_id", "runtime_role"],
}

#: Valid persona hints that the LLM client may suggest.
VALID_PERSONA_HINTS: frozenset[str] = frozenset({"architect", "engineer", "auditor", "validator"})


def require_session(tool: str, session_id: str | None) -> dict[str, Any] | None:
    if tool in REQUIRES_SESSION and (not session_id or not str(session_id).strip()):
        return {
            "verdict": "HOLD",
            "stage": "F11_AUTH",
            "floors_failed": ["F11"],
            "error": "Missing session_id",
            "next_actions": [
                "Call anchor_session first.",
                "Reuse returned session_id for downstream tools.",
            ],
        }
    return None


def validate_input(tool: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    contract = TOOL_INPUT_CONTRACTS.get(tool, {})
    for key, type_name in contract.items():
        if key not in payload:
            return {
                "verdict": "HOLD",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Missing required field: {key}",
            }
        value = payload[key]
        if type_name == "str" and (not isinstance(value, str) or not str(value).strip()):
            return {
                "verdict": "HOLD",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Field '{key}' must be non-empty string",
            }
        if type_name == "dict" and not isinstance(value, dict):
            return {
                "verdict": "HOLD",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Field '{key}' must be object",
            }
        if type_name == "bool" and not isinstance(value, bool):
            return {
                "verdict": "HOLD",
                "stage": "F3_CONTRACT",
                "floors_failed": ["F3"],
                "error": f"Field '{key}' must be boolean",
            }
    return None
