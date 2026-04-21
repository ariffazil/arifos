from arifos.well.models.state import SensorSnapshot, FloorResult

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    return FloorResult(
        floor_id="W1",
        status="PASS",
        score_delta=0.0,
        rationale="Sleep nominal.",
        recommended_action="NONE"
    ) # Baseline stub, thresholds implemented in next pass
