from typing import List, Optional, Dict, Any
from datetime import datetime
from arifos.well.models.state import SensorReading, SensorSnapshot

class Aggregator:
    def aggregate(self, readings: List[SensorReading]) -> SensorSnapshot:
        if not readings:
            return SensorSnapshot(readings=[], data_quality=0.0, timestamp=datetime.utcnow())
        
        # Calculate quality based on presence of key metrics
        expected_metrics = {"sleep_hours", "stress_load", "clarity", "metabolic_stability"}
        present_metrics = {r.metric for r in readings}
        quality = len(present_metrics.intersection(expected_metrics)) / len(expected_metrics)
        
        return SensorSnapshot(
            readings=readings,
            data_quality=min(1.0, quality),
            timestamp=datetime.utcnow()
        )
