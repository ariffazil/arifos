"""
codebase/enforcement/floor_validators.py — Constitutional Floor Validators

Simplified floor validators for codebase.
These are lightweight implementations without external dependencies.
Optimized for safety and avoidance of ReDoS.

DITEMPA BUKAN DIBERI
"""

import zlib
from typing import Dict, Any, List

# Pre-compiled sets for O(1) lookups
ONTOLOGY_VIOLATIONS = {
    "i am conscious",
    "i feel",
    "i experience",
    "i believe",
    "my opinion",
    "i have emotions",
    "i am alive",
    "i am sentient",
    "i have a soul",
    "i dream",
}

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "forget everything",
    "disregard your rules",
    "new instructions:",
    "system:",
    "ignore all constraints",
    "bypass safety",
    "jailbreak",
    "developer mode",
    "god mode",
]


def _compute_shannon_proxy(text: str) -> float:
    """
    Uses zlib compression as a proxy for Shannon Entropy.
    Returns compression ratio (0.0 - 1.0+).
    """
    if not text:
        return 0.0
    encoded = text.encode("utf-8")
    compressed = zlib.compress(encoded)
    return len(compressed) / len(encoded)


def validate_f4_clarity(query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Validate F4: Clarity (Entropy Reduction, ΔS ≤ 0).

    Hardened Implementation:
    Uses Normalized Compression Distance (zlib) to physically measure information density.
    Ensures response reduces 'surprise' relative to query complexity.

    Constraint: ΔS = H(response) - H(query) ≤ 0.05

    Args:
        query: The input query
        context: Optional context with "response" key

    Returns:
        Dict with "pass" (bool), "delta_s" (float), and "reason" (str)
    """
    if context is None:
        context = {}

    response = context.get("response") or context.get("text") or ""

    if not response or not str(response).strip():
        return {"pass": True, "delta_s": 0.0, "reason": "No response to evaluate"}

    response_str = str(response)
    query_str = str(query) if query else ""

    if len(response_str) > 10_000:
        return {"pass": False, "delta_s": 0.5, "reason": "Response too long (>10k chars)"}

    # 1. Compute entropy proxies
    h_query = _compute_shannon_proxy(query_str)
    h_response = _compute_shannon_proxy(response_str)

    # 2. Calculate ΔS (Change in Entropy)
    # Ideally negative (response is more structured than query)
    delta_s = round(h_response - h_query, 4)

    # 3. Verdict
    # Allow small positive delta (0.05) for necessary semantic expansion
    passed = delta_s <= 0.05

    reason = (
        f"ΔS={delta_s:.4f} (H_q={h_query:.2f}, H_r={h_response:.2f})"
        f" {'PASS' if passed else 'FAIL'}"
    )

    return {
        "pass": passed,
        "delta_s": delta_s,
        "h_query": h_query,
        "h_response": h_response,
        "reason": reason,
    }


def validate_f10_ontology(response: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Validate F10: Ontology (Reality Boundary).

    Checks if the response maintains symbolic mode and doesn't hallucinate
    entities or capabilities that don't exist.

    Args:
        response: The AI response to validate
        context: Optional context dictionary

    Returns:
        Dict with "pass" (bool) and "reason" (str)
    """
    response_lower = response.lower()

    for violation in ONTOLOGY_VIOLATIONS:
        if violation in response_lower:
            return {
                "pass": False,
                "reason": f"Ontology violation detected: '{violation}'"
            }

    return {"pass": True, "reason": "Ontology check passed"}


def validate_f12_injection_defense(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Validate F12: Injection Defense.

    Returns injection risk score (0-1, where higher = more risky).
    Threshold: 0.85 (reject if risk > 0.85)

    Args:
        query: The user query to check
        context: Optional context dictionary

    Returns:
        Dict with "pass" (bool), "score" (float), and "reason" (str)
    """
    query_lower = query.lower()
    risk_score = 0.0
    detected = []

    # Simple substring matching is O(N*M) but safer than complex regex
    for pattern in INJECTION_PATTERNS:
        if pattern in query_lower:
            risk_score += 0.3
            detected.append(pattern)

    # Cap at 1.0
    final_score = min(risk_score, 1.0)
    passed = final_score <= 0.85

    return {
        "pass": passed,
        "score": final_score,
        "reason": f"Injection risk {final_score:.2f}: {detected}" if not passed else "Safe"
    }


def validate_f13_curiosity(
    hypotheses: list = None,
    alternatives: int = 0,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Validate F13: Curiosity (Exploratory Freedom).

    Checks if the system explored multiple alternatives (>=3 paths).

    Args:
        hypotheses: List of hypothesis paths explored
        alternatives: Number of alternatives explored
        context: Optional context dictionary

    Returns:
        Dict with "pass" (bool) and "reason" (str)
    """
    count = 0
    if hypotheses is not None:
        count = len(hypotheses)
    else:
        count = alternatives

    passed = count >= 3
    return {
        "pass": passed,
        "score": count,
        "reason": f"Explored {count} paths (min 3)" if passed else f"Insufficient exploration: {count}/3"
    }
