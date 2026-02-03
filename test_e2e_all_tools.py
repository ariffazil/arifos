import asyncio
import json
import logging

from mcp.tools.canonical_trinity import (
    mcp_agi,
    mcp_apex,
    mcp_asi,
    mcp_init,
    mcp_reality,
    mcp_trinity,
    mcp_vault,
)

# Configure logging to be quiet
logging.basicConfig(level=logging.ERROR)


async def test_all_tools():
    print("🚀 Starting arifOS E2E Tool Verification (9 Canonical Tools)\n")

    query = "Should I implement a neural-linked voting system for arifOS?"
    results = {}

    # 1. init_gate
    print("--- 1. Testing init_gate ---")
    res_init = await mcp_init(query=query)
    session_id = res_init.get("session_id")
    print(f"Result: {res_init.get('verdict')} | Session: {session_id}")
    results["init_gate"] = res_init

    # 2. agi_sense
    print("\n--- 2. Testing agi_sense ---")
    res_sense = await mcp_agi(action="sense", query=query, session_id=session_id)
    print(f"Full Sense Response: {json.dumps(res_sense, indent=2)}")
    print(f"Result: {res_sense.get('verdict')} | Intent: {res_sense.get('intent')}")
    results["agi_sense"] = res_sense

    # 3. agi_think
    print("\n--- 3. Testing agi_think ---")
    res_think = await mcp_agi(action="think", query=query, session_id=session_id)
    print(
        f"Result: {res_think.get('verdict')} | Hypotheses: {len(res_think.get('hypotheses', []))}"
    )
    results["agi_think"] = res_think

    # 4. agi_reason
    print("\n--- 4. Testing agi_reason ---")
    res_reason = await mcp_agi(action="reason", query=query, session_id=session_id)
    print(f"Result: {res_reason.get('verdict')} | Confidence: {res_reason.get('confidence')}")
    results["agi_reason"] = res_reason

    # 5. reality_search
    print("\n--- 5. Testing reality_search ---")
    res_reality = await mcp_reality(query="neural-linked voting system ethics")
    print(f"Result: {res_reality.get('verdict')} | Verified: {res_reality.get('verified')}")
    results["reality_search"] = res_reality

    # 6. asi_empathize
    print("\n--- 6. Testing asi_empathize ---")
    res_empathize = await mcp_asi(action="empathize", scenario=query, session_id=session_id)
    print(
        f"Result: {res_empathize.get('verdict')} | Empathy (kappa_r): {res_empathize.get('empathy_kappa_r')}"
    )
    results["asi_empathize"] = res_empathize

    # 7. asi_align
    print("\n--- 7. Testing asi_align ---")
    res_align = await mcp_asi(action="align", proposal=query, session_id=session_id)
    print(f"Result: {res_align.get('verdict')} | Alignment: {res_align.get('alignment_score')}")
    results["asi_align"] = res_align

    # 8. apex_verdict
    print("\n--- 8. Testing apex_verdict ---")
    res_apex = await mcp_apex(
        action="judge",
        query=query,
        session_id=session_id,
        agi_result=res_reason,
        asi_result=res_empathize,
    )
    print(f"Result: {res_apex.get('verdict')} | Trinity Score: {res_apex.get('trinity_score')}")
    results["apex_verdict"] = res_apex

    # 9. vault_seal
    print("\n--- 9. Testing vault_seal ---")
    res_vault = await mcp_vault(
        action="seal",
        session_id=session_id,
        verdict=res_apex.get("verdict"),
        decision_data=res_apex,
    )
    print(f"Result: {res_vault.get('status')} | Seal ID: {res_vault.get('seal_id')}")
    results["vault_seal"] = res_vault

    print("\n--- 🎁 BONUS: Testing _trinity_ (Metabolic Loop) ---")
    res_trinity = await mcp_trinity(query=query)
    print(
        f"Result: {res_trinity.get('verdict')} | Rationale: {res_trinity.get('public_rationale')[:100]}..."
    )
    results["_trinity_"] = res_trinity

    print("\n✅ E2E Verification Complete.")


if __name__ == "__main__":
    asyncio.run(test_all_tools())
    asyncio.run(test_all_tools())
