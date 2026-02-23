---
name: arifos-integrate
description: 333_ATLAS — Cross-domain synthesis, context mapping. Maps knowledge boundaries with F10 Ontology enforcement.
metadata:
  arifos:
    stage: 333_ATLAS
    trinity: AGI
    floors: [F7, F8, F10]
    version: 55.5
---

# arifos-integrate

**Tagline:** Map context, establish boundaries, extract vocabulary.

**Physics:** Network Topology — graph connectivity metrics

**Math:** Ω₀ = (|Unknown| + 0.5×|Unstable|) / |Total| ∈ [0.03, 0.05]

**Code:**
```python
def integrate(parsed_intent, workspace):
    files = discover_files(workspace, parsed_intent.targets)
    deps = extract_dependencies(files)
    omega_0 = calculate_uncertainty(files, deps)
    return ContextMap(files=files, deps=deps, omega_0=omega_0)
```

**Usage:** `/action integrate targets=["file1", "file2"]`

**Floors:** F7 (Humility), F8 (Genius), F10 (Ontology)
