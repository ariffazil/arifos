# geox_validate_cutoffs

> **Phase B** | **Provenance:** POLICY | **Floor:** F1·F2·F4

Applies a CutoffPolicy schema to petrophysical results. Determines whether an interval
passes or fails reservoir quality cutoffs (Sw, phi, Vsh, NTG). Returns a POLICY-tagged
verdict — cutoffs are engineering judgements, not physics derivations.

---

## Input Schema

```json
{
  "petrophysical_result": {
    "sw": 0.41,
    "phi_effective": 0.18,
    "vsh": 0.35,
    "ntg": 0.82,
    "permeability_md": 42.0
  },
  "cutoff_policy": {
    "sw_max": 0.65,
    "phi_min": 0.10,
    "vsh_max": 0.50,
    "ntg_min": 0.30,
    "k_min_md": 0.1
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `petrophysical_result.sw` | float | Yes | Water saturation (fraction) |
| `petrophysical_result.phi_effective` | float | Yes | Effective porosity (fraction) |
| `petrophysical_result.vsh` | float | Yes | Volume of shale (fraction) |
| `petrophysical_result.ntg` | float | No | Net-to-gross ratio |
| `petrophysical_result.permeability_md` | float | No | Permeability proxy (mD) |
| `cutoff_policy.sw_max` | float | Yes | Maximum Sw for pay classification |
| `cutoff_policy.phi_min` | float | Yes | Minimum porosity |
| `cutoff_policy.vsh_max` | float | Yes | Maximum Vsh |
| `cutoff_policy.ntg_min` | float | No | Minimum NTG |
| `cutoff_policy.k_min_md` | float | No | Minimum permeability (mD) |

---

## Output Schema

```json
{
  "status": "SEAL",
  "provenance_tag": "POLICY",
  "cutoff_result": "PASS",
  "failed_cutoffs": [],
  "pay_flag": true,
  "floor_verdicts": {
    "f1_amanah": "PASS",
    "f2_truth": "PASS",
    "f4_clarity": "PASS"
  },
  "hold_triggers": []
}
```

---

## Floor Enforcement

| Floor | Trigger | Action |
|-------|---------|--------|
| F1 AMANAH | Cutoff policy not declared | 888_HOLD |
| F2 TRUTH | Sw or phi values out of physical range | 888_HOLD |
| F4 CLARITY | Cutoff values not in standard units | Warning |

---

## Cutoff Result Logic

| Condition | `cutoff_result` | `pay_flag` |
|-----------|----------------|------------|
| All cutoffs passed | `"PASS"` | `true` |
| Any cutoff failed | `"FAIL"` | `false` |
| Missing required input | `888_HOLD` | — |

---

## Example Call

```python
result = await geox_validate_cutoffs(
    petrophysical_result={"sw": 0.41, "phi_effective": 0.18, "vsh": 0.35, "ntg": 0.82},
    cutoff_policy={"sw_max": 0.65, "phi_min": 0.10, "vsh_max": 0.50},
)
assert result.provenance_tag == "POLICY"
assert result.pay_flag is True
assert result.cutoff_result == "PASS"
```

---

*DITEMPA BUKAN DIBERI*
