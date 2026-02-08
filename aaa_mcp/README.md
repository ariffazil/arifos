# aaa_mcp — Constitutional AI Governance Layer

**Version:** v55.5-HARDENED  
**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given

The AAA MCP Server provides a **Model Context Protocol** interface to the arifOS Constitutional AI system. It exposes 10 canonical tools organized as a Trinity pipeline with 13 Constitutional Floors enforcement.
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

### Running the Server

**1. Local Agent Mode (STDIO)**
Default mode for Claude Desktop, Claude Code, and local clients.

```bash
cd arifOS
python -m aaa_mcp
```

**2. Remote Server Mode (SSE)**
Run via Server-Sent Events for remote connections (Railway, Network).

```bash
python -m aaa_mcp sse
```

SSE endpoint: `http://0.0.0.0:8080/sse` (default port).

**3. Remote Server Mode (HTTP / Streamable HTTP)**
Run via HTTP MCP transport (path: `/mcp`) for clients that support streamable HTTP.

```bash
python -m aaa_mcp http
```

HTTP endpoint: `http://0.0.0.0:8080/mcp` (default port).
You can override the port using the `PORT` environment variable (e.g., `PORT=8000 python -m aaa_mcp http`).

### Health Check & Inspection

Since FastMCP v1.0, health checks are performed via the MCP protocol itself:

1. **List Tools**: `tools/list` returns all 9 tools if healthy.
2. **Ping**: Basic connection check via protocol.

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
