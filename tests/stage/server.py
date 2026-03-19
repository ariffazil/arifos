"""
arifOS MCP Bridge Server
========================
Wraps the existing arifOS REST API at aaamcp.arif-fazil.com
into a proper MCP protocol server (SSE transport) so Claude.ai
can discover and call tools.

Deploy this on Railway alongside (or replacing) the current service.
The connector URL in Claude.ai should point to this server's /sse endpoint.

Usage:
  python server.py                    # Runs on port 8000
  PORT=3000 python server.py          # Custom port

Environment Variables:
  ARIFOS_API_URL  - Base URL of your REST API (default: https://aaamcp.arif-fazil.com)
  PORT            - Server port (default: 8000)
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
    version="2026.02.15-FORGE-TRINITY-SEAL",
    instructions=(
        "arifOS Constitutional AI Governance MCP Server. "
        "Use 'forge' for full pipeline (000→999), 'think' for AGI-only, "
        "or staged tools (init, search, reason, empathy, align, reflect, seal) "
        "for step-by-step governance."
    ),
)

# Shared HTTP client
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


async def _post(endpoint: str, payload: dict) -> dict:
    """POST to the REST API and return JSON response."""
    client = await get_client()
    try:
        resp = await client.post(endpoint, json=payload)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text}
    except httpx.RequestError as e:
        return {"error": "connection_failed", "detail": str(e)}


async def _get(endpoint: str) -> dict:
    """GET from the REST API and return JSON response."""
    client = await get_client()
    try:
        resp = await client.get(endpoint)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text}
    except httpx.RequestError as e:
        return {"error": "connection_failed", "detail": str(e)}


# ---------------------------------------------------------------------------
# Tools — Primary Path
# ---------------------------------------------------------------------------


@mcp.tool()
async def forge(
    query: str,
    response: str,
    lane: str = "SOFT",
    user_id: str = "claude_user",
    context: str = "",
) -> str:
    """
    Full arifOS constitutional pipeline (000_INIT → AGI → ASI → APEX → 999_VAULT).
    Runs the entire Trinity stack and seals the result.
    Best for production and compliance use cases.

    Args:
        query: The original user query or prompt
        response: The AI-generated response to govern
        lane: Governance lane - SOFT (educational/chat) or HARD (safety-critical)
        user_id: Identifier for the requesting user
        context: Additional context for governance evaluation
    """
    result = await _post(
        "/forge",
        {
            "query": query,
            "response": response,
            "lane": lane,
            "user_id": user_id,
            "context": context,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def think(
    query: str,
    response: str,
    lane: str = "SOFT",
    user_id: str = "claude_user",
    context: str = "",
) -> str:
    """
    AGI-only pipeline (INIT + Mind reasoning, no ASI/APEX/VAULT).
    Best for research, drafting, or internal analysis without final sealing.

    Args:
        query: The original user query or prompt
        response: The AI-generated response to govern
        lane: Governance lane - SOFT or HARD
        user_id: Identifier for the requesting user
        context: Additional context
    """
    result = await _post(
        "/think",
        {
            "query": query,
            "response": response,
            "lane": lane,
            "user_id": user_id,
            "context": context,
        },
    )
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Tools — Staged Pipeline
# ---------------------------------------------------------------------------


@mcp.tool()
async def init(
    query: str,
    user_id: str = "claude_user",
    context: str = "",
) -> str:
    """
    Stage 000: Initialize governance session.
    Auth, parse, injection scan.

    Args:
        query: The query to initialize governance for
        user_id: Identifier for the requesting user
        context: Additional context
    """
    result = await _post(
        "/init",
        {
            "query": query,
            "user_id": user_id,
            "context": context,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def search(
    query: str,
    session_id: str = "",
) -> str:
    """
    Stage 111: Search — Reality grounding and evidence retrieval.
    Axiom Engine retrieves physical constants and web evidence.

    Args:
        query: The search query for grounding
        session_id: Session ID from init stage
    """
    result = await _post(
        "/search",
        {
            "query": query,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def reason(
    query: str,
    response: str,
    session_id: str = "",
) -> str:
    """
    Stage 222-333: Think and Reason — AGI Mind processing.
    Logic, truth verification, clarity assessment.

    Args:
        query: The original query
        response: The response to reason about
        session_id: Session ID from init stage
    """
    result = await _post(
        "/reason",
        {
            "query": query,
            "response": response,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def empathy(
    query: str,
    response: str,
    session_id: str = "",
) -> str:
    """
    Stage 555: Empathy — ASI Heart processing.
    Stakeholder impact, peace assessment, dignity protection.

    Args:
        query: The original query
        response: The response to assess
        session_id: Session ID from init stage
    """
    result = await _post(
        "/empathy",
        {
            "query": query,
            "response": response,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def align(
    query: str,
    response: str,
    session_id: str = "",
) -> str:
    """
    Stage 444: Constitutional alignment check.
    Validates against all 13 floors.

    Args:
        query: The original query
        response: The response to align
        session_id: Session ID from init stage
    """
    result = await _post(
        "/align",
        {
            "query": query,
            "response": response,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def reflect(
    query: str,
    response: str,
    session_id: str = "",
) -> str:
    """
    Stage 777: APEX reflection and final judgment.
    Orthogonality check, settlement, verdict generation.

    Args:
        query: The original query
        response: The response to reflect on
        session_id: Session ID from init stage
    """
    result = await _post(
        "/reflect",
        {
            "query": query,
            "response": response,
            "session_id": session_id,
        },
    )
    return json.dumps(result, indent=2)


@mcp.tool()
async def seal(
    session_id: str,
    verdict: str = "",
) -> str:
    """
    Stage 999: VAULT seal — Cryptographic sealing into Merkle DAG.
    Immutable audit trail. Irreversible.

    Args:
        session_id: Session ID to seal
        verdict: Override verdict (optional, normally auto-determined)
    """
    result = await _post(
        "/seal",
        {
            "session_id": session_id,
            "verdict": verdict,
        },
    )
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Tools — Utility
# ---------------------------------------------------------------------------


@mcp.tool()
async def health() -> str:
    """Check arifOS server health status and version."""
    result = await _get("/health")
    return json.dumps(result, indent=2)


@mcp.tool()
async def vault_query(
    session_id: str = "",
    user_id: str = "",
    limit: int = 10,
) -> str:
    """
    Query the VAULT-999 audit ledger.
    Retrieve sealed governance records.

    Args:
        session_id: Specific session ID to look up (optional)
        user_id: Filter by user ID (optional)
        limit: Max records to return
    """
    params = {"limit": limit}
    if session_id:
        params["session_id"] = session_id
    if user_id:
        params["user_id"] = user_id

    result = await _post("/vault_query", params)
    return json.dumps(result, indent=2)


@mcp.tool()
async def reality_search(
    query: str,
) -> str:
    """
    Axiom Engine: Search for physical constants and reality anchors.
    Grounds governance in measurable physical law.

    Args:
        query: Physical/scientific concept to ground (e.g., 'CO2 critical point')
    """
    result = await _post(
        "/reality_search",
        {
            "query": query,
        },
    )
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=PORT,
    )
