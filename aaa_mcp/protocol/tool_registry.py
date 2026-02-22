"""
Canonical Tool Path Registry — v60.0-FORGE

Ensures deterministic, callable tool paths for all AAA MCP tools.
Prevents "connector not installed" confusion by providing stable identifiers.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ToolSpec:
    """Canonical specification for an AAA MCP tool."""

    name: str  # Tool name (e.g., "init_gate")
    canonical_path: str  # Stable identifier (e.g., "aaa.init_gate")
    stage: str  # Pipeline stage (000-999)
    trinity: str  # Δ, Ω, Ψ, or ALL
    verb: str  # Human action (anchor, reason, validate, etc.)
    required_floors: List[str]  # Constitutional floors
    next_tool: Optional[str]  # Next tool in pipeline (None if terminal)

    # v60: Machine-readable intent tags for agent routing
    category: str  # "entry" | "reasoning" | "safety" | "judgment" | "audit"
    risk_scope: str  # "low" | "medium" | "high"
    hard_floors: List[str]  # Which floors are HARD at this stage
    requires_human_for: List[str]  # Conditions requiring human (e.g., ["prod", "finance"])

    # v60: Documentation tiers (short for agents, long for humans)
    doc_short: str  # 3-6 lines, agent-friendly
    doc_long: str  # Full governance spec (external link or full text)

    # v60: Availability status
    availability: str  # "ready" | "requires_install" | "disabled"
    install_hint: Optional[str]  # How to enable if not ready


# ═════════════════════════════════════════════════════════════════════════════
# CANONICAL TOOL REGISTRY
# ═════════════════════════════════════════════════════════════════════════════

CANONICAL_TOOLS: Dict[str, ToolSpec] = {
    # 000_INIT — Entry
    "init_gate": ToolSpec(
        name="init_gate",
        canonical_path="aaa.init_gate",
        stage="000",
        trinity="IGNITE",
        verb="anchor",
        required_floors=["F11", "F12"],
        next_tool="aaa.agi_sense",
        category="entry",
        risk_scope="low",
        hard_floors=["F11", "F12"],
        requires_human_for=[],
        doc_short="Initialize a constitutional session. CALL THIS FIRST. Returns session_id for pipeline.",
        doc_long="https://docs.arifos.org/tools/init_gate",
        availability="ready",
        install_hint=None,
    ),
    # 111-333 — AGI Mind (Δ)
    "agi_sense": ToolSpec(
        name="agi_sense",
        canonical_path="aaa.agi_sense",
        stage="111",
        trinity="Δ",
        verb="sense",
        required_floors=["F2", "F4"],
        next_tool="aaa.agi_think",
        category="reasoning",
        risk_scope="low",
        hard_floors=[],
        requires_human_for=[],
        doc_short="Parse intent and classify query lane. Requires init_gate session.",
        doc_long="https://docs.arifos.org/tools/agi_sense",
        availability="ready",
        install_hint=None,
    ),
    "agi_think": ToolSpec(
        name="agi_think",
        canonical_path="aaa.agi_think",
        stage="222",
        trinity="Δ",
        verb="think",
        required_floors=["F2", "F4", "F7"],
        next_tool="aaa.agi_reason",
        category="reasoning",
        risk_scope="low",
        hard_floors=[],
        requires_human_for=[],
        doc_short="Generate hypotheses (Conservative, Exploratory, Adversarial).",
        doc_long="https://docs.arifos.org/tools/agi_think",
        availability="ready",
        install_hint=None,
    ),
    "agi_reason": ToolSpec(
        name="agi_reason",
        canonical_path="aaa.agi_reason",
        stage="333",
        trinity="Δ",
        verb="reason",
        required_floors=["F2", "F4", "F7"],
        next_tool="aaa.asi_empathize",
        category="reasoning",
        risk_scope="medium",
        hard_floors=["F2"],
        requires_human_for=[],
        doc_short="Deep logical reasoning with truth_score and confidence.",
        doc_long="https://docs.arifos.org/tools/agi_reason",
        availability="ready",
        install_hint=None,
    ),
    # 444-666 — ASI Heart (Ω)
    "asi_empathize": ToolSpec(
        name="asi_empathize",
        canonical_path="aaa.asi_empathize",
        stage="555",  # Note: 444 is internal trinity sync
        trinity="Ω",
        verb="validate",
        required_floors=["F5", "F6"],
        next_tool="aaa.asi_align",
        category="safety",
        risk_scope="high",
        hard_floors=["F6"],
        requires_human_for=["stakeholder_harm_detected"],
        doc_short="Assess stakeholder impact. HARD FLOOR F6 (κᵣ ≥ 0.95). VOID if fails.",
        doc_long="https://docs.arifos.org/tools/asi_empathize",
        availability="ready",
        install_hint=None,
    ),
    "asi_align": ToolSpec(
        name="asi_align",
        canonical_path="aaa.asi_align",
        stage="666",
        trinity="Ω",
        verb="align",
        required_floors=["F5", "F6", "F9"],
        next_tool="aaa.apex_verdict",
        category="safety",
        risk_scope="high",
        hard_floors=[],
        requires_human_for=["ethical_conflict"],
        doc_short="Reconcile ethics, law, policy. Checks F5, F6, F9.",
        doc_long="https://docs.arifos.org/tools/asi_align",
        availability="ready",
        install_hint=None,
    ),
    # 777-999 — APEX Soul (Ψ)
    "apex_verdict": ToolSpec(
        name="apex_verdict",
        canonical_path="aaa.apex_verdict",
        stage="888",  # 777 is forge
        trinity="Ψ",
        verb="audit",
        required_floors=["F2", "F3", "F5", "F8"],
        next_tool="aaa.vault_seal",
        category="judgment",
        risk_scope="high",
        hard_floors=["F2", "F3"],
        requires_human_for=["high_stakes"],
        doc_short="Final constitutional verdict. Only APEX has verdict authority.",
        doc_long="https://docs.arifos.org/tools/apex_verdict",
        availability="ready",
        install_hint=None,
    ),
    "vault_seal": ToolSpec(
        name="vault_seal",
        canonical_path="aaa.vault_seal",
        stage="999",
        trinity="KA",  # Κα (Kappa) for Vault
        verb="seal",
        required_floors=["F1", "F3"],
        next_tool=None,
        category="audit",
        risk_scope="high",
        hard_floors=["F1", "F3"],
        requires_human_for=[],
        doc_short="Cryptographic ledger sealing. CALL THIS LAST. Immutable record.",
        doc_long="https://docs.arifos.org/tools/vault_seal",
        availability="ready",
        install_hint=None,
    ),
    # Unified pipeline
    "trinity_forge": ToolSpec(
        name="trinity_forge",
        canonical_path="aaa.trinity_forge",
        stage="ALL",
        trinity="ΔΩΨ",
        verb="forge",
        required_floors=["F11", "F12"],  # Entry only; internal stages self-enforce
        next_tool=None,
        category="entry",
        risk_scope="high",
        hard_floors=["F11", "F12"],
        requires_human_for=["high_stakes"],
        doc_short="Unified 000-999 pipeline. Single call for full constitutional processing.",
        doc_long="https://docs.arifos.org/tools/trinity_forge",
        availability="ready",
        install_hint=None,
    ),
}


# ═════════════════════════════════════════════════════════════════════════════
# LOOKUP FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def get_tool_spec(tool_name: str) -> Optional[ToolSpec]:
    """Get canonical spec for a tool by name."""
    return CANONICAL_TOOLS.get(tool_name)


def get_tool_by_stage(stage: str) -> Optional[ToolSpec]:
    """Get tool specification by pipeline stage."""
    for spec in CANONICAL_TOOLS.values():
        if spec.stage == stage:
            return spec
    return None


def get_next_tool(current_tool: str) -> Optional[str]:
    """Get canonical path of next tool in pipeline."""
    spec = CANONICAL_TOOLS.get(current_tool)
    if spec:
        return spec.next_tool
    return None


def validate_tool_path(path: str) -> bool:
    """Check if a tool path is canonical."""
    # Handle both "aaa.tool_name" and "tool_name" formats
    if path.startswith("aaa."):
        path = path[4:]
    return path in CANONICAL_TOOLS


def get_all_tool_paths() -> List[str]:
    """Get list of all canonical tool paths."""
    return [spec.canonical_path for spec in CANONICAL_TOOLS.values()]


# Mapping from actual MCP tool names (verbs) to internal registry keys
MCP_NAME_TO_REGISTRY: Dict[str, str] = {spec.verb: name for name, spec in CANONICAL_TOOLS.items()}


def get_tool_by_mcp_name(mcp_name: str) -> Optional[ToolSpec]:
    """Look up a tool spec by its actual MCP tool name (verb).

    Example: get_tool_by_mcp_name("anchor") returns the init_gate spec.
    """
    registry_key = MCP_NAME_TO_REGISTRY.get(mcp_name)
    if registry_key:
        return CANONICAL_TOOLS.get(registry_key)
    # Also check if it's a direct registry key
    return CANONICAL_TOOLS.get(mcp_name)


def get_pipeline_sequence() -> List[str]:
    """Get ordered list of canonical paths for 000-999 pipeline."""
    sequence = []
    current = "aaa.init_gate"
    while current:
        sequence.append(current)
        spec = CANONICAL_TOOLS.get(current.replace("aaa.", ""))
        current = spec.next_tool if spec else None
    return sequence


# ═════════════════════════════════════════════════════════════════════════════
# ERROR RESPONSE BUILDER (for unavailable tools)
# ═════════════════════════════════════════════════════════════════════════════


def build_tool_unavailable_error(
    requested_tool: str, session_id: str, reason: str = "Tool connector not installed"
) -> dict:
    """Build standardized error when a tool is unavailable."""
    return {
        "verdict": "VOID",
        "status": "BLOCKED",
        "blocked_by": "TOOL_UNAVAILABLE",
        "reason": reason,
        "requested_tool": requested_tool,
        "session_id": session_id,
        "remediation": {
            "action": "INSTALL_CONNECTOR",
            "message": f"The tool '{requested_tool}' requires a connector that is not installed.",
            "available_tools": get_all_tool_paths(),
            "documentation": "https://docs.arifos.org/connectors",
        },
        "_constitutional": {
            "floor_violated": "F11",  # Authority/availability
            "floors_checked": ["F11"],
            "pipeline_stage": "ERROR",
            "pipeline_complete": False,
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# HARD FLOOR FAILURE ENVELOPE (standardized block response)
# ═════════════════════════════════════════════════════════════════════════════


def build_hard_floor_block(
    floor: str,
    score: float,
    threshold: float,
    reason: str,
    session_id: str,
    remediation: Optional[dict] = None,
) -> dict:
    """
    Build standardized block envelope when a hard floor fails.

    This ensures agents always get:
    - What failed (floor)
    - By how much (score vs threshold)
    - Why (reason)
    - How to fix (remediation)
    """
    default_remediation = {
        "action": "HUMAN_REVIEW",
        "message": f"Constitutional floor {floor} not satisfied.",
        "required": f"{floor} score must be ≥ {threshold}",
        "current": score,
        "suggested_next_steps": [
            "Review stakeholder impact if F6",
            "Add external grounding if F2",
            "Reduce confidence if F7",
            "Request 888_HOLD override if critical",
        ],
    }

    return {
        "verdict": "VOID",
        "status": "BLOCKED",
        "blocked_by": floor,
        "reason": reason,
        "session_id": session_id,
        "floor_violation": {
            "floor": floor,
            "score": score,
            "threshold": threshold,
            "gap": round(threshold - score, 3),
            "unit": "normalized_score",
            "confidence_band": "hard_floor",
        },
        "remediation": remediation or default_remediation,
        "pipeline": {
            "stage": "BLOCKED",
            "next_tool": None,
            "can_resume": floor not in ["F6", "F10", "F12"],  # Some floors never resume
            "requires_888_override": floor in ["F6", "F13"],
        },
        "_constitutional": {
            "total_floors": 13,
            "floors_enforced_now": [floor],
            "floors_checked": [floor],
            "pipeline_complete": False,
            "governance_summary": f"Hard floor {floor} failed. Human review required.",
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# AGENT-FRIENDLY SCHEMA EXPORT (for tool selection)
# ═════════════════════════════════════════════════════════════════════════════


def export_tool_schema_for_agents() -> dict:
    """
    Export tool schema optimized for agent tool selection.

    Answers 5 questions in <2 seconds:
    1. What stage am I in?
    2. Which tool comes next?
    3. Is the tool callable right now?
    4. What's the minimum args needed?
    5. What happens if it fails?
    """
    schema = {}
    for name, spec in CANONICAL_TOOLS.items():
        schema[name] = {
            # Identification
            "name": spec.name,
            "canonical_path": spec.canonical_path,
            # Navigation (Q1: stage, Q2: next)
            "stage": spec.stage,
            "trinity": spec.trinity,
            "verb": spec.verb,
            "next_tool": spec.next_tool,
            "pipeline_position": (
                get_pipeline_sequence().index(spec.canonical_path) + 1
                if spec.canonical_path in get_pipeline_sequence()
                else None
            ),
            # Routing hints (Q3: callable, Q5: failure mode)
            "category": spec.category,
            "risk_scope": spec.risk_scope,
            "availability": spec.availability,
            "install_hint": spec.install_hint,
            "hard_floors": spec.hard_floors,
            "requires_human_for": spec.requires_human_for,
            # Documentation (Q4: args from doc_short)
            "doc_short": spec.doc_short,
            "doc_long": spec.doc_long,
            # Constitutional
            "required_floors": spec.required_floors,
        }
    return schema


def get_agent_selection_hints(current_stage: str) -> dict:
    """
    Get hints for agent selecting next tool.
    Returns recommended next tool with rationale.
    """
    current_spec = get_tool_by_stage(current_stage)
    if not current_spec:
        return {"error": f"Unknown stage: {current_stage}"}

    next_path = current_spec.next_tool
    if not next_path:
        return {
            "stage": current_stage,
            "pipeline_complete": True,
            "message": "Pipeline complete. No next tool.",
        }

    next_name = next_path.replace("aaa.", "")
    next_spec = get_tool_spec(next_name)

    return {
        "current_stage": current_stage,
        "current_tool": current_spec.canonical_path,
        "next_tool": next_path,
        "next_name": next_name,
        "next_category": next_spec.category if next_spec else None,
        "next_risk_scope": next_spec.risk_scope if next_spec else None,
        "next_hard_floors": next_spec.hard_floors if next_spec else [],
        "next_doc_short": next_spec.doc_short if next_spec else None,
        "pipeline_complete": False,
        "rationale": f"{current_stage} → {next_spec.stage if next_spec else 'END'}: {next_spec.doc_short if next_spec else 'Complete'}",
    }


# ═════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═════════════════════════════════════════════════════════════════════════════

__all__ = [
    "ToolSpec",
    "CANONICAL_TOOLS",
    "MCP_NAME_TO_REGISTRY",
    "get_tool_spec",
    "get_tool_by_mcp_name",
    "get_tool_by_stage",
    "get_next_tool",
    "validate_tool_path",
    "get_all_tool_paths",
    "get_pipeline_sequence",
    "build_tool_unavailable_error",
    "build_hard_floor_block",
    "export_tool_schema_for_agents",
    "get_agent_selection_hints",
]
