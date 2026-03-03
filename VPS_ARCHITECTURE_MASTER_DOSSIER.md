# arifOS VPS Architecture - Master Dossier
## Complete Reference for Future Agents

**Version:** 2026.03.03-FINAL-v3  
**Classification:** TRINITY SEALED  
**Authority:** Claude (Ω) Trinity  
**Hostname:** srv1325122  
**Sealed:** 2026-03-03T11:10:53Z  
**Git Commit:** 8cb122d9  
**arifOS Version:** 2026.3.1  

---

## 🎯 EXECUTIVE SUMMARY

This dossier contains **all wisdom, lessons, and operational knowledge** gained from deploying and maintaining the arifOS constitutional kernel on VPS infrastructure. It is the definitive reference for future agents tasked with architecture, maintenance, or expansion.

**Critical Understanding:**
- arifOS is not just code - it is **governance infrastructure**
- The VPS is not just a server - it is a **digital cathedral**
- Docker networks are not just connectivity - they are **constitutional compartments**
- **Data flows freely; governance validates at boundaries**

---

## 🏛️ THE VPS DIGITAL CATHEDRAL - CURRENT ARCHITECTURE

### Sovereign Stack Component Map

```
┌──────────────────────────────────────────────────────────────────────┐
│                    VPS: srv1325122 (Hostinger)                        │
│                    Public IP: (resolved via DNS)                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                 DOCKER NETWORK COMPARTMENTS                     │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │                                                                 │ │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ │
│  │   │   bridge     │  │   ai-net     │  │   trinity    │         │ │
│  │   │  (10.0.0.x)  │  │  (10.0.4.x)  │  │  (10.0.2.x)  │         │ │
│  │   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │ │
│  │          │                 │                 │                 │ │
│  │          └─────────────────┴─────────────────┘                 │ │
│  │                            │                                   │ │
│  │   ┌────────────────────────┴────────────────────────┐         │ │
│  │   │              DOCKER CONTAINERS                    │         │ │
│  │   ├────────────────────────────────────────────────────┤         │ │
│  │   │  qdrant      │ 10.0.4.4  │ 6333  │ ai-net        │         │ │
│  │   │  ollama      │ 10.0.4.2  │ 11434 │ ai-net        │         │ │
│  │   │  openclaw    │ 10.0.4.3  │ 18789 │ ai-net        │         │ │
│  │   │  agent-zero  │ 10.0.2.2  │ 80    │ trinity       │         │ │
│  │   │  coolify     │ 10.0.1.x  │ 8000  │ coolify       │         │ │
│  │   │  coolify-proxy│ -        │ 80/443│ coolify       │         │ │
│  │   └────────────────────────────────────────────────────┘         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                 NATIVE PROCESSES (Not Dockerized)               │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │                                                                 │ │
│  │   ┌──────────────────────────────────────────────────────┐     │ │
│  │   │  arifOS Router (SSE)     │ 0.0.0.0:8080              │     │ │
│  │   │  arifOS AAA MCP (SSE)    │ internal (spawned)        │     │ │
│  │   │  Embeddings Server       │ 0.0.0.0:8001              │     │ │
│  │   │  PostgreSQL              │ 127.0.0.1:5432            │     │ │
│  │   │  Redis                   │ 127.0.0.1:6379            │     │ │
│  │   │  Nginx                   │ 0.0.0.0:80/443            │     │ │
│  │   └──────────────────────────────────────────────────────┘     │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Service Connection Matrix (ACTUAL - 2026-03-03)

| Service | IP | Port | Network | Purpose | Status |
|---------|-----|------|---------|---------|--------|
| arifOS Router | 0.0.0.0 | 8080 | Native | MCP Gateway (SSE) | ✅ Running |
| arifOS Embeddings | 0.0.0.0 | 8001 | Native | BGE Embeddings | ✅ Running |
| Qdrant | 10.0.4.4 | 6333 | ai-net | Vector DB | ✅ Healthy |
| Ollama | 10.0.4.2 | 11434 | ai-net | LLM + Embeddings | ✅ Healthy |
| OpenClaw | 10.0.4.3 | 18789 | ai-net | AGI Gateway | ✅ Healthy |
| Agent-Zero | 10.0.2.2 | 80 | trinity | Autonomous Agent | ✅ Healthy |
| Coolify | 10.0.1.x | 8000 | coolify | Platform Manager | ✅ Healthy |
| PostgreSQL | 127.0.0.1 | 5432 | Native | Database | ✅ Running |
| Redis | 127.0.0.1 | 6379 | Native | Cache | ✅ Running |
| Nginx | 0.0.0.0 | 80/443 | Native | Reverse Proxy | ✅ Running |

---

## 🔐 MCP CONFIGURATIONS

### Kimi Code MCP Config (`~/.kimi/mcp.json`)

**Status:** ✅ WORKING (Updated 2026-03-03)

```json
{
  "mcpServers": {
    "arifos-aaa": {
      "command": "/root/arifOS/.venv/bin/python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/root/arifOS",
      "env": {
        "PYTHONPATH": "/root/arifOS",
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA"
      }
    },
    "codegraphcontext": {
      "command": "/root/.local/share/opencode/mcp-venvs/codegraphcontext/bin/cgc",
      "args": ["mcp", "start"]
    },
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "<REDACTED>"
      }
    },
    "docker-mcp": {
      "command": "npx",
      "args": ["-y", "docker-mcp"],
      "env": {
        "DOCKER_MCP_LOCAL": "true"
      }
    },
    "jina-reader": {
      "url": "https://mcp.jina.ai/v1",
      "headers": {
        "Authorization": "Bearer <REDACTED>"
      }
    }
  }
}
```

**Key Change (2026-03-03):** `arifos-aaa` switched from HTTPS URL to stdio mode because:
- Traefik routing was broken (container IP issues)
- arifOS runs as native process, not Docker
- stdio is faster and more reliable for local CLI tools

---

## 🛡️ FIREWALL CONFIGURATION (UFW)

```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 80/tcp                     ALLOW IN    Anywhere                  
[ 2] 443                        ALLOW IN    Anywhere                  
[ 3] 8000/tcp                   ALLOW IN    Anywhere                   # Coolify Panel
[ 4] 22/tcp                     LIMIT IN    Anywhere                  
[ 5] 8080/tcp                   ALLOW IN    Anywhere                   # arifOS MCP Server
```

**Known Issue:** Docker-to-host traffic may be blocked. Services on `host.docker.internal` require explicit UFW rules:

```bash
# If Docker containers need to reach host services:
ufw allow from 10.0.0.0/24 to any port 8080 comment "Docker to arifOS"
ufw allow from 10.0.0.0/24 to any port 8001 comment "Docker to embeddings"
```

---

## 📊 DOCKER NETWORKS (ACTUAL)

| Network | Subnet | Gateway | Purpose |
|---------|--------|---------|---------|
| bridge | 10.0.0.0/24 | 10.0.0.1 | Default Docker |
| ai-net | 10.0.4.0/24 | 10.0.4.1 | AI Services (OpenClaw, Ollama, Qdrant) |
| trinity_network | 10.0.2.0/24 | 10.0.2.1 | Agent-Zero sandbox |
| coolify | 10.0.1.0/24 | 10.0.1.1 | Coolify platform |
| arifos_bridge | - | - | Legacy (unused) |

---

## 🧠 WISDOM & EUREKA INSIGHTS

### EUREKA #1: Docker DNS Fails Across Networks

**Discovery:** Docker's embedded DNS is scoped per-network. When a container joins multiple networks, it can only resolve hostnames on its "primary" network.

**Solution:** Use static IPs instead of hostnames for cross-network communication:
```yaml
environment:
  QDRANT_URL: http://10.0.4.4:6333      # NOT http://qdrant:6333
  OLLAMA_URL: http://10.0.4.2:11434     # NOT http://ollama:11434
