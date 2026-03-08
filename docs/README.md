# arifosmcp — arifOS Runtime (Body)

**Part of the [arifOS Trinity](https://github.com/ariffazil/arifOS)**

This repository contains the **executable runtime** for arifOS: the Python kernel, MCP server, and tool implementations with 13-Floor thermodynamic governance.

## 🔺 Trinity Architecture

| Role | Repo | Description |
|------|------|-------------|
| 🧠 **Mind** | [arifOS](https://github.com/ariffazil/arifOS) | Constitutional theory, agent repository, governance patterns |
| 🦾 **Body** | [arifosmcp](https://github.com/ariffazil/arifosmcp) | Python kernel, MCP runtime, tools (you are here) |
| ❤️ **Heart** | [ariffazil](https://github.com/ariffazil/ariffazil) | Human narrative & coordination |

📖 [Full Trinity Spec](https://github.com/ariffazil/arifOS/blob/main/KERNEL/TRINITY_ARCHITECTURE.md)

---

## 🚀 Quick Start

### Installation

```bash
pip install arifos
```

### Run MCP Server (FastMCP)

```bash
# Using profile configs
fastmcp run dev.fastmcp.json    # Development: stdio transport (Claude Desktop, Cline)
fastmcp run prod.fastmcp.json   # Production: HTTP transport at /mcp/

# Or directly with Python
python -m arifosmcp.runtime
```

### Available Transports
- **stdio** — Local MCP clients (Claude Desktop, Cline, etc.)
- **SSE** — Server-sent events
- **HTTP** — Streamable HTTP (production deployments)

---

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/ariffazil/arifosmcp.git
cd arifosmcp

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

### Run Tests

```bash
pytest tests/
```

### Local Development Server

```bash
# Run with uvicorn (HTTP mode)
uvicorn arifosmcp.runtime.server:app --reload

# Or with fastmcp
fastmcp dev
```

---

## 📦 Package Structure

```
arifosmcp/
├── core/                    # Constitutional kernel
├── arifosmcp.runtime/          # MCP server implementation
│   ├── server.py            # Main FastMCP server
│   ├── governance.py        # 13-Floor governance engine
│   ├── contracts.py         # Constitutional contracts
│   ├── rest_routes.py       # REST API routes
│   └── fastmcp_ext/         # FastMCP extensions
├── tests/                   # Test suite
├── fastmcp.json             # FastMCP base configuration (HTTP/production default)
├── dev.fastmcp.json         # Dev profile — stdio transport, DEBUG logging
├── prod.fastmcp.json        # Prod profile — HTTP transport at /mcp/
├── server.json              # MCP registry manifest
└── pyproject.toml           # Python package config
```

---

## 🔧 Configuration

### FastMCP Profiles
Three FastMCP configuration files are provided:
- **`fastmcp.json`** — Base/default configuration (HTTP transport). See [gofastmcp.com](https://gofastmcp.com).
- **`dev.fastmcp.json`** — Development profile: stdio transport, DEBUG log level (for Claude Desktop, Cline).
- **`prod.fastmcp.json`** — Production profile: HTTP transport at `/mcp/`.

### Environment Variables
- `REDIS_URL` — Redis connection (default: `redis://localhost:6379`)
- `ANTHROPIC_API_KEY` — Claude API key (optional)
- `LOG_LEVEL` — Logging level (default: `INFO`)

---

## 📖 Documentation

All governance documentation lives in the [arifOS Mind repo](https://github.com/ariffazil/arifOS):

- **[Constitutional Law](https://github.com/ariffazil/arifOS/tree/main/KERNEL)** — 13-Floor governance, Trinity architecture
- **[Agent Patterns](https://github.com/ariffazil/arifOS/tree/main/AGENTS)** — Skills, workflows, prompts
- **[Deployment Guides](https://github.com/ariffazil/arifOS/tree/main/OPERATION)** — Docker, VPS, Kubernetes configs

---

## 🔌 Integration

### Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "arifos": {
      "command": "fastmcp",
      "args": ["run", "/path/to/arifosmcp/dev.fastmcp.json"]
    }
  }
}
```

### Cline (VS Code)

Add to Cline MCP settings:

```json
{
  "arifos": {
    "command": "python",
    "args": ["-m", "arifosmcp.runtime"]
  }
}
```

---

## 🧪 13-Floor Governance

This server implements **thermodynamic AI governance** with 13 constitutional floors:

- **F1-F3:** Truth, Entropy, Peace² (thermodynamic foundation)
- **F4-F6:** SABAR, Ω₀, Amanah (human sovereignty)
- **F7-F9:** Witness, ψₗₑ, MARUAH (governance enforcement)
- **F10-F13:** Extended governance (future expansion)

All tool executions are validated against these floors before execution.

---

## 📦 PyPI Package

Published as `arifos`:

```bash
pip install arifos
```

- **Version:** 2026.03.07
- **License:** AGPL-3.0
- **Python:** >=3.12

---

## 🤝 Contributing

This is the **runtime implementation** of arifOS constitutional law.

**For governance proposals:** Open issues in [arifOS Mind repo](https://github.com/ariffazil/arifOS/issues)  
**For bug fixes:** Open PRs in this repo  
**For new tools:** Document in [arifOS/AGENTS/skills/](https://github.com/ariffazil/arifOS/tree/main/AGENTS/skills) first

---

## 📜 License

AGPL-3.0 — See [LICENSE](./LICENSE)

---

## 🔗 Links

- **Documentation:** [arifOS Mind](https://github.com/ariffazil/arifOS)
- **PyPI:** [pypi.org/project/arifos](https://pypi.org/project/arifos/)
- **Website:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com)
- **Human:** [arif-fazil.com](https://arif-fazil.com)

---

**Trinity Status:** SEAL  
**Authority:** Arif Fazil (H-SOURCE)
