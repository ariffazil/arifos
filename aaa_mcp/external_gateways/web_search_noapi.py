"""
aaa_mcp/external_gateways/web_search_noapi.py — Web Search without API Keys

Provides web search capabilities using:
1. DuckDuckGo (ddgs) - primary, no API key needed
2. Playwright browser automation - fallback for JavaScript-heavy sites
"""

from __future__ import annotations

import asyncio
import random
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# DuckDuckGo search (no API key required)
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

# Playwright for browser automation
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class SearchResult:
    """Standardized search result."""
    title: str
    url: str
    snippet: str
    source: str = "unknown"
    rank: int = 0


class DuckDuckGoSearcher:
    """DuckDuckGo search without API key."""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        if not DDGS_AVAILABLE:
            raise ImportError("ddgs package not installed. Run: pip install ddgs")
    
    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None  # d, w, m, y
    ) -> List[SearchResult]:
        """Search DuckDuckGo and return standardized results."""
        import concurrent.futures
        
        def _do_search():
            try:
                with DDGS(timeout=self.timeout) as ddgs:
                    # DDGS 9.x API uses 'keywords' parameter
                    results = ddgs.text(
                        keywords=query,
                        region=region,
                        safesearch=safesearch,
                        timelimit=timelimit,
                        max_results=max_results
                    )
                    return list(results)
            except TypeError as te:
                # Try newer API format if old one fails
                if "missing 1 required positional argument" in str(te):
                    with DDGS(timeout=self.timeout) as ddgs:
                        results = ddgs.text(
                            query,  # Newer API uses positional arg
                            region=region,
                            safesearch=safesearch,
                            timelimit=timelimit,
                            max_results=max_results
                        )
                        return list(results)
                raise
            except Exception as e:
                import traceback
                print(f"DDGS Error: {e}")
                traceback.print_exc()
                raise
        
        # Run in thread pool since DDGS is synchronous
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            raw_results = await loop.run_in_executor(pool, _do_search)
        
        # Convert to standardized format
        search_results = []
        for i, r in enumerate(raw_results[:max_results]):
            search_results.append(SearchResult(
                title=r.get("title", ""),
                url=r.get("href", ""),
                snippet=r.get("body", ""),
                source="duckduckgo",
                rank=i + 1
            ))
        
        return search_results
    
    async def search_news(
        self,
        query: str,
        max_results: int = 10,
        timelimit: Optional[str] = None  # d, w, m
    ) -> List[SearchResult]:
        """Search news via DuckDuckGo."""
        import concurrent.futures
        
        def _do_search():
            try:
                with DDGS(timeout=self.timeout) as ddgs:
                    results = ddgs.news(
                        keywords=query,
                        region="wt-wt",
                        safesearch="moderate",
                        timelimit=timelimit,
                        max_results=max_results
                    )
                    return list(results)
            except TypeError:
                # Try newer API format
                with DDGS(timeout=self.timeout) as ddgs:
                    results = ddgs.news(
                        query,
                        region="wt-wt",
                        safesearch="moderate",
                        timelimit=timelimit,
                        max_results=max_results
                    )
                    return list(results)
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            raw_results = await loop.run_in_executor(pool, _do_search)
        
        search_results = []
        for i, r in enumerate(raw_results[:max_results]):
            search_results.append(SearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                snippet=r.get("body", ""),
                source="duckduckgo_news",
                rank=i + 1
            ))
        
        return search_results


