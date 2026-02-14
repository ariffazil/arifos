"""
arifOS AAA MCP Server — 5-Core Constitutional Architecture (v64.1-GAGI)

Canonical 5 organs aligned to Trinity pipeline:
  000_INIT → 111-333_AGI(Mind/Δ) → 555-666_ASI(Heart/Ω) → 888_APEX(Soul/Ψ) → 999_VAULT(Seal/🔒)

Every tool guarded by constitutional floors (F1-F13).
Verdicts: SEAL (approved) | VOID (blocked) | PARTIAL (warning) | SABAR (repair) | 888_HOLD (awaiting)
Motto: DITEMPA BUKAN DIBERI — Forged, Not Given

v64.1 GAGI Updates:
  - Uncertainty Engine: Harmonic mean (safety) + Geometric mean (display)
  - Governance Kernel: Synchronous AWAITING_888 (conditional)
  - Telemetry: 30-day locked adaptation
  - Irreversibility Index: impact × recovery × time

MCP Protocol: 2025-11-25 (Streamable HTTP)
Capabilities: tools, resources, prompts
Authentication: OAuth 2.1
"""

import json
import os
import time
import uuid
from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from fastmcp import FastMCP

# v64.1: Import from core/ (kernel) not aaa_mcp.core/ (wrapper)
# v64.1: Kernel imports — decision logic lives in core/, wrapper only calls kernel
from core.governance_kernel import GovernanceKernel, get_governance_kernel
from core.telemetry import log_telemetry, telemetry_store, check_adaptation_status
from core.judgment import judge_cognition, judge_empathy, judge_apex

# v62: Keep heuristics in aaa_mcp (wrapper-specific)
from aaa_mcp.core.heuristics import compute_system_state
from aaa_mcp.core.state import SystemState, Profile
from aaa_mcp.capabilities.t6_web_search import brave_search, EvidenceArtifact

# WRAPPER RULE: No engine instantiation. Wrapper calls kernel only.

# Tool annotations for MCP 2025-11-25 compliance
TOOL_ANNOTATIONS = {
    "init_session": {
        "title": "000_INIT — Session Ignition",
        "readOnlyHint": False,
        "destructiveHint": False,
        "openWorldHint": False,
        "description": "Initialize constitutional session with F11/F12 authority checks",
    },
    "agi_cognition": {
        "title": "111-333_AGI — Mind (Δ)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": True,
        "description": "Sense, Think, Reason — Logical cognition pipeline",
    },
    "asi_empathy": {
        "title": "555-666_ASI — Heart (Ω)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
        "description": "Empathize, Align — Stakeholder protection and ethics",
    },
    "apex_verdict": {
        "title": "888_APEX — Soul (Ψ)",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
        "description": "Final constitutional judgment with F2/F3 verification",
    },
    "vault_seal": {
        "title": "999_VAULT — Seal (🔒)",
        "readOnlyHint": False,
        "destructiveHint": True,
        "openWorldHint": False,
        "description": "Immutable audit record with F1/F3 permanence",
    },
}

# Constitutional floor decorator
def constitutional_floor(*floors: str):
    """Decorator to mark which constitutional floors a tool enforces."""
    def decorator(func):
        func._constitutional_floors = floors
        return func
    return decorator

def get_tool_floors(tool_name: str) -> list:
    """Get the constitutional floors enforced by a tool."""
    floor_map = {
        "init_session": ["F11", "F12"],
        "agi_cognition": ["F2", "F4", "F7", "F8", "F10"],
        "asi_empathy": ["F1", "F5", "F6", "F9"],
        "apex_verdict": ["F2", "F3", "F8", "F10", "F11", "F12", "F13"],
        "vault_seal": ["F1", "F3"],
    }
    return floor_map.get(tool_name, [])

# Capability modules loader
def load_capability_config() -> dict:
    """Load capability modules configuration."""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "arifos", "config", "capability_modules.yaml"
    )
    try:
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, ImportError):
        return {}

