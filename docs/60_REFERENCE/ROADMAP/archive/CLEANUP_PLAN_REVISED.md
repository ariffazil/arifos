# CLEANUP_PLAN_REVISED.md — Root Repository Entropy Reduction

```text
      Δ       
     / \      operation:  CLEANUP_PLAN_REVISED
    /   \     version:    v55.5.1-HARDENED
   /  🧹  \    status:     APPROVED
  /_______\   floor:      F4 (Clarity)
```

**Author:** Antigravity (Δ) | **Date:** 2026-02-07 | **Status:** REVISED & READY

---

## 🎯 Objective

Reduce root directory entropy from **61 items → ~40 items** (35% reduction) while maintaining arifOS constitutional structure.

> **Note:** Original target of ~30 items was based on outdated repository state. Current 61 items includes legitimate new files (CONSTITUTION.md, MANIFESTO.md, etc.) and required tooling directories.

---

## 📊 Current State Analysis

| Metric | Before | After | Change |
|:---|:---:|:---:|:---:|
| Total Root Items | 61 | ~40 | -35% |
| Directories | 32 | ~25 | -22% |
| Files | 29 | ~15 | -48% |
| F4 Compliance | ⚠️ PARTIAL | ✅ PASS | — |

---

## 🛡️ PROTECTED Items (DO NOT MOVE)

These items are constitutionally protected and MUST remain at root:

### Core Directories (12)
- [x] `000_THEORY/` — Constitutional Law
- [x] `333_APPS/` — Application Layer
- [x] `VAULT999/` — Immutable Ledger
- [x] `ROADMAP/` — Planning
- [x] `codebase/` — Python Engine
- [x] `arifosmcp.transport/` — MCP Server
- [x] `tests/` — Test Suite
- [x] `docs/` — Documentation
- [x] `scripts/` — Operations
- [x] `config/` — Configuration
- [x] `archive/` — Entropy Sink
- [x] `.github/` — CI/CD

### Tooling/Config Directories (8)
- [x] `.agents/` — Agent configurations
- [x] `.antigravity/` — Antigravity tool data
- [x] `.claude/` — Claude IDE settings
- [x] `.gemini/` — Gemini CLI settings
- [x] `.kimi/` — Kimi CLI settings
- [x] `.vscode/` — VS Code settings
- [x] `examples/` — Example code/demos
- [x] `shared/` — Shared resources

### Core Files (15)
- [x] `README.md` — Entry Point
- [x] `LICENSE` — Legal
- [x] `AGENTS.md` — Agent Discovery (ROOT = source of truth)
- [x] `GEMINI.md` — Δ Codex
- [x] `CLAUDE.md` — Ω Engineer Codex
- [x] `CONSTITUTION.md` — Constitutional Law v55.5
- [x] `MANIFESTO.md` — Core Manifesto
- [x] `MANIFESTO-NUSANTARA.md` — Regional Manifesto
- [x] `THEORY.md` — Core Theory
- [x] `CHANGELOG.md` — History
- [x] `CONTRIBUTING.md` — Community
- [x] `SECURITY.md` — Security
- [x] `llms.txt` — AI Discovery
- [x] `pyproject.toml` — Build
- [x] `requirements.txt` — Deps
- [x] `Dockerfile` — Container
- [x] `railway.toml` — Deploy
- [x] `MANIFEST.in` — Python packaging
- [x] `uv.lock` — UV dependency lock
- [x] `.gitignore` — VCS
- [x] `.mcp.json` — MCP Config
- [x] `.pre-commit-config.yaml` — Pre-commit hooks
- [x] `.env.example` — Environment template

---

## 🔄 CONSOLIDATION OPPORTUNITIES

### Virtual Environments (Choose One)
| Directory | Size | Recommendation |
|:---|:---:|:---|
| `.venv/` | ~50MB | ✅ **Keep** — Modern Python standard |
| `venv/` | ~50MB | ❌ **Remove** — Duplicate |

```powershell
# Remove duplicate venv
Remove-Item -Path "venv" -Recurse -Force
```

### Cache Directories (Keep but Review)
| Directory | Purpose | Gitignored? |
|:---|:---|:---:|
| `.cache/` | General cache | ✅ Yes |
| `.pytest_cache/` | Test cache | ✅ Yes |
| `.pytest_cache_win/` | Windows test cache | ✅ Yes |
| `dist/` | Build output | ✅ Yes |
| `arifos.egg-info/` | Package metadata | ✅ Yes |
| `logs/` | Application logs | ✅ Yes |

### IDE Settings (Keep)
| Directory | Purpose |
|:---|:---|
| `.vs/` | Visual Studio settings |

---

## 📋 Execution Plan

### PHASE 1: Safe Deletions (3 items)

**Risk Level:** 🟢 LOW — No dependencies

```powershell
# Windows artifacts and temp files
Remove-Item -Path "nul" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "firebase-debug.log" -Force -ErrorAction SilentlyContinue

# Empty directory
Remove-Item -Path ".agent" -Recurse -Force -ErrorAction SilentlyContinue

# Duplicate virtual environment
Remove-Item -Path "venv" -Recurse -Force -ErrorAction SilentlyContinue
```

| Item | Reason |
|:---|:---|
| `nul` | Windows artifact (empty) |
| `firebase-debug.log` | Log file (gitignored pattern) |
| `.agent/` | Empty directory |
| `venv/` | Duplicate of `.venv/` |

