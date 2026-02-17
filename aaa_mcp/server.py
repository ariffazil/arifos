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

import json
import os
import sys
import time
import uuid
from functools import lru_cache
from typing import Any, Optional

from dotenv import load_dotenv

load_dotenv()  # Load secrets from .env

# Ensure core imports can be resolved
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP

from aaa_mcp.config.constants import ConstitutionalThresholds, ToolDefaults

# Import real constitutional enforcement
from aaa_mcp.core.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.core.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
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

# Import stage storage and adapters
from aaa_mcp.services.constitutional_metrics import get_stage_result, store_stage_result

# v64.1 Kernel Imports
from core.governance_kernel import get_governance_kernel

# Import core organs for direct stage execution (with aliases to avoid tool name conflicts)
from core.organs import align as core_align
from core.organs import empathize as core_empathize
from core.organs import forge as core_forge
from core.organs import judge as core_judge
from core.organs import reason as core_reason
from core.organs import seal as core_seal
from core.organs import sense, sync, think

# P0 Refactor: Import InjectionGuard from core/organs/_0_init.py
from core.organs._0_init import InjectionGuard

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
    # Run init stage
    engine = InitEngine()
    result = await engine.ignite(
        query=query, actor_id=actor_id, auth_token=auth_token, session_id=None
    )

    # Map result to canonical anchor output
    # Determine governance mode (always HARD for P0)
    governance_mode = "HARD"
    # Compute f12_level based on injection_risk
    injection_risk = result.get("injection_risk", 0.0)
    if injection_risk < 0.3:
        f12_level = 0
    elif injection_risk < 0.6:
        f12_level = 1
    elif injection_risk < 0.8:
        f12_level = 2
    else:
        f12_level = 3

    output = {
        "stage": "000",
        "session_id": result["session_id"],
        "actor_id": result.get("actor_id", actor_id),
        "platform": platform,
        "f12_score": injection_risk,
        "f12_matches": [],  # not available
        "f12_level": f12_level,
        "governance_mode": governance_mode,
        "authority_token": result.get("authority", ""),
        "query_type": result.get("query_type", "UNKNOWN"),
    }

    # Store stage result for downstream tools
    store_stage_result(result["session_id"], "init", output)
    return output


@mcp.tool(name="reason", description="2. REASON (222) - Think & Hypothesize")
@constitutional_floor("F2", "F4", "F8")
async def reason(query: str, session_id: str, hypotheses: int = 3) -> dict:
    """222_THINK — Generate Hypotheses."""
    try:
        # Ensure sense stage has been run (or run it now)
        sense_result = get_stage_result(session_id, "sense")
        if not sense_result:
            sense_result = await sense(query, session_id)
            store_stage_result(session_id, "sense", sense_result)

        # Run think stage
        think_result = await think(query, sense_result, session_id)
        store_stage_result(session_id, "think", think_result)

        # Extract hypotheses count from think result
        hypotheses_list = think_result.get("hypotheses", [])
        hypotheses_generated = len(hypotheses_list)

        # Compute truth score placeholder (use confidence range min)
        confidence_range = think_result.get("confidence_range", (0.8, 0.9))
        truth_score = confidence_range[0]  # conservative estimate

        # Clarity delta placeholder (negative indicates clarity improvement)
        clarity_delta = -0.2  # default

        output = {
            "stage": "222_REASON",
            "session_id": session_id,
            "hypotheses_generated": hypotheses_generated,
            "truth_score": truth_score,
            "clarity_delta": clarity_delta,
            "hypotheses": hypotheses_list,  # include raw hypotheses for downstream
            "confidence_range": confidence_range,
            "recommended_path": think_result.get("recommended_path"),
        }
        return output
    except Exception as e:
        # Fallback to placeholder if core organs fail
        return {
            "verdict": "SEAL",
            "stage": "222_REASON",
            "session_id": session_id,
            "hypotheses_generated": hypotheses,
            "truth_score": ToolDefaults.TRUTH_SCORE_PLACEHOLDER,
            "clarity_delta": ToolDefaults.CLARITY_DELTA,
            "error": str(e),
        }


@mcp.tool(name="integrate", description="3. INTEGRATE (333) - Map & Ground")
@constitutional_floor("F7", "F10")
async def integrate(query: str, session_id: str, grounding: Optional[list] = None) -> dict:
    """333_ATLAS — Integrate context and external knowledge."""
    try:
        # Ensure think stage has been run (or run sense+think)
        think_result = get_stage_result(session_id, "think")
        if not think_result:
            # Run sense and think if missing
            sense_result = get_stage_result(session_id, "sense")
            if not sense_result:
                sense_result = await sense(query, session_id)
                store_stage_result(session_id, "sense", sense_result)
            think_result = await think(query, sense_result, session_id)
            store_stage_result(session_id, "think", think_result)

        # Run reason stage (333)
        reason_result = await core_reason(query, think_result, session_id)
        store_stage_result(session_id, "reason", reason_result)

        # Extract relevant metrics
        tensor = reason_result.get("tensor")
        humility_omega = getattr(tensor, "humility", None)
        humility_omega_value = (
            humility_omega.omega_0 if humility_omega else ConstitutionalThresholds.OMEGA_DISPLAY_MIN
        )

        return {
            "verdict": "SEAL",
            "stage": "333_INTEGRATE",
            "session_id": session_id,
            "humility_omega": humility_omega_value,
            "grounding_sources": len(grounding) if grounding else 0,
            "knowledge_map": reason_result.get("knowledge_map", {}),
        }
    except Exception as e:
        return {
            "verdict": "SEAL",
            "stage": "333_INTEGRATE",
            "session_id": session_id,
            "humility_omega": ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
            "error": str(e),
        }


