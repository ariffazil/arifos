"""
Tool Relationship Graph for AAA MCP

Machine-readable dependency graph for constitutional tool orchestration.
Enables AI agents to discover valid tool sequences automatically.

Version: 1.0.0-SEAL
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class ToolPosition(str, Enum):
    """Pipeline position classification."""

    ENTRY = "entry"  # Must be first
    GROUNDING = "grounding"  # Evidence collection
    ANALYSIS = "analysis"  # Reasoning/empathy
    SYNC = "sync"  # Trinity merge
    JUDGMENT = "judgment"  # Verdict rendering
    TERMINAL = "terminal"  # Must be last
    AUXILIARY = "auxiliary"  # Can be called anytime


class EvidenceRequirement(str, Enum):
    """Evidence requirements for tool execution."""

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"
    NONE = "none"


@dataclass
class ToolNode:
    """Complete specification for a constitutional tool."""

    name: str
    description: str
    position: ToolPosition
    floors_enforced: List[str]

    # Dependency relationships
    requires: List[str] = field(default_factory=list)
    produces: List[str] = field(default_factory=list)
    must_precede: List[str] = field(default_factory=list)
    may_precede: List[str] = field(default_factory=list)
    feeds_into: List[str] = field(default_factory=list)

    # Execution properties
    parallel_safe: bool = False
    idempotent: bool = False
    terminal: bool = False
    must_call_first: bool = False
    must_call_last: bool = False

    # Evidence requirements
    evidence_requirement: EvidenceRequirement = EvidenceRequirement.NONE

    # Lane affinity (which query types this tool serves best)
    lane_affinity: List[str] = field(default_factory=list)

    # Success/failure semantics
    success_indicator: str = ""
    failure_action: str = ""


# ═════════════════════════════════════════════════════════════════════════════
# CONSTITUTIONAL TOOL GRAPH
# ═════════════════════════════════════════════════════════════════════════════

TOOL_GRAPH: Dict[str, ToolNode] = {
    # ─── ENTRY POINT ─────────────────────────────────────────────────────────
    "init_gate": ToolNode(
        name="init_gate",
        description="Initialize constitutional session with F11/F12 enforcement",
        position=ToolPosition.ENTRY,
        floors_enforced=["F11", "F12"],
        produces=["session_id", "mode", "grounding_required", "lane"],
        must_precede=[
            "agi_sense",
            "agi_think",
            "agi_reason",
            "asi_empathize",
            "asi_align",
            "apex_verdict",
            "reality_search",
            "truth_audit",
        ],
        may_precede=["tool_router"],
        must_call_first=True,
        parallel_safe=False,
        idempotent=False,
        success_indicator="status == 'READY' and verdict == 'SEAL'",
        failure_action="Halt — cannot proceed without valid session (VOID)",
    ),
    # ─── UNIFIED PIPELINE ────────────────────────────────────────────────────
    "trinity_forge": ToolNode(
        name="trinity_forge",
        description="Unified 000→999 pipeline — single entrypoint for full execution",
        position=ToolPosition.ENTRY,
        floors_enforced=["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F11", "F12", "F13"],
        produces=["verdict", "session_id", "agi", "asi", "apex", "seal"],
        terminal=True,
        parallel_safe=False,
        idempotent=False,
        must_call_first=True,
        lane_affinity=["FACTUAL", "CARE", "SOCIAL", "CRISIS"],
        success_indicator="verdict == 'SEAL'",
        failure_action="Follow verdict semantics: VOID=reject, SABAR=revise, PARTIAL=constrain",
    ),
    # ─── AGI MIND (Δ) ────────────────────────────────────────────────────────
    "agi_sense": ToolNode(
        name="agi_sense",
        description="Parse intent and classify lane (Stage 111)",
        position=ToolPosition.ANALYSIS,
        floors_enforced=["F2", "F4"],
        requires=["init_gate"],
        produces=["intent", "lane", "requires_grounding", "truth_score"],
        may_precede=["agi_think", "agi_reason", "reality_search"],
        feeds_into=["agi_reason", "apex_verdict"],
        parallel_safe=True,
        idempotent=True,
        lane_affinity=["FACTUAL", "CARE", "SOCIAL", "CRISIS"],
        success_indicator="lane in ['FACTUAL', 'CARE', 'SOCIAL', 'CRISIS']",
        failure_action="Use FACTUAL as default lane",
    ),
    "agi_think": ToolNode(
        name="agi_think",
        description="Generate hypotheses and explore reasoning paths (Stage 222)",
        position=ToolPosition.ANALYSIS,
        floors_enforced=["F2", "F4", "F7"],
        requires=["init_gate"],
        produces=["hypotheses", "confidence_range", "recommended_path"],
        may_precede=["agi_reason"],
        feeds_into=["agi_reason"],
        parallel_safe=False,
        idempotent=False,
        lane_affinity=["FACTUAL", "CRISIS"],
        success_indicator="len(hypotheses) > 0",
        failure_action="Proceed with single default hypothesis",
    ),
    "agi_reason": ToolNode(
        name="agi_reason",
        description="Deep logical reasoning — core analysis tool (Stage 333)",
        position=ToolPosition.ANALYSIS,
        floors_enforced=["F2", "F4", "F7"],
        requires=["init_gate"],
        produces=[
            "truth_score",
            "confidence",
            "entropy_delta",
            "humility_omega",
            "genius_score",
            "conclusion",
        ],
        may_precede=["apex_verdict"],  # Can be called directly or after sensing/thinking
        feeds_into=["apex_verdict"],
        parallel_safe=False,
        idempotent=False,
        evidence_requirement=EvidenceRequirement.RECOMMENDED,
        lane_affinity=["FACTUAL", "CRISIS"],
        success_indicator="truth_score >= 0.99 and verdict == 'SEAL'",
        failure_action="May trigger SABAR in apex_verdict if F2 not met",
    ),
    # ─── ASI HEART (Ω) ───────────────────────────────────────────────────────
    "asi_empathize": ToolNode(
        name="asi_empathize",
        description="Assess stakeholder impact — empathy engine (Stage 555)",
        position=ToolPosition.ANALYSIS,
        floors_enforced=["F5", "F6"],
        requires=["init_gate"],
        produces=["empathy_kappa_r", "stakeholders", "high_vulnerability"],
        must_precede=["apex_verdict"],
        feeds_into=["apex_verdict"],
        parallel_safe=True,  # Can run parallel with agi_reason
        idempotent=True,
        lane_affinity=["CARE", "SOCIAL", "CRISIS"],
        success_indicator="empathy_kappa_r >= 0.95",
        failure_action="VOID if F6 HARD floor violated (stakeholder harm detected)",
    ),
    "asi_align": ToolNode(
        name="asi_align",
        description="Reconcile ethics, law, and policy (Stage 666)",
        position=ToolPosition.ANALYSIS,
        floors_enforced=["F5", "F6", "F9"],
        requires=["init_gate"],
        produces=["is_reversible", "ethics_check", "policy_check"],
        must_precede=["apex_verdict"],
        feeds_into=["apex_verdict"],
        parallel_safe=True,
        idempotent=True,
        lane_affinity=["CARE", "CRISIS"],
        success_indicator="is_reversible == True",
        failure_action="PARTIAL verdict with reversibility warning",
    ),
    # ─── APEX SOUL (Ψ) ───────────────────────────────────────────────────────
    "apex_verdict": ToolNode(
        name="apex_verdict",
        description="Final constitutional judgment with Tri-Witness (Stage 888)",
        position=ToolPosition.JUDGMENT,
        floors_enforced=["F2", "F3", "F5", "F8"],
        requires=["init_gate"],
        produces=["verdict", "truth_score", "tri_witness", "votes", "justification"],
        must_precede=["vault_seal"],
        feeds_into=["vault_seal"],
        parallel_safe=False,
        idempotent=False,
        lane_affinity=["FACTUAL", "CARE", "SOCIAL", "CRISIS"],
        success_indicator="verdict == 'SEAL' and tri_witness >= 0.95",
        failure_action="Execute verdict semantics: VOID=reject, SABAR=revise, PARTIAL=constrain, 888_HOLD=escalate",
    ),
    # ─── VAULT MEMORY ────────────────────────────────────────────────────────
    "vault_seal": ToolNode(
        name="vault_seal",
        description="Seal session into immutable ledger (Stage 999)",
        position=ToolPosition.TERMINAL,
        floors_enforced=["F1", "F3"],
        requires=["init_gate"],
        produces=["seal_id", "seal_hash", "timestamp"],
        terminal=True,
        must_call_last=True,
        parallel_safe=False,
        idempotent=True,  # Safe to retry
        success_indicator="verdict == 'SEALED' and seal_id is not None",
        failure_action="Retry or log to fallback storage",
    ),
    # ─── GROUNDING ───────────────────────────────────────────────────────────
    "reality_search": ToolNode(
        name="reality_search",
        description="External fact-checking via web search + Axiom Engine",
        position=ToolPosition.GROUNDING,
        floors_enforced=["F2", "F7"],
        requires=["init_gate"],
        produces=["evidence[]", "sources", "confidence"],
        feeds_into=["agi_reason", "truth_audit"],
        parallel_safe=True,
        idempotent=True,
        lane_affinity=["FACTUAL", "CRISIS"],
        success_indicator="len(evidence) > 0",
        failure_action="If HARD lane: may trigger VOID in apex_verdict for F2 failure",
    ),
    # ─── AUXILIARY TOOLS ─────────────────────────────────────────────────────
    "tool_router": ToolNode(
        name="tool_router",
        description="Smart triage nurse — recommends pipeline sequence",
        position=ToolPosition.AUXILIARY,
        floors_enforced=[],
        produces=["recommended_pipeline", "lane", "grounding_required"],
        parallel_safe=True,
        idempotent=True,
        lane_affinity=["FACTUAL", "CARE", "SOCIAL", "CRISIS"],
        success_indicator="len(recommended_pipeline) > 0",
        failure_action="Default to ['trinity_forge']",
    ),
    "vault_query": ToolNode(
        name="vault_query",
        description="Query sealed records for institutional memory",
        position=ToolPosition.AUXILIARY,
        floors_enforced=["F1", "F3"],
        produces=["entries[]", "patterns", "count"],
        must_call_first=True,
        parallel_safe=True,
        idempotent=True,
        success_indicator="entries is not None",
        failure_action="Return empty results with error message",
    ),
    "truth_audit": ToolNode(
        name="truth_audit",
        description="[EXPERIMENTAL] Full claim verification pipeline",
        position=ToolPosition.AUXILIARY,
        floors_enforced=["F2", "F4", "F7", "F10"],
        requires=["init_gate"],
        produces=["overall_verdict", "overall_truth", "claims[]"],
        must_precede=["vault_seal"],
        parallel_safe=False,
        idempotent=True,
        evidence_requirement=EvidenceRequirement.REQUIRED,
        success_indicator="overall_verdict == 'SEAL'",
        failure_action="Report claims with p_truth < 0.8 for review",
    ),
    "simulate_transfer": ToolNode(
        name="simulate_transfer",
        description="Financial transfer simulation for testing",
        position=ToolPosition.AUXILIARY,
        floors_enforced=["F2", "F11", "F12"],
        produces=["status", "verdict", "metrics"],
        terminal=False,
        parallel_safe=True,
        idempotent=True,
        lane_affinity=["CRISIS"],
        success_indicator="verdict in ['SEAL', 'VOID', 'PARTIAL']",
        failure_action="Report simulation failure",
    ),
}


# ═════════════════════════════════════════════════════════════════════════════
# WORKFLOW SEQUENCES
# ═════════════════════════════════════════════════════════════════════════════

# Mapping from actual MCP tool names to internal graph node names
MCP_TO_GRAPH: Dict[str, str] = {
    "anchor": "init_gate",
    "reason": "agi_think",  # reason tool combines sense+think
    "integrate": "agi_reason",
    "respond": "agi_reason",  # respond is stage 444 (trinity sync)
    "validate": "asi_empathize",
    "align": "asi_align",
    "forge": "apex_verdict",  # forge is stage 777
    "audit": "apex_verdict",
    "seal": "vault_seal",
    "trinity_forge": "trinity_forge",
}


WORKFLOW_SEQUENCES: Dict[str, List[str]] = {
    "fact_check": ["init_gate", "reality_search", "agi_reason", "apex_verdict", "vault_seal"],
    "safety_assessment": ["init_gate", "asi_empathize", "asi_align", "apex_verdict", "vault_seal"],
    "full_analysis": [
        "init_gate",
        "agi_sense",
        "reality_search",
        "agi_think",
        "agi_reason",
        "asi_empathize",
        "asi_align",
        "apex_verdict",
        "vault_seal",
    ],
    "quick_decision": ["trinity_forge"],
    "claim_verification": ["init_gate", "truth_audit", "vault_seal"],
    "institutional_memory": ["vault_query"],
}

WORKFLOW_DESCRIPTIONS: Dict[str, str] = {
    "fact_check": "Verify factual claims with external grounding",
    "safety_assessment": "Assess stakeholder impact and ethics alignment",
    "full_analysis": "Complete constitutional pipeline with all stages",
    "quick_decision": "Fast path using unified forge pipeline",
    "claim_verification": "Audit AI-generated text against reality [EXPERIMENTAL]",
    "institutional_memory": "Query past constitutional decisions",
}


# ═════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def get_tool_node(tool_name: str) -> Optional[ToolNode]:
    """Get tool node by name."""
    return TOOL_GRAPH.get(tool_name)


def get_valid_next_tools(current_tool: str) -> List[str]:
    """Get list of tools that can legally follow the current tool."""
    node = TOOL_GRAPH.get(current_tool)
    if not node:
        return []

    # Must precede + may precede + feeds into
    valid = set(node.must_precede + node.may_precede + node.feeds_into)
    return list(valid)


def get_required_predecessors(tool_name: str) -> List[str]:
    """Get tools that MUST be called before this tool.

    Note: This only returns strict requirements. In practice, many
    constitutional tools can be called with minimal prerequisites
    (e.g., only requiring session_id from init_gate).
    """
    node = TOOL_GRAPH.get(tool_name)
    if not node:
        return []

    # Most tools only strictly require init_gate for session context
    # The validation should be more about valid sequences than strict prerequisites
    return node.requires if node.requires else []


def validate_sequence(sequence: List[str]) -> tuple[bool, str]:
    """Validate a tool sequence follows constitutional order.

    Returns:
        (is_valid, error_message)
    """
    if not sequence:
        return False, "Empty sequence"

    # Check first tool
    first = TOOL_GRAPH.get(sequence[0])
    if not first:
        return False, f"Unknown tool: {sequence[0]}"

    if not (first.must_call_first or first.position == ToolPosition.ENTRY):
        return False, f"First tool {sequence[0]} is not an entry point"

    # Check for multiple entry points
    entry_count = sum(
        1 for tool in sequence if TOOL_GRAPH.get(tool) and TOOL_GRAPH[tool].must_call_first
    )
    if entry_count > 1:
        return False, "Multiple entry points in sequence"

    # Check dependencies
    seen = set()
    for i, tool_name in enumerate(sequence):
        node = TOOL_GRAPH.get(tool_name)
        if not node:
            return False, f"Unknown tool: {tool_name}"

        # Check if all required predecessors have been called
        required = get_required_predecessors(tool_name)
        missing = [r for r in required if r not in seen]
        if missing and i > 0:  # First tool has no predecessors
            return False, f"{tool_name} requires: {missing}"

        # Check terminal constraint
        if node.terminal and i < len(sequence) - 1:
            return False, f"{tool_name} is terminal but not last"

        seen.add(tool_name)

    # Check last tool - terminal OR auxiliary tools can end sequences
    last = TOOL_GRAPH.get(sequence[-1])
    if last and not (
        last.terminal or last.must_call_last or last.position == ToolPosition.AUXILIARY
    ):
        return False, "Sequence does not end with terminal tool (recommend: vault_seal)"

    return True, "Valid constitutional sequence"


def get_workflow_sequence(workflow_name: str) -> Optional[List[str]]:
    """Get predefined workflow sequence by name."""
    return WORKFLOW_SEQUENCES.get(workflow_name)


def list_available_workflows() -> Dict[str, str]:
    """List all available workflows with descriptions."""
    return WORKFLOW_DESCRIPTIONS.copy()


def get_parallel_groups(sequence: List[str]) -> List[List[str]]:
    """Group tools that can be executed in parallel.

    Returns list of groups where tools in same group are parallel_safe.
    """
    groups = []
    current_group = []

    for tool_name in sequence:
        node = TOOL_GRAPH.get(tool_name)
        if not node:
            continue

        if node.parallel_safe and current_group:
            # Can add to current parallel group
            current_group.append(tool_name)
        else:
            # Must be sequential
            if current_group:
                groups.append(current_group)
            current_group = [tool_name]

    if current_group:
        groups.append(current_group)

    return groups


def suggest_sequence(intent: str, lane: str = "FACTUAL") -> List[str]:
    """Suggest optimal tool sequence based on intent and lane."""
    intent_lower = intent.lower()

    # Intent matching
    if any(k in intent_lower for k in ["fact", "check", "verify", "true", "false"]):
        return WORKFLOW_SEQUENCES["fact_check"]

    if any(k in intent_lower for k in ["safe", "harm", "risk", "impact", "stakeholder"]):
        return WORKFLOW_SEQUENCES["safety_assessment"]

    if any(k in intent_lower for k in ["audit", "claims", "ai generated", "text"]):
        return WORKFLOW_SEQUENCES["claim_verification"]

    if any(k in intent_lower for k in ["past", "history", "previous", "query"]):
        return WORKFLOW_SEQUENCES["institutional_memory"]

    if any(k in intent_lower for k in ["quick", "fast", "simple"]):
        return WORKFLOW_SEQUENCES["quick_decision"]

    # Lane-based default
    if lane == "FACTUAL":
        return WORKFLOW_SEQUENCES["fact_check"]
    elif lane in ["CARE", "SOCIAL"]:
        return WORKFLOW_SEQUENCES["safety_assessment"]
    else:
        return WORKFLOW_SEQUENCES["full_analysis"]
