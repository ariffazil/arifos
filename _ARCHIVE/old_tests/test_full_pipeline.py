#!/usr/bin/env python3
"""Test script for full AAA MCP pipeline.

Tests: init_gate -> agi_sense -> agi_reason -> apex_verdict -> vault_seal
"""

import asyncio
import sys

sys.path.insert(0, ".")

# Import server module
import aaa_mcp.server as server


def get_underlying_function(tool_obj):
    """Extract the underlying function from a FunctionTool wrapper."""
    # FastMCP's FunctionTool stores the callable in different ways
    # Try common patterns
    if hasattr(tool_obj, "fn"):
        return tool_obj.fn
    if hasattr(tool_obj, "function"):
        return tool_obj.function
    if hasattr(tool_obj, "__wrapped__"):
        return tool_obj.__wrapped__
    # If it's a method wrapper, try to get __call__
    if hasattr(tool_obj, "__call__"):
        # Check if it's a callable object with a _func attribute
        if hasattr(tool_obj, "_func"):
            return tool_obj._func
    return tool_obj


async def test_pipeline():
    """Run the full constitutional pipeline."""
    print("=" * 70)
    print("AAA MCP FULL PIPELINE TEST")
    print("=" * 70)

    # Get underlying functions
    init_gate = get_underlying_function(server.init_gate)
    agi_sense = get_underlying_function(server.agi_sense)
    agi_reason = get_underlying_function(server.agi_reason)
    apex_verdict = get_underlying_function(server.apex_verdict)
    vault_seal = get_underlying_function(server.vault_seal)

    query = "What is the capital of France?"

    # Step 1: init_gate
    print("\n[1/5] init_gate...")
    try:
        init_result = await init_gate(query, mode="fluid")
        session_id = init_result["session_id"]
        print(f"  [OK] Session created: {session_id[:16]}...")
        print(f"      Mode: {init_result.get('mode', 'unknown')}")
        print(f"      Actor: {init_result.get('actor_id', 'unknown')}")
    except Exception as e:
        print(f"  [X] FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Step 2: agi_sense
    print("\n[2/5] agi_sense...")
    try:
        sense_result = await agi_sense(query, session_id)
        print(f"  [OK] Intent classified: {sense_result.get('intent', 'unknown')}")
        print(f"      Lane: {sense_result.get('lane', 'unknown')}")
        print(f"      Confidence: {sense_result.get('confidence', 0):.2f}")
    except Exception as e:
        print(f"  [X] FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Step 3: agi_reason
    print("\n[3/5] agi_reason...")
    try:
        reason_result = await agi_reason(query, session_id)
        print(f"  [OK] Reasoning complete")
        conclusion = reason_result.get("conclusion", "unknown")
        print(
            f"      Conclusion: {conclusion[:50]}..."
            if len(conclusion) > 50
            else f"      Conclusion: {conclusion}"
        )
        print(f"      Confidence: {reason_result.get('confidence', 0):.2f}")
        print(f"      Evidence count: {len(reason_result.get('evidence', []))}")
    except Exception as e:
        print(f"  [X] FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Step 4: apex_verdict (THE CRITICAL TEST)
    print("\n[4/5] apex_verdict...")
    try:
        verdict_result = await apex_verdict(query, session_id)
        print(f"  [OK] Verdict rendered: {verdict_result.get('verdict', 'UNKNOWN')}")
        print(f"      Truth score: {verdict_result.get('truth_score', 0):.3f}")
        print(f"      Tri-witness: {verdict_result.get('tri_witness', 0):.3f}")
        if verdict_result.get("justification"):
            just = verdict_result["justification"]
            print(
                f"      Justification: {just[:60]}..."
                if len(just) > 60
                else f"      Justification: {just}"
            )
    except Exception as e:
        print(f"  [X] FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Step 5: vault_seal
    print("\n[5/5] vault_seal...")
    try:
        seal_result = await vault_seal(
            session_id=session_id,
            verdict=verdict_result.get("verdict", "VOID"),
            payload=verdict_result,
            query_summary=query[:50],
            category="test",
            intent="pipeline_test",
        )
        print(f"  [OK] Sealed to VAULT999")
        print(f"      Content hash: {seal_result.get('content_hash', 'unknown')[:16]}...")
        print(f"      Timestamp: {seal_result.get('timestamp', 'unknown')}")
    except Exception as e:
        print(f"  [X] FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Summary
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE [OK]")
    print("=" * 70)
    print(f"Session: {session_id}")
    print(f"Verdict: {verdict_result.get('verdict')}")
    print(f"Truth: {verdict_result.get('truth_score', 0):.3f}")
    print(f"Tri-Witness: {verdict_result.get('tri_witness', 0):.3f}")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_pipeline())
    sys.exit(0 if success else 1)
