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

import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

try:
    from mcp_server.tools.asi_tool import ASITool
except ImportError:
    ASITool = None

from . import Agent, AgentResult


class ENGINEER(Agent):
    """
    ASI Agent - The Builder.

    Validates safety and executes the design.
    Ensures ethical alignment before action.
    """

    name = "ENGINEER"
    symbol = "Ω"

    async def empathize(self, query):
        """555_EMPATHIZE: Stakeholder analysis."""
        if ASITool:
            return ASITool.execute("empathize", query)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def align(self, empathy_result):
        """666_ALIGN: Ethical check."""
        if ASITool:
            return ASITool.execute("align", str(empathy_result))
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def act(self, align_result):
        """777_ACT: Execution."""
        # STUB: In production, this would call code editing tools
        # For now, we simulate safe execution based on alignment
        if align_result.get("verdict") == "SEAL":
            return {"verdict": "SEAL", "status": "Built safely"}
        return {"verdict": "VOID", "reason": "Alignment failed"}

    async def execute(self, context):
        """Run full ASI pipeline."""
        query = self._safe_get(context, "query", "")

        empathy = await self.empathize(query)
        if empathy.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=empathy, error=empathy.get("reason")
            )

        align = await self.align(empathy)
        if align.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=align, error=align.get("reason")
            )

        act = await self.act(align)

        return AgentResult(
            verdict=act.get("verdict"),
            agent=self.name,
            data={"empathy": empathy, "align": align, "act": act},
        )
