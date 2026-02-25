"""
aaa_mcp/external_gateways/brave_client.py — Brave Search Client

Constitutional Compliance:
- F1 Amanah: API key loaded securely from environment
- F2 Truth: Returns clear status when key missing
- F7 Humility: Graceful degradation with NO_API_KEY status
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

# Environment variable name for API key
BRAVE_API_KEY_ENV = "BRAVE_API_KEY"


class BraveSearchClient:
    """Brave Search API client with automatic environment key loading.

    Usage:
        # Auto-load from BRAVE_API_KEY env var
        client = BraveSearchClient()

        # Or explicit key
        client = BraveSearchClient(api_key="your-key")
    """

    def __init__(self, api_key: str | None = None):
        """Initialize client with API key from param or environment.

        Args:
            api_key: Explicit API key. If None, reads from BRAVE_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get(BRAVE_API_KEY_ENV)

    async def search(self, query: str, intent: str = "general", scar_weight: float = 0.0) -> dict:
        if not self.api_key:
            return {"query": query, "results": [], "intent": intent, "status": "NO_API_KEY"}

        # Brave Search API (web search)
        endpoint = "https://api.search.brave.com/res/v1/web/search"
        params = urllib.parse.urlencode({"q": query})
        url = f"{endpoint}?{params}"

        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("X-Subscription-Token", self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"query": query, "results": [], "intent": intent, "status": f"ERROR: {e}"}

        results = []
        for item in (payload.get("web", {}) or {}).get("results", [])[:5]:
            results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "description": item.get("description"),
                }
            )

        return {"query": query, "results": results, "intent": intent, "status": "OK"}
