"""
SSE Transport for MCP Server
"""

from typing import Any


class SSETransport:
    def __init__(self, registry: Any):
        self.registry = registry
        self.name = "sse"
