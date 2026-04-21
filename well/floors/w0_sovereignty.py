from arifos.well.models.state import SensorSnapshot, FloorResult

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    # W0 is an invariant - WELL never vetoes.
    return FloorResult(
        floor_id="W0",
        status="PASS",
        score_delta=0.0,
        rationale="Operator veto remains intact. Well holds a mirror.",
        recommended_action="NONE"
    )
