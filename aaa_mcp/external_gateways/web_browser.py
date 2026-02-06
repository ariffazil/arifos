"""
aaa_mcp/external_gateways/web_browser.py — Web Browser & Content Fetcher

Opens web pages and extracts content using:
1. Direct HTTP requests (fast, lightweight)
2. Playwright browser (JavaScript rendering, interactive)
"""

from __future__ import annotations

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

# HTTP client
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

# HTML parsing
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Playwright for browser automation
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class WebPage:
    """Extracted web page content."""
    url: str
    title: str
    content: str
    text_content: str
    links: List[Dict[str, str]]
    meta: Dict[str, str]
    status_code: int = 200
    source: str = "unknown"  # 'httpx' or 'playwright'


class SimpleHTTPFetcher:
    """Fast HTTP-based page fetcher."""
    
    def __init__(self, timeout: int = 30, follow_redirects: bool = True):
        if not HTTPX_AVAILABLE:
            raise ImportError("httpx not installed. Run: pip install httpx")
        if not BS4_AVAILABLE:
            raise ImportError("beautifulsoup4 not installed. Run: pip install beautifulsoup4")
        
        self.timeout = timeout
        self.follow_redirects = follow_redirects
        self.client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=follow_redirects,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
            }
        )
    
    async def fetch(self, url: str) -> WebPage:
        """Fetch page using HTTP."""
        response = await self.client.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Extract meta tags
        meta = {}
        for tag in soup.find_all('meta'):
            name = tag.get('name', tag.get('property', ''))
            content = tag.get('content', '')
            if name and content:
                meta[name] = content
        
        # Extract main content (prioritize article/main/content areas)
        content_html = ""
        text_content = ""
        
        # Try to find main content
        main_selectors = ['main', 'article', '[role="main"]', '.content', '#content', '.post', '.entry']
        for selector in main_selectors:
            main_elem = soup.select_one(selector)
            if main_elem:
                content_html = str(main_elem)
                text_content = main_elem.get_text(separator='\n', strip=True)
                break
        
        # Fallback to body
        if not text_content:
            body = soup.find('body')
            if body:
                content_html = str(body)
                text_content = body.get_text(separator='\n', strip=True)
        
        # Remove script and style tags from text
        soup_text = BeautifulSoup(content_html, 'html.parser')
        for tag in soup_text(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        text_content = soup_text.get_text(separator='\n', strip=True)
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            links.append({
                "text": link.get_text(strip=True),
                "url": absolute_url,
                "title": link.get('title', '')
            })
        
        return WebPage(
            url=str(response.url),
            title=title,
            content=content_html,
            text_content=text_content,
            links=links,
            meta=meta,
            status_code=response.status_code,
            source="httpx"
        )
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


class PlaywrightBrowser:
    """Full browser using Playwright."""
    
    def __init__(self, headless: bool = True):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("playwright not installed. Run: pip install playwright")
        if not BS4_AVAILABLE:
            raise ImportError("beautifulsoup4 not installed. Run: pip install beautifulsoup4")
        
        self.headless = headless
    
    async def fetch(self, url: str, wait_for: Optional[str] = None, timeout: int = 30) -> WebPage:
        """
        Fetch page using full browser.
        
        Args:
            url: URL to fetch
            wait_for: CSS selector to wait for (for dynamic content)
            timeout: Timeout in seconds
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            try:
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080}
                )
                
                page = await context.new_page()
                
                # Handle dialog popups
                page.on("dialog", lambda dialog: asyncio.create_task(dialog.dismiss()))
                
                # Navigate
                response = await page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
                
                # Wait for specific element if requested
                if wait_for:
                    await page.wait_for_selector(wait_for, timeout=timeout * 1000)
                
                # Give extra time for any lazy-loaded content
                await asyncio.sleep(1)
                
                # Extract content
                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract title
                title = await page.title()
                
                # Extract meta
                meta = {}
                for tag in soup.find_all('meta'):
                    name = tag.get('name', tag.get('property', ''))
                    content = tag.get('content', '')
                    if name and content:
                        meta[name] = content
                
                # Extract main content
                content_html = ""
                text_content = ""
                
                main_selectors = ['main', 'article', '[role="main"]', '.content', '#content']
                for selector in main_selectors:
                    main_elem = soup.select_one(selector)
                    if main_elem:
                        content_html = str(main_elem)
                        text_content = main_elem.get_text(separator='\n', strip=True)
                        break
                
                if not text_content:
                    body = soup.find('body')
                    if body:
                        content_html = str(body)
                        text_content = body.get_text(separator='\n', strip=True)
                
                # Clean text
                soup_text = BeautifulSoup(content_html, 'html.parser')
                for tag in soup_text(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    tag.decompose()
                text_content = soup_text.get_text(separator='\n', strip=True)
                
                # Extract links
                links = []
                link_elements = await page.query_selector_all('a[href]')
                for link in link_elements:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    title_attr = await link.get_attribute('title') or ''
                    if href:
                        absolute_url = urljoin(url, href)
                        links.append({
                            "text": text.strip(),
                            "url": absolute_url,
                            "title": title_attr
                        })
                
                return WebPage(
                    url=page.url,
                    title=title,
                    content=content_html,
                    text_content=text_content,
                    links=links,
                    meta=meta,
                    status_code=response.status if response else 200,
                    source="playwright"
                )
                
            finally:
                await browser.close()
    
    async def screenshot(self, url: str, output_path: str, full_page: bool = False):
        """Take screenshot of page."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            try:
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle")
                await page.screenshot(path=output_path, full_page=full_page)
                return output_path
            finally:
                await browser.close()


class WebBrowser:
    """Unified web browser - chooses best method automatically."""
    
    def __init__(self):
        self.http_available = HTTPX_AVAILABLE and BS4_AVAILABLE
        self.playwright_available = PLAYWRIGHT_AVAILABLE
        
        self._http: Optional[SimpleHTTPFetcher] = None
        self._playwright: Optional[PlaywrightBrowser] = None
    
    async def open(
        self, 
        url: str, 
        method: str = "auto",
        javascript: bool = False,
        wait_for: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Open a web page and extract content.
        
        Args:
            url: URL to open
            method: 'auto', 'http', or 'playwright'
            javascript: Whether to execute JavaScript (forces playwright)
            wait_for: CSS selector to wait for (playwright only)
        
        Returns:
            Dict with page content and metadata
        """
        # Determine method
        if javascript or wait_for:
            method = "playwright"
        
        if method == "auto":
            # Use HTTP for simple sites, Playwright for complex ones
            method = "http" if self.http_available else "playwright"
        
        # Fetch using chosen method
        try:
            if method == "http" and self.http_available:
                if self._http is None:
                    self._http = SimpleHTTPFetcher()
                page = await self._http.fetch(url)
                
            elif method == "playwright" and self.playwright_available:
                if self._playwright is None:
                    self._playwright = PlaywrightBrowser()
                page = await self._playwright.fetch(url, wait_for=wait_for)
                
            else:
                return {
                    "status": "ERROR",
                    "url": url,
                    "error": f"Method '{method}' not available"
                }
            
            return {
                "status": "OK",
                "url": page.url,
                "title": page.title,
                "content": page.text_content[:10000],  # Limit content length
                "content_length": len(page.text_content),
                "links_count": len(page.links),
                "links": page.links[:20],  # Limit links
                "meta": page.meta,
                "source": page.source,
                "status_code": page.status_code
            }
            
        except Exception as e:
            # Fallback to playwright if HTTP fails
            if method == "http" and self.playwright_available:
                try:
                    if self._playwright is None:
                        self._playwright = PlaywrightBrowser()
                    page = await self._playwright.fetch(url, wait_for=wait_for)
                    return {
                        "status": "OK",
                        "url": page.url,
                        "title": page.title,
                        "content": page.text_content[:10000],
                        "content_length": len(page.text_content),
                        "links_count": len(page.links),
                        "links": page.links[:20],
                        "meta": page.meta,
                        "source": page.source,
                        "status_code": page.status_code
                    }
                except Exception as e2:
                    return {
                        "status": "ERROR",
                        "url": url,
                        "error": f"HTTP: {str(e)}; Playwright: {str(e2)}"
                    }
            
            return {
                "status": "ERROR",
                "url": url,
                "error": str(e)
            }
    
    async def batch_open(self, urls: List[str], method: str = "auto") -> List[Dict[str, Any]]:
        """Open multiple URLs concurrently."""
        tasks = [self.open(url, method) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def close(self):
        """Close any open connections."""
        if self._http:
            await self._http.close()


# Singleton instance
_browser: Optional[WebBrowser] = None


async def get_browser() -> WebBrowser:
    """Get or create WebBrowser singleton."""
    global _browser
    if _browser is None:
        _browser = WebBrowser()
    return _browser


async def open_web(url: str, javascript: bool = False) -> Dict[str, Any]:
    """Convenience function to open a web page."""
    browser = await get_browser()
    return await browser.open(url, javascript=javascript)


async def fetch_url_content(url: str) -> str:
    """Quick fetch - returns just the text content."""
    result = await open_web(url)
    if result["status"] == "OK":
        return result["content"]
    return f"Error fetching {url}: {result.get('error', 'Unknown error')}"
