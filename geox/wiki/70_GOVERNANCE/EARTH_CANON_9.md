# EARTH.CANON_9 — Fundamental Geophysical Variables
**Version:** v1.0-SEALED | **Status:** DITEMPA BUKAN DIBERI

The 9 canonical physical quantities that completely describe any subsurface Earth material.

---

## The Canon

| # | Variable | Symbol | Unit | Physical Meaning | Primary Log/Source |
|---|----------|--------|------|------------------|-------------------|
| **1** | **Density** | ρ | kg/m³ | Bulk mass density of the medium | RHOB (density log) |
| **2** | **P-wave Velocity** | Vp | m/s | Compressional elastic wave speed | DTCO (sonic compressional) |
| **3** | **S-wave Velocity** | Vs | m/s | Shear elastic wave speed | DTSM (sonic shear) |
| **4** | **Electrical Resistivity** | ρₑ | Ω·m | Opposition to electric current flow | RT (deep resistivity) |
| **5** | **Magnetic Susceptibility** | χ | SI (dimensionless) | Response to magnetic fields | MAG (magnetic survey) |
| **6** | **Thermal Conductivity** | k | W/(m·K) | Heat transfer capacity | TC (temperature log derivative) |
| **7** | **Pressure** | P | Pa | Pore/fluid pressure state | MDT/RFT (formation tester) |
| **8** | **Temperature** | T | K | Thermal energy state | BHT/DTS (bottom-hole temp) |
| **9** | **Porosity** | φ | fraction (0–1) | Normalized void volume (Vv/Vt) | PHI (neutron/density/NMR) |

---

## Physics Completeness

With these 9, you can derive all exploration-grade geophysics:

### From Mechanical (ρ, Vp, Vs)
```
Acoustic Impedance:     I = ρ × Vp
Poisson's Ratio:        ν = (Vp² - 2Vs²) / 2(Vp² - Vs²)
Bulk Modulus:           K = ρ(Vp² - 4/3 Vs²)
Shear Modulus:          μ = ρ × Vs²
Seismic Reflectivity:   R = (I₂ - I₁) / (I₂ + I₁)
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
Water Saturation:       Sw = f(ρₑ, φ, Rw)  [Archie et al.]
Thermal Gradient:       ∇T = ∂T/∂z
Formation Volume Factor: B = f(P, T, fluid)
```

---

## Canonical Schema (GEOX Implementation)

```python
# arifos/geox/schemas/earth_canon_9.py

from pydantic import BaseModel, Field
from typing import Literal

class EarthCanon9(BaseModel):
    """
    The 9 fundamental geophysical variables.
    Minimal basis for forward-modeling crustal Earth.
    No interpretive variables (lithology, facies) allowed at this level.
    """
    # Mechanical
    density: float = Field(..., ge=1000, le=3000, description="Bulk density ρ [kg/m³]")
    vp: float = Field(..., ge=1500, le=8000, description="P-wave velocity Vp [m/s]")
    vs: float = Field(..., ge=0, le=5000, description="S-wave velocity Vs [m/s]")
    
    # EM-Thermal
    resistivity: float = Field(..., ge=0.01, le=10000, description="Electrical resistivity ρₑ [Ω·m]")
    magnetic_suscept: float = Field(..., ge=-1, le=100, description="Magnetic susceptibility χ [SI]")
    thermal_conduct: float = Field(..., ge=0.5, le=10, description="Thermal conductivity k [W/(m·K)]")
    
    # State
    pressure: float = Field(..., ge=0, le=200e6, description="Pore pressure P [Pa]")
    temperature: float = Field(..., ge=273, le=800, description="Temperature T [K]")
    
    # Porosity (canonical field representation of void volume)
    porosity: float = Field(..., ge=0, le=1, description="Total porosity φ = Vv/Vt [fraction]")
    porosity_type: Literal["total", "effective", "isolated", "primary", "secondary"] = Field(
        default="total",
        description="Type of porosity being reported (F2 disclosure requirement)"
    )
    
    # Provenance (F11 Auditability)
    measurement_sources: dict[str, str] = Field(default_factory=dict)
    uncertainty_bands: dict[str, tuple[float, float]] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "canonical_reference": "GEOX EARTH.CANON_9 v1.0",
            "physics_basis": "Continuum mechanics + EM theory + Thermodynamics",
            "completeness_test": "Can derive all exploration geophysics"
        }
    
    @property
    def acoustic_impedance(self) -> float:
        """I = ρ × Vp [kg/(m²·s)]"""
        return self.density * self.vp
    
    @property
    def poisson_ratio(self) -> float:
        """ν = (Vp² - 2Vs²) / 2(Vp² - Vs²) [dimensionless]"""
        if self.vs == 0:
            return 0.5  # Fluid limit
        return (self.vp**2 - 2*self.vs**2) / (2*(self.vp**2 - self.vs**2))
    
    @property
    def bulk_modulus(self) -> float:
        """K = ρ(Vp² - 4/3 Vs²) [Pa]"""
        return self.density * (self.vp**2 - (4/3)*self.vs**2)
    
    @property
    def shear_modulus(self) -> float:
        """μ = ρ × Vs² [Pa]"""
        return self.density * self.vs**2
    
    def to_telemetry(self) -> str:
        """Canonical telemetry format."""
        return (
            f"[EARTH.CANON_9 | ρ:{self.density:.1f} Vp:{self.vp:.1f} Vs:{self.vs:.1f} "
            f"ρₑ:{self.resistivity:.2f} χ:{self.magnetic_suscept:.4f} k:{self.thermal_conduct:.2f} "
            f"P:{self.pressure/1e6:.2f}MPa T:{self.temperature:.1f}K φ:{self.porosity:.3f} | SEALED]"
        )
```

