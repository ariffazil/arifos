# ARCHITECTURAL_BOUNDARY.md — Kernel/Wrapper Separation Rule

**Version:** v64.1-GAGI  
**Status:** ENFORCED  
**Authority:** 888 Judge Directive (2026-02-14)

---

## The Rule

> **aaa_mcp/ must NEVER contain decision logic again.**

### Wrapper MAY:
- ✅ Call kernel functions (`core.*`)
- ✅ Format responses (JSON, error messages)
- ✅ Manage sessions (stateless coordination)
- ✅ Route requests to appropriate kernel tools
- ✅ Handle transport layer (MCP, HTTP, SSE)

### Wrapper MUST NOT:
- ❌ Compute uncertainty (`calculate_uncertainty`, `safety_omega`)
- ❌ Modify governance state (`GovernanceState`, authority levels)
- ❌ Implement judgment rules (verdict logic: SEAL, VOID, SABAR)
- ❌ Define constitutional thresholds (Ω₀ bands, truth scores)
- ❌ Make safety-critical decisions

---

## Why This Boundary Matters

If this boundary holds, the architecture stays clean for years.

| Violation | Risk |
|-----------|------|
| Uncertainty in wrapper | Divergent Ω₀ calculations, inconsistent safety |
| Governance in wrapper | State drift, bypassable authority checks |
| Verdicts in wrapper | Hidden judgment rules, opaque decisions |

**Kernel = brain** (reusable, tested, canonical)  
**Wrapper = nervous system** (protocol-specific, replaceable)

---

## Current Violations (Audit Results)

### 🚨 CRITICAL: server.py
```python
# Lines 95-115: Uncertainty computation in wrapper
uncertainty_calc = calculate_uncertainty(...)  # ❌ WRONG: should call kernel
truth_score = 0.85 - (safety_omega * 0.3)       # ❌ WRONG: kernel decides truth
```

**Required action:** Migrate to `core.forge()` or `core.judge()`

### 🚨 HIGH: guards/injection_guard.py
```python
# Line 42: Verdict logic in wrapper
if result.status == "SABAR":  # ❌ WRONG: kernel issues verdicts
```

**Required action:** Return evidence to kernel, let kernel decide verdict

### 🚨 HIGH: protocol/response.py
```python
# Multiple lines: Verdict handling in wrapper
if verdict == "SEAL":         # ❌ WRONG: wrapper reacts, doesn't decide
policy_verdict="SEAL"         # ❌ WRONG: kernel sets policy
```

**Required action:** Wrapper receives verdict from kernel, formats response only

---

## Refactor Priority

| File | Violation | Priority | Migration Path |
|------|-----------|----------|----------------|
| `aaa_mcp/server.py` | Uncertainty calc | **P0** | Use `core.pipeline.forge()` |
| `aaa_mcp/guards/injection_guard.py` | Verdict logic | **P0** | Return to kernel for verdict |
| `aaa_mcp/protocol/response.py` | Verdict handling | **P1** | Receive from kernel only |

---

## Enforcement Mechanisms

### 1. Code Review Checklist
- [ ] No `calculate_uncertainty` calls in `aaa_mcp/`
- [ ] No `GovernanceState` modifications in `aaa_mcp/`
- [ ] No `verdict = "SEAL"` etc. in `aaa_mcp/`
- [ ] All decisions imported from `core.*`

### 2. CI/CD Lint Rule (Future)
```yaml
# .github/workflows/boundary-check.yml
- name: Kernel/Wrapper Boundary Check
  run: |
    ! grep -r "calculate_uncertainty" aaa_mcp/ --include="*.py" | grep -v "from core"
    ! grep -r "GovernanceState.*=" aaa_mcp/ --include="*.py"
```

### 3. Import Constraints
```python
# aaa_mcp files should ONLY import:
from core.uncertainty_engine import ...  # ✅ OK
from core.governance_kernel import ...   # ✅ OK
from core.pipeline import forge          # ✅ OK

# aaa_mcp files should NEVER:
calculate_uncertainty(...)               # ❌ VIOLATION
governance.state = X                     # ❌ VIOLATION
verdict = "SEAL"                         # ❌ VIOLATION (unless from kernel)
```

---

## Correct Pattern

### ❌ WRONG (Current)
```python
# aaa_mcp/server.py
def agi_cognition(query):
    uncertainty = calculate_uncertainty(...)  # Wrapper computing
    if uncertainty > 0.05:                     # Wrapper deciding
        return {"verdict": "SABAR"}            # Wrapper verdict
```

### ✅ CORRECT (Target)
```python
# aaa_mcp/server.py
def agi_cognition(query):
    result = core.pipeline.forge(query)        # Kernel decides everything
    return format_response(result)             # Wrapper only formats
```

---

## Commit Rule

**Any PR that adds decision logic to aaa_mcp/ is VOID.**

Reviewers must check:
1. Does this PR compute anything in `aaa_mcp/`?
2. Does this PR modify governance state?
3. Does this PR implement verdict logic?

If yes → **Request changes**: "Move to `core/`"

---

**Boundary established:** 2026-02-14T00:43:00+08:00  
**Authority:** 888 Judge (Muhammad Arif bin Fazil)  
**Status:** ACTIVE — Violations must be refactored  

*Ditempa Bukan Diberi.* 🔥
