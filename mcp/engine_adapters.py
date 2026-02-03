"""
Engine Adapters for FastMCP Migration
Bridges FastMCP tools to existing working engines
"""
from typing import Dict, Any
import asyncio

# Import real engines
from codebase.agi.engine import AGIEngine as RealAGIEngine
from codebase.asi.engine import ASIEngine as RealASIEngine
from codebase.apex.kernel import APEXKernel

class InitEngine:
    """Adapter for init — uses mcp_bridge"""
    async def ignite(self, query: str, session_id: str = None) -> Dict[str, Any]:
        import importlib
        module = importlib.import_module("codebase.init.000_init.mcp_bridge")
        mcp_000_init = module.mcp_000_init
        result = await mcp_000_init(action="init", query=query, session_id=session_id)
        return result

class AGIEngine:
    """Adapter for AGI — uses real AGIEngine.execute()"""
    def __init__(self):
        self._engine = RealAGIEngine()
    
    async def sense(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._engine.execute("sense", {"query": query, "session_id": session_id})
    
    async def think(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._engine.execute("think", {"query": query, "session_id": session_id})
    
    async def reason(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._engine.execute("reason", {"query": query, "session_id": session_id})

class ASIEngine:
    """Adapter for ASI — uses real ASIEngine"""
    def __init__(self):
        self._engine = RealASIEngine()
    
    async def empathize(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._engine.execute("empathize", {"query": query, "session_id": session_id})
    
    async def align(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._engine.execute("align", {"query": query, "session_id": session_id})

class APEXEngine:
    """Adapter for APEX — uses APEXKernel"""
    def __init__(self):
        self._kernel = APEXKernel()
    
    async def judge(self, query: str, session_id: str) -> Dict[str, Any]:
        return await self._kernel.execute("judge", {"query": query, "session_id": session_id})
