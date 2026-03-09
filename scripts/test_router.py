import asyncio
import json
import os
import sys

# Ensure the root directory is in sys.path
sys.path.append(os.getcwd())

os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"

try:
    from arifosmcp.transport.server import arifos_kernel as arifos_kernel_tool
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    sys.exit(1)


async def main():
    print("🔥 arifOS Kernel (Metabolic Loop) Test")
    print("======================================")

    # The Kernel is the ultimate external tool. It orchestrates the full 000-999 flow.
    print("\n[Calling arifOS.kernel]")
    try:
        res = await arifos_kernel_tool(
            query="Who are you and what are your 13 floors?",
            actor_id="arif",
            risk_tier="low",
            debug=True,
        )
        # The result might be a Pydantic model or dict.
        if hasattr(res, "model_dump"):
            data = res.model_dump()
        else:
            data = res

        print(f"Status: {data.get('status')}")
        print(f"Verdict: {data.get('verdict')}")
        print(f"Session Id: {data.get('session_id')}")

        # Check for Apex Output (The internal deltas)
        apex = data.get("apex_output") or data.get("data", {}).get("apex_output")
        if apex:
            print("\n[Internal Deltas Captured]")
            print(json.dumps(apex.get("governed_intelligence", {}), indent=2))
            print(json.dumps(apex.get("entropy_layer", {}), indent=2))

        # Check for the CONTRAST score (as the user requested)
        print("\n[Longitudinal Contrast Check]")
        if "contrast" in str(data).lower() or "drift" in str(data).lower():
            print("Found contrast/drift signals!")
        else:
            print("No conversational contrast/drift metrics found in router output.")

    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
