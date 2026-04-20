# Bond et al. (2007) — Cognitive Bias in Seismic Interpretation

> **Type:** Theory  
> **Epistemic Level:** OBS (empirical study results)  
> **Confidence:** 0.98  
> **Certainty Band:** [0.95, 0.995]  
> **Tags:** [bond, bias, cognitive, seismic, interpretation, failure]  
> **Sources:** [[raw/papers/bond_2007.pdf]]  
> **arifos_floor:** F9  

---

## The Study

**Citation:**
> Bond, C.E., Gibbs, A.D., Shipton, Z.K., Jones, S. (2007). "What do you think this is? 'Conceptual uncertainty' in geoscience interpretation." *GSA Today*, 17(11), 4–10.

**Study Design:**
- Presented synthetic seismic data to experienced interpreters
- Data contained **deliberate ambiguities** and **display artifacts**
- Measured: Interpretation accuracy, confidence, bias indicators

---

## The Shocking Result

### 79% Failure Rate

**79% of experienced interpreters failed** to correctly identify structures in synthetic seismic data.

### Not Because:
- ❌ Data quality was poor
- ❌ Interpreters were inexperienced
- ❌ Problem was technically complex

### But Because:
- ✅ **Display artifacts** created perceptual illusions
- ✅ **Confirmation bias** led to pattern completion
- ✅ **Overconfidence** prevented second-look
- ✅ **Anomalous contrast** fooled expert eyes

---

## The Failure Modes

### Mode 1: Display Artifact Misidentification

| Artifact | What Experts Saw | Reality |
|----------|-----------------|---------|
| **AGC edge** | Continuous reflector | Processing artifact |
| **Colormap band** | Fluid contact | Histogram binning |
| **Migration smile** | Fault | Processing geometry |
| **Vertical stretch** | Steep dip | Display exaggeration |

**Key Finding:** Experts interpreted display choices as geological signal.

### Mode 2: Premature Pattern Completion

**The Gestalt Problem:**
```
Partial data presented
       │
       ▼
Brain completes pattern (automatic)
       │
       ▼
Expert "sees" structure that isn't fully evidenced
       │
       ▼
Confidence high despite insufficient data
```

**Bond et al. Finding:** Interpreters with 10+ years experience showed **higher** pattern-completion bias than novices (expertise became overconfidence).

### Mode 3: Confirmation Bias

**The Trap:**
1. Initial hypothesis formed (often within first 30 seconds)
2. Subsequent data filtered to support hypothesis
3. Contradictory evidence minimized or ignored
4. "Confident" interpretation delivered

**Bond et al. Finding:** Only 12% of experts actively sought disconfirming evidence.

---

## The GEOX Response

Bond et al. (2007) is the **empirical foundation** for Theory of Anomalous Contrast.

### ToAC as Response

| Bond Finding | ToAC Rule | GEOX Tool |
|--------------|-----------|-----------|
| Display artifacts fool experts | **Contrast Canon** | Transform registry, audit |
| Premature pattern completion | **Multi-Model Rule** | `geox_build_structural_candidates` |
| Confirmation bias | **Bias Audit Rule** | Pre-seal bias check mandatory |
| Overconfidence | **F7 Humility** | Ω₀ ∈ [0.03, 0.15] enforced |

### Constitutional Enforcement

| Floor | Bond-Based Implementation |
|-------|--------------------------|
| **F2 Truth** | 79% failure rate cited when confidence unchecked |
| **F7 Humility** | Expert status does not override uncertainty bands |
| **F9 Anti-Hantu** | DISPLAY-ONLY triggers HOLD (Bond proves experts fail) |
| **F13 Sovereign** | Human required precisely because experts fail 79% of the time |

---

## Study Details

### Participants
- **N = 184** professional geoscientists
- Experience: 2–30+ years
- Sectors: Oil & gas, mining, geotechnical

### Materials
- Synthetic seismic sections
- Deliberately ambiguous structures
- Known display artifacts

### Results

| Metric | Value |
|--------|-------|
| Overall accuracy | 21% |
| Confidence (incorrect) | High (avg 7.2/10) |
| Confidence (correct) | Similar (avg 7.5/10) |
| Disconfirming evidence sought | 12% |
| Multi-model consideration | 8% |

### The Devastating Conclusion

> *"The majority of expert interpreters were unable to distinguish between genuine geological structure and processing artifacts."*

> *"Confidence was not correlated with accuracy."*

> *"Years of experience did not protect against display bias."*

---

## Implications for AI

### Why This Matters for GEOX

**The Paradox:**
- AI trained on expert interpretations learns **expert biases**
- AI can replicate the 79% failure rate at scale
- **Unless** AI is explicitly designed to avoid anomalous contrast

### The GEOX Solution

```
Traditional AI:
Data → [Neural Net] → "Interpretation" → Overconfident wrong answer

GEOX-Governed AI:
Data → [ToAC Audit] → [Multi-Model] → [Bias Check] → [F7 Humility]
                              │
                              ▼
                    Confidence calibrated to uncertainty
                              │
                              ▼
                    888_HOLD if risk threshold exceeded
```

---

## Key Quotes

> *"Conceptual uncertainty in geoscience interpretation is poorly understood and rarely discussed."*

> *"The interpretive process itself introduces uncertainty that is separate from data uncertainty."*

> *"Experts are particularly vulnerable to conceptual uncertainty because their expertise enables rapid pattern recognition—which can be wrong."*

---

## Replication and Extension

### Follow-Up Studies

| Study | Finding | GEOX Implication |
|-------|---------|------------------|
| **Rankey & Mitchell (2010)** | 3D visualization reduces but doesn't eliminate bias | Multi-view required, not sufficient |
| **Macrae et al. (2016)** | Team interpretation only slightly better | Tri-witness (F3) still essential |
| **Bond et al. (2012)** | Training helps temporarily, decay over time | Continuous audit (F11) required |

### Industry Impact

- AAPG Hedberg Conference 2013: "Interpretation Uncertainty" theme
- SEG 2015: Special session on cognitive bias
- Major operators now require multi-interpreter review (Tri-witness)

---

## Related Pages

- [[10_THEORY/Theory_of_Anomalous_Contrast]] — ToAC core theory
- [[10_THEORY/Contrast_Canon]] — Physical vs Display vs Perceptual
- [[10_THEORY/Conflation_Taxonomy]] — Source→Transform→Proxy→Confidence
- [[50_TOOLS/geox_build_structural_candidates]] — Multi-model enforcement

---

## Reference

**Full Citation:**
```
Bond, C.E., Gibbs, A.D., Shipton, Z.K., & Jones, S. (2007). 
What do you think this is? "Conceptual uncertainty" in geoscience interpretation. 
GSA Today, 17(11), 4-10.
https://doi.org/10.1130/GSAT01711A.1
```

**PDF:** [[raw/papers/bond_2007.pdf]]

---

*Bond et al. (2007) — The empirical foundation of ToAC*  
*79% of experts fail. GEOX ensures accountability.*
