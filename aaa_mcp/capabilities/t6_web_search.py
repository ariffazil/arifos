# aaa_mcp/capabilities/t6_web_search.py
# T6 Web Search — Brave Search API integration (v62 Step 2)
# Real evidence grounding for F2 Truth verification

import os
import hashlib
import json
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
import httpx

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"

@dataclass
class EvidenceArtifact:
    """Structured evidence from web search."""
    source: str        # URL
    snippet: str       # Relevant text
    title: str         # Page title
    timestamp: str     # ISO 8601
    query: str         # Original search query
    content_hash: str  # SHA-256 of snippet
    
    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "snippet": self.snippet[:500],  # Truncate for safety
            "title": self.title,
            "timestamp": self.timestamp,
            "query": self.query,
            "content_hash": self.content_hash
        }

async def brave_search(query: str, count: int = 5) -> List[EvidenceArtifact]:
    """
    Search Brave API and return evidence artifacts.
    
    Args:
        query: Search query
        count: Number of results (max 20)
    
    Returns:
        List of EvidenceArtifact objects
    """
    if not BRAVE_API_KEY:
        raise ValueError("BRAVE_API_KEY not configured")
    
    headers = {
        "X-Subscription-Token": BRAVE_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": 0,
        "mkt": "en-US",  # Market (can be parameterized)
        "safesearch": "moderate"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BRAVE_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Brave API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise ValueError(f"Search failed: {str(e)}")
    
    artifacts = []
    web_results = data.get("web", {}).get("results", [])
    
    for result in web_results[:count]:
        snippet = result.get("description", "")
        url = result.get("url", "")
        title = result.get("title", "")
        
        # Generate content hash
        content_hash = hashlib.sha256(f"{url}{snippet}".encode()).hexdigest()[:16]
        
        artifact = EvidenceArtifact(
            source=url,
            snippet=snippet,
            title=title,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query=query,
            content_hash=content_hash
        )
        artifacts.append(artifact)
    
    return artifacts

def format_evidence_for_context(artifacts: List[EvidenceArtifact]) -> str:
    """Format evidence artifacts as context string."""
    if not artifacts:
        return ""
    
    context_parts = []
    for i, art in enumerate(artifacts[:3], 1):  # Top 3 results
        context_parts.append(f"[{i}] {art.title}\n{art.snippet}\nSource: {art.source}")
    
    return "\n\n".join(context_parts)
