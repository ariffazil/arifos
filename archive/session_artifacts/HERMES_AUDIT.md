# HERMES — arifOS Repo Architecture Audit
**Branch:** `cleanup/unix-style-2026-04-23`
**Authority:** arifOS_bot as Hermes normalization agent
**Epoch:** EPOCH-2026-04-23

---

## A. Architecture Truth Summary

### What the repo actually is

**arifOS** is a constitutional MCP kernel for governed AI execution. It provides:
- A Python MCP server (`arifosmcp/`) with 13 canonical tools
- A constitutional runtime (`core/`) enforcing F0–F13 floors
- An agent execution framework (`agentzero/`)
- An observability layer (Nine-Signal, Prometheus)

### Main runtime path

```
MCP Request → arifosmcp/server.py (stdio_server.py)
           → arifosmcp/runtime/kernel_core.py (or kernel_runtime.py)
           → core/governance_kernel.py (F1–F13 enforcement)
           → core/judgment.py (888_JUDGE verdict)
           → arifosmcp/tools/ (canonical tools)
           → response
```

### Main control boundaries

| Boundary | Owner | Files |
|----------|-------|-------|
| Transport ingress | `arifosmcp/stdio_server.py` | MCP stdio |
| Middleware / governance | `core/governance_kernel.py` | F1–F13 floors |
| Verdict authority | `core/judgment.py` | 888_JUDGE |
| Tool implementation | `arifosmcp/tools/` | 13 canonical tools |
| Vault / audit | `core/vault999/` | MerkleV3 ledger |

---

## B. Naming Audit

### Critical Issues Found

#### 1. ROOT CHAOS — 50+ files at root (PRIORITY 1)
**Problem:** Docs, reports, session artifacts, and configs all at root. Unreadable.

**Files to move to `docs/`:**
- `BENCHMARK_REPORT.md`, `CHATGPT_DEPLOYMENT_GUIDE.md`, `CONTRAST_ANALYSIS_2026-04-12.md`
- `DEPLOYMENT.md`, `DEPLOYMENT_SUMMARY.md`, `ENV_VARS.md`, `FRAMEWORK_SUPPORT.md`
- `MCP_A2A_MAP.md`, `MCP_SITES_SEAL.md`, `MCP_TOOLS_README.md`
- `REGISTRY.md`, `ROADMAP.md`, `SEALING_CHECKLIST.md`, `TOOL_NAMESPACING.md`
- `SESSION_SEAL.md`, `SESSION_SEAL_2026-04-12.md`
- `VPS_BOOTSTRAP.md`, `VPS_CONTRAST_ANALYSIS_999_SEAL.md`
- `TODO.md`, `DISCOVERY.md`

**Status:** Already partially done in Phase 1 on the surgery branch. This list reflects full root state.

#### 2. FLOORS DUPLICATION — 2 versions, 1738 lines total (PRIORITY 2)
**Problem:**
- `core/floors.py` — 677 lines (referenced in docs as canonical)
- `core/shared/floors.py` — 1061 lines (larger, appears to be working version)

Both implement floor logic. `core/shared/floors.py` seems more complete.
`core/shared/floors.py` doesn't exist as an importable module — it appears as an alias/reference.

**Decision:** Keep `core/shared/floors.py` as canonical. Add shim at `core/floors.py`:
```python
# DEPRECATED — use core.shared.floors
from core.shared.floors import *  # forward-compat shim
```

#### 3. MEGATOOLS LEGACY — 12 files (PRIORITY 3)
**Problem:** `arifosmcp/runtime/megaTools/` contains legacy 44-tool implementations. Canonical tools now live in `arifosmcp/tools/`. MegaTools is dead code.

**Decision:** Move to `_archived/megaTools_legacy/` with index.

#### 4. MULTIPLE CONTRACTS DUPLICATION
**Files:**
- `arifosmcp/contracts/artifacts.py`
- `arifosmcp/contracts/continuity.py`
- `arifosmcp/contracts/envelopes.py` (39 lines — thin wrapper)
- `arifosmcp/contracts/identity.py`
- `arifosmcp/contracts/verdicts.py`
- `arifosmcp/runtime/contracts.py`
- `arifosmcp/runtime/contracts_v2.py`
- `arifosmcp/runtime/envelope.py` (39 lines — duplicate of contracts/envelopes.py)

