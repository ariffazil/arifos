"""
Simple HTTP Transport for Limited AI Platforms (v55.4)

Provides GET-based access to constitutional tools for AI platforms
that lack MCP client or POST capability (Qwen, some GPT instances).

Endpoints:
    GET /simple/init_gate?q={query}
    GET /simple/agi_sense?q={query}
    GET /simple/agi_think?q={query}
    GET /simple/agi_reason?q={query}
    GET /simple/asi_empathize?q={query}
    GET /simple/asi_align?q={query}
    GET /simple/apex_verdict?q={query}
    GET /simple/reality_search?q={query}

Returns simplified JSON with:
    - motto: "DITEMPA BUKAN DIBERI 💎🔥🧠"
    - verdict: SEAL/VOID/SABAR
    - apex_summary: {G, A, P, X, E2}
    - reasoning: human-readable explanation

Security:
    - Rate limited (30 req/min per IP)
    - No authentication required (read-only constitutional tools)
    - CORS enabled for browser/AI access
    - Query length limit: 500 chars

DITEMPA BUKAN DIBERI
"""

import logging
from typing import Any, Dict

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..core.tool_registry import ToolRegistry
from ..services.rate_limiter import get_rate_limiter

logger = logging.getLogger(__name__)

# Simple CORS headers for browser/AI access
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

# Tool name mapping
SIMPLE_TOOLS = {
    "init_gate": "Initialize constitutional session",
    "agi_sense": "Sense intent and lane",
    "agi_think": "Generate hypotheses",
    "agi_reason": "Deep reasoning",
    "asi_empathize": "Stakeholder analysis",
    "asi_align": "Ethical alignment",
    "apex_verdict": "Final verdict",
    "reality_search": "Fact checking",
}


