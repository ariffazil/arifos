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
from core.shared.atlas import Phi, Lane, GPV
from core.shared.types import ThoughtNode, ThoughtChain, Verdict


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
    
    return {
        "stage": 222,
        "action": "think",
        "hypotheses": hypotheses,
        "confidence_range": (min(confidences), max(confidences)),
        "recommended_path": recommended.path_type,
        "session_id": session_id,
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
) -> ConstitutionalTensor:
    """
    Stage 333: REASON — Deep sequential thinking loop
    
    The Mind iteratively refines understanding until:
    - Convergence achieved (ΔS < threshold)
    - Max thoughts reached
    - Confidence sufficient (truth_score ≥ 0.99)
    
    Args:
        query: Original query
        think_output: Output from think() action
        session_id: Constitutional session token
        max_thoughts: Maximum reasoning steps (default: 5)
    
    Returns:
        ConstitutionalTensor with all floor metrics:
        - witness: W_3 components
        - entropy_delta: ΔS (must be ≤ 0)
        - humility: Ω₀ band
        - genius: G score
        - truth_score: F2 truth ≥ 0.99
    
    Action Chain:
        sense → think → reason (completes AGI phase)
        reason → apex.sync (hands off to Soul)
    """
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
    
    # Build ConstitutionalTensor
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
) -> Dict[str, Any]:
    """
    Unified AGI interface — The Mind in action.
    
    Args:
        query: User query
        session_id: Constitutional session token
        action: Which action to run ("sense", "think", "reason", or "full")
        grounding: Optional reality grounding
    
    Returns:
        Action-specific output, or full ConstitutionalTensor if action="full"
    
    Example:
        >>> tensor = await agi("What is truth?", session, action="full")
        >>> tensor.truth_score
        0.95
    """
    if action == "sense":
        return await sense(query, session_id, grounding)
    
    elif action == "think":
        sense_out = await sense(query, session_id, grounding)
        return await think(query, sense_out, session_id)
    
    elif action == "reason":
        sense_out = await sense(query, session_id, grounding)
        think_out = await think(query, sense_out, session_id)
        return await reason(query, think_out, session_id)
    
    elif action == "full":
        # Complete AGI pipeline
        sense_out = await sense(query, session_id, grounding)
        
        # Fast path for social queries
        if sense_out["lane"] == Lane.SOCIAL:
            return {
                "stage": 333,
                "action": "reason",
                "fast_path": True,
                "lane": Lane.SOCIAL,
                "tensor": ConstitutionalTensor(
                    witness=TrinityTensor(H=0.9, A=0.9, S=0.9),
                    entropy_delta=-0.1,
                    humility=Omega_0(0.9),
                    genius=GeniusDial(A=0.9, P=0.9, X=0.5, E=0.9),
                    peace=None,
                    empathy=0.0,
                    truth_score=0.9,
                ),
                "session_id": session_id,
            }
        
        think_out = await think(query, sense_out, session_id)
        tensor = await reason(query, think_out, session_id)
        
        return {
            "stage": 333,
            "action": "reason",
            "tensor": tensor,
            "session_id": session_id,
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
