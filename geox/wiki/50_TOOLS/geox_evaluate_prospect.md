: "# geox_evaluate_prospect

> **Type:** Tool  
> **Risk Level:** GUARDED (888_HOLD required for >50 MMboe)  
> **Epistemic Level:** SPEC (speculative — prospect risking)  
> **Confidence:** Variable per parameter  
> **Certainty Band:** [0.45, 0.85]  
> **Tags:** [tool, prospect, risking, valuation, f1, f7, f13]  
> **arifos_floor:** F1, F7, F13  

---

## Purpose

Full petroleum system evaluation with constitutional safeguards. This is the **highest-stakes** GEOX tool — it directly impacts investment decisions.

**Critical Constraint:** Any prospect with >50 MMboe potential or <70% confidence on critical factors triggers **888_HOLD** requiring human review.

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prospect_name` | string | Yes | Unique prospect identifier |
| `trap_definition` | object | Yes | Structural/stratigraphic geometry |
| `reservoir_params` | object | Yes | [[30_MATERIALS/RATLAS_Index]] reference |
| `seal_params` | object | Yes | Cap rock properties and geometry |
| `source_kitchen` | object | Yes | Migration pathway and timing |
| `confidence_mode` | string | No | "conservative" (default), "moderate", "aggressive" |
| `economic_threshold` | float | No | Minimum volume for commerciality (MMboe) |

### Detailed Parameter Schema

**trap_definition:**
```json
{
  "type": "structural" | "stratigraphic" | "combination",
  "closure_area_km2": 12.5,
  "closure_height_m": 85.0,
  "spill_point_depth_m": 2150.0,
  "fill_to_spill": true,
  "confidence": 0.82,
  "epistemic_level": "INT"
}
```

**reservoir_params:**
```json
{
  "material_code": "SAND_QZ_CLEAN",
  "porosity_mean": 0.22,
  "porosity_std": 0.04,
  "saturation_mean": 0.78,
  "saturation_std": 0.12,
  "net_to_gross": 0.65,
  "pay_thickness_m": 45.0,
  "confidence": 0.75,
  "epistemic_level": "DER"
}
```

**seal_params:**
```json
{
  "material_code": "SHALE_ILL",
  "thickness_m": 120.0,
  "leakage_risk": "low" | "moderate" | "high",
  "fault_seal_probability": 0.70,
  "confidence": 0.65,
  "epistemic_level": "INT"
}
```

---

## F1 Amanah (No Irreversible Action Without Seal)

Prospect evaluation may trigger **irreversible actions**:
- Drilling commitment
- Lease acquisition
- Farm-in agreements

**888_HOLD Trigger Conditions:**

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Potential volume | >50 MMboe P50 | 888_HOLD mandatory |
| Critical factor confidence | <0.70 | 888_HOLD mandatory |
| Seal confidence | <0.60 | 888_HOLD mandatory |
| Risk factors >3 | Any at <0.50 | 888_HOLD recommended |
| Economic threshold proximity | Within 20% | Warning flag |

---

## F7 Humility (Confidence Calibration)

Output includes explicit confidence bands per component:

```json
{
  "volumes": {
    "p10": {"value": 12.5, "confidence": 0.75, "band": [0.65, 0.85]},
    "p50": {"value": 34.2, "confidence": 0.70, "band": [0.60, 0.80]},
    "p90": {"value": 78.9, "confidence": 0.65, "band": [0.55, 0.75]}
  }
}
```

**Confidence Mode Impact:**

| Mode | P50 Adjustment | Confidence Band | Use Case |
|------|----------------|-----------------|----------|
| Conservative | -20% | Narrow [±0.08] | Early exploration, limited data |
| Moderate | Baseline | Standard [±0.10] | Standard risking |
| Aggressive | +15% | Wide [±0.15] | Mature basin, analog-rich |

---

## F13 Sovereign (Human Authority)

GUARDED tools require explicit human authorization for:
- Generating final prospect report
- Exporting to external systems
- Triggering workflow actions

**Workflow:**
```
1. LLM calls geox_evaluate_prospect()
2. System evaluates 888_HOLD triggers
3. If HOLD triggered → Pause, notify human
4. Human reviews via [[70_GOVERNANCE/888_HOLD_Registry]]
5. Human approves/rejects with rationale
6. If approved → Continue with verdict
7. Audit trail written to [[arifos::999_VAULT]]
```

---

## Returns

```json
{
  "verdict": "PARTIAL",  // SEAL, PARTIAL, SABAR, or VOID
  "888_HOLD_triggered": true,
  "hold_reason": "Volume threshold exceeded (P50 = 78.9 MMboe)",
  
  "petroleum_system": {
    "trap": {
      "probability": 0.82,
      "confidence": 0.88,
      "epistemic_level": "INT"
    },
    "reservoir": {
      "probability": 0.75,
      "confidence": 0.82,
      "epistemic_level": "DER"
    },
    "seal": {
      "probability": 0.70,
      "confidence": 0.60,  // Low — triggers hold
      "epistemic_level": "INT"
    },
    "charge": {
      "probability": 0.65,
      "confidence": 0.70,
      "epistemic_level": "SPEC"
    }
  },
  
  "probability_of_success": 0.28,  // Product of above
  
  "volumes": {
    "p10": {"value": 12.5, "unit": "MMboe"},
    "p50": {"value": 34.2, "unit": "MMboe"},
    "p90": {"value": 78.9, "unit": "MMboe"}
  },
  
  "expected_monetary_value": {
    "npv_10_musd": 125.0,
    "npv_50_musd": 45.0,
    "npv_90_musd": -15.0
  },
  
  "human_review_points": [
    "Seal confidence (0.60) below threshold (0.70)",
    "Charge timing speculative — no direct evidence",
    "Fault compartmentalization not fully mapped"
  ],
  
  "risk_mitigation": [
    "Acquire 2D seismic across fault trend",
    "Drill flank well to test seal",
    "Geochemical analysis of nearby seeps"
  ],
  
  "cross_refs": [
    "[[30_MATERIALS/SAND_QZ_CLEAN]]",
    "[[30_MATERIALS/SHALE_ILL]]",
    "[[40_BASINS/Malay_Basin]]",
    "[[60_CASES/Prospect_Evaluation_Workflow]]"
  ]
}
```

---

## Risk Factor Breakdown

| Factor | Probability | Confidence | Weight | Contribution |
|--------|-------------|------------|--------|--------------|
| Trap | 0.82 | 0.88 | 0.25 | 0.205 |
| Reservoir | 0.75 | 0.82 | 0.25 | 0.188 |
| Seal | 0.70 | 0.60 | 0.20 | 0.140 |
| Charge | 0.65 | 0.70 | 0.20 | 0.130 |
| Timing | 0.80 | 0.75 | 0.10 | 0.080 |
| **Product** | **0.28** | — | — | **POS** |

---

## Example: Full Evaluation Workflow

```python
# Step 1: Define prospect
prospect = {
    "prospect_name": "Jaguar_Prospect",
    "trap_definition": {
        "type": "structural",
        "closure_area_km2": 15.3,
        "closure_height_m": 95.0,
        "confidence": 0.82
    },
    "reservoir_params": {
        "material_code": "SAND_QZ_CLEAN",
        "porosity_mean": 0.24,
        "saturation_mean": 0.80,
        "net_to_gross": 0.70,
        "confidence": 0.78
    },
    "seal_params": {
        "material_code": "SHALE_ILL",
        "thickness_m": 150.0,
        "confidence": 0.65  // Low — will trigger hold
    },
    "confidence_mode": "moderate"
}

# Step 2: Evaluate
evaluation = geox_evaluate_prospect(**prospect)

# Step 3: Handle 888_HOLD
if evaluation.888_HOLD_triggered:
    print(f"HOLD: {evaluation.hold_reason}")
    print(f"Review points: {evaluation.human_review_points}")
    # Human review required...
```

---

## Cross-References

- Materials: [[30_MATERIALS/RATLAS_Index]]
- Basin context: [[40_BASINS/Malay_Basin]]
- Workflow: [[60_CASES/Prospect_Evaluation_Workflow]]
- Governance: [[70_GOVERNANCE/888_HOLD_Registry]], [[70_GOVERNANCE/Seals_and_Verdicts]]
- Theory: [[10_THEORY/Forward_vs_Inverse_Modelling]]

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-08 | Initial specification with 888_HOLD integration |

---

*Tool Specification v1.0.0 · Part of [[50_TOOLS/Tool_Index]]*