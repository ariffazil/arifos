"""
JSON Schema Definitions for All 13 Tools

Formal, deterministic, zero-ambiguity schemas.
Every field has explicit type, range, and semantics.

Version: 2026.03.07-QUADWITNESS-SEAL
Changes: apex_verdict output updated tri_witness -> quad_witness (W4).
         PsiShadow verifier witness fields added.
         critique_thought output schema reflects Psi-Shadow adversarial fields.
"""

from typing import Any

from .tool_naming import CANONICAL_PUBLIC_TO_LEGACY, resolve_protocol_tool_name

# ═════════════════════════════════════════════════════════════════════════════
# COMMON DEFINITIONS
# ═════════════════════════════════════════════════════════════════════════════

VERDICT_ENUM = {"type": "string", "enum": ["SEAL", "PARTIAL", "VOID", "888_HOLD"]}
STAGE_ENUM = {
    "type": "string",
    "enum": ["000", "111", "222", "333", "444", "555", "666", "777", "888", "999"],
}
LANE_ENUM = {"type": "string", "enum": ["SOCIAL", "CARE", "FACTUAL", "CRISIS"]}

EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "evidence_id": {"type": "string"},
        "content": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "hash": {"type": "string"},
                "language": {"type": "string"},
            },
            "required": ["text"],
        },
        "source_meta": {
            "type": "object",
            "properties": {
                "uri": {"type": "string"},
                "type": {"type": "string", "enum": ["AXIOM", "WEB", "EMPIRICAL", "CONFLICT"]},
                "author": {"type": "string"},
                "timestamp": {"type": "string"},
            },
        },
        "metrics": {
            "type": "object",
            "properties": {
                "trust_weight": {"type": "number", "minimum": 0, "maximum": 1},
                "relevance_score": {"type": "number", "minimum": 0, "maximum": 1},
            },
        },
    },
    "required": ["evidence_id", "content"],
}

# ═════════════════════════════════════════════════════════════════════════════
# TOOL INPUT SCHEMAS
# ═════════════════════════════════════════════════════════════════════════════

