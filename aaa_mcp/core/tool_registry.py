"""
Tool Registry for MCP Server
"""

from typing import Any, Callable, Dict, List


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self._tools[name] = func

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def get_tool(self, name: str) -> Callable:
        return self._tools.get(name)
