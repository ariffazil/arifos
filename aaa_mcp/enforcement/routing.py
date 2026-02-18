"""Compatibility shim for enforcement routing.

Kernel routing logic lives in `core.enforcement.routing`.
This module keeps existing `aaa_mcp.enforcement` import paths stable.
"""

from core.enforcement.routing import route_refuse

__all__ = ["route_refuse"]
