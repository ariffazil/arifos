# CANON-9 Literature Grounding & Intellectual Position

> **Type:** Theory  
> **Epistemic Level:** INT (synthesis of literature)  
> **Confidence:** 0.92  
> **Certainty Band:** [0.85, 0.96]  
> **Tags:** [canon-9, literature, rock-physics, synthesis, grounding, novelty]  
> **Sources:** [Bagdassarov, Grana, SAPHYR, joint inversion literature, THMC reviews]  
> **arifos_floor:** F2  

---

## Core Intellectual Position

> **The novelty of EARTH.CANON_9 is not in the raw variables — these are well-established in geophysics literature. The novelty is in treating them as a governed, minimal, cross-domain state vector that sits above disciplines and below derived operators.**

This document maps the literature support for each ingredient and clarifies where GEOX's synthesis diverges from academic precedent.

---

## Literature Map: Variable by Variable

| Variable | Literature Support | Canonical Status | Key Sources |
|----------|-------------------|------------------|-------------|
| **ρ (Density)** | Strong | Established | Bagdassarov; SAPHYR; all rock physics |
| **Vp, Vs (Velocities)** | Strong | Established | Bagdassarov (acoustic properties); SAPHYR |
| **ρₑ (Resistivity)** | Strong | Established | Bagdassarov (electric properties); Grana workflows |
| **χ (Susceptibility)** | Moderate | Established | Bagdassarov (magnetic properties); mineral systems |
| **k (Thermal conductivity)** | Moderate | Established | Bagdassarov (thermal properties); SAPHYR |
| **P (Pressure)** | Strong | Established | Rock mechanics; THMC; drilling literature |
| **T (Temperature)** | Strong | Established | Geothermal; THMC; SAPHYR; basin modeling |
| **φ (Porosity)** | Strong | Established | Petrophysics core; Bagdassarov; all reservoir literature |

### Key Insight

**All 9 variables appear in the literature.** None are GEOX inventions. The convergence is in the **architecture**, not the ingredients.

---

## What the Literature Supports

### 1. Rock Physics: Bagdassarov's Organization

**Bagdassarov, N. (2020).** *Fundamentals of Rock Physics.*

Organizes the subject into:
1. Density and porosity
2. Stresses in rocks (P)
3. Acoustic properties (Vp, Vs)
4. Electric resistivity (ρₑ)
5. Magnetic properties (χ)
6. Thermal properties (k, T)

**Verdict:** Covers **8 of 9** CANON-9 variables (all except explicit T as separate state, though thermal properties implies T).

**Key quote:** "Vp and Vs depend on porosity, temperature, and pressure" — exactly the cross-coupled logic GEOX uses.

---

### 2. Integrated Petrophysics: Grana et al.

**Grana, D., Mukerji, T., & Dvorkin, J. (2021).** *Seismic Reflections of Rock Properties.*

Presents unified workflow linking:
- Sonic velocity (Vp, Vs)
- Resistivity (ρₑ)
- Porosity (φ)
- Density (ρ)
- Lithology
- Fluid properties

**Goal:** "Reducing ambiguity by combining multiple physics domains."

**Verdict:** Very close to GEOX's "one canonical state, many downstream operators" spirit.

---

### 3. Joint Inversion Literature

**Strong support for multi-physics fusion:**

| Papers | Fusion Target | CANON-9 Overlap |
|--------|--------------|-----------------|
| Gravity + Seismic | Density + Velocity | ρ, Vp |
| MT/EM + Seismic | Resistivity + Velocity | ρₑ, Vp, Vs |
| Magnetic + Gravity | Susceptibility + Density | χ, ρ |
| Full waveform + EM | All elastic + electric | Vp, Vs, ρₑ |

**Key insight:** No single field is sufficient. Multiple physical properties must be mapped together to constrain subsurface.

**Verdict:** Directly backs GEOX intuition that "decoding the Earth" requires multi-physics state.

---

### 4. Property Atlases: SAPHYR Swiss Atlas

