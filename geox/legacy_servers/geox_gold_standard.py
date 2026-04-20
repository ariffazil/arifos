
import json
from datetime import datetime
from geox_schemas import (
    CausalSceneUISummary, Canon9Item, ContrastVerdict, ContrastMetric, 
    PolicyEvaluation, PolicyBand, UnitRef, Comparator, VerdictCode
)

def generate_gold_example_a():
    """Example A: Well Marker vs Horizon Residual Verdict."""
    
    # 1. Coordinate Unit
    u_ms = UnitRef(name="millisecond", symbol="ms", quantity="time")
    u_m2 = UnitRef(name="square_meter", symbol="m2", quantity="area")

    # 2. Physics Metrics
    metrics = [
        ContrastMetric(
            metric_id="marker_res_01",
            metric_name="z_residual_ms",
            value=8.4,
            unit=u_ms,
            confidence=0.92,
            method_tag="track_interp_linear"
        ),
        ContrastMetric(
            metric_id="marker_res_02",
            metric_name="surface_area_true_m2",
            value=450000.0,
            unit=u_m2,
            confidence=0.98,
            method_tag="quad_tessellation_area"
        )
    ]
    
    # 3. Policy Band Definition
    band = PolicyBand(
        policy_name="residual_f2",
        metric_name="z_residual_ms",
        comparator=Comparator.between,
        lower_bound=-15.0,
        upper_bound=15.0,
        unit=u_ms,
        rationale="F2 Truth requirement: well-seismic residuals must be < 15ms."
    )

    # 4. Policy Evaluation
    policies = [
        PolicyEvaluation(
            metric_name="z_residual_ms",
            observed_value=8.4,
            unit=u_ms,
            band=band,
            verdict=VerdictCode.pass_green,
            explanation="Residual is within the allowed 15ms window."
        )
    ]
    
    # 5. The Final Verdict
    verdict = ContrastVerdict(
        verdict_id="V_RESID_2026_01",
        intent_id="INTENT_WELL_SEIS_TIE",
        status="PASS",
        metrics=metrics,
        links=[],
        floors_evaluated=["F2", "F9"],
        commentary="Residual check passed within 15ms tolerance. Witness data is internally consistent.",
        policy_evaluations=policies
    )
    
    return verdict

def generate_causal_scene_summary():
    """The UISummary for the UI gate."""
    canon_state = [
        Canon9Item(sym='ρ', name='Density', val='2650', unit='kg/m³'),
        Canon9Item(sym='Vp', name='P-Wave', val='4500', unit='m/s'),
        Canon9Item(sym='φ', name='Porosity', val='0.18', unit='v/v'),
    ]
    
    scene = CausalSceneUISummary(
        status="verified",
        epoch="2026.04_GOLD",
        manifold={
            "crs": "WGS84_UTM50N",
            "phi": 0.18,
            "area": 450000,
            "grossH": 250
        },
        canon9=canon_state,
        claims={"d2t_tie": True, "fault_intersection": True, "fluid_crossover": False},
        truth={"f2_passed": True, "f7_uncertainty": 0.04}
    )
    return scene

if __name__ == "__main__":
    v_a = generate_gold_example_a()
    scene = generate_causal_scene_summary()
    
    print("═══════════════════════════════════════════════════════════════════════════════")
    print("GOLD STANDARD VERIFICATION SUITE")
    print("═══════════════════════════════════════════════════════════════════════════════")
    print(f"Verdict A: {v_a.status} ({v_a.verdict_id})")
    
    with open("gold_causal_scene.json", "w") as f:
        json.dump(scene.model_dump(), f, indent=2)
