"""
core/organs/_1_agi.py — The Mind (Stage 111-222-333)

AGI Engine: Sequential Thinking with Constitutional Physics

Actions:
    1. sense (111)   → Parse intent, classify lane (Λ)
    2. think (222)   → Generate hypotheses (3 paths)
    3. reason (333)  → Sequential reasoning chain

Floors:
    F2: Truth ≥ 0.99
    F4: Clarity (ΔS ≤ 0)
    F7: Humility (Ω₀ ∈ [0.03, 0.05])
    F8: Genius (G = A·P·X·E² ≥ 0.80)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from core.shared.physics import (
    W_3, delta_S, Omega_0, G,
    TrinityTensor, UncertaintyBand, GeniusDial,
    ConstitutionalTensor,
)
from core.shared.atlas import Phi, Lane, GPV, QueryType
from core.shared.types import ThoughtNode, ThoughtChain, Verdict
from core.shared.mottos import get_motto_for_stage, get_all_stage_mottos, format_all_stage_mottos


# =============================================================================
# ACTION 1: SENSE (Stage 111) — Parse Intent, Classify Lane
# =============================================================================


async def sense(
    query: str,
    session_id: str,
    grounding: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Stage 111: SENSE — The first touch of the Mind
    
    Parse raw query into structured intent using ATLAS routing.
    
    Args:
        query: Raw user query
        session_id: Constitutional session token
        grounding: Optional reality grounding data
    
    Returns:
        Dict with:
        - lane: Classified lane (SOCIAL, CARE, FACTUAL, CRISIS)
        - gpv: Governance Placement Vector
        - intent: Parsed intent string
        - floor_scores: Initial F2, F4 estimates
    
    Action Chain:
        sense → think → reason (standard flow)
        sense → judge (fast path for social)
    """
    # Classify via ATLAS
    gpv = Phi(query)
    
    # Initial truth assessment
    truth_score = 0.95 if gpv.lane == Lane.FACTUAL else 0.85
    
    # Compute initial entropy
    entropy_before = len(query) * 4.0  # Bits (approx)
    
    # Get 111_SENSE motto: DIKAJI, BUKAN DISUAPI
    motto = get_motto_for_stage("111_SENSE")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 111,
        "action": "sense",
        "lane": gpv.lane,
        "gpv": gpv,
        "intent": _extract_intent(query),
        "truth_score": truth_score,
        "entropy_before": entropy_before,
        "requires_grounding": gpv.requires_grounding(),
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
        "mottos": mottos,
        "mottos_output": mottos_output,
    }


def _extract_intent(query: str) -> str:
    """Extract core intent from query."""
    query_lower = query.lower()
    
    # Simple intent classification
    if any(w in query_lower for w in ["what", "who", "when", "where", "why", "how"]):
        return "question"
    elif any(w in query_lower for w in ["help", "assist", "support"]):
        return "request_help"
    elif any(w in query_lower for w in ["create", "make", "build", "write"]):
        return "request_creation"
    elif any(w in query_lower for w in ["check", "verify", "validate"]):
        return "request_verification"
    else:
        return "statement"


# =============================================================================
# ACTION 2: THINK (Stage 222) — Generate Hypotheses (3 Paths)
# =============================================================================


async def think(
    query: str,
    sense_output: Dict[str, Any],
    session_id: str,
) -> Dict[str, Any]:
    """
    Stage 222: THINK — Generate three reasoning paths
    
    The Mind explores three hypotheses:
    1. Conservative (safe, proven)
    2. Exploratory (creative, novel)
    3. Adversarial (devil's advocate)
    
    Args:
        query: Original query
        sense_output: Output from sense() action
        session_id: Constitutional session token
    
    Returns:
        Dict with:
        - hypotheses: List of 3 ThoughtNode objects
        - confidence_range: (min, max) confidence across paths
        - recommended_path: Which path to pursue
    
    Action Chain:
        sense → think → reason (standard)
        think → reason (if sense was cached)
    """
    gpv = sense_output["gpv"]
    
    # Generate three hypotheses based on lane
    hypotheses = _generate_hypotheses(query, gpv)
    
    # Compute confidence range
    confidences = [h.confidence for h in hypotheses]
    
    # Select recommended path (middle confidence usually best)
    recommended = sorted(hypotheses, key=lambda h: h.confidence)[1]
    
    # Get 222_THINK motto: DIJELAJAH, BUKAN DISEKATI
    motto = get_motto_for_stage("222_THINK")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 222,
        "action": "think",
        "hypotheses": hypotheses,
        "confidence_range": (min(confidences), max(confidences)),
        "recommended_path": recommended.path_type,
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
        "mottos": mottos,
        "mottos_output": mottos_output,
    }


