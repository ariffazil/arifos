"""
aaa_mcp/tools/reality_grounding.py — Reality Grounding

Provides external fact-checking via:
1. Brave Search API (if BRAVE_API_KEY is set)
2. DuckDuckGo Search (no API key required)
3. Web browser fetching for source verification
"""

from __future__ import annotations

import os
from typing import Tuple, Dict, Any, List

# Try to import external gateways
try:
    from aaa_mcp.external_gateways.brave_client import BraveSearchClient
    BRAVE_AVAILABLE = True
except ImportError:
    BRAVE_AVAILABLE = False

try:
    from aaa_mcp.external_gateways.web_search_noapi import WebSearchNoAPI
    from aaa_mcp.external_gateways.web_browser import WebBrowser
    NOAPI_AVAILABLE = True
except ImportError:
    NOAPI_AVAILABLE = False

from codebase.enforcement.routing.prompt_router import route_refuse


def should_reality_check(
    query: str, lane: str, intent: str, scar_weight: float
) -> Tuple[bool, str]:
    """Determine if a reality check is needed."""
    # Simple heuristic: require checks for medical/finance/legal or explicit verification asks.
    q = query.lower()
    triggers = ("verify", "source", "citation", "evidence", "prove", "fact check", 
                "is it true", "confirm", "validate", "check if")
    if any(t in q for t in triggers):
        return True, "Explicit verification request"
    if any(t in q for t in ("medical", "health", "finance", "invest", "legal", "law", "diagnose")):
        return True, "High-stakes domain"
    # Check for temporal queries (recent events)
    temporal_markers = ("latest", "recent", "news", "today", "this week", "this month", "2024", "2025", "2026")
    if any(t in q for t in temporal_markers):
        return True, "Temporal query - may need current information"
    return False, "No external verification required"


class RealityGrounding:
    """Unified reality grounding with multiple backends."""
    
    def __init__(self):
        self.brave_api_key = os.getenv("BRAVE_API_KEY")
        self.brave_available = BRAVE_AVAILABLE and bool(self.brave_api_key)
        self.noapi_available = NOAPI_AVAILABLE
        
        self._brave_client: Any = None
        self._noapi_search: Any = None
        self._browser: Any = None
    
    async def _search_brave(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search using Brave API."""
        if not self.brave_available:
            return {"status": "UNAVAILABLE", "error": "Brave API not configured"}
        
        try:
            if self._brave_client is None:
                self._brave_client = BraveSearchClient(api_key=self.brave_api_key)
            
            results = await self._brave_client.search(
                query=query, 
                intent="reality", 
                scar_weight=0.0
            )
            
            return {
                "status": "OK",
                "engine": "brave",
                "results": results.get("results", [])
            }
        except Exception as e:
            return {"status": "ERROR", "engine": "brave", "error": str(e)}
    
    async def _search_noapi(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search using no-API-key methods (DuckDuckGo)."""
        if not self.noapi_available:
            return {"status": "UNAVAILABLE", "error": "No-API search not available"}
        
        try:
            if self._noapi_search is None:
                self._noapi_search = WebSearchNoAPI()
            
            result = await self._noapi_search.search(query, max_results=max_results)
            return result
        except Exception as e:
            return {"status": "ERROR", "engine": "noapi", "error": str(e)}
    
    async def _fetch_source(self, url: str) -> Dict[str, Any]:
        """Fetch and extract content from a source URL."""
        if not self.noapi_available:
            return {"status": "UNAVAILABLE", "error": "Browser not available"}
        
        try:
            if self._browser is None:
                self._browser = WebBrowser()
            
            result = await self._browser.open(url, method="auto")
            return result
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}
    
    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        fetch_sources: bool = False,
        max_sources_to_fetch: int = 3
    ) -> Dict[str, Any]:
        """
        Perform reality grounding search.
        
        Args:
            query: Query to search
            max_results: Max search results
            fetch_sources: Whether to fetch content from top sources
            max_sources_to_fetch: Number of top sources to fetch
        
        Returns:
            Dict with search results and optionally fetched content
        """
        results = {
            "query": query,
            "engines_used": [],
            "search_results": [],
            "sources_fetched": [],
            "errors": []
        }
        
        # Try Brave first if available
        if self.brave_available:
            brave_result = await self._search_brave(query, max_results)
            if brave_result["status"] == "OK":
                results["engines_used"].append("brave")
                results["search_results"] = brave_result.get("results", [])
        
        # Fallback to no-API search if Brave failed or unavailable
        if not results["search_results"] and self.noapi_available:
            noapi_result = await self._search_noapi(query, max_results)
            if noapi_result["status"] == "OK":
                results["engines_used"].append("duckduckgo")
                results["search_results"] = noapi_result.get("results", [])
            elif "error" in noapi_result:
                results["errors"].append(f"noapi: {noapi_result['error']}")
        
        # Fetch source content if requested
        if fetch_sources and results["search_results"] and self.noapi_available:
            for i, result in enumerate(results["search_results"][:max_sources_to_fetch]):
                url = result.get("url") or result.get("href", "")
                if url:
                    fetch_result = await self._fetch_source(url)
                    if fetch_result["status"] == "OK":
                        results["sources_fetched"].append({
                            "rank": i + 1,
                            "url": url,
                            "title": fetch_result.get("title", ""),
                            "content_preview": fetch_result.get("content", "")[:2000],
                            "source": fetch_result.get("source", "unknown")
                        })
        
        results["status"] = "OK" if results["search_results"] else "NO_RESULTS"
        results["results_count"] = len(results["search_results"])
        
        return results
    
    async def verify_claim(self, claim: str) -> Dict[str, Any]:
        """
        Verify a specific claim by searching for evidence.
        
        Args:
            claim: The claim to verify
        
        Returns:
            Dict with verification results
        """
        # Search for the claim
        search_query = f"{claim} fact check OR verify OR evidence"
        search_results = await self.search(
            search_query, 
            max_results=10, 
            fetch_sources=True,
            max_sources_to_fetch=3
        )
        
        return {
            "claim": claim,
            "verification_status": "REQUIRES_MANUAL_REVIEW",  # AI shouldn't auto-verify
            "search_results": search_results.get("search_results", []),
            "sources_examined": search_results.get("sources_fetched", []),
            "note": "Verification requires human judgment. Cross-reference multiple sources."
        }


