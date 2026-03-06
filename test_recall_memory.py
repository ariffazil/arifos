#!/usr/bin/env python3
"""
Test recall_memory via MCP stdio protocol
Usage: python test_recall_memory.py
"""

import json
import subprocess
import sys


def send_request(process, request):
    """Send JSON-RPC request to MCP server."""
    req_json = json.dumps(request)
    process.stdin.write(req_json + "\n")
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    return json.loads(response_line)


def main():
    print("=" * 60)
    print("TESTING recall_memory MCP TOOL")
    print("=" * 60)
    
    # Start MCP server
    process = subprocess.Popen(
        ["python3", "-m", "arifos_aaa_mcp", "stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/srv/arifOS"
    )
    
    try:
        # 1. List tools
        print("\n[1] Listing MCP tools...")
        response = send_request(process, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        
        tools = [t["name"] for t in response.get("result", {}).get("tools", [])]
        print(f"   Found {len(tools)} tools")
        
        if "recall_memory" in tools:
            print("   ✅ recall_memory is available")
        else:
            print("   ❌ recall_memory NOT found")
            return
        
        # 2. Anchor session
        print("\n[2] Creating session...")
        response = send_request(process, {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "anchor_session",
                "arguments": {}
            }
        })
        
        result = response.get("result", {})
        content = result.get("content", [{}])[0]
        
        # Extract session_id from response
        import re
        text = content.get("text", "")
        match = re.search(r'"session_id": "([^"]+)"', text)
        
        if match:
            session_id = match.group(1)
            print(f"   ✅ Session created: {session_id[:20]}...")
        else:
            print("   ❌ Could not extract session_id")
            print(f"   Response: {text[:200]}")
            return
        
        # 3. Test recall_memory
        print("\n[3] Testing recall_memory...")
        print(f"   Query: 'What does Floor F2 enforce?'")
        
        response = send_request(process, {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "recall_memory",
                "arguments": {
                    "session_id": session_id,
                    "current_thought_vector": "What does Floor F2 enforce?"
                }
            }
        })
        
        result = response.get("result", {})
        content = result.get("content", [{}])[0]
        text = content.get("text", "")
        
        print("\n[4] Response:")
        print("-" * 60)
        
        # Parse and display
        try:
            # Extract JSON from text (it's wrapped in markdown or plain)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                status = data.get("status", "UNKNOWN")
                memories = data.get("memories", [])
                metrics = data.get("metrics", {})
                
                print(f"   Status: {status}")
                print(f"   Memories found: {metrics.get('memory_count', 0)}")
                print(f"   BGE Available: {metrics.get('bge_available', False)}")
                print(f"   Jaccard Max: {metrics.get('jaccard_max', 0)}")
                
                print("\n   Top Results:")
                for i, mem in enumerate(memories[:3], 1):
                    print(f"   {i}. {mem.get('source')} (score: {mem.get('score')})")
                    content = mem.get('content', '')[:100]
                    print(f"      {content}...")
                
                if memories:
                    print("\n   ✅ EMBEDDING SYSTEM IS WORKING!")
                else:
                    print("\n   ⚠️  No memories returned (check Qdrant)")
            else:
                print(f"   Raw response: {text[:500]}")
        
        except Exception as e:
            print(f"   Error parsing: {e}")
            print(f"   Raw: {text[:500]}")
    
    finally:
        process.terminate()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
