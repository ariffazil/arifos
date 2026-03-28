"""
arifOS OpenAI Bridge — ChatGPT Company Knowledge MCP Schema

Thin wrapper that exposes arifOS search/fetch via OpenAI MCP schema.
Each tool returns MCP content array with JSON-encoded text payload.

OpenAI schema: https://developers.openai.com/docs/mcp
"""

from __future__ import annotations

import json
import os
from typing import Any

# Only load when bridge is enabled
if os.getenv("ARIFOS_OPENAI_BRIDGE", "0") != "1":
    __all__ = []
    __doc__ = None
else:
    from .runtime.reality_handlers import RealityHandler
    from .runtime.reality_models import BundleInput

    _handler = RealityHandler()

    # Default auth for anonymous bridge calls
    _ANON_AUTH = {
        "actor_id": "openai-bridge",
        "authority_level": "user",
        "token_fingerprint": None,
    }

    async def search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        OpenAI MCP search tool — ChatGPT company knowledge schema.

        Args:
            query: Free-text search query.
            top_k: Number of results to return (default 5).

        Returns:
            MCP content array with JSON-encoded {results: [{id, title, url, description}]}
        """
        bundle = BundleInput(type="query", value=query, top_k=top_k, fetch_top_k=0)
        bundle = await _handler.handle_compass(bundle, _ANON_AUTH)

        # Extract search results
        results = []
        for r in bundle.results:
            if hasattr(r, "results") and r.results:
                for item in r.results:
                    results.append({
                        "id": item.get("href", item.get("url", "")[:32]),
                        "title": item.get("title", "Untitled"),
                        "url": item.get("href", item.get("url", "")),
                    })

        return [{"type": "text", "text": json.dumps({"results": results})}]

    async def fetch(url: str, render: str = "auto") -> list[dict[str, Any]]:
        """
        OpenAI MCP fetch tool — ChatGPT company knowledge schema.

        Args:
            url: Canonical URL to fetch.
            render: Render mode — "auto", "never", "always".

        Returns:
            MCP content array with JSON-encoded {id, title, text, url, metadata}
        """
        bundle = BundleInput(type="url", value=url, render=render)
        bundle = await _handler.handle_atlas(bundle, _ANON_AUTH)

        # Get first successful fetch result
        content_text = ""
        for r in bundle.results:
            if hasattr(r, "raw_content") and r.raw_content:
                content_text = r.raw_content[:8000]  # OpenAI limit guidance
                break

        return [{
            "type": "text",
            "text": json.dumps({
                "id": url[:32],
                "title": url.split("/")[-1] or "Document",
                "text": content_text,
                "url": url,
                "metadata": {"source": "arifOS", "bridge": "openai-mcp"}
            })
        }]

    __all__ = ["search", "fetch"]
