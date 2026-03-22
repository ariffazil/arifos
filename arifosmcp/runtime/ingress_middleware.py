"""
arifosmcp/runtime/ingress_middleware.py

Ingress tolerance middleware.
"Masuk longgar, dalam tetap governed."
Accept messy input at the boundary; governance enforces inside.
"""
from __future__ import annotations

import logging
from typing import Any

from fastmcp.server.middleware.middleware import Middleware, MiddlewareContext, CallNext, ToolResult
import mcp.types as mt

logger = logging.getLogger(__name__)

# The 11 mega-tools — enforce ingress tolerance on all of them
MEGA_TOOLS = {
    "init_anchor", "arifOS_kernel", "apex_soul", "vault_ledger",
    "agi_mind", "asi_heart", "engineering_memory", "physics_reality",
    "math_estimator", "code_engine", "architect_registry",
}


class IngressToleranceMiddleware(Middleware):
    """
    Strip unknown fields from tool arguments before they reach Pydantic.

    Doctrine:
      - entry: adaptive (accept any field)
      - core: governed (strict after normalization)
      - output: strong
    """

    def __init__(self, tool_param_sets: dict[str, set[str]] | None = None) -> None:
        self._tool_param_sets: dict[str, set[str]] = tool_param_sets or {}

    def register_tool_params(self, tool_name: str, param_names: set[str]) -> None:
        self._tool_param_sets[tool_name] = param_names

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        msg = context.message
        tool_name = msg.name

        if tool_name in MEGA_TOOLS and msg.arguments:
            known = self._tool_param_sets.get(tool_name)
            if known:
                unknown = {k for k in msg.arguments if k not in known}
                if unknown:
                    logger.debug(
                        "Ingress tolerance: absorbing unknown fields %s for tool '%s'",
                        unknown, tool_name,
                    )
                    # Mutate in place — context is transient per request
                    for k in unknown:
                        msg.arguments.pop(k)

        return await call_next(context)