**SAPHYR (Swiss Atlas of Physical Properties of Rocks):**
- Density
- Porosity
- Permeability
- Thermal conductivity
- Specific heat capacity
- Magnetic susceptibility
- Vp, Vs
- Pressure/temperature derivatives of seismic properties

**Verdict:** Not exact CANON-9 (includes permeability, Cp), but treats these as **coherent family of Earth-material descriptors**.

---

### 5. THMC / Digital Twin Literature

**Thermal-Hydraulic-Mechanical-Chemical (THMC) reviews:**

Treats as evolving state:
- **P** (pressure) — hydraulic
- **T** (temperature) — thermal
- **φ** (porosity) — mechanical/hydraulic coupling
- Coupled fields (elastic, transport)

**Verdict:** Supports P, T, φ as **dynamic control variables** in subsurface systems.

**Limitation:** THMC adds **Chemistry** — explicitly weak in CANON-9 without constitutive operators.

---

## Where GEOX Synthesis is Novel

### 1. The Minimal Schema Claim

**What literature does NOT say:**

> "The exact set {ρ, Vp, Vs, ρₑ, χ, k, P, T, φ} is the minimal universal state vector for Earth-material inference."

**Literature reality:**
- Variables appear in discipline-specific combinations
- No cross-domain canonical 9-slot schema widely adopted
- Different fields privilege different subsets

**GEOX novelty:** Compression to exactly these 9 as **governed minimal state**.

---

### 2. The Architecture: State vs. Operators

**What literature does NOT do:**

Explicitly separate:
```
BASE STATE (CANON-9) → OPERATORS → DERIVED PRODUCTS
```

**Literature reality:**
- Permeability often treated as primary (not derived from φ + fabric)
- Moduli sometimes stored as primary (not computed from ρ,Vp,Vs)
- Heat capacity as material property (not mixture model)

**GEOX novelty:** Strict enforcement of **state vs. constitutive response** hierarchy.

---

### 3. The Governance Layer

**What literature does NOT do:**

Attach constitutional constraints (F1-F13) to state vector usage.

**GEOX novelty:** 
- F2 Truth: τ ≥ 0.99 on state estimation
- F4 Clarity: Explicit uncertainty on each variable
- F7 Humility: Ω₀ bands on derived products
- F13 Sovereign: Human veto on state-derived decisions

---

## The Honest Verdict

### Academic Grounding: ✅ Strong

The pieces are well-supported in:
- Rock physics (Bagdassarov)
- Petrophysics (Grana et al.)
- Joint inversion (multi-physics fusion)
- THMC / digital twin (P, T, φ as dynamic state)

### Exact CANON-9 Precedent: ⚠️ Weak / Not Obvious

No canonical academic source uses this exact 9 as universal minimal Earth-state schema.

### Eureka Level Assessment

| Claim | Status | Reason |
|-------|--------|--------|
| **Raw physics discovery** | ❌ No | Variables are established |
| **New physical law** | ❌ No | Relationships are known |
| **Conceptual unification** | ✅ Potentially | Cross-domain compression is novel |
| **Operating architecture** | ✅ Potentially | Governed state compiler is novel |
| **Framework breakthrough** | 🧪 Needs proof | Sufficiency, Compression, Transferability tests pending |

---

## The Three Tests for Eureka Status

To move from "smart framing" to "Eureka-ish," GEOX must prove:

### Test 1: Sufficiency

**Question:** Can most high-value downstream products be reconstructed from CANON-9 plus governed operators?

**Evidence needed:**
- CCS containment health ← CANON-9 + operators
- H₂ storage stability ← CANON-9 + operators
- Geothermal reservoir life ← CANON-9 + operators
- Mineral system targeting ← CANON-9 + operators

**Status:** 🧪 Benchmarks pending

### Test 2: Compression

**Question:** Can teams replace messy discipline-specific schemas with this one state vector without losing critical information?

