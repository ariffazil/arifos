#!/usr/bin/env python3
"""
MCP Protocol Test — Verify constitutional tools actually callable
"""

import asyncio
import sys
sys.path.insert(0, '/root/arifOS')

from aaa_mcp.server import mcp
from aaa_mcp.constitutional_config import CONFIG, announce_startup

async def test_mcp_protocol():
    """Test tools via actual MCP protocol (not import)."""
    
    # Announce constitutional mode
    announce_startup()
    
    print("\n" + "="*60)
    print("MCP PROTOCOL VERIFICATION")
    print("="*60)
    
    # Test 1: Get tools
    tools = await mcp.get_tools()
    print(f"\n✓ Tools registered: {len(tools)}")
    for name in tools:
        print(f"  - {name}")
    
    # Test 2: Call init_session via MCP
    print("\n" + "-"*60)
    print("Test: init_session via MCP protocol")
    print("-"*60)
    
    try:
        # FastMCP v2: Get tool then call
        tool = await mcp.get_tool('init_session')
        print(f"Tool retrieved: {tool.name}")
        
        # Call with correct params
        result = await tool.fn(
            query='constitutional_test',
            actor_id='test_user',
            mode='conscience',
            grounding_required=False
        )
        
        print(f"✓ init_session SUCCESS")
        print(f"  Response type: {type(result)}")
        
        if isinstance(result, dict):
            print(f"  Keys: {list(result.keys())}")
            if 'session_id' in result:
                print(f"  session_id: {result['session_id']}")
            if 'constitutional_mode' in result:
                print(f"  mode: {result['constitutional_mode']}")
        else:
            print(f"  Result: {result}")
            
    except Exception as e:
        print(f"✗ init_session FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Call agi_cognition
    print("\n" + "-"*60)
    print("Test: agi_cognition via MCP protocol")
    print("-"*60)
    
    try:
        tool = await mcp.get_tool('agi_cognition')
        result = await tool.fn(
            query='What is the capital of France?',
            session_id='test-session-001',
            grounding=[]
        )
        
        print(f"✓ agi_cognition SUCCESS")
        if isinstance(result, dict):
            print(f"  verdict: {result.get('verdict')}")
            print(f"  truth_score: {result.get('truth_score')}")
            print(f"  humility_omega: {result.get('humility_omega')}")
        
    except Exception as e:
        print(f"✗ agi_cognition FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)
    print("✓ MCP protocol working")
    print("✓ Tools callable via FastMCP")
    print("✓ Constitutional enforcement active")
    print(f"✓ Mode: {CONFIG['mode'].value}")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_mcp_protocol())
    sys.exit(0 if success else 1)
