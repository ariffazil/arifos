"""
codebase/mcp/tools/canonical_trinity.py

The 7 Canonical Tools of arifOS (AAA Framework)
Implementing the "Trinity of Constitutional Verdicts" and metabolic cycle.

LLM-Agnostic: Works with any MCP-compatible client (Claude, GPT, Gemini, Cursor, Codex, etc.)
All handlers normalize input to handle diverse calling conventions (args wrapping, etc.)

Scope:
1. _init_ (Gate)
2. _agi_ (Mind)
3. _asi_ (Heart)
4. _apex_ (Soul)
5. _vault_ (Seal)
6. _trinity_ (Loop)
7. _reality_ (Ground)
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from codebase.kernel import get_kernel_manager
from codebase.mcp.core.session_context import get_current_session_id, set_current_session_id

logger = logging.getLogger(__name__)

# Schema validation (v55.3) - optional, non-breaking
try:
    from codebase.schemas.validator import (
        validate_agi_output,
        validate_apex_output,
        validate_asi_output,
        validate_output,
        validate_reality_output,
        validate_vault_output,
    )

    SCHEMA_VALIDATION_AVAILABLE = True
except ImportError:
    SCHEMA_VALIDATION_AVAILABLE = False
    logger.debug("Schema validation not available")

# Strict mode flag (environment variable)
SCHEMA_STRICT_MODE = os.environ.get("AAA_SCHEMA_STRICT", "false").lower() == "true"

from codebase.mcp.core.bridge import (
    bridge_atlas_router,
    bridge_reality_check_router,
    bridge_trinity_loop_router,
)


def _normalize_kwargs(kwargs: dict) -> dict:
    """
    LLM-agnostic input normalizer.
    Some MCP clients wrap tool parameters under 'args' or 'kwargs'.
    This unwraps them so handlers receive flat keyword arguments.
    """
    # Some clients (e.g. GPT Actions) wrap params under 'args' dict
    if "args" in kwargs and isinstance(kwargs["args"], dict):
        unwrapped = kwargs.pop("args")
        unwrapped.update(kwargs)
        return unwrapped
    # Some clients wrap under 'kwargs'
    if "kwargs" in kwargs and isinstance(kwargs["kwargs"], dict):
        unwrapped = kwargs.pop("kwargs")
        unwrapped.update(kwargs)
        return unwrapped
    return kwargs


# ==============================================================================
# 1. _init_ (The Gate)
# ==============================================================================
async def mcp_init(
    action: str = "init", query: str = "", session_id: Optional[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    _init_: The 7-Step Thermodynamic Ignition Sequence.
    """
    import importlib

    kwargs = _normalize_kwargs(kwargs)
    # Extract known params that may have been wrapped
    action = kwargs.pop("action", action) or "init"
    query = kwargs.pop("query", query) or ""
    session_id = kwargs.pop("session_id", session_id)

    # Dynamic import to handle '000_init' directory name (invalid Python identifier)
    module = importlib.import_module("codebase.init.000_init.mcp_bridge")
    mcp_000_init = module.mcp_000_init

    # Only pass parameters that mcp_000_init accepts
    result = await mcp_000_init(
        action=action,
        query=query,
        session_id=session_id,
        authority_token=kwargs.get("authority_token", ""),
        context=kwargs.get("context"),
    )

    # Stamp every _init_ response with the arifOS motto
    result["motto"] = "DITEMPA, BUKAN DIBERI \U0001f9e0\U0001f525\U0001f48e"
    # result["root_key"] = "TOY_MODE"  # REMOVED: Security Hardening (P0)

    # Adapter: Map internal result to ToolRegistry schema
    # Schema requires: session_id, authority_level, budget_allocated, injection_check_passed, access_level, session_ttl, constitutional_version

    # 1. Map authority -> authority_level
    auth = result.get("authority", "GUEST").lower()
    if "judge" in auth or "admin" in auth:
        auth_level = "admin"
    elif "authorized" in str(result.get("status", "")).lower() or result.get("authority_verified"):
        auth_level = "user"
    else:
        auth_level = "guest"

    # 2. Map injection_risk -> injection_check_passed
    risk = result.get("injection_risk", 0.0)
    passed = risk < 0.15

    # 3. Fill missing schema fields
    adapted_result = {
        "session_id": result.get("session_id", session_id or "unknown"),
        "authority_level": auth_level,
        "budget_allocated": int(result.get("energy_budget", 1.0) * 100),
        "injection_check_passed": passed,
        "access_level": result.get("lane", "SOFT"),
        "session_ttl": 3600,  # Default TTL
        "constitutional_version": "v55.2",
        "verdict": result.get("verdict", "SEAL"),
        # Keep original helpful data
        "original_status": result.get("status"),
        "reason": result.get("reason"),
        "motto": result["motto"],
    }

    # Implicit Session Binding (F12 Hardening)
    if adapted_result["session_id"] and adapted_result["session_id"] != "unknown":
        set_current_session_id(adapted_result["session_id"])

    return adapted_result


