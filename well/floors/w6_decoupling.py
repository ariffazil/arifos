from arifos.well.models.state import SensorSnapshot, FloorResult

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    # W6: Incentive Decoupling
    readings = {r.metric: r.raw_value for r in snapshot.readings}
    loop_count = readings.get("intent_loop_count", 0.0)
    
    if loop_count > 10:
        return FloorResult(
            floor_id="W6", status="CRITICAL", score_delta=20.0,
            rationale="Biological capture detected (repetitive intent loops).",
            recommended_action="PAUSE"
        )
    return FloorResult(floor_id="W6", status="PASS", score_delta=0.0, rationale="No capture detected.", recommended_action="NONE")
