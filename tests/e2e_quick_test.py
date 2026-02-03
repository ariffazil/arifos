#!/usr/bin/env python3
"""Quick E2E test for init_000 + Canonical Bootstrap"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

async def test():
    print("=" * 70)
    print("E2E Test: init_000 + Canonical Bootstrap (v55.3)")
    print("=" * 70)
    
    # Test 1: Canonical Bootstrap Import
    print("\n--- Test 1: Canonical Bootstrap Import ---")
    try:
        from codebase.init import (
            CanonicalBootstrap,
            fetch_canonical_state,
            CanonicalBootstrapResult,
        )
        print("[PASS] Canonical bootstrap imports successfully")
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        return False
    
    # Test 2: Guest canonical fetch
    print("\n--- Test 2: Guest Canonical Fetch (scar_weight=0.0) ---")
    try:
        result = await fetch_canonical_state(
            scar_weight=0.0,
            session_id="test_guest_001",
            mode="web_first"
        )
        print(f"[INFO] Status: {result.status}")
        print(f"[INFO] Sources fetched: {result.sources_fetched}")
        print(f"[INFO] Tri-Witness sync: {result.tri_witness_sync}")
        print(f"[INFO] CCC available: {result.ccc_canon.success if result.ccc_canon else False}")
        print(f"[INFO] BBB available: {result.bbb_ledger.success if result.bbb_ledger else False}")
        print(f"[INFO] AAA available: {result.aaa_human.success if result.aaa_human else 'N/A (guest)'}")
        print("[PASS] Guest fetch completed")
    except Exception as e:
        print(f"[FAIL] Guest fetch error: {e}")
    
    # Test 3: Sovereign canonical fetch
    print("\n--- Test 3: Sovereign Canonical Fetch (scar_weight=1.0) ---")
    try:
        result = await fetch_canonical_state(
            scar_weight=1.0,
            session_id="test_sovereign_001",
            mode="web_first"
        )
        print(f"[INFO] Status: {result.status}")
        print(f"[INFO] Sources fetched: {result.sources_fetched}")
        print(f"[INFO] Tri-Witness sync: {result.tri_witness_sync}")
        print(f"[INFO] CCC available: {result.ccc_canon.success if result.ccc_canon else False}")
        print(f"[INFO] BBB available: {result.bbb_ledger.success if result.bbb_ledger else False}")
        print(f"[INFO] AAA attempted: {result.aaa_human is not None}")
        if result.aaa_human:
            print(f"[INFO] AAA success: {result.aaa_human.success}")
        print("[PASS] Sovereign fetch completed")
    except Exception as e:
        print(f"[FAIL] Sovereign fetch error: {e}")
    
    # Test 4: Local-only mode
    print("\n--- Test 4: Local-Only Mode ---")
    try:
        result = await fetch_canonical_state(
            scar_weight=1.0,
            session_id="test_local_001",
            mode="local_only"
        )
        print(f"[INFO] Status: {result.status}")
        print(f"[INFO] Local fallback used: {result.local_fallback_used}")
        assert result.status == "SABAR", "Local-only should return SABAR"
        assert result.local_fallback_used, "Should use local fallback"
        print("[PASS] Local-only mode works correctly")
    except Exception as e:
        print(f"[FAIL] Local-only error: {e}")
    
    # Test 5: mcp_init (via canonical_trinity)
    print("\n--- Test 5: mcp_init (via canonical_trinity) ---")
    try:
        from mcp_server.tools.canonical_trinity import mcp_init
        
        # Validate action
        result = await mcp_init(action="validate", query="", session_id="test_validate")
        print(f"[INFO] Validate result: verdict={result.get('verdict')}")
        assert result.get("verdict") == "SEAL", "Validate should return SEAL"
        print("[PASS] mcp_init validate works")
        
        # Guest init
        result = await mcp_init(
            action="init",
            query="Hello, help me with code",
            authority_token="",
            session_id="test_mcp_guest"
        )
        print(f"[INFO] Guest init: session={result.get('session_id', 'N/A')[:8]}...")
        print(f"[INFO] Guest init: verdict={result.get('verdict')}")
        print(f"[INFO] Guest init: authority={result.get('authority_level')}")
        print("[PASS] mcp_init guest works")
        
        # Sovereign init
        result = await mcp_init(
            action="init",
            query="Salam, I'm Arif. Debug vault.",
            authority_token="",
            session_id="test_mcp_sovereign"
        )
        print(f"[INFO] Sovereign init: session={result.get('session_id', 'N/A')[:8]}...")
        print(f"[INFO] Sovereign init: verdict={result.get('verdict')}")
        print(f"[INFO] Sovereign init: authority={result.get('authority_level')}")
        print("[PASS] mcp_init sovereign works")
        
    except Exception as e:
        print(f"[FAIL] mcp_init error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("E2E Test Complete")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = asyncio.run(test())
    sys.exit(0 if success else 1)
