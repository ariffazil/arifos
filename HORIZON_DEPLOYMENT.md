# Horizon Deployment Guide

> **Use `horizon/` subdirectory for Prefect Horizon deployments**

## ⚠️  IMPORTANT

Do NOT deploy the `arifosmcp/` submodule directly to Horizon. It will fail with:
```
No module named 'arifosmcp'
```

## ✅ Correct Approach

Deploy the simplified adapter from this repo:

```bash
cd /root/arifOS/horizon
# Push to GitHub
git add .
git commit -m "Horizon deployment"
git push origin main

# In Prefect Horizon Dashboard:
# - Repository: ariffazil/arifOS
# - Entrypoint: horizon/server.py:mcp
# - Branch: main
```

## Why arifosmcp/ Fails on Horizon

| Issue | Reason |
|-------|--------|
| Import errors | Uses `from arifosmcp.runtime...` absolute imports |
| Package not installed | Horizon copies files but doesn't `pip install` |
| Complex dependencies | Requires FastMCP 3.x, specific runtime |

## Why horizon/ Works

| Feature | Benefit |
|---------|---------|
| Self-contained | Single `server.py`, no package imports |
| FastMCP 2.x | Compatible with Horizon's runtime |
| Minimal deps | Only `fastmcp` in requirements |
| Proxy mode | Calls your VPS for heavy lifting |

## Architecture

```
User Request
     │
     ▼
┌─────────────────────────┐
│  Prefect Horizon        │  ☁️ Cloud (8 tools)
│  horizon/server.py      │     FastMCP 2.x
└──────────┬──────────────┘
           │ HTTPS
           ▼
┌─────────────────────────┐
│  Your VPS               │  🔥 Private (11 tools)
│  arifosmcp_server       │     Full Sovereign
│  Port 8080 (internal)   │
└─────────────────────────┘
```

## Quick Start

### 1. Prepare Horizon Code
```bash
cd /root/arifOS/horizon
cat server.py  # Verify it's the simple version
```

### 2. Push to GitHub
```bash
git add server.py README.md DEPLOYMENT_PLAN.md
git commit -m "v2026.03.28-HORIZON-READY"
git push origin main
```

### 3. Deploy in Prefect
```
Dashboard: https://horizon.prefect.io

1. Create new deployment
2. Connect GitHub repo: ariffazil/arifOS
3. Set entrypoint: horizon/server.py:mcp
4. Set environment: ARIFOS_VPS_URL=https://arifosmcp.arif-fazil.com
5. Deploy
```

### 4. Test
```bash
curl https://arifos.fastmcp.app/health  # Horizon endpoint
```

## Environment Variables

Set in Horizon dashboard:

| Variable | Value | Purpose |
|----------|-------|---------|
| `ARIFOS_VPS_URL` | `https://arifosmcp.arif-fazil.com` | Proxy target |
| `ARIFOS_VPS_API_KEY` | (optional) | Authentication |

## Troubleshooting

| Error | Solution |
|-------|----------|
| "No module named arifosmcp" | You're using arifosmcp/ instead of horizon/ |
| "FastMCP version mismatch" | horizon/ uses 2.x, arifosmcp/ uses 3.x |
| "Connection refused" | Check VPS URL, ensure traefik is running |

## Status

| Component | Status |
|-----------|--------|
| VPS (arifosmcp) | ✅ Healthy at https://arifosmcp.arif-fazil.com |
| Horizon (horizon/) | ⏸️ Ready to deploy |
| Submodule | ⚠️ VPS only, not for Horizon |

---
**Last Updated:** 2026-03-28  
**Maintainer:** arifOS Core