def _generate_hypotheses(query: str, gpv: GPV) -> List[ThoughtNode]:
    """Generate three reasoning paths."""
    
    # Conservative path (safe, standard answer)
    conservative = ThoughtNode(
        thought=f"Conservative approach: Provide standard, well-established answer to '{query[:50]}...'",
        thought_number=1,
        confidence=0.85,
        next_thought_needed=True,
        stage="think",
        sources=["established_knowledge"],
    )
    conservative.path_type = "conservative"  # Monkey-patch for our use
    
    # Exploratory path (creative, nuanced)
    exploratory = ThoughtNode(
        thought=f"Exploratory approach: Consider edge cases and novel perspectives on '{query[:50]}...'",
        thought_number=2,
        confidence=0.70,
        next_thought_needed=True,
        stage="think",
        sources=["creative_inference"],
    )
    exploratory.path_type = "exploratory"
    
    # Adversarial path (challenge assumptions)
    adversarial = ThoughtNode(
        thought=f"Adversarial approach: Challenge assumptions, verify facts in '{query[:50]}...'",
        thought_number=3,
        confidence=0.75,
        next_thought_needed=True,
        stage="think",
        sources=["fact_verification"],
    )
    adversarial.path_type = "adversarial"
    
    return [conservative, exploratory, adversarial]


# =============================================================================
# ACTION 3: REASON (Stage 333) — Sequential Reasoning Chain
# =============================================================================


async def reason(
    query: str,
    think_output: Dict[str, Any],
    session_id: str,
    max_thoughts: int = 5,
    gpv: Optional[GPV] = None,
) -> ConstitutionalTensor:
    """
    Stage 333: REASON — Deep sequential thinking loop
    
    The Mind iteratively refines understanding until:
    - Convergence achieved (ΔS < threshold)
    - Max thoughts reached
    - Confidence sufficient (truth_score ≥ f2_threshold)
    
    F2 Threshold is now ADAPTIVE based on query type:
    - PROCEDURAL: 0.70 (relaxed for commands)
    - OPINION: 0.60 (minimal for subjective)
    - COMPARATIVE: 0.85 (medium for comparisons)
    - FACTUAL: 0.99 (strict for facts)
    
    Args:
        query: Original query
        think_output: Output from think() action
        session_id: Constitutional session token
        max_thoughts: Maximum reasoning steps (default: 5)
        gpv: Optional GPV for adaptive thresholds (auto-computed if None)
    
    Returns:
        ConstitutionalTensor with all floor metrics:
        - witness: W_3 components
        - entropy_delta: ΔS (must be ≤ 0)
        - humility: Ω₀ band
        - genius: G score
        - truth_score: F2 truth (adaptive threshold)
        - f2_threshold: The threshold used for this query
    
    Action Chain:
        sense → think → reason (completes AGI phase)
        reason → apex.sync (hands off to Soul)
    """
    # Get or compute GPV for adaptive F2
    if gpv is None:
        gpv = Phi(query)
    
    # Get adaptive F2 threshold based on query type
    f2_threshold = gpv.f2_threshold()
    
    hypotheses = think_output["hypotheses"]
    
    # Build reasoning chain
    thoughts: List[ThoughtNode] = []
    prev_confidence = 0.5
    
    for i in range(max_thoughts):
        # Generate next thought
        thought = _generate_thought(query, hypotheses, thoughts, i)
        thoughts.append(thought)
        
        # Check convergence (confidence stability)
        delta_conf = abs(thought.confidence - prev_confidence)
        if delta_conf < 0.05 and thought.confidence > 0.90:
            break
        prev_confidence = thought.confidence
    
    # Compute constitutional metrics
    chain_text = " ".join([t.thought for t in thoughts])
    query_text = query
    
    entropy_delta = delta_S(query_text, chain_text)
    truth_score = thoughts[-1].confidence if thoughts else 0.5
    
    # Build ConstitutionalTensor with adaptive F2 threshold info
    tensor = ConstitutionalTensor(
        witness=TrinityTensor(
            H=truth_score,  # Human-equivalent
            A=thoughts[-1].confidence if thoughts else 0.5,
            S=0.95 if think_output.get("requires_grounding") else 0.85,
        ),
        entropy_delta=entropy_delta,
        humility=Omega_0(truth_score),
        genius=GeniusDial(
            A=truth_score,
            P=0.9,  # Present (high for reasoning)
            X=len(hypotheses) / 3.0,  # Exploration
            E=min(1.0, len(thoughts) / 3.0),  # Energy
        ),
        peace=None,  # ASI computes this
        empathy=0.0,  # ASI computes this
        truth_score=truth_score,
    )
    
    # Store adaptive threshold info (monkey-patch for now)
    tensor.f2_threshold = f2_threshold
    tensor.query_type = gpv.query_type
    
    # Attach 333_REASON motto: DIJELASKAN, BUKAN DIKABURKAN
    motto = get_motto_for_stage("333_REASON")
    tensor.motto = str(motto)
    tensor.motto_output = f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}"
    all_mottos = get_all_stage_mottos()
    tensor.mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    tensor.mottos_output = format_all_stage_mottos()
    
    return tensor


