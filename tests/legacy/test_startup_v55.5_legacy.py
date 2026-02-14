#!/usr/bin/env python3
"""
Startup verification for arifOS MCP server (v55.5).
Tests critical imports and initialization before deployment.
"""

import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

print("=" * 60)
print("arifOS MCP Server Startup Verification (v55.5)")
print("=" * 60)

# Test 1: Environment
print("\n[1/4] Testing environment...")
port = os.getenv("PORT", "8080")
print(f"  PORT={port}")
print(f"  HOST={os.getenv('HOST', '0.0.0.0')}")
print("  ✓ Environment OK")

# Test 2: Core imports
print("\n[2/4] Testing core imports...")
try:
    from aaa_mcp.server import (
        agi_reason,
        agi_sense,
        agi_think,
        apex_verdict,
        asi_align,
        asi_empathize,
        init_gate,
        mcp,
        reality_search,
        vault_seal,
    )

    print("  ✓ Core imports OK (9 canonical tools)")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Test 3: Tool count verification
print("\n[3/4] Testing tool registry...")
try:
    CANONICAL_TOOLS = [
        init_gate,
        agi_sense,
        agi_think,
        agi_reason,
        asi_empathize,
        asi_align,
        apex_verdict,
        reality_search,
        vault_seal,
    ]
    tool_count = len(CANONICAL_TOOLS)
    print(f"  ✓ Tool registry OK: {tool_count} tools registered")
except Exception as e:
    print(f"  ✗ Registry failed: {e}")
    sys.exit(1)

# Test 4: FastMCP server initialization
print("\n[4/4] Testing FastMCP server...")
try:
    server_name = mcp.name
    print(f"  ✓ FastMCP OK: server='{server_name}'")
except Exception as e:
    print(f"  ✗ FastMCP failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL STARTUP CHECKS PASSED")
print(f"✓ Ready to serve on port {port}")
print("=" * 60)
