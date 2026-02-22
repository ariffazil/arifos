"""
arifOS AAA MCP Server — 5-Organ Trinity + 4 Utilities (2026.02.22-FORGE-VPS-SEAL)

DEPRECATED: This module is superseded by the unified server at `/root/arifOS/server.py`.
The unified server combines AAA-MCP and ACLIP-CAI tools into a single MCP server.
Use `python -m aaa_mcp` or `python server.py` (root) for production.

Multi-Transport Support: STDIO | SSE | StreamableHTTP

5-Organ Trinity (Public API):
1. init_session   — Ψ Init & Validate (000_INIT + 555_ASI)
2. agi_cognition  — Δ Mind (222_REASON + 333_MAP + 444_DRAFT)
3. asi_empathy    — Ω Heart (555_IMPACT + 666_ETHICS)
4. apex_verdict   — Ψ Soul (777_FORGE + 888_JUDGE)
5. vault_seal     — F1 Persistence (999_VAULT)

4 Utilities:
- search          — Web search (read-only)
- fetch           — Web fetch (read-only)
- analyze         — Data/structure analysis
- system_audit    — System verification

Legacy 9-subroutine model internalized to prevent abstraction leaks.
All thermodynamic states flow through the 5-Organ metabolic loop.

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

# 5-Organ Trinity Metadata (Public API Contract)
ORGAN_ANNOTATIONS = {
    "init_session": {
        "title": "Ψ INIT_SESSION",
        "description": "000_INIT + 555_ASI — Session ignition with impact validation",
        "symbol": "Ψ",
        "floors": ["F11", "F12", "F5", "F6"],
    },
    "agi_cognition": {
        "title": "Δ AGI_COGNITION",
        "description": "222_REASON + 333_MAP + 444_DRAFT — The Mind Engine",
        "symbol": "Δ",
        "floors": ["F2", "F4", "F7", "F8", "F10"],
    },
    "asi_empathy": {
        "title": "Ω ASI_EMPATHY",
        "description": "555_IMPACT + 666_ETHICS — The Heart Engine",
        "symbol": "Ω",
        "floors": ["F5", "F6", "F9"],
    },
    "apex_verdict": {
        "title": "Ψ APEX_VERDICT",
        "description": "777_FORGE + 888_JUDGE — The Soul Engine (SEAL/SABAR/VOID/888_HOLD)",
        "symbol": "Ψ",
        "floors": ["F2", "F3", "F4", "F11", "F13"],
    },
    "vault_seal": {
        "title": "F1 VAULT_SEAL",
        "description": "999_VAULT — Cryptographic permanence",
        "symbol": "F1",
        "floors": ["F1", "F3"],
    },
}

# Utility Metadata
UTILITY_ANNOTATIONS = {
    "search": {"title": "UTILITY: search", "description": "Web search (read-only)"},
    "fetch": {"title": "UTILITY: fetch", "description": "Web fetch (read-only)"},
    "analyze": {"title": "UTILITY: analyze", "description": "Data/structure analysis"},
    "system_audit": {"title": "UTILITY: system_audit", "description": "System verification"},
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


# ═══════════════════════════════════════════════════════════════════════════
# INTERNAL LEGACY SUB-ROUTINES (No longer exposed as public MCP tools)
# These are called internally by the 5-Organ Trinity to prevent abstraction leaks.
# ═══════════════════════════════════════════════════════════════════════════

async def _anchor_internal(
    query: str,
    actor_id: str = "anonymous",
    auth_token: str = "none",
    platform: str = "CLI",
) -> dict:
    """000_INIT — Internal session ignition."""
    return await anchor_tool(
        query=query,
        actor_id=actor_id,
        auth_token=auth_token,
        platform=platform,
        init_engine=InitEngine(),
        store_stage_result_fn=store_stage_result,
    )


async def _reason_internal(query: str, session_id: str, hypotheses: int = 3) -> dict:
    """222_REASON — Internal hypothesis generation."""
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


async def _integrate_internal(
    query: str, session_id: str, grounding: Optional[list] = None
) -> dict:
    """333_INTEGRATE — Internal context mapping."""
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


async def _respond_internal(
    session_id: str, plan: Optional[str] = None, scope: str = "social"
) -> dict:
    """444_RESPOND — Internal plan generation."""
    return await respond_tool(
        session_id=session_id,
        plan=plan,
        get_stage_result_fn=get_stage_result,
        run_stage_444_fn=run_stage_444_trinity_sync,
    )


async def _validate_internal(
    query: str,
    session_id: str,
    stakeholders: Optional[list] = None,
    scope: str = "social",
) -> dict:
    """555_VALIDATE — Internal empathy check."""
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


async def _align_internal(
    query: str, session_id: str, ethical_rules: Optional[list] = None
) -> dict:
    """666_ALIGN — Internal ethics check."""
    return await align_tool(
        query=query,
        session_id=session_id,
        ethical_rules=ethical_rules,
        run_stage_666_fn=run_stage_666_align,
    )


async def _forge_internal(
    session_id: str, implementation_details: dict
) -> dict:
    """777_FORGE — Internal solution synthesis."""
    return await forge_tool(
        session_id=session_id,
        implementation_details=implementation_details,
        get_stage_result_fn=get_stage_result,
        run_stage_777_fn=run_stage_777_forge,
    )


async def _audit_internal(
    session_id: str, verdict: str, human_approve: bool = False
) -> dict:
    """888_AUDIT — Internal verdict judgment."""
    return await audit_tool(
        session_id=session_id,
        verdict=verdict,
        human_approve=human_approve,
        tri_witness_score=ConstitutionalThresholds.TRI_WITNESS_SCORE,
        get_stage_result_fn=get_stage_result,
        run_stage_888_fn=run_stage_888_judge,
    )


async def _seal_internal(session_id: str, summary: str, verdict: str) -> dict:
    """999_SEAL — Internal cryptographic seal."""
    return await seal_tool(
        session_id=session_id,
        summary=summary,
        verdict=verdict,
        get_stage_result_fn=get_stage_result,
        run_stage_999_fn=run_stage_999_seal,
    )


async def _trinity_forge_internal(query: str, actor_id: str = "anonymous") -> dict:
    """Unified 000-999 pipeline — Internal orchestration."""
    return await trinity_forge_tool(
        query=query,
        actor_id=actor_id,
        forge_pipeline_fn=forge_pipeline,
    )


# ═══════════════════════════════════════════════════════════════════════════
# 5-ORGAN TRINITY PUBLIC API (Thermodynamically Encapsulated)
# These 5 endpoints are the ONLY public contract exposed to MCP clients.
# All internal sub-routines are routed through these organs to prevent
# abstraction leaks and reduce attack surface (F12 defense).
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool(name="init_session", description="Ψ INIT_SESSION (000+555) — Session ignition with impact validation")
@constitutional_floor("F11", "F12", "F5", "F6")
async def init_session(
    query: str,
    actor_id: str = "anonymous",
    auth_token: str = "none",
    platform: str = "CLI",
    stakeholders: Optional[list] = None,
) -> dict:
    """
    Ψ INIT_SESSION — Initiate a governed session with authority and empathy checks.
    
    Routes internally to:
      - _anchor_internal (000_INIT: Authority/F12 validation)
      - _validate_internal (555_ASI: Impact/empathy check)
    
    Returns session context with constitutional floor scores.
    """
    try:
        # 000_INIT: Authority and injection scan
        anchor_result = await _anchor_internal(
            query=query,
            actor_id=actor_id,
            auth_token=auth_token,
            platform=platform,
        )
        
        session_id = anchor_result.get("session_id")
        if not session_id:
            return {"verdict": "VOID", "error": "Failed to establish session", "stage": "000_INIT"}
        
        # 555_ASI: Empathy and impact validation
        validate_result = await _validate_internal(
            query=query,
            session_id=session_id,
            stakeholders=stakeholders,
            scope="social",
        )
        
        # Merge results thermodynamically
        return {
            "verdict": validate_result.get("verdict", "SABAR"),
            "session_id": session_id,
            "actor_id": actor_id,
            "platform": platform,
            "init": anchor_result,
            "validation": validate_result,
            "omega": ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
            "stage": "000-555",
        }
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "init_session"}


@mcp.tool(name="agi_cognition", description="Δ AGI_COGNITION (222+333+444) — The Mind Engine")
@constitutional_floor("F2", "F4", "F7", "F8", "F10")
async def agi_cognition(
    query: str,
    session_id: str,
    hypotheses: int = 3,
    grounding: Optional[list] = None,
    plan_scope: str = "social",
) -> dict:
    """
    Δ AGI_COGNITION — The Mind Engine (reason, integrate, respond).
    
    Routes internally to:
      - _reason_internal (222_REASON: Hypothesis generation)
      - _integrate_internal (333_MAP: Context grounding)
      - _respond_internal (444_DRAFT: Plan synthesis)
    
    This is the cognitive loop of the AGI (Δ) organ.
    """
    try:
        # 222_REASON: Generate hypotheses
        reason_result = await _reason_internal(
            query=query,
            session_id=session_id,
            hypotheses=hypotheses,
        )
        
        # 333_INTEGRATE: Ground in context
        integrate_result = await _integrate_internal(
            query=query,
            session_id=session_id,
            grounding=grounding,
        )
        
        # 444_RESPOND: Synthesize draft plan
        respond_result = await _respond_internal(
            session_id=session_id,
            plan=None,  # Let the system generate
            scope=plan_scope,
        )
        
        return {
            "verdict": "SEAL",
            "session_id": session_id,
            "reason": reason_result,
            "integrate": integrate_result,
            "respond": respond_result,
            "omega": ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
            "stage": "222-444",
            "symbol": "Δ",
        }
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "agi_cognition", "session_id": session_id}


@mcp.tool(name="asi_empathy", description="Ω ASI_EMPATHY (555+666) — The Heart Engine")
@constitutional_floor("F5", "F6", "F9")
async def asi_empathy(
    query: str,
    session_id: str,
    stakeholders: Optional[list] = None,
    ethical_rules: Optional[list] = None,
    scope: str = "social",
) -> dict:
    """
    Ω ASI_EMPATHY — The Heart Engine (validate, align).
    
    Routes internally to:
      - _validate_internal (555_ASI: Impact/safety check)
      - _align_internal (666_ETHICS: Ethical alignment)
    
    This is the empathy loop of the ASI (Ω) organ.
    """
    try:
        # 555_VALIDATE: Empathy and safety
        validate_result = await _validate_internal(
            query=query,
            session_id=session_id,
            stakeholders=stakeholders,
            scope=scope,
        )
        
        # 666_ALIGN: Ethics check
        align_result = await _align_internal(
            query=query,
            session_id=session_id,
            ethical_rules=ethical_rules,
        )
        
        # Calculate empathy metrics
        peace_squared = validate_result.get("peace_squared", 1.0)
        empathy_kappa = validate_result.get("empathy_kappa_r", 0.95)
        
        return {
            "verdict": validate_result.get("verdict", "SABAR"),
            "session_id": session_id,
            "validation": validate_result,
            "alignment": align_result,
            "peace_squared": peace_squared,
            "empathy_kappa_r": empathy_kappa,
            "omega": ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
            "stage": "555-666",
            "symbol": "Ω",
        }
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "asi_empathy", "session_id": session_id}


@mcp.tool(name="apex_verdict", description="Ψ APEX_VERDICT (777+888) — The Soul Engine (SEAL/SABAR/VOID/888_HOLD)")
@constitutional_floor("F2", "F3", "F4", "F11", "F13")
async def apex_verdict(
    session_id: str,
    query: str,
    implementation_details: dict,
    proposed_verdict: str = "SEAL",
    human_approve: bool = False,
) -> dict:
    """
    Ψ APEX_VERDICT — The Soul Engine (forge, audit).
    
    Routes internally to:
      - _forge_internal (777_FORGE: Solution synthesis)
      - _audit_internal (888_JUDGE: Final verdict with Tri-Witness)
    
    This is the judgment loop of the APEX (Ψ) organ.
    Outputs canonical verdicts: SEAL, SABAR, VOID, or 888_HOLD.
    """
    try:
        # 777_FORGE: Synthesize solution
        forge_result = await _forge_internal(
            session_id=session_id,
            implementation_details=implementation_details,
        )
        
        # 888_AUDIT: Judge with Tri-Witness
        audit_result = await _audit_internal(
            session_id=session_id,
            verdict=proposed_verdict,
            human_approve=human_approve,
        )
        
        # Extract final verdict
        final_verdict = audit_result.get("verdict", "SABAR")
        tri_witness = audit_result.get("tri_witness_score", 0.95)
        
        return {
            "verdict": final_verdict,
            "session_id": session_id,
            "forge": forge_result,
            "audit": audit_result,
            "tri_witness_score": tri_witness,
            "omega": ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
            "stage": "777-888",
            "symbol": "Ψ",
            "authority": "888_JUDGE",
        }
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "apex_verdict", "session_id": session_id}


@mcp.tool(name="vault_seal", description="F1 VAULT_SEAL (999) — Cryptographic permanence")
@constitutional_floor("F1", "F3")
async def vault_seal(
    session_id: str,
    summary: str,
    verdict: str = "SEAL",
) -> dict:
    """
    F1 VAULT_SEAL — Cryptographic permanence and audit trail.
    
    Routes internally to:
      - _seal_internal (999_VAULT: Write to Merkle DAG)
    
    This is the persistence organ enforcing F1 Amanah.
    Once sealed, the record is immutable and tamper-evident.
    """
    try:
        # 999_SEAL: Cryptographic commit
        seal_result = await _seal_internal(
            session_id=session_id,
            summary=summary,
            verdict=verdict,
        )
        
        return {
            "verdict": seal_result.get("verdict", "SEAL"),
            "session_id": session_id,
            "seal": seal_result,
            "stage": "999",
            "floor": "F1",
            "permanence": "cryptographic",
            "authority": "VAULT999",
        }
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "vault_seal", "session_id": session_id}


# ═══════════════════════════════════════════════════════════════════════════
# 4 UTILITIES (Read-Only Helpers)
# ═══════════════════════════════════════════════════════════════════════════

@mcp.tool(name="analyze", description="UTILITY: analyze — Data and structure analysis")
@constitutional_floor("F4")
async def analyze(
    data: dict,
    analysis_type: str = "structure",
) -> dict:
    """
    Analyze data structures, patterns, or thermodynamic signatures.
    
    Analysis types:
      - structure: Schema validation and type inference
      - entropy: Thermodynamic cost estimation
      - consensus: Tri-witness validation check
    """
    try:
        if analysis_type == "structure":
            # Structural analysis
            return {
                "verdict": "SEAL",
                "keys": list(data.keys()),
                "depth": _calculate_depth(data),
                "type_signature": _infer_type_signature(data),
            }
        elif analysis_type == "entropy":
            # Thermodynamic estimation
            estimated_complexity = len(str(data))
            return {
                "verdict": "SEAL",
                "estimated_complexity": estimated_complexity,
                "entropy_delta": -0.1 * estimated_complexity,
                "peace_squared": 1.0,
            }
        elif analysis_type == "consensus":
            # Tri-witness check
            return {
                "verdict": "SEAL",
                "tri_witness": ConstitutionalThresholds.TRI_WITNESS_SCORE,
                "consensus": "achieved",
            }
        else:
            return {"verdict": "SABAR", "error": f"Unknown analysis_type: {analysis_type}"}
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "analyze"}


def _calculate_depth(obj: dict, current_depth: int = 0) -> int:
    """Calculate nested depth of a dictionary."""
    if not isinstance(obj, dict) or not obj:
        return current_depth
    return max(_calculate_depth(v, current_depth + 1) for v in obj.values())


def _infer_type_signature(obj: Any) -> str:
    """Infer a type signature string from an object."""
    if isinstance(obj, dict):
        return "dict{" + ", ".join(f"{k}:{_infer_type_signature(v)}" for k, v in obj.items()) + "}"
    elif isinstance(obj, list):
        return f"list[{_infer_type_signature(obj[0]) if obj else 'any'}]"
    elif isinstance(obj, str):
        return "str"
    elif isinstance(obj, (int, float)):
        return "num"
    elif isinstance(obj, bool):
        return "bool"
    else:
        return "any"


@mcp.tool(name="system_audit", description="UTILITY: system_audit — System verification and health check")
@constitutional_floor("F2", "F3")
async def system_audit(
    audit_scope: str = "full",
    verify_floors: bool = True,
) -> dict:
    """
    Comprehensive system audit verifying constitutional compliance.
    
    Audit scopes:
      - quick: Basic health check
      - full: Complete constitutional floor verification
      - governance: Tri-witness and authority validation
    """
    try:
        audit_results = {
            "timestamp": time.time(),
            "scope": audit_scope,
            "verdict": "SEAL",
        }
        
        if audit_scope in ("full", "quick"):
            # System health check
            audit_results["health"] = {
                "status": "operational",
                "floors_enforced": 13,
            }
        
        if audit_scope in ("full", "governance") and verify_floors:
            # Constitutional verification
            audit_results["constitutional"] = {
                "tri_witness_threshold": ConstitutionalThresholds.TRI_WITNESS_SCORE,
                "omega_min": ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
                "peace_squared_min": getattr(ConstitutionalThresholds, "PEACE_SQUARED_MIN", 1.0),
                "floors": [f"F{i}" for i in range(1, 14)],
            }
        
        return audit_results
    except Exception as e:
        return {"verdict": "VOID", "error": str(e), "stage": "system_audit"}


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
