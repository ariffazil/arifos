
import asyncio
import json
import sys
from arifos_aaa_mcp.server import vector_memory, search_reality, anchor_session

async def test_modern_params():
    print("🚀 Starting Modern Parameter Verification...")
    
    # 1. Anchor Session
    print("\n--- 000 ANCHOR ---")
    anch = await anchor_session(query="Verification of modern parameters", actor_id="test-validator")
    session_token = anch.get("session_id")
    print(f"✅ Session Anchored: {session_token}")
    
    # 2. Test Vector Memory with modern params
    print("\n--- 555 VECTOR MEMORY (Modern) ---")
    vm_res = await vector_memory(
        current_thought_vector="Constitutional AI Governance",
        session_token=session_token
    )
    print(f"Verdict: {vm_res.get('verdict')}")
    print(f"Status: {vm_res.get('payload', {}).get('status')}")
    assert vm_res.get("verdict") == "SEAL"
    assert "metrics" in vm_res.get("payload", {})
    print("✅ vector_memory modern params verified.")
    
    # 3. Test Search Reality with modern params
    print("\n--- SEARCH REALITY (Modern) ---")
    sr_res = await search_reality(
        grounding_query="latest news on arifOS",
        session_token=session_token
    )
    print(f"Status: {sr_res.get('status', sr_res.get('payload', {}).get('status'))}")
    # Note: Search might return ERROR if API keys are missing, but it shouldn't be VOID due to params
    if sr_res.get("verdict") == "VOID":
        print(f"❌ search_reality VOID: {sr_res.get('error')}")
        sys.exit(1)
    print("✅ search_reality modern params verified.")

    # 4. Test Backward Compatibility
    print("\n--- BACKWARD COMPATIBILITY CHECK ---")
    vm_legacy = await vector_memory(
        query="Legacy query",
        session_id=session_token
    )
    assert vm_legacy.get("verdict") == "SEAL"
    print("✅ vector_memory legacy params verified.")
    
    print("\n✨ ALL MODERN PARAMETERS VERIFIED SUCCESSFULLY.")

if __name__ == "__main__":
    asyncio.run(test_modern_params())
