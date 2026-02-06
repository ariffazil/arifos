"""
aaa_mcp/bridge.py — Constitutional Bridge (v55.5-HARDENED)

Routes MCP tool calls to the appropriate kernel engines.
Provides fallback responses when engines are unavailable.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

from aaa_mcp.external_gateways.brave_client import BraveSearchClient
from aaa_mcp.services.constitutional_metrics import get_stage_result, store_stage_result
from aaa_mcp.tools.trinity_validator import validate_trinity_request

# Initialize logger
logger = logging.getLogger(__name__)

# --- CORE AVAILABILITY ---
try:
    from codebase.kernel import get_kernel_manager

    ENGINES_AVAILABLE = True
except ImportError:
    logger.warning("arifOS Cores unavailable - Bridge in degraded mode")

    def get_kernel_manager():
        return None

    ENGINES_AVAILABLE = False


# --- ERROR CATEGORIZATION ---
class BridgeError(Exception):
    """Base class for bridge errors."""

    def __init__(self, message: str, category: str = "FATAL", status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.category = category
        self.status_code = status_code

    def to_dict(self) -> dict:
        return {
            "status": "VOID",
            "verdict": "VOID",
            "error_category": self.category,
            "reason": self.message,
            "status_code": self.status_code,
        }


_FALLBACK_RESPONSE = BridgeError("arifOS Cores unavailable", "FATAL", 503).to_dict()


# --- UTILS ---
def _serialize(obj: Any) -> Any:
    """Zero-logic serialization for transport."""
    if obj is None:
        return None
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    if hasattr(obj, "__dataclass_fields__"):
        from dataclasses import asdict

        return asdict(obj)
    if isinstance(obj, (list, tuple)):
        return [_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if hasattr(obj, "value") and not isinstance(obj, (int, float, str, bool)):
        return obj.value
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if hasattr(obj, "__dict__"):
        return {k: _serialize(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    return str(obj)


# --- ROUTERS ---


async def bridge_init_router(action: str = "init", **kwargs) -> dict:
    """Route to initialization engine."""
    if not ENGINES_AVAILABLE:
        return _FALLBACK_RESPONSE
    try:
        manager = get_kernel_manager()
        if manager is None:
            raise BridgeError("Kernel manager not initialized.", "ENGINE_FAILURE", 500)
        result = await manager.init_session(action, kwargs)
        serialized = _serialize(result)
        session_id = (serialized or {}).get("session_id") if isinstance(serialized, dict) else None
        if session_id:
            store_stage_result(str(session_id), "init", serialized)
        return serialized if isinstance(serialized, dict) else {"result": serialized}
    except Exception as e:
        logger.error(f"Init Router Error: {e}")
        if isinstance(e, BridgeError):
            return e.to_dict()
        return BridgeError(str(e), "ENGINE_FAILURE").to_dict()


async def bridge_agi_router(
    query: str, session_id: Optional[str] = None, action: str = "reason", **kwargs
) -> dict:
    """Route to AGI Mind engine."""
    if not ENGINES_AVAILABLE:
        return _FALLBACK_RESPONSE

    # Validate request first
    is_valid, reason = validate_trinity_request(query, lane=kwargs.get("lane", "SOFT"))
    if not is_valid:
        return {
            "verdict": "VOID",
            "reason": reason,
            "session_id": session_id,
            "motto": "DITEMPA BUKAN DIBERI",
        }

    try:
        manager = get_kernel_manager()
        if manager is None:
            raise BridgeError("Kernel manager not initialized.", "ENGINE_FAILURE", 500)

        kernel = manager.get_agi()
        result = await kernel.execute(action, {"query": query, "session_id": session_id, **kwargs})
        serialized = _serialize(result)

        if session_id:
            store_stage_result(session_id, "agi", serialized)

        return serialized if isinstance(serialized, dict) else {"result": serialized}
    except Exception as e:
        logger.error(f"AGI Router Error: {e}")
        if isinstance(e, BridgeError):
            return e.to_dict()
        return BridgeError(str(e), "ENGINE_FAILURE").to_dict()


async def bridge_asi_router(
    query: str,
    reasoning: str = "",
    session_id: Optional[str] = None,
    action: str = "empathize",
    **kwargs,
) -> dict:
    """Route to ASI Heart engine."""
    if not ENGINES_AVAILABLE:
        return _FALLBACK_RESPONSE

    try:
        manager = get_kernel_manager()
        if manager is None:
            raise BridgeError("Kernel manager not initialized.", "ENGINE_FAILURE", 500)

        kernel = manager.get_asi()
        context = kwargs.get("context", {})
        if reasoning:
            context["reasoning"] = reasoning

        result = await kernel.execute(
            action,
            {"text": query, "query": query, "session_id": session_id, "context": context, **kwargs},
        )
        serialized = _serialize(result)

        if session_id:
            store_stage_result(session_id, "asi", serialized)

        return serialized if isinstance(serialized, dict) else {"result": serialized}
    except Exception as e:
        logger.error(f"ASI Router Error: {e}")
        if isinstance(e, BridgeError):
            return e.to_dict()
        return BridgeError(str(e), "ENGINE_FAILURE").to_dict()


async def bridge_apex_router(
    query: str,
    session_id: Optional[str] = None,
    verdict: str = "",
    action: str = "decide",
    **kwargs,
) -> dict:
    """Route to APEX Soul engine."""
    if not ENGINES_AVAILABLE:
        return _FALLBACK_RESPONSE

    try:
        manager = get_kernel_manager()
        if manager is None:
            raise BridgeError("Kernel manager not initialized.", "ENGINE_FAILURE", 500)

        kernel = manager.get_apex()
        kwargs["pre_verdict"] = verdict

        result = await kernel.execute(action, {"query": query, "session_id": session_id, **kwargs})
        serialized = _serialize(result)

        if session_id:
            store_stage_result(session_id, "apex", serialized)

        return serialized if isinstance(serialized, dict) else {"result": serialized}
    except Exception as e:
        logger.error(f"APEX Router Error: {e}")
        if isinstance(e, BridgeError):
            return e.to_dict()
        return BridgeError(str(e), "ENGINE_FAILURE").to_dict()


async def bridge_trinity_loop_router(
    query: str, session_id: Optional[str] = None, **kwargs
) -> dict:
    """
    Full Trinity metabolic loop: INIT → AGI → ASI → APEX.

    This is the complete pipeline for processing a query through
    all three engines with constitutional governance.
    """
    if not ENGINES_AVAILABLE:
        return _FALLBACK_RESPONSE

    # Validate first
    is_valid, reason = validate_trinity_request(query, lane=kwargs.get("lane", "SOFT"))
    if not is_valid:
        return {
            "verdict": "VOID",
            "reason": reason,
            "session_id": session_id,
            "stages": [],
            "motto": "DITEMPA BUKAN DIBERI",
        }

    stages = []

    try:
        # Stage 1: AGI Mind
        agi_result = await bridge_agi_router(query, session_id, action="reason", **kwargs)
        stages.append({"stage": "AGI", "result": agi_result})

        if agi_result.get("verdict") == "VOID":
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "stages": stages,
                "halted_at": "AGI",
                "motto": "DITEMPA BUKAN DIBERI",
            }

        # Stage 2: ASI Heart
        reasoning = agi_result.get("reasoning", agi_result.get("conclusion", ""))
        asi_result = await bridge_asi_router(
            query, reasoning, session_id, action="empathize", **kwargs
        )
        stages.append({"stage": "ASI", "result": asi_result})

        if asi_result.get("verdict") == "VOID":
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "stages": stages,
                "halted_at": "ASI",
                "motto": "DITEMPA BUKAN DIBERI",
            }

        # Stage 3: APEX Soul
        apex_result = await bridge_apex_router(query, session_id, action="decide", **kwargs)
        stages.append({"stage": "APEX", "result": apex_result})

        return {
            "verdict": apex_result.get("verdict", "SEAL"),
            "session_id": session_id,
            "stages": stages,
            "motto": "DITEMPA BUKAN DIBERI",
        }

    except Exception as e:
        logger.error(f"Trinity Loop Error: {e}")
        return {
            "verdict": "VOID",
            "session_id": session_id,
            "stages": stages,
            "error": str(e),
            "motto": "DITEMPA BUKAN DIBERI",
        }


async def bridge_reality_check_router(query: str = "", **kwargs) -> dict:
    """Route to reality grounding via Brave Search."""
    from aaa_mcp.tools import reality_grounding

    return await reality_grounding.reality_check(query)