class SimpleHTTPTransport:
    """
    GET-based transport for limited AI platforms.
    
    No authentication required - these are constitutional tools
    that perform governance, not privileged operations.
    """

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.rate_limiter = get_rate_limiter()

    def register_routes(self, mcp_app):
        """Register simple GET endpoints."""
        
        @mcp_app.custom_route("/simple", methods=["GET", "OPTIONS"])
        async def simple_root(request: Request):
            """List available simple endpoints."""
            if request.method == "OPTIONS":
                return JSONResponse({}, headers=CORS_HEADERS)
            
            return JSONResponse({
                "message": "Simple HTTP Transport for Limited AI Platforms",
                "version": "v55.4",
                "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
                "endpoints": {
                    tool: f"/simple/{tool}?q=your+question"
                    for tool in SIMPLE_TOOLS
                },
                "example": "/simple/init_gate?q=Should+I+build+this",
                "note": "Query length limit: 500 characters",
            }, headers=CORS_HEADERS)

        @mcp_app.custom_route("/simple/{tool_name}", methods=["GET", "OPTIONS"])
        async def simple_tool(request: Request):
            """Execute tool via GET request."""
            if request.method == "OPTIONS":
                return JSONResponse({}, headers=CORS_HEADERS)
            
            tool_name = request.path_params.get("tool_name")
            
            # Validate tool
            if tool_name not in SIMPLE_TOOLS:
                return JSONResponse({
                    "error": f"Unknown tool: {tool_name}",
                    "available": list(SIMPLE_TOOLS.keys()),
                }, status_code=404, headers=CORS_HEADERS)
            
            # Get query parameter
            query = request.query_params.get("q", "").strip()
            if not query:
                return JSONResponse({
                    "error": "Missing 'q' query parameter",
                    "example": f"/simple/{tool_name}?q=your+question",
                }, status_code=400, headers=CORS_HEADERS)
            
            if len(query) > 500:
                return JSONResponse({
                    "error": "Query too long (max 500 characters)",
                }, status_code=400, headers=CORS_HEADERS)
            
            # Rate limit check
            client_ip = request.client.host if request.client else "unknown"
            rate_result = self.rate_limiter.check(f"simple_{tool_name}", client_ip)
            if not rate_result.allowed:
                return JSONResponse({
                    "error": "Rate limit exceeded",
                    "retry_after": rate_result.reset_in_seconds,
                }, status_code=429, headers=CORS_HEADERS)
            
            # Execute tool
            try:
                result = await self._execute_tool(tool_name, query)
                return JSONResponse(result, headers=CORS_HEADERS)
            except Exception as e:
                logger.error(f"Simple transport error: {e}")
                return JSONResponse({
                    "error": "Tool execution failed",
                    "details": str(e),
                    "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
                }, status_code=500, headers=CORS_HEADERS)

    async def _execute_tool(self, tool_name: str, query: str) -> Dict[str, Any]:
        """Execute tool and return simplified response."""
        from ..tools.canonical_trinity import (
            mcp_init, mcp_agi, mcp_asi, mcp_apex, mcp_reality
        )
        
        # Generate session ID
        import uuid
        session_id = f"sess_{uuid.uuid4().hex[:16]}"
        
        # Execute based on tool type
        if tool_name == "init_gate":
            raw = await mcp_init(action="init", query=query, session_id=session_id)
            return self._simplify_init(raw)
        
        elif tool_name in ("agi_sense", "agi_think", "agi_reason"):
            action = tool_name.replace("agi_", "")
            raw = await mcp_agi(action=action, query=query, session_id=session_id)
            return self._simplify_agi(raw, tool_name)
        
        elif tool_name in ("asi_empathize", "asi_align"):
            action = tool_name.replace("asi_", "")
            raw = await mcp_asi(action=action, query=query, session_id=session_id)
            return self._simplify_asi(raw, tool_name)
        
        elif tool_name == "apex_verdict":
            raw = await mcp_apex(action="judge", query=query, session_id=session_id)
            return self._simplify_apex(raw)
        
        elif tool_name == "reality_search":
            raw = await mcp_reality(query=query, session_id=session_id)
            return self._simplify_reality(raw)
        
        else:
            return {"error": f"Tool {tool_name} not implemented"}

    def _simplify_init(self, raw: Dict) -> Dict[str, Any]:
        """Simplify init_gate response for limited clients."""
        apex = raw.get("apex_summary", {})
        return {
            "tool": "init_gate",
            "motto": raw.get("motto", "DITEMPA BUKAN DIBERI 💎🔥🧠"),
            "seal": "💎🔥🧠",
            "verdict": raw.get("verdict", "SEAL"),
            "session_id": raw.get("session_id"),
            "authority": raw.get("authority_level", "guest"),
            "intent_lane": raw.get("access_level", "SOFT"),
            "apex_genius": {
                "G": apex.get("G", 0),
                "A": apex.get("A", 0),  # AGI Mind
                "P": apex.get("P", 0),  # APEX Soul  
                "X": apex.get("X", 0),  # ASI Heart
                "E2": apex.get("E2", 0), # Earth/Energy
                "formula": "G = A × P × X × E²",
            },
            "floors_checked": 13,
            "injection_safe": raw.get("injection_check_passed", True),
            "reasoning": raw.get("reason", "Constitutional session initialized"),
            "next_tools": [
                "agi_sense", "agi_think", "agi_reason",
                "asi_empathize", "asi_align", "apex_verdict"
            ],
            "_links": {
                "agi_sense": f"/simple/agi_sense?q={{continue}}",
                "apex_verdict": f"/simple/apex_verdict?q={{conclude}}",
            }
        }

    def _simplify_agi(self, raw: Dict, tool: str) -> Dict[str, Any]:
        """Simplify AGI tool response."""
        return {
            "tool": tool,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "verdict": raw.get("verdict", "SEAL"),
            "session_id": raw.get("session_id"),
            "confidence": raw.get("confidence", 0),
            "entropy_delta": raw.get("entropy_delta", 0),
            "reasoning": raw.get("conclusion") or raw.get("reasoning", ""),
            "intent": raw.get("intent"),
            "lane": raw.get("lane"),
            "options_count": len(raw.get("options", [])),
        }

    def _simplify_asi(self, raw: Dict, tool: str) -> Dict[str, Any]:
        """Simplify ASI tool response."""
        return {
            "tool": tool,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "verdict": raw.get("verdict", "SEAL"),
            "session_id": raw.get("session_id"),
            "empathy_kappa_r": raw.get("empathy_kappa_r", 0),
            "peace_squared": raw.get("peace_squared", 0),
            "stakeholders": len(raw.get("stakeholders", [])),
            "reversibility": raw.get("reversibility_score", 1.0),
        }

    def _simplify_apex(self, raw: Dict) -> Dict[str, Any]:
        """Simplify APEX tool response."""
        return {
            "tool": "apex_verdict",
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "verdict": raw.get("verdict", "SEAL"),
            "session_id": raw.get("session_id"),
            "final_verdict": raw.get("final_verdict"),
            "trinity_score": raw.get("trinity_score", 0),
            "constitutional_alignment": raw.get("constitutional_alignment", {}),
        }

    def _simplify_reality(self, raw: Dict) -> Dict[str, Any]:
        """Simplify reality_search response."""
        return {
            "tool": "reality_search",
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "verdict": raw.get("verdict", "SEAL"),
            "verified": raw.get("verified", False),
            "sources": raw.get("sources", []),
            "confidence": raw.get("confidence", 0),
        }