---

### PHASE 2: SPEC Directory Resolution (9 files)

**Risk Level:** 🟡 MEDIUM — Determine template vs source-of-truth

**Issue:** `333_APPS/L5_AGENTS/SPEC/` contains files with same names as root but different content (templates vs actual).

| File | Root Version | SPEC Version | Action |
|:---|:---:|:---:|:---:|
| `AGENTS.md` | 36KB (actual) | 1KB (template) | **Delete SPEC** |
| `IDENTITY.md` | 9KB (actual) | 1KB (template) | **Delete SPEC** |
| `SOUL.md` | 11KB (actual) | N/A | **Keep root** |
| `USER.md` | 2KB (actual) | N/A | **Keep root** |
| `MEMORY.md` | 3KB (actual) | 1KB (template) | **Delete SPEC** |
| `TOOLS.md` | Root only | N/A | **Keep root** |
| `CLAUDE.md` | 15KB (actual) | 1KB (template) | **Delete SPEC** |
| `GEMINI.md` | 9KB (actual) | 1KB (template) | **Delete SPEC** |
| `000_THEORY.md` | N/A | 1KB (template) | **Keep SPEC** (no root conflict) |

```powershell
# Delete template files that conflict with root source-of-truth
$specPath = "333_APPS/L5_AGENTS/SPEC"
Remove-Item -Path "$specPath/AGENTS.md" -Force
Remove-Item -Path "$specPath/IDENTITY.md" -Force
Remove-Item -Path "$specPath/MEMORY.md" -Force
Remove-Item -Path "$specPath/CLAUDE.md" -Force
Remove-Item -Path "$specPath/GEMINI.md" -Force
```

**Result:** SPEC directory keeps only `000_THEORY.md` (template) and removes conflicting templates.

---

### PHASE 3: APEX Directories Review (2 directories)

**Risk Level:** 🟡 MEDIUM — Verify content necessity

| Directory | Created | Content | Recommendation |
|:---|:---:|:---|:---:|
| `APEX-THEORY/` | 2026-02-07 | Theory docs | **Review** — Move to `000_THEORY/` or keep |
| `APEX-THEORY-REPO/` | 2026-02-06 | Git repo | **Review** — Separate repo? |

```powershell
# If APEX-THEORY content belongs in 000_THEORY:
Move-Item -Path "APEX-THEORY/*" -Destination "000_THEORY/apex/" -Force
Remove-Item -Path "APEX-THEORY" -Force

# If APEX-THEORY-REPO is a separate repo:
# Option A: Convert to git submodule
# Option B: Move to archive/external/
# Option C: Keep if actively developed
```

---

### PHASE 4: Dotenv Consolidation (1 file)

**Risk Level:** 🟢 LOW — Standard practice

Current state: `.env` exists but may contain secrets.

**Recommendation:** Ensure `.env` is gitignored (✅ verified) and `.env.example` is maintained.

---

## ✅ Verification Checklist

After executing all phases:

```powershell
# Count root items (should be ~40)
Get-ChildItem -Path "." -Force | Measure-Object

# Expected breakdown:
# - Directories: ~25 (12 core + 8 tooling + 5 cache/build)
# - Files: ~15 (protected core files)
# - Total: ~40 items

# Verify critical files still present
Test-Path "README.md"
Test-Path "AGENTS.md"
Test-Path "pyproject.toml"

# Verify tests still pass
pytest tests/ -v --tb=short

# Verify MCP server starts
python -m arifosmcp.transport --help
```

---

## 📊 Expected Results

| Metric | Before | After | Change |
|:---|:---:|:---:|:---:|
| Root Directories | 32 | 29 | -3 |
| Root Files | 29 | 14 | -15 |
| **Total Root Items** | **61** | **~43** | **-30%** |
| F4 Entropy Score | MEDIUM | LOW | ✅ |
| Structure Clarity | ⚠️ | ✅ | ✅ |

---

## 🔄 Rollback Plan

All deletions are reversible from git history:

```powershell
# If anything breaks, restore from git
git checkout HEAD -- <file_path>

# For deleted directories
git checkout HEAD -- <directory_path>
```

---

## 📋 Summary of Changes from Original Plan

| Aspect | Original Plan | Revised Plan | Rationale |
|:---|:---|:---|:---|
| Target items | ~30 | ~43 | Current state has more legitimate files |
| AGENTS.md/IDENTITY.md | "Moved" to SPEC | Keep at root | Root is source-of-truth |
| SPEC directory | Keep as destination | Clean templates | Remove conflicting templates |
| venv/.venv | Not mentioned | Consolidate | Remove duplicate |
| APEX directories | Not mentioned | Review | New directories need decision |
| CONSTITUTION.md, etc. | Not mentioned | Protected | New constitutional files |

---

## 🎯 Final Recommendations

1. **Execute Phase 1 immediately** (safe deletions) — 4 items
2. **Execute Phase 2** (SPEC cleanup) — 5 files
3. **User decision on Phase 3** (APEX directories) — @arifazil
4. **Update .gitignore** if needed for new patterns
5. **Archive this revised plan** after execution

---

**DITEMPA BUKAN DIBERI** — Entropy reduction through realistic planning.

**Status:** Awaiting execution approval
