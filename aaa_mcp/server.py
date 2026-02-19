"""
arifOS AAA MCP Server — The 9 Hardened Skills (2026.02.17-FORGE-VPS-SEAL)

Multi-Transport Support: STDIO | SSE | StreamableHTTP
9 Canonical Verbs enforcing the 13 Constitutional Floors:
1. ANCHOR (000)     — Init & Sense (F11/F12)
2. REASON (222)     — Think & Hypothesize (F2/F8)
3. INTEGRATE (333)  — Map & Ground (F7/F10)
4. RESPOND (444)    — Draft & Plan (F4/F6)
5. VALIDATE (555)   — Impact Check (F5/F6)
6. ALIGN (666)      — Ethics Check (F9)
7. FORGE (777)      — Synthesize Code (F2/F4)
8. AUDIT (888)      — Verdict & Consensus (F3/F11)
9. SEAL (999)       — Commit to Vault (F1/F3)

Motto: DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import os
import sys
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

load_dotenv()  # Load secrets from .env

# Ensure core imports can be resolved
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP

from core.kernel.constants import ConstitutionalThresholds, ToolDefaults

# Import real constitutional enforcement
from aaa_mcp.core.constitutional_decorator import constitutional_floor
from aaa_mcp.core.engine_adapters import InitEngine
from aaa_mcp.core.stage_adapter import (
    run_stage_444_trinity_sync,
    run_stage_555_empathy,
    run_stage_666_align,
    run_stage_777_forge,
    run_stage_888_judge,
    run_stage_999_seal,
)

# Container management tools (5 additional tools)
from aaa_mcp.integrations.mcp_container_tools import register_container_tools

# ChatGPT integration: web search tools
from aaa_mcp.tools.reality_grounding import web_search_noapi
import time
from typing import Dict, Any

# Import stage storage and adapters
from aaa_mcp.services.constitutional_metrics import get_stage_result, store_stage_result

from core.kernel.mcp_tool_service import (
    align_tool,
    anchor_tool,
    audit_tool,
    forge_tool,
    integrate_tool,
    reason_tool,
    respond_tool,
    seal_tool,
    trinity_forge_tool,
    validate_tool,
)
from core.organs import reason as core_reason
from core.organs import sense, think

# Import core pipeline for unified 000-999 execution
from core.pipeline import forge as forge_pipeline

# 9 Hardened Skills Metadata
TOOL_ANNOTATIONS = {
    "anchor": {"title": "1. ANCHOR", "description": "Init & Sense (Authority/F12)"},
    "reason": {"title": "2. REASON", "description": "Hypothesize & Analyze (Risk/Truth)"},
    "integrate": {"title": "3. INTEGRATE", "description": "Map Context & Ground (Facts)"},
    "respond": {"title": "4. RESPOND", "description": "Draft Response (Clarity)"},
    "validate": {"title": "5. VALIDATE", "description": "Check Impact (Stakeholders)"},
    "align": {"title": "6. ALIGN", "description": "Check Ethics (Anti-Hantu)"},
    "forge": {"title": "7. FORGE", "description": "Synthesize Solution (Code)"},
    "audit": {"title": "8. AUDIT", "description": "Verify & Judge (Consensus)"},
    "seal": {"title": "9. SEAL", "description": "Commit to Vault (Permanence)"},
    "trinity_forge": {
        "title": "TRINITY FORGE",
        "description": "Unified 000-999 Constitutional Pipeline",
    },
}


@lru_cache(maxsize=1)
def load_capability_config() -> dict:
    """Load capability config with caching to avoid repeated I/O."""
    try:
        import yaml

        with open(
            os.path.join(os.path.dirname(__file__), "config", "capability_modules.yaml"),
            "r",
        ) as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError):
        return {}


# Initialize FastMCP Server
mcp = FastMCP(
    "arifOS-AAA",
    instructions="The Trinity Governance Layer (000-999)",
)

# Register container tools
register_container_tools(mcp)


@mcp.tool(name="anchor", description="1. ANCHOR (000) - Init & Sense")
@constitutional_floor("F11", "F12")
async def anchor(
    query: str,
    actor_id: str = "anonymous",
    auth_token: str = "none",
    platform: str = "CLI",
) -> dict:
    """000_INIT — Universal Ignition Protocol."""
    return await anchor_tool(
        query=query,
        actor_id=actor_id,
        auth_token=auth_token,
        platform=platform,
        init_engine=InitEngine(),
        store_stage_result_fn=store_stage_result,
    )


@mcp.tool(name="reason", description="2. REASON (222) - Think & Hypothesize")
@constitutional_floor("F2", "F4", "F8")
async def reason(query: str, session_id: str, hypotheses: int = 3) -> dict:
    """222_THINK — Generate Hypotheses."""
    return await reason_tool(
        query=query,
        session_id=session_id,
        hypotheses=hypotheses,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
        sense_fn=sense,
        think_fn=think,
        truth_score_placeholder=ToolDefaults.TRUTH_SCORE_PLACEHOLDER,
        clarity_delta_placeholder=ToolDefaults.CLARITY_DELTA,
    )


@mcp.tool(name="integrate", description="3. INTEGRATE (333) - Map & Ground")
@constitutional_floor("F7", "F10")
async def integrate(query: str, session_id: str, grounding: Optional[list] = None) -> dict:
    """333_ATLAS — Integrate context and external knowledge."""
    return await integrate_tool(
        query=query,
        session_id=session_id,
        grounding=grounding,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
        sense_fn=sense,
        think_fn=think,
        reason_fn=core_reason,
        humility_omega_default=ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
    )


@mcp.tool(name="respond", description="4. RESPOND (444) - Draft & Plan")
@constitutional_floor("F4", "F6")
async def respond(
    query: str, session_id: str, plan: Optional[str] = None, scope: str = "social"
) -> dict:
    """444_TRINITY — Generate consolidated plan or draft."""
    return await respond_tool(
        session_id=session_id,
        plan=plan,
        get_stage_result_fn=get_stage_result,
        run_stage_444_fn=run_stage_444_trinity_sync,
    )


@mcp.tool(name="validate", description="5. VALIDATE (555) - Impact Check")
@constitutional_floor("F5", "F6")
async def validate(
    query: str,
    session_id: str,
    stakeholders: Optional[list] = None,
    scope: str = "social",
) -> dict:
    """555_ASI — Empathy & Safety Verification."""
    return await validate_tool(
        query=query,
        session_id=session_id,
        stakeholders=stakeholders,
        run_stage_555_fn=run_stage_555_empathy,
        peace_squared_min=(
            ConstitutionalThresholds.PEACE_SQUARED_MIN
            if hasattr(ConstitutionalThresholds, "PEACE_SQUARED_MIN")
            else 1.0
        ),
        empathy_kappa_r_default=ConstitutionalThresholds.EMPATHY_KAPPA_R,
        safe_default=ToolDefaults.SAFE_DEFAULT,
    )


@mcp.tool(name="align", description="6. ALIGN (666) - Ethics Check")
@constitutional_floor("F9")
async def align(query: str, session_id: str, ethical_rules: Optional[list] = None) -> dict:
    """666_ASI — Ethical Alignment."""
    return await align_tool(
        query=query,
        session_id=session_id,
        ethical_rules=ethical_rules,
        run_stage_666_fn=run_stage_666_align,
    )


@mcp.tool(name="forge", description="7. FORGE (777) - Synthesize Solution")
@constitutional_floor("F2", "F4")
async def forge(query: str, session_id: str, implementation_details: dict) -> dict:
    """777_APEX — Solution Synthesis."""
    return await forge_tool(
        session_id=session_id,
        implementation_details=implementation_details,
        get_stage_result_fn=get_stage_result,
        run_stage_777_fn=run_stage_777_forge,
    )


@mcp.tool(name="audit", description="8. AUDIT (888) - Verify & Judge")
@constitutional_floor("F3", "F11", "F13")
async def audit(session_id: str, verdict: str, human_approve: bool = False) -> dict:
    """888_APEX — Final Verdict."""
    return await audit_tool(
        session_id=session_id,
        verdict=verdict,
        human_approve=human_approve,
        tri_witness_score=ConstitutionalThresholds.TRI_WITNESS_SCORE,
        get_stage_result_fn=get_stage_result,
        run_stage_888_fn=run_stage_888_judge,
    )


@mcp.tool(name="seal", description="9. SEAL (999) - Commit to Vault")
@constitutional_floor("F1", "F3")
async def seal(session_id: str, summary: str, verdict: str) -> dict:
    """999_VAULT — Cryptographic Seal."""
    return await seal_tool(
        session_id=session_id,
        summary=summary,
        verdict=verdict,
        get_stage_result_fn=get_stage_result,
        run_stage_999_fn=run_stage_999_seal,
    )


@mcp.tool(name="trinity_forge", description="Unified 000-999 Constitutional Pipeline")
async def trinity_forge(query: str, actor_id: str = "anonymous") -> dict:
    """FORGE_PIPELINE — Orchestrate the full loop."""
    return await trinity_forge_tool(
        query=query,
        actor_id=actor_id,
        forge_pipeline_fn=forge_pipeline,
    )


# ChatGPT Deep Research integration cache
_search_cache: Dict[str, Dict[str, Any]] = {}
_CACHE_TIMEOUT = 300  # 5 minutes


def _cache_search_results(query: str, results: list) -> list:
    """Cache search results and return IDs (URLs)."""
    global _search_cache
    current_time = time.time()

    # Clean old entries
    expired_keys = [
        k for k, v in _search_cache.items() if current_time - v["timestamp"] > _CACHE_TIMEOUT
    ]
    for key in expired_keys:
        del _search_cache[key]

    # Generate IDs (use URLs)
    ids = []
    for result in results:
        url = result.get("url")
        if url:
            cache_key = f"{query}:{url}"
            _search_cache[cache_key] = {"data": result, "timestamp": current_time, "query": query}
            ids.append(url)

    return ids


@mcp.tool(name="search", annotations={"readOnlyHint": True})
async def search(query: str) -> dict:
    """
    ChatGPT Deep Research: Search for records matching the query.

    Must return {"ids": [list of string IDs]} per ChatGPT Deep Research spec.
    Uses arifOS reality grounding for web search.
    """
    try:
        # Use arifOS web search
        result = await web_search_noapi(query, max_results=10)

        # Extract results
        search_results = result.get("results", [])

        # Cache results and get IDs
        ids = _cache_search_results(query, search_results)

        return {"ids": ids}
    except Exception as e:
        return {"ids": [], "error": str(e)}


@mcp.tool(name="fetch", annotations={"readOnlyHint": True})
async def fetch(id: str) -> dict:
    """
    ChatGPT Deep Research: Fetch a complete record by ID.

    Returns the full record data for ChatGPT to analyze.
    ID should be a URL from previous search results.
    """
    global _search_cache
    current_time = time.time()

    # Find cached result
    for cache_key, cached in list(_search_cache.items()):
        if cached["data"].get("url") == id:
            # Check if expired
            if current_time - cached["timestamp"] > _CACHE_TIMEOUT:
                del _search_cache[cache_key]
                continue

            # Return full record
            return {
                "id": id,
                **cached["data"],
                "query": cached["query"],
                "cached_at": cached["timestamp"],
            }

    # Not found in cache
    return {"error": f"Record with ID '{id}' not found or expired"}


@mcp.resource("capability://modules")
def get_capability_modules() -> dict:
    """Return the available capability modules for the agent."""
    return load_capability_config()


if __name__ == "__main__":
    # Start FastMCP server (bridge to SSE or Tool transport)
    mcp.run()
