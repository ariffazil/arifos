---
type: Tool
epistemic_level: SAFE
confidence: 0.95
certainty_band: [0.90, 0.98]
tags: [tool, query, ratlas, materials, lookup]
arifos_floor: F2
sources: []
---

# geox_query_ratlas

> **Type:** Tool  
> **Risk Level:** SAFE  
> **Epistemic Level:** DER  
> **Confidence:** 0.95  
> **Certainty Band:** [0.90, 0.98]  
> **Tags:** [tool, query, ratlas, materials, lookup]  
> **arifos_floor:** F2  

---

## Purpose

Query the **RATLAS** (Rock Atlas) material database for physical properties, seismic response, and geological context.

**Use Cases:**
- Prospect evaluation: What properties to expect?
- Log interpretation: Does this match expected response?
- Modelling: Input parameters for forward models
- QA: Are these values physically reasonable?

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `material_code` | string | Conditional | Exact RATLAS code (e.g., "SAND_QZ_CLEAN") |
| `query_type` | string | No | "exact" (default), "family", "property_range", "fuzzy" |
| `family` | string | No | Material family (e.g., "SED_CLASTIC") |
| `property_constraints` | object | No | Filter by property ranges |
| `return_format` | string | No | "full" (default), "summary", "seismic_only" |

### Query Types

| Type | Use Case | Example |
|------|----------|---------|
| **exact** | Known material | Look up specific sandstone type |
| **family** | Browse materials | Show all clastics |
| **property_range** | Find matches | Materials with φ > 20% |
| **fuzzy** | Uncertain ID | Similar to "dirty sand" |

---

## Returns

```json
{
  "verdict": "SEAL",
  "query_type": "exact",
  "results": [
    {
      "material_code": "SAND_QZ_CLEAN",
      "family": "SED_CLASTIC",
      "name": "Clean Quartz Sandstone",
      "epistemic_level": "DER",
      "confidence": 0.92,
      
      "properties": {
        "porosity": {
          "value": 0.25,
          "range": [0.20, 0.30],
          "confidence": 0.88
        },
        "permeability": {
          "value": 500,
          "range": [100, 2000],
          "unit": "mD",
          "confidence": 0.75
        },
        "density": {
          "grain": 2.65,
          "bulk": 2.20,
          "unit": "g/cm³"
        },
        "acoustic_impedance": {
          "value": 8.5,
          "range": [7.0, 10.0],
          "unit": "×10⁶ kg/m²·s"
        }
      },
      
      "seismic_response": {
        "vp": "3500-4500 m/s",
        "vs": "2000-2800 m/s",
        "reflection_coefficient_vs_shale": 0.15
      },
      
      "log_response": {
        "GR": "15-45 API",
        "RHOB": "2.15-2.25 g/cm³",
        "NPHI": "0.20-0.30",
        "DT": "55-70 μs/ft"
      },
      
      "geological_context": {
        "environment": "Fluvial to shallow marine",
        "diagenesis": "Quartz cementation reduces φ",
        "analogs": ["Niger Delta", "Gulf of Mexico"]
      },
      
      "cross_refs": [
        "[[30_MATERIALS/Sedimentary_Clastics]]",
        "[[40_BASINS/Malay_Basin]]"
      ]
    }
  ]
}
```

---

## Example Queries

### Query 1: Exact Match

```python
result = geox_query_ratlas(
    material_code="SAND_QZ_CLEAN",
    query_type="exact"
)
```

### Query 2: Family Browse

```python
clastics = geox_query_ratlas(
    query_type="family",
    family="SED_CLASTIC",
    return_format="summary"
)
# Returns all 18 clastic materials with key properties
```

### Query 3: Property Filter

```python
high_porosity = geox_query_ratlas(
    query_type="property_range",
    property_constraints={
        "porosity_min": 0.25,
        "permeability_min": 100
    }
)
# Returns materials meeting criteria
```

### Query 4: Seismic Planning

```python
# For seismic modelling: get Vp, Vs, density
elastic = geox_query_ratlas(
    material_code="SHALE_ILL",
    query_type="exact",
    return_format="seismic_only"
)
# Returns only elastic properties
```

---

## Confidence Interpretation

| Confidence | Interpretation | Usage |
|------------|----------------|-------|
| >0.90 | Well-calibrated | Direct use in models |
| 0.75–0.90 | Good | Use with minor uncertainty |
| 0.60–0.75 | Moderate | Consider alternatives |
| <0.60 | Poor | Do not use without validation |

**F2 Truth:** RATLAS provides confidence values. Never override without justification.

---

## Integration

- **Input to:** [[50_TOOLS/geox_evaluate_prospect]], forward modelling
- **Validation:** [[50_TOOLS/geox_qc_logs]] (compare to RATLAS expectations)
- **Cross-refs:** All [[30_MATERIALS/*]] pages

---

*Tool Specification v1.0.0 · Part of [[50_TOOLS/Tool_Index]]*
