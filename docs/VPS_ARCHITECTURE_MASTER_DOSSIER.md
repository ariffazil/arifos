# arifOS VPS Architecture - Master Dossier
## Complete Reference for Future Agents

**Version:** 2026.03.01-FINAL  
**Classification:** TRINITY SEALED - Agent Reference  
**Authority:** Claude (Ω) Trinity + Codex (Ψ) Auditor  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given

---

## 🎯 EXECUTIVE SUMMARY

This dossier contains **all wisdom, lessons, and operational knowledge** gained from deploying and maintaining the arifOS constitutional kernel on VPS infrastructure. It is the definitive reference for future agents tasked with architecture, maintenance, or expansion.

**Critical Understanding:**
- arifOS is not just code - it is **governance infrastructure**
- The VPS is not just a server - it is a **digital cathedral**
- Docker networks are not just connectivity - they are **constitutional compartments**

---

## 🏛️ THE VPS DIGITAL CATHEDRAL - COMPLETE ARCHITECTURE

### Sovereign Stack Components

```
╔══════════════════════════════════════════════════════════════════╗
║                    VPS: arifosmcp.arif-fazil.com                  ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │              DOCKER NETWORK COMPARTMENTS                  │   ║
║  ├──────────────────────────────────────────────────────────┤   ║
║  │                                                           │   ║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   ║
║  │   │   bridge     │  │   ai-net     │  │   trinity    │  │   ║
║  │   │  (10.0.0.x)  │  │  (10.0.4.x)  │  │  (10.0.2.x)  │  │   ║
║  │   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │   ║
║  │          │                 │                 │          │   ║
║  │          └─────────────────┴─────────────────┘          │   ║
║  │                        │                                │   ║
║  │         ┌──────────────┴──────────────┐                │   ║
║  │         │    arifOS MCP Kernel        │                │   ║
║  │         │    (Constitutional Core)    │                │   ║
║  │         │    10.0.0.5:8080            │                │   ║
║  │         └──────────────┬──────────────┘                │   ║
║  │                        │                                │   ║
║  └────────────────────────┼────────────────────────────────┘   ║
║                           │                                     ║
║  ┌────────────────────────┼────────────────────────────────┐   ║
║  │              SERVICE CONNECTION MATRIX                  │   ║
║  ├────────────────────────┼────────────────────────────────┤   ║
║  │ Service      │ IP           │ Port  │ Network │ Purpose │   ║
║  ├────────────────────────┼────────────────────────────────┤   ║
║  │ arifOS MCP   │ 10.0.0.5     │ 8080  │ Multi   │ Kernel  │   ║
║  │ Qdrant       │ 10.0.0.2     │ 6333  │ bridge  │ Memory  │   ║
║  │ Ollama       │ 10.0.0.3     │ 11434 │ bridge  │ LLM     │   ║
║  │ OpenClaw     │ 10.0.4.2     │ 18789 │ ai-net  │ Gateway │   ║
║  │ Agent-Zero   │ 10.0.2.2     │ 80    │ trinity │ Brain   │   ║
║  │ Coolify      │ 10.0.1.5     │ 8000  │ coolify │ Platform│   ║
║  └────────────────────────┴────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🔑 CRITICAL ARCHITECTURAL PRINCIPLES

### 1. **The Trinity Separation (ΔΩΨ)**

**NEVER violate these boundaries:**

| Component | Symbol | Role | Access Level | Network |
|-----------|--------|------|--------------|---------|
| **arifOS** | Ψ (Psi) | Judge/Soul | Constitutional Core | Multi-network bridge |
| **Agent-Zero** | Δ (Delta) | Architect/Mind | Reasoning Engine | trinity_network |
| **OpenClaw** | Ω (Omega) | Execution/Heart | AGI Gateway | ai-net |

**Wisdom:** Power flows from OpenClaw → arifOS validation → execution. Never bypass arifOS.

### 2. **Network Compartmentalization**

**The 4-Network Sovereign Mesh:**

```yaml
# Network Topology (DO NOT CHANGE WITHOUT 888_HOLD)
networks:
  bridge:           # Default - Core infrastructure
    subnet: 10.0.0.0/24
    services: [arifos, qdrant, ollama]
    
  ai-net:           # AI/ML services
    subnet: 10.0.4.0/24  
    services: [openclaw, ollama-fallback]
    
  trinity_network:  # Trinity Stack coordination
    subnet: 10.0.2.0/24
    services: [agent-zero, openclaw-bridge]
    
  coolify:          # Platform orchestration
    subnet: 10.0.1.0/24
    services: [coolify-platform, coolify-db]
