"""
AGENT: ENGINEER (ASI Ω)
Symbol: Ω
Stages: 555-777 (Empathy → Align → Act)

The ENGINEER is the Heart of the system.
It builds, protects, and ensures safety.

Responsibilities:
- 555_EMPATHIZE: Identify stakeholders, empathy check
- 666_ALIGN: Check ethics, policy, safety floors
- 777_ACT: Execute construction (Simulated)

Constitutional Floors:
- F1: Amanah (reversibility)
- F5: Peace (stability)
- F6: Empathy (stakeholder protection)
- F9: Anti-Hantu (no deception)
"""

import inspect
from importlib import import_module
from typing import Any


def _resolve_asi_tool() -> Any:
    for module_name, attr in (
        ("aaa_mcp.server", "simulate_heart"),
        ("aaa_mcp.server", "critique_thought"),
    ):
        try:
            tool = getattr(import_module(module_name), attr)
            resolved = getattr(tool, "fn", tool)
            if attr == "simulate_heart":
                simulate = resolved
            else:
                critique = resolved
        except (ImportError, AttributeError):
            continue
    return {"simulate": locals().get("simulate"), "critique": locals().get("critique")}


ASI_TOOLS = _resolve_asi_tool()

from . import Agent, AgentResult


class ENGINEER(Agent):
    """
    ASI Agent - The Builder.

    Validates safety and executes the design.
    Ensures ethical alignment before action.
    """

    name = "ENGINEER"
    symbol = "Ω"

    async def _execute_asi(self, action: str, **kwargs: Any) -> dict[str, Any]:
        tool = ASI_TOOLS.get(action)
        if tool is None:
            return {
                "verdict": "VOID",
                "error": f"AAA MCP {action} tool not available",
                "stage": "555-777",
            }
        try:
            result = tool(**kwargs)
            if inspect.isawaitable(result):
                result = await result
            if isinstance(result, dict):
                return result
            return {
                "verdict": "VOID",
                "error": "Invalid AAA MCP response type",
                "stage": "555-777",
            }
        except Exception as exc:
            return {"verdict": "VOID", "error": str(exc), "stage": "555-777"}

    async def empathize(self, query: str, session_id: str) -> dict[str, Any]:
        """555_EMPATHIZE: Stakeholder analysis."""
        return await self._execute_asi("simulate", query=query, session_id=session_id)

    async def align(self, query: str, session_id: str) -> dict[str, Any]:
        """666_ALIGN: Ethical check."""
        return await self._execute_asi("critique", session_id=session_id, query=query)

    async def act(self, align_result: dict[str, Any]) -> dict[str, Any]:
        """777_ACT: Execution."""
        # STUB: In production, this would call code editing tools
        # For now, we simulate safe execution based on alignment
        if align_result.get("verdict") == "SEAL":
            return {"verdict": "SEAL", "status": "Built safely"}
        return {"verdict": "VOID", "reason": "Alignment failed"}

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """Run full ASI pipeline."""
        if not isinstance(context, dict):
            return AgentResult(verdict="VOID", agent=self.name, error="Context must be a dict")

        query = str(self._safe_get(context, "query", "")).strip()
        session_id = str(self._safe_get(context, "session_id", "")).strip()
        if not query:
            return AgentResult(
                verdict="SABAR", agent=self.name, error="Missing query for ENGINEER execution"
            )
        if not session_id:
            return AgentResult(
                verdict="SABAR", agent=self.name, error="Missing session_id for ENGINEER execution"
            )

        empathy = await self.empathize(query=query, session_id=session_id)
        if empathy.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=empathy, error=empathy.get("error")
            )

        align = await self.align(query=query, session_id=session_id)
        if align.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=align, error=align.get("error")
            )

        act = await self.act(align)

        return AgentResult(
            verdict=str(act.get("verdict", "VOID")),
            agent=self.name,
            data={"empathy": empathy, "align": align, "act": act},
        )
