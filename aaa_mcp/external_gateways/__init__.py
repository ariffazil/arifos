"""
aaa_mcp/external_gateways — External data gateways for arifOS

Provides:
- jina_reader_client: Jina Reader API client (PRIMARY for search_reality)
- brave_client: Brave Search API client (fallback)
- perplexity_client: Perplexity API client (fallback)
"""

from __future__ import annotations

__all__ = [
    "JinaReaderClient",
    "JinaReranker",
    "BraveSearchClient",
    "PerplexitySearchClient",
]

MAX_PRIORITY_BACKENDS = ["jina", "perplexity", "brave", "duckduckgo"]

try:
    from .jina_reader_client import JinaReaderClient, JinaReranker
except ImportError:
    JinaReaderClient = None  # type: ignore
    JinaReranker = None  # type: ignore

try:
    from .brave_client import BraveSearchClient
except ImportError:
    BraveSearchClient = None  # type: ignore

try:
    from .perplexity_client import PerplexitySearchClient
except ImportError:
    PerplexitySearchClient = None  # type: ignore
