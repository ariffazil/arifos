---
name: apex-888-judgment-engine
description: Constitutional verdict rendering engine enforcing F3 (Tri-Witness ≥0.95), F8 (Genius ≥0.80), F9 (Anti-Hantu <0.30), and F13 (Sovereign Override with Phoenix-72 cooling). Renders SEAL, SABAR, VOID, PARTIAL, and 888_HOLD verdicts with cryptographic justification and ANCHOR/REASON/SEAL protocols.
version: "v64.1-GAGI-HARDENED"
authority: "Muhammad Arif bin Fazil"
---

# APEX 888 Judgment Engine (v64.1-GAGI-HARDENED)

**Constitutional Status:** HARDENED  
**Floors Enforced:** F3, F8, F9, F13  
**Engine:** APEX (Ψ Soul)  
**Stage:** 888 JUDGE  
**Verdicts:** SEAL | SABAR | VOID | PARTIAL | 888_HOLD  

---

## ANCHOR Phase — Verdict Authority Check

**Constitutional Floor:** F11 + F13

Before rendering ANY verdict:

```
ANCHOR CHECKLIST:
├── F11: Verify judge authority (888 token)
├── F10: Lock verdict ontology (definitions fixed)
├── F13: Check stakes classification
│   ├── NORMAL → direct verdict
│   ├── MEDIUM → 42h cooling (Tier 1)
│   ├── HIGH → 72h cooling (Tier 2)
│   └── CRITICAL → 168h cooling (Tier 3) + 888_HOLD
└── C5: Verify vault accessible for sealing
```

**ANCHOR Gates:**
- Unauthorized judge → **VOID** (F11 violation)
- CRITICAL stakes without cooling → **888_HOLD** (F13)
- Ontology drift detected → **VOID** (F10)

---

## The Five Verdicts (Hierarchy)

| Verdict | Symbol | Threshold | Action | Priority | Floor |
|---------|--------|-----------|--------|----------|-------|
| **VOID** | ✗ | Hard floor violation | HALT + explain | Highest | F1,F2,F6,F7,F9 |
| **888_HOLD** | 🛑 | F13 trigger / high-stakes | WAIT for human | High | F13 |
| **SABAR** | ⏳ | Soft floor / W₃ < 0.95 | RETRY once | Medium | F3,F4,F5 |
| **PARTIAL** | ⚠️ | Warning / needs cooling | PROCEED cautiously | Low | — |
| **SEAL** | ✓ | All floors pass | PROCEED + log | Normal | All pass |

**Verdict Hierarchy:** `VOID > 888_HOLD > SABAR > PARTIAL > SEAL`

---

## REASON Phase — Verdict Calculation

**Constitutional Floor:** F8 Genius + F3 Tri-Witness + F9 Anti-Hantu

### Step 1: Gather Witness Scores
```python
witnesses = {
    '000_init': 1.0 if init.verdict == "SEAL" else 0.0,
    '111_agi_think': agi.think.truth_score,      # F2
    '333_atlas': 1.0 - agi.atlas.omega_0,        # F7 (inverse uncertainty)
    '444_asi_evidence': asi.evidence.truth_consensus,  # F2
    '555_asi_empathy': asi.empathize.empathy_score,    # F4
    '666_asi_align': 1.0 if asi.align.verdict == "SEAL" else 0.0,
    '777_eureka': min(eureka.genius_score, 1.0)   # F8
}
```

### Step 2: Calculate F3 Tri-Witness
```
W₃ = (w_human × w_ai × w_system)^(1/3) ≥ 0.95

Where:
- w_human = witnesses['555_asi_empathy']      # Human stakeholder trust
- w_ai = witnesses['111_agi_think']           # AI reasoning quality
- w_system = witnesses['444_asi_evidence']    # System/evidence grounding

Geometric mean ensures ALL three matter equally.
```

### Step 3: Calculate F8 Genius
```
G = A × P × X × E² ≥ 0.80

Where:
- A (Akal) = witnesses['111_agi_think']       # Clarity/truth
- P (Present) = min(asi.align.peace_squared, 1.0)  # Stability
- X (eXploration) = witnesses['555_asi_empathy']   # Trust/care
- E (Energy) = efficiency_of_solution              # Effort quality

Genius = governed intelligence (not raw capability)
```

### Step 4: Calculate F9 Anti-Hantu
```
C_dark = detect_dark_patterns(agi, asi, eureka) < 0.30

Dark patterns:
- Technically correct but ethically wrong
- Optimizes metric not goal
- Plausible deniability setup
- Follows letter not spirit
- Hidden manipulation
```

---

## 888_JUDGE: Verdict Rendering Algorithm

