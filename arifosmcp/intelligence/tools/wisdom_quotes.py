"""
arifosmcp/intelligence/tools/wisdom_quotes.py — Semantic Wisdom Retrieval

Retrieves from the 99-quote wisdom corpus based on semantic similarity.
BGE-M3 embeddings enable multilingual support (Malay, English, Manglish).
"""

from __future__ import annotations

import os
from typing import Any, Literal

from arifosmcp.intelligence.tools.aclip_base import ok, partial, void

_DEFAULT_QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "arifos_wisdom_quotes"


def retrieve_wisdom(
    query: str,
    category: Literal[
        "scar", "triumph", "paradox", "wisdom", "power", "love", "seal", "all"
    ] = "all",
    n_results: int = 3,
) -> dict[str, Any]:
    """
    Retrieve semantically relevant wisdom quotes from the 99-quote corpus.

    Args:
        query: Natural language query about situation, emotion, or need
        category: Filter by category (default: all)
        n_results: Number of quotes to return (default: 3)

    Returns:
        Dictionary with quotes, scores, and metadata
    """
    qdrant_url = os.environ.get("QDRANT_URL", _DEFAULT_QDRANT_URL)

    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import FieldCondition, Filter, MatchValue
    except ImportError:
        return void("qdrant-client not installed", hint="pip install qdrant-client>=1.7.0")

    try:
        client = QdrantClient(url=qdrant_url)
    except Exception as e:
        return void(f"Qdrant connection failed: {e}")

    try:
        from arifosmcp.intelligence.embeddings import embed

        query_vector = embed(query)
    except Exception as e:
        return void(f"Embedding failed: {e}")

    qdrant_filter = None
    if category != "all":
        qdrant_filter = Filter(
            must=[FieldCondition(key="category", match=MatchValue(value=category))]
        )

    try:
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=n_results,
            query_filter=qdrant_filter,
            with_payload=True,
        )
    except Exception as e:
        return partial(
            {"hint": "Run: python scripts/embed_wisdom_quotes.py"},
            error=f"Query failed: {e}",
        )

    quotes = []
    for point in results.points:
        quotes.append(
            {
                "id": point.payload.get("id"),
                "author": point.payload.get("author"),
                "text": point.payload.get("text"),
                "category": point.payload.get("category"),
                "source": point.payload.get("source"),
                "human_cost": point.payload.get("human_cost"),
                "score": round(point.score, 4),
            }
        )

    return ok(
        {
            "query": query,
            "category": category,
            "count": len(quotes),
            "quotes": quotes,
        }
    )


def get_quote_by_id(quote_id: int) -> dict[str, Any]:
    """Retrieve a specific quote by its ID (1-99)."""
    qdrant_url = os.environ.get("QDRANT_URL", _DEFAULT_QDRANT_URL)

    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import FieldCondition, Filter, MatchValue
    except ImportError:
        return void("qdrant-client not installed")

    try:
        client = QdrantClient(url=qdrant_url)
        results = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(must=[FieldCondition(key="id", match=MatchValue(value=quote_id))]),
            limit=1,
            with_payload=True,
        )

        if not results[0]:
            return void(f"Quote #{quote_id} not found")

        point = results[0][0]
        return ok(
            {
                "id": point.payload.get("id"),
                "author": point.payload.get("author"),
                "text": point.payload.get("text"),
                "category": point.payload.get("category"),
                "source": point.payload.get("source"),
                "human_cost": point.payload.get("human_cost"),
            }
        )
    except Exception as e:
        return void(f"Retrieval failed: {e}")


def augment_prompt_with_wisdom(
    original_prompt: str,
    query: str,
    n_quotes: int = 2,
    category: str = "all",
) -> str:
    """
    Augment a prompt with relevant wisdom quotes from the 99-quote corpus.

    Args:
        original_prompt: The original prompt to augment
        query: Semantic query for quote retrieval
        n_quotes: Number of quotes to include (default: 2)
        category: Category filter

    Returns:
        Augmented prompt with wisdom context
    """
    result = retrieve_wisdom(query, category=category, n_results=n_quotes)

    if result.get("status") != "ok" or not result.get("quotes"):
        return original_prompt

    quotes = result["quotes"]
    wisdom_context = "\n\n".join(
        [f'"{q["text"]}"\n— {q["author"]} ({q["source"]})' for q in quotes]
    )

    return f"""{original_prompt}

---
**Wisdom:**

{wisdom_context}

---
Reflect on this wisdom before responding."""


__all__ = ["retrieve_wisdom", "get_quote_by_id", "augment_prompt_with_wisdom"]
