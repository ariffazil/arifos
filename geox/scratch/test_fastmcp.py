
from fastmcp import FastMCP
mcp = FastMCP("test")
@mcp.tool()
def hello(): return "world"

print("Tools:", [t.name for t in mcp._tool_manager.list_tools()])