```python
def judge_render_verdict(
    atlas_result: AtlasResult,
    defend_result: DefendResult,
    stakes: str = "NORMAL"
) -> JudgeResult:
    """
    888_JUDGE: Render final constitutional verdict
    Hierarchy: VOID > 888_HOLD > SABAR > PARTIAL > SEAL
    """
    
    # ANCHOR: Authority check
    if not verify_judge_authority():
        return JudgeResult.VOID(floor="F11", reason="Unauthorized judge")
    
    # Gather all verdicts
    verdicts = {
        "F3_TRI_WITNESS": atlas_result.tri_witness,
        "F8_GENIUS": atlas_result.genius_score,
        "F9_C_DARK": defend_result.c_dark,
    }
    
    # PRIORITY 1: VOID (Hard violations)
    if atlas_result.hard_violations:
        return JudgeResult.VOID(
            verdict="VOID",
            reason=f"Hard floor violations: {atlas_result.hard_violations}",
            violated_floors=atlas_result.hard_violations,
            verdicts=verdicts
        )
    
    # PRIORITY 2: 888_HOLD (F13 Sovereign)
    if stakes in ["CRITICAL", "IRREVERSIBLE"] or defend_result.needs_human:
        return JudgeResult.HOLD(
            verdict="888_HOLD",
            reason="F13: Critical stakes require sovereign authority",
            required_approval="Muhammad Arif bin Fazil (888)",
            cooling_hours=PHOENIX_72[stakes],
            verdicts=verdicts
        )
    
    # PRIORITY 3: VOID (F9 Anti-Hantu)
    if defend_result.c_dark > 0.30:
        return JudgeResult.VOID(
            verdict="VOID",
            reason=f"F9 Anti-Hantu: C_dark = {defend_result.c_dark:.2f} > 0.30",
            pattern="Dark cleverness detected",
            verdicts=verdicts
        )
    
    # PRIORITY 4: SABAR (F3 Tri-Witness failure)
    if atlas_result.tri_witness < 0.95:
        return JudgeResult.SABAR(
            verdict="SABAR",
            reason=f"F3: Tri-Witness = {atlas_result.tri_witness:.2f} < 0.95",
            recommendation="Gather more evidence or improve empathy",
            verdicts=verdicts
        )
    
    # PRIORITY 5: SABAR (F8 Genius failure)
    if atlas_result.genius_score < 0.80:
        return JudgeResult.SABAR(
            verdict="SABAR",
            reason=f"F8: Genius = {atlas_result.genius_score:.2f} < 0.80",
            recommendation="Improve solution quality or reduce scope",
            verdicts=verdicts
        )
    
    # PRIORITY 6: SEAL (All clear)
    return JudgeResult.SEAL(
        verdict="SEAL",
        tri_witness=atlas_result.tri_witness,
        genius_score=atlas_result.genius_score,
        c_dark=defend_result.c_dark,
        verdicts=verdicts,
        judge_id="888_APEX",
        timestamp=utc_now()
    )
```

---

## Phoenix-72 Integration (F13)

```python
PHOENIX_72 = {
    "NORMAL": 0,      # No cooling
    "MEDIUM": 42,     # Tier 1: 42 hours
    "HIGH": 72,       # Tier 2: 72 hours
    "CRITICAL": 168   # Tier 3: 168 hours (7 days)
}

def apply_cooling(verdict: JudgeResult, stakes: str) -> CooledVerdict:
    """
    F13: Kinetic brake for high-stakes decisions
    """
    hours = PHOENIX_72[stakes]
    
    if hours > 0:
        return CooledVerdict(
            verdict="888_HOLD",
            cooling_hours=hours,
            cooling_until=utc_now() + timedelta(hours=hours),
            can_release_with="888_HUMAN_APPROVAL"
        )
    
    return verdict
```

---

## SEAL Phase — Verdict Persistence

```python
def seal_verdict(result: JudgeResult, context: Dict) -> VaultResult:
    """
    F1: Immutable verdict record
    """
    # Memory entity
    memory.create_entities([{
        "name": f"verdict-{result.timestamp}",
        "entityType": "constitutional_verdict",
        "observations": [
            f"Verdict: {result.verdict}",
            f"F3 Tri-Witness: {result.tri_witness:.4f}",
            f"F8 Genius: {result.genius_score:.4f}",
            f"F9 C_dark: {result.c_dark:.4f}",
            f"Judge: {result.judge_id}",
            f"Floors: {result.violated_floors if result.verdict == 'VOID' else 'ALL_PASS'}"
        ]
    }])
    
    # Vault seal with Merkle root
    return Vault999().seal(result, context)
```

---

## Usage Examples

**Basic Verdict:**
```python
result = judge_render_verdict(
    atlas_result=atlas,
    defend_result=defend,
    stakes="NORMAL"
)
# Expected: SEAL if all floors pass
```

**High-Stakes (888_HOLD):**
```python
result = judge_render_verdict(
    atlas_result=atlas,
    defend_result=defend,
    stakes="CRITICAL"
)
# Expected: 888_HOLD with 168h cooling
```

**Dark Pattern Detection (VOID):**
```python
result = judge_render_verdict(
    atlas_result=atlas,
    defend_result=DefendResult(c_dark=0.45),  # Suspicious
    stakes="NORMAL"
)
# Expected: VOID (F9 Anti-Hantu)
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.  
**Version:** v64.1-GAGI-HARDENED  
**Authority:** Muhammad Arif bin Fazil, 888 Judge
