"""
aaa_mcp/external_gateways/brave_client.py — Brave Search Client
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Dict, Any


class BraveSearchClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

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
