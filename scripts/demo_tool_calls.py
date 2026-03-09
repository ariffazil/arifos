import asyncio
import json
import os
import sys
import uuid

# Ensure the root directory is in sys.path
sys.path.append(os.getcwd())

# Mock environment variables if needed
os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"

try:
    from arifosmcp.transport.server import anchor_session, reason_mind
except ImportError as e:
    print(f"❌ Failed to import arifosmcp.transport.server: {e}")
    sys.exit(1)


async def main():
    print("🔥 arifOS MCP Tools Internal/External Test")
    print("==========================================")

    # 1. Anchor Session (000)
    # External: anchor_session
    # Internal: core.organs._0_init.anchor
    print("\n[External Call] anchor_session(query='Explain arifOS tools')")
    try:
        res1 = await anchor_session(query="Explain arifOS tools")
        print(f"  Status: {res1.get('status')}")
        print(f"  Session: {res1.get('session_id')}")
        print(f"  Verdict: {res1.get('verdict')}")

        session_id = res1.get("session_id")
        auth_context = res1.get("auth_context")

        if res1.get("status") == "ERROR":
            print(f"  ❌ Error: {res1.get('error')}")
            return

        # 2. Reason Mind (111-444)
        # External: reason_mind
        # Internal: core.organs._1_agi.reason, .think, .integrate, .respond
        print(
            f"\n[External Call] reason_mind(query='What are the 13 floors?', session_id='{session_id}')"
        )
        res2 = await reason_mind(
            query="What are the 13 floors?", session_id=session_id, auth_context=auth_context
        )
        print(f"  Status: {res2.get('status')}")
        print(f"  Verdict: {res2.get('verdict')}")
        print(f"  Stage: {res2.get('stage')}")

        if res2.get("status") == "ERROR":
            print(f"  ❌ Error: {res2.get('error') or 'Internal Fracture'}")
            # print(json.dumps(res2, indent=2))
        else:
            truth = res2.get("truth", {})
            print(f"  Truth Score: {truth.get('score')}")
            print(f"  Message: {res2.get('message', 'No message')[:100]}...")

    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback

        traceback.print_exc()

    print("\n✅ Demo complete.")


if __name__ == "__main__":
    asyncio.run(main())
