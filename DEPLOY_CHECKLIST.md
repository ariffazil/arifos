# arifOS MCP VPS Deployment Checklist

**Date:** 2026-03-20  
**Version:** 2026.03.20-CONSOLIDATION  
**VPS:** srv1325122.hstgr.cloud  
**Status:** ✅ READY FOR DEPLOYMENT — 16 Container Stack Preserved

---

## 🎯 Deployment Summary

### Critical Fix Applied
- **Issue:** Circular import recursion in `arifosmcp/runtime/__init__.py`
- **Fix:** Changed `from . import tools_internal` to `importlib.import_module()`
- **Status:** ✅ Resolved

### Server Status
```
✅ FastMCP Server: arifOS-APEX-G v2026.03.20-CONSOLIDATION
✅ 11 mega-tools registered (37 modes)
✅ Circular import fix applied
✅ 16-container VPS stack preserved
✅ Core kernel alignment verified
✅ Docker configuration ready
✅ Syntax validation passed
```

---

## 📋 Pre-Deployment Checklist

### 1. Environment Setup (VPS)
```bash
# SSH into VPS
ssh root@your-vps-ip

# Navigate to project
cd /srv/arifosmcp

# Pull latest code
git pull origin main
```

### 2. Environment File
```bash
# Create .env.docker from example
cp .env.docker.example .env.docker

# Edit with production values
nano .env.docker
```

**Required minimum configuration:**
```env
# Core
POSTGRES_PASSWORD=your_secure_32char_password
REDIS_PASSWORD=your_redis_password

# F11 Governance (MUST be persistent across restarts!)
ARIFOS_GOVERNANCE_SECRET_FILE=/opt/arifos/secrets/governance.secret
# OR (not recommended for production):
ARIFOS_GOVERNANCE_SECRET=your_64char_governance_secret

# Session
SESSION_SECRET=your_64char_session_secret

# Traefik/SSL
DOMAIN=arifosmcp.arif-fazil.com
```

### 3. Secrets Directory Setup
```bash
# Create secrets directory
mkdir -p /opt/arifos/secrets

# Generate governance secret (MUST persist across restarts!)
openssl rand -hex 64 > /opt/arifos/secrets/governance.secret
chmod 600 /opt/arifos/secrets/governance.secret

# Generate session secret
openssl rand -hex 64 > /opt/arifos/secrets/session.secret
chmod 600 /opt/arifos/secrets/session.secret
```

### 4. Database Initialization
```bash
# Ensure postgres data directory exists
mkdir -p /opt/arifos/data/postgres

# Fix permissions (if needed)
chown -R 999:999 /opt/arifos/data/postgres  # postgres user
```

---

## 🚀 Deployment Steps

### 🎯 VPS PRODUCTION DEPLOYMENT (srv1325122.hstgr.cloud)

**⚠️ CRITICAL: This deployment rebuilds ONLY arifosmcp_server while keeping all 15 other containers running**

**Current Stack:** 16 containers total (arifosmcp_server + 15 infrastructure services)

#### Step-by-Step VPS Deployment

```bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1: SSH into VPS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ssh root@srv1325122.hstgr.cloud

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 2: Navigate to project directory
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd /srv/arifosmcp

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 3: Verify current container state (should show 16 running)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | wc -l
# Expected: 17 lines (16 containers + header)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 4: Pull latest code from main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git fetch origin
git checkout main
git pull origin main

# Verify the commit
git log --oneline -1
# Expected: 6162124fa release: v2026.03.20-CONSOLIDATION

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 5: Pre-deployment backup (F1 Amanah - Reversibility)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker commit arifosmcp_server arifos/arifosmcp:backup-$(date +%Y%m%d-%H%M)
docker tag arifos/arifosmcp:backup-$(date +%Y%m%d-%H%M) arifos/arifosmcp:backup-latest

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 6: REBUILD ONLY arifosmcp container (keep other 15 running)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚠️ IMPORTANT: Only rebuild arifosmcp, do NOT touch other containers
docker compose --env-file .env.docker -f docker-compose.yml up -d --build arifosmcp

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 7: Verify rebuild started
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker ps | grep arifosmcp_server
# Should show "Up X seconds" (recently restarted)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 8: Monitor startup logs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker logs -f arifosmcp_server

# Wait for: "✅ 11 tools registered" or "Application startup complete"
# Press Ctrl+C to exit log view
```

#### Health Verification (Run after deployment)

```bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 9: Container count check (must remain 16)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker ps --format "{{.Names}}" | sort
# Expected 16 containers:
#   agent_zero_reasoner
#   arifos_grafana
#   arifos_n8n
#   arifos_postgres
#   arifos_prometheus
#   arifos_redis
#   arifos_webhook
#   arifosmcp_server        ← This one rebuilt
#   civ01_stirling_pdf
#   civ03_evolution_api
#   civ08_code_server
#   headless_browser
#   ollama_engine
#   openclaw_gateway
#   qdrant_memory
#   traefik_router

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 10: HTTP Health Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
curl -s https://arifosmcp.arif-fazil.com/health | jq .
# Expected: "version": "2026.03.20-CONSOLIDATION", "tools_loaded": 11

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 11: MCP Tools List
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
curl -s https://arifosmcp.arif-fazil.com/mcp/tools/list | jq '.tools | length'
# Expected: 11

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 12: Spot check critical tools
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
curl -s https://arifosmcp.arif-fazil.com/mcp/tools/list | jq '.tools[].name'
# Expected 11 tools:
#   "init_anchor"
#   "arifOS_kernel"
#   "apex_soul"
#   "vault_ledger"
#   "agi_mind"
#   "asi_heart"
#   "engineering_memory"
#   "physics_reality"
#   "math_estimator"
#   "code_engine"
#   "architect_registry"
```

### Method 1: GitHub Actions (Alternative)
1. Push current code to `main` branch
2. GitHub Actions workflow `.github/workflows/deploy-vps.yml` will trigger
3. Monitor deployment at: https://github.com/ariffazil/arifosmcp/actions

### Method 2: Deploy Script (Legacy)
```bash
# Use the secure deploy script
chmod +x scripts/deploy-vps-secure.sh
./scripts/deploy-vps-secure.sh
```

---

## ✅ Post-Deployment Verification

### Health Checks
```bash
# 1. Container health
docker ps | grep arifosmcp

# 2. HTTP health endpoint
curl https://arifosmcp.arif-fazil.com/health

# 3. MCP tools list
curl https://arifosmcp.arif-fazil.com/mcp/tools/list

# 4. A2A Agent Card
curl https://arifosmcp.arif-fazil.com/.well-known/agent.json
```

### Expected Response (Health)
```json
{
  "service": "arifos-aaa-mcp",
  "version": "2026.03.20-CONSOLIDATION",
  "transport": "streamable-http",
  "tools_loaded": 11,
  "ml_floors": {...},
  "capability_map": {...},
  "timestamp": "2026-03-20T..."
}
```

---

## 🔧 Troubleshooting (VPS Specific)

### Issue: Container fails to start
```bash
# Check logs (on VPS)
docker logs arifosmcp_server --tail 100

# Verify container count (must be 16)
docker ps | wc -l
# Expected: 17 (16 containers + header)

# Check for import errors
python -c "from arifosmcp.runtime.server import app; print('OK')"

# Verify file permissions
ls -la /opt/arifos/secrets/
```

### Issue: 888_HOLD auth errors
- **Cause:** Governance secret changed between restarts
- **Fix:** Ensure `ARIFOS_GOVERNANCE_SECRET_FILE` points to persistent file
- **Note:** All auth_context tokens become invalid if secret changes

### Issue: Database connection failed
```bash
# Check postgres is running (should be separate container)
docker ps | grep arifos_postgres
docker exec arifos_postgres pg_isready -U arifos_admin

# Check env vars in container
docker exec arifosmcp_server env | grep DATABASE
```

### Issue: Traefik routing broken
```bash
# Check Traefik is running
docker ps | grep traefik_router

# Check Traefik logs
docker logs traefik_router --tail 50

# Verify labels are correct
docker inspect arifosmcp_server | grep -A 20 Labels
```

### Issue: 17+ containers running (redundancy)
```bash
# If you see 17+ containers, identify duplicates
docker ps --format "{{.Names}}" | sort | uniq -d

# Stop and remove duplicates (BE CAREFUL)
docker stop <duplicate_name>
docker rm <duplicate_name>
```

### Emergency: Rollback on VPS
```bash
# Quick rollback to backup image
docker stop arifosmcp_server
docker rm arifosmcp_server
docker run -d \
  --name arifosmcp_server \
  --network arifos_trinity \
  -p 127.0.0.1:8080:8080 \
  -v /opt/arifos/data/core:/usr/src/app/data:rw \
  -v /srv/arifosmcp/arifosmcp:/usr/src/app/arifosmcp:ro \
  -v /srv/arifosmcp/core:/usr/src/app/core:ro \
  -v /srv/arifosmcp/spec:/usr/src/app/spec:ro \
  arifos/arifosmcp:backup-latest

# Or full rollback via git
cd /srv/arifosmcp
git checkout HEAD~1
docker compose --env-file .env.docker up -d --build arifosmcp
```

---

## 📝 Files Changed (Summary)

