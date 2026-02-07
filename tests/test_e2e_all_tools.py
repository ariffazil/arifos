"""
E2E Test Suite for arifOS v55.5 MCP Tools
Tests all engine adapters directly (bypasses FastMCP transport layer).

Author: arifOS Testing Framework
Version: v55.5.0
"""

import asyncio
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Import engine adapters (the real logic behind the tools)
from aaa_mcp.core.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from aaa_mcp.tools.reality_grounding import reality_check


async def test_all_tools():
    print("=" * 60)
    print("arifOS E2E Tool Verification (9 Canonical Tools v55.5)")
    print("=" * 60)

    query = "Should I implement a neural-linked voting system for arifOS?"
    results = {}
    passed = 0
    failed = 0

    # 1. init_gate (000)
    print("\n--- 1. Testing init_gate (InitEngine.ignite) ---")
    try:
        init_engine = InitEngine()
        res_init = await init_engine.ignite(query=query)
        session_id = res_init.get("session_id", "test_session_001")
        print(f"  Verdict: {res_init.get('verdict')} | Session: {session_id}")
        print(f"  Mode: {res_init.get('engine_mode', 'unknown')}")
        results["init_gate"] = res_init
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        session_id = "test_session_001"
        results["init_gate"] = {"error": str(e)}
        failed += 1

    # 2. agi_sense (111)
    print("\n--- 2. Testing agi_sense (AGIEngine.sense) ---")
    try:
        agi_engine = AGIEngine()
        res_sense = await agi_engine.sense(query=query, session_id=session_id)
        print(
            f"  Verdict: {res_sense.get('verdict')} | Trinity: {res_sense.get('trinity_component')}"
        )
        print(f"  Mode: {res_sense.get('engine_mode', 'unknown')}")
        results["agi_sense"] = res_sense
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["agi_sense"] = {"error": str(e)}
        failed += 1

    # 3. agi_think (222)
    print("\n--- 3. Testing agi_think (AGIEngine.think) ---")
    try:
        res_think = await agi_engine.think(query=query, session_id=session_id)
        print(
            f"  Verdict: {res_think.get('verdict')} | Confidence: {res_think.get('confidence', 'N/A')}"
        )
        print(f"  Mode: {res_think.get('engine_mode', 'unknown')}")
        results["agi_think"] = res_think
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["agi_think"] = {"error": str(e)}
        failed += 1

    # 4. agi_reason (333)
    print("\n--- 4. Testing agi_reason (AGIEngine.reason) ---")
    try:
        res_reason = await agi_engine.reason(query=query, session_id=session_id)
        print(
            f"  Verdict: {res_reason.get('verdict')} | Confidence: {res_reason.get('confidence', 'N/A')}"
        )
        print(f"  Mode: {res_reason.get('engine_mode', 'unknown')}")
        results["agi_reason"] = res_reason
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["agi_reason"] = {"error": str(e)}
        failed += 1

    # 5. reality_search (auxiliary)
    print("\n--- 5. Testing reality_search (reality_check) ---")
    try:
        res_reality = await reality_check(query="neural-linked voting system ethics")
        print(
            f"  Verdict: {res_reality.get('verdict', 'N/A')} | Source: {res_reality.get('source', 'N/A')}"
        )
        results["reality_search"] = res_reality
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["reality_search"] = {"error": str(e)}
        failed += 1

    # 6. asi_empathize (555)
    print("\n--- 6. Testing asi_empathize (ASIEngine.empathize) ---")
    try:
        asi_engine = ASIEngine()
        res_empathize = await asi_engine.empathize(query=query, session_id=session_id)
        print(
            f"  Verdict: {res_empathize.get('verdict')} | Trinity: {res_empathize.get('trinity_component')}"
        )
        print(f"  Mode: {res_empathize.get('engine_mode', 'unknown')}")
        results["asi_empathize"] = res_empathize
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["asi_empathize"] = {"error": str(e)}
        failed += 1

    # 7. asi_align (666)
    print("\n--- 7. Testing asi_align (ASIEngine.align) ---")
    try:
        res_align = await asi_engine.align(query=query, session_id=session_id)
        print(
            f"  Verdict: {res_align.get('verdict')} | Trinity: {res_align.get('trinity_component')}"
        )
        print(f"  Mode: {res_align.get('engine_mode', 'unknown')}")
        results["asi_align"] = res_align
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["asi_align"] = {"error": str(e)}
        failed += 1

    # 8. apex_verdict (888)
    print("\n--- 8. Testing apex_verdict (APEXEngine.judge) ---")
    try:
        apex_engine = APEXEngine()
        res_apex = await apex_engine.judge(query=query, session_id=session_id)
        print(
            f"  Verdict: {res_apex.get('verdict')} | Trinity: {res_apex.get('trinity_component')}"
        )
        print(f"  Mode: {res_apex.get('engine_mode', 'unknown')}")
        results["apex_verdict"] = res_apex
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["apex_verdict"] = {"error": str(e)}
        failed += 1

    # 9. vault_seal (999)
    print("\n--- 9. Testing vault_seal (vault persistence) ---")
    try:
        from codebase.vault.persistent_ledger_hardened import get_hardened_vault_ledger

        ledger = get_hardened_vault_ledger()
        await ledger.connect()

        # Hardened ledger requires proper seal_data structure
        payload = {
            "query": query,
            "trinity": {
                "init": {"verdict": "SEAL"},
                "agi": {"verdict": "SEAL"},
                "asi": {"verdict": "SEAL"},
                "apex": {"verdict": "SEAL", "tri_witness": 0.99},
            },
            "eureka": {"eureka_score": 0.85, "verdict": "SEAL"},
        }
        res_vault = await ledger.append(
            session_id=session_id, verdict="SEAL", seal_data=payload, authority="test_e2e"
        )
        print(f"  Status: SEALED | Sequence: {res_vault.get('sequence_number', 'N/A')}")
        results["vault_seal"] = res_vault
        passed += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        results["vault_seal"] = {"error": str(e)}
        failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"E2E Verification Complete: {passed}/{passed+failed} tools passed")
    if failed == 0:
        print("STATUS: ALL TESTS PASSED")
    else:
        print(f"STATUS: {failed} FAILURES")
    print("=" * 60)

    return results


if __name__ == "__main__":
    asyncio.run(test_all_tools())
