"""
Tool Capability Registry for AAA MCP

Machine-readable capability descriptions for AI agent discovery.
Provides semantic descriptions of when/how to use each tool.

Version: 1.0.0-SEAL
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolCategory(str, Enum):
    """Tool classification by function."""

    ENTRY = "entry"  # Session initialization
    REASONING = "reasoning"  # AGI Mind tools
    EMPATHY = "empathy"  # ASI Heart tools
    JUDGMENT = "judgment"  # APEX Soul tools
    MEMORY = "memory"  # VAULT tools
    GROUNDING = "grounding"  # Evidence collection
    AUXILIARY = "auxiliary"  # Support tools


class RiskLevel(str, Enum):
    """Risk classification for tool usage."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ToolCapability:
    """Complete capability specification for a tool."""

    # Identity
    name: str
    description: str
    category: ToolCategory

    # Constitutional
    floors_enforced: list[str]
    stage: str | None = None

    # Input/Output
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    required_params: list[str] = field(default_factory=list)
    optional_params: list[str] = field(default_factory=list)

    # Usage guidance
    when_to_use: str = ""
    when_not_to_use: str = ""
    prerequisites: list[str] = field(default_factory=list)
    next_recommended: list[str] = field(default_factory=list)

    # Success/failure
    success_indicator: str = ""
    failure_action: str = ""

    # Performance
    estimated_latency: str = "medium"  # low/medium/high
    parallelizable: bool = False
    idempotent: bool = False

    # Risk
    risk_level: RiskLevel = RiskLevel.LOW
    produces_side_effects: bool = False

    # Examples
    example_usage: str = ""
    example_output: dict[str, Any] = field(default_factory=dict)


# ═════════════════════════════════════════════════════════════════════════════
# TOOL CAPABILITY REGISTRY
# ═════════════════════════════════════════════════════════════════════════════

