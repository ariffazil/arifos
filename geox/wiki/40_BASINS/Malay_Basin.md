# Malay Basin — Regional Geoscience Profile

> **Type:** Basin  
> **Epistemic Level:** INT (interpreted from multiple sources)  
> **Confidence:** 0.88  
> **Certainty Band:** [0.80, 0.94]  
> **Tags:** [basin, malay, southeast_asia, tertiary, clastics]  
> **Sources:** [PETRONAS, Murphy Oil, academic literature]  
> **arifos_floor:** F4, F7  

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Location** | Offshore Peninsular Malaysia, South China Sea |
| **Coordinates** | 3°–7°N, 102°–106°E |
| **Basin Type** | Extensional (Tertiary rift) |
| **Age** | Eocene to Recent |
| **Water Depth** | 50–100 m (shallow), 100–200 m (deep) |
| **Area** | ~80,000 km² |

---

## Tectonic Setting

### Evolution

| Phase | Age | Event | Structural Style |
|-------|-----|-------|------------------|
| **Pre-rift** | Pre-Eocene | Basement formation | Granitic/metamorphic |
| **Syn-rift** | Eocene-Oligocene | Extension, graben formation | N-S trending half-grabens |
| **Post-rift** | Miocene-Pliocene | Thermal subsidence | Draping, minor faulting |
| **Compression** | Late Miocene | Regional inversion | Reverse reactivation |

### Key Structural Features

| Feature | Orientation | Significance |
|---------|-------------|--------------|
| **North Malay Basin** | N-S | Deepest depocenter, main petroleum system |
| **Tenggol Arch** | E-W | Southern boundary, erosion |
| **Pattani Trough** | N-S | Northern extension into Thailand |
| **East Coast Fault** | NNE-SSW | Western boundary |

---

## Stratigraphy

### Simplified Stratigraphic Column

```
Age          Group          Lithology                    Reservoir/Seal
────         ─────          ─────────                    ─────────────
Recent       Muda           Shallow marine sand          Minor
Pleistocene  
Miocene-     Belum          Deep marine shale            Regional seal
Pliocene     

Miocene      Group M        Fluvial-deltaic sandstone    Primary reservoir
             (upper)        Interbedded shale            Local seal

Miocene      Group M        Marginal marine sandstone    Secondary reservoir
             (lower)        Shale, coal                  Source + seal

Oligocene    Group K        Fluvial-lacustrine           Secondary reservoir
                            Sandstone, shale, coal       Source rock

Eocene       Basement       Granite, metamorphic         —
```

### Key Reservoirs

| Group | Age | Lithology | Φ (%) | k (mD) | Quality |
|-------|-----|-----------|-------|--------|---------|
| **Group M (upper)** | Miocene | Fluvial-deltaic sand | 20–30 | 100–2000 | Excellent |
| **Group M (lower)** | Miocene | Marginal marine sand | 15–25 | 50–500 | Good |
| **Group K** | Oligocene | Fluvial sand | 15–22 | 10–200 | Fair-Good |

### Seal Rocks

| Group | Age | Lithology | Thickness | Quality |
|-------|-----|-----------|-----------|---------|
| **Belum** | Mio-Pliocene | Deep marine shale | 200–500m | Regional |
| **Group M (intra)** | Miocene | Marine shale | 20–100m | Local |

### Source Rocks

| Group | Age | Type | TOC (%) | Kerogen | Maturity |
|-------|-----|------|---------|---------|----------|
| **Group K** | Oligocene | Coal, carbonaceous shale | 2–8 | III (gas-prone) | Mature-Late |
| **Group M (lower)** | Early Miocene | Marine shale | 1–4 | II-III | Mature |

---

## Petroleum System

### Elements

| Element | Status | Quality |
|---------|--------|---------|
| **Source** | ✅ Present | Good (coaly Type III) |
| **Reservoir** | ✅ Present | Excellent (Group M sands) |
| **Seal** | ✅ Present | Excellent (Belum shale) |
| **Trap** | ✅ Present | Structural + stratigraphic |
| **Migration** | ✅ Confirmed | Short-distance, vertical |

### Critical Moment
Late Miocene (10–5 Ma) — Peak generation coincides with trap formation.

### Play Types

