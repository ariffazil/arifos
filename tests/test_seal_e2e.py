import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_seal_e2e():
    print("=== Testing vault_seal E2E ===")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "arifosmcp.runtime", "stdio"],
        env={
            **os.environ,
            "ARIFOS_PHYSICS_DISABLED": "1",
            "AAA_MCP_OUTPUT_MODE": "debug",
            "ARIFOS_DEV_MODE": "1"
        }
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. First we need a session
            print("Calling init_anchor...")
            res_init = await session.call_tool("init_anchor", {"raw_input": "Testing seal"})
            init_envelope = json.loads(res_init.content[0].text)
            session_id = init_envelope.get("session_id")
            auth_ctx = init_envelope.get("auth_context")
            print(f"  Session created: {session_id}")
            
            # 2. Call vault_seal
            print("Calling vault_seal...")
            res_seal = await session.call_tool("vault_seal", {
                "verdict": "SEAL",
                "evidence": "E2E Test Evidence for VPS Deployment Readiness",
                "session_id": session_id,
                "auth_context": auth_ctx
            })
            
            raw_text = res_seal.content[0].text
            print(f"Raw seal response: {raw_text}")
            seal_envelope = json.loads(raw_text)
            print(f"  Seal response: {json.dumps(seal_envelope, indent=2)}")
            
            if seal_envelope.get("ok"):
                print("\nSUCCESS: vault_seal functional.")
            else:
                print("\nFAILED: vault_seal returned error.")
                sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_seal_e2e())