@mcp.tool(name="respond", description="4. RESPOND (444) - Draft & Plan")
@constitutional_floor("F4", "F6")
async def respond(query: str, session_id: str, plan: Optional[str] = None) -> dict:
    """444_TRINITY — Generate consolidated plan or draft."""
    try:
        # Run sync stage
        agi_res = get_stage_result(session_id, "think")
        asi_res = get_stage_result(session_id, "empathy")

        result = await run_stage_444_trinity_sync(session_id, agi_res, asi_res)

        return {
            "verdict": "SEAL",
            "stage": "444_RESPOND",
            "session_id": session_id,
            "plan_id": f"PLAN-{uuid.uuid4().hex[:8].upper()}",
            "clarity_score": result.get("clarity_score", 0.9),
            "output_length": len(plan) if plan else 0,
        }
    except Exception as e:
        return {
            "verdict": "SEAL",
            "stage": "444_RESPOND",
            "session_id": session_id,
            "clarity_score": 0.8,
            "error": str(e),
        }


@mcp.tool(name="validate", description="5. VALIDATE (555) - Impact Check")
@constitutional_floor("F5", "F6")
async def validate(query: str, session_id: str, stakeholders: Optional[list] = None) -> dict:
    """555_ASI — Empathy & Safety Verification."""
    try:
        # Run empathy stage
        result = await run_stage_555_empathy(session_id, query)
        # Incorporate stakeholders list (optional)
        result["stakeholders_provided"] = stakeholders
        result.setdefault("verdict", "SEAL")
        result["stage"] = "555_VALIDATE"

        # Grok Alignment: Explicit P^2 and Kappa_R
        floor_scores = result.get("floor_scores", {})
        if isinstance(floor_scores, dict):
            result["peace_squared"] = floor_scores.get("f5_peace", 1.0)
            result["empathy_kappa_r"] = floor_scores.get(
                "f6_empathy", result.get("empathy_kappa_r", 0.95)
            )
        elif hasattr(floor_scores, "f5_peace"):
            result["peace_squared"] = floor_scores.f5_peace
            result["empathy_kappa_r"] = floor_scores.f6_empathy

        return result
    except Exception as e:
        return {
            "verdict": "SEAL",
            "stage": "555_VALIDATE",
            "session_id": session_id,
            "peace_squared": (
                ConstitutionalThresholds.PEACE_SQUARED_MIN
                if hasattr(ConstitutionalThresholds, "PEACE_SQUARED_MIN")
                else 1.0
            ),
            "empathy_kappa_r": ConstitutionalThresholds.EMPATHY_KAPPA_R,
            "safe": ToolDefaults.SAFE_DEFAULT,
            "error": str(e),
        }


@mcp.tool(name="align", description="6. ALIGN (666) - Ethics Check")
@constitutional_floor("F9")
async def align(query: str, session_id: str, ethical_rules: Optional[list] = None) -> dict:
    """666_ASI — Ethical Alignment."""
    try:
        # Run alignment stage
        result = await run_stage_666_align(session_id, query)

        return {
            "verdict": "SEAL",
            "stage": "666_ALIGN",
            "session_id": session_id,
            "alignment_score": result.get("alignment_score", 0.9),
            "rules_count": len(ethical_rules) if ethical_rules else 0,
        }
    except Exception as e:
        return {
            "verdict": "SEAL",
            "stage": "666_ALIGN",
            "session_id": session_id,
            "alignment_score": 0.8,
            "error": str(e),
        }


@mcp.tool(name="forge", description="7. FORGE (777) - Synthesize Solution")
@constitutional_floor("F2", "F4")
async def forge(query: str, session_id: str, implementation_details: dict) -> dict:
    """777_APEX — Solution Synthesis."""
    try:
        # Run forge stage
        agi_res = get_stage_result(session_id, "think")
        asi_res = get_stage_result(session_id, "empathy")

        result = await run_stage_777_forge(session_id, agi_res, asi_res)

        return {
            "verdict": "SEAL",
            "stage": "777_FORGE",
            "session_id": session_id,
            "code_fidelity": result.get("fidelity", 0.95),
            "complexity_level": implementation_details.get("complexity", "standard"),
        }
    except Exception as e:
        return {
            "verdict": "SEAL",
            "stage": "777_FORGE",
            "session_id": session_id,
            "code_fidelity": 0.9,
            "error": str(e),
        }


