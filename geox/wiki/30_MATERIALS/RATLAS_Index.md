# RATLAS — Reference Atlas of Earth Materials

> **Type:** Material Index  
> **Epistemic Level:** DER (derived from lab measurements)  
> **Confidence:** 0.95  
> **Tags:** [ratlas, materials, physics, reference, atlas]  
> **Sources:** [GFZ Potsdam, DSDP Leg 78B, SDSU EM Geo]  
> **arifos_floor:** F2  

---

## Overview

**RATLAS** is GEOX's **material intelligence layer** — a physics-backed reference atlas of **99 canonical Earth material states** across **11 families**.

**Purpose:** Provide symbolic grounding for AI geoscience reasoning.

**Not a classifier.** RATLAS provides reference physics — actual formation evaluation requires calibrated field data.

---

## The 11 Material Families

| Family | Count | Description |
|--------|-------|-------------|
| **Sedimentary Clastic** | 18 | Sandstone, shale, siltstone |
| **Sedimentary Carbonate** | 9 | Limestone, dolomite, evaporites |
| **Sedimentary Chemical** | 9 | Chert, coal, organic |
| **Igneous Felsic** | 9 | Granite, rhyolite, syenite |
| **Igneous Intermediate/Mafic** | 9 | Diorite, gabbro, basalt |
| **Igneous Ultramafic/Altered** | 9 | Peridotite, serpentinite |
| **Metamorphic Foliated** | 9 | Schist, gneiss, slate |
| **Metamorphic Non-Foliated** | 9 | Quartzite, marble, hornfels |
| **Unconsolidated/Soil** | 9 | Gravel, sand, clay, loam |
| **Engineered Materials** | 9 | Steel, concrete, drilling mud |

---

## Symbolic Token Vocabulary

RATLAS drives the GEOX reasoning engine through symbolic tokens:

### Sedimentary
- `SAND_QZ_CLEAN` — Clean quartz sandstone
- `SAND_QZ_FELD` — Feldspathic sandstone
- `SHALE_ILL` — Illitic shale
- `SHALE_SME` — Smectitic shale
- `LIMESTONE_CC` — Calcitic limestone
- `DOLOMITE_DOL` — Dolomite
- `ANHYDRITE` — Anhydrite
- `HALITE` — Halite (rock salt)
- `CHERT_SIL` — Chert
- `COAL_LIG` — Lignite

### Igneous
- `GRANITE_K` — Potassic granite
- `BASALT_MAF` — Mafic basalt
- `PERIDOTITE_OL` — Olivine peridotite
- `SERPENTINE` — Serpentinite

### Metamorphic
- `SCHIST_BT` — Biotite schist
- `GNEISS_OR` — Orthogneiss

### Engineered
- `STEEL_Fe` — Steel casing
- `CONCRETE_RF` — Reinforced concrete
- `DRILLING_MUD` — Synthetic drilling fluid

---

## Forward Models

Each material includes forward models for log responses:

```
ρb = (1−φ)·ρm + φ·ρf           # Bulk density mixing law
NPHI ≈ φ·Σ(Si·HIi)             # Neutron hydrogen index
Rt = a·Rw / (φm·Swⁿ)            # Archie resistivity (clean)
Vsh = (GRlog − GRmin) / (GRmax − GRmin)  # Gamma ray index
```

---

## Constitutional Alignment

| Floor | RATLAS Implementation |
|-------|----------------------|
| **F1** | Reversibility — all reference values revisable |
| **F2** | Truth — lab measurement provenance required |
| **F4** | Clarity — units and conditions explicit |
| **F7** | Humility — uncertainty bands on all values |
| **F9** | Anti-Hantu — no anthropomorphization of materials |
| **F13** | Sovereign — human override on material calls |

---

## Access Points

| Format | URL/Path |
|--------|----------|
| **Live GUI** | https://aaa.arif-fazil.com/geox/geox_ratlas.html |
| **CSV** | https://aaa.arif-fazil.com/geox/geox_atlas_99_materials.csv |
| **Wiki** | This page + linked family pages |

---

## Family Pages

Detailed physics for each family:

- [[30_MATERIALS/Sedimentary_Clastics]] — 18 clastic materials
- [[30_MATERIALS/Sedimentary_Carbonates]] — 9 carbonate materials
- [[30_MATERIALS/Igneous_Felsic]] — 9 felsic igneous
- [[30_MATERIALS/Igneous_Mafic]] — 9 mafic igneous
- ... (additional families)

---

## Quote

> *"Anak Nusantara, bukan software Barat. Real data, physics law, constitutional verification."*

---

*RATLAS — Material Intelligence for Constitutional Earth Models*