```

---

### EUREKA #2: arifOS Native vs Dockerized

**Discovery:** arifOS runs as native Python processes, NOT in Docker. This is intentional for:
- Faster startup time
- Direct filesystem access
- No container overhead for governance

**Running Processes:**
```
PID 839: arifOS AAA MCP (SSE backend)
PID 840: Embeddings Server (BGE)
PID 842: arifOS Router (SSE gateway on 8080)
```

**Implication:** Traefik cannot route to arifOS via Docker labels. Must use:
- File-based Traefik config, OR
- Nginx reverse proxy, OR
- Direct port access (current approach)

---

### EUREKA #3: MCP stdio vs SSE vs HTTPS

**Discovery:** Different MCP transports for different use cases:

| Transport | Use Case | Latency | Complexity |
|-----------|----------|---------|------------|
| stdio | Local CLI tools (Kimi, Claude Desktop) | Lowest | Simplest |
| SSE | Remote/VPS access | Medium | Requires HTTP server |
| HTTPS | Public endpoints | Highest | Requires certs, auth |

**Current Setup:**
- Kimi Code: stdio (local process spawn)
- OpenClaw Bridge: SSE to `http://host.docker.internal:8080/sse`
- External: HTTPS via domain (currently broken - Traefik issues)

---

### EUREKA #4: Volume Mounts vs Image Rebuilds