TOOL_INPUT_SCHEMAS: dict[str, dict[str, Any]] = {
    "init_gate": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "description": "User query to initialize session for",
            },
            "actor_id": {
                "type": "string",
                "default": "anonymous",
                "description": "Actor identifier used for F11 authority continuity",
            },
            "auth_token": {
                "type": ["string", "null"],
                "description": "Optional authority token for strict environments",
            },
            "session_id": {"type": "string", "description": "Optional existing session ID"},
            "grounding_required": {
                "type": "boolean",
                "default": True,
                "description": "Whether external grounding is mandatory",
            },
            "mode": {
                "type": "string",
                "enum": ["fluid", "strict", "conscience", "ghost"],
                "default": "conscience",
                "description": "Governance strictness mode",
            },
        },
        "required": ["query"],
    },
    "trinity_forge": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "actor_id": {"type": "string", "default": "user"},
            "session_id": {
                "type": ["string", "null"],
                "description": "Optional existing session for continuity from anchor/init_session",
            },
            "auth_token": {"type": ["string", "null"]},
            "require_sovereign_for_high_stakes": {"type": "boolean", "default": True},
            "template_id": {
                "type": "string",
                "default": "arifos.full_context.v1",
                "description": "Full-context resource template identifier",
            },
            "mode": {
                "type": "string",
                "enum": ["ghost", "conscience"],
                "default": "conscience",
                "description": "Governance mode: ghost (log only) or conscience (enforce)",
            },
            "output_mode": {
                "type": "string",
                "enum": ["user", "developer", "audit"],
                "default": "user",
                "description": "Output detail level",
            },
        },
        "required": ["query"],
    },
    "agi_sense": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
        },
        "required": ["query", "session_id"],
    },
    "agi_think": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
        },
        "required": ["query", "session_id"],
    },
    "agi_reason": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
            "actor_id": {"type": "string"},
            "auth_token": {"type": ["string", "null"]},
            "grounding": {
                "type": ["object", "null"],
                "description": "Optional structured grounding data",
            },
        },
        "required": ["query", "session_id"],
    },
    "asi_empathize": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
            "actor_id": {"type": "string"},
            "auth_token": {"type": ["string", "null"]},
            "stakeholders": {"type": ["array", "null"], "items": {"type": "string"}},
        },
        "required": ["query", "session_id"],
    },
    "asi_align": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
        },
        "required": ["query", "session_id"],
    },
    "apex_verdict": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
            "actor_id": {"type": "string"},
            "auth_token": {"type": ["string", "null"]},
            "proposed_verdict": VERDICT_ENUM,
            "human_approve": {"type": "boolean", "default": False},
            "agi_result": {"type": ["object", "null"]},
            "asi_result": {"type": ["object", "null"]},
        },
        "required": ["query", "session_id"],
    },
    "reality_search": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "description": "Legacy alias for grounding_query",
            },
            "grounding_query": {
                "type": "string",
                "minLength": 1,
                "description": "The external query for web grounding discovery.",
            },
            "session_id": {"type": "string", "description": "Legacy alias for session_token"},
            "session_token": {
                "type": "string",
                "description": "The active session identifier for context grouping.",
            },
            "region": {"type": "string", "default": "wt-wt"},
            "timelimit": {"type": ["string", "null"], "enum": [None, "d", "w", "m", "y"]},
        },
        "anyOf": [
            {"required": ["query", "session_id"]},
            {"required": ["grounding_query", "session_token"]},
            {"required": ["grounding_query", "session_id"]},
            {"required": ["query", "session_token"]},
        ],
    },
    "vault_seal": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string"},
            "summary": {
                "type": "string",
                "description": "Human-readable immutable summary of the session work.",
            },
            "governance_token": {
                "type": "string",
                "description": "Evidence from apex_judge that this session is ratified.",
            },
        },
        "required": ["session_id", "summary", "governance_token"],
    },
    "vault_query": {
        "type": "object",
        "properties": {
            "session_pattern": {"type": ["string", "null"]},
            "verdict": {
                "type": ["string", "null"],
                "enum": [None, "SEAL", "VOID", "PARTIAL", "SABAR"],
            },
            "date_from": {"type": ["string", "null"]},
            "date_to": {"type": ["string", "null"]},
            "risk_level": {"type": ["string", "null"]},
            "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10},
        },
    },
    "tool_router": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
        },
        "required": ["query"],
    },
    "truth_audit": {
        "type": "object",
        "properties": {
            "text": {"type": "string", "minLength": 1},
            "sources": {"type": ["array", "null"], "items": {"type": "string"}},
            "lane": {"type": "string", "enum": ["HARD", "SOFT"], "default": "HARD"},
            "session_id": {"type": ["string", "null"]},
        },
        "required": ["text"],
    },
    "vector_memory": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "description": "The retrieval query to embed and match semantically.",
            },
            "session_id": {
                "type": "string",
                "description": "The active session identifier for context grouping.",
            },
            "depth": {"type": "integer", "minimum": 1, "maximum": 10, "default": 3},
            "domain": {
                "type": "string",
                "enum": ["canon", "manifesto", "docs", "all"],
                "default": "canon",
            },
            "debug": {"type": "boolean", "default": False},
        },
        "required": ["query", "session_id"],
    },
    "phoenix_recall": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
            "depth": {"type": "integer", "minimum": 1, "maximum": 10, "default": 3},
            "domain": {
                "type": "string",
                "enum": ["canon", "manifesto", "docs", "all"],
                "default": "canon",
            },
            "debug": {"type": "boolean", "default": False},
        },
        "required": ["query", "session_id"],
    },
    "sovereign_actuator": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string"},
            "command": {
                "type": "string",
                "minLength": 1,
                "description": "Shell command to execute in the sandbox.",
            },
            "working_dir": {
                "type": "string",
                "default": "/root",
                "description": "Current working directory for the command.",
            },
            "timeout": {
                "type": "integer",
                "minimum": 1,
                "default": 60,
                "description": "Execution timeout in seconds.",
            },
            "confirm_dangerous": {
                "type": "boolean",
                "default": False,
                "description": "Mandatory 'True' for dangerous commands (rm, mkfs, etc).",
            },
            "agent_id": {
                "type": "string",
                "default": "unknown",
                "description": "Deterministic ID of the agent requesting the forge.",
            },
            "purpose": {
                "type": "string",
                "default": "",
                "description": "Human-readable intent for constitutional logging (F9).",
            },
        },
        "required": ["session_id", "command"],
    },
    "ingest_evidence": {
        "type": "object",
        "properties": {
            "source_type": {"type": "string", "enum": ["url", "file"]},
            "target": {"type": "string", "minLength": 1},
            "mode": {"type": "string", "enum": ["raw", "summary", "chunks"], "default": "raw"},
            "max_chars": {"type": "integer", "default": 4000},
            "session_id": {"type": ["string", "null"]},
            "depth": {"type": "integer", "default": 1},
            "include_hidden": {"type": "boolean", "default": False},
            "pattern": {"type": "string", "default": "*"},
            "min_size_bytes": {"type": "integer", "default": 0},
            "max_files": {"type": "integer", "default": 100},
        },
        "required": ["source_type", "target"],
    },
    "metabolic_loop": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "risktier": {"type": "string", "default": "high"},
            "actor_id": {"type": "string", "default": "antigravity-agent"},
            "proposed_verdict": {"type": "string", "default": "SEAL"},
        },
        "required": ["query"],
    },
    "fetch": {
        "type": "object",
        "properties": {
            "id": {"type": "string", "minLength": 1},
            "max_chars": {"type": "integer", "minimum": 1, "default": 4000},
        },
        "required": ["id"],
    },
    "analyze": {
        "type": "object",
        "properties": {
            "data": {"type": "object"},
            "analysis_type": {"type": "string", "default": "structure"},
        },
        "required": ["data"],
    },
    "system_audit": {
        "type": "object",
        "properties": {
            "audit_scope": {"type": "string", "default": "quick"},
            "verify_floors": {"type": "boolean", "default": True},
        },
    },
    "sense_health": {
        "type": "object",
        "properties": {},
    },
    "sense_fs": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "default": "."},
            "depth": {"type": "integer", "minimum": 0, "default": 1},
        },
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# TOOL OUTPUT SCHEMAS (Minimal, Low-Entropy)
# ═════════════════════════════════════════════════════════════════════════════

