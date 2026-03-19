"""
arifOS MCP Bridge Server — CORRECTED VERSION
=============================================
Wraps the existing arifOS REST API at aaamcp.arif-fazil.com
into a proper MCP protocol server (SSE transport) so Claude.ai
can discover and call tools.

DEPLOY: Railway or VPS alongside existing service
URL: https://YOUR-URL/sse

FIXED: Maps to correct REST API endpoints (/{tool_name} not /forge, /think, etc.)
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ARIFOS_API_URL = os.getenv("ARIFOS_API_URL", "https://aaamcp.arif-fazil.com")
PORT = int(os.getenv("PORT", "8000"))

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "arifOS",
    version="64.2.0",
    instructions=(
        "arifOS Constitutional AI Governance MCP Server. "
        "Tools map to the 9 A-CLIP constitutional pipeline stages: "
        "anchor (000_INIT), reason (222), integrate (333), respond (444), "
        "validate (555), align (666), forge (777), audit (888), seal (999). "
        "Use 'forge' for full pipeline, individual tools for step-by-step."
    ),
)

_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=ARIFOS_API_URL,
            timeout=60.0,
            headers={"Content-Type": "application/json"},
        )
    return _client


async def _call_tool(tool_name: str, payload: dict) -> dict:
    """Call a tool via the REST API's generic tool endpoint."""
    client = await get_client()
    try:
        # The REST API accepts tool calls at /{tool_name} or /tools/{tool_name}
        resp = await client.post(f"/{tool_name}", json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text}
    except httpx.RequestError as e:
        return {"error": "connection_failed", "detail": str(e)}


# ---------------------------------------------------------------------------
# Tools — 9 A-CLIP Constitutional Pipeline
# ---------------------------------------------------------------------------


@mcp.tool()
async def anchor(
    query: str,
    actor_id: str = "claude_user",
    auth_token: str = "",
    mode: str = "conscience",
) -> str:
    """
    Stage 000_INIT: Constitutional airlock and session ignition.

    Establishes authority (F11), scans for injection attacks (F12),
    classifies query type, allocates thermodynamic budget.

    Args:
        query: The user's query to initialize governance for
        actor_id: User identifier (default: claude_user)
        auth_token: Optional authentication token
        mode: Governance mode - 'conscience' (default) or 'ghost'

    Returns:
        Session initialization result with session_id, f12_score,
        governance_mode, thermodynamic_budget
    """
    result = await _call_tool(
        "anchor",
        {
            "query": query,
            "actor_id": actor_id,
            "auth_token": auth_token,
            "mode": mode,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def reason(
    query: str,
    session_id: str,
    hypotheses: int = 3,
) -> str:
    """
    Stage 222_REASON: AGI Mind — Hypothesis generation and analysis.

    Generates multiple hypotheses, evaluates truth (F2),
    clarity (F4), and genius (F8). The thinking layer.

    Args:
        query: The query to reason about
        session_id: Session ID from anchor()
        hypotheses: Number of hypotheses to generate (default: 3)

    Returns:
        Reasoning result with hypotheses, truth_score, clarity_delta
    """
    result = await _call_tool(
        "reason",
        {
            "query": query,
            "session_id": session_id,
            "hypotheses": hypotheses,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def integrate(
    query: str,
    session_id: str,
    grounding: list = None,
) -> str:
    """
    Stage 333_INTEGRATE: Map and ground external knowledge.

    Grounds reasoning in external evidence (F7 Humility, F10 Ontology).
    Connects to reality search, vector DB, physical constants.

    Args:
        query: The query to ground
        session_id: Session ID from anchor()
        grounding: Optional list of evidence artifacts

    Returns:
        Integration result with grounded flag, evidence_count, humility_omega
    """
    result = await _call_tool(
        "integrate",
        {
            "query": query,
            "session_id": session_id,
            "grounding": grounding or [],
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def respond(
    session_id: str,
    draft_content: str,
) -> str:
    """
    Stage 444_RESPOND: Draft plan and response creation.

    Creates draft response with F4 Clarity and F6 Empathy checks.

    Args:
        session_id: Session ID from anchor()
        draft_content: The draft content to evaluate

    Returns:
        Response drafting result with status and clarity metrics
    """
    result = await _call_tool(
        "respond",
        {
            "session_id": session_id,
            "draft_content": draft_content,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def validate(
    session_id: str,
    stakeholders: list = None,
) -> str:
    """
    Stage 555_VALIDATE: ASI Heart — Safety and impact validation.

    Evaluates stakeholder impact (F5 Peace², F6 Empathy, F1 Amanah).
    Checks reversibility, identifies weakest stakeholder.

    Args:
        session_id: Session ID from anchor()
        stakeholders: List of stakeholder identifiers

    Returns:
        Validation result with empathy scores, reversibility flags
    """
    result = await _call_tool(
        "validate",
        {
            "session_id": session_id,
            "stakeholders": stakeholders or [],
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def align(
    query: str,
    session_id: str,
) -> str:
    """
    Stage 666_ALIGN: Ethics and constitution check (F9 Anti-Hantu).

    Validates against anti-anthropomorphism, ontological boundaries.
    Ensures no consciousness claims, no soul/sentience pretense.

    Args:
        query: The query to check
        session_id: Session ID from anchor()

    Returns:
        Alignment result with F9 score, anti_hantu flag
    """
    result = await _call_tool(
        "align",
        {
            "query": query,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def forge(
    query: str,
    session_id: str,
) -> str:
    """
    Stage 777_FORGE: Synthesize solution.

    Combines all prior stages into synthesized output.
    Resource-aware synthesis with thermodynamic constraints.

    Args:
        query: The query to forge a solution for
        session_id: Session ID from anchor()

    Returns:
        Forge result with synthesized solution, resource usage
    """
    result = await _call_tool(
        "forge",
        {
            "query": query,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def audit(
    session_id: str,
) -> str:
    """
    Stage 888_AUDIT: APEX Soul — Final judgment synthesis.

    Tri-witness consensus (F3), final verdict (SEAL/SABAR/VOID/HOLD).
    Synthesizes AGI + ASI outputs into constitutional verdict.

    Args:
        session_id: Session ID from anchor()

    Returns:
        Audit result with final verdict, confidence, floor scores
    """
    result = await _call_tool(
        "audit",
        {
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def seal(
    session_id: str,
) -> str:
    """
    Stage 999_SEAL: Cryptographic vault seal (F1 Amanah, F3 Tri-Witness).

    Immutably seals the session to VAULT999 Merkle DAG.
    Creates permanent audit trail. Irreversible.

    Args:
        session_id: Session ID to seal

    Returns:
        Seal result with seal_id, seal_hash, timestamp
    """
    result = await _call_tool(
        "seal",
        {
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def self_diagnose() -> str:
    """
    SELF_OPS: Infrastructure health check.

    Diagnoses REST API reachability, endpoint health,
    protocol compatibility. Non-constitutional utility.

    Returns:
        Full diagnostic report with all health checks
    """
    result = await _call_tool("self_diagnose", {})
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


@mcp.tool()
async def health() -> str:
    """Check arifOS server health status and version."""
    client = await get_client()
    try:
        resp = await client.get("/health")
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=PORT,
    )
