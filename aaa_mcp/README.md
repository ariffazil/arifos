# aaa_mcp — Constitutional AI Governance Layer

**Version:** v55.5-HARDENED  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given

The AAA MCP Server provides a **Model Context Protocol** interface to the arifOS Constitutional AI system. It exposes 9 canonical tools organized as a Trinity pipeline with 13 Constitutional Floors enforcement.

---

## 🏗️ Architecture

```
aaa_mcp/
├── server.py                 # FastMCP server with 9 canonical tools
├── __init__.py               # Package exports
├── __main__.py               # Entry point: python -m aaa_mcp
├── bridge.py                 # Engine routing layer
├── mcp_config.py             # External server registry
├── mcp_integration.py        # Constitutional governance wrapper
│
├── core/                     # Core framework
│   ├── constitutional_decorator.py   # Floor enforcement decorators
│   ├── engine_adapters.py           # AGI/ASI/APEX engine adapters
│   └── mode_selector.py             # Transport mode selection
│
├── sessions/                 # Session management
│   ├── session_ledger.py            # Merkle-chained ledger (F1 Amanah)
│   └── session_dependency.py         # Session store for persistence
│
├── services/                 # Services layer
│   ├── constitutional_metrics.py    # Verdict & stage metrics
│   └── redis_client.py              # MindVault Redis persistence
│
├── tools/                    # Tool implementations
│   ├── trinity_validator.py         # Request validation (F11, F12)
│   └── reality_grounding.py         # External fact-checking (F7)
│
├── infrastructure/           # Operational infrastructure
│   └── rate_limiter.py              # Token bucket rate limiting (F12)
│
├── transports/               # Transport layer
│   └── sse.py                       # SSE transport
│
├── external_gateways/        # External API clients
│   └── brave_client.py              # Brave Search integration
│
└── config/                   # Configuration management
```

---

## 🔧 The 9 Canonical Tools

| Tool | Engine | Floors | Description |
|:-----|:------:|:------:|:------------|
| `init_gate` | 🚪 INIT | F11, F12 | Session initialization & injection defense |
| `agi_sense` | Δ Mind | F2, F4 | Intent parsing & lane classification |
| `agi_think` | Δ Mind | F2, F4, F7 | Hypothesis generation |
| `agi_reason` | Δ Mind | F2, F4, F7 | Deep logical reasoning |
| `asi_empathize` | Ω Heart | F5, F6 | Stakeholder impact analysis |
| `asi_align` | Ω Heart | F5, F6, F9 | Ethics & Anti-Hantu check |
| `apex_verdict` | Ψ Soul | F3, F5, F8 | Final constitutional judgment |
| `reality_search` | Δ Ground | F2, F7 | External fact-checking |
| `vault_seal` | 🔒 SEAL | F1, F3 | Immutable ledger recording |

---

## 🛡️ Constitutional Floors (v55.5)

| Floor | Name | Type | Enforcement |
|:-----:|:-----|:----:|:------------|
| F1 | Amanah | HARD | Reversibility/Auditability |
| F2 | Truth | HARD | Factual fidelity ≥ 0.99 |
| F3 | Consensus | Derived | Tri-Witness ≥ 0.95 |
| F4 | Clarity | SOFT | Entropy reduction (ΔS ≤ 0) |
| F5 | Peace² | SOFT | Safety margins ≥ 1.0 |
| F6 | Empathy | HARD | Weakest stakeholder check |
| F7 | Humility | Derived | Uncertainty band [0.03, 0.15] |
| F8 | Genius | Derived | G = A×P×X×E² ≥ 0.80 |
| F9 | Anti-Hantu | SOFT | No consciousness claims |
| F10 | Ontology | HARD | Tool, not Being |
| F11 | Authority | HARD | Sovereign command |
| F12 | Defense | HARD | Injection scan |
| F13 | Curiosity | SOFT | Multi-hypothesis paths |

---

## 🚀 Usage

### Running via FastMCP (SSE)

```bash
cd arifOS
python -m aaa_mcp
# Or directly:
python aaa_mcp/server.py
```

Server runs at `http://localhost:6274` with SSE transport.

### Health Check

```
GET /health
{
  "status": "ok",
  "service": "arifOS",
  "version": "v55.5-HARDENED",
  "tools": 9,
  "constitution": "13 Floors"
}
```

### Tool Invocation (MCP Protocol)

```json
{
  "method": "tools/call",
  "params": {
    "name": "init_gate",
    "arguments": {
      "query": "What is 2+2?",
      "session_id": "sess_001"
    }
  }
}
```

---

## 📦 Dependencies

- `fastmcp` — MCP server framework
- `redis` — Session persistence (optional)
- `starlette` — HTTP framework

---

## 🔗 Related

- **codebase/** — Core engine implementations
- **000_THEORY/** — Constitutional law documents
- **333_APPS/** — Application layer

---

*DITEMPA BUKAN DIBERI* 💎🔥🧠