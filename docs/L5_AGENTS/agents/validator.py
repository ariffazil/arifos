"""
AGENT: VALIDATOR (APEX Ψ)
Symbol: Ψ
Stages: 888-999 (Judge → Seal)

The VALIDATOR is the Soul of the system.
It renders the final verdict and seals the ledger.

Responsibilities:
- 888_JUDGE: Tri-witness consensus, Genius check
- 999_SEAL: Cryptographic logging, closure

Constitutional Floors:
- F3: Tri-Witness (Consensus)
- F8: Genius (G ≥ 0.80)
- F11: Authority (Command verified)
"""

import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

try:
    from mcp_server.tools.apex_tool import APEXTool
except ImportError:
    APEXTool = None

from . import Agent, AgentResult


class VALIDATOR(Agent):
    """
    APEX Agent - The Judge.

    Final constitutional authority.
    Seals the outcome if floors are met.
    """

    name = "VALIDATOR"
    symbol = "Ψ"

    async def judge(self, query):
        """888_JUDGE: Render verdict."""
        if APEXTool:
            # We assume query contains the full context needed for judgment
            return APEXTool.execute("judge", query)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def seal(self, judge_result):
        """999_SEAL: Cryptographic seal."""
        if APEXTool:
            return APEXTool.execute("proof", str(judge_result))
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def execute(self, context):
        """Run full APEX pipeline."""
        query = self._safe_get(context, "query", "")

        judge = await self.judge(query)
        if judge.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=judge, error=judge.get("reason")
            )

        seal = await self.seal(judge)

        return AgentResult(
            verdict="SEAL",
            agent=self.name,
            data={"judge": judge, "seal": seal},
        )