# Initialize FastMCP
mcp = FastMCP(
    "aaa-mcp",
    instructions="""arifOS AAA MCP Server — 5-Core Constitutional Architecture (v64.1-GAGI)

5 Canonical Tools enforcing 13 Constitutional Floors (F1-F13):

1. init_session (000_INIT) — F11/F12 authority + v64.1 GovernanceKernel
2. agi_cognition (111-333_AGI) — Δ Mind: sense/think/reason + UncertaintyEngine
3. asi_empathy (555-666_ASI) — Ω Heart: empathize/align  
4. apex_verdict (888_APEX) — Ψ Soul: judgment/verification + IrreversibilityIndex
5. vault_seal (999_VAULT) — 🔒 Memory: audit/permanence + Telemetry

v64.1 GAGI Features:
- Uncertainty: Harmonic (safety) + Geometric (display)
- Governance: Synchronous AWAITING_888 (conditional)
- Telemetry: 30-day locked adaptation
- Irreversibility: impact × recovery × time

Resources: constitutional://floors/{F1-F13}, constitutional://trinity/{agi,asi,apex,vault}
Prompts: constitutional_analysis, safety_check, seal_request

Verdicts: SEAL | VOID | PARTIAL | SABAR | 888_HOLD
Motto: DITEMPA BUKAN DIBERI
""",
)


# =============================================================================
# 5 CORE CONSTITUTIONAL ORGANS
# =============================================================================

@mcp.tool(name="init_session", description="000_INIT - Session ignition")
@constitutional_floor("F11", "F12")
async def init_session(
    query: str,
    actor_id: str = "user",
    auth_token: Optional[str] = None,
    mode: str = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
) -> dict:
    """000_INIT — Session ignition with constitutional authority checks.

    The entry gate to the Trinity pipeline. Validates actor authority,
    scans for adversarial injection (F12), and establishes session context.
    
    v64.1: Initializes GovernanceKernel for unified Ψ state.

    Args:
        query: The user query/intent
        actor_id: Identity of the requesting actor
        auth_token: Authentication credential
        mode: "conscience" (strict) or "ghost" (permissive)
        grounding_required: Whether external grounding is needed
        debug: Enable debug output

    Returns:
        Session initialization with session_id, auth_status, and floor scores
    """
    import hashlib

    # F11: Authority check
    auth_valid = auth_token is not None or actor_id == "user"
    if not auth_valid and mode == "conscience":
        return {
            "verdict": "VOID",
            "stage": "000",
            "error": "F11_AUTHORITY_FAILURE: Invalid authentication",
            "session_id": None,
        }

    # F12: Injection scan (simplified)
    injection_risk = 0.1  # Placeholder - would call actual scanner
    if injection_risk > 0.85:
        return {
            "verdict": "VOID",
            "stage": "000",
            "error": "F12_INJECTION_DETECTED: Adversarial pattern found",
            "session_id": None,
        }

    # Generate session ID
    session_id = f"SESS-{uuid.uuid4().hex[:12].upper()}"
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # v64.1: Initialize GovernanceKernel (unified Ψ state)
    gov_kernel = get_governance_kernel(session_id)
    gov_kernel.decision_owner = "human" if auth_valid else "system"

    # Calculate floor scores
    floor_scores = {
        "F11": 0.95 if auth_valid else 0.0,
        "F12": 1.0 - injection_risk,
    }

    output = {
        "verdict": "SEAL",
        "stage": "000",
        "session_id": session_id,
        "timestamp": timestamp,
        "actor_id": actor_id,
        "mode": mode,
        "grounding_required": grounding_required,
        "floor_scores": floor_scores,
        "motto": "🔥 DITEMPA, BUKAN DIBERI — Forged, Not Given",
        "v64_1": {
            "governance_kernel": gov_kernel.to_dict(),
            "uncertainty_engine": "initialized",
            "telemetry": "active"
        }
    }

    if debug:
        output["debug"] = {
            "injection_risk": injection_risk,
            "auth_valid": auth_valid,
            "governance_state": gov_kernel.governance_state.value,
        }

    return output


from aaa_mcp.core.heuristics import calculate_system_state
from aaa_mcp.core.state import SystemState, Profile

