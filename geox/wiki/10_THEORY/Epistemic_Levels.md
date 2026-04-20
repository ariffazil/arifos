# Epistemic Levels — OBS / DER / INT / SPEC

> **Type:** Theory  
> **Epistemic Level:** OBS (observational definition)  
> **Confidence:** 1.0  
> **Tags:** [epistemology, classification, uncertainty, levels, truth]  
> **Sources:** [[raw/papers/earth_science_epistemology.pdf]]  
> **arifos_floor:** F2, F9  

---

## The Four Levels

GEOX enforces explicit classification of all outputs by **how they relate to physical reality**:

| Level | Code | Definition | Certainty | Human Gate |
|-------|------|------------|-----------|------------|
| **Observational** | OBS | Direct sensor measurement | High | No |
| **Derived** | DER | Computed from observations | Medium | No |
| **Interpreted** | INT | Inferred from derived data | Low | Yes |
| **Speculated** | SPEC | Proposed but unverified | Very Low | Required |

---

## Level Definitions

### Level 1: OBSERVATIONAL (OBS)

**Definition:** Raw sensor data. The closest we get to "ground truth" without interpretation.

**Examples:**
- Seismic amplitude traces
- Log curves (GR, RHOB, NPHI, RT)
- Core photographs
- Outcrop measurements
- GPS coordinates

**Characteristics:**
- Calibrated instrument output
- Units declared (F4 Clarity)
- Provenance documented (F11 Audit)
- Still contains noise, but noise is random, not systematic

**GEOX Verdict:** Can auto-SEAL with standard confidence band.

---

### Level 2: DERIVED (DER)

**Definition:** Computed from observational data using defined algorithms.

**Examples:**
- Porosity from density log: `φ = (ρma - ρb) / (ρma - ρf)`
- Acoustic impedance: `I = ρ × Vp`
- Seismic attributes (coherence, curvature)
- Temperature gradients

**Characteristics:**
- Algorithm is reversible (F1 Amanah)
- Assumptions explicit (matrix density, fluid properties)
- Uncertainty propagates from inputs (F7 Humility)
- **Not** the same as observational — depends on model choices

**GEOX Verdict:** Can SEAL with explicit uncertainty band.

---

### Level 3: INTERPRETED (INT)

**Definition:** Inferred from derived data using geological models and professional judgment.

**Examples:**
- Lithology identification (sandstone vs shale)
- Fluid type (oil vs water vs gas)
- Depositional environment
- Structural geometry (fault interpretation)
- Sequence boundaries

**Characteristics:**
- Requires geological training
- Multiple valid interpretations possible (non-uniqueness)
- Biases significant (Bond et al. 2007)
- Often presented as fact when still inference

**GEOX Verdict:** 888_HOLD recommended. Human confirmation required before SEAL.

---

### Level 4: SPECULATED (SPEC)

**Definition:** Proposed but lacking direct or indirect observational support.

**Examples:**
- Prospect resource estimates (OOIP, OGIP)
- Exploration targets in untested areas
- Analog-based predictions
- Long-term production forecasts
- Basin models with sparse control

**Characteristics:**
- High uncertainty (often ± order of magnitude)
- Multiple assumptions chained together
- Cannot be verified with current data
- **Must** be labeled as speculative in all communications

**GEOX Verdict:** 888_HOLD mandatory. Human sign-off required. Cannot auto-SEAL.

---

## The Collapse Problem (F9 Violation)

### The Danger

The most common failure mode in geoscience communication is **level collapse** — presenting a higher-uncertainty level as if it were lower-uncertainty:

| Collapse | Example | Risk |
|----------|---------|------|
| **INT → OBS** | "This is sandstone" (actually an interpretation) | Overconfidence, bad decisions |
| **SPEC → DER** | "We have 500 MMbbl" (actually a speculation) | Financial misrepresentation |
| **DER → OBS** | "Porosity is 15%" (actually derived from assumptions) | False precision |

### GEOX Enforcement

**Automatic 888_HOLD triggers:**
- Any output that collapses levels without explicit disclosure
- Interpretations presented without confidence bands
- Speculations lacking "SPECULATED" label

---

## Level Labeling Convention

### Required on All GEOX Outputs

```yaml
epistemic_classification:
  level: [OBS | DER | INT | SPEC]
  basis: "Description of how this was determined"
  assumptions: [list of key assumptions]
  uncertainty: Ω₀ value or range
  confidence: τ value (F2 Truth)
```

### Example Labels

**OBS:**
```
[OBS] Seismic amplitude at TWT 1200ms: -2500 mV
Source: Line 1234, SEG-Y trace 456
Instrument: GSI 408UL, gain 24dB
Units: millivolts (uncalibrated)
```

**DER:**
```
[DER] Porosity from density log: 0.15 ± 0.03
Assumptions: Sandstone matrix (ρma = 2.65), fluid (ρf = 1.0)
Algorithm: Wyllie equation
Uncertainty: Matrix uncertainty ±0.05 g/cc
```

**INT:**
```
[INT] Lithology: Clean sandstone
Basis: Low GR (45 API), moderate ρb (2.35 g/cc), φ ≈ 15%
Alternatives: Silty limestone (low probability)
Confidence: τ = 0.82 (< 0.99, uncertainty declared)
Recommendation: 888_HOLD — thin section verification suggested
```

**SPEC:**
```
[SPEC] Original Oil in Place: 450 MMbbl ± 300 MMbbl (P90-P10)
Basis: Analog to Field X, 20km away
Control: No wells in structure
Assumptions: Sandstone reservoir, 15% φ, 70% Sw, 100m pay
⚠️ SPECULATED — requires drilling to verify
888_HOLD: Human decision required before inclusion in portfolio
```

---

## Multi-Level Analysis Example

### Well Log Interpretation

| Depth | Observation | Derivation | Interpretation | Speculation |
|-------|-------------|------------|----------------|-------------|
| 1500m | GR = 45 API | Vsh = 0.15 | Clean sand | — |
| 1500m | RHOB = 2.35 | φ = 0.18 | — | — |
| 1500m | RT = 50 Ω·m | Sw = 0.55 | Oil-bearing? | OOIP? |

**Proper GEOX Output:**
```
Interval 1495-1505m:
- [OBS] GR=45 API, RHOB=2.35 g/cc, RT=50 Ω·m
- [DER] φ=0.18 ± 0.03, Vsh=0.15 ± 0.05, Sw=0.55 ± 0.15
- [INT] Likely clean sandstone with oil shows
- [SPEC] OOIP estimate: 2.5 MMbbl ± 1.5 MMbbl (high uncertainty)

Verdict: 888_HOLD on SPEC component
```

---

## Constitutional Enforcement

| Floor | Epistemic Level Enforcement |
|-------|---------------------------|
| **F2 Truth** | Level must match actual derivation chain |
| **F4 Clarity** | Level explicit on every output |
| **F7 Humility** | Uncertainty band commensurate with level |
| **F9 Anti-Hantu** | No level collapse without disclosure |
| **F13 Sovereign** | INT/SPEC require human confirmation |

---

## Related Pages

- [[10_THEORY/Theory_of_Anomalous_Contrast]] — F9 Anti-Hantu enforcement
- [[10_THEORY/Contrast_Canon]] — Separation of concerns
- [[60_CASES/Petrophysical_Analysis_Example]] — Multi-level workflow

---

*Epistemic Levels — Honest classification of how we know what we claim to know*  
*OBS → DER → INT → SPEC: Never collapse without warning*
