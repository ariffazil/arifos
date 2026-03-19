"""Test full ASI flow to find the bug."""

import sys

sys.path.insert(0, ".")

import asyncio


async def test_flow():
    from aaa_mcp.core.engine_adapters import ASIEngine

    engine = ASIEngine()

    print("Testing _core_agi_tensor...")
    try:
        tensor = await engine._core_agi_tensor("test query", "test-session")
        print(f"Got tensor: {type(tensor)}")
        print(f"Has metrics: {hasattr(tensor, 'metrics')}")
    except Exception as e:
        print(f"Error in _core_agi_tensor: {e}")
        import traceback

        traceback.print_exc()
        return

    print("\nTesting empathize...")
    try:
        result = await engine.empathize("test query", "test-session")
        print(f"Got result: {type(result)}")
        print(f"Result keys: {result.keys() if hasattr(result, 'keys') else 'N/A'}")
    except Exception as e:
        print(f"Error in empathize: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_flow())
