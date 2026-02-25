"""Transport wrapper for kernel constitutional decorator logic."""

from __future__ import annotations

from core.kernel.constitutional_decorator import FLOOR_ENFORCEMENT, get_tool_floors
from core.kernel.constitutional_decorator import (
    constitutional_floor as _kernel_constitutional_floor,
)


def constitutional_floor(*floors: str):
    # Lazy import avoids circulars and keeps transport deps in adapter layer.
    from aaa_mcp.presentation.formatter import format_tool_output, resolve_output_mode
    from aaa_mcp.protocol.tool_registry import build_hard_floor_block

    return _kernel_constitutional_floor(
        *floors,
        format_tool_output_fn=format_tool_output,
        resolve_output_mode_fn=resolve_output_mode,
        build_hard_floor_block_fn=build_hard_floor_block,
    )


__all__ = ["constitutional_floor", "get_tool_floors", "FLOOR_ENFORCEMENT"]
