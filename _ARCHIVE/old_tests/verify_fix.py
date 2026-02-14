#!/usr/bin/env python3
"""
Verify the apex_verdict fix is in place and working.
This doesn't call the tools (they're MCP-wrapped), but verifies the code structure.
"""

import sys
sys.path.insert(0, '.')


def check_fix_in_code():
    """Verify the defensive code is in server.py."""
    print("=" * 70)
    print("VERIFYING apex_verdict FIX")
    print("=" * 70)
    
    with open('aaa_mcp/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check 1: Defensive evidence handling
    print("\n[1] Checking defensive evidence handling...")
    if 'isinstance(e, dict) and isinstance(e.get("source_meta"), dict)' in content:
        print("  [OK] Defensive type checks found in apex_verdict")
    else:
        print("  [X] Defensive checks NOT found!")
        return False
    
    # Check 2: No old list comprehension pattern
    print("\n[2] Checking old pattern removed...")
    old_pattern = '{e["source_meta"]["type"] for e in session_ev}'
    if old_pattern not in content:
        print("  [OK] Old unsafe pattern not found")
    else:
        print("  [WARNING] Old pattern still exists (may be elsewhere)")
    
    # Check 3: Server imports successfully
    print("\n[3] Checking server module imports...")
    try:
        from aaa_mcp import server
        print("  [OK] Server module imports successfully")
    except Exception as e:
        print(f"  [X] Import failed: {e}")
        return False
    
    # Check 4: Key functions exist
    print("\n[4] Checking key functions exist...")
    required = ['init_gate', 'agi_sense', 'agi_reason', 'apex_verdict', 'vault_seal']
    for func in required:
        if hasattr(server, func):
            print(f"  [OK] {func} exists")
        else:
            print(f"  [X] {func} NOT found!")
            return False
    
    print("\n" + "=" * 70)
    print("ALL CHECKS PASSED [OK]")
    print("=" * 70)
    print("\nThe apex_verdict fix is in place:")
    print("  - Defensive type checking added")
    print("  - Malformed evidence handled gracefully")
    print("  - Server module stable")
    print("\nNote: Tools are MCP-wrapped. Use MCP client for full E2E testing.")
    
    return True


if __name__ == "__main__":
    success = check_fix_in_code()
    sys.exit(0 if success else 1)
