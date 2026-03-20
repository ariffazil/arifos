# arifOS MCP VPS Deployment Checklist

**Date:** 2026-03-20  
**Version:** 2026.03.19-ANTI-CHAOS  
**Status:** ✅ READY FOR DEPLOYMENT

---

## 🎯 Deployment Summary

### Critical Fix Applied
- **Issue:** Circular import recursion in `arifosmcp/runtime/__init__.py`
- **Fix:** Changed `from . import tools_internal` to `importlib.import_module()`
- **Status:** ✅ Resolved

### Server Status
```
✅ FastMCP Server: arifOS-APEX-G v2026.03.14-VALIDATED
✅ 11 canonical tools registered
✅ 37 modes available
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

### Method 1: GitHub Actions (Recommended)
1. Push current code to `main` branch
2. GitHub Actions workflow `.github/workflows/deploy-vps.yml` will trigger
3. Monitor deployment at: https://github.com/ariffazil/arifosmcp/actions

### Method 2: Manual Deployment
```bash
# 1. SSH to VPS
ssh root@your-vps-ip

# 2. Navigate to project
cd /srv/arifosmcp

# 3. Pull latest code
git pull origin main

# 4. Rebuild and restart
docker compose --env-file .env.docker up -d --build arifosmcp

# 5. Verify deployment
docker ps | grep arifosmcp
docker logs -f arifosmcp_server
```

### Method 3: Deploy Script
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
  "version": "2026.03.19-ANTICHAOS",
  "transport": "streamable-http",
  "tools_loaded": 11,
  "ml_floors": {...},
  "capability_map": {...},
  "timestamp": "2026-03-20T..."
}
```

---

## 🔧 Troubleshooting

### Issue: Container fails to start
```bash
# Check logs
docker logs arifosmcp_server --tail 100

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
# Check postgres is running
docker ps | grep postgres
docker exec arifos_postgres pg_isready -U arifos_admin

# Check env vars in container
docker exec arifosmcp_server env | grep DATABASE
```

---

## 📝 Files Changed (Summary)

| File | Change | Status |
|------|--------|--------|
| `arifosmcp/runtime/__init__.py` | Fixed circular import | ✅ Critical |
| `arifosmcp/runtime/tools.py` | 11 mega-tool consolidation | ✅ |
| `arifosmcp/runtime/tools_internal.py` | Implementation layer | ✅ |
| `spec/mcp-manifest.json` | Updated API spec | ✅ |
| `Dockerfile` | Production hardened | ✅ |
| `docker-compose.yml` | Full stack config | ✅ |

---

## 🎉 Deployment Success Criteria

- [ ] `docker ps` shows `arifosmcp_server` healthy
- [ ] `curl /health` returns 200 with tools_loaded: 11
- [ ] `curl /mcp/tools/list` returns 11 tools
- [ ] No errors in `docker logs arifosmcp_server`
- [ ] WebMCP endpoint `/webmcp` accessible
- [ ] A2A endpoint `/a2a` accessible
- [ ] Dashboard loads at `/dashboard`

---

## 📞 Support

**Emergency rollback:**
```bash
docker compose down
git checkout HEAD~1
docker compose up -d --build
```

**View logs:**
```bash
docker logs -f arifosmcp_server
journalctl -u arifos-mcp -f  # if using systemd
```

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