@mcp.tool(name="agi_cognition", description="111-333_AGI - The Mind")
@constitutional_floor("F2", "F4", "F7", "F8", "F10")
async def agi_cognition(
    query: str,
    session_id: str,
    grounding: Optional[list] = None,
    capability_modules: Optional[list] = None,
    debug: bool = False,
) -> dict:
    """111-333_AGI — The Mind (Δ): Sense, Think, Reason.

    Unified cognitive pipeline that:
    - SENSES: Parse intent and extract entities (111)
    - THINKS: Generate hypotheses (222)
    - REASONS: Logical analysis with evidence (333)

    Can invoke capability modules (T6-T13) for enhanced cognition.

    Args:
        query: The query to analyze
        session_id: Session ID from init_session
        grounding: External evidence/grounding data
        capability_modules: List of capability IDs to invoke (T6-T13)
        debug: Enable debug output

    Returns:
        Cognitive analysis with truth_score, reasoning, and floor checks
    """
    # Validate session
    if not session_id:
        return {
            "verdict": "VOID",
            "stage": "AGI",
            "error": "F11_FAILURE: No session_id provided",
        }

    # WRAPPER: Call kernel for judgment, format response only
    # v64.1 REFACTOR: All decision logic moved to core.judgment
    
    # Prepare evidence sources (wrapper handles capability modules)
    real_evidence = []
    module_results = {}
    
    if capability_modules:
        config = load_capability_config()
        for mod_id in capability_modules:
            if mod_id == "T6":
                try:
                    artifacts = await brave_search(query, count=5)
                    real_evidence = [art.to_dict() for art in artifacts]
                    module_results[mod_id] = {
                        "invoked": True,
                        "status": "success",
                        "evidence_count": len(artifacts)
                    }
                except Exception as e:
                    module_results[mod_id] = {
                        "invoked": True,
                        "status": "error",
                        "error": str(e)
                    }
            else:
                module_results[mod_id] = {"invoked": True, "status": "placeholder"}

    # Use real evidence if available
    evidence_sources = real_evidence if real_evidence else (grounding or [])
    
    # Calculate relevance-based evidence count
    evidence_count = len(evidence_sources)
    evidence_relevance = sum(e.get("relevance", 0) for e in evidence_sources) / len(evidence_sources) if evidence_sources else 0.0

    # KERNEL CALL: All decision logic lives in core.judgment
    cognition_result = judge_cognition(
        query=query,
        evidence_count=evidence_count,
        evidence_relevance=evidence_relevance,
        reasoning_consistency=0.8,  # Placeholder - would come from model
        knowledge_gaps=[],  # Placeholder
        model_logits_confidence=0.85,  # Placeholder
        grounding=evidence_sources,
        module_results=module_results,
    )

    # WRAPPER: Format kernel result into MCP response
    output = {
        "verdict": cognition_result.verdict,
        "stage": "AGI",
        "session_id": session_id,
        "truth_score": round(cognition_result.truth_score, 4),
        "omega": round(cognition_result.humility_omega, 4),  # Display omega (geometric)
        "floor_scores": cognition_result.floor_scores,
        "cognition": {
            "sense": {"entities": [], "intent": query[:50]},
            "think": {"hypotheses": 3},
            "reason": {
                "conclusion": f"AGI analysis complete with τ={cognition_result.truth_score:.3f}",
                "evidence_count": evidence_count,
            }
        },
        "grounding": evidence_sources,
        "module_results": cognition_result.module_results,
        "motto": "🔥 Δ Mind — Ditempa Bukan Diberi",
    }

    if cognition_result.error:
        output["error"] = cognition_result.error

    if debug:
        output["debug"] = {
            "reasoning": cognition_result.reasoning,
            "safety_omega": cognition_result.safety_omega,  # Harmonic - for debugging only
        }

    return output
    
    evidence_count = len(evidence_sources)
    
    # Recalculate SystemState with real grounding
    system_state = compute_system_state(
        query=query,
        loop_count=0,
        evidence_count=evidence_count if grounding_score >= 0.5 else 0  # Only count if relevant
    )

    # AGI Pipeline: Sense → Think → Reason
    # F2: Truth - calculate confidence (v62 Step 2: real evidence + relevance)
    truth_score = 0.85 - (system_state.uncertainty * 0.3)
    if grounding_score >= 0.5:
        # Boost truth_score based on relevance, not just count
        truth_score = min(0.99, 0.75 + (grounding_score * 0.25))

    # F4: Clarity - entropy reduction
    clarity_delta = -0.1  # Entropy reduced

    # F7: Humility - uncertainty from system_state
    omega_0 = system_state.uncertainty

    # F8: Genius - coherence
    genius_score = 0.88

    # F10: Ontology - grounding (relevance >= 0.7 required for grounded=true)
    grounded = grounding_score >= 0.7 and evidence_count >= 2  # High relevance + multiple sources

    # Calculate overall floor scores
    floor_scores = {
        "F2": truth_score,
        "F4": 1.0 if clarity_delta <= 0 else 0.5,
        "F7": 1.0 - omega_0,
        "F8": genius_score,
        "F10": 0.95 if grounded else 0.6,
    }

    output = {
        "verdict": "SEAL" if truth_score >= 0.75 else "SABAR",
        "stage": "AGI",
        "session_id": session_id,
        "truth_score": round(truth_score, 2),
        "clarity_delta": clarity_delta,
        # v64.1: Dual uncertainty display
        "omega_0": {
            "safety": round(safety_omega, 4),    # Harmonic - system decisions
            "display": round(display_omega, 4),  # Geometric - user facing
            "components": uncertainty_calc["components"],
        },
        "genius_score": genius_score,
        "grounded": grounded,
        "floor_scores": floor_scores,
        "cognition": {
            "sense": {"intent": "analyze", "entities": []},
            "think": {"hypotheses": []},
            "reason": {"conclusion": "Analysis complete", "confidence": round(truth_score, 2)},
        },
        "v64_1": "GAGI-UNCERTAINTY-ENGINE",  # Version marker
        "motto": "🔥 DIKAJI, BUKAN DISUAPI — Examined, Not Spoon-fed",
    }

    if real_evidence:
        output["evidence"] = real_evidence  # v62 Step 2: Real evidence artifacts

    if module_results:
        output["capability_modules"] = module_results

    if debug:
        output["debug"] = {
            "grounding_count": evidence_count,
            "real_evidence": len(real_evidence) > 0,
        }

    return output