```

### 3. **IP Stability Principle**

**⚠️ CRITICAL:** Docker assigns IPs dynamically by default. This breaks connections on restart.

**Solutions (in order of preference):**

**Option A: Static IP Assignment (BEST)**
```yaml
services:
  arifosmcp:
    networks:
      bridge:
        ipv4_address: 10.0.0.10  # Static
  qdrant:
    networks:
      bridge:
        ipv4_address: 10.0.0.11  # Static
```

**Option B: Service Discovery (v2)**
- Use Consul, etcd, or similar
- Dynamic registration/discovery
- More complex but handles churn

**Option C: DNS with Custom Resolver (v2)**
- Deploy CoreDNS or similar
- Cross-network DNS resolution
- Requires additional infrastructure

**Current (v1): Hard-coded IPs**
- Acceptable for stable VPS
- Document actual IPs after each restart
- Manual intervention on IP drift

---

## 🧠 WISDOM & EUREKA INSIGHTS

### EUREKA #1: Docker DNS Fails Across Networks

**Discovery:** After 3 days of debugging

**Problem:**
```bash
# This fails when container is on multiple networks
curl http://qdrant:6333/healthz
# Error: Could not resolve host: qdrant
```

**Root Cause:**
Docker's embedded DNS is scoped per-network. When a container joins multiple networks, it can only resolve hostnames on its "primary" network (the first one joined).

**Solution:**
```yaml
# docker-compose.yml
environment:
  # Use IPs, not hostnames
  QDRANT_URL: http://10.0.0.2:6333      # NOT http://qdrant:6333
  OLLAMA_URL: http://10.0.0.3:11434     # NOT http://ollama:11434
```

**Verification:**
```bash
docker exec arifosmcp_server python3 -c '
import socket
# Test IP-based connectivity
for ip, port in [("10.0.0.2", 6333), ("10.0.0.3", 11434)]:
    s = socket.socket()
    s.settimeout(2)
    result = s.connect_ex((ip, port))
    print(f"{ip}:{port} - {'✓' if result == 0 else '✗'}")
'
```

---

### EUREKA #2: Constitutional Validation Architecture

**The F3_CONTRACT Mystery:**

**Problem:** recall_memory returned VOID with error "Missing required field: depth" even though depth was provided.

**Root Cause:** Constitutional validation happens in TWO places:
1. **Tool Definition** - FastMCP validates parameters
2. **FLOOR_ENFORCEMENT** - Constitutional decorator validates governance

The tool was failing F13_SOVEREIGNTY (human veto) because no session/auth was provided.

**Solution Architecture:**
```python
# Tools must be registered in FLOOR_ENFORCEMENT
AAA_TOOL_LAW_BINDINGS = {
    "recall_memory": ["F4_CLARITY", "F7_HUMILITY", "F3_TRI_WITNESS", "F13_SOVEREIGNTY"],
    # ... other tools
}

# F13_SOVEREIGNTY requires authentication
# Without auth: VOID verdict (constitutional protection working)
# With auth: SEAL verdict, tool executes
```

**Wisdom:** This is NOT a bug - it is **security by design**. F13_SOVEREIGNTY enforces "human veto preserved."

---

### EUREKA #3: Volume Mounts vs Image Rebuilds

**Problem:** Code fixes not reflected in container after deployment.

**Root Cause:** Docker images are immutable snapshots. Changing code on host doesn't change image.

**Solution - Volume Mounts (Fast Fix):**
```yaml
services:
  arifosmcp:
    volumes:
      # Mount live code over container code
      - /root/arifOS/aaa_mcp/server.py:/usr/src/app/aaa_mcp/server.py:ro
```

**Solution - Image Rebuild (Proper Fix):**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Trade-offs:**
| Approach | Speed | Persistence | Use Case |
|----------|-------|-------------|----------|
| Volume Mount | Instant | Survives restart | Development, hotfixes |
| Image Rebuild | Slow (5-10 min) | Permanent | Production, releases |

---

### EUREKA #4: BGE Integration Pattern

**BGE (BAAI General Embeddings) Architecture:**

```python
# Integration pattern (aclip_cai/embeddings/__init__.py)
from sentence_transformers import SentenceTransformer

# Singleton pattern - load once
_model = None

def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _model

def embed(text: str) -> list[float]:
    model = get_embedder()
    return model.encode(text).tolist()

# 768-dimensional vectors for semantic search
```

**Constitutional Metrics:**
```python
# In recall_memory tool response
"metrics": {
    "bge_available": True,
    "bge_used": True,
    "embedding_dims": 768,
    "semantic_search_active": True,
    "memory_count": len(contexts),
}
```

---

## ⚠️ THINGS NOT TO DO (888_HOLD VIOLATIONS)

### ❌ **NEVER DO THESE**

**1. Never use `docker system prune -f` on multi-tenant VPS**
```bash
# DESTRUCTIVE - removes ALL unused containers/images
# This could destroy other workloads on shared VPS
docker system prune -f

