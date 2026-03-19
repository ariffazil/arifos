"""aaa_mcp.external_gateways.perplexity_client

Perplexity search client.

This is an optional search provider used by the arifOS AAA MCP surface. Secrets
must be provided via environment variables (never committed):
- `PPLX_API_KEY` (preferred)
- `PERPLEXITY_API_KEY` (alias)

The Perplexity API is OpenAI-compatible (chat/completions).
"""

from __future__ import annotations

import json
import os
from typing import Any

import httpx

PPLX_API_KEY_ENV = "PPLX_API_KEY"
PERPLEXITY_API_KEY_ENV = "PERPLEXITY_API_KEY"
PPLX_MODEL_ENV = "PPLX_MODEL"


class PerplexitySearchClient:
    """Perplexity-backed search that returns a Brave-like result shape."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        endpoint: str = "https://api.perplexity.ai/chat/completions",
    ) -> None:
        self.api_key = api_key or os.getenv(PPLX_API_KEY_ENV) or os.getenv(PERPLEXITY_API_KEY_ENV)
        self.model = model or os.getenv(PPLX_MODEL_ENV) or "sonar-pro"
        self.endpoint = endpoint

    async def search(self, query: str, intent: str = "general", scar_weight: float = 0.0) -> dict:
        if not self.api_key:
            return {"query": query, "results": [], "intent": intent, "status": "NO_API_KEY"}

        system = (
            "You are a web search assistant. Return STRICT JSON only with shape: "
            '{"results":[{"title":"...","url":"https://...","description":"..."}]}. '
            "Include 1-5 high-signal links. No markdown."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": query},
            ],
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": 500,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(self.endpoint, headers=headers, json=payload)
                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
        except Exception as e:
            return {"query": query, "results": [], "intent": intent, "status": f"ERROR: {e}"}

        # Prefer explicit citations list if present.
        citations = data.get("citations")
        if isinstance(citations, list) and citations:
            results = []
            for idx, url in enumerate(citations[:5], start=1):
                if not isinstance(url, str) or not url.startswith("http"):
                    continue
                results.append({"title": url, "url": url, "description": ""})
            return {"query": query, "results": results, "intent": intent, "status": "OK"}

        # Fall back to parsing assistant content as JSON.
        content = (
            (((data.get("choices") or [{}])[0].get("message") or {}).get("content"))
            if isinstance(data, dict)
            else None
        )
        if not isinstance(content, str):
            return {"query": query, "results": [], "intent": intent, "status": "BAD_RESPONSE"}

        try:
            parsed = json.loads(content)
        except Exception:
            return {
                "query": query,
                "results": [],
                "intent": intent,
                "status": "BAD_JSON",
            }

        results = parsed.get("results") if isinstance(parsed, dict) else None
        if not isinstance(results, list):
            return {"query": query, "results": [], "intent": intent, "status": "BAD_SHAPE"}

        cleaned = []
        for item in results[:5]:
            if not isinstance(item, dict):
                continue
            url = item.get("url")
            if not isinstance(url, str) or not url.startswith("http"):
                continue
            cleaned.append(
                {
                    "title": str(item.get("title") or url),
                    "url": url,
                    "description": str(item.get("description") or ""),
                }
            )

        return {"query": query, "results": cleaned, "intent": intent, "status": "OK"}


__all__ = ["PerplexitySearchClient"]
