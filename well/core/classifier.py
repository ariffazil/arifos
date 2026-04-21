from typing import Literal
from arifos.well.const import OFS_NOMINAL_MIN, OFS_ELEVATED_MIN, OFS_DEGRADED_MIN

class Classifier:
    def classify(self, score: float) -> Literal["NOMINAL", "ELEVATED", "DEGRADED", "CRITICAL"]:
        if score >= OFS_NOMINAL_MIN: return "NOMINAL"
        if score >= OFS_ELEVATED_MIN: return "ELEVATED"
        if score >= OFS_DEGRADED_MIN: return "DEGRADED"
        return "CRITICAL"