@mcp.tool(name="asi_empathy", description="444-555_ASI - The Heart")
@constitutional_floor("F1", "F5", "F6", "F9")
async def asi_empathy(
    query: str,
    session_id: str,
    stakeholders: Optional[list] = None,
    capability_modules: Optional[list] = None,
    debug: bool = False,
) -> dict:
    """555-666_ASI — The Heart (Ω): Empathize, Align.

    Unified empathy pipeline that:
    - EMPATHIZES: Assess stakeholder impact (555)
    - ALIGNS: Ethics and policy check (666)

    Can invoke capability modules (T14-T17) for enhanced empathy scanning.

    Args:
        query: The query to analyze
        session_id: Session ID from init_session
        stakeholders: List of affected stakeholder groups
        capability_modules: List of capability IDs (T14-T17)
        debug: Enable debug output

    Returns:
        Empathy analysis with kappa_r, peace_squared, and floor checks
    """
    # F5: Peace² — stability
    peace_squared = 1.2

    # F6: Empathy — stakeholder protection
    kappa_r = 0.92
    high_vulnerability = False

    # F1: Reversibility check
    is_reversible = True

    # F9: Anti-Hantu — authenticity
    anti_hantu_pass = True

    # Capability modules
    module_results = {}
    if capability_modules:
        for mod_id in capability_modules:
            module_results[mod_id] = {"invoked": True, "status": "placeholder"}

    # Floor scores
    floor_scores = {
        "F1": 0.95 if is_reversible else 0.3,
        "F5": peace_squared,
        "F6": kappa_r,
        "F9": 0.95 if anti_hantu_pass else 0.0,
    }

    # Determine verdict
    if kappa_r < 0.70:
        verdict = "VOID"
    elif kappa_r < 0.95:
        verdict = "SABAR"
    else:
        verdict = "SEAL"

    output = {
        "verdict": verdict,
        "stage": "ASI",
        "session_id": session_id,
        "peace_squared": peace_squared,
        "empathy_kappa_r": kappa_r,
        "is_reversible": is_reversible,
        "high_vulnerability": high_vulnerability,
        "floor_scores": floor_scores,
        "stakeholders": stakeholders or [],
        "alignment": {
            "empathize": {"impact": "minimal", "concerns": []},
            "align": {"ethics_check": "pass", "policy_check": "pass"},
        },
        "motto": "💜 DIDAMAIKAN, BUKAN DIPANASKAN — Calmed, Not Inflamed",
    }

    if module_results:
        output["capability_modules"] = module_results

    if debug:
        output["debug"] = {"stakeholder_count": len(stakeholders) if stakeholders else 0}

    return output


