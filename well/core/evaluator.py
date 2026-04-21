from typing import List
from arifos.well.models.state import SensorSnapshot, FloorResult
from arifos.well.floors import (
    w0_sovereignty, w1_sleep, w2_metabolic, w3_stress, 
    w4_physical, w5_cognitive, w6_decoupling, w7_atrophy
)

class Evaluator:
    def __init__(self):
        self.floors = [
            w0_sovereignty, w1_sleep, w2_metabolic, w3_stress,
            w4_physical, w5_cognitive, w6_decoupling, w7_atrophy
        ]

    def evaluate_all(self, snapshot: SensorSnapshot) -> List[FloorResult]:
        return [f.evaluate(snapshot) for f in self.floors]
