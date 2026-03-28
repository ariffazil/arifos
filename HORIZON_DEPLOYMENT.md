# Horizon Deployment Guide

> **arifosmcp now auto-detects Horizon and switches to 2.x compatible mode!**

---

## ✅ Quick Deploy

| Setting | Value |
|---------|-------|
| **Repository** | `https://github.com/ariffazil/arifosmcp` ✅ |
| **Entrypoint** | `server.py:mcp` ✅ |
| **Branch** | `main` |

---

## 🎉 What's New

**arifosmcp** now has **auto-detection**:

```python
# server.py automatically detects environment:
if FastMCP 2.x or Horizon env:
    → Load server_horizon.py (8 tools, proxy mode)
else:
    → Load runtime/server.py (11 tools, full kernel)
```

**Result:** Same repo works for BOTH VPS and Horizon! 🎊

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  PREFECT HORIZON (FastMCP 2.12.3)                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  arifosmcp/server.py                                │    │
│  │  └── Auto-detects → loads server_horizon.py         │    │
│  │       • 8 public-safe tools                         │    │
│  │       • Proxies to VPS for heavy ops                │    │
│  └──────────────┬──────────────────────────────────────┘    │
│                 │ HTTPS                                      │
│                 ▼                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  YOUR VPS                                           │    │
│  │  arifosmcp_server (Docker)                          │    │
│  │  └── Full 11-tool Sovereign Kernel                  │    │
│  │       • Vault, Memory, Code Execution               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## How It Works

### Detection Logic (server.py)

```python
def _is_horizon_environment():
    # Check 1: Horizon env vars
    if os.getenv("FASTMCP_CLOUD_URL"): return True
    
    # Check 2: FastMCP version < 3.x
    if fastmcp.__version__ < "3.0.0": return True
    
    # Check 3: Container without VPS_MODE flag
    if in_docker and not os.getenv("VPS_MODE"): return True
    
    return False
```

### Modes

| Mode | Trigger | File Loaded | Tools | FastMCP |
|------|---------|-------------|-------|---------|
| **Horizon** | Cloud env detected | `server_horizon.py` | 8 | 2.x |
| **VPS** | `VPS_MODE=1` or no cloud signals | `runtime/server.py` | 11 | 3.x |

---

## Deployment Options

### Option 1: Horizon Cloud (Recommended for public access)

```bash
# In Prefect Horizon Dashboard:
Repository:  https://github.com/ariffazil/arifosmcp
Entrypoint:  server.py:mcp
Branch:      main

# Environment Variables:
ARIFOS_VPS_URL=https://arifosmcp.arif-fazil.com
ARIFOS_GOVERNANCE_SECRET=your_secret_here
```

**Result:** Public URL at `https://arifos.fastmcp.app`

### Option 2: VPS Sovereign (Recommended for full power)

```bash
# On your VPS
cd /root/arifOS
docker compose up -d arifosmcp

# Or with explicit VPS mode
VPS_MODE=1 python server.py
```

**Result:** Your domain at `https://arifosmcp.arif-fazil.com`

---

## Tool Comparison

| Tool | Horizon (8) | VPS (11) | Notes |
|------|-------------|----------|-------|
| `init_anchor` | ✅ | ✅ | Session anchoring |
| `arifOS_kernel` | ✅ | ✅ | Primary router |
| `agi_mind` | ✅ | ✅ | Reasoning engine |
| `apex_soul` | ✅ | ✅ | Constitutional judge |
| `asi_heart` | ✅ | ✅ | Safety critique |
| `physics_reality` | ✅ | ✅ | Time/search |
| `math_estimator` | ✅ | ✅ | Cost estimation |
| `architect_registry` | ✅ | ✅ | Tool discovery |
| `vault_ledger` | ❌ | ✅ | **VPS only** - security |
| `engineering_memory` | ❌ | ✅ | **VPS only** - Redis |
| `code_engine` | ❌ | ✅ | **VPS only** - code exec |

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `No module named 'fastmcp.dependencies'` | Old arifosmcp version | `git pull` to get latest |
| `ImportError during inspect` | Detection failed | Set `HORIZON_ENVIRONMENT=1` env var |
| `Proxy failure` | VPS not accessible | Check `ARIFOS_VPS_URL` is correct |
| `Only 8 tools on VPS` | Wrong mode detected | Set `VPS_MODE=1` env var |

---

## Status

| Component | Repository | Status |
|-----------|------------|--------|
| **arifosmcp** | `ariffazil/arifosmcp` | ✅ **Horizon + VPS Compatible** |
| VPS Endpoint | `arifosmcp.arif-fazil.com` | ✅ Healthy (11 tools) |
| Horizon Endpoint | `arifos.fastmcp.app` | ⏸️ Deploy with entrypoint `server.py:mcp` |

---

**API Key:** `fmcp_Z9oLZZ0OtOZkr4dzPCzp7hIm_GA2H-D94RUC2BzYnYw`  
**Last Updated:** 2026-03-28  
**Maintainer:** arifOS Core  
**Constitutional Seal:** ΔΩΨ
