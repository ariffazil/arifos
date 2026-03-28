# Horizon Deployment Guide

> **Use `arifOS/horizon/` subdirectory for Prefect Horizon deployments**

---

## 🚨 CRITICAL: Version Compatibility

| Component | FastMCP Version | Result on Horizon |
|-----------|-----------------|-------------------|
| `arifosmcp/` submodule | 3.x (`fastmcp.dependencies`) | ❌ **FAILS** |
| `arifOS/horizon/` | 2.x (compatible) | ✅ **WORKS** |
| Horizon Platform | 2.12.3 (locked) | — |

### The Error You'll Get (If Wrong)

If you try to deploy `arifosmcp/` directly to Horizon:
```
No module named 'fastmcp.dependencies'
```

This happens because `arifosmcp/runtime/megaTools/tool_05_agi_mind.py` imports:
```python
from fastmcp.dependencies import CurrentContext  # FastMCP 3.x only
```

**Horizon cannot be upgraded** — you MUST use the 2.x compatible adapter.

---

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

---

## Deployment Comparison

| Aspect | `arifosmcp/` (VPS) | `horizon/` (Cloud) |
|--------|-------------------|-------------------|
| **FastMCP Version** | 3.x | 2.x |
| **Import Pattern** | `from fastmcp.dependencies import CurrentContext` | `from fastmcp import FastMCP` |
| **Package Install** | Required (`pip install -e .`) | Not needed (self-contained) |
| **Tool Count** | 11 (full sovereign) | 8 (public-safe) |
| **VAULT999** | ✅ Full access | ❌ Disabled (security) |
| **Memory/Code Exec** | ✅ Available | ❌ Disabled (security) |
| **Deployment** | Docker on VPS | Prefect Horizon |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      TRINITY ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────┐                                 │
│  │  Prefect Horizon        │  ☁️ Cloud Tier                  │
│  │  horizon/server.py      │     FastMCP 2.12.3              │
│  │  • 8 public-safe tools  │     8 tools (safe subset)       │
│  │  • No vault/memory      │     Proxies to VPS              │
│  │  • FastMCP 2.x          │                                 │
│  └──────────┬──────────────┘                                 │
│             │ HTTPS                                          │
│             ▼                                                │
│  ┌─────────────────────────┐                                 │
│  │  Your VPS (Sovereign)   │  🔥 Private Kernel              │
│  │  arifosmcp_server       │     FastMCP 3.x                 │
│  │  Port 8080 (internal)   │     11 tools (full band)        │
│  │  • Full vault access    │     Constitutional ΔΩΨ         │
│  │  • Memory persistence   │                                 │
│  │  • Code execution       │                                 │
│  └─────────────────────────┘                                 │
│                                                              │
│  Entry Point for Horizon:                                    │
│  Repository: ariffazil/arifOS                                │
│  Entrypoint: horizon/server.py:mcp                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Verify Horizon Code

```bash
cd /root/arifOS/horizon
cat server.py  # Verify it's the simple version (no fastmcp.dependencies imports)
```

### 2. Push to GitHub

```bash
git add horizon/server.py horizon/README.md horizon/DEPLOYMENT_PLAN.md
git commit -m "v2026.03.28-HORIZON-READY"
git push origin main
```

### 3. Deploy in Prefect Horizon Dashboard

1. Go to: https://horizon.prefect.io
2. Create new deployment
3. **Connect GitHub repo**: `ariffazil/arifOS`
4. **Set entrypoint**: `horizon/server.py:mcp`
5. **Set environment variable**: 
   - `ARIFOS_VPS_URL=https://arifosmcp.arif-fazil.com`
6. **Deploy**

### 4. Test

```bash
# Horizon endpoint (once deployed)
curl https://arifos.fastmcp.app/health

# Your VPS endpoint (should already work)
curl https://arifosmcp.arif-fazil.com/health
```

---

## Environment Variables

Set in Horizon dashboard:

| Variable | Value | Purpose |
|----------|-------|---------|
| `ARIFOS_VPS_URL` | `https://arifosmcp.arif-fazil.com` | Proxy target for heavy operations |
| `ARIFOS_VPS_API_KEY` | (optional) | Authentication with VPS |

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `No module named 'fastmcp.dependencies'` | Using `arifosmcp/` instead of `horizon/` | Switch to `arifOS/horizon/` entrypoint |
| `No module named 'arifosmcp'` | Package not installed | Use `horizon/` (self-contained) |
| `ImportError: cannot import name 'CurrentContext'` | FastMCP version mismatch | `horizon/` uses 2.x compatible imports |
| `Connection refused` | VPS not accessible | Check VPS URL, ensure traefik running |
| `Tool not found` | Wrong entrypoint | Use `horizon/server.py:mcp` not `server.py` |

---

## Status

| Component | Repository | Status |
|-----------|------------|--------|
| VPS (Sovereign) | `arifosmcp/` | ✅ Healthy at https://arifosmcp.arif-fazil.com |
| Horizon (Cloud) | `arifOS/horizon/` | ⏸️ Ready to deploy |
| Submodule | `arifosmcp/` | ⚠️ VPS only, NOT for Horizon |

---

**Last Updated:** 2026-03-28  
**Maintainer:** arifOS Core  
**Constitutional Seal:** ΔΩΨ
