"""
AGENT: ARCHITECT (AGI Δ)
Symbol: Δ
Stages: 111-333 (Sense → Think → Atlas)

The ARCHITECT is the Mind of the system.
It designs, plans, and maps the solution space.

Responsibilities:
- 111_SENSE: Parse intent, extract entities
- 222_THINK: Generate hypotheses, reason
- 333_ATLAS: Map context, plan structure

Constitutional Floors:
- F2: Truth (τ ≥ 0.99)
- F4: Clarity (ΔS ≤ 0)
- F7: Humility (Ω₀ ∈ [0.03,0.05])
- F10: Ontology (reality check)
- F12: Injection defense
"""

import inspect
from importlib import import_module
from typing import Any


def _resolve_reason_tool() -> Any:
    for module_name in ("aaa_mcp.server",):
        try:
            tool = getattr(import_module(module_name), "reason_mind")
            return getattr(tool, "fn", tool)
        except (ImportError, AttributeError):
            continue
    return None


REASON_TOOL = _resolve_reason_tool()

from . import Agent, AgentResult


class ARCHITECT(Agent):
    """
    AGI Agent - The Designer.

    Maps user intent to structural design.
    Creates the blueprint before building.
    """

    name = "ARCHITECT"
    symbol = "Δ"

    async def _reason(self, query: str, session_id: str) -> dict[str, Any]:
        if REASON_TOOL is None:
            return {
                "verdict": "VOID",
                "error": "AAA MCP reason_mind tool not available",
                "stage": "111-333",
            }
        try:
            result = REASON_TOOL(query=query, session_id=session_id)
            if inspect.isawaitable(result):
                result = await result
            if isinstance(result, dict):
                return result
            return {
                "verdict": "VOID",
                "error": "Invalid reason_mind response type",
                "stage": "111-333",
            }
        except Exception as exc:
            return {"verdict": "VOID", "error": str(exc), "stage": "111-333"}

    async def sense(self, query: str) -> dict[str, Any]:
        """111_SENSE: Parse and understand."""
        return {"verdict": "SEAL", "stage": "111_SENSE", "query": query}

    async def think(self, query: str, session_id: str) -> dict[str, Any]:
        """222_THINK: Generate hypotheses."""
        return await self._reason(query=query, session_id=session_id)

    async def atlas(self, think_result: dict[str, Any]) -> dict[str, Any]:
        """333_ATLAS: Map the solution space."""
        if think_result.get("verdict") == "VOID":
            return {"verdict": "VOID", "stage": "333_ATLAS", "error": think_result.get("error")}
        return {
            "verdict": "SEAL",
            "stage": "333_ATLAS",
            "next_actions": think_result.get("next_actions", []),
            "truth": think_result.get("truth", {}),
        }

    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """Run full AGI pipeline. Context is a dict with 'query' key."""
        if not isinstance(context, dict):
            return AgentResult(verdict="VOID", agent=self.name, error="Context must be a dict")

        query = str(self._safe_get(context, "query", "")).strip()
        session_id = str(self._safe_get(context, "session_id", "")).strip()
        if not query:
            return AgentResult(
                verdict="SABAR", agent=self.name, error="Missing query for ARCHITECT execution"
            )
        if not session_id:
            return AgentResult(
                verdict="SABAR", agent=self.name, error="Missing session_id for ARCHITECT execution"
            )

        # Pipeline: Sense -> Think -> Atlas
        sense = await self.sense(query)

        # If sense fails (e.g. Injection), stop early
        if sense.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=sense, error=sense.get("error")
            )

        think = await self.think(query=query, session_id=session_id)

        atlas = await self.atlas(think)

        return AgentResult(
            verdict="SEAL",
            agent=self.name,
            data={"sense": sense, "think": think, "atlas": atlas},
        )
