
from arifos_aaa_mcp.server import mcp
import inspect

print(f"Type of mcp: {type(mcp)}")
print(f"Has 'tool' attribute: {hasattr(mcp, 'tool')}")

# Check mcp.tool signature
try:
    sig = inspect.signature(mcp.tool)
    print(f"mcp.tool signature: {sig}")
except Exception as e:
    print(f"Error checking mcp.tool signature: {e}")

# Check if it has a 'server' attribute (some people mistake it for mcp.server)
print(f"Has 'server' attribute: {hasattr(mcp, 'server')}")

# Check if it has an '_app' or similar
print(f"Has '_mcp_server' attribute: {hasattr(mcp, '_mcp_server')}")

if hasattr(mcp, '_mcp_server'):
    print(f"Type of mcp._mcp_server: {type(mcp._mcp_server)}")
    print(f"Has 'tool' attribute on _mcp_server: {hasattr(mcp._mcp_server, 'tool')}")