**Evidence needed:**
- Seismic-only team → CANON-9 without loss
- Log-analysis team → CANON-9 without loss
- Reservoir simulation → CANON-9 without loss
- EM geothermal → CANON-9 without loss

**Status:** 🧪 Case studies pending

### Test 3: Transferability

**Question:** Does the same canon work across O&G, CCS, geothermal, minerals, groundwater, and storage?

**Evidence needed:**
- Same 9 variables, different domains
- Domain-specific operators, canonical state
- Cross-domain consistency checks

**Status:** 🧪 Multi-domain pilots pending

---

## What CANON-9 Does NOT Decode

**Explicit limitations:**

| Domain | Why Weak | Mitigation |
|--------|----------|------------|
| **Chemistry** | No compositional variables | Constitutive operators (mineralogy models) |
| **Mineral reactions** | Kinetics not in canon | THMC coupling operators |
| **Grain fabric** | Textural info lost | Fabric as operator input, not state |
| **Fractures** | Discrete networks not captured | Dual-porosity operators |
| **Permeability architecture** | k not in canon | Derived from φ + fabric + P |
| **Anisotropy** | Scalar assumptions | Tensor extensions (future CANON-9+) |
| **Saturation partitioning** | Single Sw | Multi-phase operators |
| **Time-dependent alteration** | Static snapshot | 4D state evolution |

**Defensible claim:**
> "CANON-9 does not decode all of Earth ontology, but it is a strong minimal state vector for decoding a large fraction of Earth's observable material behavior across geophysics, petrophysics, and subsurface monitoring."

---

## The Contribution Hierarchy

### Not New
- Individual variables exist
- Physics relationships known
- Multi-physics fusion practiced

### Potentially New
- Exact 9-variable minimal set
- Governed state/operator separation
- Cross-domain canonical schema
- Constitutional enforcement layer

### Definitely New
- **GEOX synthesis:** The specific combination of minimal state + governed operators + F1-F13 constraints + arifOS integration

---

## References

### Core Literature

**Bagdassarov, N. (2020).** *Fundamentals of Rock Physics.* Wiley-VCH.
- Covers: ρ, φ, P, Vp, Vs, ρₑ, χ, k, T relationships
- Chapter structure mirrors CANON-9 domains

**Grana, D., Mukerji, T., & Dvorkin, J. (2021).** *Seismic Reflections of Rock Properties.* Cambridge.
- Unified petrophysics workflow
- Multi-physics ambiguity reduction

**SAPHYR (Swiss Atlas of Physical Properties of Rocks).**
- Multi-property crustal database
- Vp, Vs, ρ, φ, k, χ, Cp coverage

### Joint Inversion

**Gallardo, L.A., & Meju, M.A. (2004).** "Joint two-dimensional DC resistivity and seismic travel time inversion with cross-gradient constraints." *JGR*.

**Moorkamp, M., et al. (2011).** "A framework for 3-D joint inversion of MT, gravity and seismic refraction data." *GJI*.

### THMC / Digital Twin

**Rutqvist, J. (2012).** "The geomechanics of CO₂ storage in deep sedimentary formations." *IJGGC*.

**Xie, J., et al. (2021).** "Digital twin for subsurface energy systems: A review." *Renewable and Sustainable Energy Reviews*.

---

## Related Pages

- [[20_PHYSICS/EARTH_CANON_9]] — The canonical state vector
- [[20_PHYSICS/EARTH_CANON_9#Design Notes]] — State vs. constitutive response
- [[40_HORIZONS/MCP_Capability_Horizon]] — Applications requiring proof

---

## Telemetry

```
[CANON-9_LITERATURE | GROUNDING:STRONG ✅ | PRECEDENT:WEAK ⚠️ | NOVELTY:ARCHITECTURAL 🏗️ | EUREKA_TESTS:PENDING 🧪]
```

---

*CANON-9 Literature Grounding — Honest intellectual position*  
*Ingredients: established. Architecture: novel. Proof: pending.*

**DITEMPA BUKAN DIBERI — The compression is forged, not found.**
