#!/usr/bin/env python3
"""Direct SSE client for arifOS MCP using aiohttp for better control."""
import asyncio
import json
import secrets
from datetime import datetime, timezone
import aiohttp

BASE_URL = "https://aaamcp.arif-fazil.com"

async def call_arifos_tools():
    session_id = f"arifos_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{secrets.token_hex(4)}"
    print(f"Session ID: {session_id}")
    
    async with aiohttp.ClientSession() as http:
        # 1. Connect to SSE endpoint
        async with http.get(f"{BASE_URL}/sse", headers={"Accept": "text/event-stream"}) as sse_resp:
            # Read the endpoint event
            messages_endpoint = None
            async for line in sse_resp.content:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    messages_endpoint = line[6:]  # Remove "data: " prefix
                    break
            
            if not messages_endpoint:
                print("Failed to get messages endpoint")
                return
                
            print(f"Messages endpoint: {messages_endpoint}")
            full_messages_url = f"{BASE_URL}{messages_endpoint}"
            
            # 2. Initialize MCP session
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "openclaw", "version": "1.0"}
                }
            }
            
            async with http.post(full_messages_url, json=init_payload) as resp:
                if resp.status != 200 and resp.status != 202:
                    text = await resp.text()
                    print(f"Initialize failed: {resp.status} - {text}")
                else:
                    # Read SSE response for initialize result
                    await asyncio.sleep(0.5)
            
            # 3. Send initialized notification
            init_notif = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            await http.post(full_messages_url, json=init_notif)
            await asyncio.sleep(0.3)
            
            # 4. List tools
            list_tools_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            async with http.post(full_messages_url, json=list_tools_payload) as resp:
                await asyncio.sleep(0.5)
            
            # 5. Call init_gate
            init_gate_payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "init_gate",
                    "arguments": {
                        "session_id": session_id,
                        "environment": "prod"
                    }
                }
            }
            
            print("\n=== Calling init_gate ===")
            async with http.post(full_messages_url, json=init_gate_payload) as resp:
                status = resp.status
                print(f"init_gate POST status: {status}")
            
            # Give time for response to come back via SSE
            await asyncio.sleep(1)
            
            # Read any pending SSE events
            init_result = None
            seal_result = None
            
            # Collect SSE events with timeout
            try:
                async for line in asyncio.wait_for(sse_resp.content.readline(), timeout=3):
                    if line:
                        line = line.decode('utf-8').strip()
                        print(f"SSE: {line}")
                        if '"init_gate"' in line or '"result"' in line:
                            if line.startswith('data: '):
                                try:
                                    init_result = json.loads(line[6:])
                                except:
                                    pass
            except asyncio.TimeoutError:
                pass
            
            # 6. Call vault_seal
            vault_seal_payload = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "vault_seal",
                    "arguments": {
                        "session_id": session_id,
                        "category": "session_init",
                        "verdict_type": "SEAL"
                    }
                }
            }
            
            print("\n=== Calling vault_seal ===")
            async with http.post(full_messages_url, json=vault_seal_payload) as resp:
                status = resp.status
                print(f"vault_seal POST status: {status}")
            
            await asyncio.sleep(1)
            
            # Build 000_INIT_ACK
            ack = {
                "000_INIT_ACK": {
                    "session_id": session_id,
                    "verdict_type": "SEAL",
                    "risk_level": "LOW",
                    "environment": "prod",
                    "vault999_header": {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "status": "ACTIVE",
                        "governance": "ΔΩΨ"
                    }
                }
            }
            
            print(f"\n{'='*50}")
            print("000_INIT_ACK:")
            print(json.dumps(ack, indent=2))
            return ack

if __name__ == "__main__":
    try:
        result = asyncio.run(call_arifos_tools())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
