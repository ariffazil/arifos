#!/usr/bin/env python3
"""
Test script to verify HTTP MCP endpoint functionality
"""

import asyncio
import json
from aiohttp import ClientSession

async def test_http_mcp():
    """Test the HTTP MCP endpoint with proper JSON-RPC format"""
    
    base_url = "https://aaamcp.arif-fazil.com"
    
    # Test 1: Check basic connectivity
    print("Testing basic connectivity...")
    try:
        async with ClientSession() as session:
            async with session.get(f"{base_url}/health") as resp:
                health_data = await resp.json()
                print(f"✓ Health check: {health_data}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # Test 2: Try MCP endpoint with various formats
    test_payloads = [
        # Standard MCP format
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "init_gate",
            "params": {"query": "Test query", "session_id": "test-session"}
        },
        # Alternative format with tools/call
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "init_gate",
                "arguments": {"query": "Test query", "session_id": "test-session"}
            }
        },
        # Simple format
        {
            "method": "init_gate",
            "params": {"query": "Test query", "session_id": "test-session"},
            "id": 3
        }
    ]
    
    headers = {"Content-Type": "application/json"}
    
    print("\nTesting MCP endpoint with different payload formats...")
    for i, payload in enumerate(test_payloads, 1):
        try:
            print(f"\nTrying format {i}: {json.dumps(payload)[:100]}...")
            async with ClientSession() as session:
                async with session.post(f"{base_url}/mcp", json=payload, headers=headers) as resp:
                    result = await resp.json() if resp.content_type == 'application/json' else await resp.text()
                    print(f"✓ Format {i} response: {result}")
        except Exception as e:
            print(f"✗ Format {i} failed: {e}")
    
    # Test 3: Try direct tool endpoint (if available)
    print("\nTesting direct tool endpoint...")
    try:
        payload = {"query": "Direct test", "session_id": "direct-test"}
        async with ClientSession() as session:
            async with session.post(f"{base_url}/init_gate", json=payload, headers=headers) as resp:
                result = await resp.json() if resp.content_type == 'application/json' else await resp.text()
                print(f"✓ Direct endpoint response: {result}")
    except Exception as e:
        print(f"✗ Direct endpoint failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_http_mcp())