class PlaywrightSearcher:
    """Browser-based search using Playwright (no API key)."""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("playwright not installed. Run: pip install playwright")
    
    async def search_google(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search Google using browser automation."""
        search_results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            try:
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = await context.new_page()
                
                # Navigate to Google
                await page.goto(f"https://www.google.com/search?q={query.replace(' ', '+')}")
                await page.wait_for_load_state("networkidle")
                
                # Handle cookie consent if present
                try:
                    consent_button = await page.query_selector('button:has-text("Reject all")')
                    if consent_button:
                        await consent_button.click()
                        await asyncio.sleep(0.5)
                except:
                    pass
                
                # Extract search results
                results = await page.query_selector_all('div.g')
                
                for i, result in enumerate(results[:max_results]):
                    try:
                        title_elem = await result.query_selector('h3')
                        link_elem = await result.query_selector('a')
                        snippet_elem = await result.query_selector('div.VwiC3b, span.aCOpRe')
                        
                        title = await title_elem.inner_text() if title_elem else ""
                        url = await link_elem.get_attribute('href') if link_elem else ""
                        snippet = await snippet_elem.inner_text() if snippet_elem else ""
                        
                        if title and url:
                            search_results.append(SearchResult(
                                title=title,
                                url=url,
                                snippet=snippet,
                                source="google",
                                rank=i + 1
                            ))
                    except Exception:
                        continue
                        
            finally:
                await browser.close()
        
        return search_results
    
    async def search_duckduckgo_html(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search DuckDuckGo HTML version using browser."""
        search_results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            try:
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = await context.new_page()
                
                # Use DuckDuckGo HTML version
                await page.goto(f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}")
                await page.wait_for_load_state("networkidle")
                
                # Extract results
                results = await page.query_selector_all('.result')
                
                for i, result in enumerate(results[:max_results]):
                    try:
                        title_elem = await result.query_selector('.result__title a')
                        snippet_elem = await result.query_selector('.result__snippet')
                        
                        title = await title_elem.inner_text() if title_elem else ""
                        url = await title_elem.get_attribute('href') if title_elem else ""
                        snippet = await snippet_elem.inner_text() if snippet_elem else ""
                        
                        if title and url:
                            search_results.append(SearchResult(
                                title=title,
                                url=url,
                                snippet=snippet,
                                source="duckduckgo_html",
                                rank=i + 1
                            ))
                    except Exception:
                        continue
                        
            finally:
                await browser.close()
        
        return search_results


class WebSearchNoAPI:
    """Unified web search without API keys."""
    
    def __init__(self):
        self.ddgs_available = DDGS_AVAILABLE
        self.playwright_available = PLAYWRIGHT_AVAILABLE
        self._ddgs: Optional[DuckDuckGoSearcher] = None
        self._playwright: Optional[PlaywrightSearcher] = None
    
    async def search(
        self, 
        query: str, 
        max_results: int = 10,
        engines: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search using available engines (no API key required).
        
        Args:
            query: Search query
            max_results: Maximum results per engine
            engines: List of engines to use ['ddgs', 'playwright_google', 'playwright_ddg']
                    If None, tries all available engines.
        
        Returns:
            Dict with results and metadata
        """
        if engines is None:
            engines = []
            if self.ddgs_available:
                engines.append("ddgs")
            if self.playwright_available:
                engines.extend(["playwright_ddg", "playwright_google"])
        
        all_results = []
        errors = []
        
        for engine in engines:
            try:
                if engine == "ddgs" and self.ddgs_available:
                    if self._ddgs is None:
                        self._ddgs = DuckDuckGoSearcher()
                    results = await self._ddgs.search(query, max_results)
                    all_results.extend(results)
                
                elif engine == "playwright_google" and self.playwright_available:
                    if self._playwright is None:
                        self._playwright = PlaywrightSearcher()
                    results = await self._playwright.search_google(query, max_results)
                    all_results.extend(results)
                
                elif engine == "playwright_ddg" and self.playwright_available:
                    if self._playwright is None:
                        self._playwright = PlaywrightSearcher()
                    results = await self._playwright.search_duckduckgo_html(query, max_results)
                    all_results.extend(results)
                    
            except Exception as e:
                import traceback
                error_msg = f"{engine}: {str(e)}"
                errors.append(error_msg)
                print(f"[WebSearch Error] {error_msg}")
                traceback.print_exc()
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                unique_results.append(r)
        
        # Sort by rank
        unique_results.sort(key=lambda x: x.rank)
        
        return {
            "status": "OK" if unique_results else "NO_RESULTS",
            "query": query,
            "engines_used": engines,
            "results_count": len(unique_results),
            "results": [
                {
                    "rank": r.rank,
                    "title": r.title,
                    "url": r.url,
                    "snippet": r.snippet,
                    "source": r.source
                }
                for r in unique_results[:max_results]
            ],
            "errors": errors if errors else None
        }
    
    async def search_news(
        self,
        query: str,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """Search news (DuckDuckGo only)."""
        if not self.ddgs_available:
            return {
                "status": "ERROR",
                "query": query,
                "error": "ddgs not installed"
            }
        
        try:
            if self._ddgs is None:
                self._ddgs = DuckDuckGoSearcher()
            
            results = await self._ddgs.search_news(query, max_results)
            
            return {
                "status": "OK",
                "query": query,
                "results_count": len(results),
                "results": [
                    {
                        "rank": r.rank,
                        "title": r.title,
                        "url": r.url,
                        "snippet": r.snippet,
                        "source": r.source
                    }
                    for r in results
                ]
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "query": query,
                "error": str(e)
            }


# Singleton instance
_web_search: Optional[WebSearchNoAPI] = None


async def get_web_search() -> WebSearchNoAPI:
    """Get or create WebSearchNoAPI singleton."""
    global _web_search
    if _web_search is None:
        _web_search = WebSearchNoAPI()
    return _web_search


async def search_web_noapi(query: str, max_results: int = 10) -> Dict[str, Any]:
    """Convenience function for web search without API key."""
    searcher = await get_web_search()
    return await searcher.search(query, max_results)