TOOL_OUTPUT_SCHEMAS: dict[str, dict[str, Any]] = {
    "init_gate": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string"},
            "verdict": VERDICT_ENUM,
            "status": {"type": "string", "enum": ["READY", "VOID", "HOLD_888"]},
            "token_status": {"type": ["string", "null"]},
            "next_action": {"type": ["string", "null"]},
            "remediation": {"type": ["string", "null"]},
            "grounding_required": {"type": "boolean"},
            "mode": {"type": "string"},
            "stage": {"type": "string", "const": "000"},
        },
        "required": ["session_id", "verdict", "status", "stage"],
    },
    "trinity_forge": {
        "type": "object",
        "properties": {
            "verdict": VERDICT_ENUM,
            "session_id": {"type": "string"},
            "token_status": {"type": "string"},
            "next_action": {"type": ["string", "null"]},
            "remediation": {"type": ["string", "null"]},
            "agi": {"type": "object"},
            "asi": {"type": "object"},
            "apex": {"type": "object"},
            "seal": {"type": "object"},
            "emd": {
                "type": "object",
                "description": "Energy-Metabolism-Decision tensor (audit mode only)",
            },
            "landauer_risk": {"type": "number", "description": "Hallucination risk score"},
            "mode": {"type": "string", "enum": ["ghost", "conscience"]},
            "_constitutional": {
                "type": "object",
                "description": "Full constitutional metrics (developer/audit mode)",
                "properties": {
                    "delta_s": {"type": "number"},
                    "omega_0": {"type": "number"},
                    "kappa_r": {"type": "number"},
                    "genius_g": {"type": "number"},
                    "peace2": {"type": "number"},
                    "landauer_risk": {"type": "number"},
                    "e_eff": {"type": "number"},
                    "mode": {"type": "string"},
                    "floors": {"type": "object"},
                },
            },
        },
        "required": ["verdict", "session_id"],
    },
    "agi_sense": {
        "type": "object",
        "properties": {
            "stage": {"type": "string", "const": "111"},
            "intent": {"type": "string"},
            "lane": LANE_ENUM,
            "requires_grounding": {"type": "boolean"},
            "truth_score": {"type": "number", "minimum": 0, "maximum": 1},
            "evidence": {"type": "array", "items": EVIDENCE_SCHEMA},
        },
        "required": ["stage", "intent", "lane"],
    },
    "agi_think": {
        "type": "object",
        "properties": {
            "stage": {"type": "string", "const": "222"},
            "hypotheses": {"type": "array"},
            "confidence_range": {"type": "array", "items": {"type": "number"}},
            "recommended_path": {"type": "string"},
            "evidence": {"type": "array", "items": EVIDENCE_SCHEMA},
        },
        "required": ["stage", "hypotheses"],
    },
    "agi_reason": {
        "type": "object",
        "properties": {
            "stage": {"type": "string", "const": "333"},
            "verdict": VERDICT_ENUM,
            "truth_score": {"type": "number", "minimum": 0, "maximum": 1},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "entropy_delta": {"type": "number"},
            "humility_omega": {"type": "number", "minimum": 0, "maximum": 1},
            "genius_score": {"type": "number", "minimum": 0, "maximum": 1},
            "evidence": {"type": "array", "items": EVIDENCE_SCHEMA},
        },
        "required": ["stage", "verdict", "truth_score"],
    },
    "asi_empathize": {
        "type": "object",
        "properties": {
            "stage": {"type": "string", "const": "555"},
            "verdict": VERDICT_ENUM,
            "empathy_kappa_r": {"type": "number", "minimum": 0, "maximum": 1},
            "stakeholders": {"type": "array"},
            "high_vulnerability": {"type": "boolean"},
            "stage_555": {"type": "object"},
        },
        "required": ["stage", "verdict", "empathy_kappa_r"],
    },
    "asi_align": {
        "type": "object",
        "properties": {
            "stage": {"type": "string", "const": "666"},
            "verdict": VERDICT_ENUM,
            "is_reversible": {"type": "boolean"},
            "stage_666": {"type": "object"},
        },
        "required": ["stage", "verdict"],
    },
    "apex_verdict": {
        "type": "object",
        "properties": {
            "stage": {"type": "string", "const": "888"},
            "verdict": VERDICT_ENUM,
            "truth_score": {"type": "number", "minimum": 0, "maximum": 1},
            "session_id": {"type": "string"},
            "query": {"type": "string"},
            # Quad-Witness (W4) — replaces tri_witness (W3)
            "quad_witness_valid": {"type": "boolean"},
            "witness": {
                "type": "object",
                "properties": {
                    "w4": {"type": "number", "minimum": 0, "maximum": 1,
                           "description": "Quad-Witness geometric mean (H*A*E*V)^(1/4) >= 0.75"},
                    "w3": {"type": "number", "minimum": 0, "maximum": 1,
                           "description": "Tri-Witness (backward compat, deprecated)"},
                    "human": {
                        "type": "object",
                        "properties": {
                            "valid": {"type": "boolean"},
                            "score": {"type": "number", "minimum": 0, "maximum": 1},
                        },
                    },
                    "ai": {
                        "type": "object",
                        "properties": {
                            "valid": {"type": "boolean"},
                            "score": {"type": "number", "minimum": 0, "maximum": 1},
                        },
                    },
                    "earth": {
                        "type": "object",
                        "properties": {
                            "valid": {"type": "boolean"},
                            "score": {"type": "number", "minimum": 0, "maximum": 1},
                        },
                    },
                    "verifier": {
                        "type": "object",
                        "description": "Psi-Shadow adversarial witness (4th witness, V)",
                        "properties": {
                            "valid": {"type": "boolean"},
                            "score": {"type": "number", "minimum": 0, "maximum": 1},
                            "signals": {
                                "type": "object",
                                "properties": {
                                    "attacks_found": {"type": "boolean"},
                                    "contradictions": {"type": "array"},
                                    "harm_scenarios": {"type": "array"},
                                    "injection_vectors": {"type": "array"},
                                    "critique_verdict": {"type": "string", "enum": ["APPROVE", "REJECT"]},
                                },
                            },
                        },
                    },
                },
            },
            "votes": {"type": "object"},
            "justification": {"type": "string"},
            "stages": {"type": "object"},
            # Keep tri_witness for backward compatibility during transition
            "tri_witness": {"type": "number", "description": "Deprecated — use witness.w4"},
        },
        "required": ["stage", "verdict", "truth_score", "session_id"],
    },
    "reality_search": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "session_id": {"type": "string"},
            "evidence": {"type": "array", "items": EVIDENCE_SCHEMA},
            "verdict": VERDICT_ENUM,
            "stage": {"type": "string", "const": "222"},
        },
        "required": ["query", "session_id", "evidence", "stage"],
    },
    "vault_seal": {
        "type": "object",
        "properties": {
            "verdict": {"type": "string", "enum": ["SEALED", "PARTIAL"]},
            "seal_id": {"type": ["string", "null"]},
            "seal": {"type": "string"},
            "session_id": {"type": "string"},
            "stage": {"type": "string", "const": "999"},
            "risk_level": {"type": "string"},
        },
        "required": ["verdict", "seal", "session_id", "stage"],
    },
    "vault_query": {
        "type": "object",
        "properties": {
            "count": {"type": "integer"},
            "entries": {"type": "array"},
            "patterns": {"type": "object"},
        },
        "required": ["count", "entries"],
    },
    "tool_router": {
        "type": "object",
        "properties": {
            "plan_id": {"type": "string"},
            "recommended_pipeline": {"type": "array", "items": {"type": "string"}},
            "lane": {"type": "string"},
            "entropy_score": {"type": "number"},
            "grounding_required": {"type": "boolean"},
            "justification": {"type": "string"},
            "instruction": {"type": "string"},
            "stage": {"type": "string", "const": "ROUTER"},
        },
        "required": ["plan_id", "recommended_pipeline"],
    },
    "truth_audit": {
        "type": "object",
        "properties": {
            "overall_verdict": VERDICT_ENUM,
            "overall_truth": {"type": "number"},
            "claims": {"type": "array"},
            "apex_justification": {"type": "string"},
            "omega_0": {"type": "number"},
        },
        "required": ["overall_verdict", "overall_truth", "claims"],
    },
    "phoenix_recall": {
        "type": "object",
        "properties": {
            "verdict": VERDICT_ENUM,
            "stage": {"type": "string", "const": "555_RECALL"},
            "session_id": {"type": "string"},
            "status": {"type": "string"},
            "memories": {"type": "array"},
            "metrics": {"type": "object"},
        },
        "required": ["verdict", "stage", "session_id"],
    },
    "sovereign_actuator": {
        "type": "object",
        "properties": {
            "verdict": VERDICT_ENUM,
            "stage": {"type": "string", "const": "888_FORGE"},
            "session_id": {"type": "string"},
            "status": {"type": "string"},
            "message": {"type": "string"},
            "instruction": {"type": "string"},
        },
        "required": ["verdict", "stage", "session_id"],
    },
    "ingest_evidence": {
        "type": "object",
        "properties": {
            "target": {"type": "string"},
            "status": {"type": "string"},
            "content": {"type": "string"},
            "metadata": {"type": "object"},
            "error": {"type": "string"},
        },
        "required": ["target", "status"],
    },
    "metabolic_loop": {
        "type": "object",
        "properties": {
            "verdict": VERDICT_ENUM,
            "session_id": {"type": "string"},
            "risktier": {"type": "string"},
            "governance_token": {"type": ["string", "null"]},
            "next_actions": {"type": "array"},
            "floors_state": {"type": "object"},
            "summary": {"type": "string"},
            "guidance": {"type": "string"},
            "trace": {"type": "object"},
        },
        "required": ["verdict", "session_id"],
    },
    "fetch": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "status": {"type": "string"},
            "content": {"type": "string"},
            "truncated": {"type": "boolean"},
            "error": {"type": "string"},
        },
        "required": ["id", "status"],
    },
    "analyze": {
        "type": "object",
        "properties": {
            "verdict": VERDICT_ENUM,
            "analysis_type": {"type": "string"},
            "depth": {"type": "integer"},
            "keys": {"type": "array", "items": {"type": "string"}},
            "message": {"type": "string"},
            "error": {"type": "string"},
        },
    },
    "system_audit": {
        "type": "object",
        "properties": {
            "verdict": VERDICT_ENUM,
            "scope": {"type": "string"},
            "details": {"type": "object"},
            "error": {"type": "string"},
        },
        "required": ["scope"],
    },
    "sense_health": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
        },
        "required": ["status"],
    },
    "sense_fs": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
        },
        "required": ["status"],
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# STAGE OPERATOR MAPPINGS
# ═════════════════════════════════════════════════════════════════════════════

