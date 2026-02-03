"""
AGENT: AUDITOR (EYE)
Symbol: 👁
Stages: Cross-cutting (Verification)

The AUDITOR is the Witness.
It verifies facts, checks reality, and ensures truth.

Responsibilities:
- 444_EVIDENCE: Fact-checking, reality grounding
- Cross-stage verification
- Truth validation (F2)
- Injection detection (F12)

The AUDITOR sees all and speaks truth.
"""

import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

try:
    from mcp_server.tools.reality_tool import RealityTool
except ImportError:
    RealityTool = None

from . import Agent, AgentResult


class AUDITOR(Agent):
    """
    EYE Agent - The Witness.

    Verifies claims against external reality.
    Grounds the system in facts, not hallucinations.
    """

    name = "AUDITOR"
    symbol = "👁"

    async def evidence(self, claim):
        """444_EVIDENCE: Fact-check claim."""
        if RealityTool:
            return await RealityTool.execute("check", claim)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def detect_injection(self, input_data):
        """F12: Injection defense."""
        if RealityTool:
            # We treat injection scan as a synchronous check in the wrapper, but let's keep async api
            return await RealityTool.execute("scan", input_data)
        return {"verdict": "VOID", "error": "L4 Core not found"}

    async def execute(self, context):
        """Run audit pipeline. Context is a dict with 'claim' and 'input' keys."""
        claim = self._safe_get(context, "claim", "")
        input_data = self._safe_get(context, "input", "")

        # 1. Check Injection (F12)
        injection = await self.detect_injection(input_data)
        if injection.get("verdict") == "VOID":
            return AgentResult(
                verdict="VOID", agent=self.name, data=injection, error=injection.get("reason")
            )

        # 2. Check Truth (F2)
        if claim:
            evidence = await self.evidence(claim)
            truth_data = {
                "score": evidence.get("truth_score", 0),
                "sources": evidence.get("sources", []),
            }
            # If external reality contradicts claim, we might switch to SABAR, but usually Auditor just reports findings
        else:
            evidence = {"status": "No claim to check"}
            truth_data = {}

        return AgentResult(
            verdict="SEAL",
            agent=self.name,
            data={"evidence": evidence, "truth": truth_data, "injection_safe": injection},
        )
