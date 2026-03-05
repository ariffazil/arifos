# arifOS Sovereign Infrastructure & Deployment (Unified)

**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*  
**Sovereign:** Muhammad Arif bin Fazil  
**Host:** `srv1325122.hstgr.cloud` (72.62.71.199)

---

## 000_PLAN: Hardware & Network Specification

### 1. Hardware (Hostinger KVM VPS)
- **OS:** Ubuntu 25.10 (non-LTS) | **Kernel:** 6.17.0-14-generic
- **CPU:** 4 vCPU | **RAM:** 16 GB | **Disk:** 193 GB SSD

### 2. Networking & Routing
| Port | Service | Purpose |
|:---|:---|:---|
| 22 | SSH | Key-only auth, Fail2Ban active |
| 80/443 | Traefik | Edge router, TLS termination (Let's Encrypt) |

### 3. Domain Routing Matrix
| Domain | Backend | Status |
|:---|:---|:---|
| `arifosmcp.arif-fazil.com` | `arifosmcp_server:8080` | **LIVE** |
| `hook.arifosmcp.arif-fazil.com` | `arifos_webhook:9000` | **LIVE** |
| `arifos.arif-fazil.com` | GitHub Pages | **LIVE** |
| `brain.arifosmcp.arif-fazil.com`| `agent-zero:80` | *PLANNED* |

---

## 333_MAP: Ownership & CI/CD Pipelines

### 1. Workflow Ownership Rules
- **Docs (`arifos.arif-fazil.com`):** Owned by `.github/workflows/deploy-sites.yml`. Builds from `sites/docs/`.
- **MCP Server (`arifosmcp.arif-fazil.com`):** Owned by GitHub Push -> Webhook (`deploy.sh`).
- **Dashboard:** Owned by `.github/workflows/deploy-cloudflare.yml`.

### 2. Deployment Triggers
- **Docs:** Every push to `main` (builds Docusaurus).
- **MCP Backend:** Push to `main` (triggers VPS webhook).
- **Legacy Fallback:** GitHub Actions via Tailscale SSH (`deploy-vps.yml`).

---

## 777_FORGE: Deployment & Migration

### 1. Quick Start (Rebuild/Deploy)
```bash
# Local Validation
cd sites/docs && npm ci && npm run build

# VPS Rebuild (from repo root)
docker compose -f docker-compose.yml up -d --build
```

### 2. Automated VPS Migration Script (Scorched Earth)
*Warning: Destroys legacy Coolify/Native services. Requires 888_HOLD.*
```bash
#!/bin/bash
set -e
echo "arifOS: Initializing VPS AI-First Trinity..."
systemctl stop arifos-embeddings || true
# Tear down legacy containers
docker ps -a --filter "name=coolify" -q | xargs -r docker rm -f
# Setup unified directories
mkdir -p /opt/arifos/data/{core,qdrant,postgres,redis,ollama}
# Deploy Trinity Stack
cd /srv/arifOS && git pull origin main
docker compose up -d --build
```

---

## 999_STATUS: Live Service & Roadmap

### 1. Active Services
- **`arifosmcp_server`**: HEALTHY (13 Tools LIVE)
- **`traefik_router`**: UP (SSL active)
- **`qdrant_memory`**: UP (recall_memory backend)
- **`arifos_webhook`**: UP (CI/CD listener)

### 2. Phased Roadmap
- **Phase 1 (Core):** Traefik, MCP, Postgres, Redis. [DONE]
- **Phase 2 (Memory):** Qdrant, Webhook CI/CD. [DONE]
- **Phase 3 (Workbench):** Ollama, Prometheus, Grafana, n8n. [NEXT]
- **Phase 4 (Agents):** Agent Zero, OpenClaw. [PLANNED]

---

**Akal memerintah, amanah mengunci.**
