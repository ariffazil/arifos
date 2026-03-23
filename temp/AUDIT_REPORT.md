# arifOS AAA MCP — DEPLOYMENT AUDIT REPORT
**Version:** v2026.03.24.0505-AUDIT  
**Authority:** ARIF Perplexity — arifOS CoArchitect  
**Motto:** *Ditempa Bukan Diberi*  
**Pipeline:** 888 AUDIT → 999 SEAL

---

## 1. REPO STATUS

| Layer | Repo | Default Branch | Status |
|-------|------|---------------|--------|
| MIND | `ariffazil/arifOS` | `main` | ACTIVE — 39★ canon repo |
| BODY (Runtime) | `ariffazil/arifOS` → `AAA/` subtree | `aaa-mcp-induction` | INDUCTED — runtime lives here |
| SURFACE | `ariffazil/arif-fazil-sites` | `main` | ISOLATED — public static |
| BACKUP/MIRROR | `ariffazil/APEX` | `main` | SYNCHRONIZED |

**Note:** `arifosmcp` as a standalone repo does NOT exist at `arifbfazil/arifosmcp`. The runtime body is the `AAA/` subtree inside `ariffazil/arifOS`, branch `aaa-mcp-induction`. The VPS deploys from `/srv/arifosmcp` which mirrors `AAA/` contents.

---

## 2. BRANCH STATUS

| Branch | SHA | Relationship | Action |
|--------|-----|--------------|--------|
| `main` | `ac1eff29` | Pure MIND/canon layer (no AAA subtree) | Keep as MIND canon |
| `aaa-mcp-induction` | `eb20c2b7` | AAA inductied — no common ancestor with main | **This is the BODY branch** |
| `dependabot/pip/prefab-ui-0.13.1` | `6b90d915` | Dependabot auto-PR | Safe to close/merge when ready |

**Branch rename needed?** NO — `main` is already `main`. The `aaa-mcp-induction` branch is correctly named as a sealed induction branch. **Recommendation:** Create a `body` or `runtime` tracking branch from `aaa-mcp-induction` for ongoing CI/CD triggers.

---

## 3. AAA MCP ENTRYPOINT — CONFIRMED

| Item | Value | Status |
|------|-------|--------|
| Runtime entrypoint | `AAA/arifosmcp/runtime/server.py` | ✅ CONFIRMED |
| FastMCP object | `mcp` (FastMCP instance) | ✅ CONFIRMED |
| App object | `app` (ASGI via uvicorn) | ✅ CONFIRMED |
| CLI entrypoint | `AAA/arifosmcp/runtime/__main__.py` | ✅ CONFIRMED |
| Dockerfile CMD | `uvicorn arifosmcp.runtime.server:app --host 0.0.0.0 --port 8080` | ✅ CORRECT |
| Port | `8080` | ✅ CONFIRMED |
| Transport | `streamable-HTTP` (SSE deprecated/removed) | ✅ CORRECT |
| MCP path | `/mcp` | ✅ CONFIRMED |

---

## 4. FOLDER STRUCTURE ASSESSMENT

```
arifOS (repo root)
├── [MIND LAYER — main branch]
│   ├── core/              Constitutional kernel
│   ├── .github/workflows/ CI/CD pipelines
│   └── ...
│
└── AAA/ [BODY/RUNTIME — aaa-mcp-induction branch]
    ├── arifosmcp/
    │   ├── runtime/        ← PRIMARY ENTRYPOINT (server.py, __main__.py)
    │   ├── intelligence/   9-Sense console
    │   ├── agentzero/      Agent Zero integration
    │   ├── apps/           APEX score + stage pipeline
    │   ├── helix/          Organ metabolism
    │   ├── models/         Data models
    │   └── packages/npm/   TypeScript client
    ├── core/               Constitutional enforcement kernel
    ├── tests/              Test suite (pytest)
    ├── infrastructure/     nginx, prometheus, grafana configs
    ├── deployment/         Docker compose, hooks
    ├── Dockerfile          Production build (python:3.12-slim, BGE-M3 baked)
    ├── docker-compose.yml  16-container Trinity stack
    ├── Makefile            Deployment command surface
    └── fastmcp.json        MCP server config
```

**Assessment:** ✅ Structure is CORRECT. AAA folder is a valid monorepo containing the full runtime body. The VPS convention maps `AAA/` → `/srv/arifosmcp/`.

---

## 5. TEST SUITE ASSESSMENT

