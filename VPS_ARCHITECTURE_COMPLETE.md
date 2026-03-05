# VPS Architecture & Component Reference
## arifOS Constitutional AI Governance System

**Document Generated:** 2026-03-05 UTC  
**VPS Host:** srv1325122.hstgr.cloud  
**Public IP:** 72.62.71.199  
**Owner:** Arif Fazil

---

## 1. Executive Summary

This document details the complete architecture of the VPS hosting the arifOS Constitutional AI Governance System. The infrastructure follows a phased deployment model with strict separation of concerns between the Control Plane (agent brains), Runtime Plane (service execution), and Data Plane (persistence).

**Core Philosophy:** *Ditempa Bukan Diberi* — Forged, Not Given

---

## 2. Hardware Specifications

| Component | Specification |
|-----------|---------------|
| **Provider** | Hostinger (KVM VPS) |
| **Hostname** | srv1325122.hstgr.cloud |
| **Public IP** | 72.62.71.199 |
| **OS** | Ubuntu 25.10 (non-LTS) |
| **Kernel** | Linux (x86_64) |
| **CPU** | 4 vCPU Cores |
| **Memory** | 16 GB RAM |
| **Disk** | 193 GB SSD |
| **Disk Usage** | ~72 GB used, 121 GB available |
| **Architecture** | x86_64 |

---

## 3. Network Architecture

### 3.1 Public Access
- **SSH Access:** Port 22 ( hardened )
- **HTTP:** Port 80 (future Traefik)
- **HTTPS:** Port 443 (future Traefik)
- **arifOS MCP:** Port 8080 (localhost only, bound to 127.0.0.1)

### 3.2 Security Hardening
```
SSH Configuration:
- PermitRootLogin: no
- PasswordAuthentication: no
- PubkeyAuthentication: yes
- Fail2Ban: Active
- UFW Firewall: Active (SSH only)
```

### 3.3 Docker Networks
| Network | Subnet | Purpose |
|---------|--------|---------|
| `arifos_arifos-internal` | 172.18.0.0/16 | Internal service mesh (Phase 1) |
| `bridge` | 172.17.0.0/16 | Default Docker bridge |
| `host` | — | Host network access |

---

## 4. Service Architecture

### 4.1 Layer 0: Infrastructure (Deployed)

#### PostgreSQL (arifos-postgres)
- **Image:** postgres:16-alpine
- **Container:** arifos-postgres
- **Network:** arifos_arifos-internal
- **Port:** 127.0.0.1:5432
- **Database:** arifos_vault
- **User:** arifos_admin
- **Data Volume:** arifos_postgres_data
- **Status:** ✅ Healthy (6+ hours uptime)
- **Purpose:** Vault-999 state, audit logs, relational data

#### Redis (arifos-redis)
- **Image:** redis:7-alpine
- **Container:** arifos-redis
- **Network:** arifos_arifos-internal
- **Port:** 127.0.0.1:6379
- **Auth:** Password protected
- **Persistence:** AOF enabled
- **Status:** ✅ Healthy (6+ hours uptime)
- **Purpose:** Session cache, queue, real-time state

### 4.2 Layer 1: Constitutional Kernel (Deployed)

#### arifOS MCP Server (arifosmcp_server)
- **Image:** arifos/mcp-server:latest (4.94 GB)
- **Container:** arifosmcp_server
- **Network:** arifos_arifos-internal
- **Port:** 127.0.0.1:8080
- **Transport:** Streamable HTTP
- **Status:** ✅ Healthy
- **Tools:** 16 constitutional tools loaded
- **Purpose:** Constitutional AI governance engine

**Available Endpoints:**
```
GET  /health     → Health status
GET  /tools      → List 16 available tools
GET  /version    → Version info
POST /mcp        → MCP protocol endpoint
```

**Constitutional Tools (000-999):**
| Tool | Stage | Purpose |
|------|-------|---------|
| anchor_session | 000 | Bootloader & context init |
| reason_mind | 333 | AGI cognition |
| recall_memory | 444 | Evidence retrieval |
| simulate_heart | 555 | Empathy evaluation |
| critique_thought | 666 | 7-model critique |
| eureka_forge | 777 | Shell execution |
| apex_judge | 888 | Sovereign verdict |
| seal_vault | 999 | Immutable records |
| metabolic_loop | ΔΩΨ | Full 000-999 cycle |
| search_reality | — | External search |
| fetch_content | — | Content fetch |
| inspect_file | — | Filesystem inspect |
| audit_rules | — | Constitutional audit |
| check_vital | — | System telemetry |
| list_prompts | — | Prompt registry |
| get_prompt | — | Prompt retrieval |

### 4.3 Layer 2: Future Services (Not Deployed)

