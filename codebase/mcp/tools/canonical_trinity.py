"""
codebase/mcp/tools/canonical_trinity.py

The 7 Canonical Tools of arifOS (AAA Framework)
Implementing the "Trinity of Constitutional Verdicts" and metabolic cycle.

LLM-Agnostic: Works with Claude, ChatGPT, Gemini, Cursor, Codex, any MCP client.
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

import uuid
from typing import Any, Dict, Optional, List
from codebase.kernel import get_kernel_manager
from codebase.mcp.core.bridge import (
    bridge_trinity_loop_router,
    bridge_reality_check_router,
    bridge_atlas_router,
)


def _normalize_kwargs(kwargs: dict) -> dict:
    """
    LLM-agnostic input normalizer.
    Some MCP clients (ChatGPT) wrap tool parameters under 'args' or 'kwargs'.
    This unwraps them so handlers receive flat keyword arguments.
    """
    # ChatGPT wraps params under 'args' dict
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
    result["root_key"] = "TOY_MODE"

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
        # Keep original helpful data
        "original_status": result.get("status"),
        "reason": result.get("reason"),
        "motto": result["motto"],
    }

    return adapted_result


# ==============================================================================
# 2. _agi_ (The Mind)
# ==============================================================================
async def mcp_agi(
    action: str = "full", query: str = "", session_id: Optional[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    _agi_: Mind Engine (Δ) - Logic, Sense, Think, Map.
    """
    kwargs = _normalize_kwargs(kwargs)
    action = kwargs.pop("action", action) or "full"
    query = kwargs.pop("query", query) or ""
    session_id = kwargs.pop("session_id", session_id)

    kernel = get_kernel_manager().get_agi()
    
    try:
        raw_result = await kernel.execute(action, {"query": query, "session_id": session_id, **kwargs})
    except Exception as e:
        # Handle errors gracefully
        return {
            "session_id": session_id or "unknown",
            "entropy_delta": 0.0,
            "omega_0": 0.04,
            "precision": {},
            "hierarchical_beliefs": {},
            "action_policy": {},
            "vote": "VOID",
            "floor_scores": {},
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e),
                "suggestion": "Check action parameter or query format"
            }
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

    # Ensure required fields
    if "entropy_delta" not in result:
        # Try to calculate or default
        result["entropy_delta"] = result.get("clarity_score", 0.0) - 0.5  # Approximation

    if "vote" not in result:
        result["vote"] = result.get("status", "VOID")

    # Ensure schema compliance
    adapted = {
        "session_id": result.get("session_id", session_id),
        "entropy_delta": float(result.get("entropy_delta", 0.0)),
        "omega_0": float(result.get("omega_0", 0.04)),
        "precision": result.get("precision", {}),
        "hierarchical_beliefs": result.get("hierarchical_beliefs", {}),
        "action_policy": result.get("action_policy", {}),
        "vote": result.get("vote", "VOID"),
        "floor_scores": result.get("floor_scores", {}),
    }

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
    session_id = kwargs.pop("session_id", session_id)

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
        "vote": data.get("vote", "VOID"),
        "empathy_kappa_r": float(
            data.get("empathy", {}).get("kappa_r", 0.0)
            if isinstance(data.get("empathy"), dict)
            else 0.0
        ),
        "peace_squared": float(
            data.get("system", {}).get("peace_squared", 0.0)
            if isinstance(data.get("system"), dict)
            else 0.0
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
    session_id = kwargs.pop("session_id", session_id)

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
        "trinity_score": float(trinity_score),
        "paradox_scores": raw_result.get("paradox_scores", {}),
        "equilibrium": raw_result.get("equilibrium", {}),
        "constitutional_alignment": raw_result.get("constitutional_alignment", {}),
        "proof": raw_result.get("proof", {}),
    }

    return adapted


# ==============================================================================
# 5. _vault_ (The Seal)
# ==============================================================================
async def mcp_vault(
    action: str = "seal",
    verdict: str = "SEAL",
    decision_data: Optional[Dict] = None,
    target: str = "seal",
    session_id: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    _vault_: Immutable Ledger - Seal, List, Read.
    """
    kwargs = _normalize_kwargs(kwargs)
    action = kwargs.pop("action", action) or "seal"
    verdict = kwargs.pop("verdict", verdict) or "SEAL"
    session_id = kwargs.pop("session_id", session_id)
    if not session_id:
        session_id = str(uuid.uuid4())

    kernel = get_kernel_manager().get_apex()
    return await kernel.execute(
        "seal" if action == "seal" else action,
        {
            "session_id": session_id,
            "verdict": verdict,
            "data": decision_data,
            "target_ledger": target,
            **kwargs,
        },
    )


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
    session_id = kwargs.pop("session_id", session_id)

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
    session_id = kwargs.pop("session_id", session_id)

    if not query.strip():
        return {
            "status": "VOID",
            "verdict": "VOID",
            "reason": "Empty query — provide a question to fact-check.",
            "source": "none",
        }

    return await bridge_reality_check_router(query=query, session_id=session_id, **kwargs)
