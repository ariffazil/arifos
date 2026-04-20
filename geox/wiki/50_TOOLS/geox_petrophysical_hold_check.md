# geox_petrophysical_hold_check

> **Phase B** | **Provenance:** POLICY | **Floor:** F2·F4·F7·F9

Runs constitutional floor checks against petrophysical results. Triggers 888_HOLD
when any active floor is violated. Each floor check is independently configurable.
This is the governance gate — the last line of defence before a petrophysical
interpretation reaches the SEAL verdict pathway.

---

## Input Schema

```json
{
  "sw_value": 0.41,
  "phi_value": 0.18,
  "vsh_value": 0.35,
  "depth_m": 2400.0,
  "data_source": "Well-A LAS 2024",
  "run_f2_check": true,
  "run_f4_check": true,
  "run_f7_check": true,
  "run_f9_check": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sw_value` | float | Yes | Water saturation (fraction) |
| `phi_value` | float | Yes | Effective porosity (fraction) |
| `vsh_value` | float | Yes | Volume of shale (fraction) |
| `depth_m` | float | No | Reference depth (m) |
| `data_source` | str | No | Provenance declaration for F11 |
| `run_f2_check` | bool | No | Enable F2 TRUTH check (default: true) |
| `run_f4_check` | bool | No | Enable F4 CLARITY check (default: true) |
| `run_f7_check` | bool | No | Enable F7 HUMILITY check (default: true) |
| `run_f9_check` | bool | No | Enable F9 ANTI-HANTU check (default: true) |

---

## Output Schema

```json
{
  "status": "SEAL",
  "provenance_tag": "POLICY",
  "floor_verdicts": {
    "f2_truth": "PASS",
    "f4_clarity": "PASS",
    "f7_humility": "PASS",
    "f9_anti_hantu": "PASS"
  },
  "hold_triggers": [],
  "overall_verdict": "SEAL",
  "reasoning": "All active floors passed. Interpretation may proceed."
}
```

### 888_HOLD response

```json
{
  "status": "888_HOLD",
  "provenance_tag": "POLICY",
  "floor_verdicts": {
    "f2_truth": "HOLD",
    "f9_anti_hantu": "PASS"
  },
  "hold_triggers": ["sw_value out of physical range [0,1]"],
  "overall_verdict": "888_HOLD",
  "reasoning": "F2 TRUTH violated: sw_value=1.42 is not physically plausible."
}
```

---

## Floor Enforcement

| Floor | Check | Trigger Condition |
|-------|-------|-------------------|
| F2 TRUTH | `run_f2_check` | `sw < 0` or `sw > 1`, or `phi < 0` or `phi > 1` |
| F4 CLARITY | `run_f4_check` | `phi` or `vsh` missing when sw calculation is attempted |
| F7 HUMILITY | `run_f7_check` | Sw uncertainty not propagated (Monte Carlo not run) |
| F9 ANTI-HANTU | `run_f9_check` | Physically impossible combination: e.g., `sw=0.95` with `vsh=0.05` (clean wet) |

---

## Critical Implementation Note

The parameters `run_f2_check`, `run_f4_check`, `run_f7_check`, `run_f9_check` are
**boolean flags** — they must NOT be named the same as the imported service functions
`check_f2_truth`, `check_f4_clarity`, etc. This was a name-shadowing bug fixed in
v0.6.0 (commit `c188394`).

---

## Example Call

```python
result = await geox_petrophysical_hold_check(
    sw_value=0.41,
    phi_value=0.18,
    vsh_value=0.35,
    data_source="Well-A LAS 2024",
    run_f2_check=True,
    run_f9_check=True,
)
assert result.status == "SEAL"
assert result.hold_triggers == []
```

---

*DITEMPA BUKAN DIBERI*