# ==============================================================================
# 2. _agi_ (The Mind)
# ==============================================================================
async def mcp_agi(
    action: str = "full", query: str = "", session_id: Optional[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    _agi_: Mind Engine (Δ) - Logic, Sense, Think, Reason.

    Supported actions:
        action="sense"   → Stage 111 only (intent classification, risk flags)
        action="think"   → Stage 111+222 (hypotheses with pros/cons)
        action="reflect" → Constitutional critique of thought (Meta-Cognition)
        action="physics" → Thermodynamic constraints check (Entropy/F4)
        action="reason"  → Full pipeline with reflection
        action="full"    → Same as "reason" (backward compat)
    """
    kwargs = _normalize_kwargs(kwargs)
    action = kwargs.pop("action", action) or "full"
    query = kwargs.pop("query", query) or ""
    session_id = kwargs.pop("session_id", session_id) or get_current_session_id()

    kernel = get_kernel_manager().get_agi()
    try:
        raw_result = await kernel.execute(
            action, {"query": query, "session_id": session_id, **kwargs}
        )
    except Exception as e:
        logger.error("mcp_agi execute failed: %s", e, exc_info=True)
        return {
            "session_id": session_id or "unknown",
            "entropy_delta": 0.0,
            "omega_0": 0.04,
            "precision": {},
            "hierarchical_beliefs": {},
            "action_policy": {},
            "vote": "VOID",
            "verdict": "VOID",
            "floor_scores": {},
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal processing error",
                "suggestion": "Check action parameter or query format",
            },
        }

    # Adapter: Map to ToolRegistry schema
    # Schema requires: session_id, entropy_delta, vote

    # Convert Dataclass/Pydantic to dict if needed
    if hasattr(raw_result, "dict"):
        result = raw_result.dict()
    elif hasattr(raw_result, "asdict"):
        result = raw_result.asdict()
    elif hasattr(raw_result, "__dict__"):
        result = raw_result.__dict__
    elif isinstance(raw_result, dict):
        result = raw_result
    else:
        result = {"error": "Unknown result type", "raw": str(raw_result)}

    # Per-stage results are already schema-compliant from AGINeuralCore
    action_upper = action.upper()
    if action_upper in ("SENSE", "THINK"):
        if "verdict" not in result:
            result["verdict"] = result.get("vote", "SEAL")
        return result

    # Full/reason pipeline: ensure backward-compatible required fields
    if "entropy_delta" not in result:
        result["entropy_delta"] = result.get("clarity_score", 0.0) - 0.5

    if "vote" not in result:
        result["vote"] = result.get("status", "VOID")

    adapted = {
        "session_id": result.get("session_id", session_id),
        "entropy_delta": float(result.get("entropy_delta", 0.0)),
        "omega_0": float(result.get("omega_0", 0.04)),
        "precision": result.get("precision", {}),
        "hierarchical_beliefs": result.get("hierarchical_beliefs", result.get("hierarchy", {})),
        "action_policy": result.get("action_policy", {}),
        "vote": result.get("vote", "VOID"),
        "verdict": result.get("vote", "VOID"),
        "floor_scores": result.get("floor_scores", {}),
        # New contentful fields (v55.2)
        "conclusion": result.get("conclusion", ""),
        "confidence": result.get("confidence", 0.0),
        "premises": result.get("premises", []),
        "counterarguments": result.get("counterarguments", []),
        "failure_conditions": result.get("failure_conditions", []),
        "free_energy": result.get("free_energy", 0.0),
    }

    # Include reflection if present
    if "reflection" in result:
        adapted["reflection"] = result["reflection"]

    # F4 Clarity: Schema validation (v55.3)
    if SCHEMA_VALIDATION_AVAILABLE:
        validate_agi_output(adapted, strict=SCHEMA_STRICT_MODE)

    return adapted


# ==============================================================================
# 3. _asi_ (The Heart)
# ==============================================================================
async def mcp_asi(
    action: str = "full",
    query: str = "",
    reasoning: str = "",
    session_id: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    _asi_: Heart Engine (Ω) - Empathy, Safety, Alignment.
    """
    kwargs = _normalize_kwargs(kwargs)
    action = kwargs.pop("action", action) or "full"
    query = kwargs.pop("query", query) or ""
    reasoning = kwargs.pop("reasoning", reasoning) or ""
    session_id = kwargs.pop("session_id", session_id) or get_current_session_id()

    kernel = get_kernel_manager().get_asi()
    context = kwargs.pop("context", {})
    if reasoning:
        context["reasoning"] = reasoning

    result = await kernel.execute(
        action,
        {"text": query, "query": query, "session_id": session_id, "context": context, **kwargs},
    )

    # Adapter: Map to ToolRegistry schema
    # Schema requires: session_id, omega_total, vote

    if hasattr(result, "dict"):
        data = result.dict()
    elif hasattr(result, "asdict"):  # Dataclass support
        from dataclasses import asdict

        data = asdict(result)
    elif isinstance(result, dict):
        data = result
    else:
        data = result.__dict__ if hasattr(result, "__dict__") else {}

    adapted = {
        "session_id": data.get("session_id", session_id),
        "omega_total": float(data.get("omega_total", 0.0)),
        "vote": data.get("vote") or data.get("verdict", "VOID"),
        "verdict": data.get("verdict") or data.get("vote", "VOID"),
        "empathy_kappa_r": float(
            data.get("empathy_kappa_r")  # Direct from _execute_full
            or (data.get("trinity_self") or {}).get("empathy_kappa_r")  # From empathize action
            or (data.get("empathy") or {}).get("kappa_r")  # From OmegaBundle
            or 0.0
        ),
        "peace_squared": float(
            data.get("peace_squared")  # Direct from _execute_full
            or (data.get("trinity_system") or {}).get("peace_squared")  # From align action
            or (data.get("system") or {}).get("peace_squared")  # From OmegaBundle
            or 0.0
        ),
        "thermodynamic_justice": float(
            data.get("society", {}).get("thermodynamic_justice", 0.0)
            if isinstance(data.get("society"), dict)
            else 0.0
        ),
        "stakeholders": data.get("stakeholders", []),
        "weakest_stakeholder": data.get("weakest_stakeholder", {}),
        "reversibility_score": float(data.get("floor_scores", {}).get("F1_reversibility", 1.0)),
        "consent_verified": bool(data.get("floor_scores", {}).get("F11_consent", False)),
    }

    # F4 Clarity: Schema validation (v55.3)
    if SCHEMA_VALIDATION_AVAILABLE:
        validate_asi_output(adapted, strict=SCHEMA_STRICT_MODE)

    return adapted


# ==============================================================================
# 4. _apex_ (The Soul)
# ==============================================================================
async def mcp_apex(
    action: str = "full",
    query: str = "",
    response: str = "",
    verdict: str = "",
    session_id: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    _apex_: Soul Engine (Ψ) - Judgment, Verdict, Proof.
    """
    kwargs = _normalize_kwargs(kwargs)
    action = kwargs.pop("action", action) or "full"
    query = kwargs.pop("query", query) or ""
    response = kwargs.pop("response", response) or ""
    verdict = kwargs.pop("verdict", verdict) or ""
    session_id = kwargs.pop("session_id", session_id) or get_current_session_id()

    kernel = get_kernel_manager().get_apex()
    kwargs["pre_verdict"] = verdict

    raw_result = await kernel.execute(
        action, {"query": query, "response": response, "session_id": session_id, **kwargs}
    )

    # Adapter: Map to ToolRegistry schema
    # Schema requires: session_id, final_verdict, trinity_score

    # Map 'verdict' -> 'final_verdict'
    final_verdict = raw_result.get("verdict", raw_result.get("status", "VOID"))

    # Extract trinity_score
    trinity_score = 0.0
    if "trinity_score" in raw_result:
        trinity_score = raw_result["trinity_score"]
    elif "equilibrium" in raw_result:
        trinity_score = raw_result["equilibrium"].get("score", 0.0)

    adapted = {
        "session_id": raw_result.get("session_id", session_id),
        "final_verdict": final_verdict,
        "verdict": final_verdict,
        "trinity_score": float(trinity_score),
        "paradox_scores": raw_result.get("paradox_scores", {}),
        "equilibrium": raw_result.get("equilibrium", {}),
        "constitutional_alignment": raw_result.get("constitutional_alignment", {}),
        "proof": raw_result.get("proof", {}),
    }

    # F4 Clarity: Schema validation (v55.3)
    if SCHEMA_VALIDATION_AVAILABLE:
        validate_apex_output(adapted, strict=SCHEMA_STRICT_MODE)

    return adapted


# ==============================================================================
# 5. _vault_ (The Seal) — HARDENED with EUREKA Sieve
# ==============================================================================
async def mcp_vault(
    action: str = "seal",
    verdict: str = "SEAL",
    decision_data: Optional[Dict] = None,
    target: str = "seal",
    session_id: Optional[str] = None,
    # HARDENED: Full Trinity results for EUREKA evaluation
    query: str = "",
    response: str = "",
    init_result: Optional[Dict] = None,
    agi_result: Optional[Dict] = None,
    asi_result: Optional[Dict] = None,
    apex_result: Optional[Dict] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    _vault_: HARDENED Immutable Ledger with EUREKA Sieve.

    Theory of Anomalous Contrast:
    - Only EUREKA insights (score ≥ 0.75) → Permanent VAULT999
    - Medium insights (0.50-0.75) → Cooling ledger (SABAR)
    - Trivial queries (< 0.50) → TRANSIENT (not stored)

    Actions:
        seal    — EUREKA-filtered append with hash chain + Merkle root
        list    — Paginated listing (cursor/limit)
        read    — Retrieve by session_id or sequence number
        query   — Filter by verdict and time range
        verify  — Verify chain integrity
        proof   — Get Merkle inclusion proof
    """
    # Use consolidated vault_tool with EUREKA Sieve (v55.3)
    from codebase.mcp.tools.vault_tool import AUTHORITY_NOTICE, VaultTool

    kwargs = _normalize_kwargs(kwargs)
    action = kwargs.pop("action", action) or "seal"
    verdict = kwargs.pop("verdict", verdict) or "SEAL"
    session_id = kwargs.pop("session_id", session_id) or get_current_session_id()
    decision_data = kwargs.pop("decision_data", decision_data) or {}

    # HARDENED: Extract Trinity results for EUREKA evaluation
    query = kwargs.pop("query", query) or decision_data.get("query", "")
    response = kwargs.pop("response", response) or decision_data.get("response", "")
    init_result = kwargs.pop("init_result", init_result) or decision_data.get("init_result", {})
    agi_result = kwargs.pop("agi_result", agi_result) or decision_data.get("agi_result", {})
    asi_result = kwargs.pop("asi_result", asi_result) or decision_data.get("asi_result", {})
    apex_result = kwargs.pop("apex_result", apex_result) or decision_data.get("apex_result", {})

    if not session_id:
        session_id = str(uuid.uuid4())

    # Build payload from decision_data + kwargs for VaultTool
    payload: Dict[str, Any] = dict(decision_data)

    if action == "seal":
        # HARDENED: Run APEX kernel for proof, include in seal_data
        try:
            kernel = get_kernel_manager().get_apex()
            kernel_result = await kernel.execute(
                "seal",
                {
                    "session_id": session_id,
                    "verdict": verdict,
                    "data": decision_data,
                    "target_ledger": target,
                    **kwargs,
                },
            )
            payload["kernel_result"] = kernel_result if isinstance(kernel_result, dict) else {}
        except Exception as e:
            logger.warning(f"[VAULT_999] APEX kernel seal failed, sealing without proof: {e}")
            payload["kernel_result"] = {"error": str(e)}

        payload["verdict"] = verdict
        payload["authority"] = decision_data.get("authority") or kwargs.get("authority", "system")

        # HARDENED: Build Trinity bundle for EUREKA Sieve
        payload["init_result"] = init_result
        payload["agi_result"] = agi_result
        payload["asi_result"] = asi_result
        payload["apex_result"] = apex_result

    elif action == "query":
        # Map query-specific params into payload keys VaultTool expects
        payload.setdefault(
            "verdict", decision_data.get("verdict") or kwargs.get("query_verdict") or "SEAL"
        )
        for key in ("start_time", "end_time"):
            val = decision_data.get(key) or kwargs.get(key)
            if val is not None:
                payload.setdefault(key, val)

    else:
        # list / read / proof: forward limit, cursor, sequence from kwargs
        for key in ("limit", "cursor", "sequence"):
            val = kwargs.get(key) or decision_data.get(key)
            if val is not None:
                payload.setdefault(key, val)

    try:
        # HARDENED: Pass Trinity results for EUREKA evaluation
        return await VaultTool.execute(
            action=action,
            session_id=session_id,
            target=target,
            payload=payload,
            query=query,
            response=response,
            trinity_bundle={
                "init": init_result,
                "agi": agi_result,
                "asi": asi_result,
                "apex": apex_result,
            },
        )
    except Exception as e:
        logger.error(f"[VAULT_999] Error: {e}")
        return {
            "operation": "error",
            "verdict": "VOID",
            "error": str(e),
            "authority_notice": AUTHORITY_NOTICE,
        }


# ==============================================================================
# 6. _trinity_ (The Loop)
# ==============================================================================
async def mcp_trinity(
    query: str = "", session_id: Optional[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    _trinity_: Full Metabolic Loop (AGI->ASI->APEX->VAULT).
    """
    kwargs = _normalize_kwargs(kwargs)
    query = kwargs.pop("query", query) or ""
    session_id = kwargs.pop("session_id", session_id) or get_current_session_id()

    return await bridge_trinity_loop_router(query=query, session_id=session_id, **kwargs)


# ==============================================================================
# 7. _reality_ (The Ground)
# ==============================================================================
async def mcp_reality(
    query: str = "", session_id: Optional[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    _reality_: External Fact-Checking & Grounding.
    """
    kwargs = _normalize_kwargs(kwargs)
    query = kwargs.pop("query", query) or ""
    session_id = kwargs.pop("session_id", session_id) or get_current_session_id()

    if not query.strip():
        return {
            "status": "VOID",
            "verdict": "VOID",
            "reason": "Empty query — provide a question to fact-check.",
            "source": "none",
        }

    try:
        result = await bridge_reality_check_router(query=query, session_id=session_id, **kwargs)

        # Meta-Atlas Fallback Protocol (v55.2)
        # If external sensor fails (Circuit Breaker/API Error), guide the Agent to self-correct.
        if result.get("status") in ["SABAR", "VOID", "ERROR"] or "error" in result:
            result["fallback_guidance"] = (
                "⚠️ EXTERNAL SENSOR OFFLINE (Circuit Breaker Active). "
                "The Agent MUST now initiate internal web search capabilities with **Meta-Atlas Protocol**: "
                "1. **Humility (F7)**: Explicitly state that arifOS sensors are offline and you are using fallback tools. "
                "2. **Map Topology**: Search for 'Context of [X]', 'Opposing views to [X]', and 'Source credibility'. "
                "3. **Triangulate (F2)**: Verify facts across at least 3 distinct domains/sources. "
                "4. **Recursive Depth**: Drill down into unclear concepts before synthesizing."
            )
            # Ensure verdict allows for manual intervention if it was VOID
            if result.get("verdict") == "VOID":
                result["verdict"] = "SABAR"  # Shift to SABAR to allow agent action

        # F4 Clarity: Schema validation (v55.3)
        if SCHEMA_VALIDATION_AVAILABLE:
            validate_reality_output(result, strict=SCHEMA_STRICT_MODE)

        return result

    except Exception as e:
        logger.error(f"[REALITY_CHECK] Error: {e}")
        return {
            "status": "ERROR",
            "verdict": "SABAR",  # Allow fallback
            "error": {"message": str(e), "code": "INTERNAL_ERROR"},
            "session_id": session_id,
            "fallback_guidance": (
                "⚠️ SYSTEM ERROR in Reality Bridge. "
                "The Agent MUST initiate internal web search capabilities (Meta-Atlas Protocol). "
                "Triangulate facts and cite sources explicitly (F7)."
            ),
        }