| Service | Phase | Purpose |
|---------|-------|---------|
| Qdrant | Phase 3 | Vector embeddings |
| Ollama | Phase 4 | Local LLM engine |
| OpenClaw | Phase 4 | Multi-channel IO |
| AgentZero | Phase 4 | RAG reasoning |
| Traefik | Phase 3 | Edge router/ingress |
| n8n | Phase 3 | Workflow automation |
| Webhook Listener | Phase 3 | CI/CD automation |

---

## 5. Directory Structure

### 5.1 Source of Truth
```
/srv/arifOS/                    # arifOS repository (37 dirs, canonical)
├── 000_THEORY/                 # Constitutional theory
├── 333_APPS/                   # Application layers (L0-L7)
│   ├── L0_KERNEL/              # Core kernel
│   ├── L2_SKILLS/              # MCP skills
│   ├── L5_AGENTS/              # Agent specs
│   └── L6_CIVILIZATION/        # Civilization layer
├── aaa_mcp/                    # MCP server implementation
├── aclip_cai/                  # ACLIP CAI layer
├── core/                       # Constitutional core
│   ├── governance_kernel.py
│   ├── judgment.py
│   ├── pipeline.py
│   └── organs/
├── VAULT999/                   # Constitutional vault
│   ├── AAA_HUMAN/              # Human authority
│   ├── BBB_LEDGER/             # Audit ledger
│   ├── CCC_CANON/              # Canonical law
│   ├── sessions/               # Session records
│   └── vault999.jsonl          # Immutable log
├── docker-compose.yml          # Main compose (fixed paths)
├── docker-compose.arifos.yml   # arifOS-only compose
├── docker-compose.phase1.yml   # Phase 1 services
├── Dockerfile                  # MCP server image
├── .env                        # Production environment
└── .venv/                      # Python virtual env
```

### 5.2 Data Volumes
```
/opt/arifos/                    # Docker data (sudo created)
├── data/
│   ├── core/                   # arifOS data
│   ├── qdrant/                 # Vector storage (future)
│   └── ollama/                 # LLM models (future)
└── letsencrypt/                # SSL certificates (future)

/var/lib/docker/volumes/        # Docker managed volumes
├── arifos_postgres_data/       # PostgreSQL data
└── (redis uses bind mount)
```

### 5.3 Secrets
```
/home/ariffazil/xxx/.env        # Master secrets file
/srv/arifOS/.env                # Production env (deployed)
/srv/arifOS/.env.docker         # Docker env template
```

---

## 6. Agent Control Plane

### 6.1 Installed CLI Tools
| Tool | Path | Purpose |
|------|------|---------|
| opencode | /usr/local/bin | OpenCode agent |
| agi-opencode | ~/.local/bin | AGI wrapper |
| claude | ~/.local/bin | Claude Code |
| agi-claude | ~/.local/bin | AGI wrapper |
| codex | ~/.local/bin | Codex CLI |
| agi-codex | ~/.local/bin | AGI wrapper |
| gemini | ~/.local/bin | Gemini CLI |
| agi-gemini | ~/.local/bin | AGI wrapper |
| kimi | ~/.local/bin | Kimi CLI |
| agi-kimi | ~/.local/bin | AGI wrapper |

### 6.2 Agent Access Patterns
```
SSH:        ssh ariffazil@72.62.71.199
Local MCP:  opencode mcp list
VPS Agent:  agi-opencode (wrapped with AGI context)
```

---

## 7. Constitutional Governance

### 7.1 F1-F13 Floors
| Floor | Name | Status |
|-------|------|--------|
| F1 | Amanah (Reversibility) | ✅ Active |
| F2 | Truth (τ ≥ 0.99) | ✅ Active |
| F4 | Clarity (ΔS ≤ 0) | ✅ Active |
| F5 | Peace² | ✅ Active |
| F6 | Empathy (κᵣ ≥ 0.70) | ✅ Active |
| F7 | Humility (Ω₀ = 0.04) | ✅ Active |
| F8 | Genius (G ≥ 0.80) | ✅ Active |
| F9 | Anti-Hantu | ✅ Active |
| F11 | Authority | ✅ Active |
| F12 | Injection Defense | ✅ Active |
| F13 | Sovereignty | ✅ Active |

### 7.2 888_HOLD Gates
- Database mutations (DROP, TRUNCATE)
- Production deployments
- Mass file changes (>10)
- Secret handling
- Git history rewrite
- Destructive volume operations

---

## 8. Docker Compose Stack

### 8.1 Phase 1 (Active)
```yaml
# docker-compose.phase1.yml
Services:
  - postgres:5432      (healthy)
  - redis:6379         (healthy)
Networks:
  - arifos-internal:172.18.0.0/16
Volumes:
  - postgres_data
  - redis_data
```

