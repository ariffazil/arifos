"""
L5_AGENTS - The 4 Constitutional Agents

Architecture:
├── ARCHITECT (AGI/Mind) → Design & Planning
├── ENGINEER (ASI/Heart) → Implementation & Safety
├── AUDITOR (EYE/Witness) → Verification & Facts
└── VALIDATOR (APEX/Soul) → Judgment & Sealing

Reference: 000-999 Metabolic Loop
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

__version__ = "v55.5-stub"
__all__ = ["ARCHITECT", "ENGINEER", "AUDITOR", "VALIDATOR", "Agent", "AgentResult"]

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Typed result from any agent execution."""
    verdict: str = "VOID"          # SEAL / VOID / SABAR / PARTIAL / 888_HOLD
    data: Dict[str, Any] = field(default_factory=dict)
    session_id: Optional[str] = None
    agent: str = ""
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.verdict in ("SEAL", "PARTIAL")


class Agent:
    """Base agent with typed contract and error handling."""
    name: str = "base"
    symbol: str = "?"

    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """
        Execute agent pipeline.

        Args:
            context: Dict with task-specific keys. Always use dict access (context["key"]),
                     never attribute access (context.key).

        Returns:
            AgentResult with verdict and data.

        Override in subclasses. Base raises NotImplementedError.
        """
        raise NotImplementedError(f"{self.name} not implemented")

    def _safe_get(self, context: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Safely get a value from context dict."""
        if isinstance(context, dict):
            return context.get(key, default)
        # Fallback: attribute access for legacy callers
        return getattr(context, key, default)
