# aaa_mcp — Constitutional AI Governance Server v60.0-FORGE

**Version:** v60.0-FORGE (RUKUN AGI)  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given  
**Status:** PRODUCTION READY

The AAA MCP Server provides a **Model Context Protocol** interface to the arifOS Constitutional AI system. It exposes 13 canonical tools organized as a 5-Organ Trinity pipeline with 13 Constitutional Floors enforcement.

---

## Quick Start

```bash
# Install
pip install -e .

# Run (stdio mode for local agents)
python -m aaa_mcp

# Run (SSE mode for network)
python -m aaa_mcp sse

# Validate deployment
python scripts/deploy_mcp.py --mode validate
```

---

## Architecture

### 5-Organ Constitutional Kernel

```
┌────────────────────────────────────────────────────────────┐
│                    AAA MCP Server                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   init_gate         → Airlock (F11/F12)                    │
│   agi_sense         → Mind Stage 111 (F4/F7)               │
│   agi_think         → Mind Stage 222 (F2/F4)               │
│   agi_reason        → Mind Stage 333 (F2/F4/F7/F8)         │
│   asi_empathize     → Heart Stage 555 (F5/F6)              │
│   asi_align         → Heart Stage 666 (F5/F6/F9)           │
│   apex_verdict      → Soul Stages 444-888 (F3/F8/F9/F10)   │
│   vault_seal        → Memory Stage 999 (F1/F3/F13)         │
│                                                            │
│   forge_pipeline    → Full 000-999 pipeline                │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 13 Constitutional Floors

| Floor | Name | Type | Threshold |
|:-----:|:-----|:----:|:----------|
| F1 | **Amanah** | HARD | Reversible actions |
| F2 | **Truth** | HARD | τ ≥ 0.99 |
| F3 | **Consensus** | DERIVED | W₃ ≥ 0.95 |
| F4 | **Clarity** | SOFT | ΔS ≤ 0 |
| F5 | **Peace²** | SOFT | ≥ 1.0 |
| F6 | **Empathy** | HARD | κᵣ ≥ 0.70 |
| F7 | **Humility** | HARD | Ω₀ ∈ [0.03,0.05] |
| F8 | **Genius** | DERIVED | G ≥ 0.80 |
| F9 | **Anti-Hantu** | SOFT | C_dark < 0.30 |
| F10 | **Ontology** | HARD | Grounded |
| F11 | **Authority** | HARD | Valid auth |
| F12 | **Defense** | HARD | Clean scan |
| F13 | **Sovereign** | HARD | Human override |

---

## Usage

### Running the Server

**1. stdio Mode (Default)**

For Claude Desktop, Kimi, and local agents:

```bash
python -m aaa_mcp
```

**2. SSE Mode (Network)**

For Railway, remote connections:

```bash
python -m aaa_mcp sse
# Endpoint: http://0.0.0.0:8080/sse
```

**3. HTTP Mode (Streamable HTTP)**

For MCP 2024 spec clients:

```bash
python -m aaa_mcp http
# Endpoint: http://0.0.0.0:8080/mcp
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port |
| `HOST` | `0.0.0.0` | Bind address |
| `AAA_MCP_TRANSPORT` | `sse` | Transport mode |
| `LOG_LEVEL` | `info` | Logging level |
| `BRAVE_API_KEY` | — | Web search API |
| `DATABASE_URL` | — | PostgreSQL URL |

### Health Check

```bash
curl http://localhost:8080/health

# Response:
{
  "status": "healthy",
  "version": "60.0-FORGE",
  "service": "arifOS MCP Server"
}
```

### Metrics

```bash
curl http://localhost:8080/metrics     # Prometheus
curl http://localhost:8080/stats       # JSON stats
```

---

## Client Configuration

### Kimi

**File:** `.kimi/mcp.json`

```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS",
      "env": {
        "ARIFOS_CONSTITUTIONAL_MODE": "AAA"
      },
      "alwaysAllow": [
        "init_gate", "forge_pipeline",
        "agi_sense", "agi_reason",
        "asi_empathize", "apex_verdict", "vault_seal"
      ]
    }
  }
}
```

### Claude Desktop

**File:** `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "arifos-local": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS"
    },
    "arifos-cloud": {
      "transport": "sse",
      "url": "https://mcp.yourdomain.com/sse"
    }
  }
}
```

### Cursor

**File:** `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"],
      "cwd": "/path/to/arifOS"
    }
  }
}
```

---

## Deployment

### Railway (Cloud)

```bash
# Install CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway up

# Set environment
railway variables set PORT=8080
railway variables set AAA_MCP_TRANSPORT=sse
```

### Docker

```bash
# Build
docker build -t arifos-mcp:v60 .

# Run
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e AAA_MCP_TRANSPORT=sse \
  arifos-mcp:v60
```

### Validation

```bash
python scripts/deploy_mcp.py --mode validate
```

---

## Tool Reference

### Core Pipeline

**`forge_pipeline(query, actor_id, auth_token, require_sovereign_for_high_stakes)`**

The unified 000-999 constitutional pipeline.

- **Input:** User query
- **Output:** Complete constitutional assessment
- **Stages:** 000_INIT → 111-333_MIND → 555-666_HEART → 444-888_SOUL → 999_VAULT

### Individual Tools

| Tool | Purpose | Floors |
|------|---------|--------|
| `init_gate` | Session initialization | F11, F12 |
| `agi_sense` | Parse intent | F4, F7 |
| `agi_think` | Generate hypotheses | F2, F4 |
| `agi_reason` | Logical reasoning | F2, F4, F7 |
| `asi_empathize` | Stakeholder analysis | F5, F6 |
| `asi_align` | Ethics/policy check | F5, F6, F9 |
| `apex_verdict` | Final judgment | F3, F8, F9, F10 |
| `vault_seal` | Immutable ledger | F1, F3 |
| `reality_search` | Web grounding | F2, F10 |

---

## Development

### Testing

```bash
# Run all tests
pytest core/tests/ -v

# Run specific module
pytest core/tests/test_pipeline.py -v
```

### Architecture

```
aaa_mcp/
├── server.py              # 13 MCP tools
├── core/
│   ├── engine_adapters.py # Bridge to core organs
│   ├── constitutional_decorator.py  # Floor enforcement
│   └── mode_selector.py   # Transport selection
├── infrastructure/
│   ├── monitoring.py      # Metrics & health
│   └── rate_limiter.py    # Rate limiting
└── sessions/
    └── session_ledger.py  # Session persistence
```

### Core Integration

```python
# Direct core usage
from core.pipeline import forge

result = await forge(
    query="What is the capital of Malaysia?",
    actor_id="user_123"
)

print(result.verdict)        # SEAL, VOID, PARTIAL, etc.
print(result.W_3)            # Tri-Witness score
print(result.processing_time_ms)  # Latency
```

---

## Documentation

- **Full Guide:** `docs/MCP_DEPLOYMENT_GUIDE_V60.md`
- **Architecture:** `docs/V60_ARCHITECTURE.md`
- **Deployment:** `docs/RAILWAY_DEPLOYMENT.md`
- **API Reference:** `docs/API_REFERENCE.md`

---

## Support

- **Repository:** https://github.com/ariffazil/arifOS
- **Documentation:** https://arifos.arif-fazil.com
- **Health:** https://aaamcp.arif-fazil.com/health
- **Issues:** https://github.com/ariffazil/arifOS/issues

---

*DITEMPA BUKAN DIBERI* 💎🔥🧠
