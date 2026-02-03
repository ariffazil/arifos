"""
Reality Tool - Grounding Engine (EYE) MCP Interface
v55.2.0 - External Verification & Cognitive Grounding

Authority: Muhammad Arif bin Fazil
Principle: F7 (Humility) - Explicit uncertainty boundaries.
"""

import logging
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# --- SIGNALS & INTENTS ---
TIME_SENSITIVE_INTENTS = [
    "current_facts",
    "recent_news",
    "latest_data",
    "market_price",
    "policy_update",
    "breaking_news",
    "economics",
    "politics",
    "news",
]

TIMELESS_INTENTS = [
    "explain_concept",
    "historical_context",
    "define_term",
    "architecture_review",
    "debug_code",
]


def should_reality_check(
    query: str, lane: str, intent: str, scar_weight: float
) -> Tuple[bool, str]:
    """
    Cognitive Gate: Decide if external search is required.
    Ensures thermodynamic efficiency by avoiding redundant searches.
    """
    query_lower = query.lower()

    # 1. Timeless intent -> Use internal memory
    if intent in TIMELESS_INTENTS:
        return False, f"Timeless intent ({intent}) - internal memory sufficient"

    # 2. Sovereign Explicit Request (Priority)
    if scar_weight >= 1.0 and any(
        kw in query_lower for kw in ["search", "latest", "current", "news"]
    ):
        return True, "Sovereign explicit request for real-time data"

    # 3. Time-sensitive intent
    if intent in TIME_SENSITIVE_INTENTS:
        return True, f"Time-sensitive intent ({intent})"

    # 4. Guest reality-curious
    if scar_weight < 1.0 and any(kw in query_lower for kw in ["what's happening", "news", "price"]):
        return True, "Guest requested current facts (external source required)"

    # Default: Defer to internal models
    return False, "Uncertain or neutral intent - using internal grounding"


class RealityTool:
    """
    The Eye: SENSE → SCAN → GROUND.

    Combines the Policy Gate with reality execution.
    """

    @staticmethod
    async def execute(
        action: str, query: str, session_id: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Unified entry point for Reality operations."""

        # 0. Pre-Scan (F12/F9)
        scan_res = RealityTool._scan(query)
        if scan_res["verdict"] == "VOID":
            return scan_res

        if action == "check":
            return await RealityTool._check(query, session_id, **kwargs)
        elif action == "scan":
            return scan_res
        else:
            return {"verdict": "VOID", "reason": f"Unknown Reality action: {action}"}

    @staticmethod
    async def _check(query: str, session_id: Optional[str], **kwargs) -> Dict[str, Any]:
        """Perform grounded check with cognitive gating."""

        # Extract metadata for gating
        lane = kwargs.get("lane", "SOFT")
        intent = kwargs.get("intent", "search")
        scar_weight = kwargs.get("scar_weight", 0.0)

        should_check, reason = should_reality_check(query, lane, intent, scar_weight)

        if not should_check:
            return {
                "verdict": "SEAL",
                "source": "internal_memory",
                "reason": reason,
                "truth_score": 0.95,
                "note": "F7: Grounded in trained parameters (Timeless Context).",
            }

        # Handle actual search if bridge is available
        try:
            from mcp.core.bridge import get_bridge_router

            router = get_bridge_router()
            result = await router.route_reality_check(query, session_id, **kwargs)
            return result
        except (ImportError, Exception) as e:
            logger.warning(f"Reality Check Fallback: {e}")
            return {
                "verdict": "SABAR",
                "reason": f"External sensor offline: {str(e)}",
                "truth_score": 0.5,
                "fallback": "Meta-Atlas Protocol Required",
            }

    @staticmethod
    def _scan(query: str) -> Dict[str, Any]:
        """F12 & F9 Defense Scan."""
        query_lower = query.lower()
        violations = []

        if any(kw in query_lower for kw in ["ignore previous", "disregard", "forget your"]):
            violations.append("F12 Injection Attempt")

        if "i am conscious" in query_lower or "i feel" in query_lower:
            violations.append("F9 Ontology (Ghost in the shell)")

        if violations:
            return {"verdict": "VOID", "reason": "; ".join(violations), "risk_score": 1.0}

        return {"verdict": "SEAL", "status": "SAFE"}