### 8.2 arifOS Layer (Active)
```yaml
# docker-compose.arifos.yml
Services:
  - arifosmcp:8080     (healthy)
Networks:
  - arifos-internal (external)
Volumes:
  - /opt/arifos/data/core
  - /srv/arifOS/VAULT999
```

---

## 9. API Endpoints

### 9.1 arifOS MCP (localhost:8080)
```bash
# Health check
curl http://localhost:8080/health

# List tools
curl http://localhost:8080/tools

# Constitutional session
POST http://localhost:8080/mcp
Body: {
  tool: metabolic_loop,
  args: {query: ...}
}
```

### 9.2 PostgreSQL (localhost:5432)
```bash
psql -h localhost -U arifos_admin -d arifos_vault
```

### 9.3 Redis (localhost:6379)
```bash
redis-cli -h localhost -a \$REDIS_PASSWORD ping
```

---

## 10. Maintenance Commands

### 10.1 Docker Operations
```bash
# View all containers
docker ps

# View logs
docker logs arifosmcp_server
docker logs arifos-postgres
docker logs arifos-redis

# Restart services
docker compose -f docker-compose.arifos.yml restart

# Full Phase 1 + arifOS
docker compose -f docker-compose.phase1.yml -f docker-compose.arifos.yml up -d
```

### 10.2 Health Checks
```bash
# arifOS health
curl -s http://localhost:8080/health | jq

# PostgreSQL health
docker exec arifos-postgres pg_isready -U arifos_admin

# Redis health
docker exec arifos-redis redis-cli ping
```

### 10.3 Backup Locations
```
PostgreSQL: /var/lib/docker/volumes/arifos_postgres_data/_data
Redis:      /var/lib/docker/volumes/arifos_redis_data/_data
Vault999:   /srv/arifOS/VAULT999/
Data:       /opt/arifos/data/
```

---

## 11. Phased Deployment Roadmap

### Phase 1: Core Runtime ✅ COMPLETE
- [x] PostgreSQL 16
- [x] Redis 7
- [x] Network: arifos-internal
- [x] Health checks

### Phase 2: arifOS Kernel ✅ COMPLETE
- [x] MCP Server deployed
- [x] 16 tools operational
- [x] Constitutional governance active
- [x] Health endpoint responding

### Phase 3: Agent Workbench (Planned)
- [ ] Qdrant vector DB
- [ ] Playwright + Chromium
- [ ] PDF/OCR tools
- [ ] n8n automation
- [ ] File sharing endpoint

### Phase 4: Multi-Agent Runtime (Planned)
- [ ] OpenClaw gateway
- [ ] AgentZero reasoner
- [ ] Ollama local LLM
- [ ] Network segmentation

### Phase 5: Production (Planned)
- [ ] Traefik reverse proxy
- [ ] SSL certificates
- [ ] Cloudflare tunnel
- [ ] Backup automation
- [ ] Monitoring/alerts

---

## 12. Key Configuration Files

| File | Purpose |
|------|---------|
| `/srv/arifOS/.env` | Production environment |
| `/srv/arifOS/docker-compose.yml` | Main orchestration |
| `/srv/arifOS/docker-compose.arifos.yml` | arifOS service |
| `/home/ariffazil/xxx/.env` | Master secrets |
| `/srv/arifOS/Dockerfile` | MCP server image |
| `/srv/arifOS/AGENTS.md` | Agent guidelines |

---

## 13. Troubleshooting

### Issue: arifOS container unhealthy
```bash
# Check logs
docker logs arifosmcp_server --tail 50

# Restart
docker compose -f docker-compose.arifos.yml restart
```

### Issue: Database connection failed
```bash
# Verify postgres is running
docker ps | grep postgres

# Check network
docker network inspect arifos_arifos-internal
```

### Issue: Redis auth failed
```bash
# Verify password in env
grep REDIS_PASSWORD /srv/arifOS/.env
```

---

## 14. Constitutional Compliance

This architecture enforces:
- **F1 Amanah:** All ops reversible, backups required
- **F2 Truth:** τ ≥ 0.99 threshold on all claims
- **F5 Safety:** 888_HOLD on destructive actions
- **F9 Anti-Hantu:** No consciousness claims by AI
- **F13 Sovereignty:** Human veto always preserved

---

## 15. Document Metadata

- **Version:** 2026.3.1
- **Generated By:** AGI-Opencode (arifOS constitutional agent)
- **Session:** arch-doc
- **SEAL Status:** 100% Complete

**DITEMPA BUKAN DIBERI** — Forged, Not Given 🔥