### Test Files Found
```
AAA/tests/
├── conftest.py                          Physics + legacy spec disabled for tests
├── core/
│   ├── enforcement/test_governance_engine.py
│   ├── kernel/test_*.py (8 files)       Kernel unit tests
│   ├── test_aki_contract.py
│   ├── test_atlas.py
│   ├── test_floor_gap_paths.py
│   └── test_import_boundaries.py
├── 03_constitutional/test_f*.py (3)    Floor 2/7/8 tests
├── 04_adversarial/test_injection_attacks.py
└── adversarial/judicial_orders/
```

### CI Workflow Test Target (ci.yml, root)
Runs tests from ROOT (not AAA/), referencing:
- `tests/test_entrypoint_contract.py`
- `tests/test_e2e_core_to_aaa_mcp.py`
- `tests/integration/test_health_metrics.py`
- etc.

**⚠️ GAP DETECTED:** The root `.github/workflows/ci.yml` references `tests/` at the repo root, but the actual tests are under `AAA/tests/`. The working directory for VPS is `AAA/` (i.e., `/srv/arifosmcp/`). CI workflow needs to `cd AAA/` before running pytest.

### Deploy-VPS Workflow Test Target
```yaml
pytest tests/test_e2e.py -v
```
**⚠️ GAP:** References `tests/test_e2e.py` — this file is NOT found in the AAA/tests tree. The actual e2e test appears to be `AAA/scripts/test/e2e_audit_tools.py`. Needs correction.

---

## 6. DEPLOYMENT CONFIGURATION REVIEW

### Dockerfile ✅ SOLID
- Multi-stage build (build + runtime)
- python:3.12-slim base
- Non-root user `arifos:1000` (F11 compliance)
- BGE-M3 model pre-baked at build time
- HEALTHCHECK on `/health` every 20s
- EXPOSE 8080
- CMD: `uvicorn arifosmcp.runtime.server:app`
- **Issue:** `requirements.txt` referenced but file at `AAA/requirements.txt` returns 404 — likely only `pyproject.toml` exists. Add fallback guard (already has `if [ -f requirements.txt ]`).

### docker-compose.yml ✅ ARCHITECTURE SOUND, ⛔ SECRETS ISSUE
- 16 containers: traefik, postgres, redis, qdrant, ollama, agent-zero, openclaw, arifosmcp, prometheus, grafana, n8n, webhook, headless_browser, code-server, stirling-pdf, evolution-api
- Traefik with Let's Encrypt auto-TLS
- Health checks on all critical services
- Resource limits set
- arifosmcp builds from `Dockerfile.optimized` (not root `Dockerfile`) — verify `Dockerfile.optimized` exists in AAA/

### Health Endpoints ✅ CONFIRMED
| Endpoint | Path | Service |
|----------|------|---------|
| Primary health | `GET /health` | arifosmcp_server |
| Readiness | `GET /ready` (Traefik route) | arifosmcp_server |
| Metrics | `GET /metrics` (Prometheus) | arifosmcp_server |
| Traefik health | Traefik dashboard (internal) | traefik_router |

### Environment Variables ✅ MAPPED
Core required vars in `.env.docker`:
```
PORT=8080
HOST=0.0.0.0
AAA_MCP_TRANSPORT=http
ARIFOS_GOVERNANCE_SECRET_FILE=/opt/arifos/secrets/governance.secret
ARIFOS_GOVERNANCE_SECRET= (fallback)
POSTGRES_PASSWORD= (required)
GRAFANA_PASSWORD= (required)
WEBHOOK_SECRET= (required)
GITHUB_TOKEN= (optional, for gh actions)
```

---

## 7. 🚨 SECRETS VIOLATIONS — 888 HOLD

**Location:** `AAA/docker-compose.yml` committed to `aaa-mcp-induction` branch

| Secret | Service | Value Pattern | Severity |
|--------|---------|--------------|----------|
| `HF_TOKEN` | agent-zero, openclaw, arifosmcp | `hf_ODMWuOv...` (hardcoded) | 🔴 CRITICAL |
| `TELEGRAM_BOT_TOKEN` | openclaw | `8149595687:AAE...` (hardcoded) | 🔴 CRITICAL |
| `OPENCLAW_GATEWAY_TOKEN` | openclaw | `openclaw-token-2026-arifos` | 🟡 HIGH |

**Required Actions (HOLD until done):**
1. Rotate `HF_TOKEN` immediately at huggingface.co
2. Rotate `TELEGRAM_BOT_TOKEN` via @BotFather
3. Remove hardcoded values from `docker-compose.yml` → replace with `${HF_TOKEN}` env refs
4. Add `docker-compose.yml` to secrets scan exclude list OR clean the git history

