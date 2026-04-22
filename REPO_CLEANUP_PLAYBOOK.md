# REPO CLEANUP PLAYBOOK — 2026-04-22
# DITEMPA BUKAN DIBERI — Forged, Not Given

## Purpose

Step-by-step playbook for OpenClaw to clean both repos, formalize B++ architecture,
and establish success metrics. Each phase has qual + quant checkpoints.

---

## PHASE 0 — Ground Truth Map (read-only)

**Goal:** Confirm what is canonical vs runtime-only before touching anything.

### Steps

```bash
# arifOS repo
git -C /root/arifos remote -v
git -C /root/arifos submodule status
git -C /root/arifos status --short | grep "^[ M]"

# GEOX repo (sibling)
git -C /srv/siblings/GEOX-repo/ remote -v
git -C /srv/siblings/GEOX-repo/ log --oneline -1 origin/main

# Container reality
docker inspect arifos-mcp-prod --format '{{json .Mounts}}'
```

### Current State Confirmed

| Item | Status |
|------|--------|
| `/root/arifos/geox/` | EMPTY — submodule was never initialized |
| `.gitmodules` geox entry | REMOVED (commit `70d0a3617`) |
| `/srv/siblings/GEOX-repo/` | 47MB, clean, at `fe03bcb` |
| Container mount | `/root/arifos → /usr/src/app` |
| GEOX consumed via | Sibling path in container, NOT via git submodule |

### Qual Success
- Operator can state which dirs are canonical source vs runtime convention
- No ambiguity about "where GEOX actually lives"

### Quant Success
- arifOS git status: ≤ 8 untracked files (current: 8 known local dirs)
- GEOX sibling: 0 uncommitted changes
- 0 ghost submodule entries in `git submodule status`

---

## PHASE 1 — Repo Sanitization

**Goal:** Remove untracked/runtime-only cruft from arifOS tracked tree.

### 1.1 — Audit all untracked files

Categorize each of the 8 untracked items:

```
333_APPS/         → local app experiments (NOT canonical)
AGENTS.md.sig     → signature artifact (NOT canonical)
arifos/tools/floors.py → real code (KEEP, commit)
deploy/           → B++ deploy artifact (KEEP, stack.manifest.json committed)
identity/         → OpenClaw identity config (NOT canonical, local only)
skills/           → OpenClaw skills (NOT canonical, local only)
soul/             → OpenClaw soul config (NOT canonical, local only)
user/             → OpenClaw user config (NOT canonical, local only)
well/             → well-organ tool (NOT a git repo, local only)
commands/         → markdown command docs (NOT canonical)
```

### 1.2 — Decision: .gitignore

```bash
# Add to /root/arifos/.gitignore
# Local runtime & OpenClaw config — never commit
identity/
soul/
user/
skills/
commands/
333_APPS/
well/
*.sig
```

### 1.3 — Commit sanitization

```bash
git -C /root/arifos add .gitignore
git -C /root/arifos commit -m "IGNORE: exclude local-only dirs from git tracking

- identity/ soul/ user/ skills/ commands/ → .gitignore
- 333_APPS/ → .gitignore
- well/ → .gitignore
- *.sig → .gitignore
- arifos/tools/floors.py: KEEP — real code, NOT local config
- deploy/: KEEP — stack.manifest.json is canonical"
```

### Quant Success
- `git status` shows ≤ 3 untracked items
- 0 untracked items that should have been in .gitignore

---

## PHASE 2 — Deploy Path Formalization (B++)

**Goal:** Make GEOX consumption explicit, not sibling-magic.

### Two options

**Option D (recommended): Image-based**
- GEOX repo builds to `ghcr.io/ariffazil/geox:<tag>`
- docker-compose pulls pinned image
- stack.manifest.json records image tag + SHA

**Option E (sibling-acceptable):**
- /srv/siblings/GEOX-repo/ cloned once, fixed ref checked out
- refs.lock records exact SHA
- docker-compose COPY from sibling path

### Pre-deploy check script

Create `scripts/pre-deploy-check.sh`:

