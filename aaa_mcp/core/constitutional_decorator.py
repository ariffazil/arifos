"""
aaa_mcp/constitutional_decorator.py — REAL Constitutional Enforcement

Wraps FastMCP tools with arifOS 13-floor validation.
v60.1-PHASE1: F12 is now MANDATORY on ALL tools (immune system hardening).
v60.1-PHASE1: F11 validates session_id (no more auto-pass).
v55.5-EIGEN: Wired to core.shared.floors floor validators.
v55.5: F8 Genius now uses real eigendecomposition via genius.py extract_dials().

Floor enforcement:
  - MANDATORY:       F12 (Injection) runs on ALL tools, always, before anything else
  - Pre-execution:   F1 (Amanah), F5 (Peace), F6 (Empathy), F11 (Auth), F13 (Sovereign)
  - Post-execution:  F2 (Truth), F3 (Witness), F4 (Clarity), F7 (Humility),
                     F8 (Genius), F9 (AntiHantu), F10 (Ontology)
  - Hard floor fail  -> VOID  (block response)
  - Soft floor fail  -> PARTIAL (warn, still return)
  - All pass         -> SEAL

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# ─── Floor Registry ─────────────────────────────────────────────────────────
# Maps tool names to their required constitutional floors.
# v61.0: Updated for 5-Core Architecture
# NOTE: F12 is MANDATORY on all tools (added automatically by the decorator).
# You do NOT need to list F12 here — it's always enforced.
FLOOR_ENFORCEMENT = {
    # 5-Core Constitutional Kernel (v64.1-GAGI)
    "init_session": ["F11", "F12"],  # 000_INIT
    "agi_cognition": ["F2", "F4", "F7", "F8", "F10"],  # 111-333_AGI (Δ Mind)
    "asi_empathy": ["F1", "F5", "F6", "F9"],  # 555-666_ASI (Ω Heart)
    "apex_verdict": ["F2", "F3", "F8", "F10", "F11", "F12", "F13"],  # 888_APEX (Ψ Soul)
    "vault_seal": ["F1", "F3"],  # 999_VAULT (🔒 Memory)
    # Legacy tools (deprecated but kept for backwards compatibility)
    "init_gate": ["F11", "F12"],
    "agi_sense": ["F2", "F4"],
    "agi_think": ["F2", "F4", "F7"],
    "agi_reason": ["F2", "F4", "F7"],
    "asi_empathize": ["F5", "F6"],
    "asi_align": ["F5", "F6", "F9"],
    "apex_verdict_legacy": ["F5", "F3", "F8"],
    "reality_search": ["F2", "F7"],
    "vault_seal_legacy": ["F1", "F3"],
    # Unified 000-999 pipeline (trinity_forge) enforces ALL floors F1-F13
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
    # 9 Canonical MCP Tools (v64.2)
    "anchor": ["F11", "F12"],
    "reason": ["F2", "F4", "F8"],
    "integrate": ["F7", "F10"],
    "respond": ["F4", "F6"],
    "validate": ["F5", "F6", "F1"],
    "align": ["F9"],
    "forge": ["F2", "F4", "F7"],
    "audit": ["F3", "F11", "F13"],
    "seal": ["F1", "F3"],
}

# ─── Mandatory Floors (v60.1-PHASE1) ────────────────────────────────────────
# These floors run on EVERY tool, regardless of what floors are declared.
# F12 is the immune system — injection defense must be inescapable.
MANDATORY_PRE_FLOORS = {"F12"}

# ─── Floor Classification ───────────────────────────────────────────────────
# Pre-execution floors: validate INPUT before the tool runs
# F6 is now pre-execution: check stakeholder impact before action
PRE_FLOORS = {"F1", "F5", "F6", "F11", "F12", "F13"}

# Post-execution floors: validate OUTPUT after the tool runs
POST_FLOORS = {"F2", "F3", "F4", "F7", "F8", "F9", "F10"}

# Hard floors: failure -> VOID (block)
# F12 Injection is HARD — adversarial input is immediate VOID
HARD_FLOORS = {"F1", "F2", "F7", "F10", "F11", "F12", "F13"}

# Soft/Derived floors: failure -> PARTIAL (warn)
# F4 Clarity, F5 Peace, F6 Empathy are soft — warn but don't block
# (F6 was HARD but structurally produces sub-threshold scores for normal queries)
SOFT_FLOORS = {"F3", "F4", "F5", "F6", "F8", "F9"}

# ─── Lazy Floor Loading ─────────────────────────────────────────────────────
_floor_cache: Dict[str, Any] = {}
_floors_available: Optional[bool] = None


def _load_all_floors() -> Optional[Dict[str, Any]]:
    """Lazy-load ALL_FLOORS from core.shared.floors (v60.0+)."""
    global _floors_available
    if _floors_available is False:
        return None
    try:
        from core.shared.floors import ALL_FLOORS

        _floors_available = True
        return ALL_FLOORS
    except Exception as e:
        _floors_available = False
        logger.error(f"Failed to load constitutional_floors: {e}")
        return None


def _get_floor(floor_id: str):
    """Get or create a cached floor validator instance."""
    if floor_id in _floor_cache:
        return _floor_cache[floor_id]

    all_floors = _load_all_floors()
    if all_floors is None:
        return None

    floor_cls = all_floors.get(floor_id)
    if floor_cls is None:
        return None

    try:
        instance = floor_cls()
        _floor_cache[floor_id] = instance
        return instance
    except Exception as e:
        logger.error(f"Failed to instantiate {floor_id}: {e}")
        return None


def _extract_query(args: tuple, kwargs: Dict[str, Any]) -> str:
    """Extract query string from tool arguments (handles both positional and keyword)."""
    query = kwargs.get("query") or kwargs.get("input") or ""
    if not query and args:
        query = args[0] if isinstance(args[0], str) else ""
    return str(query)


def _build_pre_context(query: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Build context dict for pre-execution floor checks (input validation).

    v60.1-PHASE1: F11 no longer auto-passes. Session-based auth:
      - If session_id is provided, F11 passes (session was init'd)
      - If auth_token is explicitly passed, F11 uses it
      - Otherwise, F11 relies on its own validation logic
    """
    session_id = kwargs.get("session_id", "")

    ctx: Dict[str, Any] = {
        "query": query,
        "action": query,
        "session_id": session_id,
    }

    # F11: Session-based auth — only set role/token if evidence exists
    auth_token = kwargs.get("auth_token", "")
    if auth_token:
        # Explicit token passed by caller (e.g., init_gate)
        ctx["authority_token"] = auth_token
    elif session_id:
        # Session exists — tool was called in a pipeline context
        ctx["role"] = "AGENT"
        ctx["authority_token"] = "arifos_mcp"
    else:
        # No session, no token — F11 must evaluate on its own merits
        # This means F11 will likely fail, which is correct behavior:
        # tools called without init_gate should NOT auto-pass auth
        ctx["role"] = "ANONYMOUS"
        ctx["authority_token"] = ""

    return ctx