---

## Physics Note: Void Volume is the Primitive

At **F2 physics** level, the fundamental quantity is **void volume** (Vv) — the absolute volume of empty space (pores, cracks, vugs) inside the material.

**Canonical 9 uses φ (porosity)** as the field representation:
- φ = Vv / Vt (void volume / total bulk volume)
- Dimensionless, bounded [0, 1]
- Invertible into saturation, permeability models, formation factor

**Alternative representations:**
- **Void ratio** (soil mechanics): e = Vv / Vs (void volume / solid grain volume)
- **Void volume** (absolute): Vv = φ × Vt

## Porosity Types (Next Layer)

EARTH.CANON_9 φ is **total porosity** (φt). Downstream distinction:

| Type | Definition | Symbol | Physics |
|------|------------|--------|---------|
| **Total Porosity** | All void space | φt | φt = Vv_total / Vt |
| **Effective Porosity** | Connected voids only | φe | φe = Vv_connected / Vt |
| **Isolated Porosity** | Non-connected voids | φi | φi = φt - φe |
| **Primary Porosity** | Depositional | φp | Intergranular |
| **Secondary Porosity** | Post-depositional | φs | Fractures, vugs, dissolution |

**888 HOLD trigger:** Reporting φe as φt without disclosure (F2 violation).

## Substitution Rules

For **fluid-saturated porous media**, #9 (porosity) may be substituted:

| Context | Variable | Symbol | Unit | When to Use |
|---------|----------|--------|------|-------------|
| **Storage** | Porosity | φ | fraction | Reservoir characterization |
| **Flow** | Permeability | k | m² (or mD) | Production engineering |
| **Saturation** | Water Saturation | Sw | fraction | Petrophysical interpretation |

**Constraint:** Only ONE of {φ, k, Sw} in the canonical 9. The others are derived.

---

## References

- **DSDP Leg 78B:** Physical properties of basalts and sediments — [deepseadrilling.org](http://www.deepseadrilling.org/78b/volume/dsdp78b_15.pdf)
- **GFZ Potsdam:** Rock physical properties database — [gfzpublic.gfz-potsdam.de](https://gfzpublic.gfz-potsdam.de/rest/items/item_5028750_1/component/file_5028752/content)
- **SDSU EM Geo:** Electrical properties of rocks — [emgeo.sdsu.edu](https://emgeo.sdsu.edu/emrockprop.html)

---

## Telemetry

```
[EARTH.CANON_9 | ρ:2650.0 Vp:3500.0 Vs:1800.0 ρₑ:10.50 χ:0.0012 k:2.50 P:25.00MPa T:373.0K φ:0.150 | SEALED]
```

---

*DITEMPA BUKAN DIBERI — Physics first, interpretation second.*
