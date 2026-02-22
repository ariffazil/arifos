"""
JSON Schema Definitions for All 13 Tools

Formal, deterministic, zero-ambiguity schemas.
Every field has explicit type, range, and semantics.

Version: 2026.02.22-LOW_ENTROPY
"""

from typing import Dict, Any

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

TOOL_INPUT_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "init_gate": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "description": "User query to initialize session for",
            },
            "session_id": {"type": "string", "description": "Optional existing session ID"},
            "grounding_required": {
                "type": "boolean",
                "default": True,
                "description": "Whether external grounding is mandatory",
            },
            "mode": {
                "type": "string",
                "enum": ["fluid", "strict"],
                "default": "fluid",
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
            "auth_token": {"type": ["string", "null"]},
            "require_sovereign_for_high_stakes": {"type": "boolean", "default": True},
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
        },
        "required": ["query", "session_id"],
    },
    "reality_search": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "session_id": {"type": "string"},
            "region": {"type": "string", "default": "wt-wt"},
            "timelimit": {"type": ["string", "null"], "enum": [None, "d", "w", "m", "y"]},
        },
        "required": ["query", "session_id"],
    },
    "vault_seal": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string"},
            "verdict": VERDICT_ENUM,
            "payload": {"type": "object"},
            "query_summary": {"type": ["string", "null"]},
            "risk_level": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
            "category": {
                "type": "string",
                "enum": ["finance", "safety", "content", "code", "governance"],
            },
        },
        "required": ["session_id", "verdict", "payload"],
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
}

# ═════════════════════════════════════════════════════════════════════════════
# TOOL OUTPUT SCHEMAS (Minimal, Low-Entropy)
# ═════════════════════════════════════════════════════════════════════════════

TOOL_OUTPUT_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "init_gate": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string"},
            "verdict": VERDICT_ENUM,
            "status": {"type": "string", "enum": ["READY", "VOID", "HOLD_888"]},
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
            "tri_witness": {"type": "number"},
            "votes": {"type": "object"},
            "justification": {"type": "string"},
            "stages": {"type": "object"},
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


def get_input_schema(tool_name: str) -> Dict[str, Any] | None:
    """Return input schema for legacy, canonical, or verb alias tool names."""
    return TOOL_INPUT_SCHEMAS.get(resolve_protocol_tool_name(tool_name))


def get_output_schema(tool_name: str) -> Dict[str, Any] | None:
    """Return output schema for legacy, canonical, or verb alias tool names."""
    return TOOL_OUTPUT_SCHEMAS.get(resolve_protocol_tool_name(tool_name))
