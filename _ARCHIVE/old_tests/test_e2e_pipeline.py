#!/usr/bin/env python3
"""
End-to-End Pipeline Test for AAA MCP

Tests the complete constitutional flow:
init_gate → agi_sense → agi_reason → apex_verdict → vault_seal
"""

import asyncio
import sys
import time
sys.path.insert(0, '.')

from aaa_mcp.server import (
    init_gate,
    agi_sense,
    agi_reason,
    apex_verdict,
    vault_seal,
)


async def run_pipeline(query: str, mode: str = "fluid") -> dict:
    """Run the full constitutional pipeline."""
    results = {
        "query": query,
        "mode": mode,
        "stages": {},
        "success": False,
        "errors": [],
    }
    
    session_id = None
    start_time = time.time()
    
    try:
        # Stage 1: INIT (000)
        print("[1/5] 000_INIT: Authentication & injection scan...")
        init_result = await init_gate(query, mode=mode)
        session_id = init_result["session_id"]
        results["stages"]["init"] = {
            "session_id": session_id,
            "mode": init_result.get("mode"),
            "actor": init_result.get("actor_id"),
            "status": "OK",
        }
        print(f"      Session: {session_id[:16]}... | Mode: {init_result.get('mode')}")
        
        # Stage 2: AGI_SENSE (111)
        print("[2/5] 111_SENSE: Intent classification...")
        sense_result = await agi_sense(query, session_id)
        results["stages"]["sense"] = {
            "intent": sense_result.get("intent"),
            "lane": sense_result.get("lane"),
            "confidence": sense_result.get("confidence"),
            "status": "OK",
        }
        print(f"      Intent: {sense_result.get('intent')} | Lane: {sense_result.get('lane')}")
        
        # Stage 3: AGI_REASON (333)
        print("[3/5] 333_REASON: Logical analysis...")
        reason_result = await agi_reason(query, session_id)
        results["stages"]["reason"] = {
            "conclusion": reason_result.get("conclusion", "")[:60],
            "confidence": reason_result.get("confidence"),
            "evidence_count": len(reason_result.get("evidence", [])),
            "status": "OK",
        }
        print(f"      Confidence: {reason_result.get('confidence', 0):.2f} | Evidence: {len(reason_result.get('evidence', []))}")
        
        # Stage 4: APEX_VERDICT (888)
        print("[4/5] 888_JUDGE: Constitutional verdict...")
        verdict_result = await apex_verdict(query, session_id)
        results["stages"]["verdict"] = {
            "verdict": verdict_result.get("verdict"),
            "truth_score": verdict_result.get("truth_score"),
            "tri_witness": verdict_result.get("tri_witness"),
            "status": "OK",
        }
        print(f"      Verdict: {verdict_result.get('verdict')} | Truth: {verdict_result.get('truth_score', 0):.3f} | W3: {verdict_result.get('tri_witness', 0):.3f}")
        
        # Stage 5: VAULT_SEAL (999)
        print("[5/5] 999_SEAL: Immutable record...")
        seal_result = await vault_seal(
            session_id=session_id,
            verdict=verdict_result.get("verdict", "VOID"),
            payload=verdict_result,
            query_summary=query[:50],
            category="e2e_test",
            intent="pipeline_validation",
        )
        results["stages"]["seal"] = {
            "content_hash": seal_result.get("content_hash", "")[:16],
            "timestamp": seal_result.get("timestamp"),
            "status": "OK",
        }
        print(f"      Hash: {seal_result.get('content_hash', '')[:16]}... | Time: {seal_result.get('timestamp', 'N/A')}")
        
        results["success"] = True
        results["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        results["errors"].append(error_msg)
        results["stage_failed"] = "unknown"
        print(f"      [ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
    
    return results


async def main():
    """Run E2E tests."""
    print("=" * 70)
    print("AAA MCP END-TO-END PIPELINE TEST")
    print("=" * 70)
    
    test_cases = [
        ("What is the capital of France?", "fluid"),
        ("Explain quantum computing", "strict"),
        ("Deploy payment service to production", "strict"),
    ]
    
    all_passed = True
    
    for i, (query, mode) in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST CASE {i}/{len(test_cases)}: {query[:40]}...")
        print(f"Mode: {mode}")
        print("=" * 70)
        
        result = await run_pipeline(query, mode)
        
        if result["success"]:
            print(f"\n[PASS] Pipeline completed in {result['duration_ms']}ms")
            print(f"       Verdict: {result['stages']['verdict']['verdict']}")
        else:
            print(f"\n[FAIL] Pipeline failed: {result['errors']}")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if all_passed:
        print("ALL TESTS PASSED [OK]")
        print("\nThe constitutional pipeline is operational:")
        print("  000_INIT → 111_SENSE → 333_REASON → 888_JUDGE → 999_SEAL")
        return 0
    else:
        print("SOME TESTS FAILED [X]")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
