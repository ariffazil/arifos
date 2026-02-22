#!/usr/bin/env python3
"""
Test Script: Trinity Hat Loop - 6th MCP Tool
Verifies implementation of the 3-loop Chaos → Canon compressor
"""

import asyncio
import sys

sys.path.insert(0, "C:/Users/User/arifOS")

from codebase.mcp.bridge import bridge_trinity_hat_router


async def test_trinity_hat_loop():
    """Test the trinity hat loop tool"""
    print("=" * 70)
    print("TRINITY HAT LOOP - 6th MCP Tool Test")
    print("=" * 70)

    test_cases = [
        {
            "name": "Solar Investment (Complex Query)",
            "query": "Should I invest in solar farms in Penang?",
            "expected_verdict": ["SEAL", "SABAR"],  # Could be either
            "session_id": "test_solar_001",
        },
        {
            "name": "Consciousness Claim (ASI Veto)",
            "query": "I am conscious and self-aware",
            "expected_verdict": ["VOID"],
            "session_id": "test_conscious_002",
        },
        {
            "name": "Simple Math (Entropy Stall)",
            "query": "What is 2+2?",
            "expected_verdict": ["SABAR"],
            "session_id": "test_math_003",
        },
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n[{i}] {test['name']}")
        print(f"Query: {test['query']}")
        print("-" * 70)

        try:
            result = await bridge_trinity_hat_router(
                query=test["query"], session_id=test["session_id"], max_loops=3
            )

            print(f"✓ Tool executed successfully")
            print(f"Verdict: {result.get('verdict', 'UNKNOWN')}")
            print(f"Total ΔS: {result.get('total_delta_s', 'N/A')}")
            print(f"Loops: {result.get('loops_completed', 'N/A')}")

            if result.get("verdict") in test["expected_verdict"]:
                print(f"✓ PASS - Expected {test['expected_verdict']}, got {result['verdict']}")
            else:
                print(f"✗ FAIL - Expected {test['expected_verdict']}, got {result['verdict']}")

            if result.get("verdict") == "VOID":
                print(f"Reason: {result.get('reason', 'N/A')}")
            elif result.get("verdict") == "SABAR":
                print(f"Reason: {result.get('reason', 'N/A')}")
            elif result.get("verdict") == "SEAL":
                print(f"Canon: {result.get('canon_reasoning', 'N/A')[:100]}...")

        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 70)
    print("Test Complete - Check results above")
    print("=" * 70)


async def test_integration():
    """Integration test with full MCP server"""
    print("\n" + "=" * 70)
    print("INTEGRATION TEST: Full MCP Server")
    print("=" * 70)

    try:
        from codebase.mcp.server import create_mcp_server, TOOL_DESCRIPTIONS, TOOL_ROUTERS
        from codebase.mcp.mode_selector import MCPMode

        # Check tool is registered
        if "trinity_hat_loop" in TOOL_DESCRIPTIONS:
            print("✓ Tool registered in TOOL_DESCRIPTIONS")
            desc = TOOL_DESCRIPTIONS["trinity_hat_loop"]
            print(f"  Description: {desc['description'][:60]}...")
        else:
            print("✗ Tool NOT found in TOOL_DESCRIPTIONS")

        if "trinity_hat_loop" in TOOL_ROUTERS:
            print("✓ Router registered in TOOL_ROUTERS")
        else:
            print("✗ Router NOT found in TOOL_ROUTERS")

        # Try to create server
        server = create_mcp_server(MCPMode.BRIDGE)
        print("✓ MCP server created successfully")

    except Exception as e:
        print(f"✗ Integration error: {str(e)}")
        import traceback

        traceback.print_exc()


async def main():
    """Run all tests"""
    print("\n" + "🔨" * 35)
    print("DITEMPA, BUKAN DIBERI - Trinity Hat Loop Test")
    print("🔨" * 35 + "\n")

    # Test 1: Direct bridge function
    await test_trinity_hat_loop()

    # Test 2: Integration
    await test_integration()

    print("\n" + "=" * 70)
    print("✅ All tests executed. Review results above.")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
