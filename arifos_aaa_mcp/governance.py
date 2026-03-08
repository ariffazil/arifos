"""Compatibility shim — re-exports from core.governance."""
from core.governance import *  # noqa: F401, F403
from core.governance import (  # noqa: F401
    LAW_13_CATALOG, TOOL_DIALS_MAP, TOOL_LAW_BINDINGS, TOOL_STAGE_MAP,
    TRINITY_BY_TOOL, wrap_tool_output,
)
