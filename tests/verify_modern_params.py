
import asyncio
import json
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
        query="Constitutional AI Governance",
        session_id=session_token
    )
    print(f"Full VM Response: {json.dumps(vm_res, indent=2)}")
    print(f"Verdict: {vm_res.get('verdict')}")
    
    # Check if we got the session_id back
    assert vm_res.get("session_id") == session_token
    
    # 3. Test Search Reality with modern params
    print("\n--- SEARCH REALITY (Modern) ---")
    sr_res = await search_reality(
        grounding_query="latest news on arifOS",
        session_token=session_token
    )
    print(f"Full SR Response: {json.dumps(sr_res, indent=2)}")
    assert sr_res.get("session_id") == session_token
    
    print("\n✨ ALL MODERN PARAMETERS VERIFIED SUCCESSFULLY.")

if __name__ == "__main__":
    asyncio.run(test_modern_params())
