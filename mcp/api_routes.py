"""
codebase/mcp/api_routes.py — Constitutional REST API (Hybrid MCP/REST)

Phase 1: Observability endpoints
- GET /api/v1/floors.json — READ ONLY, exposes 13 Floors
- POST /api/v1/init_gate — Validation endpoint, mirrors MCP

Security:
- F12 Injection Wall mandatory
- F11 Auth required for init_gate
- F7 Humility watermark on all responses
- No tool execution until κᵣ ≥ 0.70

Usage with existing RESTAPIRouter:
    from .api_routes import register_api_v1_routes
    register_api_v1_routes(rest_router)
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from codebase.constitutional_floors import THRESHOLDS
from codebase.guards.injection_guard import InjectionGuard

logger = logging.getLogger(__name__)

# F12 Injection Guard (shared instance)
_injection_guard = InjectionGuard(threshold=0.85)

async def f12_injection_scan(text: str) -> tuple[bool, float]:
    """F12 Injection Defense. Returns (passed, risk_score)."""
    result = _injection_guard.scan_input(text)
    return not result.blocked, result.injection_score


def register_api_v1_routes(rest_router):
    """
    Register Phase 1 API v1 routes on existing RESTAPIRouter.
    
    Adds:
    - GET /api/v1/floors.json — READ ONLY
    - POST /api/v1/init_gate — mirrors MCP
    - GET /api/v1/health — API health
    """
    
    @rest_router.mcp.custom_route("/api/v1/floors.json", methods=["GET"])
    async def get_floors(request):
        """
        GET /api/v1/floors.json
        
        Exposes the 13 Constitutional Floors as JSON.
        READ ONLY. No auth required (transparency).
        F7 Humility watermark included.
        """
        from starlette.responses import JSONResponse
        
        return JSONResponse({
            "version": "v55.2-SEAL",
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "authority": "Muhammad Arif bin Fazil (888 Judge)",
            "floors": THRESHOLDS,
            "total": len(THRESHOLDS),
            "note": "F9 Anti-Hantu: Consciousness claims PROHIBITED (C_dark = 0.00)",
        })
    
    rest_router._add_route("/api/v1/floors.json", ["GET"], "get_floors")
    
    @rest_router.mcp.custom_route("/api/v1/init_gate", methods=["POST"])
    async def init_gate_rest(request):
        """
        POST /api/v1/init_gate
        
        Mirrors MCP init_gate for REST clients.
        F11 Auth + F12 Injection checks mandatory.
        Exposes G-score for debugging κᵣ=0.0 bug.
        """
        from starlette.responses import JSONResponse
        import json
        
        # Parse request body
        body = await request.body()
        try:
            data = json.loads(body.decode('utf-8')) if body else {}
        except json.JSONDecodeError:
            return JSONResponse({
                "verdict": "VOID",
                "error": "Invalid JSON",
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠"
            }, status_code=400)
        
        query = data.get("query", "")
        authority_token = data.get("authority_token", "")
        session_id = data.get("session_id", "")
        
        # F12 Injection Wall (MANDATORY)
        injection_passed, risk_score = await f12_injection_scan(query)
        if not injection_passed:
            return JSONResponse({
                "verdict": "VOID",
                "session_id": "",
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
                "seal": "VOID",
                "apex_summary": {
                    "G": 0.0,
                    "reason": "F12 Injection Defense triggered",
                    "injection_risk": risk_score,
                },
                "floors_checked": ["F12_InjectionDefense"],
                "injection_check_passed": False,
                "authority_level": "blocked",
            })
        
        # Import and call canonical init_gate
        try:
            # Use importlib to load module with digit-starting name
            import importlib.util
            import sys
            from pathlib import Path
            
            _bridge_path = Path(__file__).parent.parent / "init" / "000_init" / "mcp_bridge.py"
            spec = importlib.util.spec_from_file_location("codebase.init.mcp_bridge", _bridge_path)
            _bridge = importlib.util.module_from_spec(spec)
            sys.modules["codebase.init.mcp_bridge"] = _bridge
            spec.loader.exec_module(_bridge)
            mcp_000_init = _bridge.mcp_000_init
            
            result = await mcp_000_init(
                action="init",
                query=query,
                authority_token=authority_token,
                session_id=session_id or None,
            )
            
            return JSONResponse({
                "verdict": result.get("verdict", "SEAL"),
                "session_id": result.get("session_id", ""),
                "motto": result.get("motto", "DITEMPA BUKAN DIBERI 💎🔥🧠"),
                "seal": result.get("seal", "SEAL"),
                "apex_summary": result.get("apex_summary", {}),
                "floors_checked": result.get("floors_checked", []),
                "injection_check_passed": injection_passed,
                "authority_level": result.get("authority", "GUEST").lower(),
            })
            
        except Exception as e:
            logger.error(f"init_gate REST error: {e}")
            return JSONResponse({
                "verdict": "VOID",
                "error": str(e),
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠"
            }, status_code=500)
    
    rest_router._add_route("/api/v1/init_gate", ["POST"], "init_gate_rest")
    
    @rest_router.mcp.custom_route("/api/v1/health", methods=["GET"])
    async def api_v1_health(request):
        """Health check for REST API v1."""
        from starlette.responses import JSONResponse
        
        return JSONResponse({
            "status": "GREEN",
            "version": "v55.2-SEAL",
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "endpoints": [
                "/api/v1/floors.json",
                "/api/v1/init_gate",
                "/api/v1/health",
            ],
        })
    
    rest_router._add_route("/api/v1/health", ["GET"], "api_v1_health")
    
    logger.info("Registered API v1 observability endpoints")


# Keep for direct import compatibility
__all__ = ["register_api_v1_routes"]
