# aaa_mcp/core/state.py
# SystemState exposure for v62 - Step 1 of cognitive runtime transformation
# Minimal schema: uncertainty, risk, grounding, loop_count, profile

from dataclasses import dataclass
from typing import Literal

Profile = Literal["factual", "creative", "crisis", "routine"]


@dataclass
class SystemState:
    """
    Minimal SystemState for v62.
    Exposes system metrics for scheduler routing (Step 4).

    Fields:
        uncertainty: 0.0-1.0 (epistemic uncertainty)
        risk: 0.0-1.0 (stakeholder impact)
        grounding: 0.0-1.0 (evidence strength - currently heuristic)
        loop_count: int (iteration detection)
        profile: domain classification for adaptive floors
    """

    uncertainty: float  # 0..1
    risk: float  # 0..1
    grounding: float  # 0..1 (Step 1: heuristic only, Step 2: real evidence)
    loop_count: int
    profile: Profile

    def to_dict(self) -> dict:
        return {
            "uncertainty": round(self.uncertainty, 2),
            "risk": round(self.risk, 2),
            "grounding": round(self.grounding, 2),
            "loop_count": self.loop_count,
            "profile": self.profile,
        }
