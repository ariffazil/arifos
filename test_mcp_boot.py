"""Quick test: can the MCP server boot without crashing?"""
import sys, os, traceback

os.environ["PYTHONPATH"] = "C:/Users/User/arifOS"
os.environ["PYTHONIOENCODING"] = "utf-8"

try:
    print("Step 1: Importing ToolRegistry...")
    from codebase.mcp.core.tool_registry import ToolRegistry
    print("  OK")

    print("Step 2: Creating ToolRegistry (registers 7 tools)...")
    registry = ToolRegistry()
    print(f"  OK - {len(registry.list_tools())} tools registered")

    print("Step 3: Importing StdioTransport...")
    from codebase.mcp.transports.stdio import StdioTransport
    print("  OK")

    print("Step 4: Creating StdioTransport...")
    transport = StdioTransport(registry)
    print("  OK")

    print("Step 5: Importing BaseTransport to check resource/prompt registries...")
    print(f"  Resources: {len(transport.resource_registry.list_resources())}")
    print(f"  Prompts: {len(transport.prompt_registry.list_prompts())}")

    print("\nStep 6: Checking mcp.server.stdio.stdio_server...")
    from mcp.server.stdio import stdio_server
    print("  OK")

    print("\n=== ALL IMPORTS AND INIT PASSED ===")
    print("The server CAN boot. Issue is likely in MCP protocol handshake.")

except Exception as e:
    print(f"\n!!! CRASH at above step !!!")
    traceback.print_exc()
    sys.exit(1)
