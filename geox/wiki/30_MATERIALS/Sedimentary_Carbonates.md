: "# Sedimentary Carbonates — RATLAS Material Family

> **Type:** Material  
> **Epistemic Level:** DER (derived from lab & well measurements)  
> **Confidence:** 0.92  
> **Certainty Band:** [0.87, 0.96]  
> **Tags:** [ratlas, materials, sedimentary, carbonates, limestone, dolomite]  
> **Sources:** [DSDP Leg 95, Luconia core data, laboratory measurements]  
> **arifos_floor:** F2, F4  

---

## Family Overview

**RATLAS Family Code:** `SED_CARBONATE`  
**Materials in Family:** 15  
**Main Types:** Limestone, dolomite, chalk, marl  
**Porosity Range:** 0.05 – 0.35 (highly variable by diagenesis)  
**Formation Environment:** Shallow marine to deepwater  

**Note:** Carbonate properties are highly sensitive to diagenetic history. Fresh limestone can have 40%+ porosity; deeply buried dolomite may have <5%.

---

## Material Matrix

| Symbol | Name | Mineralogy | Φ typical | Permeability | Reservoir Quality |
|--------|------|------------|-----------|--------------|-------------------|
| `LST_FRESH` | Fresh Limestone | Calcite | 0.25–0.40 | Low-Mod | Good–Excellent |
| `LST_CHALK` | Chalk | Calcite (micrite) | 0.20–0.45 | Very Low | Fair (fractured) |
| `LST_MIC` | Micritic Limestone | Calcite (micrite) | 0.05–0.15 | Negligible | Seal |
| `LST_OO` | Oolitic Limestone | Calcite (ooids) | 0.15–0.30 | Mod-High | Excellent |
| `LST_PEL` | Peloidal Limestone | Calcite (peloids) | 0.15–0.25 | Moderate | Good |
| `LST_BIO` | Bioclastic Limestone | Calcite (fossils) | 0.10–0.30 | Variable | Fair–Good |
| `LST_REC` | Recrystallized Limestone | Calcite (sparry) | 0.05–0.20 | Low | Poor–Fair |
| `DOL_PRIMARY` | Primary Dolomite | Dolomite | 0.15–0.30 | Mod-High | Good–Excellent |
| `DOL_SECOND` | Secondary Dolomite | Dolomite (replacive) | 0.10–0.35 | Moderate | Fair–Good |
| `DOL_DENSE` | Dense Dolomite | Dolomite | 0.02–0.08 | Negligible | Seal |
| `MARL_CALC` | Calcareous Marl | Calcite + Clay | 0.15–0.30 | Low | Fair |
| `MARL_DOL` | Dolomitic Marl | Dolomite + Clay | 0.10–0.25 | Low | Poor–Fair |
| `LST_DOL_VUG` | Vuggy Dolomitized Limestone | Dolomite + Vugs | 0.10–0.40 | High | Excellent |
| `LST_SIL` | Silicified Limestone | Calcite + Quartz | 0.05–0.15 | Low | Poor |
| `LST_ARG` | Argillaceous Limestone | Calcite + Clay | 0.08–0.20 | Very Low | Poor |

---

## Representative Material: `DOL_SECOND`

### Description

Secondary (replacive) dolomite formed by dolomitization of precursor limestone. Common in Luconia Province reservoirs.

### Physical Properties

| Property | Value | Unit | Confidence |
|----------|-------|------|------------|
| **Porosity (φ)** | 0.15–0.30 | fraction | 0.88 |
| **Permeability (k)** | 1–100 | mD | 0.75 |
| **Grain Density (ρg)** | 2.80–2.87 | g/cm³ | 0.95 |
| **Bulk Density (ρb)** | 2.20–2.55 | g/cm³ | 0.80 |
| **P-wave Velocity (Vp)** | 4500–6500 | m/s | 0.82 |
| **S-wave Velocity (Vs)** | 2500–3500 | m/s | 0.78 |
| **Acoustic Impedance (Z)** | 9.9–16.6 | kg/m²·s ×10⁶ | 0.80 |
| **Poisson's Ratio (ν)** | 0.25–0.32 | — | 0.75 |

### Seismic Response

| Attribute | Value |
|-----------|-------|
| **Acoustic Impedance** | High (10–17 ×10⁶ kg/m²·s) |
| **Reflection Coefficient vs. Shale** | +0.15 to +0.35 |
| **AVO Class** | Class I (high impedance, decreasing amplitude with offset) |
| **Frequency Content** | Often higher than clastics (less attenuation) |

