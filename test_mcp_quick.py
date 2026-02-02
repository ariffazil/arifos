#!/usr/bin/env python
"""Quick test of all 7 MCP canonical tools."""

import asyncio
import sys
import time

# Test the canonical tools directly
from codebase.mcp.tools.canonical_trinity import (
    mcp_init,
    mcp_agi,
    mcp_asi,
    mcp_apex,
    mcp_vault,
    mcp_trinity,
    mcp_reality,
)

async def test_all_tools():
    """Test all 7 MCP tools."""
    print("=" * 70)
    print("AAA MCP DEPLOYMENT READINESS CHECK")
    print("=" * 70)
    
    session_id = f"test_{int(time.time())}"
    query = "What are best practices for Python error handling?"
    
    results = {
        "mcp_init": False,
        "mcp_agi": False,
        "mcp_asi": False,
        "mcp_apex": False,
        "mcp_vault": False,
        "mcp_trinity": False,
        "mcp_reality": False,
    }
    
    # 1. Test mcp_init (000 Gate)
    print("\n[1/7] Testing mcp_init (000 Gate)...")
    try:
        init_result = await mcp_init(query=query, session_id=session_id)
        print(f"  Status: {init_result.get('verdict', 'UNKNOWN')}")
        print(f"  Session: {init_result.get('session_id', 'N/A')[:20]}...")
        print(f"  Authority: {init_result.get('authority_level', 'N/A')}")
        results["mcp_init"] = init_result.get('verdict') in ['SEAL', 'AUTHORIZED']
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # 2. Test mcp_agi (111-333 Mind)
    print("\n[2/7] Testing mcp_agi (111-333 Mind)...")
    try:
        agi_result = await mcp_agi(query=query, session_id=session_id, action="sense")
        print(f"  Status: {agi_result.get('verdict', 'UNKNOWN')}")
        print(f"  Entropy Delta: {agi_result.get('entropy_delta', 'N/A')}")
        results["mcp_agi"] = agi_result.get('verdict') == 'SEAL'
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # 3. Test mcp_asi (555 Heart) - T1.3 Bug should be fixed now
    print("\n[3/7] Testing mcp_asi (555 Heart)...")
    try:
        asi_result = await mcp_asi(query=query, session_id=session_id, action="empathize")
        print(f"  Status: {asi_result.get('verdict', 'UNKNOWN')}")
        print(f"  Omega Total: {asi_result.get('omega_total', 'N/A')}")
        print(f"  Empathy (kappa_r): {asi_result.get('empathy_kappa_r', 'N/A')}")
        print(f"  Peace²: {asi_result.get('peace_squared', 'N/A')}")
        # After T1.3 fix, benign queries should SEAL
        results["mcp_asi"] = asi_result.get('verdict') == 'SEAL'
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # 4. Test mcp_apex (777-888 Soul)
    print("\n[4/7] Testing mcp_apex (777-888 Soul)...")
    try:
        apex_result = await mcp_apex(query=query, session_id=session_id, action="full")
        print(f"  Status: {apex_result.get('verdict', 'UNKNOWN')}")
        print(f"  Trinity Score: {apex_result.get('trinity_score', 'N/A')}")
        results["mcp_apex"] = apex_result.get('verdict') in ['SEAL', 'APPROVE']
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # 5. Test mcp_vault (999 Seal)
    print("\n[5/7] Testing mcp_vault (999 Seal)...")
    try:
        vault_result = await mcp_vault(
            action="seal",
            verdict="SEAL",
            session_id=session_id,
            query=query,
            response="Test response",
            decision_data={"test": "data"}
        )
        print(f"  Operation: {vault_result.get('operation', 'N/A')}")
        print(f"  Verdict: {vault_result.get('verdict', 'N/A')}")
        print(f"  Position: {vault_result.get('position', 'N/A')}")
        results["mcp_vault"] = vault_result.get('operation') == 'seal'
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # 6. Test mcp_trinity (Full Loop)
    print("\n[6/7] Testing mcp_trinity (Full 000-999 Loop)...")
    try:
        trinity_result = await mcp_trinity(query=query, session_id=session_id)
        print(f"  Status: {trinity_result.get('status', 'UNKNOWN')}")
        print(f"  Final Verdict: {trinity_result.get('final_verdict', 'N/A')}")
        print(f"  Stages Completed: {trinity_result.get('stages_completed', 'N/A')}")
        results["mcp_trinity"] = trinity_result.get('status') == 'complete'
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # 7. Test mcp_reality (Grounding)
    print("\n[7/7] Testing mcp_reality (External Grounding)...")
    try:
        reality_result = await mcp_reality(query="What is the capital of France?", session_id=session_id)
        print(f"  Status: {reality_result.get('status', 'UNKNOWN')}")
        print(f"  Verdict: {reality_result.get('verdict', 'N/A')}")
        results["mcp_reality"] = reality_result.get('status') in ['VERIFIED', 'SABAR', 'complete']
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("DEPLOYMENT READINESS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for tool, status in results.items():
        symbol = "✓" if status else "✗"
        print(f"  [{symbol}] {tool}")
    
    print(f"\n  {passed}/{total} tools ready ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n  🎉 ALL TOOLS READY FOR DEPLOYMENT!")
        return 0
    else:
        print(f"\n  ⚠️ {total - passed} tools need attention before deployment")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_all_tools())
    sys.exit(exit_code)