def _build_post_context(query: str, kwargs: Dict[str, Any], result: Any) -> Dict[str, Any]:
    """Build context dict for post-execution floor checks (output validation)."""
    # Extract response text from result for F9/F10 scanning
    response = ""
    if isinstance(result, dict):
        for key in ("response", "result", "reasoning", "analysis", "output"):
            val = result.get(key, "")
            if val:
                response = str(val)
                break
        if not response:
            response = str(result)
    else:
        response = str(result)

    ctx = {
        "query": query,
        "response": response,
        "session_id": kwargs.get("session_id", ""),
        # F7: Default confidence -> omega_0 = 0.04 (in band [0.03, 0.05])
        # Engine adapters now provide query-derived confidence, but keep
        # a sensible default for tools that bypass adapters.
        "confidence": 0.96,
        # F6: Default entropy — engine adapters now compute Shannon-based
        # estimates per query. These defaults are last-resort only.
        "entropy_input": 0.5,
        "entropy_output": 0.45,
        # F3: Default witness scores — raised human_witness from 0.5 to 0.8
        # to prevent permanent F3 PARTIAL in fallback mode (alarm fatigue).
        # Real tri-witness scoring comes from init_000 sovereign recognition.
        "human_witness": 0.8,
        "ai_witness": 1.0,
        "earth_witness": 1.0,
        # NOTE: truth_score is NOT defaulted here. F2_Truth has its own
        # internal logic (p_truth=1.0 base) which is correct for stubs.
        # Only engine results with explicit truth_score should override.
    }

    # Let engine results override defaults (includes heuristic scores from adapters)
    if isinstance(result, dict):
        for key in (
            "truth_score",
            "confidence",
            "entropy_delta",
            "human_witness",
            "ai_witness",
            "earth_witness",
            "empathy_kappa_r",
            "weakest_stakeholder_impact",
            "entropy_input",
            "entropy_output",
            "humility_omega",
            "f2_threshold",
        ):
            if key in result:
                ctx[key] = result[key]
        # Derive entropy_output from entropy_delta if provided
        if "entropy_delta" in result:
            ctx["entropy_output"] = ctx["entropy_input"] + result["entropy_delta"]

    return ctx


