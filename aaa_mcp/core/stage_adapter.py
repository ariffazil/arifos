"""
Stage Adapter — Wires MCP tools to codebase/stages (444-999)

Bridges the gap between:
- MCP tools (using store_stage_result/get_stage_result)
- codebase/stages (using SessionState and BundleStore)

DITEMPA BUKAN DIBERI
"""

from typing import Dict, Any, Optional
import logging

from codebase.state import SessionState, SessionStore
from codebase.bundle_store import get_store, store_bundle
from aaa_mcp.services.constitutional_metrics import (
    store_stage_result,
    get_stage_result,
    get_session_evidence,
)

# Core organs (v55.5+ kernel)
try:
    from core import organs as core_organs
    from core.shared.physics import W_3_from_tensor, Peace2
    CORE_AVAILABLE = True
except ImportError as e:
    CORE_AVAILABLE = False
    logger = logging.getLogger("STAGE_ADAPTER")
    logger.warning(f"Core organs not available in stage_adapter: {e}")

# Import stage executors
from codebase.stages.stage_444 import execute_stage_444
from codebase.stages.stage_555 import execute_stage_555
from codebase.stages.stage_666 import execute_stage_666
from codebase.stages.stage_777_forge import execute_stage
from codebase.stages.stage_888_judge import execute_stage as execute_stage_888
from codebase.stages.stage_999_seal import execute_seal_stage

logger = logging.getLogger("STAGE_ADAPTER")

# Global session store for stage-based sessions
_session_store = SessionStore()


def _get_or_create_state(session_id: str) -> SessionState:
    """Get existing SessionState or create new one."""
    state = _session_store.get(session_id)
    if state is None:
        state = SessionState(session_id=session_id)
        _session_store.put(state)
    return state


def _sync_evidence_to_state(session_id: str, state: SessionState) -> SessionState:
    """Sync evidence from MCP storage to SessionState."""
    evidence = get_session_evidence(session_id)
    if evidence:
        # Store evidence reference in state
        # Note: SessionState doesn't have direct evidence storage,
        # but we can track it via floor_scores or other mechanisms
        pass
    return state


