import sys
import asyncio
from pathlib import Path

# Add the WELL directory to sys.path so we can import the mcp object
well_dir = Path(__file__).parent
sys.path.append(str(well_dir))

from server import mcp

async def test_well_tools():
    print("🧪 Testing WELL MCP Server tools...")
    
    # 1. Test well_state
    print("\n--- Testing well_state ---")
    state = await mcp.call_tool("well_state")
    print(f"Result: {state}")
    
    # 2. Test well_check_floors
    print("\n--- Testing well_check_floors ---")
    floors = await mcp.call_tool("well_check_floors")
    print(f"Result: {floors}")
    
    # 3. Test well_readiness
    print("\n--- Testing well_readiness ---")
    readiness = await mcp.call_tool("well_readiness")
    print(f"Result: {readiness}")
    
    # 4. Test well_log (dry run - just log a note)
    print("\n--- Testing well_log ---")
    log_result = await mcp.call_tool("well_log", arguments={"note": "Automated test run"})
    print(f"Result: {log_result}")
    
    # 5. Test well_anchor
    print("\n--- Testing well_anchor ---")
    # Using force=True to ensure it writes even if score delta is small
    anchor_result = await mcp.call_tool("well_anchor", arguments={"force": True})
    print(f"Result: {anchor_result}")

if __name__ == "__main__":
    try:
        asyncio.run(test_well_tools())
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
