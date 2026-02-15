"""
aaa_mcp/external_gateways — External data gateways for arifOS

Provides:
- brave_client: Brave Search API client (requires API key)
- web_search_noapi: Web search without API keys (DuckDuckGo)
- web_browser: Web page fetching and content extraction
"""

from __future__ import annotations

__all__ = [
    "BraveSearchClient",
    "WebSearchNoAPI",
    "WebBrowser",
    "DuckDuckGoSearcher",
    "PlaywrightSearcher",
    "SimpleHTTPFetcher",
    "PlaywrightBrowser",
]

# Try to import each module - some may have optional dependencies
try:
    from .brave_client import BraveSearchClient
except ImportError:
    BraveSearchClient = None  # type: ignore

try:
    from .web_search_noapi import (
        WebSearchNoAPI,
        DuckDuckGoSearcher,
        PlaywrightSearcher,
    )
except ImportError:
    WebSearchNoAPI = None  # type: ignore
    DuckDuckGoSearcher = None  # type: ignore
    PlaywrightSearcher = None  # type: ignore

try:
    from .web_browser import (
        WebBrowser,
        SimpleHTTPFetcher,
        PlaywrightBrowser,
    )
except ImportError:
    WebBrowser = None  # type: ignore
    SimpleHTTPFetcher = None  # type: ignore
    PlaywrightBrowser = None  # type: ignore
