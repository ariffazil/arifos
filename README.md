<div align="center">

# arifOS — Constitutional Intelligence Kernel  
**The System That Knows It Doesn't Know**  
Ditempa Bukan Diberi — Forged, Not Given

[![Version](https://img.shields.io/badge/version-2026.2.23-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/ariffazil/arifOS/releases)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange?style=for-the-badge)](https://github.com/ariffazil/arifOS/blob/main/LICENSE)
[![MCP Ready](https://img.shields.io/badge/MCP-Ready-8B5CF6?style=for-the-badge&logo=shield&logoColor=white)](https://registry.modelcontextprotocol.io)
[![Deploy to Coolify](https://img.shields.io/badge/Deploy%20to-Coolify-06b6d4?style=for-the-badge&logo=docker)](https://coolify.io)

**arifOS** is a governance kernel that wraps any LLM (Claude, GPT, Gemini, custom) inside a **constitutional pipeline** with 13 mathematical floors + human veto.  
Every output must pass truth, sovereignty, empathy, ontology locks — or get **SEAL**, **SABAR/HOLD**, or **VOID**.

</div>

## Quick Start (Deploy in 5–10 Minutes)

### 1. Local / Development (Stdio — fastest)
```bash
pip install arifos
python -m aaa_mcp  # Starts in stdio mode — connect Claude Desktop / Cursor / OpenClaw
```

### 2. Production (Recommended: Coolify + Docker Compose)

1. In **Coolify** → **New Resource** → **Git Repository** (yours: `ariffazil/arifOS`)
2. **Build Pack**: Docker Compose
3. **Docker Compose Location**: `docker-compose.yml` (root)
4. Add these **Environment Variables** (required for Vault + Redis + Postgres):

| Key | Example Value | Required? |
|:---|:---|:---|
| `DB_PASSWORD` | `your-strong-secret` | Yes |
| `ARIF_JWT_SECRET` | `openssl rand -hex 32` | Recommended |
| `DATABASE_URL` | `postgresql://arifos:${DB_PASSWORD}@postgres:5432/vault999` | Auto-filled if using compose |
| `REDIS_URL` | `redis://redis:6379/0` | Auto-filled |
| `AAA_MCP_OUTPUT_MODE` | `user` or `debug` | Optional |
| `ARIFOS_PHYSICS_DISABLED` | `0` (or `1` to skip thermo calcs) | Optional |

5. **Domain**: `arifosmcp.arif-fazil.com` (or your subdomain)
6. Click **Deploy** → wait ~2–5 min

**After deploy check:**
- `https://arifosmcp.arif-fazil.com/health` → should return `"status": "healthy"`
- If degraded → check logs for Postgres/Redis connection errors → ensure `DB_PASSWORD` matches

### 3. Docker Compose (Standalone or VPS)
Use this minimal `docker-compose.yml` (copy to root):

```yaml
version: '3.9'
services:
  arifosmcp:
    image: ghcr.io/ariffazil/arifos:latest  # or build: .
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "8089:8089"  # optional for HTTP MCP
    env_file: .env
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: vault999
      POSTGRES_USER: arifos
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U arifos"]
      interval: 10s

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Then:**
```bash
docker compose up -d
```

### 4. ChatGPT Sovereign Connector (Developer Mode)
1. Enable **Developer Mode** in ChatGPT Settings → Connectors
2. Create Connector → URL: `https://arifosmcp.arif-fazil.com/mcp`
3. ChatGPT discovers tools (`apex_judge`, `vault_seal`, etc.)
4. Add to any chat → ask governed questions

Docs: [https://arifos.arif-fazil.com/chatgpt](https://arifos.arif-fazil.com/chatgpt)

---

## Why arifOS? (The Problem We Solve)
Ungoverned LLMs → persuasive hallucinations, sovereign overreach, entropic decay.  
arifOS enforces constitutional law before any verdict:

- **13 Floors** (F1 Amanah → F13 Sovereignty)
- **Metabolic pipeline**: 000 INIT → 999 VAULT
- **Verdicts**: `SEAL` | `SABAR/HOLD` | `VOID`
- **Immutable audit**: VAULT999 (Postgres-backed hash chain)

Full floors: [`000_THEORY/000_LAW.md`](000_THEORY/000_LAW.md)

---

## Architecture (Trinity: Δ Ω Ψ)

| Organ | Symbol | Role | Question |
|:---|:---:|:---|:---|
| **AGI** | Δ | Logic / Truth | *Is it true?* |
| **ASI** | Ω | Safety / Empathy | *Is it safe?* |
| **APEX** | Ψ | Authority / Law | *Is it lawful?* |

**Layers**: L0 Kernel (invariant) → L7 Ecosystem

---

## MCP Tools (Exposed via `/tools`)

| Tool | Purpose | Floors Enforced |
|:---|:---|:---|
| `apex_judge` | Full pipeline (000→999) | All |
| `init_session` | Session ignition | F11, F12 |
| `vault_seal` | Commit to immutable Vault | F1, F3 |
| ... | 22+ tools (governance + sensory) | Varies |

---

## Production Hardening
- **HTTPS**: Force in Coolify / Nginx
- **Auth**: Use `ARIF_JWT_SECRET` + JWT middleware (roadmap: RBAC per floor)
- **Scaling**: Add replicas behind load balancer (stateless per request)
- **Monitoring**: Prometheus at `/metrics`, Grafana stack in compose
- **Backup**: Volume backups for `postgres_data` + `VAULT999/`

---

## Contributing & License
- **AGPL-3.0-only** — see `LICENSE`
- PRs welcome: focus on core purity, floor rigor, MCP compliance
- **Oath**: Every output must reduce confusion.

**Ditempa Bukan Diberi**  
Forged, Not Given.

Live MCP: [https://arifosmcp.arif-fazil.com](https://arifosmcp.arif-fazil.com)  
Docs: [https://arifos.arif-fazil.com](https://arifos.arif-fazil.com)  
Trinity: **HUMAN** ↔ **THEORY** ↔ **APPS**

Ditempa Bukan Diberi 🔥
