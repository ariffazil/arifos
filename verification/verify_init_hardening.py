import asyncio
import json
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.getcwd())

from aaa_mcp.server import init_gate


async def verify_init_hardening():
    print("🔨 Verifying init_gate hardening (Option 3: Progressive Disclosure)...")

    # Run init_gate
    # Access .fn to bypass FastMCP wrapper (which makes it a FunctionTool object)
    result = await init_gate.fn(
        query="Verify constitutional governance metrics",
        mode="conscience",
        debug=True,
        # Required args for hardened init_gate
        intent_hint="test",
        urgency="low",
        user_context={},
    )

    # Extract structural content
    structured = result.get("structuredContent", {})
    data = structured.get("data", {})
    constitutional = structured.get("_constitutional", {})

    # 1. Verify Governance Object
    gov = data.get("governance")
    if not gov:
        print("❌ FAIL: 'governance' object missing from data.")
        return False

    print("✅ Governance object found.")

    # 2. Verify Metrics
    if gov.get("total_floors") != 13:
        print(f"❌ FAIL: total_floors is {gov.get('total_floors')}, expected 13")
        return False

    checked = gov.get("floors_checked_count")
    pending = gov.get("floors_pending_count")
    summary = gov.get("summary")

    print(f"   - Total Floors: {gov.get('total_floors')}")
    print(f"   - Checked: {checked}")
    print(f"   - Pending: {pending}")
    print(f"   - Summary: {summary}")

    if not isinstance(summary, str) or "11 floors pending" not in summary:
        print(f"⚠️ WARNING: Summary text might not match expectations: '{summary}'")

    # 3. Verify Pipeline Object
    pipe = data.get("pipeline")
    if not pipe:
        print("❌ FAIL: 'pipeline' object missing from data.")
        return False

    print("✅ Pipeline object found.")
    print(f"   - Stage: {pipe.get('stage')}")
    print(f"   - Next: {pipe.get('next_stage')}")

    if pipe.get("stage") != "000_INIT":
        print(f"❌ FAIL: Stage mismatch: {pipe.get('stage')}")
        return False

    # 4. Verify Decorator Alias (floors_enforced)
    enforced = constitutional.get("floors_enforced")
    if not enforced:
        print("❌ FAIL: 'floors_enforced' missing from _constitutional.")
        return False

    print(f"✅ Alias 'floors_enforced' found: {enforced}")

    print("\nSample Output:")
    print(json.dumps(data, indent=2))

    return True


if __name__ == "__main__":
    success = asyncio.run(verify_init_hardening())
    sys.exit(0 if success else 1)
    sys.exit(0 if success else 1)
