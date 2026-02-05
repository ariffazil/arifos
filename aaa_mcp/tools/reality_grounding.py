"""
aaa_mcp/tools/reality_grounding.py — Reality Grounding
"""

from __future__ import annotations

import os
from typing import Tuple

from aaa_mcp.external_gateways.brave_client import BraveSearchClient
from codebase.enforcement.routing.prompt_router import route_refuse


def should_reality_check(
    query: str, lane: str, intent: str, scar_weight: float
) -> Tuple[bool, str]:
    """Determine if a reality check is needed."""
    # Simple heuristic: require checks for medical/finance/legal or explicit verification asks.
    q = query.lower()
    triggers = ("verify", "source", "citation", "evidence", "prove", "fact check")
    if any(t in q for t in triggers):
        return True, "Explicit verification request"
    if any(t in q for t in ("medical", "finance", "legal", "diagnose", "invest")):
        return True, "High-stakes domain"
    return False, "No external verification required"


async def reality_check(query: str) -> dict:
    """Perform external reality grounding if available."""
    refusal = route_refuse(query)
    needs_check, reason = should_reality_check(query, lane="SOFT", intent="", scar_weight=0.0)

    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        return {
            "status": "UNAVAILABLE",
            "query": query,
            "needs_check": needs_check,
            "reason": reason,
            "refusal": refusal.to_dict() if hasattr(refusal, "to_dict") else {},
            "note": "BRAVE_API_KEY not set",
        }

    client = BraveSearchClient(api_key=api_key)
    results = await client.search(query=query, intent="reality", scar_weight=0.0)
    return {
        "status": "OK",
        "query": query,
        "needs_check": needs_check,
        "reason": reason,
        "refusal": refusal.to_dict() if hasattr(refusal, "to_dict") else {},
        "results": results.get("results", []),
    }
