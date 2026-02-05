"""
aaa_mcp/bridge.py — Pure Bridge (v52.0.0)
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

from aaa_mcp.external_gateways.brave_client import BraveSearchClient

# Updated imports for aaa_mcp
from aaa_mcp.services.constitutional_metrics import get_stage_result, store_stage_result
from aaa_mcp.tools import reality_grounding
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


async def bridge_atlas_router(**kwargs) -> dict:
    return {"status": "MOCKED", "note": "Atlas router unavailable"}


async def bridge_trinity_loop_router(
    query: str, session_id: Optional[str] = None, **kwargs
) -> dict:
    """Mock trinity loop for now."""
    return {
        "verdict": "SEAL",
        "session_id": session_id or "mock_sess",
        "query": query,
        "stages": [],
        "motto": "DITEMPA BUKAN DIBERI",
    }


async def bridge_reality_check_router(**kwargs) -> dict:
    return await reality_grounding.reality_check(kwargs.get("query", ""))
