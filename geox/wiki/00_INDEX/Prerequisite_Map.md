# GEOX Prerequisite Map

> **Type:** Index  
> **Purpose:** Dependency graph for wiki navigation  

---

## Graph Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GEOX KNOWLEDGE GRAPH                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ENTRY POINTS                                                               │
│  ────────────                                                               │
│  [[00_INDEX/Quickstart]]                                                    │
│       │                                                                     │
│       ├──► [[00_INDEX/LLM_LEM_Manifesto]] ──► Foundation philosophy        │
│       │                                                                     │
│       └──► [[10_THEORY/Theory_of_Anomalous_Contrast]] ◄──┐                 │
│              │                                           │                 │
│              ▼                                           │                 │
│  CORE THEORY         PHYSICS         MATERIALS           │                 │
│  ───────────         ───────         ─────────           │                 │
│  [[10_THEORY/]]      [[20_PHYSICS/]] [[30_MATERIALS/]]   │                 │
│       │                  │                │              │                 │
│       │                  ▼                ▼              │                 │
│       │           [[EARTH_CANON_9]] [[RATLAS_Index]]     │                 │
│       │                  │                │              │                 │
│       │                  └────────┬───────┘              │                 │
│       │                           ▼                      │                 │
│       └────────────────► [[50_TOOLS/]] ──► Application   │                 │
│                               │                          │                 │
│                               ▼                          │                 │
│                         [[60_CASES/]] ──► Real examples  │                 │
│                               │                          │                 │
│                               ▼                          │                 │
│  GOVERNANCE ◄─────────────────┘                          │                 │
│  [[70_GOVERNANCE/]]                                      │                 │
│       │                                                  │                 │
│       └──► 888_HOLD, Floor Enforcement, Confidence       │                 │
│              │                                           │                 │
│              ▼                                           │                 │
│       [[arifos::Floors]] ◄───────────────────────────────┘                 │
│       [[arifos::888_JUDGE]]                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Learning Paths

### Path 1: The Theorist
For understanding the core principles:

1. [[00_INDEX/LLM_LEM_Manifesto]] — Intelligence stack
2. [[10_THEORY/Theory_of_Anomalous_Contrast]] — Core theory
3. [[10_THEORY/Contrast_Canon]] — Domain separation
4. [[10_THEORY/Bond_2007_Cognitive_Bias]] — Empirical foundation
5. [[20_PHYSICS/EARTH_CANON_9]] — Physics completeness

### Path 2: The Practitioner
For using GEOX tools:

1. [[00_INDEX/Quickstart]] — Getting started
2. [[50_TOOLS/geox_load_seismic_line]] — Load data
3. [[50_TOOLS/geox_build_structural_candidates]] — Generate hypotheses
4. [[60_CASES/Structural_Interpretation_Workflow]] — Workflow example
5. [[70_GOVERNANCE/888_HOLD_Registry]] — Understand gates

### Path 3: The Integrator
For arifOS federation:

1. [[arifos::What-is-arifOS]] — Constitutional framework
2. [[00_INDEX/LLM_LEM_Manifesto]] — Stack positioning
3. [[80_INTEGRATION/Trinity_Architecture]] — ΔΩΨ mapping
4. [[80_INTEGRATION/VAULT999_Wiring]] — Audit integration
5. [[arifos::Floors]] — Constitutional enforcement

---

## Page Dependencies

| Page | Prerequisites | Leads To |
|------|--------------|----------|
| [[Theory_of_Anomalous_Contrast]] | — | Conflation_Taxonomy, Bond_2007 |
| [[EARTH_CANON_9]] | — | Acoustic_Impedance, Porosity_Types |
| [[RATLAS_Index]] | EARTH_CANON_9 | Material family pages |
| [[geox_evaluate_prospect]] | ToAC, RATLAS | 888_HOLD_Registry |
| [[888_HOLD_Registry]] | geox_evaluate_prospect | arifos::888_JUDGE |

---

*Navigate the knowledge graph.*
