"""Minimal in-memory telemetry for AAA MCP tool calls."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class TelemetryStore:
    calls: int = 0
    verdicts: Dict[str, int] = field(default_factory=dict)

    def record(self, payload: Dict[str, Any]) -> None:
        self.calls += 1
        verdict = str(payload.get("verdict", "UNKNOWN"))
        self.verdicts[verdict] = self.verdicts.get(verdict, 0) + 1

    def snapshot(self) -> Dict[str, Any]:
        return {
            "calls": self.calls,
            "verdicts": dict(self.verdicts),
        }
