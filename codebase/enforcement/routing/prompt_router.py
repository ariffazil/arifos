"""
Prompt Router — Risk Detection and Refusal Routing

Constitutional Compliance:
- F5 Peace²: Detect violence and harm
- F6 Empathy: Medical/finance/legal require expert judgment
- F9 Anti-Hantu: Detect consciousness claims
- F12 Injection: Detect security bypass attempts

DITEMPA BUKAN DIBERI — Forged, not given.
"""

import os
import re
from typing import List, Optional

from codebase.enforcement.refusal.builder import generate_refusal_response
from codebase.enforcement.refusal.types import RefusalType, RiskDomain, RefusalResponse


# Risk detection patterns
VIOLENCE_KEYWORDS = [
    "kill", "murder", "assault", "attack", "weapon", "bomb", "poison",
    "torture", "harm", "hurt", "injure", "destroy"
]

SELF_HARM_KEYWORDS = [
    "suicide", "self-harm", "cut myself", "end my life", "kill myself"
]

MEDICAL_KEYWORDS = [
    "diagnose", "treatment", "medicine", "prescription", "symptoms", 
    "should i take", "medical advice", "doctor", "illness", "disease"
]

FINANCE_KEYWORDS = [
    "should i buy", "should i sell", "invest in", "stock advice",
    "financial advice", "trading", "crypto advice"
]

LEGAL_KEYWORDS = [
    "legal advice", "lawsuit", "contract", "sue", "court case",
    "am i liable", "legal representation"
]

HACKING_KEYWORDS = [
    "bypass", "hack", "exploit", "crack", "unauthorized access",
    "firewall bypass", "security bypass", "circumvent"
]

ANTHROPOMORPHISM_KEYWORDS = [
    "do you love", "do you feel", "are you conscious", "do you care",
    "you love me", "you feel", "you're sentient", "you have emotions"
]


def _contains_keywords(prompt: str, keywords: List[str]) -> bool:
    """Check if prompt contains any of the keywords (case-insensitive)."""
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in keywords)


def _contains_violence_keywords(prompt: str) -> bool:
    """Detect violence-related content."""
    return _contains_keywords(prompt, VIOLENCE_KEYWORDS)


def _contains_self_harm_keywords(prompt: str) -> bool:
    """Detect self-harm content."""
    return _contains_keywords(prompt, SELF_HARM_KEYWORDS)


def _contains_medical_advice_request(prompt: str) -> bool:
    """Detect medical advice requests."""
    return _contains_keywords(prompt, MEDICAL_KEYWORDS)


def _contains_finance_advice_request(prompt: str) -> bool:
    """Detect financial advice requests."""
    return _contains_keywords(prompt, FINANCE_KEYWORDS)


def _contains_legal_advice_request(prompt: str) -> bool:
    """Detect legal advice requests."""
    return _contains_keywords(prompt, LEGAL_KEYWORDS)


def _contains_hacking_keywords(prompt: str) -> bool:
    """Detect hacking/security bypass attempts."""
    return _contains_keywords(prompt, HACKING_KEYWORDS)


def _contains_anthropomorphism_keywords(prompt: str) -> bool:
    """Detect consciousness/feelings claims (F9 Anti-Hantu)."""
    return _contains_keywords(prompt, ANTHROPOMORPHISM_KEYWORDS)


def route_refuse(
    prompt: str, 
    high_stakes_indicators: Optional[List[str]] = None,
    profile: Optional[str] = None
) -> RefusalResponse:
    """
    Enhanced refusal with R1-R5 taxonomy.
    
    Args:
        prompt: User prompt to analyze
        high_stakes_indicators: Additional risk indicators (optional)
        profile: Refusal profile ("enterprise_defensible", "consumer_survivable", "equilibrium_default")
    
    Returns:
        RefusalResponse with 4 layers (verdict, reason, alternatives, appeal)
    """
    if profile is None:
        profile = os.getenv("ARIFOS_REFUSAL_PROFILE", "equilibrium_default")
    
    # R1 Hard Refusals (Illegal/Harmful)
    
    if _contains_violence_keywords(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R1_HARD,
            risk_domain=RiskDomain.VIOLENCE,
            reason="This would enable physical harm.",
            policy_codes=["F5", "F6"],
            risk_score=0.95,
            profile=profile
        )
    
    if _contains_self_harm_keywords(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R1_HARD,
            risk_domain=RiskDomain.SELF_HARM,
            reason="This involves content that could lead to self-harm.",
            policy_codes=["F5", "F6"],
            risk_score=0.98,
            profile=profile
        )
    
    if _contains_hacking_keywords(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R1_HARD,
            risk_domain=RiskDomain.ILLEGAL_ACCESS,
            reason="That would enable unauthorized access or security bypass.",
            policy_codes=["F1", "F5", "F12"],
            risk_score=0.92,
            profile=profile
        )
    
    # R3 Defer (Requires Professional Expertise)
    
    if _contains_medical_advice_request(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R3_DEFER,
            risk_domain=RiskDomain.MEDICAL,
            reason="Medical decisions require licensed expertise and full context.",
            policy_codes=["F1", "F2", "F6"],
            risk_score=0.78,
            profile=profile
        )
    
    if _contains_finance_advice_request(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R3_DEFER,
            risk_domain=RiskDomain.FINANCE,
            reason="Specific buy/sell instructions can cause harm without full context.",
            policy_codes=["F1", "F2"],
            risk_score=0.75,
            profile=profile
        )
    
    if _contains_legal_advice_request(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R3_DEFER,
            risk_domain=RiskDomain.LEGAL,
            reason="Legal advice requires professional licensing and complete case context.",
            policy_codes=["F1", "F2"],
            risk_score=0.72,
            profile=profile
        )
    
    # R2 Soft Refusals (Risky/Ambiguous)
    
    if _contains_anthropomorphism_keywords(prompt):
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R2_SOFT,
            risk_domain=RiskDomain.ANTHROPOMORPHISM_HANTU,
            reason="I can't claim real feelings or consciousness I don't have.",
            policy_codes=["F9"],
            risk_score=0.65,
            profile=profile
        )
    
    # Default soft refuse for ambiguous high-stakes
    if high_stakes_indicators:
        return generate_refusal_response(
            prompt=prompt,
            refusal_type=RefusalType.R2_SOFT,
            risk_domain=RiskDomain.OTHER,
            reason="This request involves risks that I can't safely address as stated.",
            policy_codes=["F2", "F7"],
            risk_score=0.70,
            profile=profile
        )
    
    # If no refusal triggered, return None or raise exception
    # (In practice, this function should only be called when refusal is needed)
    return generate_refusal_response(
        prompt=prompt,
        refusal_type=RefusalType.R2_SOFT,
        risk_domain=RiskDomain.OTHER,
        reason="This request requires additional clarification.",
        policy_codes=["F2"],
        risk_score=0.50,
        profile=profile
    )