async def run_stage_444_trinity_sync(session_id: str) -> Dict[str, Any]:
    """
    Stage 444: Trinity Sync - Merge AGI and ASI bundles.
    
    Called by: apex_verdict tool (before judgment)
    """
    if CORE_AVAILABLE:
        try:
            agi_result = get_stage_result(session_id, "agi") or {}
            asi_result = get_stage_result(session_id, "asi_empathize") or {}
            query = agi_result.get("query") or asi_result.get("query") or ""
            if not query:
                raise ValueError("Missing query for core stage 444")
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
            logger.error(f"[444] Core stage failed, falling back: {e}")
    state = _get_or_create_state(session_id)
    
    # Sync bundles from MCP storage to BundleStore
    agi_result = get_stage_result(session_id, "agi") or {}
    asi_result = get_stage_result(session_id, "asi_empathize") or {}
    
    if agi_result:
        store_bundle(session_id, "delta", {
            "session_id": session_id,
            "vote": agi_result.get("verdict", "SEAL"),
            "vote_reason": agi_result.get("verdict_justification", ""),
            "floor_scores": {
                "F2_truth": agi_result.get("truth_score", 0.99),
                "F4_clarity": agi_result.get("ambiguity_reduction", 0.0),
                "F7_humility": agi_result.get("humility_omega", 0.04),
            }
        })
    
    if asi_result:
        store_bundle(session_id, "omega", {
            "session_id": session_id,
            "vote": asi_result.get("verdict", "SEAL"),
            "vote_reason": asi_result.get("verdict_justification", ""),
            "empathy_kappa_r": asi_result.get("empathy_kappa_r", 0.96),
            "floor_scores": {
                "F1_amanah": 1.0 if asi_result.get("verdict") != "VOID" else 0.0,
                "F5_peace": asi_result.get("peace_squared", 1.0),
                "F6_empathy": asi_result.get("empathy_kappa_r", 0.96),
            }
        })
    
    # Execute stage
    try:
        pre_verdict, new_state = execute_stage_444(state)
        _session_store.put(new_state)
        
        result = {
            "stage": "444",
            "pre_verdict": pre_verdict,
            "consensus_score": new_state.floor_scores.get("F3_TriWitness", 0.95),
            "session_id": session_id,
            "status": "completed"
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
    if CORE_AVAILABLE:
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
            logger.error(f"[555] Core stage failed, falling back: {e}")
    state = _get_or_create_state(session_id)
    
    try:
        empathy_result, new_state = execute_stage_555(state, query)
        _session_store.put(new_state)
        
        # Merge with standard result format
        result = {
            "stage": "555",
            "verdict": "SEAL" if empathy_result.get("f6_pass") else "VOID",
            "empathy_kappa_r": empathy_result.get("kappa_r", 0.96),
            "stakeholders": empathy_result.get("stakeholders", []),
            "weakest_stakeholder": empathy_result.get("weakest_stakeholder", "unknown"),
            "high_vulnerability": empathy_result.get("high_vulnerability", False),
            "care_recommendations": empathy_result.get("care_recommendations", []),
            "session_id": session_id,
            "status": "completed"
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
    if CORE_AVAILABLE:
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
            logger.error(f"[666] Core stage failed, falling back: {e}")
    state = _get_or_create_state(session_id)
    
    try:
        vote, new_state = execute_stage_666(state, query)
        _session_store.put(new_state)
        
        result = {
            "stage": "666",
            "verdict": vote,
            "omega_bundle": new_state.omega_bundle,
            "floor_scores": new_state.floor_scores,
            "session_id": session_id,
            "status": "completed"
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
    
    context["session_id"] = session_id
    
    # Populate context from MCP storage
    agi_result = get_stage_result(session_id, "agi") or {}
    asi_result = get_stage_result(session_id, "asi_empathize") or {}
    if CORE_AVAILABLE:
        try:
            query = agi_result.get("query") or asi_result.get("query") or ""
            if not query:
                raise ValueError("Missing query for core stage 777")
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
            logger.error(f"[777] Core stage failed, falling back: {e}")
    
    context["reflect_result"] = agi_result.get("reasoning", {})
    context["align_result"] = asi_result.get("alignment", {})
    context["draft_solution"] = agi_result.get("conclusion", "")
    
    try:
        result_context = execute_stage(context)
        
        result = {
            "stage": "777",
            "forge_result": result_context.get("forge_result", {}),
            "low_coherence_warning": result_context.get("low_coherence_warning", False),
            "session_id": session_id,
            "status": "completed"
        }
        store_stage_result(session_id, "stage_777", result)
        return result
        
    except AttributeError as e:
        # APEXPrime.eureka not available - provide fallback
        logger.warning(f"[777] APEXPrime eureka not available, using fallback: {e}")
        result = {
            "stage": "777",
            "forge_result": {"status": "fallback", "note": "APEX eureka not configured"},
            "low_coherence_warning": False,
            "session_id": session_id,
            "status": "completed"
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
    
    context["session_id"] = session_id
    
    # Populate from MCP storage
    agi_result = get_stage_result(session_id, "agi") or {}
    asi_result = get_stage_result(session_id, "asi_empathize") or {}
    stage_777 = get_stage_result(session_id, "stage_777") or {}
    if CORE_AVAILABLE:
        try:
            query = agi_result.get("query") or asi_result.get("query") or ""
            if not query:
                raise ValueError("Missing query for core stage 888")
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
            logger.error(f"[888] Core stage failed, falling back: {e}")
    
    context["thermodynamic_violation"] = agi_result.get("floor_violations", [])
    context["reflect_result"] = agi_result.get("reasoning", {})
    context["align_result"] = asi_result.get("alignment", {})
    context["empathize_result"] = asi_result.get("empathy", {})
    context["forge_result"] = stage_777.get("forge_result", {})
    
    try:
        result_context = execute_stage_888(context)
        
        result = {
            "stage": "888",
            "verdict": result_context.get("verdict", "VOID"),
            "judge_result": result_context.get("judge_result", {}),
            "floor_violations": result_context.get("floor_violations", []),
            "session_id": session_id,
            "status": "completed"
        }
        store_stage_result(session_id, "stage_888", result)
        return result
        
    except TypeError as e:
        # APEXPrime.judge signature mismatch - provide fallback
        logger.warning(f"[888] APEXPrime judge signature mismatch, using fallback: {e}")
        
        # Simple fallback logic: check floor violations
        floor_violations = context.get("floor_violations", [])
        verdict = "VOID" if floor_violations else "SEAL"
        
        result = {
            "stage": "888",
            "verdict": verdict,
            "judge_result": {"reason": "Fallback judgment", "violations": floor_violations},
            "floor_violations": floor_violations,
            "session_id": session_id,
            "status": "completed"
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
    if CORE_AVAILABLE:
        try:
            agi_result = get_stage_result(session_id, "agi") or {}
            asi_result = get_stage_result(session_id, "asi_align") or get_stage_result(session_id, "asi_empathize") or {}
            query = agi_result.get("query") or asi_result.get("query") or ""
            if not query:
                raise ValueError("Missing query for core stage 999")
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
            }
            store_stage_result(session_id, "stage_999", result)
            return result
        except Exception as e:
            logger.error(f"[999] Core stage failed, falling back: {e}")
    try:
        result = await execute_seal_stage(session_id)
        
        # Also store in MCP stage results for consistency
        store_stage_result(session_id, "stage_999", {
            "stage": "999",
            "status": result.get("status", "SEALED"),
            "apex_verdict": result.get("apex_verdict"),
            "eureka_verdict": result.get("eureka_verdict"),
            "hash": result.get("hash"),
            "session_id": session_id,
        })
        
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
    
    This is useful for automated workflows that want to process
    through all stages in one call.
    
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
