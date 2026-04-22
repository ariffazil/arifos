"""
ChatGPT MCP Tools — Deep Research + Chat Mode Compatible

Implements OpenAI's required tool interface for MCP integration:
- search: Returns document IDs matching query
- fetch: Returns full document content by ID

All tools marked with readOnlyHint for seamless ChatGPT experience.
"""

from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

# In-memory cache for search results (mapping id -> document)
_search_cache: dict[str, dict[str, Any]] = {}


async def search(query: str) -> dict[str, Any]:
    """
    Search for documents matching the query.
    
    ChatGPT Deep Research compatible tool.
    Returns document IDs that can be fetched for full content.
    
    Args:
        query: Search query string
        
    Returns:
        {"results": [{"id": str, "title": str, "url": str}]}
    """
    # Lazy import to avoid circular dependencies at module load
    from arifosmcp.runtime.megaTools.tool_08_physics_reality import physics_reality
    
    logger.info(f"[ChatGPT] search query: {query}")
    
    try:
        # Use physics_reality in search mode to find information
        result = await physics_reality(
            mode="search",
            payload={"query": query, "limit": 10}
        )
        
        # Extract results from arifOS response
        payload = result.payload if hasattr(result, 'payload') else result
        
        if isinstance(payload, dict):
            hits = payload.get("results", payload.get("hits", []))
        else:
            hits = []
        
        # Transform to ChatGPT expected format
        chatgpt_results = []
        for idx, hit in enumerate(hits):
            doc_id = hit.get("id") or f"doc-{idx}"
            title = hit.get("title") or hit.get("name") or f"Result {idx + 1}"
            url = hit.get("url") or hit.get("source") or ""
            
            # Cache for fetch()
            _search_cache[doc_id] = {
                "id": doc_id,
                "title": title,
                "text": hit.get("text") or hit.get("content") or hit.get("snippet", ""),
                "url": url,
                "metadata": {k: v for k, v in hit.items() if k not in ["id", "title", "text", "content", "snippet", "url"]}
            }
            
            chatgpt_results.append({
                "id": doc_id,
                "title": title,
                "url": url
            })
        
        # Return in MCP content format
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"results": chatgpt_results})
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"[ChatGPT] search error: {e}")
        return {
            "content": [
                {
                    "type": "text", 
                    "text": json.dumps({"results": [], "error": str(e)})
                }
            ]
        }


async def fetch(id: str) -> dict[str, Any]:
    """
    Fetch full document content by ID.
    
    ChatGPT Deep Research compatible tool.
    Retrieves complete document for citation.
    
    Args:
        id: Document ID from search results
        
    Returns:
        {"id": str, "title": str, "text": str, "url": str, "metadata": dict}
    """
    # Lazy import to avoid circular dependencies at module load
    from arifosmcp.runtime.megaTools.tool_07_engineering_memory import engineering_memory
    
    logger.info(f"[ChatGPT] fetch id: {id}")
    
    try:
        # Check cache first
        if id in _search_cache:
            doc = _search_cache[id]
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(doc)
                    }
                ]
            }
        
        # Try to fetch from vector memory
        result = await engineering_memory(
            mode="vector_query",
            payload={"id": id}
        )
        
        payload = result.payload if hasattr(result, 'payload') else result
        
        if isinstance(payload, dict) and "content" in payload:
            doc = {
                "id": id,
                "title": payload.get("title", "Untitled"),
                "text": payload["content"],
                "url": payload.get("url", ""),
                "metadata": payload.get("metadata", {})
            }
        else:
            doc = {
                "id": id,
                "title": "Not Found",
                "text": "Document not found in knowledge base.",
                "url": "",
                "metadata": {}
            }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(doc)
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"[ChatGPT] fetch error: {e}")
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "id": id,
                        "title": "Error",
                        "text": f"Failed to fetch document: {str(e)}",
                        "url": "",
                        "metadata": {}
                    })
                }
            ]
        }


async def decide(query: str) -> dict[str, Any]:
    """
    Constitutional decision evaluation for a proposed action.
    
    Runs 888_JUDGE and returns verdict, failed floors, and recommendation.
    """
    from arifosmcp.runtime.tools import arifos_judge
    
    logger.info(f"[ChatGPT] decide query: {query}")
    
    try:
        result = await arifos_judge(
            candidate_action=query,
            risk_tier="medium",
            dry_run=True,
        )
        payload = result.payload if hasattr(result, 'payload') else result
        if isinstance(payload, dict):
            # Nested primary_artifact payload (current runtime shape)
            artifact = payload.get("primary_artifact", {}) or {}
            artifact_payload = artifact.get("payload", {}) if isinstance(artifact, dict) else {}

            # Verdict: try envelope enum first, then artifact payload
            verdict = "SEAL"
            if hasattr(result, "verdict") and result.verdict is not None:
                verdict_str = str(result.verdict)
                # Verdict enum names are like 'Verdict.SEAL' or 'SEAL'
                verdict = verdict_str.split(".")[-1]
            elif isinstance(artifact_payload, dict):
                verdict = artifact_payload.get("verdict", "SEAL")

            # Floors: extract failures from artifact floors dict
            floors = artifact_payload.get("floors", {}) if isinstance(artifact_payload, dict) else {}
            floors_failed = [k for k, v in (floors.items() if isinstance(floors, dict) else []) if v != "pass"] if floors else []

            # Recommendation: reasoning summary or default
            reasoning = artifact_payload.get("reasoning", {}) if isinstance(artifact_payload, dict) else {}
            recommendation = reasoning.get("summary") if isinstance(reasoning, dict) else None
            if not recommendation:
                recommendation = artifact_payload.get("summary") if isinstance(artifact_payload, dict) else None
            if not recommendation:
                recommendation = "No recommendation available."
        else:
            verdict = "VOID"
            floors_failed = []
            recommendation = "Invalid judge response"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "verdict": verdict,
                        "floors_failed": floors_failed,
                        "recommendation": recommendation,
                    })
                }
            ]
        }
    except Exception as e:
        logger.error(f"[ChatGPT] decide error: {e}")
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "verdict": "VOID",
                        "floors_failed": ["ALL"],
                        "recommendation": f"Decision evaluation failed: {str(e)}",
                    })
                }
            ]
        }


# Tool registry for direct access
chatgpt_tools = {
    "search": search,
    "fetch": fetch,
    "decide": decide,
}


# Convenience function to register all ChatGPT tools on FastMCP instance
def register_chatgpt_tools(mcp) -> None:
    """Register search and fetch tools for ChatGPT Deep Research compatibility."""
    
    # Simple async tool registration - let FastMCP handle the async
    @mcp.tool(annotations={"readOnlyHint": True})
    async def search_tool(query: str) -> dict:
        """Search for documents matching the query. Returns document IDs."""
        return await search(query)
    
    @mcp.tool(annotations={"readOnlyHint": True})
    async def fetch_tool(id: str) -> dict:
        """Fetch full document content by ID from search results."""
        return await fetch(id)
    
    @mcp.tool(annotations={"readOnlyHint": True})
    async def decide_tool(query: str) -> dict:
        """Evaluate a proposed action through constitutional judgment (888_JUDGE)."""
        return await decide(query)
    
    logger.info("[ChatGPT] Registered search, fetch, and decide tools for Deep Research")
