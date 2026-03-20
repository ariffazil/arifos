
import asyncio
import json
from arifosmcp.runtime.bridge import call_kernel

async def test_mapping():
    payload = {"query": "Test query"}
    session_id = "test-session"
    result = await call_kernel("agi_reason", session_id, payload)
    print(f"Result for agi_reason: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_mapping())
