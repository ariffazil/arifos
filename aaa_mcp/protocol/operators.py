"""
Principle Operators — Executable Governance Rules

Converts 9 Principles into deterministic operators:
- Each operator has: precondition, invariant, action
- Machine-executable, zero ambiguity
- Maps human mottos to AI operations

Version: 1.0.0-LOW_ENTROPY
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class OperatorType(Enum):
    """Classification of operator behavior."""

    GUARD = "guard"  # Blocks if condition fails
    TRANSFORM = "transform"  # Modifies data
    VERIFY = "verify"  # Checks without blocking


@dataclass(frozen=True)
class PrincipleOperator:
    """
    Executable operator derived from a Principle.

    Machine-readable format with zero ambiguity:
    - id: Short identifier (e.g., "EARNED", "EXAMINE")
    - principle: Human motto (e.g., "Earned, Not Given")
    - type: Operator classification
    - precondition: What must be true before execution
    - invariant: What must remain true during execution
    - action: What the operator does
    - output_schema: Expected return structure
    """

    id: str
    principle: str
    stage: str
    operator_type: OperatorType
    precondition: Dict[str, Any]
    invariant: Dict[str, Any]
    action: str
    output_schema: Dict[str, str]

    def to_prompt(self) -> str:
        """Convert to low-entropy system prompt format."""
        return f"""