```bash
#!/bin/bash
MANIFEST="deploy/stack.manifest.json"

ARIFOS_REF=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['arifos']['ref'])")
GEOX_REF=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['geox']['ref'])")

ARIFOS_CURRENT=$(git -C /root/arifos rev-parse HEAD)
GEOX_CURRENT=$(git -C /srv/siblings/GEOX-repo/ rev-parse HEAD)

[ "$ARIFOS_CURRENT" = "$ARIFOS_REF" ] || { echo "MISMATCH arifOS"; exit 1; }
[ "$GEOX_CURRENT" = "$GEOX_REF" ] || { echo "MISMATCH GEOX"; exit 1; }
echo "PASS"
```

### Quant Success
- Mismatch deploy attempts: 0 in routine ops
- Time to answer "what's live?": < 30 seconds
- Pre-deploy check script exists + executable

---

## PHASE 3 — arifOS Tools Code Audit

### Known real code

| File | Action |
|------|--------|
| `arifos/tools/floors.py` | COMMIT if not already tracked |

### floors.py review checklist
- [ ] No secret values embedded
- [ ] No hardcoded production credentials
- [ ] Imports are from canonical arifOS packages

### Quant Success
- `floors.py` has meaningful implementation (not stub)
- Committed to git with clear message

---

## PHASE 4 — General vs Specialization Contrast

| Dimension | arifOS (General/Kernel) | GEOX (Special/Domain) |
|-----------|--------------------------|----------------------|
| What it does | Constitutional governance, MCP orchestration | Petrophysics, seismic, spatial logic |
| Change frequency | Lower — core floors stable | Higher — domain logic evolves |
| Release coupling | Independent via manifest pinning | Independent via manifest pinning |

### What stays GENERAL (arifOS)
- Constitutional floors F1-F13
- MCP server orchestration
- Guard middleware logic
- Deploy contracts and manifests
- AMANAH governance tests
- Vault and audit trail

### What stays SPECIAL (GEOX)
- Physics engine (geox_physics9)
- Well correlation algorithms
- Seismic interpretation
- Petrophysics calculations
- AC_Risk formula
- Material properties database

### What is OPERATOR CONFIG (neither repo)
- OpenClaw identity, soul, user configs
- Skills catalog
- Local command docs
- Well-organ tooling

---

## PHASE 5 — GEOX Image Tagging (Option D)

```bash
# In GEOX repo
git tag v2026.04.22
docker build -t ghcr.io/ariffazil/geox:v2026.04.22 .
docker push ghcr.io/ariffazil/geox:v2026.04.22
```

---

## SUCCESS METRICS SUMMARY

### Quant Metrics

| Metric | Target |
|--------|--------|
| `git status` untracked (arifOS) | ≤ 3 |
| `git submodule status` | clean |
| Deploy mismatch events | 0 |
| Answer "what's live?" time | < 30s |
| Pre-deploy check script | exists + executable |
| stack.manifest.json | present in main |

### Qual Metrics

| Metric | Target |
|--------|--------|
| Operator can state what's live in < 30s | YES |
| No ghost submodule declarations | YES |
| Deploy truth is manifest-not-memory | YES |
| arifOS/GEOX separation respected | YES |

---

## EXECUTION ORDER

```
Step 1 → Phase 1: Write .gitignore, commit
Step 2 → Phase 2: Write pre-deploy-check.sh
Step 3 → Phase 3: Review + commit floors.py
Step 4 → Phase 4: Verify G/S separation
Step 5 → Phase 5: Image-tag GEOX (Option D) or lock sibling ref (Option E)
Step 6 → Commit all as cleanup batch
Step 7 → 888 HOLD: await A3 approval for main merge + guard wiring
```

---

## 888 HOLD

**Non-governance-affecting cleanup** — safe to execute now:
- Phase 1 (.gitignore)
- Phase 2 (pre-deploy check)
- Phase 3 (floors.py commit)
- Phase 4 (G/S check)

**888 HOLD remains on:**
- Wiring `constitutional_guard` into MCP pipeline
- Merging `autoresearch/2026-04-22` to main
- Rebuilding `arifos-mcp-prod` container

**DITEMPA BUKAN DIBERI — cleanup first, governance fix after.**
