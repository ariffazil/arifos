# arifOS Deployment Guide

**Version**: 2026-03-06 · VPS-HARDENED  
**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*  
**Sovereign:** Muhammad Arif bin Fazil

---

## 🚀 $15 VPS Production Deployment (Recommended)

### Prerequisites
- Ubuntu 22.04+ VPS ($5–15/month: DigitalOcean, Hetzner, Vultr, Hostinger)
- Docker + Docker Compose installed
- Domain pointed to VPS IP (optional, for TLS via Traefik)

### One-Command Deploy
```bash
# Clone repo
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# Deploy (full stack — Traefik, Qdrant, Prometheus, etc.)
docker compose up -d

# Verify
curl http://localhost:8080/health
# Expected: {"status": "healthy", ...}
```

### MCP Endpoints
- **HTTP**: `http://your-vps-ip:8080/mcp`  (or `https://arifosmcp.arif-fazil.com/mcp` with Traefik)
- **Health**: `http://your-vps-ip:8080/health`

### Troubleshooting
```bash
# View logs
docker compose logs -f arifosmcp

# Restart MCP server
docker compose restart arifosmcp

# Rebuild after code changes
cd /srv/arifOS && git pull origin main
docker compose up -d --build
```

---

## 🔧 Local Development

### stdio (Claude Desktop, Cursor)
```bash
pip install -e .
python -m arifos_aaa_mcp stdio
```

### http (Testing VPS mode locally)
```bash
python -m arifos_aaa_mcp http
# OR
python server.py --mode http
curl http://localhost:8080/health
```

---

## 📂 MCP Client Configuration

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS"
    }
  }
}
```

**Cursor** (`cursor_mcp_config.json`):
```json
{
  "servers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS"
    }
  }
}
```

---

## 🔒 Environment Variables (Production)

Create `.env` file (never commit to git):
```env
ARIFOS_GOVERNANCE_SECRET=your_secret_here_32_chars_min
VAULT_PATH=/usr/src/app/VAULT999/BBB_LEDGER/vault.jsonl
LOG_LEVEL=INFO
PORT=8080
HOST=0.0.0.0
```

---

## 🏗️ Infrastructure Overview (Live VPS)

**Host:** `srv1325122.hstgr.cloud` (72.62.71.199)

### Network Routing
| Port | Service | Purpose |
|:---|:---|:---|
| 22 | SSH | Key-only auth, Fail2Ban active |
| 80/443 | Traefik | Edge router, TLS termination (Let's Encrypt) |

### Domain Routing Matrix
| Domain | Backend | Status |
|:---|:---|:---|
| `arifosmcp.arif-fazil.com` | `arifosmcp_server:8080` | **LIVE** |
| `hook.arifosmcp.arif-fazil.com` | `arifos_webhook:9000` | **LIVE** |
| `arifos.arif-fazil.com` | GitHub Pages | **LIVE** |

### Workflow Ownership
- **Docs (`arifos.arif-fazil.com`):** `.github/workflows/deploy-sites.yml`
- **MCP Server (`arifosmcp.arif-fazil.com`):** GitHub Push → Webhook (`deploy.sh`)
- **Dashboard:** `.github/workflows/deploy-cloudflare.yml`

---

## 📊 Monitoring (Optional)

Monitor `http://your-vps:8080/health` via Uptime Kuma or similar.
Prometheus + Grafana are included in `docker-compose.yml` for the full stack.

---

**Akal memerintah, amanah mengunci.**
