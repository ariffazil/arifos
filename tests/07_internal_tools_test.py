import asyncio
import os
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parents[1]))

# Set Profile to full to expose internal tools
os.environ["ARIFOS_PUBLIC_TOOL_PROFILE"] = "full"
os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
os.environ["AAA_MCP_OUTPUT_MODE"] = "debug"

from fastmcp import Client
from arifosmcp.runtime.server import create_aaa_mcp_server

async def test_internal_tools():
    print("🚀 Starting arifOS INTERNAL Tools Test...")
    server = create_aaa_mcp_server()
    
    internal_tools = [
        ("chroma_query", {"query": "test"}),
        ("config_flags", {}),
        ("cost_estimator", {"input_nodes": 10}),
        ("forge_guard", {"markdown": "# Test"}),
        ("fs_inspect", {"path": "."}),
        ("list_resources", {}),
        ("log_tail", {"lines": 5}),
        ("metabolic_loop", {"raw_input": "Internal Test", "session_id": "test_internal"}),
        ("metabolic_loop_router", {"payload": {"test": True}}),
        ("net_status", {}),
        ("process_list", {}),
        ("read_resource", {"uri": "canon://index"}),
        ("register_tools", {}),
        ("stage_pipeline_app", {"stage": "init"}),
        ("system_health", {}),
        ("trace_replay", {"session_id": "test_internal"}),
    ]

    async with Client(server) as client:
        # First, Anchor session to get auth context
        print("\nAnchoring session...")
        anchor_res = await client.call_tool("init_anchor", {"raw_input": "Internal Tools Test", "session_id": "test_internal"})
        auth_ctx = None
        try:
            res_json = json.loads(anchor_res.content[0].text)
            auth_ctx = res_json.get("auth_context")
            print(f"Auth Context ready: {auth_ctx.get('nonce')}")
        except:
            print("Failed to get auth context, proceeding with default")

        for tool_name, args in internal_tools:
            print(f"\nTesting {tool_name}...")
            # Inject auth_context and session_id if not present
            if "session_id" not in args and tool_name not in ["list_resources", "register_tools", "system_health", "check_vital"]:
                 args["session_id"] = "test_internal"
            if "auth_context" not in args and auth_ctx:
                 args["auth_context"] = auth_ctx

            try:
                res = await client.call_tool(tool_name, args)
                print(f"✅ {tool_name} Success: {str(res)[:150]}...")
            except Exception as e:
                print(f"❌ {tool_name} Failed: {e}")

    print("\n✅ Internal Tools Test Completed.")

if __name__ == "__main__":
    asyncio.run(test_internal_tools())
