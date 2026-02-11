"""
Canonical Tool Path Registry — v60.0-FORGE

Ensures deterministic, callable tool paths for all AAA MCP tools.
Prevents "connector not installed" confusion by providing stable identifiers.
"""

from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ToolSpec:
    """Canonical specification for an AAA MCP tool."""
    name: str                    # Tool name (e.g., "init_gate")
    canonical_path: str          # Stable identifier (e.g., "aaa.init_gate")
    stage: str                   # Pipeline stage (000-999)
    trinity: str                 # Δ, Ω, Ψ, or ALL
    verb: str                    # Human action (anchor, reason, validate, etc.)
    required_floors: List[str]   # Constitutional floors
    next_tool: Optional[str]     # Next tool in pipeline (None if terminal)
    description: str


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
        description="Initialize constitutional session"
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
        description="Parse intent and classify lane"
    ),
    
    "agi_think": ToolSpec(
        name="agi_think",
        canonical_path="aaa.agi_think",
        stage="222",
        trinity="Δ",
        verb="think",
        required_floors=["F2", "F4", "F7"],
        next_tool="aaa.agi_reason",
        description="Generate hypotheses"
    ),
    
    "agi_reason": ToolSpec(
        name="agi_reason",
        canonical_path="aaa.agi_reason",
        stage="333",
        trinity="Δ",
        verb="reason",
        required_floors=["F2", "F4", "F7"],
        next_tool="aaa.asi_empathize",
        description="Deep logical reasoning"
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
        description="Assess stakeholder impact"
    ),
    
    "asi_align": ToolSpec(
        name="asi_align",
        canonical_path="aaa.asi_align",
        stage="666",
        trinity="Ω",
        verb="align",
        required_floors=["F5", "F6", "F9"],
        next_tool="aaa.apex_verdict",
        description="Reconcile ethics, law, policy"
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
        description="Final constitutional verdict"
    ),
    
    "vault_seal": ToolSpec(
        name="vault_seal",
        canonical_path="aaa.vault_seal",
        stage="999",
        trinity="KA",  # Κα (Kappa) for Vault
        verb="seal",
        required_floors=["F1", "F3"],
        next_tool=None,
        description="Cryptographic ledger sealing"
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
        description="Unified 000-999 pipeline"
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
    requested_tool: str,
    session_id: str,
    reason: str = "Tool connector not installed"
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
            "documentation": "https://docs.arifos.org/connectors"
        },
        "_constitutional": {
            "floor_violated": "F11",  # Authority/availability
            "floors_checked": ["F11"],
            "pipeline_stage": "ERROR",
            "pipeline_complete": False
        }
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
    remediation: Optional[dict] = None
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
            "Request 888_HOLD override if critical"
        ]
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
            "confidence_band": "hard_floor"
        },
        "remediation": remediation or default_remediation,
        "pipeline": {
            "stage": "BLOCKED",
            "next_tool": None,
            "can_resume": floor not in ["F6", "F10", "F12"],  # Some floors never resume
            "requires_888_override": floor in ["F6", "F13"]
        },
        "_constitutional": {
            "total_floors": 13,
            "floors_enforced_now": [floor],
            "floors_checked": [floor],
            "pipeline_complete": False,
            "governance_summary": f"Hard floor {floor} failed. Human review required."
        }
    }


# ═════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═════════════════════════════════════════════════════════════════════════════

__all__ = [
    "ToolSpec",
    "CANONICAL_TOOLS",
    "get_tool_spec",
    "get_tool_by_stage",
    "get_next_tool",
    "validate_tool_path",
    "get_all_tool_paths",
    "get_pipeline_sequence",
    "build_tool_unavailable_error",
    "build_hard_floor_block",
]
