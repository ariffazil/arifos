: "# Seals and Verdicts

> **Type:** Governance  
> **Epistemic Level:** INT (interpreted decision)  
> **Confidence:** Variable per verdict  
> **Certainty Band:** [0.00, 1.00]  
> **Tags:** [governance, verdicts, seals, f1, f2, confidence]  
> **arifos_floor:** F1, F2  

---

## Purpose

Define the **verdict system** that governs all GEOX outputs. Every evaluation receives a verdict that determines:
- Whether output can be used downstream
- Whether human review is required
- Whether the result is auditable

**Verdicts are not arbitrary** — they are calculated from floor compliance, confidence bands, and epistemic levels.

---

## The Five Verdicts

```
┌─────────────────────────────────────────────────────────────┐
│                    GEOX VERDICT HIERARCHY                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   SEAL ████████████████████  τ ≥ 0.80                       │
│        Auto-proceed, full confidence                        │
│                                                              │
│   PARTIAL ████████████████   τ ≥ 0.50                       │
│        Proceed with caveats, review recommended             │
│                                                              │
│   SABAR ██████████           τ ≥ 0.25                       │
│        Hold — gather more data (Sabar = Malay "patience")   │
│                                                              │
│   VOID ██                    τ < 0.25                       │
│        Block — contradictions detected                      │
│                                                              │
│   REVIEW ?                   Insufficient data to evaluate  │
│        Queue for expert review                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Verdict Calculation

### Formula

```
τ = confidence × floor_compliance × epistemic_weight

Where:
- confidence ∈ [0, 1] — tool-specific confidence
- floor_compliance ∈ [0, 1] — % of floors passed
- epistemic_weight: OBS=1.0, DER=0.9, INT=0.8, SPEC=0.6
```

### Example Calculation

| Component | Value | Weight | Contribution |
|-----------|-------|--------|--------------|
| Confidence | 0.85 | — | 0.85 |
| Floor Compliance | 5/6 passed | 0.83 | ×0.83 |
| Epistemic Level | INT | 0.8 | ×0.8 |
| **τ (Final)** | **0.56** | — | **PARTIAL** |

---

## Verdict Definitions

### SEAL (τ ≥ 0.80)

**Color:** Green  
**Icon:** 🔒  
**Action:** Auto-proceed

**Criteria:**
- Confidence ≥ 0.85
- All critical floors passed
- Epistemic level: OBS or DER
- No 888_HOLD triggers
- Evidence trail complete

**Usage:**
- Routine data loading
- Well-established interpretation
- Low-stakes decisions

**Audit Trail:**
```json
{
  "verdict": "SEAL",
  "tau": 0.88,
  "confidence": 0.90,
  "floor_compliance": 1.0,
  "epistemic_level": "DER",
  "seal_id": "SEAL_2026_0089",
  "expires": null
}
```

---

### PARTIAL (τ ≥ 0.50)

**Color:** Yellow  
**Icon:** ⚠️  
**Action:** Proceed with caveats

**Criteria:**
- Confidence ≥ 0.60
- Most floors passed (≥70%)
- Minor violations acceptable
- Human review recommended but not required

**Caveats:**
- Document limitations
- Flag for periodic review
- Consider alternative interpretations

**Usage:**
- Interpretation with uncertainty
- Prospects with mixed signals
- Preliminary evaluations

**Audit Trail:**
```json
{
  "verdict": "PARTIAL",
  "tau": 0.65,
  "confidence": 0.72,
  "floor_compliance": 0.83,
  "epistemic_level": "INT",
  "caveats": [
    "Seal confidence below threshold",
    "Alternative interpretation possible"
  ],
  "review_by": "2026-05-08T00:00:00Z"
}
```

---

### SABAR (τ ≥ 0.25)

**Color:** Orange  
**Icon:** ⏸️  
**Action:** Hold — gather more data

**Etymology:** *Sabar* (صبر) — Malay/Arabic for "patience" — the wisdom to wait for better data.

**Criteria:**
- Confidence 0.40–0.60
- Significant floor violations
- Missing critical data
- High uncertainty acceptable range

**Actions:**
- PAUSE workflow
- Identify data gaps
- Suggest acquisition priorities
- Schedule re-evaluation

**Usage:**
- Early exploration with limited data
- Conflicting interpretations
- Data quality issues

**Audit Trail:**
```json
{
  "verdict": "SABAR",
  "tau": 0.42,
  "confidence": 0.55,
  "floor_compliance": 0.67,
  "epistemic_level": "SPEC",
  "data_gaps": [
    "No well control on seal",
    "Seismic quality poor below 3.5s"
  ],
  "recommended_actions": [
    "Acquire well on flank",
    "Reprocess seismic with focused imaging"
  ],
  "revisit_date": "2026-07-01T00:00:00Z"
}
```

---

### VOID (τ < 0.25)

**Color:** Red  
**Icon:** 🚫  
**Action:** Block — contradictions detected

**Criteria:**
- Confidence < 0.40
- Critical floor violations
- Geologically impossible
- Contradictions in evidence

**Actions:**
- REJECT output
- Halt dependent workflows
- Log contradiction in [[90_AUDITS/Contradiction_Log]]
- Require rework from different approach

**Usage:**
- Anomalous contrast violations
- Physically impossible structures
- Fundamental errors

**Audit Trail:**
```json
{
  "verdict": "VOID",
  "tau": 0.18,
  "confidence": 0.35,
  "floor_compliance": 0.50,
  "epistemic_level": "SPEC",
  "contradictions": [
    "Display contrast 4.2x physical contrast",
    "Dip angle 65° exceeds plausible range",
    "Closure inconsistent with regional dip"
  ],
  "violation_type": "F9_Anti_Hantu",
  "requires": "Complete reinterpretation"
}
```

---

### REVIEW

**Color:** Gray  
**Icon:** 🔍  
**Action:** Queue for expert review

**Criteria:**
- Insufficient data for automated verdict
- Novel situation not in training
- Complex multi-factor decision

**Usage:**
- First-of-kind analysis
- Multi-disciplinary integration
- Edge cases

---

## Verdict by Use Case

| Use Case | Typical Verdict | Threshold | Notes |
|----------|----------------|-----------|-------|
| Seismic loading | SEAL | τ ≥ 0.95 | OBS level, minimal risk |
| Structural interp | PARTIAL | τ ≥ 0.60 | INT level, ambiguity present |
| Prospect risking | PARTIAL/SABAR | τ ≥ 0.50 | SPEC level, high uncertainty |
| Conflation audit | SEAL/VOID | Binary | Pass/fail on F9 |
| Material query | SEAL | τ ≥ 0.90 | DER level, well-established |

---

## Verdict Transitions

```
SEAL ←──[new data]── PARTIAL ←──[new data]── SABAR
  │                      │                       │
  └──[degradation]───────┴──[degradation]───────┘

