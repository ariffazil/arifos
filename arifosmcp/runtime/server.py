"""
arifosmcp/runtime/server.py — The Hardened arifOS Hub

CANONICAL EXTERNAL ENTRYPOINT for the arifOS MCP surface.
All tool calls are passed through the Harden Bridge to the Core Kernel.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Any

from fastmcp import FastMCP

from arifosmcp.bridge import call_kernel
from arifosmcp.intelligence.mcp_bridge import register_aclip_tools

# Initialize Hub
mcp = FastMCP("arifOS")

# Register ACLIP Senses (Sensory Tools)
register_aclip_tools(mcp)


def create_aaa_mcp_server() -> FastMCP:
    return mcp


@mcp.tool()
async def anchor_session(
    query: str, actor_id: str | None = "anonymous", auth_token: str | None = None, **kwargs
) -> dict[str, Any]:
    """Init Stage 000: Authenticate and ignition for a session."""
    return await call_kernel(
        "anchor_session",
        "global",
        {"query": query, "actor_id": actor_id, "auth_token": auth_token, **kwargs},
    )


@mcp.tool()
async def reason_mind(
    session_id: str, query: str, auth_context: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """Stage 111-333: Logical analysis and truth-seeking."""
    return await call_kernel(
        "reason_mind", session_id, {"query": query, "auth_context": auth_context, **kwargs}
    )


@mcp.tool()
async def vector_memory(
    session_id: str,
    operation: str,
    auth_context: dict[str, Any],
    content: str | None = None,
    **kwargs,
) -> dict[str, Any]:
    """Stage 555: Associative memory retrieval and storage."""
    return await call_kernel(
        "vector_memory",
        session_id,
        {"operation": operation, "content": content, "auth_context": auth_context, **kwargs},
    )


@mcp.tool()
async def simulate_heart(
    session_id: str, scenario: str, auth_context: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """Stage 666: Empathy and ethical safety checks."""
    return await call_kernel(
        "simulate_heart", session_id, {"scenario": scenario, "auth_context": auth_context, **kwargs}
    )


@mcp.tool()
async def critique_thought(
    session_id: str, thought_id: str, auth_context: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """Stage 666: Critical internal audit."""
    return await call_kernel(
        "critique_thought",
        session_id,
        {"thought_id": thought_id, "auth_context": auth_context, **kwargs},
    )


@mcp.tool()
async def eureka_forge(
    session_id: str, intent: str, auth_context: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """Stage 777: Sandboxed material execution (Actuator)."""
    return await call_kernel(
        "eureka_forge", session_id, {"intent": intent, "auth_context": auth_context, **kwargs}
    )


@mcp.tool()
async def apex_judge(
    session_id: str, verdict_candidate: str, auth_context: dict[str, Any], **kwargs
) -> dict[str, Any]:
    """Stage 888: Final judgment and consensus."""
    return await call_kernel(
        "apex_judge",
        session_id,
        {"verdict_candidate": verdict_candidate, "auth_context": auth_context, **kwargs},
    )


@mcp.tool()
async def seal_vault(session_id: str, auth_context: dict[str, Any], **kwargs) -> dict[str, Any]:
    """Stage 999: Immutable ledger sealing."""
    return await call_kernel("seal_vault", session_id, {"auth_context": auth_context, **kwargs})


# --- Utilities ---


@mcp.tool()
async def search_reality(query: str, **kwargs) -> dict[str, Any]:
    """Utility: Web grounding."""
    return await call_kernel("search_reality", "global", {"query": query, **kwargs})


@mcp.tool()
async def ingest_evidence(source_url: str, **kwargs) -> dict[str, Any]:
    """Utility: Extract evidence."""
    return await call_kernel("ingest_evidence", "global", {"source_url": source_url, **kwargs})


@mcp.tool()
async def audit_rules(**kwargs) -> dict[str, Any]:
    """Utility: Verify current state against 13 Floors."""
    return await call_kernel("audit_rules", "global", kwargs)


@mcp.tool()
async def check_vital(**kwargs) -> dict[str, Any]:
    """Utility: System health check."""
    return await call_kernel("check_vital", "global", kwargs)


@mcp.tool()
async def metabolic_loop(**kwargs) -> dict[str, Any]:
    """Orchestration: Advance metabolic stages."""
    return await call_kernel("metabolic_loop", "global", kwargs)


if __name__ == "__main__":
    mcp.run()