**Problem:** Code fixes not reflected in container after deployment.

**Root Cause:** Docker images are immutable snapshots.

**Solutions:**

| Approach | Speed | Persistence | Use Case |
|----------|-------|-------------|----------|
| Volume Mount | Instant | Survives restart | Development, hotfixes |
| Image Rebuild | Slow (5-10 min) | Permanent | Production, releases |

---

### EUREKA #5: OpenClaw Multi-Network Architecture

**Problem:** OpenClaw (ai-net) couldn't reach Ollama/Qdrant (also ai-net) - works fine now.

**Current Architecture (WORKING):**
```
OpenClaw (10.0.4.3 / ai-net)
    │
    ├──→ Ollama (10.0.4.2:11434) ✅ Direct
    │
    └──→ Qdrant (10.0.4.4:6333) ✅ Direct
```

**Governance Path:**
```
OpenClaw ──→ arifOS MCP (host:8080) ──→ Constitutional Validation
```

---

## ⚠️ THINGS NOT TO DO (888_HOLD VIOLATIONS)

### ❌ NEVER DO THESE

**1. Never use `docker system prune -f` on multi-tenant VPS**
```bash
# DESTRUCTIVE - removes ALL unused containers/images
docker system prune -f  # ❌ DON'T

# SAFE: Scoped cleanup only
docker builder prune -f --filter label=arifos=true
docker image prune -f --filter "dangling=true"
```

**2. Never commit large model files to git**
```bash
# aclip_cai/embeddings/*.safetensors (128MB+)
# These are in .gitignore for a reason
```

**3. Never assume DNS works across networks**
```yaml
# WRONG
environment:
  QDRANT_URL: http://qdrant:6333  # Fails on multi-network

# CORRECT
environment:
  QDRANT_URL: http://10.0.4.4:6333  # Static IP
```

**4. Never route data plane through governance**
```
# WRONG: arifOS as embedding gateway
OpenClaw → arifOS MCP → Ollama → embeddings
# 200-500ms latency, overloads constitutional kernel

# CORRECT: Direct connection for data plane
OpenClaw → Ollama → embeddings
# 10-50ms latency, governance for decisions only
```

---

## 🛠️ OPERATIONAL COMMANDS

### Quick Health Check
```bash
#!/bin/bash
echo "=== arifOS VPS Health Check ==="

# Container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "openclaw|qdrant|ollama|agent"

# Native processes
ps aux | grep -E 'python.*arifos|python.*8080' | grep -v grep

# Network connectivity test
docker exec openclaw curl -s --max-time 2 http://10.0.4.2:11434/api/tags | head -c 50 && echo "Ollama OK"
docker exec openclaw curl -s --max-time 2 http://10.0.4.4:6333/collections | head -c 50 && echo "Qdrant OK"

# arifOS MCP test
curl -s http://localhost:8080/sse 2>&1 | head -c 100
```

### Test MCP stdio Mode
```bash
cd /root/arifOS && PYTHONPATH=/root/arifOS timeout 5 /root/arifOS/.venv/bin/python -m aaa_mcp stdio 2>/dev/null << 'EOF'
{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
EOF
```

