from typing import List
from arifos.well.models.state import FloorResult

class Scorer:
    def compute_score(self, violations: List[FloorResult]) -> float:
        base_score = 100.0
        # Sum deltas but cap at 100.0 subtraction
        total_delta = sum(v.score_delta for v in violations)
        return max(0.0, min(100.0, base_score - total_delta))
