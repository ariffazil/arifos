# Theory of Anomalous Contrast (ToAC)

> **Type:** Theory  
> **Epistemic Level:** DER (derived from empirical studies)  
> **Confidence:** 0.97  
> **Certainty Band:** [0.92, 0.99]  
> **Tags:** [contrast, perception, bias, seismic, theory]  
> **Sources:** [[raw/papers/bond_2007.pdf]]  
> **arifos_floor:** F9  

---

## The Core Thesis

> **Anomalous Contrast** is the systematic error that occurs when **visual/display contrast** (how something looks) is conflated with **physical contrast** (what the signal actually represents).

This is the "79% problem" from [[Bond_2007_Cognitive_Bias]] — experts failing not because of data quality, but because:

1. **Display choices** (colormap, gain, filtering) create perceptual artifacts
2. These artifacts are mistaken for **geological signal**
3. Interpretation proceeds without awareness of the **conflation error**

---

## The Three Domains of Contrast

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THEORY OF ANOMALOUS CONTRAST                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHYSICAL DOMAIN          DISPLAY DOMAIN          PERCEPTUAL DOMAIN        │
│  ───────────────          ─────────────          ────────────────         │
│                                                                             │
│  • Impedance contrast     • Colormap choice      • What human             │
│  • Waveform similarity    • Dynamic range          sees                   │
│  • Discontinuity          • Gamma correction      • Pattern               │
│  • Geological truth       • Filter kernels          recognition           │
│                                                                             │
│  ════════════════         ══════════════         ═══════════════          │
│       TRUTH                  DISPLAY                PERCEPTION            │
│   (Earth Physics)         (Visualization)         (Human Vision)          │
│                                                                             │
│                           ⚠️ ANOMALOUS CONTRAST ⚠️                          │
│              When Display → Perception is mistaken for                    │
│                      Physical → Truth                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Domain Definitions

| Domain | Description | Examples |
|--------|-------------|----------|
| **Physical** | Actual Earth properties | Impedance, velocity, density |
| **Display** | Visualization transforms | Colormap, gain, gamma, filters |
| **Perceptual** | Human visual processing | Edge detection, pattern recognition |

---

## Known Failure Modes (Automatic GEOX_BLOCK)

| Artifact | Description | Risk |
|----------|-------------|------|
| **Polarity convention error** | Wrong impedance assumption | Misidentified fluid contacts |
| **AGC gain distortion** | Automatic gain control artifacts | False amplitude anomalies |
| **Migration smile** | Processing artifacts from migration | Phantom structures |
| **Display stretch** | Vertical exaggeration | Misinterpreted dip angles |

---

## The Contrast Canon

Three rules to prevent anomalous contrast:

### Rule 1: Multi-Model Candidates (Non-Uniqueness Principle)

> **Never collapse to a single inverse solution prematurely.**

Maintain a ranked ensemble of structural hypotheses. The Earth is underdetermined — multiple models can explain the same data.

**GEOX enforcement:** `geox_build_structural_candidates` returns minimum 3 candidates with confidence scores. Collapse to single model triggers F7 violation.

### Rule 2: Physical Attributes First

> **All visual interpretation must be anchored in deterministic physics.**

- Coherence
- Dip-azimuth
- Curvature
- Spectral decomposition

**F9 Anti-Hantu violation:** Interpretation from aesthetics alone triggers automatic 888_HOLD.

### Rule 3: Bias Audit Before Seal

> **Run an explicit professional bias check before `geox_evaluate_prospect` seals the verdict.**

Reference: Bond et al. (2007) on cognitive bias in seismic interpretation.

**GEOX enforcement:** Bias audit step mandatory in prospect evaluation workflow.

---

## Universal Applicability

ToAC applies across domains:

| Domain | Physical Signal | Display Artifact | Anomalous Risk |
|--------|-----------------|------------------|----------------|
| **Seismic** | Impedance contrast | CLAHE edge enhancement | Faults that are just display edges |
| **Medical** | Tissue density | Window/level settings | Tumors that are just contrast bands |
| **Satellite** | Surface reflectance | Color stretching | Features that are histogram artifacts |
| **Radar** | Backscatter | MTF enhancement | Targets that are processing artifacts |

**Key insight:** Seismic is ONE domain. The Theory is UNIVERSAL.

---

## Taxonomy: Source → Transform → Proxy → Confidence

Every contrast operation traces through four stages:

```
┌─────────┐    ┌───────────┐    ┌────────┐    ┌─────────────┐
│ SOURCE  │───►│ TRANSFORM │───►│ PROXY  │───►│ CONFIDENCE  │
└─────────┘    └───────────┘    └────────┘    └─────────────┘
     │               │              │               │
     ▼               ▼              ▼               ▼
Raw data       Display op      Visual feature   Uncertainty
(impedance)    (colormap)      (edge)           (Ω₀)
```

### Stage Definitions

| Stage | Question | Example |
|-------|----------|---------|
| **Source** | What physical signal? | Acoustic impedance contrast |
| **Transform** | What display operations? | Seismic colormap, AGC gain |
| **Proxy** | What visual feature? | Bright reflector, discontinuity |
| **Confidence** | How certain? | Ω₀ = 0.08 (F7 Humility band) |

---

## Constitutional Enforcement

| Floor | ToAC Implementation |
|-------|---------------------|
| **F1 Amanah** | Every contrast transformation reversible (provenance chain) |
| **F2 Truth** | Physical axes explicitly declared and verified |
| **F4 Clarity** | Visual transforms documented separately from physical signal |
| **F7 Humility** | Confidence capped at 0.15 when conflation risk detected |
| **F9 Anti-Hantu** | DISPLAY-ONLY inputs trigger automatic 888_HOLD |
| **F13 Sovereign** | Human override required for >2 valid alternatives |

---

## References

- **Bond, C.E., Gibbs, A.D., Shipton, Z.K., Jones, S. (2007).** "What do you think this is? 'Conceptual uncertainty' in geoscience interpretation." *GSA Today*, 17(11), 4–10. [[raw/papers/bond_2007.pdf]]

---

## Related Pages

- [[10_THEORY/Contrast_Canon]] — Detailed domain separation
- [[10_THEORY/Conflation_Taxonomy]] — Source→Transform→Proxy→Confidence
- [[10_THEORY/Bond_2007_Cognitive_Bias]] — Empirical foundation
- [[50_TOOLS/geox_build_structural_candidates]] — Multi-model enforcement

---

*Theory of Anomalous Contrast — GEOX Core Doctrine*  
*Visual contrast ≠ Physical reality*