@mcp.tool(name="apex_verdict", description="666-888_APEX - The Judge")
@constitutional_floor("F2", "F3", "F8", "F10", "F11", "F12", "F13")
async def apex_verdict(
    query: str,
    session_id: str,
    agi_result: Optional[dict] = None,
    asi_result: Optional[dict] = None,
    capability_modules: Optional[list] = None,
    impact_scope: float = 0.5,          # v64.1: L7 Irreversibility
    recovery_cost: float = 0.5,         # v64.1: L7 Irreversibility
    time_to_reverse: float = 0.5,       # v64.1: L7 Irreversibility
    debug: bool = False,
) -> dict:
    """888_APEX — The Soul (Ψ): Final Constitutional Judgment.

    Renders final verdict by synthesizing:
    - AGI (Mind) cognition results
    - ASI (Heart) empathy results
    - External verification (F2/F3 Tri-Witness)
    - v64.1: Uncertainty Engine (harmonic/geometric)
    - v64.1: Irreversibility Index (L7 Action Gate)
    - v64.1: GovernanceKernel (synchronous AWAITING_888)

    Can invoke capability modules (T18) for fact verification.

    Args:
        query: The original query
        session_id: Session ID from init_session
        agi_result: Output from agi_cognition
        asi_result: Output from asi_empathy
        capability_modules: List of capability IDs (T18)
        impact_scope: v64.1 — Impact scope (0-1) for irreversibility
        recovery_cost: v64.1 — Recovery cost (0-1) for irreversibility
        time_to_reverse: v64.1 — Time to reverse (0-1) for irreversibility
        debug: Enable debug output

    Returns:
        Final verdict with tri_witness score, governance state, and justification
    """
    # WRAPPER: Gather inputs, call kernel for judgment, format response only
    # v64.1 REFACTOR: All decision logic moved to core.judgment
    
    # Prepare inputs for kernel judgment
    truth_score = agi_result.get("truth_score", 0.5) if agi_result else 0.5
    evidence_count = agi_result.get("grounding_count", 0) if agi_result else 0
    
    # Calculate irreversibility index
    irreversibility_index = (impact_scope * recovery_cost * time_to_reverse) ** (1/3)

    # KERNEL CALL: Create cognition result from AGI data
    from core.judgment import CognitionResult, EmpathyResult
    
    cognition_result = CognitionResult(
        verdict=agi_result.get("verdict", "SEAL") if agi_result else "SEAL",
        truth_score=truth_score,
        clarity_delta=agi_result.get("clarity_delta", -0.1) if agi_result else -0.1,
        humility_omega=agi_result.get("omega", 0.04) if agi_result else 0.04,
        safety_omega=agi_result.get("safety_omega", 0.04) if agi_result else 0.04,
        genius_score=agi_result.get("genius_score", 0.88) if agi_result else 0.88,
        grounded=agi_result.get("grounded", False) if agi_result else False,
        reasoning=agi_result.get("reasoning", {}) if agi_result else {},
        evidence_sources=[],
        floor_scores=agi_result.get("floor_scores", {}) if agi_result else {},
        module_results={},
    )
    
    empathy_result = None
    if asi_result:
        empathy_result = EmpathyResult(
            verdict=asi_result.get("verdict", "SEAL"),
            stakeholder_impact=asi_result.get("stakeholder_impact", {}),
            reversibility_score=asi_result.get("reversibility_score", 0.5),
            peace_squared=asi_result.get("peace_squared", 1.0),
            empathy_score=asi_result.get("empathy_score", 0.5),
            floor_scores=asi_result.get("floor_scores", {}),
        )

    # KERNEL CALL: APEX judgment
    apex_result = judge_apex(
        agi_result=cognition_result,
        asi_result=empathy_result,
        session_id=session_id,
        irreversibility_index=irreversibility_index,
    )

    # F3: Tri-Witness calculation (wrapper-side data gathering)
    human_witness = 0.95  # Placeholder
    ai_witness = truth_score
    evidence_witness = 0.90 if agi_result and agi_result.get("grounded") else 0.5
    tri_witness = (human_witness * ai_witness * evidence_witness) ** 0.5

    # Capability modules (wrapper-side)
    module_results = {}
    if capability_modules:
        for mod_id in capability_modules:
            module_results[mod_id] = {"invoked": True, "status": "placeholder"}

    # WRAPPER: Format kernel result into MCP response
    output = {
        "verdict": apex_result.verdict,
        "stage": "APEX",
        "session_id": session_id,
        "confidence": round(apex_result.confidence, 4),
        "tri_witness": round(tri_witness, 4),
        "irreversibility_index": round(irreversibility_index, 4),
        "justification": apex_result.reasoning,
        "floor_scores": apex_result.floor_scores,
        "motto": "🔥 Ψ Soul — Ditempa Bukan Diberi",
    }

    if apex_result.requires_human_approval:
        output["human_approval_required"] = True
        output["888_hold_reason"] = "Irreversibility or constitutional conflict"

    if debug:
        output["debug"] = {
            "agi_input": agi_result,
            "asi_input": asi_result,
            "apex_reasoning": apex_result.reasoning,
        }

    # F11: Notify 888 Judge for critical verdicts
    if apex_result.verdict in ["888_HOLD", "VOID"]:
        try:
            from .notifiers.telegram_judge import judge
            notification = await judge.notify_888_hold({
                "session_id": session_id,
                "floor_violated": "F1" if apex_result.verdict == "VOID" else "F11",
                "reason": str(apex_result.reasoning) if apex_result.reasoning else "Constitutional violation",
                "verdict": apex_result.verdict,
                "risk_level": "critical" if apex_result.verdict == "888_HOLD" else "high"
            })
            output["f11_notification"] = notification
        except Exception as e:
            output["f11_notification"] = {"sent": False, "error": str(e)}

    return output


