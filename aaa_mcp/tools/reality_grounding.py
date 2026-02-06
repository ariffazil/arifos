"""
aaa_mcp/tools/reality_grounding.py — Hardened Reality Grounding

Provides external fact-checking via thermodynamically optimal cascade:
1. DDGS (DuckDuckGo) — Primary, no API key, low entropy
2. Playwright DDG HTML — Fallback if DDGS fails
3. Playwright Google — Last resort (high entropy, CAPTCHA risk)

Constitutional Compliance:
- F1 Amanah: Reversible throttling, no vendor lock-in
- F2 Truth: ASEAN source bias, timelimit filters
- F7 Humility: Uncertainty tracking (Ω₀) for all results
- F9 Anti-Hantu: Full source attribution

Thermodynamic Profile: Low entropy cascade (DDGS → HTML → Browser)
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Optional Dependencies
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from codebase.enforcement.routing.prompt_router import route_refuse

# Configuration
DEFAULT_THROTTLE_SECONDS = 2.0
ASEAN_SITES = [".my", ".sg", ".id", ".th", ".ph", ".vn", ".bn", ".kh", ".la", ".mm"]
UNCERTAINTY_DDGS = 0.04
UNCERTAINTY_PLAYWRIGHT = 0.07


@dataclass
class SearchResult:
    """Standardized search result with governance metadata."""
    title: str
    url: str
    snippet: str
    source: str
    rank: int
    uncertainty: float = field(default=UNCERTAINTY_DDGS)
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "rank": self.rank,
            "uncertainty_omega": self.uncertainty,
            "timestamp": self.timestamp or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }


@dataclass
class RealityGroundingResult:
    """Complete result with constitutional audit trail."""
    status: str
    query: str
    results: List[SearchResult]
    engines_used: List[str]
    engines_failed: List[str]
    uncertainty_aggregate: float
    audit_trail: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "query": self.query,
            "results_count": len(self.results),
            "results": [r.to_dict() for r in self.results],
            "engines_used": self.engines_used,
            "engines_failed": self.engines_failed,
            "uncertainty_aggregate": self.uncertainty_aggregate,
            "audit_trail": self.audit_trail,
        }


class ThrottleGovernor:
    """Rate limiter with reversible throttling (F1 Amanah)."""
    
    def __init__(self, min_interval: float = DEFAULT_THROTTLE_SECONDS):
        self.min_interval = min_interval
        self._last_call_time: Optional[float] = None
        self._lock = asyncio.Lock()
    
    async def wait(self) -> float:
        """Wait for throttle interval. Returns wait time."""
        async with self._lock:
            now = time.time()
            if self._last_call_time is not None:
                elapsed = now - self._last_call_time
                if elapsed < self.min_interval:
                    wait_time = self.min_interval - elapsed
                    await asyncio.sleep(wait_time)
                    return wait_time
            self._last_call_time = time.time()
            return 0.0


# Singleton throttle governor
_throttle_governor = ThrottleGovernor()


class DDGSEngine:
    """DuckDuckGo search via ddgs library - LOW entropy."""
    
    NAME = "ddgs"
    UNCERTAINTY = UNCERTAINTY_DDGS
    
    def __init__(self, timeout: int = 30):
        if not DDGS_AVAILABLE:
            raise ImportError("ddgs not installed")
        self.timeout = timeout
        self._throttle = _throttle_governor
    
    def _build_query(self, query: str, region: str = "wt-wt") -> str:
        """Build query with ASEAN bias if requested (F2 Truth)."""
        if region == "asean":
            sites = " OR ".join([f"site:*{s}" for s in ASEAN_SITES])
            return f"({query}) ({sites})"
        return query
    
    async def search(self, query: str, max_results: int = 10,
                     region: str = "wt-wt", safesearch: str = "moderate",
                     timelimit: Optional[str] = None) -> Tuple[List[SearchResult], Optional[str]]:
        """Search DuckDuckGo."""
        await self._throttle.wait()
        built_query = self._build_query(query, region)
        
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self._sync_search(built_query, max_results, safesearch, timelimit)
            )
            return results, None
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.warning(f"DDGS search failed: {error_msg}")
            return [], error_msg
    
    def _sync_search(self, query: str, max_results: int,
                     safesearch: str, timelimit: Optional[str]) -> List[SearchResult]:
        """Synchronous DDGS search."""
        with DDGS(timeout=self.timeout) as ddgs:
            raw_results = ddgs.text(
                query,
                region="wt-wt",
                safesearch=safesearch,
                timelimit=timelimit,
                max_results=max_results,
            )
            
            results = []
            for i, r in enumerate(raw_results, 1):
                results.append(SearchResult(
                    title=r.get("title", ""),
                    url=r.get("href", ""),
                    snippet=r.get("body", ""),
                    source=self.NAME,
                    rank=i,
                    uncertainty=self.UNCERTAINTY,
                ))
            return results


class PlaywrightDDGEngine:
    """DuckDuckGo HTML search via Playwright - MEDIUM entropy."""
    
    NAME = "playwright_ddg"
    UNCERTAINTY = UNCERTAINTY_PLAYWRIGHT
    
    def __init__(self, headless: bool = True):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("playwright not installed")
        self.headless = headless
        self._throttle = ThrottleGovernor(min_interval=5.0)
    
    async def search(self, query: str, max_results: int = 10,
                     region: str = "wt-wt") -> Tuple[List[SearchResult], Optional[str]]:
        """Search DuckDuckGo HTML version via browser."""
        await self._throttle.wait()
        results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                try:
                    context = await browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    )
                    page = await context.new_page()
                    
                    encoded_query = query.replace(" ", "+")
                    await page.goto(
                        f"https://html.duckduckgo.com/html/?q={encoded_query}",
                        wait_until="networkidle",
                        timeout=30000,
                    )
                    
                    result_elements = await page.query_selector_all(".result")
                    
                    for i, elem in enumerate(result_elements[:max_results], 1):
                        try:
                            title_elem = await elem.query_selector(".result__title a")
                            snippet_elem = await elem.query_selector(".result__snippet")
                            
                            title = await title_elem.inner_text() if title_elem else ""
                            url = await title_elem.get_attribute("href") if title_elem else ""
                            snippet = await snippet_elem.inner_text() if snippet_elem else ""
                            
                            if title and url:
                                results.append(SearchResult(
                                    title=title.strip(),
                                    url=url,
                                    snippet=snippet.strip(),
                                    source=self.NAME,
                                    rank=i,
                                    uncertainty=self.UNCERTAINTY,
                                ))
                        except Exception as e:
                            logger.debug(f"Failed to extract result {i}: {e}")
                            continue
                finally:
                    await browser.close()
            
            return results, None
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.warning(f"Playwright DDG failed: {error_msg}")
            return [], error_msg


class PlaywrightGoogleEngine:
    """Google search via Playwright - HIGH entropy (last resort)."""
    
    NAME = "playwright_google"
    UNCERTAINTY = UNCERTAINTY_PLAYWRIGHT + 0.03
    
    def __init__(self, headless: bool = True):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("playwright not installed")
        self.headless = headless
        self._throttle = ThrottleGovernor(min_interval=10.0)
    
    async def search(self, query: str, max_results: int = 10,
                     region: str = "wt-wt") -> Tuple[List[SearchResult], Optional[str]]:
        """Search Google via browser - WARNING: High CAPTCHA risk."""
        await self._throttle.wait()
        results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                try:
                    context = await browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        viewport={"width": 1920, "height": 1080},
                    )
                    page = await context.new_page()
                    
                    encoded_query = query.replace(" ", "+")
                    await page.goto(
                        f"https://www.google.com/search?q={encoded_query}",
                        wait_until="networkidle",
                        timeout=30000,
                    )
                    
                    captcha = await page.query_selector("text=I'm not a robot")
                    if captcha:
                        return [], "CAPTCHA detected - Google blocking automation"
                    
                    result_elements = await page.query_selector_all("div.g")
                    
                    for i, elem in enumerate(result_elements[:max_results], 1):
                        try:
                            title_elem = await elem.query_selector("h3")
                            link_elem = await elem.query_selector("a")
                            snippet_elem = await elem.query_selector("div.VwiC3b, span.aCOpRe")
                            
                            title = await title_elem.inner_text() if title_elem else ""
                            url = await link_elem.get_attribute("href") if link_elem else ""
                            snippet = await snippet_elem.inner_text() if snippet_elem else ""
                            
                            if title and url:
                                results.append(SearchResult(
                                    title=title.strip(),
                                    url=url,
                                    snippet=snippet.strip(),
                                    source=self.NAME,
                                    rank=i,
                                    uncertainty=self.UNCERTAINTY,
                                ))
                        except Exception as e:
                            logger.debug(f"Failed to extract result {i}: {e}")
                            continue
                finally:
                    await browser.close()
            
            return results, None
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.warning(f"Playwright Google failed: {error_msg}")
            return [], error_msg


class RealityGroundingCascade:
    """Thermodynamic cascade: DDGS → Playwright DDG → Playwright Google."""
    
    def __init__(self):
        self.engines: List[Any] = []
        self._init_engines()
    
    def _init_engines(self):
        """Initialize available engines in priority order."""
        if DDGS_AVAILABLE:
            try:
                self.engines.append(DDGSEngine())
                logger.info("DDGS engine initialized")
            except Exception as e:
                logger.warning(f"Failed to init DDGS: {e}")
        
        if PLAYWRIGHT_AVAILABLE:
            try:
                self.engines.append(PlaywrightDDGEngine())
                logger.info("Playwright DDG engine initialized")
            except Exception as e:
                logger.warning(f"Failed to init Playwright DDG: {e}")
            
            try:
                self.engines.append(PlaywrightGoogleEngine())
                logger.info("Playwright Google engine initialized")
            except Exception as e:
                logger.warning(f"Failed to init Playwright Google: {e}")
    
    async def search(self, query: str, max_results: int = 10,
                     region: str = "wt-wt", timelimit: Optional[str] = None) -> RealityGroundingResult:
        """Execute thermodynamic cascade search."""
        if not self.engines:
            return RealityGroundingResult(
                status="ERROR",
                query=query,
                results=[],
                engines_used=[],
                engines_failed=["none_available"],
                uncertainty_aggregate=1.0,
                audit_trail={
                    "error": "No search engines available",
                    "install_hint": "pip install duckduckgo-search playwright httpx beautifulsoup4",
                },
            )
        
        all_results: List[SearchResult] = []
        engines_used: List[str] = []
        engines_failed: List[str] = []
        
        for engine in self.engines:
            try:
                logger.info(f"Trying engine: {engine.NAME}")
                
                if isinstance(engine, DDGSEngine):
                    results, error = await engine.search(query, max_results, region, timelimit=timelimit)
                else:
                    results, error = await engine.search(query, max_results, region)
                
                if error:
                    engines_failed.append(f"{engine.NAME}: {error}")
                    continue
                
                if results:
                    all_results = results
                    engines_used.append(engine.NAME)
                    logger.info(f"Success with {engine.NAME}: {len(results)} results")
                    break
                else:
                    engines_failed.append(f"{engine.NAME}: no_results")
            except Exception as e:
                error_msg = f"{engine.NAME}: {type(e).__name__}: {str(e)}"
                engines_failed.append(error_msg)
                logger.error(f"Engine {engine.NAME} crashed: {e}")
                continue
        
        if all_results:
            uncertainties = [r.uncertainty for r in all_results]
            avg_uncertainty = sum(uncertainties) / len(uncertainties)
            status = "OK" if len(engines_failed) == 0 else "PARTIAL"
        else:
            avg_uncertainty = 1.0
            status = "ERROR"
        
        audit_trail = {
            "query_original": query,
            "query_processed": self._add_asean_bias(query) if region == "asean" else query,
            "region": region,
            "timelimit": timelimit,
            "max_results_requested": max_results,
            "max_results_returned": len(all_results),
            "engines_attempted": [e.NAME for e in self.engines],
            "engines_used": engines_used,
            "engines_failed": engines_failed,
            "throttle_applied": True,
            "constitutional_notes": [
                "F1 Amanah: Rate limiting applied",
                "F2 Truth: ASEAN bias available" if region == "asean" else "F2 Truth: No regional bias",
                "F7 Humility: Uncertainty tracked per result",
                "F9 Anti-Hantu: Source attribution enforced",
            ],
        }
        
        return RealityGroundingResult(
            status=status,
            query=query,
            results=all_results,
            engines_used=engines_used,
            engines_failed=engines_failed,
            uncertainty_aggregate=round(avg_uncertainty, 3),
            audit_trail=audit_trail,
        )
    
    def _add_asean_bias(self, query: str) -> str:
        """Add ASEAN site bias to query."""
        sites = " OR ".join([f"site:*{s}" for s in ASEAN_SITES])
        return f"({query}) ({sites})"


class WebBrowser:
    """Fetches and extracts content from web pages."""
    
    def __init__(self):
        self.http_available = HTTPX_AVAILABLE and BS4_AVAILABLE
        self.playwright_available = PLAYWRIGHT_AVAILABLE
        self._throttle = ThrottleGovernor(min_interval=1.0)
    
    async def fetch(self, url: str, javascript: bool = False) -> Dict[str, Any]:
        """Fetch page content."""
        await self._throttle.wait()
        
        if not javascript and self.http_available:
            result = await self._fetch_http(url)
            if result["status"] == "OK":
                return result
            logger.info(f"HTTP failed for {url}, trying Playwright")
        
        if self.playwright_available:
            return await self._fetch_playwright(url)
        
        return {
            "status": "ERROR",
            "url": url,
            "error": "No fetch method available",
            "content": "",
            "title": "",
        }
    
    async def _fetch_http(self, url: str) -> Dict[str, Any]:
        """Fetch via HTTP (httpx + BeautifulSoup)."""
        try:
            async with httpx.AsyncClient(
                timeout=30,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                
                title = ""
                title_tag = soup.find("title")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                
                content = ""
                for selector in ["main", "article", '[role="main"]', ".content", "#content"]:
                    elem = soup.select_one(selector)
                    if elem:
                        content = elem.get_text(separator="\n", strip=True)
                        break
                
                if not content:
                    body = soup.find("body")
                    if body:
                        content = body.get_text(separator="\n", strip=True)
                
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                content = "\n".join(lines)
                
                return {
                    "status": "OK",
                    "url": str(response.url),
                    "title": title,
                    "content": content[:10000],
                    "content_length": len(content),
                    "source": "httpx",
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "url": url,
                "error": f"HTTP: {type(e).__name__}: {str(e)}",
                "content": "",
                "title": "",
            }
    
    async def _fetch_playwright(self, url: str) -> Dict[str, Any]:
        """Fetch via Playwright."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                try:
                    page = await browser.new_page()
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                    
                    title = await page.title()
                    content = await page.evaluate("""
                        () => {
                            const main = document.querySelector('main, article, [role="main"], .content, #content');
                            const body = main || document.body;
                            return body.innerText;
                        }
                    """)
                    
                    return {
                        "status": "OK",
                        "url": page.url,
                        "title": title,
                        "content": content[:10000],
                        "content_length": len(content),
                        "source": "playwright",
                    }
                finally:
                    await browser.close()
        except Exception as e:
            return {
                "status": "ERROR",
                "url": url,
                "error": f"Playwright: {type(e).__name__}: {str(e)}",
                "content": "",
                "title": "",
            }