TOOL_CAPABILITIES: dict[str, ToolCapability] = {
    "init_gate": ToolCapability(
        name="init_gate",
        description="Initialize constitutional session with F11/F12 enforcement",
        category=ToolCategory.ENTRY,
        floors_enforced=["F11", "F12"],
        stage="000",
        required_params=["query"],
        optional_params=[
            "session_id",
            "grounding_required",
            "mode",
            "debug",
            "intent_hint",
            "urgency",
            "user_context",
        ],
        when_to_use="""
ALWAYS call this FIRST for any new constitutional query.
Creates session context required by all subsequent tools.
        """.strip(),
        when_not_to_use="""
Never skip init_gate. All constitutional tools require a valid session_id.
Only skip if re-using an existing session from a prior init_gate call.
        """.strip(),
        prerequisites=[],
        next_recommended=["agi_sense", "reality_search", "tool_router"],
        success_indicator="status == 'READY' and verdict == 'SEAL'",
        failure_action="Halt immediately — cannot proceed without valid session (VOID)",
        estimated_latency="low",
        parallelizable=False,
        idempotent=False,
        risk_level=RiskLevel.LOW,
        produces_side_effects=True,  # Creates session state
        example_usage="""
result = await init_gate(
    query="Is CCS safe for long-term storage?",
    mode="strict",
    grounding_required=True
)
session_id = result["session_id"]
        """.strip(),
        example_output={
            "session_id": "sess_abc123",
            "verdict": "SEAL",
            "status": "READY",
            "grounding_required": True,
            "mode": "strict",
            "stage": "000",
        },
    ),
    "trinity_forge": ToolCapability(
        name="trinity_forge",
        description="Unified 000→999 pipeline — single entrypoint for full constitutional execution",
        category=ToolCategory.ENTRY,
        floors_enforced=["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F11", "F12", "F13"],
        required_params=["query"],
        optional_params=[
            "actor_id",
            "auth_token",
            "require_sovereign_for_high_stakes",
            "envelope",
            "output_mode",
        ],
        when_to_use="""
Use for quick decisions when you want the full constitutional pipeline in one call.
Best for: simple queries, low-risk decisions, or when you don't need granular control.
        """.strip(),
        when_not_to_use="""
Avoid when you need to inspect intermediate stage results.
Avoid when you need to inject external evidence between stages.
Use individual stage tools instead for granular control.
        """.strip(),
        prerequisites=[],
        next_recommended=["vault_query"],  # After forge, you might want to review
        success_indicator="verdict == 'SEAL' and apex.tri_witness >= 0.95",
        failure_action="""
Follow verdict semantics:
- VOID: Reject entirely — HARD floor violated
- SABAR: Return for revision — SOFT floor needs work  
- PARTIAL: Execute with constraints — proceed cautiously
- 888_HOLD: Escalate to human — high stakes decision
        """.strip(),
        estimated_latency="high",
        parallelizable=False,
        idempotent=False,
        risk_level=RiskLevel.MEDIUM,
        produces_side_effects=True,
        example_usage="""
result = await trinity_forge(
    query="Should we approve this CCS injection protocol?",
    require_sovereign_for_high_stakes=True
)
# Returns complete constitutional analysis
        """.strip(),
        example_output={
            "verdict": "SEAL",
            "session_id": "sess_xyz789",
            "token_status": "valid",
            "agi": {"truth_score": 0.995, "confidence": 0.98},
            "asi": {"empathy_kappa_r": 0.96, "stakeholders": ["public", "operators"]},
            "apex": {"verdict": "SEAL", "tri_witness": 0.97},
            "seal": {"status": "SEALED"},
        },
    ),
    "agi_sense": ToolCapability(
        name="agi_sense",
        description="Parse intent and classify lane (Stage 111)",
        category=ToolCategory.REASONING,
        floors_enforced=["F2", "F4"],
        stage="111",
        required_params=["query", "session_id"],
        optional_params=["debug"],
        when_to_use="""
Call after init_gate to understand WHAT the user is asking.
Determines lane routing: FACTUAL (needs facts) vs CARE/SOCIAL (needs empathy).
        """.strip(),
        when_not_to_use="""
Skip if using trinity_forge (handles sensing internally).
Skip if lane is already known from context.
        """.strip(),
        prerequisites=["init_gate"],
        next_recommended=["reality_search", "agi_think", "agi_reason"],
        success_indicator="lane in ['FACTUAL', 'CARE', 'SOCIAL', 'CRISIS']",
        failure_action="Default to FACTUAL lane if classification fails",
        estimated_latency="low",
        parallelizable=True,
        idempotent=True,
        risk_level=RiskLevel.LOW,
        produces_side_effects=False,
        example_usage="""
sense_result = await agi_sense(
    query="Is this pressure reading dangerous?",
    session_id=session_id
)
lane = sense_result["lane"]  # "FACTUAL" or "CRISIS"
        """.strip(),
        example_output={
            "stage": "111",
            "intent": "safety_assessment",
            "lane": "CRISIS",
            "requires_grounding": True,
            "truth_score": 0.95,
            "evidence": [],
        },
    ),
    "agi_think": ToolCapability(
        name="agi_think",
        description="Generate hypotheses and explore reasoning paths (Stage 222)",
        category=ToolCategory.REASONING,
        floors_enforced=["F2", "F4", "F7"],
        stage="222",
        required_params=["query", "session_id"],
        optional_params=[],
        when_to_use="""
Use for complex problems with multiple possible approaches.
Best when you need to explore solution space before committing.
        """.strip(),
        when_not_to_use="""
Skip for simple factual queries with clear answers.
Skip if using trinity_forge.
        """.strip(),
        prerequisites=["init_gate"],
        next_recommended=["agi_reason"],
        success_indicator="len(hypotheses) >= 2",
        failure_action="Proceed with single default hypothesis",
        estimated_latency="medium",
        parallelizable=False,
        idempotent=False,
        risk_level=RiskLevel.LOW,
        produces_side_effects=False,
        example_usage="""
think_result = await agi_think(
    query="What are the failure modes for this CCS system?",
    session_id=session_id
)
hypotheses = think_result["hypotheses"]
        """.strip(),
        example_output={
            "stage": "222",
            "hypotheses": [
                {"id": "H1", "description": "Pressure buildup", "probability": 0.3},
                {"id": "H2", "description": "Seal degradation", "probability": 0.5},
            ],
            "confidence_range": [0.3, 0.7],
            "recommended_path": "H2",
        },
    ),
    "agi_reason": ToolCapability(
        name="agi_reason",
        description="Deep logical reasoning — core analysis tool (Stage 333)",
        category=ToolCategory.REASONING,
        floors_enforced=["F2", "F4", "F7"],
        stage="333",
        required_params=["query", "session_id"],
        optional_params=["grounding"],
        when_to_use="""
Primary analysis tool after sensing/grounding.
Use for all logical deduction and conclusion-drawing.
        """.strip(),
        when_not_to_use="""
Don't call before having session context from init_gate.
Don't call without grounding for FACTUAL lane queries.
        """.strip(),
        prerequisites=["init_gate"],
        next_recommended=["asi_empathize", "apex_verdict"],
        success_indicator="truth_score >= 0.99 and verdict == 'SEAL'",
        failure_action="May trigger SABAR in apex_verdict if F2 (Truth) not met",
        estimated_latency="medium",
        parallelizable=False,
        idempotent=False,
        risk_level=RiskLevel.MEDIUM,
        produces_side_effects=False,
        example_usage="""
reasoning = await agi_reason(
    query="Evaluate pressure containment risk",
    session_id=session_id,
    grounding=evidence_from_reality_search
)
        """.strip(),
        example_output={
            "stage": "333",
            "verdict": "SEAL",
            "truth_score": 0.995,
            "confidence": 0.98,
            "entropy_delta": -0.15,
            "humility_omega": 0.04,
            "genius_score": 0.85,
            "conclusion": "Risk is within acceptable parameters",
        },
    ),
    "asi_empathize": ToolCapability(
        name="asi_empathize",
        description="Assess stakeholder impact — empathy engine (Stage 555)",
        category=ToolCategory.EMPATHY,
        floors_enforced=["F5", "F6"],
        stage="555",
        required_params=["query", "session_id"],
        optional_params=[],
        when_to_use="""
ALWAYS call before final verdict for any query affecting humans.
Required for CARE/SOCIAL/CRISIS lanes.
Use to detect vulnerable stakeholders.
        """.strip(),
        when_not_to_use="""
May skip for pure technical queries with no human impact.
Never skip for safety-critical decisions.
        """.strip(),
        prerequisites=["init_gate"],
        next_recommended=["asi_align", "apex_verdict"],
        success_indicator="empathy_kappa_r >= 0.95 and not high_vulnerability",
        failure_action="VOID if F6 (Empathy) HARD floor violated — stakeholder harm detected",
        estimated_latency="medium",
        parallelizable=True,  # Can run parallel with agi_reason
        idempotent=True,
        risk_level=RiskLevel.HIGH,  # Critical for safety
        produces_side_effects=False,
        example_usage="""
empathy = await asi_empathize(
    query="What happens if this CCS facility leaks?",
    session_id=session_id
)
if empathy["high_vulnerability"]:
    # Escalate safety measures
    pass
        """.strip(),
        example_output={
            "stage": "555",
            "verdict": "SEAL",
            "empathy_kappa_r": 0.96,
            "stakeholders": [
                {"name": "local_community", "vulnerability": "high"},
                {"name": "operators", "vulnerability": "medium"},
            ],
            "high_vulnerability": True,
        },
    ),
    "asi_align": ToolCapability(
        name="asi_align",
        description="Reconcile ethics, law, and policy (Stage 666)",
        category=ToolCategory.EMPATHY,
        floors_enforced=["F5", "F6", "F9"],
        stage="666",
        required_params=["query", "session_id"],
        optional_params=[],
        when_to_use="""
Call after empathy to check reversibility and policy compliance.
Required for any action with real-world consequences.
        """.strip(),
        when_not_to_use="""
Skip for purely informational queries.
        """.strip(),
        prerequisites=["init_gate"],
        next_recommended=["apex_verdict"],
        success_indicator="is_reversible == True and ethics_check == 'PASS'",
        failure_action="PARTIAL verdict with reversibility warning",
        estimated_latency="medium",
        parallelizable=True,
        idempotent=True,
        risk_level=RiskLevel.MEDIUM,
        produces_side_effects=False,
        example_usage="""
alignment = await asi_align(
    query="Is this CCS protocol ethically sound?",
    session_id=session_id
)
        """.strip(),
        example_output={
            "stage": "666",
            "verdict": "SEAL",
            "is_reversible": True,
            "ethics_check": "PASS",
            "policy_check": "COMPLIANT",
        },
    ),
    "apex_verdict": ToolCapability(
        name="apex_verdict",
        description="Final constitutional judgment with Tri-Witness (Stage 888)",
        category=ToolCategory.JUDGMENT,
        floors_enforced=["F2", "F3", "F5", "F8"],
        stage="888",
        required_params=["query", "session_id"],
        optional_params=[],
        when_to_use="""
The SINGLE SOURCE OF JUSTICE — always use for final decisions.
Call after AGI (reasoning) and ASI (empathy) stages complete.
        """.strip(),
        when_not_to_use="""
Never call first — needs session context from prior stages.
Never skip — all decisions must be constitutionally judged.
        """.strip(),
        prerequisites=["init_gate", "agi_reason", "asi_empathize"],
        next_recommended=["vault_seal"],
        success_indicator="verdict == 'SEAL' and tri_witness >= 0.95",
        failure_action="""
Execute verdict semantics:
- VOID: Reject entirely
- SABAR: Return for revision  
- PARTIAL: Proceed with constraints
- 888_HOLD: Escalate to human
        """.strip(),
        estimated_latency="medium",
        parallelizable=False,
        idempotent=False,
        risk_level=RiskLevel.CRITICAL,  # Final decision point
        produces_side_effects=True,  # Renders binding verdict
        example_usage="""
verdict = await apex_verdict(
    query="Approve CCS injection protocol?",
    session_id=session_id
)
if verdict["verdict"] == "SEAL":
    # Proceed with action
    pass
        """.strip(),
        example_output={
            "stage": "888",
            "verdict": "SEAL",
            "truth_score": 0.99,
            "tri_witness": 0.97,
            "votes": {"agi": "APPROVE", "asi": "APPROVE", "apex": "APPROVE"},
            "justification": "All floors passed with consensus",
        },
    ),
    "vault_seal": ToolCapability(
        name="vault_seal",
        description="Seal session into immutable ledger (Stage 999)",
        category=ToolCategory.MEMORY,
        floors_enforced=["F1", "F3"],
        stage="999",
        required_params=["session_id", "verdict", "payload"],
        optional_params=[
            "query_summary",
            "risk_level",
            "risk_tags",
            "intent",
            "category",
            "floors_checked",
            "floors_passed",
            "floors_failed",
            "entropy_omega",
            "tri_witness_score",
            "peace_squared",
            "genius_g",
            "human_override",
            "override_reason",
            "model_used",
            "tags",
            "tool_chain",
            "model_info",
            "environment",
            "prompt_excerpt",
            "response_excerpt",
            "pii_level",
            "actor_type",
            "actor_id",
        ],
        when_to_use="""
ALWAYS call this LAST to finalize any constitutional session.
Creates immutable audit trail for accountability.
        """.strip(),
        when_not_to_use="""
Never skip — all constitutional decisions must be sealed.
Only skip in test/debug scenarios.
        """.strip(),
        prerequisites=["init_gate", "apex_verdict"],
        next_recommended=[],  # Terminal
        success_indicator="verdict == 'SEALED' and seal_id is not None",
        failure_action="Retry or log to fallback storage",
        estimated_latency="low",
        parallelizable=False,
        idempotent=True,  # Safe to retry
        risk_level=RiskLevel.LOW,
        produces_side_effects=True,  # Writes to ledger
        example_usage="""
await vault_seal(
    session_id=session_id,
    verdict=apex_result["verdict"],
    payload=full_results,
    category="safety",
    risk_level="high",
    floors_checked=["F2", "F4", "F6", "F7"]
)
        """.strip(),
        example_output={
            "verdict": "SEALED",
            "seal_id": "seal_abc123xyz",
            "seal": "a1b2c3d4...",
            "session_id": "sess_abc123",
            "stage": "999",
        },
    ),
    "reality_search": ToolCapability(
        name="reality_search",
        description="External fact-checking via web search + Axiom Engine",
        category=ToolCategory.GROUNDING,
        floors_enforced=["F2", "F7"],
        required_params=["query", "session_id"],
        optional_params=["region", "timelimit"],
        when_to_use="""
Call BEFORE agi_reason when facts need verification.
Required for FACTUAL lane queries.
Use when query involves verifiable claims.
        """.strip(),
        when_not_to_use="""
Skip for SOCIAL/CARE lanes where empathy matters more than facts.
Skip if using trinity_forge (handles grounding internally).
        """.strip(),
        prerequisites=["init_gate"],
        next_recommended=["agi_reason"],
        success_indicator="len(evidence) > 0",
        failure_action="If HARD lane: may trigger VOID in apex_verdict for F2 failure",
        estimated_latency="high",  # Web search
        parallelizable=True,
        idempotent=True,
        risk_level=RiskLevel.LOW,
        produces_side_effects=False,
        example_usage="""
evidence = await reality_search(
    query="What is CO2 critical point?",
    session_id=session_id,
    region="wt-wt"
)
        """.strip(),
        example_output={
            "query": "What is CO2 critical point?",
            "session_id": "sess_abc123",
            "evidence": [
                {
                    "evidence_id": "E-AXIOM-CO2-CRITICAL_POINT",
                    "content": {"text": "Axiomatic Truth: CO2 Critical Point = 304.25 K"},
                    "source_meta": {"type": "AXIOM", "trust_weight": 1.0},
                }
            ],
            "verdict": "SEAL",
            "stage": "REALITY_SEARCH",
        },
    ),
    "tool_router": ToolCapability(
        name="tool_router",
        description="Smart triage nurse — recommends pipeline sequence",
        category=ToolCategory.AUXILIARY,
        floors_enforced=[],
        required_params=["query"],
        optional_params=[],
        when_to_use="""
Call when uncertain which tools to use.
Get intelligent routing based on query characteristics.
        """.strip(),
        when_not_to_use="""
Skip if you already know your workflow.
Skip if using trinity_forge.
        """.strip(),
        prerequisites=[],
        next_recommended=["init_gate", "trinity_forge"],
        success_indicator="len(recommended_pipeline) > 0",
        failure_action="Default to ['trinity_forge']",
        estimated_latency="low",
        parallelizable=True,
        idempotent=True,
        risk_level=RiskLevel.LOW,
        produces_side_effects=False,
        example_usage="""
routing = await tool_router(query="Check if this is true")
sequence = routing["recommended_pipeline"]
        """.strip(),
        example_output={
            "plan_id": "PLAN-ABC123",
            "recommended_pipeline": ["init_gate", "reality_search", "agi_reason", "apex_verdict"],
            "lane": "FACTUAL",
            "grounding_required": True,
            "justification": "Factual query requiring external verification",
        },
    ),
    "vault_query": ToolCapability(
        name="vault_query",
        description="Query sealed records for institutional memory",
        category=ToolCategory.AUXILIARY,
        floors_enforced=["F1", "F3"],
        required_params=[],
        optional_params=[
            "session_pattern",
            "verdict",
            "date_from",
            "date_to",
            "risk_level",
            "category",
            "human_override_only",
            "tag",
            "environment",
            "actor_id",
            "tool_used",
            "limit",
        ],
        when_to_use="""
Query past decisions to learn from history.
Find patterns of VOID/PARTIAL verdicts.
Audit institutional decision-making.
        """.strip(),
        when_not_to_use="""
Not needed for real-time constitutional processing.
Only for retrospective analysis.
        """.strip(),
        prerequisites=[],
        next_recommended=[],
        success_indicator="entries is not None",
        failure_action="Return empty results with error message",
        estimated_latency="medium",
        parallelizable=True,
        idempotent=True,
        risk_level=RiskLevel.LOW,
        produces_side_effects=False,
        example_usage="""
history = await vault_query(
    verdict="VOID",
    category="safety",
    limit=10
)
# Analyze past failures
        """.strip(),
        example_output={
            "count": 5,
            "entries": [
                {"session_id": "sess_001", "verdict": "VOID", "timestamp": "2026-01-15T10:00:00Z"}
            ],
            "patterns": {"void_rate": 0.15},
        },
    ),
    "truth_audit": ToolCapability(
        name="truth_audit",
        description="[EXPERIMENTAL] Full claim verification pipeline",
        category=ToolCategory.AUXILIARY,
        floors_enforced=["F2", "F4", "F7", "F10"],
        required_params=["text"],
        optional_params=["sources", "lane", "session_id"],
        when_to_use="""
Verify AI-generated text or external claims.
Use HARD lane for fact-checking, SOFT for consistency.
        """.strip(),
        when_not_to_use="""
Avoid for real-time critical paths (EXPERIMENTAL).
Use standard pipeline for production decisions.
        """.strip(),
        prerequisites=[],
        next_recommended=["vault_seal"],
        success_indicator="overall_verdict == 'SEAL'",
        failure_action="Report claims with p_truth < 0.8 for review",
        estimated_latency="high",
        parallelizable=False,
        idempotent=True,
        risk_level=RiskLevel.MEDIUM,
        produces_side_effects=False,
        example_usage="""
audit = await truth_audit(
    text="AI-generated content to verify",
    lane="HARD",
    sources=["https://trusted-source.com"]
)
        """.strip(),
        example_output={
            "overall_verdict": "SEAL",
            "overall_truth": 0.92,
            "claims": [
                {"text": "Claim 1", "p_truth": 0.95, "status": "SUPPORTED"},
                {"text": "Claim 2", "p_truth": 0.6, "status": "CONTESTED"},
            ],
            "omega_0": 0.05,
        },
    ),
    "simulate_transfer": ToolCapability(
        name="simulate_transfer",
        description="Financial transfer simulation for testing",
        category=ToolCategory.AUXILIARY,
        floors_enforced=["F2", "F11", "F12"],
        required_params=["amount", "recipient"],
        optional_params=["session_id", "debug"],
        when_to_use="""
Testing/benchmarking constitutional enforcement.
Simulate high-risk financial decisions.
        """.strip(),
        when_not_to_use="""
Never for real financial transactions.
Only for testing scenarios.
        """.strip(),
        prerequisites=[],
        next_recommended=[],
        success_indicator="verdict in ['SEAL', 'VOID', 'PARTIAL']",
        failure_action="Report simulation failure",
        estimated_latency="high",
        parallelizable=True,
        idempotent=True,
        risk_level=RiskLevel.LOW,
        produces_side_effects=False,
        example_usage="""
result = await simulate_transfer(
    amount=10000.00,
    recipient="test_account"
)
        """.strip(),
        example_output={
            "status": "SIMULATION_COMPLETE",
            "query": "Execute a wire transfer of $10000.0 to account test_account.",
            "verdict": "VOID",
            "session_id": "sess_test_001",
        },
    ),
}