| Play | Trap Type | Reservoir | Risk Level |
|------|-----------|-----------|------------|
| **Drape anticlines** | 4-way dip | Group M upper | Low |
| **Fault closures** | 2–3 way | Group M | Low-Med |
| **Inversion structures** | Reverse fault | Group K-M | Medium |
| **Stratigraphic pinchouts** | Facies change | Group M | Med-High |

---

## Production History

### Major Fields

| Field | Discovery | Reserves (MMboe) | Operator |
|-------|-----------|------------------|----------|
| **Dulang** | 1982 | 300+ | PETRONAS |
| **Tiong** | 1983 | 150+ | PETRONAS |
| **Bekok** | 1969 | 500+ | PETRONAS/Exxon |
| **Seligi** | 1983 | 200+ | PETRONAS |
| **Kikeh** | 2002 | 400+ | Murphy Oil |

### Cumulative Production
- **Oil:** >3 billion barrels
- **Gas:** >20 TCF

---

## Regional Analogs

| Analog | Similarity | Key Difference |
|--------|------------|----------------|
| **Gulf of Thailand** | Tertiary rift, coaly source | Higher heat flow, more gas-prone |
| **Mekong Basin** | Tertiary deltaic | Different provenance, younger |
| **Bohai Bay** | Tertiary rift | Lacustrine source, higher maturity |

---

## GEOX Application

### Typical Workflow

```
1. Load seismic (Group M level, ~2s TWT)
   └── F4: WGS84, Malay Basin coordinate system
   
2. Build structural candidates
   └── ToAC: Multi-model (drape vs fault-controlled)
   
3. Feasibility check
   └── F7: Confidence Ω₀ ∈ [0.06, 0.12] (good well control)
   
4. Well log integration
   └── [[30_MATERIALS/Sedimentary_Clastics]] — Group M sands
   
5. Petrophysical analysis
   └── φ = 20–30%, Sw = 20–40%, Net sand >70%
   
6. Prospect evaluation
   └── 888_JUDGE: Usually SEAL (proven play)
       Exception: Stratigraphic traps → HOLD
```

### RATLAS Materials

Primary: [[30_MATERIALS/Sedimentary_Clastics]]
- `SAND_QZ_CLEAN` — Clean Group M sands
- `SAND_ARG` — Argillaceous lower Group M
- `SHALE_ILL` — Belum seal shale

### Key Uncertainties

| Uncertainty | Ω₀ Impact | Mitigation |
|-------------|-----------|------------|
| Depth conversion | ±0.05 | Checkshot, VSP |
| Sand connectivity | ±0.08 | Pressure data, 4D seismic |
| Gas-oil contact | ±0.03 | Monitoring wells |
| Shallow gas | ±0.06 | Seismic hazard analysis |

---

## Constitutional Enforcement

### F2 Truth (τ ≥ 0.99)
- Regional maps from PETRONAS/public sources
- Well data proprietary (confidence <0.99 without well)
- Analog data explicitly labeled as DERIVED/INT

### F4 Clarity (ΔS ≤ 0)
- Datum: MSL
- Coordinate system: WGS84 / UTM 48N
- Depth: Measured, True Vertical, or SS
- Seismic: Two-way time vs depth explicit

### F7 Humility (Ω₀ ∈ [0.03, 0.15])
- Proven play areas: Ω₀ ~0.06
- Frontier areas: Ω₀ ~0.12
- Stratigraphic traps: Ω₀ ~0.15 (approaching HOLD)

### F9 Anti-Hantu (C_dark < 0.30)
- No "analog certainty" without local calibration
- Display artifacts flagged in vintage seismic
- Multi-model candidates for inversion structures

### F13 Sovereign (Human Veto)
- 888_HOLD for: New play types, deep targets, stratigraphic traps
- Human required: All prospect economics

---

## References

### Industry
- PETRONAS. (Various). Malay Basin field development plans.
- Murphy Oil. (2003). Kikeh discovery paper.

### Academic
- Madon, M. (1999). "Basement structure and sedimentary basins of Peninsular Malaysia."
- Morley, C.K. (2013). "Rifting and inversion in the Malay Basin."

---

## Related Pages

- [[30_MATERIALS/Sedimentary_Clastics]] — Primary reservoir types
- [[20_PHYSICS/EARTH_CANON_9]] — Physics foundation
- [[10_THEORY/Theory_of_Anomalous_Contrast]] — Structural interpretation

---

*Malay Basin — The type example of Tertiary rift petroleum systems in SE Asia*  
*Proven play, mature data, excellent GEOX test case.*
