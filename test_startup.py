#!/usr/bin/env python3
"""
Simple startup test for arifOS MCP server.
Verifies the app can start without crashing.
"""

import sys
import os

# Test basic imports
try:
    print("Testing imports...")
    from mcp.core.tool_registry import ToolRegistry
    from mcp.transports.sse import SSETransport
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test tool registry initialization
try:
    print("Testing tool registry...")
    registry = ToolRegistry()
    tool_count = len(registry.list_tools())
    print(f"✓ Tool registry initialized: {tool_count} tools")
except Exception as e:
    print(f"✗ Tool registry failed: {e}")
    sys.exit(1)

# Test environment
port = os.getenv("PORT", "8080")
print(f"✓ PORT={port}")

print("\n✓ All startup checks passed!")
print(f"Ready to start SSE server on port {port}")
