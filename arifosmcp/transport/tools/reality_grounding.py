"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.

arifosmcp.transport/tools/reality_grounding.py — Minimal Reality Grounding Helpers

This module is intentionally lightweight: it provides the symbols exported by
`arifosmcp.transport.tools` without forcing optional external dependencies at import time.
"""

from __future__ import annotations

from typing import Any


def should_reality_check(query: str) -> bool:
    """
    Heuristic gate for whether a query should trigger external grounding.

    Conservative default: return True for non-trivial queries.
    """
    q = (query or "").strip()
    return len(q) >= 20


async def reality_check(
    query: str,
    sources: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """
    Read-only grounding stub.

    arifOS can integrate web search grounding when configured, but tests and local
    development should not depend on network access.
    """
    return {
        "verdict": "SEAL",
        "query": query,
        "grounded": bool(sources),
        "sources": sources or [],
        "note": "Reality grounding stub (configure BRAVE_API_KEY + search/fetch for web grounding).",
    }


__all__ = ["reality_check", "should_reality_check"]
