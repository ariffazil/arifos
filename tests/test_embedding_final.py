#!/usr/bin/env python3
"""Quick test of the embedding system - run with: python3 test_embedding_final.py"""

import json
import subprocess


def test():
    print("=" * 60)
    print("TESTING arifOS EMBEDDING SYSTEM")
    print("=" * 60)

    # Run test inside MCP container
    cmd = """docker exec arifosmcp_server python3 -c "
import sys
sys.path.insert(0, '/usr/src/app')
import asyncio
import json
from arifosmcp.runtime.server import vector_memory

async def test():
    result = await vector_memory(
        query='What does Floor F2 enforce?',
        session_id='test-session'
    )
    data = result.get('data', {}).get('payload', {})
    print(json.dumps({
        'status': data.get('status'),
        'memories': len(data.get('memories', [])),
        'top_result': data.get('memories', [{}])[0].get('source') if data.get('memories') else None
    }))

asyncio.run(test())
" 2>&1 | tail -1"""

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    try:
        data = json.loads(result.stdout.strip())

        print("\n✅ vector_memory responded")
        print(f"   Status: {data.get('status')}")
        print(f"   Memories: {data.get('memories')}")
        print(f"   Top result: {data.get('top_result')}")

        if data.get("memories", 0) > 0:
            print("\n" + "=" * 60)
            print("✅ EMBEDDING SYSTEM IS WORKING!")
            print("=" * 60)
            return True
        else:
            print("\n⚠️  No memories found")
            return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Raw output: {result.stdout}")
        return False


if __name__ == "__main__":
    success = test()
    exit(0 if success else 1)