VOID ←──[correction]── ANY VERDICT
```

**Degradation Triggers:**
- New contradictory data
- Discovery of data quality issues
- Updated geological model

**Upgrade Path:**
- Additional well control
- Better seismic imaging
- Independent validation

---

## Seal Registry

All SEAL verdicts are recorded:

| Seal ID | Timestamp | Tool | Prospect/Case | τ | Expires |
|---------|-----------|------|---------------|-----|---------|
| SEAL_2026_0089 | 2026-04-08T10:30:00Z | geox_load_seismic_line | Malay_Basin_3D | 0.95 | Never |
| SEAL_2026_0088 | 2026-04-07T14:22:00Z | geox_query_ratlas | Material lookup | 0.92 | Never |

**Seal Expiration:**
- Data loading seals: Never expire (OBS level)
- Interpretation seals: 90 days or until new data
- Prospect seals: Until drilled or data update

---

## Integration

- **Calculation:** Performed by all [[50_TOOLS/*]]
- **Logging:** [[70_GOVERNANCE/Floor_Enforcement_Log]]
- **Audit:** [[arifos::999_VAULT]]
- **Reporting:** [[90_AUDITS/Weekly_Lint_Reports]]

---

## Philosophical Anchor

> **F1 Amanah** — "No irreversible action without seal"

The verdict system is the implementation of F1. It ensures that trust (amanah) is earned through evidence, not assumed through automation.

> **F2 Truth** — "No ungrounded claims"

τ (tau) is the mathematical expression of truth probability. It forces explicit acknowledgment of uncertainty.

---

*GEOX Seals and Verdicts v1.0.0 · arifOS Constitutional Federation · DITEMPA BUKAN DIBERI*