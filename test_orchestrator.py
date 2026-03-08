import asyncio
import json
import os
import sys

# Ensure the root directory is in the path
sys.path.insert(0, os.getcwd())

from arifosmcp.runtime.orchestrator import metabolic_loop


async def main():
    print("🚀 Starting arifOS Metabolic Loop Test (Stage 444)...")

    query = "What are the 13 constitutional floors and how do they reduce entropy?"
    actor_id = "arif-fazil"

    try:
        # We invoke the metabolic loop directly to simulate the MCP tool execution
        result = await metabolic_loop(query=query, actor_id=actor_id)

        print("\n✅ Test Completed Successfully.")
        print("-" * 40)
        print(f"Session ID: {result.get('session_id')}")
        print(f"Final Verdict: {result.get('verdict')}")
        if result.get("verdict") != "SEAL":
            print(f"Error: {result.get('data', {}).get('error_message')}")
            print(f"Details: {result.get('data')}")
        print("-" * 40)

        print("\n🔍 Trace Analysis:")
        trace = result.get("trace", {})
        for stage, verdict in trace.items():
            print(f"  [{stage}]: {verdict}")

        print("\n📊 Telemetry Summary:")
        telemetry = result.get("telemetry", {})
        print(f"  dS: {telemetry.get('dS')}")
        print(f"  Peace²: {telemetry.get('peace2')}")
        print(f"  Confidence: {telemetry.get('confidence')}")

    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(main())