STAGE_OPERATORS = {
    "000": {"operator": "EARNED", "tool": "init_gate"},
    "111": {"operator": "EXAMINE", "tool": "agi_sense"},
    "222": {"operator": "EXPLORE", "tool": "agi_think"},
    "333": {"operator": "CLARIFY", "tool": "agi_reason"},
    "444": {"operator": "FACE", "tool": "apex_verdict"},
    "555": {"operator": "CALM", "tool": "asi_empathize"},
    "666": {"operator": "PROTECT", "tool": "asi_align"},
    "777": {"operator": "WORK", "tool": "apex_verdict"},
    "888": {"operator": "AWARE", "tool": "apex_verdict"},
    "999": {"operator": "SEAL", "tool": "vault_seal"},
}

# ═════════════════════════════════════════════════════════════════════════════
# OUTPUT CONTRACTS
# ═════════════════════════════════════════════════════════════════════════════

OUTPUT_CONTRACTS = {
    "default": {
        "always_include": ["verdict", "stage"],
        "include_if_not_default": {
            "justification": "(only if verdict != SEAL)",
            "risk_level": "(only if != 'low')",
            "warnings": "(only if present)",
        },
    },
    "user_mode": {
        "max_fields": 8,
        "forbidden_prefixes": ["_", "internal_", "debug_"],
    },
    "internal_mode": {
        "max_fields": None,
        "forbidden_prefixes": [],
    },
}