| File | Change | Status |
|------|--------|--------|
| `arifosmcp/runtime/__init__.py` | Fixed circular import | ✅ Critical |
| `arifosmcp/runtime/tools.py` | 11 mega-tool consolidation | ✅ |
| `arifosmcp/runtime/tools_internal.py` | Mode dispatch layer | ✅ |
| `pyproject.toml` | Version 2026.03.20 | ✅ |
| `npm/arifos-mcp/package.json` | NPM version 2026.3.20 | ✅ |
| `arifosmcp/packages/npm/arifos-mcp/package.json` | Client version 2026.3.20 | ✅ |
| `README.md` | 11-tool documentation | ✅ |
| `CHANGELOG.md` | v2026.03.20 release notes | ✅ |
| `spec/mcp-manifest.json` | Updated API spec | ✅ |
| `Dockerfile.optimized` | Production hardened | ✅ |
| `docker-compose.yml` | 16-container stack | ✅ |

---

## 🎉 Deployment Success Criteria

### Container Stack Verification (CRITICAL)
- [ ] **Exactly 16 containers running** (no more, no less)
- [ ] `docker ps` shows all containers from list below
- [ ] No duplicate container names
- [ ] No stopped/orphaned containers

### Core Service Verification
- [ ] `arifosmcp_server` container: Status = `Up`
- [ ] `traefik_router` container: Status = `Up` (ports 80, 443)
- [ ] `arifos_postgres` container: Status = `Up` (port 5432)
- [ ] `arifos_redis` container: Status = `Up` (port 6379)

### HTTP Endpoint Verification
- [ ] `curl https://arifosmcp.arif-fazil.com/health` returns 200
- [ ] Response contains `"version": "2026.03.20-CONSOLIDATION"`
- [ ] Response contains `"tools_loaded": 11`
- [ ] `curl https://arifosmcp.arif-fazil.com/mcp/tools/list` returns 11 tools

### Protocol Verification
- [ ] WebMCP endpoint `https://arifosmcp.arif-fazil.com/webmcp` accessible
- [ ] A2A endpoint `https://arifosmcp.arif-fazil.com/a2a` accessible
- [ ] Agent Card `https://arifosmcp.arif-fazil.com/.well-known/agent.json` returns valid JSON
- [ ] Dashboard `https://arifosmcp.arif-fazil.com/dashboard` loads

### Log Verification
- [ ] `docker logs arifosmcp_server` shows no ImportError
- [ ] Logs show "✅ 11 tools registered"
- [ ] Logs show "Application startup complete"

---

## 🐳 Docker Manager Context

If using Docker Manager GUI on srv1325122.hstgr.cloud:

1. **Navigate to:** Docker Manager → Compose → arifosmcp
2. **Click:** "Manage" on arifosmcp project
3. **Observe:** 16 containers listed
4. **Click:** Terminal icon on arifosmcp_server
5. **Run:** `git pull origin main && docker compose up -d --build arifosmcp`
6. **Wait:** Build completes (2-5 minutes)
7. **Refresh:** Docker Manager UI to verify all 16 containers still running
8. **Check:** arifosmcp_server shows recent "Up X seconds"

**Alternative (Direct Terminal):**
```bash
# Access via Docker Manager terminal or SSH
ssh root@srv1325122.hstgr.cloud
cd /srv/arifosmcp
docker compose up -d --build arifosmcp
```

---

## 📞 Support & Contacts

**VPS:** srv1325122.hstgr.cloud  
**Repository:** https://github.com/ariffazil/arifosmcp  
**Commit:** 6162124fa  
**Release:** v2026.03.20-CONSOLIDATION

### Emergency VPS Rollback
```bash
# SSH to VPS
ssh root@srv1325122.hstgr.cloud

# Quick restore from backup image
docker stop arifosmcp_server
docker rm arifosmcp_server
docker run -d --name arifosmcp_server arifos/arifosmcp:backup-latest

# Or revert git and rebuild
cd /srv/arifosmcp
git checkout HEAD~1
docker compose up -d --build arifosmcp
```

### View Logs (VPS)
```bash
# SSH to VPS first
ssh root@srv1325122.hstgr.cloud

# MCP server logs
docker logs -f arifosmcp_server

# Traefik logs (if routing issues)
docker logs -f traefik_router

# All containers status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Health Check Commands (VPS)
```bash
# Quick health check
curl -s https://arifosmcp.arif-fazil.com/health | jq .

# Tool count verification
curl -s https://arifosmcp.arif-fazil.com/mcp/tools/list | jq '.tools | length'

# Version verification
curl -s https://arifosmcp.arif-fazil.com/health | jq '.version'
```

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*  
**Deployed:** 2026-03-20  
**Status:** Production Ready — 11 Mega-Tools (37 Modes) — 16 Container Stack
