# PHYSICS_9 — Minimal Governed State Vector

> **Type:** Physics  
> **Epistemic Level:** OBS (observational foundation)  
> **Confidence:** 1.0  
> **Tags:** [physics, foundation, geophysics, state-vector]  
> **Sources:** [[raw/papers/earth_physics_canon.pdf]]  
> **arifos_floor:** F2, F9

---

## Design Principle: State vs. Constitutive Response

> **PHYSICS_9 is the minimal governed state vector for Earth-material inference: {ρ, Vp, Vs, ρₑ, χ, k, P, T, φ}.**
> 
> Variables such as **permeability, elastic moduli, heat capacity, impedance, and strength** are treated as **derived constitutive responses**, not canonical state slots.

This separation prevents **derived quantities from contaminating the base state** — essential for governed physics inference where causal clarity is required (F2 Truth, F9 Physics9).  

---

## The Physics 9

The 9 canonical physical quantities that **completely describe the base state** of any subsurface Earth material:

| # | Variable | Symbol | Unit | Physical Meaning | Primary Log/Source |
|---|----------|--------|------|------------------|-------------------|
| **1** | **Density** | ρ | kg/m³ | Bulk mass density | RHOB (density log) |
| **2** | **P-wave Velocity** | Vp | m/s | Compressional elastic wave speed | DTCO (sonic) |
| **3** | **S-wave Velocity** | Vs | m/s | Shear elastic wave speed | DTSM (sonic) |
| **4** | **Electrical Resistivity** | ρₑ | Ω·m | Opposition to current flow | RT (resistivity) |
| **5** | **Magnetic Susceptibility** | χ | SI (dimensionless) | Response to magnetic fields | MAG (survey) |
| **6** | **Thermal Conductivity** | k | W/(m·K) | Heat transfer capacity | TC (temp log) |
| **7** | **Pressure** | P | Pa | Pore/fluid pressure | MDT/RFT (tester) |
| **8** | **Temperature** | T | K | Thermal energy state | BHT/DTS (temp) |
| **9** | **Porosity** | φ | fraction (0–1) | Normalized void volume | PHI (neutron/density/NMR) |

---

## Physics Completeness

With these 9 **state variables**, you can derive **all exploration-grade geophysics** as constitutive responses:

### Constitutive Responses from Mechanical State (ρ, Vp, Vs)

These are **derived**, not canonical:

```
Acoustic Impedance:     I = ρ × Vp                     [DERIVED]
Poisson's Ratio:        ν = (Vp² - 2Vs²) / 2(Vp² - Vs²) [DERIVED]
Bulk Modulus:           K = ρ(Vp² - 4/3 Vs²)           [DERIVED]
Shear Modulus:          μ = ρ × Vs²                    [DERIVED]
Seismic Reflectivity:   R = (I₂ - I₁) / (I₂ + I₁)      [DERIVED]
```

### From EM-Thermal (ρₑ, χ, k)
```
Formation Factor:       F = ρₑ(rock) / ρₑ(fluid)
Heat Flow:              q = -k × ∇T
Apparent Resistivity:   ρa = f(ρₑ, χ, geometry)
```

### From State (P, T, φ)
```
Effective Stress:       σ' = σ - P
Water Saturation:       Sw = f(ρₑ, φ, Rw) [Archie]
Thermal Gradient:       ∇T = ∂T/∂z
Formation Volume Factor: B = f(P, T, fluid)
```

### Constitutive Responses: NOT Canonical

These **depend on** the 9 base state variables but are **not in the canon**:

| Response | Depends On | Why Not Canonical |
|----------|-----------|-------------------|
| **Permeability (k)** | φ, P, T, pore geometry | Fabric-dependent, not state |
| **Heat Capacity (Cp)** | Mineralogy, φ, fluids | Mixture property |
| **Thermal Expansivity** | Mineralogy, T | Derived material property |
| **Electrokinetic coupling** | ρₑ, k, fluid chemistry | Coupled phenomenon |

**Rule:** If you need to know the material's **fabric, history, or mixture components** beyond the 9, it is constitutive, not canonical.

---

## Canonical Schema

```python
class Physics9(BaseModel):
    """
    The 9 fundamental geophysical variables.
    Minimal basis for forward-modeling crustal Earth.
    """
    # Mechanical
    density: float = Field(..., ge=1000, le=3000)  # kg/m³
    vp: float = Field(..., ge=1500, le=8000)       # m/s
    vs: float = Field(..., ge=0, le=5000)          # m/s
    
    # EM-Thermal
    resistivity: float = Field(..., ge=0.01, le=10000)  # Ω·m
    magnetic_suscept: float = Field(..., ge=-1, le=100)  # SI
    thermal_conduct: float = Field(..., ge=0.5, le=10)   # W/(m·K)
    
    # State
    pressure: float = Field(..., ge=0, le=200e6)    # Pa
    temperature: float = Field(..., ge=273, le=800) # K
    porosity: float = Field(..., ge=0, le=1)        # fraction
```

---

## Why These 9? State vs. Derived

| Category | Examples | Status in PHYSICS_9 |
|----------|----------|-------------------|
| **Base State** | ρ, Vp, Vs, ρₑ, χ, k, P, T, φ | ✅ Canonical |
| **Constitutive Response** | K, μ, I, ν, Sw, k_perm, Cp | ❌ Derived |
| **Geometric** | Void ratio (e), aspect ratio | ❌ Alternative representation |

**The rule:** If it can be computed unambiguously from the 9, it is **derived**, not canonical.

## Physics Note: Void Volume is the Primitive

At **F9 Physics9** level, the fundamental quantity is **void volume** (Vv).

**PHYSICS_9 uses φ (porosity)** as the field representation:
- φ = Vv / Vt (void volume / total bulk volume)
- Dimensionless, bounded [0, 1]
- Invertible into saturation, permeability, formation factor

---

## Related Pages

- [[20_PHYSICS/Acoustic_Impedance]] — Derivation from ρ, Vp **[DERIVED]**
- [[20_PHYSICS/Elastic_Moduli]] — K, μ, ν derivations **[DERIVED]**
- [[20_PHYSICS/Porosity_Types]] — φt vs φe distinction **[CANONICAL]**
- [[20_PHYSICS/Saturation_Models]] — Sw from Archie equations **[DERIVED]**
- [[30_MATERIALS/RATLAS_Index]] — Material-specific Physics_9 values **[CANONICAL]**

---

## Design Notes

### Why Not Permeability in Canon?

Permeability (k) is critically important for flow, but it is **not a base state variable** because:

1. **Same φ, different k:** Two sandstones with φ = 0.20 can have k = 10 mD or k = 1000 mD depending on pore throat size
2. **Stress dependence:** k decreases with effective stress (P) — it's not intrinsic
3. **Fabric history:** Diagenesis, cementation, fracturing all change k without changing φ significantly

**Canonical φ captures the void. Constitutive k captures the flow path.**

---

## Telemetry

```
[PHYSICS_9 | ρ:2650.0 Vp:3500.0 Vs:1800.0 ρₑ:10.50 χ:0.0012 k:2.50 P:25.00MPa T:373.0K φ:0.150 | SEALED]
```

---

*DITEMPA BUKAN DIBERI — Physics first, interpretation second.*  
*State clearly. Derive carefully. Govern ruthlessly.*
