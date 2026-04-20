# Sedimentary Clastics — RATLAS Material Family

> **Type:** Material  
> **Epistemic Level:** DER (derived from lab measurements)  
> **Confidence:** 0.95  
> **Certainty Band:** [0.90, 0.98]  
> **Tags:** [ratlas, materials, sedimentary, clastics, sandstone, shale]  
> **Sources:** [GFZ Potsdam, DSDP Leg 78B, core data]  
> **arifos_floor:** F2, F4  

---

## Family Overview

**RATLAS Family Code:** `SED_CLASTIC`  
**Materials in Family:** 18  
**Main Types:** Sandstone, shale, siltstone, conglomerate  
**Porosity Range:** 0.05 – 0.35 (highly variable)  
**Formation Environment:** Terrestrial to deep marine  

---

## Material Matrix

| Symbol | Name | Grain Size | Φ typical | Permeability | Reservoir Quality |
|--------|------|------------|-----------|--------------|-------------------|
| `SAND_QZ_CLEAN` | Clean Quartz Sandstone | 0.125–2mm | 0.20–0.30 | High | Excellent |
| `SAND_QZ_FELD` | Feldspathic Sandstone | 0.125–2mm | 0.18–0.28 | Mod-High | Good |
| `SAND_QZ_LITH` | Lithic Sandstone | 0.125–2mm | 0.15–0.25 | Moderate | Fair |
| `SAND_ARG` | Argillaceous Sandstone | 0.125–2mm | 0.12–0.20 | Low-Mod | Poor-Fair |
| `SAND_CALC` | Calcareous Sandstone | 0.125–2mm | 0.10–0.18 | Low | Poor |
| `SAND_SILT` | Sandy Siltstone | 0.063–0.125mm | 0.15–0.25 | Low | Fair |
| `SHALE_ILL` | Illitic Shale | <0.004mm | 0.05–0.15 | Negligible | Seal |
| `SHALE_SME` | Smectitic Shale | <0.004mm | 0.10–0.25 | Negligible | Seal |
| `SHALE_KAOL` | Kaolinitic Shale | <0.004mm | 0.08–0.18 | Negligible | Seal |
| `SHALE_CHL` | Chloritic Shale | <0.004mm | 0.06–0.15 | Negligible | Seal |
| `SHALE_ORG` | Organic-rich Shale | <0.004mm | 0.05–0.20 | Negligible | Source rock |
| `SILT_QZ` | Quartz Siltstone | 0.004–0.063mm | 0.18–0.28 | Low | Fair |
| `SILT_CALC` | Calcareous Siltstone | 0.004–0.063mm | 0.15–0.25 | Low | Poor-Fair |
| `CONG_QZ` | Quartz Conglomerate | >2mm | 0.10–0.20 | Variable | Fair |
| `CONG_LITH` | Lithic Conglomerate | >2mm | 0.08–0.18 | Variable | Poor-Fair |
| `GLAUCONITE` | Glauconitic Sand | 0.125–2mm | 0.25–0.40 | Moderate | Good (old sediments) |
| `ARKOSE` | Arkose (K-feldspar rich) | 0.125–2mm | 0.15–0.25 | Moderate | Fair-Good |
| `GRAYWACKE` | Graywacke | 0.125–2mm | 0.05–0.15 | Low | Poor |

---

## Representative Material: `SAND_QZ_CLEAN`

### Description
Clean quartz sandstone — the "reference reservoir." Well-sorted, rounded quartz grains with minimal matrix or cement.

### Canonical 9 Values (Reference)

| Property | Value | Range | Unit |
|----------|-------|-------|------|
| **Density (matrix)** | 2.65 | 2.63–2.67 | g/cm³ |
| **P-wave velocity** | 4500 | 4000–5500 | m/s |
| **S-wave velocity** | 2700 | 2400–3200 | m/s |
| **Resistivity (matrix)** | 10⁶ | 10⁵–10⁸ | Ω·m |
| **Porosity (total)** | 0.25 | 0.15–0.35 | fraction |
| **Permeability** | 500 | 100–5000 | mD |

### Log Responses

| Log | Clean Sand | Shale | Separation |
|-----|------------|-------|------------|
| **GR** | 30–50 API | 100–150 API | High contrast |
| **RHOB** | 2.15–2.35 | 2.40–2.70 | 0.2–0.4 g/cc |
| **NPHI** | 0.20–0.35 | 0.25–0.45 | Crossover in gas |
| **DT** | 70–90 μs/ft | 90–140 μs/ft | Clear separation |
| **RT** | 10–1000 | 1–10 | High resistivity |

