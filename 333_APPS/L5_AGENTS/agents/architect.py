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

import os
import sys

# Ensure we can import from root if running standalone
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

try:
    from mcp_server.tools.agi_tool import AGITool
except ImportError:
    # Fallback for testing environments where codebase isn't in path
    AGITool = None

from . import Agent, AgentResult


class ARCHITECT(Agent):
    """
    AGI Agent - The Designer.

    Maps user intent to structural design.
    Creates the blueprint before building.
    """

    name = "ARCHITECT"
    symbol = "Δ"

    async def sense(self, query):
        """111_SENSE: Parse and understand."""
        if AGITool:
            return AGITool.execute("sense", query)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def think(self, sense_result):
        """222_THINK: Generate hypotheses."""
        if AGITool:
            # We pass the sense result as context for thinking
            context_str = str(sense_result)
            return AGITool.execute("think", context_str)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def atlas(self, think_result):
        """333_ATLAS: Map the solution space."""
        if AGITool:
            context_str = str(think_result)
            return AGITool.execute("map", context_str)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def execute(self, context):
        """Run full AGI pipeline. Context is a dict with 'query' key."""
        query = self._safe_get(context, "query", "")

        # Pipeline: Sense -> Think -> Atlas
        sense = await self.sense(query)

        # If sense fails (e.g. Injection), stop early
        if sense.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=sense, error=sense.get("reason")
            )

        think = await self.think(sense)

        atlas = await self.atlas(think)

        return AgentResult(
            verdict="SEAL",
            agent=self.name,
            data={"sense": sense, "think": think, "atlas": atlas},
        )
