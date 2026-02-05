"""Mode selector for MCP server."""
from enum import Enum

class MCPMode(Enum):
    STDIO = "stdio"
    SSE = "sse"
    HTTP = "http"

def get_mcp_mode():
    # Return default mode
    return MCPMode.STDIO