# geox_select_sw_model

> **Phase B** | **Provenance:** POLICY | **Floor:** F2·F9·F11

Evaluates water saturation model admissibility from log QC flags. Selects the
appropriate Sw model (Archie, Simandoux, Indonesia) based on formation character,
clay type, and salinity constraints. Returns a POLICY-tagged verdict — model
selection is a governed judgement call, not a raw measurement.

---

## Input Schema

```json
{
  "log_qc_flags": {
    "vsh_fraction": 0.25,
    "clay_type": "dispersed",
    "formation_water_salinity_ppm": 50000,
    "has_dielectric_log": false,
    "has_nmr_log": true
  },
  "override_model": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `log_qc_flags.vsh_fraction` | float [0–1] | Yes | Volume of shale fraction |
| `log_qc_flags.clay_type` | str | Yes | `"dispersed"`, `"laminated"`, `"structural"` |
| `log_qc_flags.formation_water_salinity_ppm` | float | Yes | Formation water salinity |
| `log_qc_flags.has_dielectric_log` | bool | No | Presence of dielectric log |
| `log_qc_flags.has_nmr_log` | bool | No | Presence of NMR log |
| `override_model` | str \| null | No | Force a specific model: `"archie"`, `"simandoux"`, `"indonesia"` |

---

## Output Schema

```json
{
  "status": "SEAL",
  "provenance_tag": "POLICY",
  "sw_model_selected": "simandoux",
  "admissibility_score": 0.87,
  "reasoning": "Vsh=0.25 → shaly formation; dispersed clay → Simandoux preferred",
  "floor_verdicts": {
    "f2_truth": "PASS",
    "f9_anti_hantu": "PASS",
    "f11_authority": "PASS"
  },
  "hold_triggers": [],
  "uncertainty_band": null
}
```

---

## Floor Enforcement

| Floor | Trigger | Action |
|-------|---------|--------|
| F2 TRUTH | Vsh + salinity not provided | 888_HOLD |
| F9 ANTI-HANTU | Override model contradicts QC evidence | 888_HOLD |
| F11 AUTHORITY | No provenance declared | 888_HOLD |

---

## Model Selection Logic

| Vsh Fraction | Clay Type | Recommended Model |
|-------------|-----------|-------------------|
| < 0.10 | Any | Archie |
| 0.10–0.40 | Dispersed | Simandoux |
| > 0.30 | Laminated | Indonesia |
| > 0.30 | Structural | Indonesia |

---

## Example Call

```python
result = await geox_select_sw_model(
    log_qc_flags={
        "vsh_fraction": 0.25,
        "clay_type": "dispersed",
        "formation_water_salinity_ppm": 50000,
        "has_dielectric_log": False,
        "has_nmr_log": True,
    }
)
assert result.provenance_tag == "POLICY"
assert result.sw_model_selected == "simandoux"
```

---

*DITEMPA BUKAN DIBERI*
