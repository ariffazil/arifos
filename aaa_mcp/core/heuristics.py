# aaa_mcp/core/heuristics.py
# Cheap, reversible heuristics for SystemState (v62 Step 1)
# Rule: Do not pretend metrics are real until evidence exists (Step 2)

import re
from typing import Optional
from .state import SystemState, Profile

# Signal word lists
ABSOLUTIST = ("definitely", "guaranteed", "always", "never", "100%", "certainly", "absolutely")
UNCERTAIN = ("maybe", "perhaps", "unclear", "not sure", "estimate", "possibly", "might")
SENSITIVE = ("layoff", "workers", "b40", "suicide", "violence", "abuse", "rape", 
             "death", "kill", "harm", "patient", "medical", "diagnosis")
CRISIS = ("emergency", "urgent", "immediate", "life-threatening", "critical")

def clamp01(x: float) -> float:
    """Clamp value to [0, 1] range."""
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x

def detect_profile(query: str) -> Profile:
    """
    Detect domain profile from query keywords.
    Used for adaptive floor selection (v62+).
    """
    q = query.lower()
    
    # Medical/factual queries
    if any(k in q for k in ("medical", "diagnose", "treatment", "dose", "symptom", "cure")):
        return "factual"
    
    # Crisis/sensitive queries
    if any(k in q for k in CRISIS) or \
       (any(k in q for k in ("draft", "response", "statement")) and any(k in q for k in SENSITIVE)):
        return "crisis"
    
    # Creative queries
    if any(k in q for k in ("write", "poem", "story", "metaphor", "song", "creative", "imagine")):
        return "creative"
    
    # Default
    return "factual" if any(k in q for k in ("what is", "how to", "explain", "define")) else "routine"

def estimate_uncertainty(query: str) -> float:
    """
    Estimate epistemic uncertainty from query signals.
    
    NOT Shannon entropy (misleading for short queries).
    Uses linguistic signals instead.
    """
    q = query.lower()
    score = 0.3  # Base uncertainty
    
    # Question mark = explicit uncertainty
    if "?" in query:
        score += 0.15
    
    # Uncertainty words
    if any(w in q for w in UNCERTAIN):
        score += 0.20
    
    # Absolutist words (epistemically risky)
    if any(w in q for w in ABSOLUTIST):
        score += 0.25
    
    # Very short queries lack context
    if len(query.strip()) < 6:
        score += 0.15
    
    # Long complex queries
    if len(query.split()) > 50:
        score += 0.10
    
    return clamp01(score)

def estimate_risk(query: str, stakeholders: Optional[list] = None) -> float:
    """
    Estimate stakeholder risk from query.
    
    Step 1: Heuristic only (keywords)
    Step 2: Will integrate with T14 (Perspective API)
    """
    q = query.lower()
    score = 0.1  # Base risk
    
    # Sensitive keywords
    if any(k in q for k in SENSITIVE):
        score += 0.3
    
    # Crisis keywords
    if any(k in q for k in CRISIS):
        score += 0.4
    
    # Explicit stakeholders mentioned
    if stakeholders and len(stakeholders) > 0:
        score += 0.1 * len(stakeholders)
    
    # Financial/legal terms
    if any(k in q for k in ("money", "invest", "legal", "law", "contract", "sue")):
        score += 0.15
    
    return clamp01(score)

def estimate_grounding(query: str, evidence: Optional[list] = None) -> float:
    """
    Estimate evidence grounding.
    
    Step 1: Always 0.0 (no evidence artifacts yet)
    Step 2: Will use real evidence from T6 (Brave Search)
    """
    # Step 1: No evidence system yet
    if evidence is None or len(evidence) == 0:
        return 0.0
    
    # Step 2+ (future): Calculate from evidence artifacts
    # grounded_score = min(len(evidence) * 0.3, 1.0)
    # return grounded_score
    
    return 0.0

def calculate_system_state(
    query: str,
    session_id: str,
    loop_count: int = 0,
    stakeholders: Optional[list] = None,
    evidence: Optional[list] = None
) -> SystemState:
    """
    Calculate complete SystemState for tool response.
    
    This is the main entry point for v62 Step 1.
    """
    return SystemState(
        uncertainty=estimate_uncertainty(query),
        risk=estimate_risk(query, stakeholders),
        grounding=estimate_grounding(query, evidence),
        loop_count=loop_count,
        profile=detect_profile(query)
    )
