from __future__ import annotations

from importlib import import_module
from typing import Any


def get_tool_adapter(name: str) -> Any:
    module = import_module("aaa_mcp.server")
    tool = getattr(module, name)
    return getattr(tool, "fn", tool)
