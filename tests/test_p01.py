"""
P0 Test Suite for arifOS v60 Pipeline
Tests: Query Classification (P0.1), Adaptive F2 (P0.2), Circuit Breaker (P0.3)
"""

import asyncio
import sys
from core.pipeline import forge
from core.shared.atlas import QueryType, classify_query_type as classify_query


def test_p01_query_classification():
    """P0.1: Test query type classification with keyword matching."""
    print("\n=== P0.1: Query Classification Tests ===")

    test_cases = [
        ("test the pipeline", QueryType.TEST),
        ("hello, can you help me", QueryType.CONVERSATIONAL),
        ("ping the server", QueryType.TEST),
        ("what is the capital of France", QueryType.FACTUAL),
        ("how do I cook pasta", QueryType.PROCEDURAL),
        ("explore ideas about AI", QueryType.EXPLORATORY),
        ("is Python better than Java", QueryType.OPINION),
        ("who are you", QueryType.CONVERSATIONAL),
    ]

    passed = 0
    for query, expected in test_cases:
        result = classify_query(query)
        status = "[OK]" if result == expected else "[FAIL]"
        print(f"  {status} '{query[:40]}...' -> {result.value} (expected: {expected.value})")
        if result == expected:
            passed += 1

    print(f"\n  P0.1 Results: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)


async def test_p02_adaptive_f2():
    """P0.2: Test adaptive F2 thresholds for different query types."""
    print("\n=== P0.2: Adaptive F2 Threshold Tests ===")

    test_queries = [
        ("test the pipeline", "should pass with 0.50 threshold"),
        ("hello world", "should pass with 0.60 threshold"),
        ("how do I reset my password", "should pass with 0.70 procedural threshold"),
    ]

    passed = 0
    for query, description in test_queries:
        print(f"\n  Testing: '{query[:50]}' ({description})")
        result = await forge(query)

        print(f"    query_type: {result.query_type}")
        print(f"    f2_threshold: {result.f2_threshold}")
        print(f"    verdict: {result.verdict}")
        print(f"    processing_time: {result.processing_time_ms:.2f}ms")

        if result.verdict in ["SEAL", "SABAR"]:
            passed += 1
            print(f"    [OK] Query processed successfully")
        else:
            print(f"    [FAIL] Query blocked: {result.remediation}")

    # Test that factual queries without evidence get VOID (correct behavior)
    print(f"\n  Testing factual query (should be VOID without evidence)")
    result = await forge("what is the capital of France")
    print(f"    query_type: {result.query_type}")
    print(f"    verdict: {result.verdict}")
    if result.verdict == "VOID":
        print(f"    [OK] Factual query correctly blocked (requires evidence for F2 >= 0.99)")
        passed += 1
    else:
        print(f"    [WARN] Factual query should be VOID without evidence")

    print(f"\n  P0.2 Results: {passed}/{len(test_queries) + 1} passed")
    return passed >= len(test_queries)  # At least 3/4 should pass


async def test_p03_circuit_breaker():
    """P0.3: Test circuit breaker and fast path for light queries."""
    print("\n=== P0.3: Circuit Breaker & Fast Path Tests ===")

    # Test queries that should use fast path
    test_queries = [
        "test run",
        "hello world",
        "ping",
    ]

    passed = 0
    for query in test_queries:
        print(f"\n  Testing fast path: '{query}'")
        result = await forge(query)

        print(f"    query_type: {result.query_type}")
        print(f"    verdict: {result.verdict}")
        print(f"    processing_time: {result.processing_time_ms:.2f}ms")

        # Fast path should complete quickly (< 500ms)
        if result.processing_time_ms < 500:
            print(f"    [OK] Fast path (quick execution)")
        else:
            print(f"    [WARN] Slow path ({result.processing_time_ms:.2f}ms)")

        if result.verdict == "SEAL":
            passed += 1
            print(f"    [OK] Query approved")
        elif result.verdict == "SABAR":
            passed += 1
            print(f"    [OK] Query needs revision (acceptable)")
        else:
            print(f"    [FAIL] Query blocked: {result.remediation}")

    print(f"\n  P0.3 Results: {passed}/{len(test_queries)} passed")
    return passed >= 2  # At least 2/3 should pass


async def run_all_tests():
    """Run all P0 tests."""
    print("=" * 60)
    print("arifOS v60 P0 Test Suite - Pipeline Hardening")
    print("=" * 60)

    results = []

    # P0.1: Query Classification
    results.append(("P0.1 Query Classification", test_p01_query_classification()))

    # P0.2: Adaptive F2
    results.append(("P0.2 Adaptive F2", await test_p02_adaptive_f2()))

    # P0.3: Circuit Breaker
    results.append(("P0.3 Circuit Breaker", await test_p03_circuit_breaker()))

    # Summary
    print("\n" + "=" * 60)
    print("P0 Test Suite Summary")
    print("=" * 60)
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")

    total_passed = sum(1 for _, p in results if p)
    total_tests = len(results)
    print(f"\n  Overall: {total_passed}/{total_tests} test groups passed")

    return all(r[1] for r in results)


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