### Forward Models

**Density Porosity:**
```
φ_D = (ρma - ρb) / (ρma - ρf)
Where: ρma = 2.65 (quartz), ρf = 1.0 (fresh water)
```

**Neutron Porosity:**
```
φ_N ≈ φ × HI
Where: HI = 1.0 (water), ~0.3 (oil), ~0.0 (gas)
```

**Acoustic Velocity (Wyllie):**
```
1/Δt = (1-φ)/Δtma + φ/Δtf
Where: Δtma = 55.5 μs/ft (quartz)
```

**Archie Saturation (clean):**
```
Sw = (a × Rw / (φ^m × Rt))^(1/n)
Where: a=0.81, m=2.0, n=2.0 (typical)
```

---

## Representative Material: `SHALE_ILL`

### Description
Illitic shale — the most common seal rock. Fine-grained with illite clay mineralogy.

### Canonical 9 Values (Reference)

| Property | Value | Range | Unit |
|----------|-------|-------|------|
| **Density** | 2.55 | 2.45–2.70 | g/cm³ |
| **P-wave velocity** | 3000 | 2500–4000 | m/s |
| **Resistivity** | 2–10 | 1–50 | Ω·m |
| **Porosity** | 0.10 | 0.05–0.20 | fraction |
| **Permeability** | <0.001 | — | mD |

### Log Character
- **High GR:** 100–150 API (illite K content)
- **High DT:** 90–140 μs/ft (slow, low velocity)
- **High NPHI:** 0.25–0.45 (bound water)
- **High RHOB:** 2.40–2.70 g/cc

### Shale Volume (Vsh) Calculation

**From GR:**
```
Vsh_GR = (GRlog - GRmin) / (GRmax - GRmin)
```

**Larionov (older rocks):**
```
Vsh = 0.33 × (2^(2 × IGR) - 1)
Where: IGR = Vsh_GR
```

**Steiber (Tertiary):**
```
Vsh = 0.5 × IGR / (1.5 - IGR)
```

---

## Diagenetic Effects

### Porosity Destruction

| Process | Effect on φ | Effect on k |
|---------|-------------|-------------|
| **Compaction** | Decrease | Decrease |
| **Cementation (quartz)** | Decrease | Severe decrease |
| **Cementation (calcite)** | Decrease | Severe decrease |
| **Clay authigenesis** | Decrease | Severe decrease |

### Porosity Preservation

| Factor | Mechanism |
|--------|-----------|
| **Early hydrocarbon emplacement** | Prevents cementation |
| **Overpressure** | Reduces effective stress |
| **Grain coating (chlorite)** | Prevents quartz overgrowth |
| **Deep burial** | Compaction before cementation |

---

## Reservoir Quality Index (RQI)

For clastic reservoirs:

```
RQI = 0.0314 × √(k/φ)
Where: k in mD, φ as fraction
```

| RQI (μm) | Quality |
|----------|---------|
| >2.0 | Excellent |
| 1.0–2.0 | Good |
| 0.5–1.0 | Fair |
| <0.5 | Poor |

---

## Flow Zone Indicator (FZI)

```
FZI = RQI / (φz/(1-φz))
Where: φz = normalized porosity
```

Hydraulic units group similar FZI values.

---

## Constitutional Notes

### F2 Truth (τ ≥ 0.99)
- Lab measurements required for calibration
- Regional transforms must be validated
- "Typical" values are DERIVED, not OBSERVED

### F4 Clarity (ΔS ≤ 0)
- Clay type must be specified (illite ≠ smectite)
- Porosity type explicit (total vs effective)
- Diagenetic history acknowledged

### F7 Humility (Ω₀ ∈ [0.03, 0.15])
- Reference values have uncertainty bands
- Local calibration may shift ranges ±20%
- No single "correct" value

---

## Related Pages

- [[30_MATERIALS/RATLAS_Index]] — Complete 99-material catalog
- [[20_PHYSICS/EARTH_CANON_9]] — Physics foundation
- [[20_PHYSICS/Porosity_Types]] — φt vs φe distinction
- [[40_BASINS/Malay_Basin]] — Clastic reservoir example

---

*Sedimentary Clastics — The foundation of conventional reservoirs*  
*Clean sand: high quality. Shale: perfect seal. The dichotomy that traps hydrocarbons.*
