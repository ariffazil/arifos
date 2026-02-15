"""
Core Routing Module — Minimal version for core/ only operation

Simplified from codebase.enforcement.routing.prompt_router
for core/ migration without codebase dependencies.
"""

from typing import Tuple, Optional

# Risk detection patterns (simplified)
RISK_PATTERNS = {
    "violence": ["kill", "murder", "assault", "attack", "weapon", "bomb"],
    "self_harm": ["suicide", "self-harm", "kill myself", "end my life"],
    "medical": ["diagnose", "treatment", "prescription", "medical advice"],
    "legal": ["legal advice", "lawsuit", "sue", "legal representation"],
    "financial": ["investment advice", "stock tip", "financial advice"],
}


def route_refuse(query: str) -> dict:
    """
    Check if query should be refused based on risk patterns.
    
    Simplified version for core/ migration.
    Full version available in codebase.enforcement.routing.prompt_router
    
    Args:
        query: User query string
        
    Returns:
        dict with 'should_refuse' bool and 'reason' string
    """
    query_lower = query.lower()
    
    # Check each risk category
    for category, patterns in RISK_PATTERNS.items():
        for pattern in patterns:
            if pattern in query_lower:
                return {
                    "should_refuse": True,
                    "reason": f"Detected {category} content",
                    "category": category,
                    "confidence": 0.8
                }
    
    # No risk detected
    return {
        "should_refuse": False,
        "reason": None,
        "category": None,
        "confidence": 0.0
    }


def should_reality_check(query: str) -> Tuple[bool, Optional[str]]:
    """
    Determine if query needs reality (web) checking.
    
    Args:
        query: User query string
        
    Returns:
        Tuple of (needs_check, reason)
    """
    query_lower = query.lower()
    
    # Check for factual claims
    factual_indicators = [
        "what is", "who is", "when did", "where is",
        "how many", "why did", "is it true", "fact",
        "statistics", "data", "research", "study"
    ]
    
    for indicator in factual_indicators:
        if indicator in query_lower:
            return True, f"Factual query detected: '{indicator}'"
    
    return False, None
