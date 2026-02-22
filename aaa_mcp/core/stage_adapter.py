"""
Stage Adapter — Wires MCP tools to core/organs (444-999)

v60.0-CORE: Now uses core/organs exclusively — codebase/ dependency removed.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import logging
from typing import Any, Dict, Optional

from aaa_mcp.services.constitutional_metrics import (
    get_stage_result,
    store_stage_result,
)
from core import organs as core_organs
from core.shared.physics import Peace2
from aaa_mcp.services.constitutional_metrics import (
    store_stage_result,
    get_stage_result,
)
from aaa_mcp.sessions.session_ledger import log_asi_decision

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

        # Handle Pydantic model output
        if hasattr(sync_out, "verdict"):
            pre_verdict = (
                sync_out.verdict.value
                if hasattr(sync_out.verdict, "value")
                else str(sync_out.verdict)
            )
            w3_score = (
                sync_out.floor_scores.f3_tri_witness if hasattr(sync_out, "floor_scores") else 0.95
            )
        else:
            sync_data = sync_out.model_dump() if hasattr(sync_out, "model_dump") else sync_out
            pre_verdict = sync_data.get("verdict", "SEAL")
            w3_score = sync_data.get("floor_scores", {}).get("f3_tri_witness", 0.95)

        result = {
            "stage": "444",
            "pre_verdict": pre_verdict,
            "consensus_score": w3_score,
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
            "status": "failed",
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

        # Handle Pydantic model output
        if hasattr(emp_out, "model_dump"):
            emp_data = emp_out.model_dump()
        elif hasattr(emp_out, "dict"):
            emp_data = emp_out.dict()
        else:
            emp_data = emp_out

        kappa_r = emp_data.get("kappa_r", 0.96)

        result = {
            "stage": "555",
            "verdict": "SEAL" if kappa_r >= 0.70 else "VOID",
            "empathy_kappa_r": kappa_r,
            "stakeholders": emp_data.get("stakeholders", []),
            "weakest_stakeholder": emp_data.get("weakest_stakeholder", "unknown"),
            "high_vulnerability": emp_data.get("weakest_vulnerability", 0.0) >= 0.8,
            "care_recommendations": emp_data.get("care_recommendations", []),
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_555", result)
        # Ω Incident Logging
        try:
            floor_scores = emp_data.get("floor_scores", {})
            floors_checked = ["F5", "F6", "F9"]
            floors_failed = []
            for floor, score in floor_scores.items():
                if floor == "f5_peace" and score < 0.5:
                    floors_failed.append("F5")
                elif floor == "f6_empathy" and score < 0.5:
                    floors_failed.append("F6")
                elif floor == "f9_anti_hantu" and score < 0.5:
                    floors_failed.append("F9")
            await log_asi_decision(
                session_id=session_id,
                stage="555",
                query=query,
                asi_output=emp_data,
                verdict=result["verdict"],
                floors_checked=floors_checked,
                floors_failed=floors_failed,
            )
        except Exception as e:
            logger.warning(f"[555] Failed to log ASI incident: {e}")
        return result

    except Exception as e:
        logger.error(f"[555] Stage execution failed: {e}")
        return {
            "stage": "555",
            "verdict": "VOID",
            "error": str(e),
            "session_id": session_id,
            "status": "failed",
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

        # Handle Pydantic model output
        if hasattr(align_out, "model_dump"):
            align_data = align_out.model_dump()
        elif hasattr(align_out, "dict"):
            align_data = align_out.dict()
        else:
            align_data = align_out

        result = {
            "stage": "666",
            "verdict": align_data.get("verdict", "SEAL"),
            "omega_bundle": align_data,
            "floor_scores": {
                "F1_amanah": 1.0 if align_data.get("is_reversible") else 0.0,
                "F5_peace": align_data.get("peace_squared", 1.0),
                "F6_empathy": align_data.get("kappa_r", 0.96),
            },
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_666", result)
        # Ω Incident Logging
        try:
            floors_checked = ["F1", "F5", "F6", "F9"]
            floors_failed = []
            violations = align_data.get("violations", [])
            for v in violations:
                if v.startswith("F1_"):
                    floors_failed.append("F1")
                elif v.startswith("F5_"):
                    floors_failed.append("F5")
                elif v.startswith("F6_"):
                    floors_failed.append("F6")
                elif v.startswith("F9_"):
                    floors_failed.append("F9")
            # Also check floor scores below threshold
            floor_scores = align_data.get("floor_scores", {})
            for floor, score in floor_scores.items():
                if floor == "f1_amanah" and score < 0.5:
                    if "F1" not in floors_failed:
                        floors_failed.append("F1")
                elif floor == "f5_peace" and score < 0.5:
                    if "F5" not in floors_failed:
                        floors_failed.append("F5")
                elif floor == "f6_empathy" and score < 0.5:
                    if "F6" not in floors_failed:
                        floors_failed.append("F6")
                elif floor == "f9_anti_hantu" and score < 0.5:
                    if "F9" not in floors_failed:
                        floors_failed.append("F9")
            await log_asi_decision(
                session_id=session_id,
                stage="666",
                query=query,
                asi_output=align_data,
                verdict=result["verdict"],
                floors_checked=floors_checked,
                floors_failed=floors_failed,
            )
        except Exception as e:
            logger.warning(f"[666] Failed to log ASI incident: {e}")
        return result

    except Exception as e:
        logger.error(f"[666] Stage execution failed: {e}")
        return {
            "stage": "666",
            "verdict": "VOID",
            "error": str(e),
            "session_id": session_id,
            "status": "failed",
        }


async def run_stage_777_forge(
    session_id: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
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

        # Handle dict output from forge
        forge_data = (
            forge_out
            if isinstance(forge_out, dict)
            else (forge_out.model_dump() if hasattr(forge_out, "model_dump") else forge_out)
        )

        result = {
            "stage": "777",
            "forge_result": forge_data,
            "low_coherence_warning": forge_data.get("coherence", 1.0) < 0.7,
            "session_id": session_id,
            "status": "completed",
        }
        store_stage_result(session_id, "stage_777", result)
        return result

    except Exception as e:
        logger.error(f"[777] Stage execution failed: {e}")
        return {"stage": "777", "error": str(e), "session_id": session_id, "status": "failed"}


async def run_stage_888_judge(
    session_id: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
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

        # Handle both Pydantic model and dict outputs
        if hasattr(judge_out, "model_dump"):
            judge_data = judge_out.model_dump()
        elif hasattr(judge_out, "dict"):
            judge_data = judge_out.dict()
        else:
            judge_data = judge_out

        # Get verdict - handle both object attribute and dict access
        if hasattr(judge_out, "verdict"):
            verdict_val = (
                judge_out.verdict.value
                if hasattr(judge_out.verdict, "value")
                else str(judge_out.verdict)
            )
            floors_failed = getattr(judge_out, "violations", [])
        else:
            verdict_val = judge_data.get("verdict", "VOID")
            floors_failed = judge_data.get("violations", [])

        result = {
            "stage": "888",
            "verdict": verdict_val,
            "judge_result": judge_data,
            "floor_violations": floors_failed,
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
            "status": "failed",
        }


async def run_stage_999_seal(session_id: str) -> Dict[str, Any]:
    """
    Stage 999: Seal - EUREKA-filtered immutable audit.

    Called by: vault_seal tool
    """
    try:
        agi_result = get_stage_result(session_id, "agi") or {}
        asi_result = (
            get_stage_result(session_id, "asi_align")
            or get_stage_result(session_id, "asi_empathize")
            or {}
        )
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

        # Handle Pydantic model output from align
        if hasattr(align_out, "model_dump"):
            align_data = align_out.model_dump()
        elif hasattr(align_out, "dict"):
            align_data = align_out.dict()
        else:
            align_data = align_out

        asi_output = {
            "kappa_r": align_data.get("kappa_r", 0.7),
            "peace_squared": align_data.get("peace_squared", 1.0),
            "is_reversible": align_data.get("is_reversible", True),
            "verdict": align_data.get("verdict", "SEAL"),
        }

        apex_out = await core_organs.apex(agi_tensor, asi_output, session_id, action="full")

        # Handle Pydantic model output from apex
        if hasattr(apex_out, "model_dump"):
            apex_data = apex_out.model_dump()
        elif hasattr(apex_out, "dict"):
            apex_data = apex_out.dict()
        else:
            apex_data = apex_out

        judge_out = apex_data.get("judge", {})

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
    results = {"session_id": session_id, "stages": {}}

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
