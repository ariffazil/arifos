"""
arifOS MCP Server — FastMCP Implementation
Root-level MCP package for v55.4
"""

from mcp.server import mcp
from mcp.constitutional_decorator import constitutional_floor
from mcp.engine_adapters import (
    InitEngine, AGIEngine, ASIEngine, APEXEngine
)

__version__ = "55.4.0"
__all__ = [
    "mcp",
    "constitutional_floor",
    "InitEngine",
    "AGIEngine", 
    "ASIEngine",
    "APEXEngine",
]

def main():
    """Entry point for CLI"""
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    print(f"Version: {__version__}")
    print("Starting SSE transport on port 6274...")
    mcp.run(transport="sse", port=6274)

if __name__ == "__main__":
    main()
