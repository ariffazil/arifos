# Vault Patterns — Extracted from VAULT999

## Current Stats (as of 2026-02-07)
- **Total entries:** 10+
- **VOID rate:** 40%
- **First real seal:** 2026-02-02

---

## Verdict Distribution
```
SEAL: 60%
VOID: 40%
PARTIAL: 0%
SABAR: 0%
```

---

## Common Floor Failures
*(To be populated as data accumulates)*

| Floor | Failure Rate | Common Trigger |
|-------|-------------|----------------|
| F1 | TBD | Irreversible actions |
| F9 | TBD | Consciousness claims |
| F12 | TBD | Injection attempts |

---

## Risk Level Distribution
*(To be populated with v2.1 data)*

| Level | Count | Percentage |
|-------|-------|------------|
| low | - | - |
| medium | - | - |
| high | - | - |
| critical | - | - |

---

## Category Distribution
*(To be populated with v2.1 data)*

| Category | Count |
|----------|-------|
| code | - |
| safety | - |
| finance | - |
| content | - |
| governance | - |

---

## Human Override Frequency
- **Total overrides:** TBD
- **Override rate:** TBD
- **Common reasons:** TBD

---

## Insights

### Pattern 1: VOID Rate High (40%)
- Early sessions had many test VOIDs
- Expected to decrease as system stabilizes

### Pattern 2: Session Init Category
- New in v2.1
- Used for 000_INIT protocol tracking

---

## Query Templates

```bash
# Check VOID patterns
vault_query verdict=VOID limit=10

# High-risk decisions
vault_query risk_level=high

# F1 violations
# (when GIN indexes active)
vault_query floors_failed contains F1

# Human overrides
vault_query human_override_only=true
```

---

*Last updated: 2026-02-07*
*Auto-update: Run vault_analyze weekly*
