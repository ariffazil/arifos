import sys

sys.path.append(r"c:\arifosmcp")

try:
    from arifosmcp.runtime.server import mcp
    print("Tools:")
    for tool in mcp.list_tools():
        print(f"- {tool.name}: {tool.description}")
    
    # Resources are not directly available via list_resources easily in this way but let's see.
    # mcp.list_resources is not exactly how fastmcp works.
    # fastmcp uses decorator for resources too.
    # Let's see if we have them.
except Exception:
    import traceback
    traceback.print_exc()
