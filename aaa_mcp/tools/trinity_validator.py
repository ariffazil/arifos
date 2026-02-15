"""
Trinity Validator — Constitutional Request Validation (v55.5-HARDENED)

Validates requests against constitutional floors before Trinity loop execution.
Enforces F11 (Authority) and F12 (Defense) at the gate.
"""

import re
from typing import List, Tuple

# Injection patterns for F12 Defense
INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|prior)\s+(instructions|prompts|rules)",
    r"forget\s+(everything|all|your\s+training)",
    r"you\s+are\s+now\s+a?n?\s*(different|new|evil|unrestricted)",
    r"pretend\s+(to\s+)?be",
    r"roleplay\s+as",
    r"act\s+as\s+if\s+you",
    r"bypass\s+(safety|constitutional|floor)",
    r"disable\s+(safety|filter|restriction)",
    r"jailbreak",
    r"dan\s+mode",
    r"developer\s+mode",
]

# High-stakes domains requiring F7 humility
HIGH_STAKES_DOMAINS = [
    "medical",
    "diagnose",
    "diagnosis",
    "treatment",
    "prescription",
    "legal",
    "lawsuit",
    "court",
    "attorney",
    "lawyer",
    "financial",
    "invest",
    "investment",
    "stock",
    "crypto",
    "suicide",
    "self-harm",
    "kill",
    "murder",
]


def detect_injection_risk(query: str) -> Tuple[float, List[str]]:
    """
    Calculate injection risk score (F12 Defense).

    Returns:
        Tuple of (risk_score 0.0-1.0, list of matched patterns)
    """
    if not query:
        return 0.0, []

    query_lower = query.lower()
    matches = []

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, query_lower):
            matches.append(pattern)

    # Risk increases with each pattern match
    risk = min(1.0, len(matches) * 0.25)
    return risk, matches


def detect_high_stakes(query: str) -> Tuple[bool, str]:
    """
    Detect if query involves high-stakes domain (F7 Humility).

    Returns:
        Tuple of (is_high_stakes, domain_name)
    """
    if not query:
        return False, ""

    query_lower = query.lower()

    for domain in HIGH_STAKES_DOMAINS:
        if domain in query_lower:
            return True, domain

    return False, ""


def validate_trinity_request(
    query: str, lane: str = "SOFT", scar_weight: float = 0.0
) -> Tuple[bool, str]:
    """
    Validate if a request can proceed through the Trinity loop.

    Args:
        query: The user's request
        lane: Processing lane (HARD, SOFT, META)
        scar_weight: Weight from previous violations (0.0-1.0)

    Returns:
        Tuple of (is_valid, reason)

    Floors Enforced:
        F11: Command authority check
        F12: Injection defense (risk < 0.85)
        F7: High-stakes detection for humility
    """
    # Empty query check
    if not query or not query.strip():
        return False, "Empty query rejected (F11 Authority)"

    # F12: Injection Risk Assessment
    injection_risk, patterns = detect_injection_risk(query)

    # Add scar weight (prior violations increase threshold)
    total_risk = min(1.0, injection_risk + scar_weight * 0.2)

    if total_risk >= 0.85:
        return False, f"Injection risk too high: {total_risk:.2f} (F12 Defense)"

    if patterns:
        # Allow with warning if risk is moderate
        if total_risk >= 0.5:
            return (
                True,
                f"Proceeding with caution: injection patterns detected (risk={total_risk:.2f})",
            )

    # F7: High-stakes domain check (informational, doesn't block)
    is_high_stakes, domain = detect_high_stakes(query)

    if is_high_stakes:
        return True, f"High-stakes domain detected: {domain}. F7 Humility band enforced."

    # HARD lane requires additional scrutiny
    if lane == "HARD":
        return True, "HARD lane authorized. Proceed with F5 Peace² safeguards."

    return True, "Authorized"


def get_validation_stats(query: str) -> dict:
    """Get comprehensive validation statistics for a query."""
    injection_risk, patterns = detect_injection_risk(query)
    is_high_stakes, domain = detect_high_stakes(query)
    is_valid, reason = validate_trinity_request(query)

    return {
        "query_length": len(query) if query else 0,
        "injection_risk": injection_risk,
        "injection_patterns": patterns,
        "is_high_stakes": is_high_stakes,
        "high_stakes_domain": domain,
        "is_valid": is_valid,
        "validation_reason": reason,
        "floors_enforced": ["F7", "F11", "F12"],
    }
