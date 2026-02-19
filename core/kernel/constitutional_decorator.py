"""Kernel constitutional decorator logic.

This module contains floor enforcement logic independent of transport frameworks.
"""

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from core.kernel.evaluator import (
    HARD_FLOORS,
    MANDATORY_PRE_FLOORS,
    POST_FLOORS,
    PRE_FLOORS,
    SOFT_FLOORS,
    evaluator,
)

logger = logging.getLogger(__name__)

FLOOR_ENFORCEMENT = {
    "anchor": ["F11", "F12"],
    "reason": ["F2", "F4", "F8"],
    "integrate": ["F7", "F10"],
    "respond": ["F4", "F6"],
    "validate": ["F5", "F6", "F1"],
    "align": ["F9"],
    "forge": ["F2", "F4", "F7"],
    "audit": ["F3", "F11", "F13"],
    "seal": ["F1", "F3"],
    "trinity_forge": [
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "F13",
    ],
}


def _extract_query(args: tuple, kwargs: Dict[str, Any]) -> str:
    query = kwargs.get("query") or kwargs.get("input") or ""
    if not query and args:
        query = args[0] if isinstance(args[0], str) else ""
    return str(query)


def _default_format_tool_output(_tool_name: str, payload: Any, _output_mode: str) -> Any:
    return payload


def _default_resolve_output_mode(_kwargs: Dict[str, Any]) -> str:
    return "debug"


def _default_build_hard_floor_block(
    *,
    floor: str,
    score: float,
    threshold: float,
    reason: str,
    session_id: str,
    remediation: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "verdict": "VOID",
        "blocked_by_floor": floor,
        "score": score,
        "threshold": threshold,
        "reason": reason,
        "session_id": session_id,
        "remediation": remediation,
    }


def constitutional_floor(
    *floors: str,
    format_tool_output_fn: Optional[Callable[[str, Any, str], Any]] = None,
    resolve_output_mode_fn: Optional[Callable[[Dict[str, Any]], str]] = None,
    build_hard_floor_block_fn: Optional[Callable[..., Dict[str, Any]]] = None,
):
    """Decorator to enforce constitutional floors on tool callables."""

    format_tool_output = format_tool_output_fn or _default_format_tool_output
    resolve_output_mode = resolve_output_mode_fn or _default_resolve_output_mode
    build_hard_floor_block = build_hard_floor_block_fn or _default_build_hard_floor_block

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            tool_name = func.__name__
            floor_details: List[Dict[str, Any]] = []
            query = _extract_query(args, kwargs)
            output_mode = resolve_output_mode(kwargs)
            session_id = kwargs.get("session_id", "unknown")

            all_floors = list(dict.fromkeys(list(MANDATORY_PRE_FLOORS) + list(floors)))

            pre_ctx = evaluator.build_pre_context(query, kwargs)
            for fid in MANDATORY_PRE_FLOORS:
                if fid not in floors:
                    detail = evaluator.check_floor(fid, pre_ctx)
                    detail["phase"] = "mandatory_pre"
                    floor_details.append(detail)
                    if not detail["passed"] and fid in HARD_FLOORS:
                        elapsed_ms = round((time.time() - start) * 1000, 1)
                        logger.warning(f"VOID [{tool_name}]: MANDATORY {fid} blocked")
                        payload = build_hard_floor_block(
                            floor=fid,
                            score=detail["score"],
                            threshold=0.85,
                            reason=detail["reason"],
                            session_id=session_id,
                            remediation={
                                "action": "BLOCK",
                                "message": f"Mandatory floor {fid} failed.",
                                "tool": tool_name,
                            },
                        )
                        payload["_constitutional"] = {
                            "floors_enforced": list(all_floors),
                            "details": floor_details,
                            "enforcement_ms": elapsed_ms,
                        }
                        return format_tool_output(tool_name, payload, output_mode)

            pre = [f for f in floors if f in PRE_FLOORS]
            for fid in pre:
                detail = evaluator.check_floor(fid, pre_ctx)
                detail["phase"] = "pre"
                floor_details.append(detail)
                if not detail["passed"] and fid in HARD_FLOORS:
                    elapsed_ms = round((time.time() - start) * 1000, 1)
                    logger.warning(f"VOID [{tool_name}]: {fid} blocked")
                    payload = build_hard_floor_block(
                        floor=fid,
                        score=detail["score"],
                        threshold=0.95,
                        reason=detail["reason"],
                        session_id=session_id,
                        remediation={
                            "action": "HUMAN_REVIEW",
                            "message": f"Floor {fid} failed.",
                            "tool": tool_name,
                        },
                    )
                    payload["_constitutional"] = {
                        "floors_enforced": list(floors),
                        "details": floor_details,
                        "enforcement_ms": elapsed_ms,
                    }
                    return format_tool_output(tool_name, payload, output_mode)

            result = await func(*args, **kwargs)

            post = [f for f in floors if f in POST_FLOORS]
            if post and isinstance(result, dict):
                post_ctx = evaluator.build_post_context(query, result, kwargs)
                for fid in post:
                    if fid == "F8":
                        post_ctx["_floor_scores"] = evaluator.accumulate_floor_scores(floor_details)
                    detail = evaluator.check_floor(fid, post_ctx)
                    detail["phase"] = "post"
                    floor_details.append(detail)

            verdict = evaluator.evaluate_verdict(floor_details)
            elapsed_ms = round((time.time() - start) * 1000, 1)

            if isinstance(result, dict):
                result["verdict"] = verdict
                result["_constitutional"] = {
                    "floors_declared": list(floors),
                    "floors_checked": [d["floor"] for d in floor_details],
                    "details": floor_details,
                    "enforcement_ms": elapsed_ms,
                    "version": "v64.2-CORE",
                }
                if verdict == "VOID":
                    result["status"] = "BLOCKED"
                    result["blocked_by"] = [
                        d["floor"]
                        for d in floor_details
                        if not d["passed"] and d["floor"] in HARD_FLOORS
                    ]
                elif verdict == "PARTIAL":
                    result["warnings"] = [
                        {"floor": d["floor"], "reason": d["reason"]}
                        for d in floor_details
                        if not d["passed"] and d["floor"] in SOFT_FLOORS
                    ]

            return format_tool_output(tool_name, result, output_mode)

        wrapper._constitutional_floors = floors
        return wrapper

    return decorator


def get_tool_floors(tool_name: str) -> list:
    return FLOOR_ENFORCEMENT.get(tool_name, [])


__all__ = ["constitutional_floor", "get_tool_floors", "FLOOR_ENFORCEMENT"]