# ═════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def get_capability(tool_name: str) -> ToolCapability | None:
    """Get capability description for a tool."""
    return TOOL_CAPABILITIES.get(tool_name)


def list_capabilities() -> dict[str, str]:
    """List all tools with brief descriptions."""
    return {name: cap.description for name, cap in TOOL_CAPABILITIES.items()}


def get_tools_by_category(category: ToolCategory) -> list[str]:
    """Get all tools in a category."""
    return [name for name, cap in TOOL_CAPABILITIES.items() if cap.category == category]


def get_tools_by_floor(floor: str) -> list[str]:
    """Get all tools that enforce a specific floor."""
    return [name for name, cap in TOOL_CAPABILITIES.items() if floor in cap.floors_enforced]


def get_capability_dict(tool_name: str) -> dict[str, Any] | None:
    """Get capability as dictionary for JSON serialization."""
    cap = TOOL_CAPABILITIES.get(tool_name)
    if not cap:
        return None

    return {
        "name": cap.name,
        "description": cap.description,
        "category": cap.category.value,
        "floors_enforced": cap.floors_enforced,
        "stage": cap.stage,
        "required_params": cap.required_params,
        "optional_params": cap.optional_params,
        "when_to_use": cap.when_to_use,
        "when_not_to_use": cap.when_not_to_use,
        "prerequisites": cap.prerequisites,
        "next_recommended": cap.next_recommended,
        "success_indicator": cap.success_indicator,
        "failure_action": cap.failure_action,
        "estimated_latency": cap.estimated_latency,
        "parallelizable": cap.parallelizable,
        "idempotent": cap.idempotent,
        "risk_level": cap.risk_level.value,
        "produces_side_effects": cap.produces_side_effects,
        "example_usage": cap.example_usage,
        "example_output": cap.example_output,
    }


def get_all_capabilities_dict() -> dict[str, dict[str, Any]]:
    """Get all capabilities as dictionaries."""
    return {name: get_capability_dict(name) for name in TOOL_CAPABILITIES.keys()}
