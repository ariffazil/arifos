try:
    print("Importing aaa_mcp...")
    import aaa_mcp

    print("Importing aaa_mcp.asi_gateway...")
    import aaa_mcp.asi_gateway

    print("Importing aaa_mcp.tools.canonical_trinity...")
    import aaa_mcp.tools.canonical_trinity

    print("Importing aaa_mcp.bridge...")
    import aaa_mcp.bridge

    print("SUCCESS: All key modules imported.")
except Exception as e:
    print(f"FAILURE: {e}")
    import traceback

    traceback.print_exc()