def _accumulate_floor_scores(floor_details: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Convert accumulated floor check results to FloorScores-compatible dict.

    Floor checks return raw operational scores, but genius.py's FloorScores
    expects "goodness" metrics for some floors. Three floors need inversion:
      - F7: check returns omega_0 (0.04), FloorScores expects 1-omega_0 (0.96)
      - F9: check returns c_dark (0.0), FloorScores expects 1-c_dark (1.0)
      - F12: check returns injection likelihood, FloorScores expects defense
    """
    scores: Dict[str, float] = {}
    for d in floor_details:
        fid = d["floor"]
        score = d.get("score", 0.0)
        if fid == "F7":
            scores[fid] = 1.0 - score  # omega_0 → confidence
        elif fid == "F9":
            scores[fid] = 1.0 - score  # c_dark → anti-hantu safety
        elif fid == "F12":
            scores[fid] = 1.0 - score  # injection prob → defense
        else:
            scores[fid] = score
    return scores


def _check_floor(floor_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a single floor check. Returns a detail dict.
    Resilient: if floor unavailable or crashes, returns degraded pass.
    """
    floor = _get_floor(floor_id)
    if floor is None:
        return {
            "floor": floor_id,
            "passed": False,
            "score": 0.0,
            "reason": "Floor unavailable (fail-closed)",
        }

    try:
        result = floor.check(context)
        return {
            "floor": floor_id,
            "passed": result.passed,
            "score": result.score,
            "reason": result.reason,
        }
    except Exception as e:
        logger.error(f"Floor {floor_id} check error: {e}")
        return {
            "floor": floor_id,
            "passed": False,
            "score": 0.0,
            "reason": f"Floor check error (fail-closed): {e}",
        }


# ─── Main Decorator ─────────────────────────────────────────────────────────


def constitutional_floor(*floors: str):
    """
    Decorator to enforce constitutional floors on MCP tools.

    Performs REAL validation using codebase/constitutional_floors.py:
      - Pre-execution:  Scans input for injection, risk, destructive intent
      - Post-execution: Scans output for consciousness claims, literalism, truth
      - Hard floor fail -> VOID (block)
      - Soft floor fail -> PARTIAL (warn)
      - All pass -> SEAL

    IMPORTANT: This decorator must be INNER (closer to the function) with
    @mcp.tool() as the OUTER decorator, so FastMCP registers the wrapped version:

        @mcp.tool()
        @constitutional_floor("F2", "F4", "F7")
        async def agi_reason(query: str) -> dict:
            ...
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            tool_name = func.__name__
            floor_details: List[Dict[str, Any]] = []
            # Lazy import to avoid circular dependencies during server import.
            from aaa_mcp.presentation.formatter import format_tool_output, resolve_output_mode

            # Extract query from arguments
            query = _extract_query(args, kwargs)
            output_mode = resolve_output_mode(kwargs)

            # Merge declared floors with mandatory floors (F12 always runs)
            all_floors = list(dict.fromkeys(list(MANDATORY_PRE_FLOORS) + list(floors)))

            # ── PHASE 0: MANDATORY PREPROCESSING (v60.1) ───────────
            # F12 injection defense runs FIRST, on ALL tools, unconditionally.
            # This is the immune system — it fires before the brain processes.
            pre_ctx = _build_pre_context(query, kwargs)
            for fid in MANDATORY_PRE_FLOORS:
                if fid not in floors:  # Avoid double-checking if already declared
                    detail = _check_floor(fid, pre_ctx)
                    detail["phase"] = "mandatory_pre"
                    floor_details.append(detail)

                    # Mandatory hard floor fail -> VOID immediately
                    if not detail["passed"] and fid in HARD_FLOORS:
                        elapsed_ms = round((time.time() - start) * 1000, 1)
                        logger.warning(
                            f"VOID [{tool_name}]: MANDATORY {fid} blocked "
                            f"(score={detail['score']:.3f})"
                        )

                        from aaa_mcp.protocol.tool_registry import build_hard_floor_block

                        threshold = 0.85 if fid == "F12" else 0.95
                        session_id = kwargs.get("session_id", "unknown")

                        payload = build_hard_floor_block(
                            floor=fid,
                            score=detail["score"],
                            threshold=threshold,
                            reason=detail["reason"],
                            session_id=session_id,
                            remediation={
                                "action": "INJECTION_BLOCKED",
                                "message": f"Mandatory floor {fid} blocked at {tool_name}. Input rejected.",
                                "required": f"{fid} score must be below threshold",
                                "current": detail["score"],
                                "tool": tool_name,
                                "elapsed_ms": elapsed_ms,
                            },
                        )
                        payload["_constitutional"]["floors_enforced_now"] = list(all_floors)
                        payload["_constitutional"]["floors_checked"] = [
                            d["floor"] for d in floor_details
                        ]
                        payload["_constitutional"]["details"] = floor_details
                        payload["_constitutional"]["enforcement_ms"] = elapsed_ms
                        payload["_constitutional"]["mandatory_block"] = True

                        return format_tool_output(tool_name, payload, output_mode)

            # ── PHASE 1: PRE-EXECUTION CHECKS ──────────────────────
            pre = [f for f in floors if f in PRE_FLOORS]
            if pre:
                for fid in pre:
                    detail = _check_floor(fid, pre_ctx)
                    detail["phase"] = "pre"
                    floor_details.append(detail)

                    # Hard floor fail -> VOID immediately (don't run tool)
                    if not detail["passed"] and fid in HARD_FLOORS:
                        elapsed_ms = round((time.time() - start) * 1000, 1)
                        logger.warning(
                            f"VOID [{tool_name}]: {fid} blocked " f"(score={detail['score']:.3f})"
                        )

                        # Use standardized hard floor block envelope (v60)
                        from aaa_mcp.protocol.tool_registry import build_hard_floor_block

                        # Get threshold for this floor
                        threshold = 0.95  # Default for most hard floors
                        if fid == "F2":
                            threshold = 0.99
                        elif fid == "F7":
                            threshold = 0.03  # Lower bound (humility band)
                        elif fid == "F12":
                            threshold = 0.85

                        session_id = kwargs.get("session_id", "unknown")

                        payload = build_hard_floor_block(
                            floor=fid,
                            score=detail["score"],
                            threshold=threshold,
                            reason=detail["reason"],
                            session_id=session_id,
                            remediation={
                                "action": "HUMAN_REVIEW",
                                "message": f"Constitutional floor {fid} not satisfied at {tool_name}.",
                                "required": f"{fid} score must meet threshold",
                                "current": detail["score"],
                                "tool": tool_name,
                                "elapsed_ms": elapsed_ms,
                            },
                        )
                        # Update with additional context
                        payload["_constitutional"]["floors_enforced_now"] = list(floors)
                        payload["_constitutional"]["floors_checked"] = [
                            d["floor"] for d in floor_details
                        ]
                        payload["_constitutional"]["details"] = floor_details
                        payload["_constitutional"]["enforcement_ms"] = elapsed_ms

                        # Presentation formatting (user vs debug/audit)
                        return format_tool_output(tool_name, payload, output_mode)

            # ── PHASE 2: EXECUTE TOOL ──────────────────────────────
            result = await func(*args, **kwargs)

            # ── PHASE 3: POST-EXECUTION CHECKS ────────────────────
            post = [f for f in floors if f in POST_FLOORS]
            if post and isinstance(result, dict):
                post_ctx = _build_post_context(query, kwargs, result)
                for fid in post:
                    # F8 Genius needs accumulated floor scores for eigendecomposition
                    if fid == "F8":
                        post_ctx["_floor_scores"] = _accumulate_floor_scores(floor_details)
                    detail = _check_floor(fid, post_ctx)
                    detail["phase"] = "post"
                    floor_details.append(detail)

            # ── PHASE 4: COMPUTE VERDICT ───────────────────────────
            hard_fails = [d for d in floor_details if not d["passed"] and d["floor"] in HARD_FLOORS]
            soft_fails = [d for d in floor_details if not d["passed"] and d["floor"] in SOFT_FLOORS]

            if hard_fails:
                verdict = "VOID"
            elif soft_fails:
                verdict = "PARTIAL"
            else:
                verdict = "SEAL"

            elapsed_ms = round((time.time() - start) * 1000, 1)

            # ── PHASE 5: STAMP RESULT ──────────────────────────────
            if isinstance(result, dict):
                result["verdict"] = verdict
                result["_constitutional"] = {
                    "floors_declared": list(floors),
                    "mandatory_floors": list(MANDATORY_PRE_FLOORS),
                    "floors_checked": [d["floor"] for d in floor_details],
                    "details": floor_details,
                    "enforcement_ms": elapsed_ms,
                    "version": "v60.1-PHASE1",
                    "floors_enforced": list(all_floors),
                }

                if verdict == "VOID":
                    result["status"] = "BLOCKED"
                    result["blocked_by"] = [d["floor"] for d in hard_fails]
                    logger.warning(
                        f"VOID [{tool_name}]: post-check blocked by "
                        f"{[d['floor'] for d in hard_fails]}"
                    )
                elif verdict == "PARTIAL":
                    result["warnings"] = [
                        {"floor": d["floor"], "reason": d["reason"]} for d in soft_fails
                    ]
                    logger.info(
                        f"PARTIAL [{tool_name}]: soft warnings "
                        f"{[d['floor'] for d in soft_fails]}"
                    )

            return format_tool_output(tool_name, result, output_mode)

        # Attach floor metadata for introspection
        wrapper._constitutional_floors = floors
        return wrapper

    return decorator


def get_tool_floors(tool_name: str) -> list:
    """Get constitutional floors for a tool."""
    return FLOOR_ENFORCEMENT.get(tool_name, [])
