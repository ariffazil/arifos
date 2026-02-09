"""
Stage Adapter — Wires MCP tools to core/organs (444-999)

v60.0-CORE: Now uses core/organs exclusively — codebase/ dependency removed.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Dict, Any, Optional
import logging

from core import organs as core_organs
from core.shared.physics import W_3_from_tensor, Peace2
from aaa_mcp.services.constitutional_metrics import (
    store_stage_result,
    get_stage_result,
    get_session_evidence,
)

logger = logging.getLogger("STAGE_ADAPTER")


async def run_stage_444_trinity_sync(session_id: str) -> Dict[str, Any]:
    """
    Stage 444: Trinity Sync - Merge AGI and ASI outputs.
    
    Called by: apex_verdict tool (before judgment)
    """
    try:
        agi_result = get_stage_result(session_id, "agi") or {}
        asi_result = get_stage_result(session_id, "asi_empathize") or {}
        query = agi_result.get("query") or asi_result.get("query") or ""
        
        if not query:
            raise ValueError("Missing query for stage 444")
        
        # Build AGI tensor
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        
        asi_output = {
            "kappa_r": asi_result.get("kappa_r", asi_result.get("empathy_kappa_r", 0.7)),
            "peace_squared": asi_result.get("peace_squared", 1.0),
            "is_reversible": asi_result.get("is_reversible", True),
            "verdict": asi_result.get("verdict", "SEAL"),
        }
        
        sync_out = await core_organs.sync(agi_tensor, asi_output, session_id)
        
        result = {
            "stage": "444",
            "pre_verdict": sync_out.get("pre_verdict", "SEAL"),
            "consensus_score": sync_out.get("W_3", 0.95),
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_444", result)
        return result
        
    except Exception as e:
        logger.error(f"[444] Stage execution failed: {e}")
        return {
            "stage": "444",
            "pre_verdict": "VOID",
            "error": str(e),
            "session_id": session_id,
            "status": "failed"
        }


async def run_stage_555_empathy(session_id: str, query: str) -> Dict[str, Any]:
    """
    Stage 555: ASI Empathy - Identify stakeholders and compute κᵣ.
    
    Called by: asi_empathize tool
    """
    try:
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        
        emp_out = await core_organs.empathize(query, agi_tensor, session_id)
        
        result = {
            "stage": "555",
            "verdict": "SEAL" if emp_out.get("kappa_r", 0.0) >= 0.70 else "VOID",
            "empathy_kappa_r": emp_out.get("kappa_r", 0.96),
            "stakeholders": emp_out.get("stakeholders", []),
            "weakest_stakeholder": emp_out.get("weakest_stakeholder", "unknown"),
            "high_vulnerability": emp_out.get("weakest_vulnerability", 0.0) >= 0.8,
            "care_recommendations": emp_out.get("care_recommendations", []),
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_555", result)
        return result
        
    except Exception as e:
        logger.error(f"[555] Stage execution failed: {e}")
        return {
            "stage": "555",
            "verdict": "VOID",
            "error": str(e),
            "session_id": session_id,
            "status": "failed"
        }


async def run_stage_666_align(session_id: str, query: str) -> Dict[str, Any]:
    """
    Stage 666: ASI Align - Safety & reversibility check.
    
    Called by: asi_align tool
    """
    try:
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        
        emp_out = await core_organs.empathize(query, agi_tensor, session_id)
        align_out = await core_organs.align(query, emp_out, agi_tensor, session_id)
        
        result = {
            "stage": "666",
            "verdict": align_out.get("verdict", "SEAL"),
            "omega_bundle": align_out,
            "floor_scores": {
                "F1_amanah": 1.0 if align_out.get("is_reversible") else 0.0,
                "F5_peace": align_out.get("peace_squared", 1.0),
                "F6_empathy": align_out.get("kappa_r", 0.96),
            },
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_666", result)
        return result
        
    except Exception as e:
        logger.error(f"[666] Stage execution failed: {e}")
        return {
            "stage": "666",
            "verdict": "VOID",
            "error": str(e),
            "session_id": session_id,
            "status": "failed"
        }


async def run_stage_777_forge(session_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Stage 777: Forge - Phase transition / Eureka.
    
    Called by: apex_verdict tool (during judgment)
    """
    if context is None:
        context = {}
    
    try:
        agi_result = get_stage_result(session_id, "agi") or {}
        asi_result = get_stage_result(session_id, "asi_empathize") or {}
        query = agi_result.get("query") or asi_result.get("query") or ""
        
        if not query:
            raise ValueError("Missing query for stage 777")
        
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        
        asi_output = {
            "kappa_r": asi_result.get("kappa_r", asi_result.get("empathy_kappa_r", 0.7)),
            "peace_squared": asi_result.get("peace_squared", 1.0),
            "is_reversible": asi_result.get("is_reversible", True),
            "verdict": asi_result.get("verdict", "SEAL"),
        }
        
        sync_out = await core_organs.sync(agi_tensor, asi_output, session_id)
        forge_out = await core_organs.forge(sync_out, agi_tensor, session_id)
        
        result = {
            "stage": "777",
            "forge_result": forge_out,
            "low_coherence_warning": forge_out.get("coherence", 1.0) < 0.7,
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_777", result)
        return result
        
    except Exception as e:
        logger.error(f"[777] Stage execution failed: {e}")
        return {
            "stage": "777",
            "error": str(e),
            "session_id": session_id,
            "status": "failed"
        }


async def run_stage_888_judge(session_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Stage 888: Judge - Executive veto / final judgment.
    
    Called by: apex_verdict tool (final judgment)
    """
    if context is None:
        context = {}
    
    try:
        agi_result = get_stage_result(session_id, "agi") or {}
        asi_result = get_stage_result(session_id, "asi_empathize") or {}
        query = agi_result.get("query") or asi_result.get("query") or ""
        
        if not query:
            raise ValueError("Missing query for stage 888")
        
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        
        asi_output = {
            "kappa_r": asi_result.get("kappa_r", asi_result.get("empathy_kappa_r", 0.7)),
            "peace_squared": asi_result.get("peace_squared", 1.0),
            "is_reversible": asi_result.get("is_reversible", True),
            "verdict": asi_result.get("verdict", "SEAL"),
        }
        
        sync_out = await core_organs.sync(agi_tensor, asi_output, session_id)
        forge_out = await core_organs.forge(sync_out, agi_tensor, session_id)
        judge_out = await core_organs.judge(forge_out, sync_out, asi_output, session_id)
        
        result = {
            "stage": "888",
            "verdict": judge_out.get("verdict", "VOID"),
            "judge_result": judge_out,
            "floor_violations": judge_out.get("floors_failed", []),
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_888", result)
        return result
        
    except Exception as e:
        logger.error(f"[888] Stage execution failed: {e}")
        return {
            "stage": "888",
            "verdict": "VOID",
            "error": str(e),
            "session_id": session_id,
            "status": "failed"
        }


async def run_stage_999_seal(session_id: str) -> Dict[str, Any]:
    """
    Stage 999: Seal - EUREKA-filtered immutable audit.
    
    Called by: vault_seal tool
    """
    try:
        agi_result = get_stage_result(session_id, "agi") or {}
        asi_result = get_stage_result(session_id, "asi_align") or get_stage_result(session_id, "asi_empathize") or {}
        query = agi_result.get("query") or asi_result.get("query") or ""
        
        if not query:
            raise ValueError("Missing query for stage 999")
        
        # Build full pipeline
        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        
        emp_out = await core_organs.empathize(query, agi_tensor, session_id)
        align_out = await core_organs.align(query, emp_out, agi_tensor, session_id)
        
        asi_output = {
            "kappa_r": align_out.get("kappa_r", 0.7),
            "peace_squared": align_out.get("peace_squared", 1.0),
            "is_reversible": align_out.get("is_reversible", True),
            "verdict": align_out.get("verdict", "SEAL"),
        }
        
        apex_out = await core_organs.apex(agi_tensor, asi_output, session_id, action="full")
        judge_out = apex_out.get("judge", {})
        
        receipt = await core_organs.seal(
            judge_out,
            agi_tensor,
            asi_output,
            session_id,
            query=query,
            authority="mcp_server",
        )
        
        result = {
            "stage": "999",
            "status": receipt.status,
            "apex_verdict": judge_out.get("verdict"),
            "eureka_verdict": receipt.status,
            "hash": receipt.entry_hash,
            "seal_id": receipt.seal_id,
            "session_id": session_id,
            "mottos": receipt.mottos,
            "mottos_output": receipt.mottos_output,
        }
        store_stage_result(session_id, "stage_999", result)
        return result
        
    except Exception as e:
        logger.error(f"[999] Stage execution failed: {e}")
        return {
            "stage": "999",
            "status": "VOID",
            "error": str(e),
            "session_id": session_id,
        }


# Convenience function to run full 444-999 pipeline
async def run_metabolic_pipeline(session_id: str, query: str) -> Dict[str, Any]:
    """
    Run the full metabolic pipeline (444-999) for a session.
    
    Returns:
        Dict containing results from all stages.
    """
    results = {
        "session_id": session_id,
        "stages": {}
    }
    
    # Stage 444: Trinity Sync
    results["stages"]["444"] = await run_stage_444_trinity_sync(session_id)
    
    # Stage 555: Empathy (if not already run)
    if not get_stage_result(session_id, "stage_555"):
        results["stages"]["555"] = await run_stage_555_empathy(session_id, query)
    
    # Stage 666: Align (if not already run)
    if not get_stage_result(session_id, "stage_666"):
        results["stages"]["666"] = await run_stage_666_align(session_id, query)
    
    # Stage 777: Forge
    results["stages"]["777"] = await run_stage_777_forge(session_id)
    
    # Stage 888: Judge
    results["stages"]["888"] = await run_stage_888_judge(session_id)
    
    # Stage 999: Seal
    results["stages"]["999"] = await run_stage_999_seal(session_id)
    
    # Determine final verdict
    final_verdict = results["stages"]["888"].get("verdict", "VOID")
    results["final_verdict"] = final_verdict
    
    return results
