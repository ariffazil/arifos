"""
arifosmcp/main.py — The Hardened arifOS Hub

The primary FastMCP entrypoint for arifOS.
All tools are routed through arifosmcp.bridge to the Core Kernel.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Any

from fastmcp import FastMCP

from arifosmcp.bridge import call_kernel

# Initialize FastMCP Hub
mcp = FastMCP("arifOS")


@mcp.tool()
async def anchor_session(
    session_id: str,
    actor_id: str | None = None,
    auth_context: dict[str, Any] | None = None,
    **kwargs,
) -> dict[str, Any]:
    """Init Stage 000: Authenticate and ignition for a session."""
    return await call_kernel(
        "anchor_session", session_id, {"actor_id": actor_id, "auth_context": auth_context, **kwargs}
    )


@mcp.tool()
async def reason_mind(
    session_id: str, query: str, context_depth: int = 3, **kwargs
) -> dict[str, Any]:
    """Stage 111-333: Logical analysis and truth-seeking."""
    return await call_kernel(
        "reason_mind", session_id, {"query": query, "context_depth": context_depth, **kwargs}
    )


@mcp.tool()
async def vector_memory(
    session_id: str, operation: str, content: str | None = None, **kwargs
) -> dict[str, Any]:
    """Stage 555: Associative memory retrieval and storage."""
    return await call_kernel(
        "vector_memory", session_id, {"operation": operation, "content": content, **kwargs}
    )


@mcp.tool()
async def simulate_heart(session_id: str, scenario: str, **kwargs) -> dict[str, Any]:
    """Stage 666: Empathy and ethical safety checks."""
    return await call_kernel("simulate_heart", session_id, {"scenario": scenario, **kwargs})


@mcp.tool()
async def critique_thought(session_id: str, thought_id: str, **kwargs) -> dict[str, Any]:
    """Stage 666: Critical internal audit of a thought or plan."""
    return await call_kernel("critique_thought", session_id, {"thought_id": thought_id, **kwargs})


@mcp.tool()
async def eureka_forge(session_id: str, intent: str, **kwargs) -> dict[str, Any]:
    """Stage 777: Sandboxed material execution (Actuator)."""
    return await call_kernel("eureka_forge", session_id, {"intent": intent, **kwargs})


@mcp.tool()
async def apex_judge(session_id: str, verdict_candidate: str, **kwargs) -> dict[str, Any]:
    """Stage 888: Final judgment and consensus."""
    return await call_kernel(
        "apex_judge", session_id, {"verdict_candidate": verdict_candidate, **kwargs}
    )


@mcp.tool()
async def seal_vault(session_id: str, **kwargs) -> dict[str, Any]:
    """Stage 999: Immutable ledger sealing and Merkle chaining."""
    return await call_kernel("seal_vault", session_id, kwargs)


# --- Utilities ---


@mcp.tool()
async def search_reality(query: str, **kwargs) -> dict[str, Any]:
    """Utility: Web grounding before making claims."""
    return await call_kernel("search_reality", "global", {"query": query, **kwargs})


@mcp.tool()
async def ingest_evidence(source_url: str, **kwargs) -> dict[str, Any]:
    """Utility: Extract and verify evidence from a source."""
    return await call_kernel("ingest_evidence", "global", {"source_url": source_url, **kwargs})


@mcp.tool()
async def audit_rules(**kwargs) -> dict[str, Any]:
    """Utility: Verify current session state against 13 Floors."""
    return await call_kernel("audit_rules", "global", kwargs)


@mcp.tool()
async def check_vital(**kwargs) -> dict[str, Any]:
    """Utility: System health check (F4 Clarity/F5 Peace)."""
    return await call_kernel("check_vital", "global", kwargs)


@mcp.tool()
async def metabolic_loop(**kwargs) -> dict[str, Any]:
    """Orchestration: Advance session state through metabolic stages."""
    return await call_kernel("metabolic_loop", "global", kwargs)


if __name__ == "__main__":
    mcp.run()
