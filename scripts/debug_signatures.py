import asyncio
import inspect
import json
import os
import sys

# Ensure the root directory is in sys.path
sys.path.append(os.getcwd())

os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"

try:
    from arifosmcp.transport.server import (
        _init_anchor_state,
        _init_session,
        anchor_session,
        reason_mind,
    )
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)


async def main():
    print("🔥 arifOS MCP Tools Signature Check")
    print("==================================")

    print(f"_init_session signature: {inspect.signature(_init_session)}")
    print(f"_init_anchor_state signature: {inspect.signature(_init_anchor_state)}")

    print("\n[Step 1] Calling anchor_session")
    try:
        # Try calling with minimal arguments
        res1 = await anchor_session(query="Explain arifOS tools", actor_id="arif")
        print(f"  Status: {res1.get('status')}")
        print(f"  Session: {res1.get('session_id')}")

        session_id = res1.get("session_id")
        auth_context = res1.get("auth_context")

        if res1.get("status") == "SUCCESS":
            print(f"\n[Step 2] Calling reason_mind")
            res2 = await reason_mind(
                query="What are the 13 floors?", session_id=session_id, auth_context=auth_context
            )
            print(f"  Status: {res2.get('status')}")
            print(f"  Verdict: {res2.get('verdict')}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
