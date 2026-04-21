from typing import List, Literal, Tuple
from arifos.well.models.state import FloorResult

class Throttle:
    def emit(self, score: float, violations: List[FloorResult]) -> Tuple[float, Literal["FULL", "REDUCED", "LIMITED", "PAUSED"], str]:
        bandwidth = 1.0
        scope: Literal["FULL", "REDUCED", "LIMITED", "PAUSED"] = "FULL"
        rationales = []

        # High-severity floor check
        for v in violations:
            if v.recommended_action == "PAUSE":
                return 0.0, "PAUSED", f"Mandatory Pause: {v.rationale}"
            
            if v.recommended_action == "REDUCE_BANDWIDTH":
                bandwidth = min(bandwidth, 0.5)
                scope = "REDUCED"
                rationales.append(v.rationale)

        # Global score check
        if score < 50:
            bandwidth = min(bandwidth, 0.3)
            scope = "LIMITED"
            rationales.append("Global biological readiness below critical threshold.")

        final_rationale = " | ".join(rationales) if rationales else "Nominal Operator Functional State."
        return bandwidth, scope, final_rationale
