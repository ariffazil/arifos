"""Minimal in-memory telemetry for AAA MCP tool calls."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TelemetryStore:
    calls: int = 0
    verdicts: dict[str, int] = field(default_factory=dict)

    def record(self, payload: dict[str, Any]) -> None:
        self.calls += 1
        verdict = str(payload.get("verdict", "UNKNOWN"))
        self.verdicts[verdict] = self.verdicts.get(verdict, 0) + 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "verdicts": dict(self.verdicts),
        }
