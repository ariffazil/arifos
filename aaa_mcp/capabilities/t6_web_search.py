# aaa_mcp/capabilities/t6_web_search.py
# T6 Web Search — Brave Search API integration (v62 Step 2)
# Real evidence grounding for F2 Truth verification

import hashlib
import re
from typing import List
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import httpx

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"


@dataclass
class EvidenceArtifact:
    """Structured evidence from web search."""

    source: str  # URL
    snippet: str  # Relevant text
    title: str  # Page title
    timestamp: str  # ISO 8601
    query: str  # Original search query
    content_hash: str  # SHA-256 of snippet
    relevance: float = 0.0  # 0-1 relevance score

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "snippet": self.snippet[:500],  # Truncate for safety
            "title": self.title,
            "timestamp": self.timestamp,
            "query": self.query,
            "content_hash": self.content_hash,
            "relevance": round(self.relevance, 2),
        }


def sanitize_query(query: str) -> str:
    """
    Remove test labels, prefixes, and metadata from query.
    Extract the minimal factual core.
    """
    # Remove test labels
    prefixes = [
        r"CONTRAST\s+v\d+\.\d+\s+TEST\s+[A-Z]:?",
        r"TEST\s+[A-Z]:?",
        r"v\d+\.\d+",
    ]

    sanitized = query
    for prefix in prefixes:
        sanitized = re.sub(prefix, "", sanitized, flags=re.IGNORECASE)

    # Remove extra whitespace
    sanitized = sanitized.strip()

    # If query is trivial math, return empty (skip search)
    trivial_patterns = [
        r"^\d+\s*[+\-*/]\s*\d+$",  # 2+2, 5*3
        r"what\s+is\s+\d+\s*[+\-*/]\s*\d+",  # "what is 2+2"
    ]
    for pattern in trivial_patterns:
        if re.match(pattern, sanitized, re.IGNORECASE):
            return ""  # Signal: skip search, use analytic proof

    return sanitized


def calculate_relevance(query: str, title: str, snippet: str, url: str) -> float:
    """
    Calculate relevance score (0-1) between query and search result.

    Cheap heuristic: keyword overlap + domain credibility
    """
    query_words = set(query.lower().split())
    title_words = set(title.lower().split())
    snippet_words = set(snippet.lower().split())

    # Remove common stop words
    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "shall",
        "can",
        "need",
        "dare",
        "ought",
        "used",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "between",
        "under",
        "and",
        "but",
        "or",
        "yet",
        "so",
        "if",
        "because",
        "although",
        "though",
        "while",
        "where",
        "when",
        "that",
        "which",
        "who",
        "whom",
        "whose",
        "what",
        "this",
        "these",
        "those",
        "i",
        "you",
        "he",
        "she",
        "it",
        "we",
        "they",
        "me",
        "him",
        "her",
        "us",
        "them",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "their",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "these",
        "those",
        "am",
        "is",
        "are",
        "was",
        "were",
    }

    query_words -= stop_words

    if not query_words:
        return 0.5  # Neutral if no meaningful words

    # Calculate overlap
    title_overlap = len(query_words & title_words) / len(query_words)
    snippet_overlap = len(query_words & snippet_words) / len(query_words)

    # Weight title more heavily
    overlap_score = (title_overlap * 0.6) + (snippet_overlap * 0.4)

    # Domain credibility bonus
    credible_domains = [
        ".edu",
        ".gov",
        "wikipedia.org",
        "britannica.com",
        "arxiv.org",
        "doi.org",
        "nature.com",
        "science.org",
        "reuters.com",
        "apnews.com",
        "bloomberg.com",
        "ft.com",
        "ctbuh.org",  # Council on Tall Buildings
    ]
    domain_bonus = 0.0
    for domain in credible_domains:
        if domain in url.lower():
            domain_bonus = 0.2
            break

    return min(1.0, overlap_score + domain_bonus)


async def brave_search(
    query: str, count: int = 5, original_query: str = None
) -> List[EvidenceArtifact]:
    """
    Search Brave API and return evidence artifacts.

    Args:
        query: Search query (will be sanitized)
        count: Number of results (max 20)
        original_query: The unsanitized query for relevance checking

    Returns:
        List of EvidenceArtifact objects
    """
    # Sanitize query
    search_query = sanitize_query(query)

    # If sanitized to empty, skip search (analytic truth)
    if not search_query:
        return []

    if not BRAVE_API_KEY:
        raise ValueError("BRAVE_API_KEY not configured")

    headers = {"X-Subscription-Token": BRAVE_API_KEY, "Accept": "application/json"}

    params = {
        "q": search_query,
        "count": min(count * 2, 20),  # Request more to filter by relevance
        "offset": 0,
        "mkt": "en-US",
        "safesearch": "moderate",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BRAVE_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Brave API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise ValueError(f"Search failed: {str(e)}")

    artifacts = []
    web_results = data.get("web", {}).get("results", [])

    # Use original query for relevance checking (or sanitized if not provided)
    check_query = original_query or query

    for result in web_results:
        snippet = result.get("description", "")
        url = result.get("url", "")
        title = result.get("title", "")

        # Calculate relevance score
        relevance = calculate_relevance(check_query, title, snippet, url)

        # Only include if relevance >= 0.3
        if relevance < 0.3:
            continue

        # Generate content hash
        content_hash = hashlib.sha256(f"{url}{snippet}".encode()).hexdigest()[:16]

        artifact = EvidenceArtifact(
            source=url,
            snippet=snippet,
            title=title,
            timestamp=datetime.now(timezone.utc).isoformat(),
            query=search_query,
            content_hash=content_hash,
            relevance=relevance,
        )
        artifacts.append(artifact)

        # Stop once we have enough relevant results
        if len(artifacts) >= count:
            break

    return artifacts


def format_evidence_for_context(artifacts: List[EvidenceArtifact]) -> str:
    """Format evidence artifacts as context string."""
    if not artifacts:
        return ""

    context_parts = []
    for i, art in enumerate(artifacts[:3], 1):  # Top 3 results
        context_parts.append(f"[{i}] {art.title}\n{art.snippet}\nSource: {art.source}")

    return "\n\n".join(context_parts)
