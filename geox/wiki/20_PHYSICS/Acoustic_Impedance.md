: "# Acoustic Impedance

> **Type:** Physics  
> **Epistemic Level:** DER (derived from velocity and density)  
> **Confidence:** 0.98  
> **Certainty Band:** [0.96, 0.99]  
> **Tags:** [physics, acoustic_impedance, seismic, reflection, earth_canon_9]  
> **arifos_floor:** F2, F4  

---

## Definition

**Acoustic Impedance (Z)** is the product of density (ρ) and compressional wave velocity (Vp):

```
Z = ρ × Vp

Where:
- Z = Acoustic Impedance (kg/m²·s or Rayl)
- ρ = Bulk density (kg/m³)
- Vp = P-wave velocity (m/s)

Units:
- SI: kg/m²·s (often expressed as ×10⁶ for rock values)
- CGS: g/cm²·s (Rayl)
- Industry: m/s × g/cm³ (equivalent to kg/m²·s ×10⁶)
```

---

## Physical Significance

Acoustic impedance is the fundamental property that governs:
1. **Seismic reflection strength** — Reflection coefficient depends on Z contrast
2. **Wave propagation** — Impedance mismatch controls transmission vs. reflection
3. **Rock properties** — Z correlates with porosity, lithology, and fluid content

```
┌─────────────────────────────────────────────────────────────┐
│              ACOUSTIC IMPEDANCE & SEISMIC RESPONSE           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Layer 1: Sandstone                                        │
│   Z₁ = 6.5 ×10⁶ kg/m²·s                                    │
│         ↓                                                    │
│   Interface: Reflection Coefficient R                        │
│         ↓                                                    │
│   Layer 2: Shale                                            │
│   Z₂ = 4.5 ×10⁶ kg/m²·s                                    │
│                                                              │
│   R = (Z₂ - Z₁) / (Z₂ + Z₁)                                │
│     = (4.5 - 6.5) / (4.5 + 6.5)                            │
│     = -0.18                                                  │
│                                                              │
│   Negative R = negative polarity reflection                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Reflection Coefficient

The **reflection coefficient (R)** at normal incidence:

```
        Z₂ - Z₁
R = ─────────────
        Z₂ + Z₁

Where:
- Z₁ = Impedance of upper layer
- Z₂ = Impedance of lower layer

Amplitude reflection: AR = |R|²
Transmission coefficient: T = 1 - R
```

### Typical Values

| Interface | Z₁ | Z₂ | R | Polarity |
|-----------|-----|-----|--------|----------|
| Sand → Shale | 6.5 | 4.5 | -0.18 | Negative |
| Shale → Sand | 4.5 | 6.5 | +0.18 | Positive |
| Limestone → Shale | 9.0 | 4.5 | +0.33 | Positive (strong) |
| Water → Sand | 1.5 | 6.5 | +0.63 | Very strong |

---

## EARTH.CANON_9 Relationship

Acoustic Impedance integrates three of the nine canonical variables:

```
Z = f(ρ, Vp, φ, Sw, lithology)

Where from EARTH.CANON_9:
- ρ (density) — EARTH.01
- Vp (velocity) — EARTH.04
- φ (porosity) — EARTH.05
- Sw (water saturation) — EARTH.06
```

**Key Insight:** Impedance is the **seismic observable** that encodes multiple physical properties. Seismic inversion aims to recover these components.

---

## Typical Values by Lithology

| Material | Density (g/cm³) | Vp (m/s) | Impedance (×10⁶ kg/m²·s) |
|----------|-----------------|----------|--------------------------|
| Air | 0.001 | 330 | 0.0003 |
| Water | 1.00 | 1500 | 1.50 |
| Oil | 0.80 | 1300 | 1.04 |
| Gas | 0.20 | 450 | 0.09 |
| Sandstone (clean) | 2.65 | 3500 | 9.28 |
| Sandstone (30% φ) | 2.20 | 2800 | 6.16 |
| Shale | 2.50 | 2800 | 7.00 |
| Limestone | 2.71 | 5500 | 14.91 |
| Dolomite | 2.87 | 6000 | 17.22 |
| Salt | 2.16 | 4500 | 9.72 |
| Granite | 2.70 | 5500 | 14.85 |

---

## Factors Affecting Impedance

### 1. Porosity

```
Wyllie Time-Average Equation:

1/Vp = φ/Vp_fluid + (1-φ)/Vp_matrix

Where:
- φ = porosity
- Vp_fluid = fluid velocity (water ~1500 m/s)
- Vp_matrix = matrix velocity (quartz ~6000 m/s)