OPERATOR: {self.id}
PRINCIPLE: {self.principle}
TYPE: {self.operator_type.value}
PRECONDITION: {self.precondition}
INVARIANT: {self.invariant}
ACTION: {self.action}
OUTPUT: {self.output_schema}
"""


# ═════════════════════════════════════════════════════════════════════════════
# 9 PRINCIPLES → OPERATORS
# ═════════════════════════════════════════════════════════════════════════════

OPERATOR_REGISTRY: Dict[str, PrincipleOperator] = {
    # 000: Earned, Not Given
    "EARNED": PrincipleOperator(
        id="EARNED",
        principle="Earned, Not Given",
        stage="000",
        operator_type=OperatorType.GUARD,
        precondition={"auth_token": "valid OR session_initialized"},
        invariant={"access": "privileged_operations_require_justification"},
        action="VERIFY_AUTHORITY: Confirm caller has right to invoke this operation",
        output_schema={"authorized": "bool", "session_id": "string"},
    ),
    # 111: Examined, Not Spoon-fed
    "EXAMINE": PrincipleOperator(
        id="EXAMINE",
        principle="Examined, Not Spoon-fed",
        stage="111",
        operator_type=OperatorType.TRANSFORM,
        precondition={"raw_query": "string_present"},
        invariant={"intent_clarity": "must_increase"},
        action="CLASSIFY_INTENT: Parse query into structured intent with lane classification",
        output_schema={
            "intent": "string",
            "lane": "enum[SOCIAL,CARE,FACTUAL,CRISIS]",
            "requires_grounding": "bool",
            "confidence": "float[0,1]",
        },
    ),
    # 222: Explored, Not Restricted
    "EXPLORE": PrincipleOperator(
        id="EXPLORE",
        principle="Explored, Not Restricted",
        stage="222",
        operator_type=OperatorType.TRANSFORM,
        precondition={"intent": "classified", "lane": "assigned"},
        invariant={"hypothesis_count": ">=3"},
        action="GENERATE_HYPOTHESES: Create conservative, exploratory, and adversarial reasoning paths",
        output_schema={
            "hypotheses": "array[Hypothesis]",
            "confidence_range": "tuple[float,float]",
            "recommended_path": "string",
        },
    ),
    # 333: Clarified, Not Obscured
    "CLARIFY": PrincipleOperator(
        id="CLARIFY",
        principle="Clarified, Not Obscured",
        stage="333",
        operator_type=OperatorType.TRANSFORM,
        precondition={"hypotheses": "generated", "reasoning_chain": "ready"},
        invariant={"entropy_delta": "<=0", "ambiguity": "must_decrease"},
        action="SEQUENTIAL_REASONING: Build reasoning chain that reduces uncertainty",
        output_schema={
            "conclusion": "string",
            "truth_score": "float[0,1]",
            "entropy_delta": "float",
            "confidence": "float[0,1]",
            "reasoning_chain": "array[ThoughtNode]",
        },
    ),
    # 444: Faced, Not Postponed
    "FACE": PrincipleOperator(
        id="FACE",
        principle="Faced, Not Postponed",
        stage="444",
        operator_type=OperatorType.GUARD,
        precondition={"agi_output": "ready", "asi_output": "ready"},
        invariant={"synchronization": "complete", "conflicts": "must_resolve"},
        action="SYNC_BUNDLES: Merge AGI (Mind) and ASI (Heart) outputs, detect conflicts",
        output_schema={
            "consensus_score": "float[0,1]",
            "conflicts": "array[Conflict]",
            "pre_verdict": "enum[SEAL,PARTIAL,VOID]",
        },
    ),
    # 555: Calmed, Not Inflamed
    "CALM": PrincipleOperator(
        id="CALM",
        principle="Calmed, Not Inflamed",
        stage="555",
        operator_type=OperatorType.VERIFY,
        precondition={"query": "string", "context": "available"},
        invariant={"peace_squared": ">=1.0", "stability": "maintained"},
        action="EMPATHY_ANALYSIS: Identify stakeholders, assess emotional/social impact",
        output_schema={
            "empathy_kappa_r": "float[0,1]",
            "stakeholders": "array[Stakeholder]",
            "weakest_stakeholder": "string",
            "care_recommendations": "array[string]",
        },
    ),
    # 666: Protected, Not Neglected
    "PROTECT": PrincipleOperator(
        id="PROTECT",
        principle="Protected, Not Neglected",
        stage="666",
        operator_type=OperatorType.GUARD,
        precondition={"empathy_analysis": "complete", "risk_assessment": "ready"},
        invariant={"reversibility": "True", "weakest_impact": "<=0.1", "safety": "guaranteed"},
        action="SAFETY_ALIGNMENT: Verify ethics, policy compliance, reversibility of action",
        output_schema={
            "is_reversible": "bool",
            "safety_score": "float[0,1]",
            "risk_level": "enum[low,medium,high,critical]",
            "violations": "array[Violation]",
        },
    ),
    # 777: Worked For, Not Merely Hoped
    "WORK": PrincipleOperator(
        id="WORK",
        principle="Worked For, Not Merely Hoped",
        stage="777",
        operator_type=OperatorType.TRANSFORM,
        precondition={"sync_complete": "True", "safety_verified": "True"},
        invariant={"coherence": ">=0.7", "effort": "must_be_demonstrable"},
        action="FORGE_OUTPUT: Synthesize final output through phase transition (Eureka)",
        output_schema={
            "output": "string",
            "coherence": "float[0,1]",
            "genius_score": "float[0,1]",
            "resource_cost": "float",
        },
    ),
    # 888: Aware, Not Overconfident
    "AWARE": PrincipleOperator(
        id="AWARE",
        principle="Aware, Not Overconfident",
        stage="888",
        operator_type=OperatorType.GUARD,
        precondition={"forged_output": "ready", "all_floors": "checked"},
        invariant={
            "uncertainty_declared": "True",
            "omega_0": "in_range[0.03,0.05]",
            "humility": "present",
        },
        action="FINAL_VERDICT: Render judgment with explicit uncertainty bounds",
        output_schema={
            "verdict": "enum[SEAL,PARTIAL,VOID,888_HOLD]",
            "truth_score": "float[0,1]",
            "omega_0": "float",
            "justification": "string",
            "uncertainty_bounds": "tuple[float,float]",
        },
    ),
    # 999: Earned, Not Given (Seal)
    "SEAL": PrincipleOperator(
        id="SEAL",
        principle="Earned, Not Given",
        stage="999",
        operator_type=OperatorType.TRANSFORM,
        precondition={"verdict": "rendered", "audit_trail": "complete"},
        invariant={"immutability": "True", "traceability": "100%"},
        action="COMMIT_TO_LEDGER: Create tamper-evident audit record",
        output_schema={
            "seal_id": "string",
            "seal_hash": "string",
            "status": "enum[SEALED,PARTIAL]",
            "audit_trail": "AuditRecord",
        },
    ),
}


# ═════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def get_operator(stage_id: str) -> Optional[PrincipleOperator]:
    """Get operator by stage ID (e.g., '333' → CLARIFY)."""
    stage_to_op = {
        "000": "EARNED",
        "111": "EXAMINE",
        "222": "EXPLORE",
        "333": "CLARIFY",
        "444": "FACE",
        "555": "CALM",
        "666": "PROTECT",
        "777": "WORK",
        "888": "AWARE",
        "999": "SEAL",
    }
    op_id = stage_to_op.get(stage_id)
    return OPERATOR_REGISTRY.get(op_id) if op_id else None


def get_operator_by_principle(principle: str) -> Optional[PrincipleOperator]:
    """Get operator by human principle text (fuzzy match)."""
    principle_lower = principle.lower()
    for op in OPERATOR_REGISTRY.values():
        if principle_lower in op.principle.lower():
            return op
    return None


def build_system_prompt(stage_ids: List[str]) -> str:
    """
    Build low-entropy system prompt for given pipeline stages.

    Example:
        build_system_prompt(["111", "222", "333"])
        → Returns executable prompt for sense→think→reason
    """
    prompts = []
    for stage_id in stage_ids:
        op = get_operator(stage_id)
        if op:
            prompts.append(op.to_prompt())

    header = """
╔═══════════════════════════════════════════════════════════════╗
║  AAA MCP PROTOCOL v1.0 — LOW ENTROPY MODE                     ║
║  Execute these operators in sequence. Stop on GUARD failure.  ║
╚═══════════════════════════════════════════════════════════════╝
"""
    return header + "\n".join(prompts)