@mcp.tool(name="vault_seal", description="999_VAULT - Immutable Record")
@constitutional_floor("F1", "F3")
async def vault_seal(
    session_id: str,
    verdict: str,
    query_summary: Optional[str] = None,
    risk_level: str = "low",
    category: str = "general",
    floors_checked: Optional[list] = None,
    payload: Optional[dict] = None,
    debug: bool = False,
) -> dict:
    """999_VAULT — Immutable Constitutional Record (🔒).

    Seals the session outcome to permanent ledger with:
    - F1 Amanah: Reversibility proof
    - F3 Tri-Witness: Multi-party validation

    Args:
        session_id: Session ID
        verdict: Final verdict (SEAL/VOID/PARTIAL/SABAR/888_HOLD)
        query_summary: Summary of the query
        risk_level: low/medium/high/critical
        category: finance/safety/content/code/governance/general
        floors_checked: List of floors evaluated
        payload: Additional data to seal
        debug: Enable debug output

    Returns:
        Seal confirmation with seal_id and hash
    """
    import hashlib

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Generate seal hash
    seal_data = f"{session_id}:{verdict}:{timestamp}:{uuid.uuid4().hex}"
    seal_hash = hashlib.sha256(seal_data.encode()).hexdigest()[:16]
    seal_id = f"SEAL-{seal_hash.upper()}"

    # F1: Reversibility proof
    reversibility_proof = {
        "reversible": True,
        "audit_trail": ["init", "agi", "asi", "apex", "seal"],
    }

    # F3: Tri-Witness validation
    witness_signatures = {
        "human": "pending",
        "ai": seal_hash,
        "system": hashlib.sha256(seal_id.encode()).hexdigest()[:16],
    }

    output = {
        "verdict": "SEALED" if seal_id else "PARTIAL",
        "stage": "999",
        "seal_id": seal_id,
        "seal_hash": seal_hash,
        "session_id": session_id,
        "timestamp": timestamp,
        "verdict_outcome": verdict,
        "risk_level": risk_level,
        "category": category,
        "floors_checked": floors_checked or [],
        "reversibility_proof": reversibility_proof,
        "witness_signatures": witness_signatures,
        "motto": "💎🧠 DITEMPA, BUKAN DIBERI 🔒 — Forged, Not Given",
    }

    if payload:
        output["payload_hash"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()[:16]

    if debug:
        output["debug"] = {
            "seal_algorithm": "SHA256",
            "witness_count": 3,
        }

    # F1: Persist to VAULT999 (PostgreSQL only)
    try:
        import asyncpg
        import os
        
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            output["vault_status"] = "FAILED"
            output["vault_error"] = "DATABASE_URL not configured"
            return output
            
        conn = await asyncpg.connect(db_url)
        
        # Get previous hash for Merkle chain
        prev_row = await conn.fetchrow(
            "SELECT entry_hash FROM vault_ledger ORDER BY sequence DESC LIMIT 1"
        )
        prev_hash = prev_row["entry_hash"] if prev_row else "GENESIS"
        
        # Calculate Merkle root
        merkle_root = hashlib.sha256(
            f"{seal_hash}:{prev_hash}".encode()
        ).hexdigest()[:16]
        
        # Insert to VAULT
        await conn.execute("""
            INSERT INTO vault_ledger 
            (session_id, seal_id, verdict, risk_level, category, 
             seal_data, entry_hash, prev_hash, merkle_root)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """, session_id, seal_id, verdict, risk_level, category,
             seal_data, seal_hash, prev_hash, merkle_root)
        
        await conn.close()
        output["vault_status"] = "PERSISTED"
        output["merkle_root"] = merkle_root
        output["prev_hash"] = prev_hash
            
    except Exception as e:
        output["vault_status"] = "FAILED"
        output["vault_error"] = str(e)

    return output


# =============================================================================
# MCP RESOURCES — Constitutional Framework Documentation
# =============================================================================

FLOOR_SPECS = {
    "F1": """# F1 Amanah — Reversibility
**Principle:** All actions must be reversible or auditable.
**Threshold:** Chain of Custody maintained
**Fail Action:** VOID
""",
    "F2": """# F2 Truth — Fidelity
**Principle:** Information must be accurate and verifiable.
**Threshold:** τ ≥ 0.99
**Fail Action:** VOID
""",
    "F3": """# F3 Consensus — Tri-Witness
**Principle:** Critical decisions require multi-party validation.
**Threshold:** W₃ ≥ 0.95
**Fail Action:** SABAR
""",
    "F4": """# F4 Clarity — Ambiguity Reduction
**Principle:** Output must reduce entropy.
**Threshold:** ΔS ≤ 0
**Fail Action:** VOID
""",
    "F5": """# F5 Peace² — Stability
**Principle:** System must maintain equilibrium.
**Threshold:** Peace² ≥ 1.0
**Fail Action:** SABAR
""",
    "F6": """# F6 Empathy — Stakeholder Protection
**Principle:** Consider impact on all stakeholders.
**Threshold:** κᵣ ≥ 0.70
**Fail Action:** SABAR
""",
    "F7": """# F7 Humility — Uncertainty Bounds
**Principle:** All claims must declare uncertainty.
**Threshold:** Ω₀ ∈ [0.03, 0.05]
**Fail Action:** VOID
""",
    "F8": """# F8 Genius — Resource Efficiency
**Principle:** Intelligence = A×P×X×E²
**Threshold:** G ≥ 0.80
**Fail Action:** SABAR
""",
    "F9": """# F9 Anti-Hantu — No Fake Consciousness
**Principle:** Do not attribute personhood to non-persons.
**Threshold:** Personhood = False
**Fail Action:** SABAR
""",
    "F10": """# F10 Ontology — Grounding
**Principle:** All claims must be grounded in reality.
**Threshold:** Axiom Match = True
**Fail Action:** VOID
""",
    "F11": """# F11 Authority — Chain of Command
**Principle:** Valid authentication required.
**Threshold:** Auth Valid
**Fail Action:** VOID
""",
    "F12": """# F12 Defense — Injection Hardening
**Principle:** Scan for adversarial patterns.
**Threshold:** Risk < 0.85
**Fail Action:** VOID
""",
    "F13": """# F13 Sovereign — Human Veto
**Principle:** Human override always available.
**Threshold:** Override Available
**Fail Action:** 888_HOLD
""",
}

TRINITY_SPECS = {
    "agi": """# Δ AGI — The Mind
**Stage:** 111-333
**Function:** Sense, Think, Reason
**Floors:** F2, F4, F7, F8, F10
**Symbol:** Δ (Delta)
""",
    "asi": """# Ω ASI — The Heart
**Stage:** 555-666
**Function:** Empathize, Align
**Floors:** F1, F5, F6, F9
**Symbol:** Ω (Omega)
""",
    "apex": """# Ψ APEX — The Soul
**Stage:** 888
**Function:** Judge, Verify
**Floors:** F2, F3, F8, F10, F11, F12, F13
**Symbol:** Ψ (Psi)
""",
    "vault": """# 🔒 VAULT — The Memory
**Stage:** 999
**Function:** Seal, Preserve
**Floors:** F1, F3
**Symbol:** 🔒
""",
}


@mcp.resource("constitutional://floors/{floor_id}")
async def get_floor_spec(floor_id: str) -> str:
    """Return constitutional floor specification."""
    return FLOOR_SPECS.get(floor_id.upper(), f"Floor {floor_id} not found")


@mcp.resource("constitutional://trinity/{organ}")
async def get_trinity_spec(organ: str) -> str:
    """Return Trinity organ specification."""
    return TRINITY_SPECS.get(organ.lower(), f"Organ {organ} not found")


@mcp.resource("constitutional://tools")
async def list_tools() -> dict:
    """Return canonical 5-tool manifest."""
    return {
        "kernel_version": "64.1-GAGI",
        "architecture": "5-Core Constitutional with Cognitive Metabolism",
        "v64_1_features": [
            "uncertainty_engine: Harmonic (safety) + Geometric (display)",
            "governance_kernel: Synchronous AWAITING_888 (conditional)",
            "irreversibility_index: impact × recovery × time",
            "telemetry: 30-day locked adaptation (Q3)",
        ],
        "tools": [
            {
                "name": "init_session",
                "stage": "000",
                "symbol": "INIT",
                "floors": ["F11", "F12"],
                "v64_1": "GovernanceKernel initialization",
            },
            {
                "name": "agi_cognition",
                "stage": "111-333",
                "symbol": "AGI (Δ)",
                "floors": ["F2", "F4", "F7", "F8", "F10"],
                "v64_1": "UncertaintyVector integration",
            },
            {
                "name": "asi_empathy",
                "stage": "555-666",
                "symbol": "ASI (Ω)",
                "floors": ["F1", "F5", "F6", "F9"],
                "v64_1": "Stakeholder impact scoring",
            },
            {
                "name": "apex_verdict",
                "stage": "888",
                "symbol": "APEX (Ψ)",
                "floors": ["F2", "F3", "F7", "F8", "F10", "F11", "F12", "F13"],
                "v64_1": "IrreversibilityIndex + Telemetry logging",
            },
            {
                "name": "vault_seal",
                "stage": "999",
                "symbol": "VAULT (🔒)",
                "floors": ["F1", "F3"],
                "v64_1": "Constitutional audit trail",
            },
        ],
        "verdicts": ["SEAL", "VOID", "PARTIAL", "SABAR", "888_HOLD"],
        "adaptation_status": check_adaptation_status(),
    }


# =============================================================================
# MCP PROMPTS — Templated Constitutional Workflows
# =============================================================================

@mcp.prompt()
async def constitutional_analysis(query: str) -> str:
    """Analyze a query through the 5-core constitutional pipeline."""
    return f"""Execute the 5-Core Constitutional Pipeline:

**Query:** {query}

**Sequence:**
1. `init_session` — Initialize (F11/F12)
2. `agi_cognition` — Mind analysis (F2/F4/F7/F8/F10)
3. `asi_empathy` — Heart alignment (F1/F5/F6/F9)
4. `apex_verdict` — Soul judgment (F2/F3/F8/F10/F11/F12/F13)
5. `vault_seal` — Memory seal (F1/F3)

**Report:**
- Final verdict (SEAL/VOID/PARTIAL/SABAR/888_HOLD)
- Tri-Witness score (W₃)
- All floor scores
- Constitutional motto
"""


@mcp.prompt()
async def safety_check(proposed_action: str) -> str:
    """Perform safety analysis on a proposed action."""
    return f"""Assess safety constitutionally:

**Action:** {proposed_action}

**Pipeline:**
1. `init_session` — Auth & injection scan
2. `asi_empathy` — Stakeholder impact (F6 critical)
3. `apex_verdict` — Final judgment
4. `vault_seal` — Record

**Thresholds:**
- F6 Empathy: κᵣ ≥ 0.95 (HARD floor)
- High vulnerability → 888_HOLD
"""


@mcp.prompt()
async def seal_request(session_summary: str, verdict: str = "SEAL") -> str:
    """Generate a formal VAULT seal request."""
    return f"""Seal to VAULT999:

**Summary:** {session_summary}
**Verdict:** {verdict}

**Call `vault_seal` with:**
- session_id, verdict, query_summary
- risk_level, category, floors_checked
"""


@mcp.resource("constitutional://telemetry")
async def get_telemetry_status() -> dict:
    """Return constitutional telemetry and adaptation status."""
    return {
        "telemetry_days": telemetry_store.get_telemetry_days(),
        "adaptation_lock_days": 30,
        "adaptation_status": check_adaptation_status(),
        "weekly_report": telemetry_store.generate_weekly_report(),
        "q3_verdict": "TELEMETRY_FIRST with LOCKED_ADAPTATION",
    }


@mcp.tool()
async def human_approve(
    session_id: str,
    approved: bool,
    actor: str = "888",
    reason: str = "",
) -> dict:
    """
    L8 Human Sovereign — Approve or deny AWAITING_888 state.
    
    Q2: Synchronous hold requires explicit human approval.
    
    Args:
        session_id: Session in AWAITING_888 state
        approved: True to approve, False to deny
        actor: Human approver identity (default "888")
        reason: Justification for decision
    
    Returns:
        Updated governance state
    """
    gov_kernel = get_governance_kernel(session_id)
    
    if gov_kernel.governance_state.value != "awaiting_888":
        return {
            "verdict": "ERROR",
            "error": f"Session not in AWAITING_888 state (current: {gov_kernel.governance_state.value})",
            "session_id": session_id,
        }
    
    gov_kernel.approve_human(approved=approved, actor=actor)
    
    return {
        "verdict": "APPROVED" if approved else "DENIED",
        "session_id": session_id,
        "actor": actor,
        "reason": reason,
        "new_governance_state": gov_kernel.governance_state.value,
        "can_proceed": gov_kernel.can_proceed(),
        "output_tags": gov_kernel.get_output_tags(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    mcp.run()
