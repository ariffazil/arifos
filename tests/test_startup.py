#!/usr/bin/env python3
"""
Startup verification for arifOS MCP server.
Tests critical imports and initialization before deployment.
"""

import sys
import os

print("=" * 60)
print("arifOS MCP Server Startup Verification")
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
    from mcp_server.core.tool_registry import ToolRegistry
    from mcp_server.transports.sse import SSETransport
    print("  ✓ Core imports OK")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Test 3: Tool registry
print("\n[3/4] Testing tool registry...")
try:
    registry = ToolRegistry()
    tool_count = len(registry.list_tools())
    print(f"  ✓ Tool registry OK: {tool_count} tools registered")
except Exception as e:
    print(f"  ✗ Registry failed: {e}")
    sys.exit(1)

# Test 4: Transport initialization
print("\n[4/4] Testing transport initialization...")
try:
    transport = SSETransport(registry)
    print(f"  ✓ Transport OK: {transport.name}")
except Exception as e:
    print(f"  ✗ Transport failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL STARTUP CHECKS PASSED")
print(f"✓ Ready to serve on port {port}")
print("=" * 60)