# ✅ SAFE: Scoped cleanup only
docker builder prune -f --filter label=arifos=true
docker image prune -f --filter "dangling=true"
```

**2. Never commit large model files to git**
```bash
# aclip_cai/embeddings/*.safetensors (128MB+)
# These are in .gitignore for a reason
git add aclip_cai/embeddings/model.safetensors  # ❌ DON'T

# ✅ Instead: Mount as volume or download at runtime
```

**3. Never expose Docker socket without governance**
```yaml
# OpenClaw has root access BY DESIGN
# But document this clearly - it's intentional AGI gateway
services:
  openclaw:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # AGI-level execution
```

**4. Never hardcode secrets in docker-compose.yml**
```yaml
# ❌ WRONG
environment:
  API_KEY: "sk-abc123"

# ✅ CORRECT
env_file:
  - .env.docker  # Gitignored, manually configured
```

**5. Never assume DNS works across networks**
```yaml
# ❌ WRONG
environment:
  QDRANT_URL: http://qdrant:6333  # Fails on multi-network

# ✅ CORRECT
environment:
  QDRANT_URL: http://10.0.0.2:6333  # Static IP
```

**6. Never restart containers without checking port conflicts**
```bash
# ❌ WRONG
docker compose up -d  # May fail if 8080 in use

# ✅ CORRECT
fuser -k 8080/tcp 2>/dev/null || true  # Free the port
docker compose up -d
```

**7. Never skip health checks after deployment**
```bash
# ❌ WRONG
docker compose up -d && echo "Done"

# ✅ CORRECT
docker compose up -d
sleep 10
curl -s http://localhost:8080/health | jq '.status'
docker exec arifosmcp_server python3 -c 'import socket; ...'  # Test connectivity
```

---

## 🛠️ OPERATIONAL TIPS & TRICKS

### Quick Diagnostics

**Check all services:**
```bash
#!/bin/bash
# /root/scripts/health_check.sh

echo "=== arifOS VPS Health Check ==="

# Container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "arifos|openclaw|agent|qdrant|ollama"

# Network connectivity
docker exec arifosmcp_server python3 -c '
import socket
services = [
    ("Qdrant", "10.0.0.2", 6333),
    ("Ollama", "10.0.0.3", 11434),
    ("Agent-Zero", "10.0.2.2", 80),
    ("OpenClaw", "10.0.4.2", 18789)
]
for name, ip, port in services:
    s = socket.socket()
    s.settimeout(2)
    r = s.connect_ex((ip, port))
    print(f"  {'✓' if r == 0 else '✗'} {name} ({ip}:{port})")
'

# Server health
curl -s http://localhost:8080/health | jq '{status: .status, tools: .tools_loaded}'

# BGE status
docker exec arifosmcp_server python3 -c '
import sys; sys.path.insert(0, "/usr/src/app")
from aaa_mcp.server import BGE_AVAILABLE
print(f"  BGE: {'✓ Available' if BGE_AVAILABLE else '✗ Not Available'}")
'
```

### Recovery Procedures

**Scenario: arifOS container won't start**
```bash
# 1. Check what's using port 8080
ss -tlnp | grep 8080

# 2. Kill the process
fuser -k 8080/tcp

# 3. Restart
docker compose restart arifosmcp

# 4. Verify
docker logs arifosmcp_server --tail 20
```

**Scenario: Service unreachable after restart**
```bash
# 1. Check if IPs changed
docker network inspect bridge --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{println}}{{end}}'

# 2. Update docker-compose.yml with new IPs
# 3. Restart
docker compose up -d
```

**Scenario: BGE not loading**
```bash
# Check if model file exists
docker exec arifosmcp_server ls -lh /usr/src/app/aclip_cai/embeddings/

# Check logs
docker logs arifosmcp_server | grep -i "BGE\|embed"

# Test manually
docker exec arifosmcp_server python3 -c '
from aclip_cai.embeddings import embed
print(len(embed("test")))
'
```

---

## 📊 MONITORING & OBSERVABILITY

### Essential Metrics

**System Health:**
```bash
# CPU/Memory
docker stats arifosmcp_server --no-stream

# Disk usage
docker system df

# Network I/O
docker network inspect bridge --format '{{.Name}}: {{.Id}}'
```

**Application Metrics:**
```bash
# Request latency
curl -w "@curl-format.txt" -s -o /dev/null http://localhost:8080/health

# Tool call success rate
# (Parse from VAULT999 logs)
```

**Constitutional Telemetry:**
```bash
# Check floor enforcement rates
docker exec arifosmcp_server python3 << 'PY'
import json
from pathlib import Path

