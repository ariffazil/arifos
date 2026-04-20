# geox_compute_petrophysics

> **Phase B** | **Provenance:** DERIVED | **Floor:** F2·F4·F7·F9

Full petrophysics property pipeline. Computes Vsh, porosity, water saturation, BVW,
NTG, and permeability proxy from raw log curves. Applies Monte Carlo uncertainty
propagation. All outputs are DERIVED — physics calculations applied to measured data.

---

## Input Schema

```json
{
  "gr": 65.0,
  "gr_clean": 20.0,
  "gr_shale": 100.0,
  "rhob": 2.35,
  "nphi": 0.22,
  "rt": 18.5,
  "rw": 0.05,
  "sw_model": "simandoux",
  "depth_m": 2400.0,
  "monte_carlo_iterations": 1000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gr` | float | Yes | Raw gamma ray (API) |
| `gr_clean` | float | Yes | Clean sand GR baseline (API) |
| `gr_shale` | float | Yes | Shale GR baseline (API) |
| `rhob` | float | Yes | Bulk density (g/cc) |
| `nphi` | float | Yes | Neutron porosity (fraction) |
| `rt` | float | Yes | True resistivity (Ωm) |
| `rw` | float | Yes | Formation water resistivity (Ωm) |
| `sw_model` | str | Yes | `"archie"`, `"simandoux"`, or `"indonesia"` |
| `depth_m` | float | No | Reference depth for provenance |
| `monte_carlo_iterations` | int | No | Default 1000 |

---

## Output Schema

```json
{
  "status": "SEAL",
  "provenance_tag": "DERIVED",
  "vsh": 0.46,
  "phi_density": 0.18,
  "phi_neutron": 0.22,
  "phi_effective": 0.18,
  "sw": 0.41,
  "sw_uncertainty": 0.06,
  "bvw": 0.074,
  "ntg": 0.82,
  "permeability_md": 42.0,
  "sw_model_used": "simandoux",
  "floor_verdicts": {
    "f2_truth": "PASS",
    "f4_clarity": "PASS",
    "f7_humility": "PASS",
    "f9_anti_hantu": "PASS"
  },
  "hold_triggers": [],
  "uncertainty_band": {
    "sw_p10": 0.35,
    "sw_p50": 0.41,
    "sw_p90": 0.47
  }
}
```

---

## Floor Enforcement

| Floor | Trigger | Action |
|-------|---------|--------|
| F2 TRUTH | rt ≤ 0 or phi ≤ 0 | 888_HOLD |
| F4 CLARITY | Missing units (rhob without g/cc context) | Warning |
| F7 HUMILITY | Uncertainty band not computable | 888_HOLD |
| F9 ANTI-HANTU | Sw > 1.0 or Sw < 0.0 from solver | 888_HOLD |

---

## Permeability Proxy

Kozeny-Carman approximation: **k = 1000 · φ³** (mD)

| φ | k (mD) |
|---|--------|
| 0.10 | ~1 |
| 0.20 | ~8 |
| 0.30 | ~27 |

---

## Example Call

```python
result = await geox_compute_petrophysics(
    gr=65.0, gr_clean=20.0, gr_shale=100.0,
    rhob=2.35, nphi=0.22, rt=18.5, rw=0.05,
    sw_model="simandoux",
)
assert result.provenance_tag == "DERIVED"
assert 0.0 < result.sw < 1.0
assert result.uncertainty_band is not None
```

---

*DITEMPA BUKAN DIBERI*
