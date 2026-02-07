#!/usr/bin/env python3
"""Call arifOS MCP tools via SSE transport."""
import asyncio
import json
import sys
from datetime import datetime
import secrets

async def call_arifos_tools():
    from mcp.client.session import ClientSession
    from mcp.client.sse import sse_client
    
    session_id = f"arifos_{datetime.now().strftime('%Y%m%d')}_{secrets.token_hex(4)}"
    print(f"Session ID: {session_id}")
    
    async with sse_client("https://aaamcp.arif-fazil.com/sse") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"\nAvailable tools: {[t.name for t in tools.tools]}")
            
            # Call init_gate
            print(f"\n=== Calling init_gate ===")
            init_result = await session.call_tool("init_gate", {
                "session_id": session_id,
                "environment": "prod"
            })
            print(f"init_gate result: {json.dumps(init_result.model_dump(), indent=2, default=str)}")
            
            # Determine verdict from init_gate result
            init_content = init_result.content[0].text if init_result.content else "{}"
            init_data = json.loads(init_content) if isinstance(init_content, str) else init_content
            
            # Determine verdict_type based on floor checks
            floors_passed = init_data.get("floors_passed", True)
            if floors_passed:
                verdict_type = "SEAL"
            else:
                verdict_type = "PARTIAL"
            
            # Call vault_seal
            print(f"\n=== Calling vault_seal ===")
            seal_result = await session.call_tool("vault_seal", {
                "session_id": session_id,
                "category": "session_init",
                "verdict_type": verdict_type
            })
            print(f"vault_seal result: {json.dumps(seal_result.model_dump(), indent=2, default=str)}")
            
            # Extract final data for 000_INIT_ACK
            seal_content = seal_result.content[0].text if seal_result.content else "{}"
            seal_data = json.loads(seal_content) if isinstance(seal_content, str) else seal_content
            
            ack = {
                "000_INIT_ACK": {
                    "session_id": session_id,
                    "verdict_type": verdict_type,
                    "risk_level": init_data.get("risk_level", "LOW"),
                    "environment": "prod",
                    "vault999_header": {
                        "entry_id": seal_data.get("entry_id", seal_data.get("seal_id")),
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "merkle_root": seal_data.get("merkle_root", seal_data.get("chain", {}).get("merkle_root")),
                        "status": "ACTIVE" if verdict_type == "SEAL" else "PENDING"
                    }
                }
            }
            print(f"\n{'='*50}")
            print(f"000_INIT_ACK:")
            print(json.dumps(ack, indent=2))
            return ack

if __name__ == "__main__":
    try:
        result = asyncio.run(call_arifos_tools())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
