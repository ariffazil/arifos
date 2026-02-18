"""Transport adapters for kernel stage orchestration.

This module keeps legacy import paths stable while delegating all stage logic
to `core.kernel.stage_orchestrator`.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from aaa_mcp.services.constitutional_metrics import get_stage_result, store_stage_result
from aaa_mcp.sessions.session_ledger import log_asi_decision
from core.kernel.stage_orchestrator import (
    run_metabolic_pipeline as _run_metabolic_pipeline,
    run_stage_444_trinity_sync as _run_stage_444_trinity_sync,
    run_stage_555_empathy as _run_stage_555_empathy,
    run_stage_666_align as _run_stage_666_align,
    run_stage_777_forge as _run_stage_777_forge,
    run_stage_888_judge as _run_stage_888_judge,
    run_stage_999_seal as _run_stage_999_seal,
)


async def run_stage_444_trinity_sync(
    session_id: str,
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return await _run_stage_444_trinity_sync(
        session_id=session_id,
        agi_result=agi_result,
        asi_result=asi_result,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
    )


async def run_stage_555_empathy(session_id: str, query: str) -> Dict[str, Any]:
    return await _run_stage_555_empathy(
        session_id=session_id,
        query=query,
        store_stage_result_fn=store_stage_result,
        log_asi_decision_fn=log_asi_decision,
    )


async def run_stage_666_align(session_id: str, query: str) -> Dict[str, Any]:
    return await _run_stage_666_align(
        session_id=session_id,
        query=query,
        store_stage_result_fn=store_stage_result,
        log_asi_decision_fn=log_asi_decision,
    )


async def run_stage_777_forge(
    session_id: str,
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return await _run_stage_777_forge(
        session_id=session_id,
        agi_result=agi_result,
        asi_result=asi_result,
        context=context,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
    )


async def run_stage_888_judge(
    session_id: str,
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return await _run_stage_888_judge(
        session_id=session_id,
        agi_result=agi_result,
        asi_result=asi_result,
        context=context,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
    )


async def run_stage_999_seal(
    session_id: str,
    judge_result: Optional[Dict[str, Any]] = None,
    agi_result: Optional[Dict[str, Any]] = None,
    asi_result: Optional[Dict[str, Any]] = None,
    summary: Optional[str] = None,
) -> Dict[str, Any]:
    return await _run_stage_999_seal(
        session_id=session_id,
        judge_result=judge_result,
        agi_result=agi_result,
        asi_result=asi_result,
        summary=summary,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
    )


async def run_metabolic_pipeline(session_id: str, query: str) -> Dict[str, Any]:
    return await _run_metabolic_pipeline(
        session_id=session_id,
        query=query,
        get_stage_result_fn=get_stage_result,
        store_stage_result_fn=store_stage_result,
        log_asi_decision_fn=log_asi_decision,
    )


__all__ = [
    "run_stage_444_trinity_sync",
    "run_stage_555_empathy",
    "run_stage_666_align",
    "run_stage_777_forge",
    "run_stage_888_judge",
    "run_stage_999_seal",
    "run_metabolic_pipeline",
]