# Singletons
_cascade: Optional[RealityGroundingCascade] = None
_browser: Optional[WebBrowser] = None


def get_cascade() -> RealityGroundingCascade:
    """Get or create cascade singleton."""
    global _cascade
    if _cascade is None:
        _cascade = RealityGroundingCascade()
    return _cascade


def get_browser() -> WebBrowser:
    """Get or create browser singleton."""
    global _browser
    if _browser is None:
        _browser = WebBrowser()
    return _browser


def should_reality_check(query: str) -> Tuple[bool, str]:
    """Determine if reality check is needed."""
    q = query.lower()
    
    verification_triggers = (
        "verify", "source", "citation", "evidence", "prove", "fact check",
        "is it true", "confirm", "validate", "check if", "according to"
    )
    if any(t in q for t in verification_triggers):
        return True, "explicit_verification"
    
    high_stakes = ("medical", "health", "diagnose", "finance", "invest", "legal", "law")
    if any(t in q for t in high_stakes):
        return True, "high_stakes_domain"
    
    temporal_markers = ("latest", "recent", "news", "today", "this week", "2025", "2026")
    if any(t in q for t in temporal_markers):
        return True, "temporal_query"
    
    return False, "no_verification_needed"


async def reality_check(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    timelimit: Optional[str] = None,
    fetch_sources: bool = False,
    max_sources: int = 2,
) -> Dict[str, Any]:
    """Perform constitutional reality grounding. Main MCP entry point."""
    refusal = route_refuse(query)
    needs_check, reason = should_reality_check(query)
    
    cascade = get_cascade()
    result = await cascade.search(query, max_results, region, timelimit)
    
    sources_fetched = []
    if fetch_sources and result.results:
        browser = get_browser()
        for r in result.results[:max_sources]:
            fetch_result = await browser.fetch(r.url)
            if fetch_result["status"] == "OK":
                sources_fetched.append({
                    "rank": r.rank,
                    "url": r.url,
                    "title": fetch_result.get("title", ""),
                    "content_preview": fetch_result.get("content", "")[:2000],
                    "source_method": fetch_result.get("source", "unknown"),
                })
    
    response = {
        "status": result.status,
        "query": query,
        "needs_check": needs_check,
        "check_reason": reason,
        "refusal": refusal.to_dict() if hasattr(refusal, "to_dict") else {},
        "engines_used": result.engines_used,
        "engines_failed": result.engines_failed,
        "results_count": len(result.results),
        "results": [r.to_dict() for r in result.results],
        "uncertainty_aggregate": result.uncertainty_aggregate,
        "audit_trail": result.audit_trail,
    }
    
    if sources_fetched:
        response["sources_fetched"] = sources_fetched
    
    if result.uncertainty_aggregate > 0.05:
        response["warning"] = "High uncertainty detected. Cross-verify with multiple sources."
    
    return response


async def open_web_page(url: str, javascript: bool = False) -> Dict[str, Any]:
    """Open and extract content from a web page."""
    browser = get_browser()
    return await browser.fetch(url, javascript)


async def web_search_noapi(
    query: str,
    max_results: int = 10,
    region: str = "wt-wt",
    timelimit: Optional[str] = None,
) -> Dict[str, Any]:
    """Search web without API key. Simplified interface."""
    cascade = get_cascade()
    result = await cascade.search(query, max_results, region, timelimit)
    return result.to_dict()