**Decision:**
- Merge `runtime/envelope.py` → `contracts/envelopes.py` (envelopes is the canonical name, singular)
- `contracts/artifacts.py` and `contracts/continuity.py` → keep as-is (legitimate separate concerns)
- `runtime/contracts.py` vs `runtime/contracts_v2.py` → `contracts_v2` replaces `contracts`; add compatibility shim

#### 5. SCHEMA DUPLICATION
**Files:**
- `arifosmcp/runtime/schemas.py`
- `arifosmcp/specs/tool_specs.py`
- `arifosmcp/specs/contracts.py`
- `arifosmcp/specs/prompt_specs.py`
- `arifosmcp/specs/resource_specs.py`

**Decision:** Keep `specs/tool_specs.py` as canonical tool schema. `runtime/schemas.py` → rename to `runtime/schema.py` (singular) and keep as runtime schema processing layer. Investigate overlap before merging.

#### 6. RUNTIME OVERLAP — Kernel files
**Files:**
- `runtime/kernel_core.py`
- `runtime/kernel_router.py`
- `runtime/kernel_runtime.py`
- `runtime/orchestrator.py`

**Decision:** `kernel_router.py` and `kernel_runtime.py` both route/execute. Merge into `kernel.py` (singular, canonical). `kernel_core.py` appears to be the actual core — keep. `orchestrator.py` → keep as separate concern (orchestration vs kernel). Add compatibility shims.

#### 7. PLURAL FILENAMES — canonical singular forms needed
- `arifosmcp/contracts/envelopes.py` → `envelope.py`
- `arifosmcp/runtime/schemas.py` → `schema.py`
- `arifosmcp/evals/breach_test_runner.py` — already singular ✅
- `arifosmcp/runtime/sessions.py` → `session.py`
- `arifosmcp/runtime/contracts.py` → keep, but `contracts_v2.py` replaces it

---

## C. Migration Plan

### Phase 1 (Safe — no behavior change)

1. **Move root chaos files → `docs/`** (Phase 1 already done in surgery branch)
2. **Archive MegaTools** → `_archived/megaTools_legacy/`
3. **Add compatibility shims** for renamed files

### Phase 2 (Medium risk — add shims)

4. **Canonical floors** → keep `core/shared/floors.py`, add shim at `core/floors.py`
5. **Merge `runtime/envelope.py` → `contracts/envelopes.py`**
6. **Rename `runtime/schemas.py` → `runtime/schema.py`**
7. **Merge `kernel_router.py` + `kernel_runtime.py` → `kernel.py`**

### Phase 3 (Higher risk — requires import graph analysis)

8. Consolidate `runtime/contracts.py` + `contracts_v2.py`
9. Clean up `specs/` vs `runtime/` schema overlap

---

## D. Implementation

### Phase 1 — Root chaos + MegaTools archive

```bash
# Move docs from root
mkdir -p docs/governance docs/deployment docs/analysis docs/audits

# Move these (already done in surgery branch, ensure consistency)
# Archive MegaTools
mkdir -p _archived/megaTools_legacy
mv arifosmcp/runtime/megaTools/ _archived/megaTools_legacy/

# Add compatibility shims for plural → singular renames
```

### Phase 2 — Compatibility shims

For every file that gets renamed/merged, add a shim in the old location:

```python
# Old location — DEPRECATED shim
# Use: new.location instead
from new.location import *
import warnings
warnings.warn("old.plural.name is deprecated. Use new.singular.name", DeprecationWarning)
```

---

## E. Technical Debt

| Debt | Severity | Notes |
|------|----------|-------|
| `core/shared/floors.py` not importable as module | High | Should be `core/shared/floors/__init__.py` |
| `kernel_router.py` + `kernel_runtime.py` overlap | Medium | Both do routing — should merge |
| `specs/` vs `runtime/schemas.py` overlap | Medium | Two schema definitions — need dedup |
| `.archive` dirs throughout (22 files) | Low | Legacy, can stay |
| `philosophy*.py` files | Low | Policy layer, keep |
| `truth_pipeline_hardened.py` | Medium | References old tool names |

---

## Rollback Plan

Each change is a separate commit. Rollback via:
```bash
git revert <commit-hash>
```

Branches are safe — all work on `cleanup/unix-style-2026-04-23`. Do not force-push this branch.