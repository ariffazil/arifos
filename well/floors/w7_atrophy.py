from arifos.well.models.state import SensorSnapshot, FloorResult

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    # W7: Skill Atrophy
    readings = {r.metric: r.raw_value for r in snapshot.readings}
    days_since_manual = readings.get("days_since_practice", 0.0)
    
    if days_since_manual > 60:
        return FloorResult(
            floor_id="W7", status="WARNING", score_delta=15.0,
            rationale="Severe skill atrophy risk (>60 days without manual practice).",
            recommended_action="MONITOR"
        )
    return FloorResult(floor_id="W7", status="PASS", score_delta=0.0, rationale="Skills maintained.", recommended_action="NONE")
