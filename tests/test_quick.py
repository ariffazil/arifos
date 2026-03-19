"""Quick test with timeout."""

import sys

sys.path.insert(0, ".")

import asyncio


async def test_sense():
    from core.organs._1_agi import sense

    print("Calling sense...")
    result = await sense("test query", "test-session")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")


async def main():
    try:
        await asyncio.wait_for(test_sense(), timeout=10)
    except asyncio.TimeoutError:
        print("TIMEOUT!")


if __name__ == "__main__":
    asyncio.run(main())