# Singleton instance
_reality_grounding: RealityGrounding = None


def get_reality_grounding() -> RealityGrounding:
    """Get or create RealityGrounding singleton."""
    global _reality_grounding
    if _reality_grounding is None:
        _reality_grounding = RealityGrounding()
    return _reality_grounding


async def reality_check(query: str) -> dict:
    """
    Perform external reality grounding.
    
    This is the main entry point used by the MCP server.
    Tries Brave API first, falls back to DuckDuckGo (no API key).
    """
    refusal = route_refuse(query)
    needs_check, reason = should_reality_check(query, lane="SOFT", intent="", scar_weight=0.0)
    
    # Initialize grounding
    grounding = get_reality_grounding()
    
    # Perform search
    results = await grounding.search(
        query=query,
        max_results=10,
        fetch_sources=True,
        max_sources_to_fetch=2
    )
    
    # Build response
    response = {
        "status": results["status"],
        "query": query,
        "needs_check": needs_check,
        "reason": reason,
        "refusal": refusal.to_dict() if hasattr(refusal, "to_dict") else {},
        "engines_used": results.get("engines_used", []),
        "results_count": results.get("results_count", 0),
        "results": results.get("search_results", []),
    }
    
    # Add source content if fetched
    if results.get("sources_fetched"):
        response["sources_verified"] = results["sources_fetched"]
    
    # Add note about fallback
    if "brave" not in results.get("engines_used", []):
        if "duckduckgo" in results.get("engines_used", []):
            response["note"] = "Using DuckDuckGo (no API key required). For Brave API, set BRAVE_API_KEY."
        else:
            response["note"] = "No search engine available. Install 'ddgs' package: pip install ddgs"
    
    return response


async def open_web_page(url: str) -> dict:
    """
    Open and extract content from a web page.
    
    Can be called independently for web browsing capabilities.
    """
    if not NOAPI_AVAILABLE:
        return {
            "status": "ERROR",
            "url": url,
            "error": "Web browser not available. Install dependencies: pip install httpx beautifulsoup4 playwright"
        }
    
    grounding = get_reality_grounding()
    result = await grounding._fetch_source(url)
    return result
