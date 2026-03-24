# Constitutional GitOps Toolchain — Deployment Plan

**PR:** `feature/constitutional-gitops` → `main`  
**Scope:** Add F1-F13 enforcement at filesystem layer  
**Risk:** Low (new tools, no existing code changes)

---

## Files Added

```
scripts/constitutional-gitops/
├── README.md                    # Toolchain documentation
├── arifos-worktree-add.sh       # F1 sandbox creator
├── arifos-worktree-remove.sh    # VOID execution
├── arifos-agent-run.sh          # Agent runtime wrapper
├── arifos-f3-eval.sh            # Bash F3 evaluator
└── arifos_f3_eval.py            # Python CLI (spec-compliant)

templates/
└── arifos.yml.template          # Constitutional manifest schema

.github/workflows/
└── 888-judge.yml                # CI enforcement (NEW)
```

---

## Commit Message

```
feat: constitutional git worktree toolchain (F1-F13)

Add filesystem-level governance for AI agent development:

- arifos-worktree-add.sh: Create F1-compliant agent sandboxes
- arifos-worktree-remove.sh: Collapse rejected universe → VOID
- arifos-agent-run.sh: Agent runtime with F7 dry_run enforced
- arifos-f3-eval.sh: Tri-Witness bash evaluator
- arifos_f3_eval.py: Python CLI with exact Perplexity spec
  - Exit 0: executed (any verdict)
  - Exit 1: config error (no arifos.yml)
  - Exit 2: --enforce violated
- templates/arifos.yml.template: Constitutional manifest schema
- .github/workflows/888-judge.yml: PR = 888_JUDGE enforcement

F3 Tri-Witness: W₃ = (H × A × E)^(1/3)
Thresholds: low=0.85, medium=0.95, high=0.99, critical=1.0

Verdicts: SEAL | PROVISIONAL | SABAR | HOLD | HOLD_888 | VOID

Closes: constitutional-gitops-milestone
```

---

## Rollout Plan (Perplexity Phase 1-3)

### Phase 1: Soft (This PR)
- [ ] Merge tooling to main
- [ ] Use locally for new branches
- [ ] 888_JUDGE runs advisory mode (comments only)

### Phase 2: Strict Governance Paths
- [ ] Require 888_JUDGE for PRs touching:
  - `0_KERNEL/`
  - `000_THEORY/`
  - `AGENTS/`
  - Any F1-F13 floor definitions

### Phase 3: Agent Integration
- [ ] Bake `arifos-f3-eval` into MCP skills
- [ ] Agents must pass F3 locally before PR

---

## Testing Checklist

```bash
# Test 1: Create sandbox
./scripts/constitutional-gitops/arifos-worktree-add.sh test feature-test

# Test 2: F3 evaluation
cd ../arifos-worktrees/arifos-test-feature-test
/mnt/arifos/scripts/constitutional-gitops/arifos_f3_eval.py --worktree .

# Test 3: Clean up
/mnt/arifos/scripts/constitutional-gitops/arifos-worktree-remove.sh feature/test-feature-test
```

---

## F1-F13 Coverage Map

| Floor | Tool | Enforcement |
|-------|------|-------------|
| F1 | worktree-add/remove | Reversible sandboxes |
| F2 | worktree-add, 888-judge | Main locked, τ ≥ 0.99 |
| F3 | f3-eval, 888-judge | Tri-Witness W₃ ≥ 0.95 |
| F4 | worktree-add | Naming convention |
| F5 | worktree-list | State visibility |
| F7 | agent-run, f3-eval | dry_run default |
| F11 | worktree-add | Command separation |
| F12 | worktree-add | .gitignore injection |
| F13 | 888-judge.yml | Arif merge rights |

---

*Ditempa bukan diberi.* 🔥
