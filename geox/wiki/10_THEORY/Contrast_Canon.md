# Contrast Canon — Physical vs Display vs Perceptual

> **Type:** Theory  
> **Epistemic Level:** DER (derived from perceptual psychology)  
> **Confidence:** 0.94  
> **Certainty Band:** [0.88, 0.98]  
> **Tags:** [contrast, perception, display, physics, domains]  
> **Sources:** [[raw/papers/bond_2007.pdf]], [[10_THEORY/Theory_of_Anomalous_Contrast]]  
> **arifos_floor:** F4, F9  

---

## The Three Domains

The Contrast Canon formalizes the separation between:

| Domain | What It Is | What Can Go Wrong |
|--------|-----------|-------------------|
| **Physical** | Actual Earth properties | Measurement error, noise |
| **Display** | Visualization transforms | Artifacts, distortions |
| **Perceptual** | Human visual processing | Illusions, bias, pattern completion |

---

## Domain Separation Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONTRAST DOMAIN MATRIX                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PHYSICAL              DISPLAY               PERCEPTUAL                    │
│   ─────────            ────────              ──────────                     │
│                                                                             │
│   Impedance contrast    Colormap choice       Edge detection                │
│   │                     │                     │                             │
│   ▼                     ▼                     ▼                             │
│   Waveform similarity   Dynamic range         Pattern recognition           │
│   │                     │                     │                             │
│   ▼                     ▼                     ▼                             │
│   Geological truth      Filter kernels        Gestalt completion            │
│   │                     │                     │                             │
│   ▼                     ▼                     ▼                             │
│   [SENSOR] ────────►  [PROCESSING] ───────► [HUMAN]                        │
│       │                    │                    │                          │
│       └────────────────────┴────────────────────┘                          │
│                         │                                                   │
│                         ▼                                                   │
│              ⚠️ ANOMALOUS CONTRAST ⚠️                                       │
│      When DISPLAY artifacts are mistaken for PHYSICAL signal               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Physical Domain

### Definition
Properties of the actual Earth that exist independent of observation.

### Examples
| Property | Unit | Measurement |
|----------|------|-------------|
| Acoustic Impedance | kg/(m²·s) | Requires source + receiver |
| Density | kg/m³ | Core, log, or seismic inversion |
| Velocity | m/s | Sonic log, VSP, checkshot |
| Porosity | fraction | Neutron, density, NMR |

### Key Principle
**Physical properties exist whether or not anyone looks at them.**

---

## Display Domain

### Definition
Transformations applied to data for visualization.

### Common Transforms
| Transform | Purpose | Risk |
|-----------|---------|------|
| **Colormap** | Encode amplitude as color | Diverging colormaps create false boundaries |
| **AGC (Automatic Gain Control)** | Normalize amplitude | Creates false continuity |
| **Gamma correction** | Adjust brightness | Distorts amplitude relationships |
| **Filtering** | Remove noise | Removes signal if misapplied |
| **Vertical exaggeration** | Enhance visual dip | Creates structural illusions |
| **CLAHE** | Local contrast enhancement | Creates "faults" that are just edges |

### Key Principle
**Every display choice is a decision that can obscure or distort physical reality.**

### F4 Clarity Requirement
Every display transform must be documented:
```yaml
display_transforms:
  - type: AGC
    window_ms: 500
    operator: rms
  - type: colormap
    name: seismic
    reversal: false
  - type: vertical_exaggeration
    ratio: 2.0
    declared: true  # F4: Must be explicit
```

---

## Perceptual Domain

### Definition
How the human visual system interprets displayed information.

### Known Perceptual Biases
| Bias | Effect | Mitigation |
|------|--------|------------|
| **Pattern completion** | Brain fills in gaps | Multi-model candidates (ToAC Rule 1) |
| **Confirmation bias** | See what you expect | Bias audit before seal (ToAC Rule 3) |
| **Scale insensitivity** | Miss scale changes | F4: Scale explicit or "UNKNOWN" |
| **Color constancy** | Ignore colormap effects | Physical attributes first (ToAC Rule 2) |

### Bond et al. (2007) Findings
- 79% of experienced interpreters failed on synthetic seismic
- **Not** because data was poor
- **Because** display artifacts created perceptual illusions
- Experts interpreted artifacts as geology

### Key Principle
**The human visual system evolved for survival, not seismic interpretation.**

---

## Anomalous Contrast Detection

### Warning Signs (Auto-HOLD Triggers)

| Condition | Risk | Action |
|-----------|------|--------|
| Interpretation based solely on "visual appearance" | High | 888_HOLD — require physical attributes |
| Undisclosed vertical exaggeration > 2x | High | 888_HOLD — F4 violation |
| AGC without window documentation | Medium | QUALIFY with caveats |
| Single colormap interpretation | Medium | Require multi-view confirmation |
| No coherence/curvature backup | Medium | Request attribute validation |

### The Anomalous Contrast Formula

```
Anomalous Risk = f(Display_Artifacts, Perceptual_Bias, Physical_Uncertainty)

Where:
- Display_Artifacts ∈ [0, 1] — measured transform risk
- Perceptual_Bias ∈ [0, 1] — known cognitive bias presence
- Physical_Uncertainty ∈ [0, 1] — Ω₀ from F7 Humility

If Anomalous Risk > 0.5:
    Trigger 888_HOLD
Else if Anomalous Risk > 0.25:
    QUALIFY with explicit caveats
Else:
    PROCEED with standard confidence band
```

---

## Cross-Domain Verification

### Required Checks Before SEAL

1. **Physical verification** — Can this be forward modeled?
2. **Display audit** — What transforms were applied?
3. **Perceptual check** — Is this pattern-completion or real?

### Example Workflow

```
Seismic Line Loaded
    │
    ▼
Physical attributes computed (coherence, dip, curvature)
    │
    ▼
Multi-contrast views generated (different colormaps, gains)
    │
    ▼
Perceptual consistency check (do features persist across views?)
    │
    ▼
Anomalous Risk calculated
    │
    ├── Risk > 0.5 ──► 888_HOLD
    ├── Risk > 0.25 ─► QUALIFY
    └── Risk < 0.25 ─► SEAL (with confidence band)
```

---

## Constitutional Enforcement

| Floor | Contrast Canon Implementation |
|-------|------------------------------|
| **F2 Truth** | Physical signal explicitly declared |
| **F4 Clarity** | All display transforms documented |
| **F7 Humility** | Perceptual uncertainty quantified |
| **F9 Anti-Hantu** | DISPLAY-ONLY → automatic HOLD |
| **F11 Audit** | Transform chain logged to 999_VAULT |

---

## Related Pages

- [[10_THEORY/Theory_of_Anomalous_Contrast]] — Core ToAC theory
- [[10_THEORY/Conflation_Taxonomy]] — Source→Transform→Proxy→Confidence
- [[10_THEORY/Bond_2007_Cognitive_Bias]] — Empirical evidence
- [[10_THEORY/Epistemic_Levels]] — OBS/DER/INT/SPEC classification

---

*Contrast Canon — Separation of concerns for geoscience interpretation*  
*Physical ≠ Display ≠ Perceptual*