### Log Response

| Log | Response | Value Range |
|-----|----------|-------------|
| **GR** | Low | 10–40 API |
| **Density (RHOB)** | High | 2.30–2.75 g/cm³ |
| **Neutron (NPHI)** | Low | 0.00–0.15 (dolomite effect) |
| **Sonic (DT)** | Fast | 50–70 μs/ft |
| **PEF** | High | 3.0–5.0 b/e |
| **Resistivity** | Very High | 100–10,000 Ω·m |

### Geological Context

| Aspect | Detail |
|--------|--------|
| **Environment** | Shallow marine shelf, evaporitic |
| **Diagenesis** | Early to burial dolomitization |
| **Age** | Miocene (Luconia), Jurassic (Arab D) |
| **Analogs** | Luconia Province, Malaysia; Arab Formation, Middle East |

---

## Porosity-Permeability Relationships

### Carbonate Porosity Types

| Porosity Type | Origin | Connectivity | Permeability Impact |
|---------------|--------|--------------|---------------------|
| **Interparticle** | Between grains | High | Good permeability |
| **Intraparticle** | Within grains (fossil chambers) | Moderate | Fair permeability |
| **Moldic** | Dissolved grains | Variable | Can be excellent |
| **Vuggy** | Large dissolution cavities | Variable | Often excellent |
| **Fracture** | Tectonic/diagenetic | Very High | Dominates flow |
| **Microporosity** | Micrite matrix | Low | Often poor |

### Winland r35 Method

For carbonates, use r35 (radius at 35% mercury saturation):

```
log(r35) = 0.732 + 0.588·log(k) - 0.864·log(φ)

Where:
- r35 = pore throat radius at 35% Hg saturation (microns)
- k = permeability (mD)
- φ = porosity (fraction)

Reservoir Quality Index (RQI):
- r35 > 2.0 μm: Excellent reservoir
- r35 0.5–2.0 μm: Good reservoir
- r35 0.1–0.5 μm: Fair reservoir
- r35 < 0.1 μm: Poor reservoir
```

---

## Diagenetic Controls

### Porosity Evolution

```
┌──────────────────────────────────────────────────────────────┐
│                    CARBONATE POROSITY EVOLUTION              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Time ──►                                                    │
│                                                               │
│  40% ┤ ████  Initial marine porosity (unconsolidated)       │
│      │   ↓                                                   │
│  30% ┤ ███   Early cementation (marine hardgrounds)         │
│      │   ↓                                                   │
│  25% ┤ ██    Shallow burial (mechanical compaction)          │
│      │   ↓                                                   │
│  15% ┤ █     Deep burial (chemical compaction, stylolites)   │
│      │   ↓                                                   │
│  10% ┤ █     Dolomitization (can increase or decrease)       │
│      │   ↓                                                   │
│   5% ┤ ░     Extensive cementation (barrier)                 │
│      │                                                       │
│   0% ┼──────┬────────┬────────┬────────┬────────┬────────►   │
│      0m   500m    1000m    2000m    3000m    4000m Depth    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## RATLAS Lookup Table

| Code | Φ_min | Φ_max | k_min | k_max | Vp_min | Vp_max | Use Case |
|------|-------|-------|-------|-------|--------|--------|----------|
| LST_FRESH | 0.25 | 0.40 | 0.1 | 100 | 3500 | 5000 | Near-surface reservoir |
| LST_CHALK | 0.20 | 0.45 | 0.01 | 10 | 2000 | 3500 | Chalk reservoirs (Ekofisk) |
| DOL_SECOND | 0.10 | 0.35 | 1 | 500 | 4500 | 6500 | Luconia platforms |
| LST_DOL_VUG | 0.10 | 0.40 | 10 | 10000 | 5000 | 6500 | Karst reservoirs |

---

## Cross-References

- Clastic comparison: [[30_MATERIALS/Sedimentary_Clastics]]
- Basin context: [[40_BASINS/Sarawak_Basin#Luconia Carbonate Platform]]
- Physics: [[20_PHYSICS/Acoustic_Impedance]]
- Tools: [[50_TOOLS/geox_query_ratlas]]

---

*RATLAS Sedimentary Carbonates v1.0.0 · Part of [[30_MATERIALS/RATLAS_Index]]*