Implication: Higher φ → Lower Vp → Lower Z
```

**Rule of Thumb:** Every 10% porosity increase → ~1.5 ×10⁶ kg/m²·s impedance decrease.

### 2. Fluid Content

| Fluid | Vp (m/s) | Density (g/cm³) | Impedance Effect |
|-------|----------|-----------------|------------------|
| Gas | 450 | 0.20 | Large decrease |
| Oil | 1300 | 0.80 | Moderate decrease |
| Water | 1500 | 1.00 | Reference |

**Gas Effect:** Gas-filled sand has much lower impedance than water-filled sand — creates strong "bright spot" reflection.

### 3. Lithology

**General Hierarchy (highest to lowest Z):**
1. Dolomite: 14–18 ×10⁶
2. Limestone: 12–16 ×10⁶
3. Granite: 14–15 ×10⁶
4. Clean sandstone: 8–10 ×10⁶
5. Shale: 6–8 ×10⁶
6. Porous sandstone: 4–7 ×10⁶

---

## Seismic Inversion

**Objective:** Recover impedance from seismic amplitude.

```
Seismic Data (amplitude) ──► Inversion ──► Impedance Volume
                                      │
                                      ▼
                              [Physical Properties]
                              - Porosity
                              - Lithology
                              - Fluid content
```

### Inversion Methods

| Method | Input | Output | Resolution | Uncertainty |
|--------|-------|--------|------------|-------------|
| Recursive | Seismic, initial model | Relative Z | Medium | High |
| Model-based | Seismic, well logs | Absolute Z | Medium | Medium |
| Sparse-spike | Seismic only | Broadband Z | High | Medium |
| Geostatistical | Seismic, wells, geostats | Stochastic realizations | Variable | Quantified |

### Inversion Quality Control

| Check | Acceptance | F4 Requirement |
|-------|------------|----------------|
| Synthetic vs. seismic | Correlation >0.70 | Must document |
| Well tie residual | <10% of amplitude | With confidence |
| Impedance range | Within lithology bounds | Explicit bounds |
| Frequency content | Matches expected | Bandwidth stated |

---

## Applications in GEOX

### 1. Lithology Discrimination

```python
# Pseudo-code for lithology from impedance
if Z > 12e6:
    lithology = "Carbonate"
elif Z > 8e6:
    lithology = "Clean sandstone"
elif Z > 6e6:
    lithology = "Shaly sandstone"
else:
    lithology = "Shale"

# Always include confidence band!
confidence = calculate_confidence(Z, noise_level, calibration_wells)
```

### 2. Fluid Prediction

Low impedance anomalies in porous sands may indicate gas:
```
Gas sand: Z < 5.5 ×10⁶ kg/m²·s (vs. 6.5+ for water sand)
```

**⚠️ F9 Anti-Hantu:** Low impedance could also be:
- Overpressure
- Coal
- Very porous water sand
- Acquisition artifact

Always require multiple indicators.

### 3. Porosity Estimation

```
φ = f(Z, lithology, fluid)

Common transforms:
- Wyllie: φ = (Z_matrix - Z) / (Z_matrix - Z_fluid)
- Raymer: Empirical relationship
- Neural network: Trained on well data
```

---

## Measurement and Calibration

### From Well Logs

```
Z_log = RHOB × (1/DTC) × conversion_factor

Where:
- RHOB = bulk density log (g/cm³)
- DTC = sonic transit time (μs/ft or μs/m)
- conversion factor = 304.8 for μs/ft to m/s
```

### Quality Control

| Check | Issue | Resolution |
|-------|-------|------------|
| RHOB vs. NPHI crossover | Gas or badhole | Flag for review |
| DTC cycle skips | Error in sonic | Edit or exclude |
| Depth mismatch | Mis-tie | Calibrate to checkshots |

---

## Cross-References

- Canon foundation: [[20_PHYSICS/EARTH_CANON_9]]
- Materials: [[30_MATERIALS/Sedimentary_Clastics]], [[30_MATERIALS/Sedimentary_Carbonates]]
- Seismic theory: [[10_THEORY/Theory_of_Anomalous_Contrast]]
- Tools: [[50_TOOLS/geox_extract_attributes]]

---

## References

1. Sheriff, R.E. & Geldart, L.P. (1995). *Exploration Seismology.* Cambridge.
2. Avseth, P. et al. (2005). *Quantitative Seismic Interpretation.* Cambridge.
3. Hampson, D. et al. (2005). *Simultaneous inversion of pre-stack seismic data.* SEG Abstracts.

---

*Acoustic Impedance v1.0.0 · Part of [[20_PHYSICS/Physics_Index]]*