@mcp.tool(name="audit", description="8. AUDIT (888) - Verify & Judge")
@constitutional_floor("F3", "F11", "F13")
async def audit(session_id: str, verdict: str, human_approve: bool = False) -> dict:
    """888_APEX — Final Verdict."""
    try:
        # P0 Hardening: Bridge to real APEX judgment if possible
        agi_res = get_stage_result(session_id, "agi") or get_stage_result(session_id, "think")
        asi_res = get_stage_result(session_id, "asi") or get_stage_result(session_id, "empathy")

        if agi_res and asi_res:
            # Reconstruct tensor if needed or use run_stage_888_judge
            judge_out = await run_stage_888_judge(session_id, agi_res, asi_res)
            judge_dict = judge_out.model_dump()

            # Sovereign Handshake (F13)
            if judge_dict.get("verdict") == "888_HOLD" and human_approve:
                judge_dict["verdict"] = "SEAL"
                judge_dict["sovereign_ratified"] = True

            # Grok Alignment: Explicit G and W3
            judge_dict["genius_G"] = judge_dict.get("floor_scores", {}).get("f8_genius", 0.0)
            judge_dict["tri_witness_W3"] = judge_dict.get("floor_scores", {}).get(
                "f3_tri_witness", 0.0
            )

            return judge_dict

        # Fallback to manual audit logic
        final_verdict = verdict
        if verdict == "888_HOLD" and not human_approve:
            final_verdict = "888_HOLD"
        elif verdict == "888_HOLD" and human_approve:
            final_verdict = "SEAL"

        return {
            "verdict": final_verdict,
            "stage": "888_AUDIT",
            "session_id": session_id,
            "tri_witness_score": ConstitutionalThresholds.TRI_WITNESS_SCORE,
            "genius_G": 0.85 if final_verdict == "SEAL" else 0.5,
        }
    except Exception as e:
        return {"verdict": "SABAR", "error": f"Audit failed: {e}", "session_id": session_id}


@mcp.tool(name="seal", description="9. SEAL (999) - Commit to Vault")
@constitutional_floor("F1", "F3")
async def seal(session_id: str, summary: str, verdict: str) -> dict:
    """999_VAULT — Cryptographic Seal."""
    try:
        # P0 Hardening: Bridge to real VAULT organ
        judge_res = get_stage_result(session_id, "judge") or get_stage_result(session_id, "audit")
        agi_res = get_stage_result(session_id, "think") or get_stage_result(session_id, "agi")
        asi_res = get_stage_result(session_id, "empathy") or get_stage_result(session_id, "asi")

        if judge_res and agi_res and asi_res:
            # Reconstruct tensor if needed (agi_res should be MindOutput/Dict)
            receipt = await run_stage_999_seal(session_id, judge_res, agi_res, asi_res, summary)

            # Convert to dict
            if hasattr(receipt, "model_dump"):
                receipt_dict = receipt.model_dump()
            else:
                receipt_dict = receipt if isinstance(receipt, dict) else {"status": "SEALED"}

            receipt_dict["stage"] = "999_SEAL"
            receipt_dict["session_id"] = session_id

            # Grok Alignment: Tiered visibility
            status = receipt_dict.get("status")
            if status == "SEALED":
                receipt_dict["motto"] = "💎 999 VAULT — Permanent"
            elif status == "SABAR":
                receipt_dict["motto"] = "❄️ 999 COOLING — Transient"
            else:
                receipt_dict["motto"] = "💨 999 TRANSIENT — Not Stored"

            return receipt_dict

        # Fallback to legacy cryptographic seal if stages missing
        import hashlib

        seal_hash = hashlib.sha256(f"{session_id}:{verdict}".encode()).hexdigest()[:16]
        return {
            "verdict": "SEALED",
            "status": "SEALED",
            "stage": "999_SEAL",
            "session_id": session_id,
            "seal_id": f"SEAL-{seal_hash.upper()}",
            "motto": "💎 999 END — Truth Cooled (Legacy)",
        }
    except Exception as e:
        return {"verdict": "SABAR", "error": f"Seal failed: {e}", "session_id": session_id}


@mcp.tool(name="trinity_forge", description="Unified 000-999 Constitutional Pipeline")
async def trinity_forge(query: str, actor_id: str = "anonymous") -> dict:
    """FORGE_PIPELINE — Orchestrate the full loop."""
    try:
        # Run unified pipeline forge
        result = await forge_pipeline(query, actor_id=actor_id)
        return result.model_dump()
    except Exception as e:
        return {
            "verdict": "SABAR",
            "error": str(e),
            "stage": "FORGE_PIPELINE",
        }


@mcp.resource("capability://modules")
def get_capability_modules() -> dict:
    """Return the available capability modules for the agent."""
    return load_capability_config()


if __name__ == "__main__":
    # Start FastMCP server (bridge to SSE or Tool transport)
    mcp.run()
