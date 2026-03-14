import asyncio
import os
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parents[1]))

# Set E2E environment profile
os.environ["ARIFOS_PUBLIC_TOOL_PROFILE"] = "full"
os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
os.environ["ARIFOS_ALLOW_LEGACY_SPEC"] = "1"
os.environ["AAA_MCP_OUTPUT_MODE"] = "debug"

from fastmcp import Client
from arifosmcp.runtime.server import create_aaa_mcp_server

async def run_e2e_test():
    print("🚀 Starting arifOS E2E Full Surface Test...")
    server = create_aaa_mcp_server()
    
    async with Client(server) as client:
        print("\n--- [1] PROMPTS ---")
        prompts = await client.list_prompts()
        print(f"Found {len(prompts)} prompts.")
        for p in prompts:
            print(f"  - {p.name}")

        print("\n--- [2] RESOURCES ---")
        resources = await client.list_resources()
        print(f"Found {len(resources)} resources.")
        for r in resources:
            print(f"  - {r.uri}")
            # Try to read one
            # content = await client.read_resource(r.uri)
            # print(f"    Content: {content[:50]}...")

        print("\n--- [3] TOOLS ---")
        tools = await client.list_tools()
        print(f"Found {len(tools)} tools.")
        
        session_id = "e2e_test_session"
        
        # 1. INIT ANCHOR
        print("\nTesting init_anchor...")
        init_res = await client.call_tool("init_anchor", {"raw_input": "E2E Test Run"})
        print(f"Result: {str(init_res)[:100]}...")

        # 2. CHECK VITAL
        print("\nTesting check_vital...")
        vital_res = await client.call_tool("check_vital", {})
        print(f"Result: {str(vital_res)[:100]}...")

        # 3. AUDIT RULES
        print("\nTesting audit_rules...")
        audit_res = await client.call_tool("audit_rules", {})
        print(f"Result: {str(audit_res)[:100]}...")

        # 4. SEARCH REALITY
        print("\nTesting search_reality...")
        search_res = await client.call_tool("search_reality", {"query": "arifOS Constitution"})
        print(f"Result: {str(search_res)[:100]}...")

        # 5. INGEST EVIDENCE
        print("\nTesting ingest_evidence...")
        ingest_res = await client.call_tool("ingest_evidence", {"url": "https://example.com"})
        print(f"Result: {str(ingest_res)[:100]}...")

        # 6. SACRED CHAIN (REASON -> FORGE -> JUDGE)
        # agi_reason
        print("\nTesting agi_reason...")
        reason_res = await client.call_tool("agi_reason", {"query": "Test logic", "session_id": session_id})
        print(f"Result: {str(reason_res)[:100]}...")

        # forge
        print("\nTesting forge...")
        forge_res = await client.call_tool("forge", {"spec": "Test materials", "session_id": session_id})
        print(f"Result: {str(forge_res)[:100]}...")

        # apex_judge
        print("\nTesting apex_judge...")
        judge_res = await client.call_tool("apex_judge", {"candidate_output": "forge_output", "session_id": session_id})
        print(f"Result: {str(judge_res)[:100]}...")

        # 7. AGENTZERO TOOLS
        print("\nTesting agentzero_validate...")
        az_val_res = await client.call_tool("agentzero_validate", {"input_to_validate": "test", "session_id": session_id})
        print(f"Result: {str(az_val_res)[:100]}...")

        # 8. INTERNAL/PHASE2 TOOLS (if exposed)
        print("\nTesting trace_replay...")
        try:
            trace_res = await client.call_tool("trace_replay", {"session_id": session_id})
            print(f"Result: {str(trace_res)[:100]}...")
        except Exception as e:
            print(f"trace_replay failed (expected if hidden/restricted): {e}")

        print("\n--- [4] RESOURCE READING ---")
        # Read a canon resource
        print("Reading canon://floors...")
        floors_data = await client.read_resource("canon://floors")
        print(f"Result: {str(floors_data)[:100]}...")


    print("\n✅ E2E Test Completed.")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
