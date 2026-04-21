from arifos.well.models.state import SensorSnapshot, FloorResult

def evaluate(snapshot: SensorSnapshot) -> FloorResult:
    readings = {r.metric: r.raw_value for r in snapshot.readings}
    stability = readings.get("metabolic_stability", 10.0)
    hydration = readings.get("hydration", "hydrated")

    delta = 0.0
    if hydration == "dehydrated": delta += 5.0
    
    if stability < 5:
        return FloorResult(
            floor_id="W2", status="CAUTION", score_delta=delta + 10.0,
            rationale="Metabolic instability detected.",
            recommended_action="MONITOR"
        )
    
    return FloorResult(floor_id="W2", status="PASS", score_delta=delta, rationale="Metabolic nominal.", recommended_action="NONE")
