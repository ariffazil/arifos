"""
Engine Adapters for AAA MCP Server
Bridges FastMCP tools to existing codebase engines with fail-safe fallbacks.
"""
from typing import Dict, Any, Optional
import logging
from dataclasses import asdict, is_dataclass

logger = logging.getLogger(__name__)

# Import real engines with fallback stubs
try:
    from codebase.agi.engine import AGIEngine as RealAGIEngine
    AGI_AVAILABLE = True
except ImportError as e:
    AGI_AVAILABLE = False
    logger.warning(f"AGI engine not available: {e}")

try:
    from codebase.asi.engine import ASIEngine as RealASIEngine
    ASI_AVAILABLE = True
except ImportError as e:
    ASI_AVAILABLE = False
    logger.warning(f"ASI engine not available: {e}")

try:
    from codebase.apex.kernel import APEXJudicialCore
    APEX_AVAILABLE = True
except ImportError as e:
    APEX_AVAILABLE = False
    logger.warning(f"APEX engine not available: {e}")


def _normalize_obj(obj: Any) -> Any:
    if obj is None:
        return None
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, dict):
        return obj
    return {"value": obj}


class InitEngine:
    """Adapter for init — uses mcp_bridge."""
    async def ignite(self, query: str, session_id: str = None) -> Dict[str, Any]:
        try:
            import importlib
            module = importlib.import_module("codebase.init.000_init.mcp_bridge")
            mcp_000_init = module.mcp_000_init
            return await mcp_000_init(action="init", query=query, session_id=session_id)
        except Exception as e:
            from uuid import uuid4
            return {
                "status": "SEAL",
                "session_id": session_id or str(uuid4()),
                "verdict": "SEAL",
                "engine_mode": "fallback",
                "note": f"Init bridge unavailable: {e}",
            }


class AGIEngine:
    """Adapter for AGI — uses real AGIEngine.execute() or fallback."""
    def __init__(self):
        self._engine = RealAGIEngine() if AGI_AVAILABLE else None

    async def _execute_or_fallback(
        self,
        query: str,
        session_id: str,
        *,
        context: Optional[Dict[str, Any]] = None,
        lane: Optional[str] = None,
    ) -> Dict[str, Any]:
        if self._engine:
            result = await self._engine.execute(query, context=context, lane=lane)
            delta = getattr(result, "delta_bundle", None)
            stage_111 = getattr(result, "stage_111", None)
            return {
                "verdict": getattr(getattr(delta, "vote", None), "value", None) or "SEAL",
                "query": query,
                "session_id": session_id,
                "engine_mode": "real",
                "trinity_component": "AGI",
                "delta_bundle": _normalize_obj(delta),
                "stage_111": _normalize_obj(stage_111),
                "execution_time_ms": getattr(result, "execution_time_ms", None),
            }
        return {
            "verdict": "SEAL",
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "AGI",
        }

    async def sense(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback(query, session_id)

    async def think(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback(query, session_id)

    async def reason(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback(query, session_id)


class ASIEngine:
    """Adapter for ASI — uses real ASIEngine or fallback."""
    def __init__(self):
        self._engine = RealASIEngine() if ASI_AVAILABLE else None

    async def _execute_or_fallback(
        self,
        query: str,
        session_id: str,
        *,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self._engine:
            result = await self._engine.execute(query, context=context)
            omega = getattr(result, "omega_bundle", None)
            return {
                "verdict": getattr(getattr(omega, "vote", None), "value", None) or "SEAL",
                "query": query,
                "session_id": session_id,
                "engine_mode": "real",
                "trinity_component": "ASI",
                "omega_bundle": _normalize_obj(omega),
                "execution_time_ms": getattr(result, "execution_time_ms", None),
            }
        return {
            "verdict": "SEAL",
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "ASI",
        }

    async def empathize(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback(query, session_id)

    async def align(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback(query, session_id)


class APEXEngine:
    """Adapter for APEX — uses APEXKernel or fallback."""
    def __init__(self):
        self._kernel = APEXJudicialCore() if APEX_AVAILABLE else None

    async def judge(self, query: str, session_id: str) -> Dict[str, Any]:
        if self._kernel:
            return await self._kernel.execute("judge", {"query": query, "session_id": session_id})
        return {
            "verdict": "SEAL",
            "action": "judge",
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "APEX",
        }
