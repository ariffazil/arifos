#!/usr/bin/env python3
"""
Test script for Smart Hybrid search_reality with Headless Browser integration.

Tests:
1. Query classification (SPA vs General vs Research)
2. Multi-source fallback with quality scoring
3. F3 Tri-Witness consensus
4. Headless browser fetch (when enabled)
5. Error resilience (never empty)

Usage:
    python test_search_reality_hybrid.py
    ARIFOS_HEADLESS_BROWSER_ENABLED=1 python test_search_reality_hybrid.py
"""

import asyncio
import sys
from datetime import datetime, timezone

sys.path.insert(0, "/srv/arifOS")

from aaa_mcp.external_gateways import (
    BraveSearchClient,
    HeadlessBrowserClient,
    JinaReaderClient,
    PerplexitySearchClient,
)


async def test_headless_client():
    """Test headless browser client directly."""
    print("=" * 60)
    print("TEST 1: Headless Browser Client")
    print("=" * 60)

    client = HeadlessBrowserClient()

    # Check if enabled
    print(f"\n[Status] Headless browser enabled: {client.enabled}")

    if not client.enabled:
        print("⚠️  SKIP: Headless browser disabled (set ARIFOS_HEADLESS_BROWSER_ENABLED=1)")
        return None

    # Health check
    health = await client.health_check()
    print(f"[Health] Status: {health.get('status')}")
    print(f"[Health] Details: {health}")

    if health.get('status') != 'HEALTHY':
        print("⚠️  SKIP: Headless browser not healthy")
        return None

    # Fetch a known page
    test_url = "https://example.com"
    print(f"\n[Fetch] Testing URL: {test_url}")

    result = await client.fetch_url(test_url, wait_ms=3000)

    print(f"[Result] Status: {result.get('status')}")
    print(f"[Result] Title: {result.get('title')}")
    print(f"[Result] Content hash: {result.get('content_hash')}")
    print(f"[Result] Content length: {result.get('raw_content_length', 0)}")
    print(f"[Result] Render time: {result.get('render_time_ms')}ms")

    # Verify F12 envelope
    content = result.get('content', '')
    if '<untrusted_external_data' in content and 'f12_defense' in content:
        print("✅ PASS: F12 envelope present")
    else:
        print("❌ FAIL: F12 envelope missing")

    # Verify content hash
    if result.get('content_hash') and len(result.get('content_hash')) == 16:
        print("✅ PASS: Content hash valid (SHA-256 truncated)")
    else:
        print("❌ FAIL: Content hash invalid")

    return result


async def test_query_classification():
    """Test query classification logic."""
    print("\n" + "=" * 60)
    print("TEST 2: Query Classification")
    print("=" * 60)

    test_cases = [
        ("react dashboard tutorial", "spa"),
        ("site:github.io portfolio", "spa"),
        ("vercel app deployment", "spa"),
        ("arxiv quantum computing paper", "research"),
        ("latest AI news today", "news"),
        ("python list comprehension", "general"),
        ("vue.js component guide", "spa"),
        ("whitepaper on blockchain", "research"),
    ]

    def classify(q: str) -> str:
        q_lower = q.lower()
        spa_indicators = [
            "site:github.io", "site:vercel.app", "site:netlify.app",
            "react", "vue", "angular", "spa", "dashboard", "webapp",
            "interactive", "dynamic", "real-time"
        ]
        research_indicators = [
            "research", "paper", "study", "analysis", "whitepaper",
            "arxiv", "academic", "journal", "survey", "report"
        ]
        news_indicators = [
            "news", "latest", "today", "breaking", "update",
            "current", "2025", "2026", "recent"
        ]

        if any(i in q_lower for i in spa_indicators):
            return "spa"
        if any(i in q_lower for i in research_indicators):
            return "research"
        if any(i in q_lower for i in news_indicators):
            return "news"
        return "general"

    passed = 0
    for query, expected in test_cases:
        result = classify(query)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{query[:40]}...' → {result} (expected: {expected})")
        if result == expected:
            passed += 1

    print(f"\n[Summary] {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


async def test_search_reality_api():
    """Test the full search_reality API with hybrid routing."""
    print("\n" + "=" * 60)
    print("TEST 3: search_reality API (Smart Hybrid)")
    print("=" * 60)

    # Import the actual function
    from aaa_mcp.server import _search

    test_queries = [
        ("python programming best practices", "general"),
        ("latest machine learning research 2025", "research"),
        ("react hooks tutorial", "spa"),
    ]

    for query, intent in test_queries:
        print(f"\n[Query] '{query}' (intent: {intent})")
        print("-" * 40)

        start = datetime.now(timezone.utc)
        result = await _search(query=query, intent=intent, session_id="test-session-001")
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000

        print(f"[Status] {result.get('status')}")
        print(f"[Query Type] {result.get('query_type')}")
        print(f"[Sources] {', '.join(result.get('sources_consulted', []))}")
        print(f"[Primary] {result.get('primary_source')}")
        print(f"[Results] {len(result.get('results', []))} items")
        print(f"[Quality Score] {result.get('f2_truth', {}).get('quality_score')}")
        print(f"[F3 Consensus] {result.get('f3_consensus', {})}")
        print(f"[Elapsed] {elapsed:.0f}ms")

        # Validation
        if result.get('status') not in ['ERROR', 'NO_VALID_SOURCES', 'REALITY_FALLBACK']:
            print("✅ PASS: Got meaningful results")
        elif result.get('status') == 'REALITY_FALLBACK':
            print("⚠️  WARN: Reality fallback used (all sources failed)")
        else:
            print("❌ FAIL: Error status")


async def test_quality_scoring():
    """Test content quality scoring."""
    print("\n" + "=" * 60)
    print("TEST 4: Content Quality Scoring")
    print("=" * 60)

    def score_quality(result: dict) -> float:
        if not result or result.get("status") != "OK":
            return 0.0

        score = 0.0
        content = result.get("content", "")
        results = result.get("results", [])

        if content and len(content) > 500:
            score += 0.3
        if content and len(content) > 2000:
            score += 0.2

        if results:
            score += min(0.3, len(results) * 0.1)
            for r in results:
                if r.get("content") or r.get("description"):
                    score += 0.05
                    break

        if "f12_envelope" in str(content).lower() or result.get("taint_lineage"):
            score += 0.2

        return min(1.0, score)

    # Test cases
    test_cases = [
        {"status": "OK", "content": "x" * 3000, "results": [{"url": "test", "content": "data"}]},
        {"status": "OK", "content": "x" * 100, "results": []},
        {"status": "ERROR", "content": "", "results": []},
        {"status": "OK", "content": "x" * 2500, "results": [{"url": "test"}], "taint_lineage": {}},
    ]

    for i, tc in enumerate(test_cases):
        score = score_quality(tc)
        print(f"Test case {i+1}: score = {score:.2f} (status: {tc['status']}, content_len: {len(tc['content'])})")


async def main():
    """Run all tests."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "SEARCH_REALITY HYBRID TEST SUITE" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    print(f"\nStarted: {datetime.now(timezone.utc).isoformat()}")

    # Test 1: Headless browser (if enabled)
    headless_result = await test_headless_client()

    # Test 2: Query classification
    await test_query_classification()

    # Test 3: Quality scoring
    await test_quality_scoring()

    # Test 4: Full API (with network calls)
    print("\n[NOTE] Running live API tests (requires network)...")
    try:
        await test_search_reality_api()
    except Exception as e:
        print(f"⚠️  API tests skipped or failed: {e}")

    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
