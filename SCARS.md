# SCARS.md — Constitutional Battle Scars

## SCAR-001: The Mock Test Trap (2026-02-14)

### The Wound
**Claim:** "5 tests passing, core works"
**Reality:** τ ≈ 0 — tests mocked infrastructure, no real enforcement verified
**Discovery:** FastMCP v2 FunctionTool not callable directly, PostgreSQL missing, 178 tests failing

### The Pain
- F2 Truth violated (false confidence)
- F7 Humility forgotten (Ω₀ elevated)
- Time wasted on W@W/router before core verified

### The Lesson
> "Tests yang pass tanpa infrastructure adalah lebih berbahaya daripada code yang fail."

**New Rule (F2 Enforcement):**
- Setiap "works" claim mesti 3 witnesses:
  1. Human manual check (888 Judge)
  2. AI cross-reference (self-consistency)
  3. Infrastructure proof (real DB, real network)

### The Recovery
- Phase 0.1: Constitutional bootstrap (extract truth)
- Phase 1.1: Forensic audit (categorize 178 failures)
- Phase 1.2: MCP protocol verification (真功夫 confirmed)

### Prevention
**Mock Detector:** Add check dalam AAA untuk detect MOCK mode vs REAL mode.

```python
if CONFIG['mode'] == ConstitutionalMode.MOCK:
    raise ConstitutionalViolation(
        "F2 Truth: Running in mock mode. "
        "Cannot verify real enforcement."
    )
```

### Healed
**Date:** 2026-02-14  
**Status:** Core validated, foundation solid  
**Nonce:** v65.0-truth-003

---

*DITEMPA DARI KEGAGALAN INI* 🔥
