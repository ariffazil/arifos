---
name: apex-docs
description: "Harden and forge documentation with constitutional governance. Use when documenting code, hardening existing docs, fixing outdated or missing documentation, or running drift detection. Triggers: forge docs, apex docs, document this, harden documentation, doc drift, verify docs."
user-invocable: true
type: flow
---

# apex-docs — APEX Documentation Forge

Forges documentation that reduces entropy, preserves reversibility, and links evidence. Not generic "write good docs" — hardened docs with constitutional governance.

---

## 6-Phase APEX Flow

```
READ → RISK → REASON → FORGE → VERIFY → SEAL
```

| Phase | Action |
|-------|--------|
| **0. READ** | Read target file + git log; establish actual state |
| **1. RISK** | Classify doc gap by CVSS tier (Critical → Cosmetic) |
| **2. REASON** | Check F1 (reversible?), F2 (evidence?), F4 (clarity?) |
| **3. FORGE** | Edit minimally; one purpose per change; raw > perfect |
| **4. VERIFY** | Check links, no orphans, clarity read-aloud |
| **5. SEAL** | Commit + log to memory |

---

## Risk Tiers

| Tier | Indicator | Action |
|------|-----------|--------|
| **Critical** | Auth, payment, deletion undocumented | Immediate 888_HOLD |
| **High** | Public API mismatches code | Same-day fix |
| **Medium** | Internal helper outdated | Backlog |
| **Low** | Typo, formatting | Batch |
| **Cosmetic** | "Sounds better" rewrites | Skip (PROPA) |

---

## FORGE Rules

1. Edit, don't rewrite
2. One purpose per commit
3. No PROPA (polished performance with no substance)
4. Raw > Perfect

**New section template:**
```markdown
## <Section Name>
> Source: `<file>:<line-range>`
> Last verified: `<YYYY-MM-DD>`
> Ω₀: <0.03-0.05>

<Content>
**TODO:** <what's missing>
```

---

## Constitutional Constraints

| Floor | Rule |
|-------|------|
| **F1 Reversibility** | Git commit before edit; 60-second recovery path |
| **F2 Truth** | Every claim links to source; τ ≥ 0.99 |
| **F4 Clarity** | ΔS ≤ 0; Tables > Lists > Prose; no PROPA |
| **F7 Humility** | State Ω₀ uncertainty; mark TODOs explicitly |
| **F11 Command Auth** | Destructive actions (delete, rewrite) → propose first |
| **F13 Sovereignty** | Human veto is absolute |

---

## Anti-Patterns

| Anti-Pattern | Why | Alternative |
|--------------|-----|-------------|
| "Documentation sprint" | Bulk rewrite = irreversible | One file at a time |
| "Polish pass" | PROPA — no substance | Skip if content correct |
| AI writes, human skips review | Hallucination risk | Human must verify F2 |

---

## Drift Detection

**Weekly:** Scan for orphaned doc references.
**Monthly:** Compare code exports to doc coverage; flag undocumented public functions.

---

*Ditempa bukan diberi*
