"""
Engine Adapters for AAA MCP Server
Bridges FastMCP tools to existing codebase engines with fail-safe fallbacks.
"""
from typing import Dict, Any
import logging

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
    from codebase.apex.kernel import APEXKernel
    APEX_AVAILABLE = True
except ImportError as e:
    APEX_AVAILABLE = False
    logger.warning(f"APEX engine not available: {e}")


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

    async def _execute_or_fallback(self, action: str, query: str, session_id: str) -> Dict[str, Any]:
        if self._engine:
            return await self._engine.execute(action, {"query": query, "session_id": session_id})
        return {
            "verdict": "SEAL",
            "action": action,
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "AGI",
        }

    async def sense(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback("sense", query, session_id)

    async def think(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback("think", query, session_id)

    async def reason(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback("reason", query, session_id)


class ASIEngine:
    """Adapter for ASI — uses real ASIEngine or fallback."""
    def __init__(self):
        self._engine = RealASIEngine() if ASI_AVAILABLE else None

    async def _execute_or_fallback(self, action: str, query: str, session_id: str) -> Dict[str, Any]:
        if self._engine:
            return await self._engine.execute(action, {"query": query, "session_id": session_id})
        return {
            "verdict": "SEAL",
            "action": action,
            "query": query,
            "session_id": session_id,
            "engine_mode": "fallback",
            "trinity_component": "ASI",
        }

    async def empathize(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback("empathize", query, session_id)

    async def align(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._execute_or_fallback("align", query, session_id)


class APEXEngine:
    """Adapter for APEX — uses APEXKernel or fallback."""
    def __init__(self):
        self._kernel = APEXKernel() if APEX_AVAILABLE else None

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