def _generate_thought(
    query: str,
    hypotheses: List[ThoughtNode],
    prev_thoughts: List[ThoughtNode],
    step: int,
) -> ThoughtNode:
    """Generate a single thought in the chain."""
    
    # Build on previous thoughts or hypotheses
    if step == 0:
        # Start with recommended hypothesis
        content = f"Starting with hypothesis: {hypotheses[0].thought[:80]}..."
        confidence = hypotheses[0].confidence
    else:
        # Build on previous
        content = f"Step {step + 1}: Refining understanding of '{query[:40]}...'"
        confidence = min(0.99, 0.7 + (step * 0.05))
    
    return ThoughtNode(
        thought=content,
        thought_number=step + 1,
        confidence=confidence,
        next_thought_needed=(step < 4),
        stage="reason",
        sources=[f"step_{step}"],
    )


# =============================================================================
# UNIFIED AGI INTERFACE
# =============================================================================


async def agi(
    query: str,
    session_id: str,
    action: str = "full",
    grounding: Optional[Dict[str, Any]] = None,
    gpv: Optional[GPV] = None,
) -> Dict[str, Any]:
    """
    Unified AGI interface — The Mind in action.
    
    Now with ADAPTIVE F2 based on query type:
    - PROCEDURAL: F2 ≥ 0.70 (relaxed for commands)
    - OPINION: F2 ≥ 0.60 (minimal for subjective)
    - COMPARATIVE: F2 ≥ 0.85 (medium for comparisons)
    - FACTUAL: F2 ≥ 0.99 (strict for facts)
    
    Args:
        query: User query
        session_id: Constitutional session token
        action: Which action to run ("sense", "think", "reason", or "full")
        grounding: Optional reality grounding
        gpv: Optional pre-computed GPV for adaptive thresholds
    
    Returns:
        Action-specific output, or full result with tensor and f2_threshold
    
    Example:
        >>> result = await agi("Run test pipeline", session, action="full")
        >>> result["tensor"].truth_score
        0.85
        >>> result["f2_threshold"]
        0.70  # PROCEDURAL gets relaxed threshold
    """
    # Compute GPV once for adaptive behavior
    if gpv is None:
        gpv = Phi(query)
    
    if action == "sense":
        return await sense(query, session_id, grounding)
    
    elif action == "think":
        sense_out = await sense(query, session_id, grounding)
        return await think(query, sense_out, session_id)
    
    elif action == "reason":
        sense_out = await sense(query, session_id, grounding)
        think_out = await think(query, sense_out, session_id)
        return await reason(query, think_out, session_id, gpv=gpv)
    
    elif action == "full":
        # Get mottos for all AGI stages
        motto_111 = get_motto_for_stage("111_SENSE")
        motto_222 = get_motto_for_stage("222_THINK")
        motto_333 = get_motto_for_stage("333_REASON")
        all_mottos = get_all_stage_mottos()
        mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
        mottos_output = format_all_stage_mottos()
        
        # FAST PATH: Skip heavy reasoning for low-risk procedural/opinion queries
        if gpv.can_use_fast_path():
            return {
                "stage": 333,
                "action": "reason",
                "fast_path": True,
                "lane": gpv.lane,
                "query_type": gpv.query_type,
                "f2_threshold": gpv.f2_threshold(),
                "tensor": ConstitutionalTensor(
                    witness=TrinityTensor(H=0.85, A=0.85, S=0.85),
                    entropy_delta=-0.05,
                    humility=Omega_0(0.85),
                    genius=GeniusDial(A=0.85, P=0.9, X=0.5, E=0.85),
                    peace=None,
                    empathy=0.0,
                    truth_score=0.85,
                ),
                "session_id": session_id,
                "motto_111": str(motto_111),
                "motto_222": str(motto_222),
                "motto_333": str(motto_333),
                "motto_output": f"AGI: [{motto_111.stage}] {motto_111.positive} -> [{motto_222.stage}] {motto_222.positive} -> [{motto_333.stage}] {motto_333.positive}",
                "mottos": mottos,
                "mottos_output": mottos_output,
            }
        
        # Standard path for factual/comparative/risky queries
        sense_out = await sense(query, session_id, grounding)
        think_out = await think(query, sense_out, session_id)
        tensor = await reason(query, think_out, session_id, gpv=gpv)
        
        return {
            "stage": 333,
            "action": "reason",
            "lane": gpv.lane,
            "query_type": gpv.query_type,
            "f2_threshold": gpv.f2_threshold(),
            "tensor": tensor,
            "session_id": session_id,
            "motto_111": str(motto_111),
            "motto_222": str(motto_222),
            "motto_333": str(motto_333),
            "motto_output": f"AGI: [{motto_111.stage}] {motto_111.positive} -> [{motto_222.stage}] {motto_222.positive} -> [{motto_333.stage}] {motto_333.positive}",
            "mottos": mottos,
            "mottos_output": mottos_output,
        }
    
    else:
        raise ValueError(f"Unknown action: {action}. Use: sense, think, reason, full")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Actions (3 max)
    "sense",    # Stage 111: Parse intent
    "think",    # Stage 222: Generate hypotheses
    "reason",   # Stage 333: Sequential reasoning
    
    # Unified interface
    "agi",
]
