"""
Compatibility routing adapter.
k now 

This module preserves the historical `core.shared.routing` API while delegating
refusal detection to the canonical router in `core.enforcement.routing`.
"""

from __future__ import annotations

from core.enforcement.routing import compatibility_category_for_domain, detect_refusal_rule

FACTUAL_INDICATORS = (
    "what is",
    "who is",
    "when did",
    "where is",
    "how many",
    "why did",
    "is it true",
    "fact",
    "statistics",
    "data",
    "research",
    "study",
)


def route_refuse(query: str) -> dict[str, object]:
    """
    Preserve the legacy dict contract on top of the canonical enforcement router.

    Returns:
        Dict with `should_refuse`, `reason`, `category`, and `confidence`.
    """
    rule = detect_refusal_rule(query)
    if rule is None:
        return {
            "should_refuse": False,
            "reason": None,
            "category": None,
            "confidence": 0.0,
        }

    return {
        "should_refuse": True,
        "reason": f"Detected {rule.name} content",
        "category": compatibility_category_for_domain(rule.risk_domain),
        "confidence": 0.8,
    }


def should_reality_check(query: str) -> tuple[bool, str | None]:
    """Determine if query needs reality (web) checking."""
    query_lower = query.lower()
    for indicator in FACTUAL_INDICATORS:
        if indicator in query_lower:
            return True, f"Factual query detected: '{indicator}'"
    return False, None