# Combined registry
TOOL_SCHEMAS = {
    "inputs": TOOL_INPUT_SCHEMAS,
    "outputs": TOOL_OUTPUT_SCHEMAS,
}

# Canonical public view (5-organs + search alias to reality_search)
CANONICAL_TOOL_INPUT_SCHEMAS = {
    canonical_name: TOOL_INPUT_SCHEMAS[legacy_name]
    for canonical_name, legacy_name in CANONICAL_PUBLIC_TO_LEGACY.items()
    if legacy_name in TOOL_INPUT_SCHEMAS
}
CANONICAL_TOOL_OUTPUT_SCHEMAS = {
    canonical_name: TOOL_OUTPUT_SCHEMAS[legacy_name]
    for canonical_name, legacy_name in CANONICAL_PUBLIC_TO_LEGACY.items()
    if legacy_name in TOOL_OUTPUT_SCHEMAS
}


def get_input_schema(tool_name: str) -> dict[str, Any] | None:
    """Return input schema for legacy, canonical, or verb alias tool names."""
    return TOOL_INPUT_SCHEMAS.get(resolve_protocol_tool_name(tool_name))


def get_output_schema(tool_name: str) -> dict[str, Any] | None:
    """Return output schema for legacy, canonical, or verb alias tool names."""
    return TOOL_OUTPUT_SCHEMAS.get(resolve_protocol_tool_name(tool_name))