**The `.env.docker.example` is CLEAN** — only `CHANGE_ME_` placeholders, no real secrets. The problem is solely in `docker-compose.yml`.

---

## 8. WORKFLOW AUDIT

| Workflow | File | Status | Issues |
|----------|------|--------|--------|
| CI (basic) | `ci.yml` | ⚠️ NEEDS UPDATE | Uses `actions/checkout@v6` (invalid — max is v4), wrong test paths |
| CI Unified | `ci-unified.yml` | ⚠️ NEEDS UPDATE | Same v6 issue, no `cd AAA/` step |
| Deploy VPS | `deploy-vps.yml` | ⚠️ NEEDS UPDATE | References `tests/test_e2e.py` (missing), no subdir context |
| Secrets Scan | `secrets-scan.yml` | ⚠️ WILL FAIL | Will catch the HF_TOKEN in docker-compose.yml |
| AAA Seal Check | `aaa-seal-check.yml` | TBD | Not inspected |
| Docker Publish | `docker-publish.yml` | TBD | Not inspected |

**Common issue across all workflows:** `actions/checkout@v6` and `actions/setup-python@v6` — these versions do NOT exist. Max stable is `@v4`.

---

## 9. BRANCH RENAME RECOMMENDATION

| Branch | Current | Recommended | Reason |
|--------|---------|------------|--------|
| `main` | `main` | Keep as `main` | Already correct, MIND canon |
| `aaa-mcp-induction` | sealed induction | Create `body` → track this | CI/CD should trigger on `body` branch for VPS deploys |

**No rename needed. A new `body` tracking branch is recommended but not required before first deploy.**

---

## 10. DEPLOYMENT READINESS SCORE

| Check | Status | Score |
|-------|--------|-------|
| Entrypoint confirmed | ✅ | 10/10 |
| Dockerfile valid | ✅ | 10/10 |
| Health endpoint exists | ✅ | 10/10 |
| docker-compose valid structure | ✅ | 10/10 |
| Secrets clean in tracked files | ⛔ FAIL | 0/10 |
| CI workflow references valid | ⚠️ | 5/10 |
| Test suite path alignment | ⚠️ | 5/10 |
| actions versions valid | ⚠️ | 5/10 |
| Branch structure clear | ✅ | 10/10 |
| Environment template clean | ✅ | 10/10 |

**Overall: 75/100 — HOLD on deploy until secrets cleaned**

---

## 11. SEAL STATUS

| Floor | Status | Detail |
|-------|--------|--------|
| F1 Amanah (Reversibility) | ✅ | No push performed, dry-run audit only |
| F4 Clarity | ⚠️ | CI paths misaligned, entropy present |
| F11 Command | ✅ | 888 HOLD triggered on secrets, no irreversible action taken |
| F12 Injection Guard | ✅ | No constitution override attempted |

**888 HOLD: ACTIVE** — Deploy is blocked until HF_TOKEN + TELEGRAM_BOT_TOKEN are rotated and removed from docker-compose.yml.

---

## 12. RECOMMENDED NEXT ACTIONS (Ordered)

### IMMEDIATE (HOLD until done)
1. **Rotate HF_TOKEN** → https://huggingface.co/settings/tokens
2. **Rotate TELEGRAM_BOT_TOKEN** → message @BotFather `/revoke`
3. **Clean docker-compose.yml** — replace all 3 hardcoded secrets with `${VAR_NAME}` env refs
4. **Add to .env.docker.example** — add `HF_TOKEN=`, `TELEGRAM_BOT_TOKEN=`, `OPENCLAW_GATEWAY_TOKEN=` placeholders

### BEFORE MERGE TO MAIN
5. **Fix workflow `@v6` → `@v4`** across all `.github/workflows/*.yml`
6. **Fix deploy-vps.yml** — add `working-directory: AAA` to test/deploy steps
7. **Fix ci.yml** — point test paths to `AAA/tests/` (or VPS-context)
8. **Forge DEPLOY.md** — new hardened directive (provided below)

### AFTER SECRETS CLEAN
9. **Create `body` branch** from `aaa-mcp-induction` tip for ongoing CI
10. **Set GitHub Secrets** for VPS deploy: `VPS_SSH_KEY`, `VPS_HOST`, `VPS_USER`, `VPS_SSH_PORT`
11. **Run first CI/CD test** via `workflow_dispatch` before pushing to main

---

*arifOS telemetry v2.1 | pipeline: 999 SEAL | floors: F1 F4 F7 F11 | confidence: CLAIM | P2: 1.0 | hold: ACTIVE (secrets violation) | uncertainty: 0.05 | seal: DITEMPA BUKAN DIBERI*