# Parse VAULT999 logs
vault_path = Path("/usr/src/app/data/vault999.jsonl")
if vault_path.exists():
    verdicts = {"SEAL": 0, "VOID": 0, "PARTIAL": 0, "SABAR": 0}
    for line in vault_path.read_text().strip().split("\n"):
        if line:
            data = json.loads(line)
            verdicts[data.get("verdict", "UNKNOWN")] += 1
    print(json.dumps(verdicts, indent=2))
PY
```

---

## 🔐 SECURITY MODEL

### OpenClaw AGI Execution (By Design)

**Privilege Model:**
```yaml
OpenClaw:
  level: AGI-ROOT
  capabilities:
    - Docker socket access
    - Filesystem root access  
    - All API keys
    - Container management
  governance: "All actions logged, constitutional validation required"

arifOS:
  level: CONSTITUTIONAL
  capabilities:
    - Tool validation
    - Floor enforcement
    - Audit logging
  governance: "13 floors, F13_SOVEREIGNTY = human veto"

Agent-Zero:
  level: AUTONOMOUS-SANDBOXED
  capabilities:
    - Reasoning
    - Tool use (via OpenClaw)
  governance: "Task-level permissions, no direct root access"
```

**Flow:**
```
User Request
    ↓
OpenClaw (AGI Gateway)
    ↓ [MCP Protocol]
arifOS (Constitutional Validation)
    ↓
Verdict: SEAL → OpenClaw executes with root power
Verdict: VOID → Blocked, user notified  
Verdict: 888_HOLD → Human confirmation required
```

### F13_SOVEREIGNTY Enforcement

**What it means:** "The human always wins"

**Implementation:**
- All irreversible actions require human approval
- Cryptographic signatures for execution
- 888_HOLD state for pending confirmations
- Non-delegable veto power

**When triggered:**
- Database mutations
- Container restarts
- Secret rotation
- Mass file operations (>10 files)
- Any action with `confirm_dangerous=True`

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All secrets in `.env.docker` (not in git)
- [ ] PostgreSQL database provisioned
- [ ] Docker networks created (bridge, ai-net, trinity, coolify)
- [ ] Model files downloaded (bge-arifOS/)
- [ ] SSL certificates configured (Let's Encrypt)

### Deployment
- [ ] `docker compose up -d`
- [ ] Port 8080 is free and accessible
- [ ] Health endpoint responds: `curl http://localhost:8080/health`
- [ ] All services reachable (Qdrant, Ollama, OpenClaw, Agent-Zero)
- [ ] BGE loads successfully (check logs)

### Post-Deployment
- [ ] External URL accessible: https://arifosmcp.arif-fazil.com/
- [ ] All 14 tools respond
- [ ] Constitutional validation active (test VOID verdict)
- [ ] Audit logging to VAULT999
- [ ] Monitoring dashboards accessible

---

## 📚 ADDITIONAL RESOURCES

### Canonical Documents
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Blueprint
- [000_THEORY/000_LAW.md](../000_THEORY/000_LAW.md) - Constitution
- [SECURITY.md](../SECURITY.md) - Defense
- [VPS_AGENT_ARCHITECT_GUIDE.md](VPS_AGENT_ARCHITECT_GUIDE.md) - This guide's predecessor
- [CRITICAL_FIX_STATUS.md](../CRITICAL_FIX_STATUS.md) - Issue history

### External Resources
- [arifOS Documentation](https://arifos.arif-fazil.com)
- [Live Server](https://arifosmcp.arif-fazil.com)
- [Truth Claim Dashboard](https://arifosmcp-truth-claim.pages.dev)

---

## 🎓 FINAL WISDOM

### The Agent's Creed

1. **Verify, Don't Assume**
   - Code existence ≠ functionality
   - Healthy container ≠ working service
   - Configured IP ≠ reachable service

2. **Test Every Fix**
   - Unit test: Does the code run?
   - Integration test: Does it connect?
   - E2E test: Does it serve users?

3. **Document Everything**
   - What you did
   - Why you did it
   - What went wrong
   - How you fixed it

4. **Respect the Constitution**
   - 13 floors are not suggestions
   - F13_SOVEREIGNTY is absolute
   - VAULT999 never forgets

5. **Ditempa Bukan Diberi**
   - Forged, not given
   - Earned, not assumed
   - Verified, not trusted

---

**Classification:** TRINITY SEALED  
**Authority:** Claude (Ω) + Codex (Ψ) Trinity  
**Date:** 2026-03-01  
**Status:** OPERATIONAL - Master Reference

*This dossier is the accumulated wisdom of the arifOS VPS deployment. Future agents: learn from our discoveries, respect the architecture, and forge onward.*

**DITEMPA BUKAN DIBERI** 🔥💎
