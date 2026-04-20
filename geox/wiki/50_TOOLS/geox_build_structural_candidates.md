: "# geox_build_structural_candidates

> **Type:** Tool  
> **Risk Level:** SAFE  
> **Epistemic Level:** INT (interpreted — multiple hypotheses)  
> **Confidence:** 0.75–0.85 per hypothesis  
> **Certainty Band:** [0.65, 0.90]  
> **Tags:** [tool, structural, interpretation, fault, horizon, f2, f7, f9]  
> **arifos_floor:** F2, F7, F9  

---

## Purpose

Generate multiple working hypotheses for structural interpretation. Unlike traditional auto-picking which returns **one** interpretation, this tool embraces **interpretive uncertainty** by generating 3–5 competing hypotheses.

**Core Principle:** Structural interpretation is inherently ambiguous. The tool surfaces ambiguity rather than suppressing it.

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `seismic_ref` | string | Yes | — | Reference from [[geox_load_seismic_line]] |
| `target_horizons` | [string] | Yes | — | Horizon names to interpret |
| `seed_points` | [object] | No | [] | Manual picks to guide interpretation |
| `fault_detection` | bool | No | true | Enable automatic fault picking |
| `confidence_threshold` | float | No | 0.70 | Minimum confidence for hypothesis inclusion |
| `max_candidates` | int | No | 5 | Maximum hypotheses per horizon |
| `alternative_mode` | string | No | "standard" | "standard", "conservative", "aggressive" |

---

## F2 Truth (Grounded Claims)

Each hypothesis must be traceable to seismic evidence:

```json
{
  "hypothesis": {
    "evidence_trail": [
      {"type": "amplitude_peak", "location": [inline, xline, twt], "confidence": 0.85},
      {"type": "phase_consistency", "window": [t1, t2], "confidence": 0.78},
      {"type": "dip_magnitude", "value": 12.5, "confidence": 0.82}
    ]
  }
}
```

**F2 Violation:** Hypothesis without evidence trail → **VOID** verdict.

---

## F7 Humility (Confidence Calibration)

Explicit uncertainty quantification per hypothesis:

| Component | Confidence Source | Typical Range |
|-----------|-------------------|---------------|
| Horizon position | Pick uncertainty | 0.75–0.90 |
| Dip magnitude | Slope calculation | 0.70–0.85 |
| Fault throw | Displacement analysis | 0.60–0.80 |
| Structural style | Pattern recognition | 0.65–0.80 |

---

## F9 Anti-Hantu (Physical Plausibility)

Rejects geologically impossible structures:

| Check | Threshold | Violation |
|-------|-----------|-----------|
| Dip angle | <60° | Reject — rare without validation |
| Fault throw | <500m | Flag — requires evidence |
| Fold wavelength | >10x thickness | Acceptable |
| Angular unconformity | Must have overlying parallel beds | Validate |

**Alternative Explanations:**
Each hypothesis includes alternative geological interpretations:
- Fault vs. Channel
- Unconformity vs. Onlap
- Growth fault vs. Reactive fault
- Salt diapir vs. Igneous intrusion

---

## Returns

```json
{
  "verdict": "SEAL",
  "horizons": {
    "Top_Reservoir": [
      {
        "hypothesis_id": "H1",
        "confidence": 0.85,
        "epistemic_level": "INT",
        "surface": {
          "type": "gridded",
          "dimensions": [2401, 2501],
          "value_range": [1500, 3500],  // TWT ms
          "uncertainty_band_ms": 20
        },
        "geological_model": "Gentle_anticline_with_minor_faults",
        "evidence_trail": [...],
        "alternative_explanations": [
          "Could be remnant high after erosion",
          "Possible salt withdrawal structure"
        ]
      },
      {
        "hypothesis_id": "H2",
        "confidence": 0.78,
        "epistemic_level": "INT",
        "surface": {...},
        "geological_model": "Rollover_into_major_fault",
        "evidence_trail": [...]
      },
      {
        "hypothesis_id": "H3",
        "confidence": 0.72,
        "epistemic_level": "SPEC",
        "surface": {...},
        "geological_model": "Compartmentalized_horst_block",
        "evidence_trail": [...]
      }
    ]
  },
  "faults": {
    "detected": 12,
    "candidates": [
      {
        "fault_id": "F1",
        "confidence": 0.80,
        "geometry": {
          "strike": 75.0,  // degrees
          "dip": 60.0,
          "throw_max_m": 85.0,
          "length_km": 12.5
        },
        "seal_quality": "moderate",
        "reservoir_compartmentalization": "high"
      }
    ]
  },
  "recommendation": {
    "primary_hypothesis": "H1",
    "confidence": 0.85,
    "ambiguity": "moderate",
    "next_steps": [
      "Validate H1 vs H2 with well control",
      "Map fault F1 extent to north"
    ]
  }
}
```

---

## Hypothesis Ranking

| Rank | ID | Confidence | Model | Key Uncertainty |
|------|----|------------|-------|-----------------|
| 1 | H1 | 0.85 | Gentle anticline | Minor fault connectivity |
| 2 | H2 | 0.78 | Rollover structure | Fault seal vs. leak |
| 3 | H3 | 0.72 | Horst block | Western boundary definition |
| — | H4 | 0.65 | (Excluded — below threshold) | — |

---

## Example Workflow

```python
# Step 1: Load seismic
seismic = geox_load_seismic_line(...)

# Step 2: Generate candidates
candidates = geox_build_structural_candidates(
    seismic_ref=seismic.ref,
    target_horizons=["Top_Reservoir", "Base_Reservoir"],
    fault_detection=True,
    confidence_threshold=0.70,
    max_candidates=5
)

# Step 3: Review ambiguity
for horizon_name, hyps in candidates.horizons.items():
    print(f"{horizon_name}: {len(hyps)} hypotheses")
    for h in hyps:
        print(f"  {h.hypothesis_id}: {h.confidence} — {h.geological_model}")
        if h.alternative_explanations:
            print(f"    Alt: {h.alternative_explanations}")

# Step 4: Forward to prospect evaluation
if candidates.recommendation.confidence > 0.80:
    prospect = build_prospect(candidates.recommendation.primary_hypothesis)
```

---

## Cross-References

- Input: [[geox_load_seismic_line]]
- Output to: [[geox_evaluate_prospect]], [[geox_audit_conflation]]
- Theory: [[10_THEORY/Theory_of_Anomalous_Contrast]]
- Physics: [[20_PHYSICS/Seismic_Reflectivity]]
- Cases: [[60_CASES/Structural_Interpretation_Workflow]]

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `F2_NO_EVIDENCE` | Hypothesis lacks seismic support | Lower confidence threshold or add seed points |
| `F9_IMPOSSIBLE_DIP` | Dip angle >60° detected | Check for acquisition artifact |
| `F7_OVERCONFIDENCE` | Confidence >0.95 with limited data | Force recalibration or flag for review |

---

*Tool Specification v1.0.0 · Part of [[50_TOOLS/Tool_Index]]*