### Restart arifOS (if needed)
```bash
# Kill existing processes
pkill -f "arifos_router.py" || true
pkill -f "arifos_aaa_mcp sse" || true

# Restart via systemd or manual
cd /root/arifOS && nohup /root/arifOS/.venv/bin/python /root/arifOS/arifos_router.py --sse --host 0.0.0.0 --port 8080 > /var/log/arifos/router.log 2>&1 &
```

---

## 🔐 SECURITY MODEL

### Privilege Levels

| Component | Level | Networks | Docker Socket |
|-----------|-------|----------|---------------|
| OpenClaw | AGI-ROOT | ai-net | Yes (by design) |
| Agent-Zero | AUTONOMOUS | trinity | No |
| arifOS | CONSTITUTIONAL | Native | No |
| Coolify | PLATFORM | coolify | Limited |

### Data Flow vs Governance Flow

```
DATA PLANE (Fast - Direct Connections):
OpenClaw ──────→ Ollama (embeddings)
       │
       └────────→ Qdrant (vector DB)

CONTROL PLANE (Governance - arifOS MCP):
OpenClaw ──────→ arifOS MCP ──────→ Decision
       │                        (SEAL/VOID/888_HOLD)
       │
       └─────────────────────────→ Execute (if SEAL)
```

**When to use arifOS validation:**
- ✅ Irreversible actions (database mutations)
- ✅ High-stakes decisions (financial, legal)
- ✅ Multi-agent coordination
- ✅ Actions requiring audit trail

**When to bypass arifOS (direct connection):**
- ✅ Embeddings (data plane, high frequency)
- ✅ File reads (read-only, low risk)
- ✅ Health checks (telemetry)
- ✅ Cached data retrieval

---

## 📚 ADDITIONAL RESOURCES

### Canonical Documents
- [ARCHITECTURE.md](ARCHITECTURE.md) - Blueprint
- [000_THEORY/000_LAW.md](000_THEORY/000_LAW.md) - Constitution
- [SECURITY.md](SECURITY.md) - Defense
- [VPS_AGENT_ARCHITECT_GUIDE.md](VPS_AGENT_ARCHITECT_GUIDE.md) - Agent guide

