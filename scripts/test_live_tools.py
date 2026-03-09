import asyncio
import json
import os
import sys

# Ensure the root directory is in sys.path
sys.path.append(os.getcwd())

os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
os.environ["ARIFOS_CONTINUITY_STRICT"] = "false"

try:
    from arifosmcp.transport.server import anchor_session, reason_mind
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)


async def main():
    print("🔥 arifOS MCP Tools Live Test")
    print("============================")

    # Let's perform a metabolic loop if possible, or sequential calls
    # Step 1: Anchor
    print("\n[Stage 000] anchor_session")
    res1 = await anchor_session(query="I am arif. Show me the tools.")

    # FastMCP might wrap the response, let's look at it
    print(f"Response Type: {type(res1)}")

    # If it's a ToolResult (FastMCP), we need to handle it.
    # But usually in arifOS server.py, they return dicts or Pydantic models.

    data = res1
    if hasattr(res1, "content"):  # FastMCP ToolResult
        print("Detected FastMCP ToolResult")
        try:
            data = json.loads(res1.content[0].text)
        except:
            data = res1

    print(f"Status: {data.get('status')}")
    print(f"Session: {data.get('session_id')}")
    print(f"Verdict: {data.get('verdict')}")

    session_id = data.get("session_id")
    auth_context = data.get("auth_context")

    if session_id and session_id != "unknown":
        print("\n[Stage 111-444] reason_mind")
        res2 = await reason_mind(
            query="Tell me about F2 Truth.", session_id=session_id, auth_context=auth_context
        )
        data2 = res2
        if hasattr(res2, "content"):
            data2 = json.loads(res2.content[0].text)

        print(f"Status: {data2.get('status')}")
        print(f"Verdict: {data2.get('verdict')}")

        # Check for delta signals the user mentioned
        apex = data2.get("apex_output", {})
        if apex:
            print("\n[Delta Signals Detected]")
            print(f"G_dagger: {apex.get('governed_intelligence', {}).get('governed_score')}")
            print(f"delta_S: {apex.get('entropy_layer', {}).get('delta_S')}")
        else:
            print("\nNo apex_output found in reason_mind response.")
            # Let's see the keys
            print(f"Response Keys: {list(data2.keys())}")

    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