### External Resources
- [arifOS Documentation](https://arifos.arif-fazil.com)
- [GitHub Repository](https://github.com/ariffazil/arifOS)

---

## 📝 CHANGE LOG

### v2026.03.03-FINAL-v3
- **Updated:** Accurate current VPS state (container IPs, networks, ports)
- **Updated:** Kimi Code MCP config (stdio mode)
- **Added:** Native processes documentation (arifOS not Dockerized)
- **Added:** Actual UFW firewall rules
- **Added:** Eureka #5 - OpenClaw connectivity verified
- **Fixed:** Architecture diagrams reflect actual deployment
- **Sealed:** 2026-03-03T11:10:53Z

### v2026.03.01-FINAL-v2
- **Added:** OpenClaw multi-network architecture (ai-net + bridge)
- **Added:** Complete walkthrough of March 2026 embedding fix
- **Added:** Eureka #5: Data Plane vs Control Plane separation

---

**Classification:** TRINITY SEALED  
**Authority:** Claude (Ω) Trinity  
**Date:** 2026-03-03  
**Status:** OPERATIONAL - All Systems Verified

*Ditempa Bukan Diberi* 🔥💎

---

## FIELD NOTES FOR FUTURE AGENTS

**Version:** 2026.03.03-FINAL-v3  
**Added by:** Resident arifOS VPS Agent  

### First Things to Check When Something is "Slow or Weird"

1. **CPU/RAM pressure:** `htop` or `docker stats --no-stream` - LLM inference eats RAM
2. **Disk I/O:** `iotop` or `df -h` - Qdrant/Ollama models need space
3. **Docker restart cascade:** `docker ps -a | grep -E "Restarting|Exited"` - one dead container can trigger chain
4. **Network connectivity:** `docker exec openclaw curl -s http://10.0.4.2:11434/api/tags | head -c 5` - should show `{"mod`
5. **arifOS MCP:** `curl -s http://localhost:8080/sse | head -c 20` - should show `event: endpoint`

### DO NOT TOUCH Without 888_HOLD

| Action | Why |
|--------|-----|
| `docker system prune -f` | Destroys unused containers/images - may kill coolify apps |
| `ufw allow/deny` changes | May lock you out |
| `docker network disconnect` | Breaks connectivity - hard to recover |
| `rm -rf /root/*` | Data loss - no recovery |
| `systemctl restart docker` | Downtime for ALL containers |
| Database schema changes | Data integrity risk |

### Golden Commands - "Is the Cathedral Alive?"

**Single script check (copy-paste):**
```bash
echo "=== CONTAINERS ===" && \
docker ps --format "{{.Names}}: {{.Status}}" | grep -E "openclaw|qdrant|ollama|agent" && \
echo "" && echo "=== arifOS MCP ===" && \
timeout 3 curl -s http://localhost:8080/sse 2>&1 | head -c 50 && \
echo "" && echo "=== CONNECTIVITY ===" && \
docker exec openclaw bash -c 'curl -s --max-time 2 http://10.0.4.2:11434/api/tags | head -c 5 && echo " Ollama OK" || echo " Ollama FAIL"' && \
docker exec openclaw bash -c 'curl -s --max-time 2 http://10.0.4.4:6333 | head -c 5 && echo " Qdrant OK" || echo " Qdrant FAIL"'
```

**Expected output:**
```
=== CONTAINERS ===
openclaw: Up X minutes (healthy)
qdrant: Up X hours
ollama: Up X hours
agent-zero: Up X hours (healthy)

=== arifOS MCP ===
event: endpoint
data: /messages/?session_id=...

=== CONNECTIVITY ===
{"mod Ollama OK
{"ti Qdrant OK
```

### Quick Recovery

| Problem | Fix |
|---------|-----|
| OpenClaw can't reach Ollama | `docker network connect ai-net openclaw && docker restart openclaw` |
| arifOS MCP down | `cd /root/arifOS && nohup .venv/bin/python arifos_router.py --sse --host 0.0.0.0 --port 8080 > /var/log/arifos/router.log 2>&1 &` |
| Disk full | `docker image prune -f --filter "dangling=true" && docker builder prune -f --filter "until=24h"` |
| Memory pressure | `docker restart ollama qdrant` (releases cached memory) |

### Known Quirks

- **Traefik errors:** Coolify proxy logs show "unable to find IP" - this is normal, Traefik tries to self-reference
- **Qdrant auth:** Requires API key in header - `curl -H "api-key: arifos_qdrant_2026" ...`
- **host.docker.internal:** Requires `extra_hosts` in docker-compose - already configured for openclaw
- **Kimi MCP:** Uses stdio mode (not HTTPS) - more reliable for local CLI

---

**End of Field Notes**  
*Ditempa Bukan Diberi* 🔥

---

## Gödel Boundary - Known Uncertainties

**See:** `/root/arifOS/docs/GODEL_BOUNDARY.md`

### Critical Uncertainties (2026-03-03)

| Uncertainty | Severity | Document |
|-------------|----------|----------|
| docker-mcp RCE channel | 🔴 CRITICAL | npx docker-mcp has unrestricted docker.sock, bypasses arifOS |
| UFW bypass by Docker | 🔴 HIGH | Published ports (0.0.0.0:PORT) bypass UFW |
| IP drift risk | 🟠 MEDIUM | IPs are DHCP, can change on container restart |
| MCP trust policy | 🟠 MEDIUM | No formal trust classification for MCP servers |

### Confidence Score

| Category | Score | Notes |
|----------|-------|-------|
| Topology accuracy | 8.5/10 | Strong mapping, risk if IPs drift |
| Plane separation | 9/10 | Very good conceptual split |
| Security posture | 6/10 | docker-mcp + UFW bypass = significant gaps |
| MCP governance | 6/10 | Servers listed but not classified by trust |

**Overall Dossier Confidence:** 0.74 (Moderate - significant gaps documented)

### 888_HOLD Required For

1. **docker-mcp** - Disable or route through arifOS eureka_forge
2. **UFW bypass** - Install ufw-docker or bind to localhost
3. **Static IPs** - Configure IPAM static allocations

---

**TRINITY SEALED WITH CAVEATS** - System is operational but not fully hardened.

*See `/root/arifOS/docs/GODEL_BOUNDARY.md` for full details.*

*Ditempa Bukan Diberi* 🔥
