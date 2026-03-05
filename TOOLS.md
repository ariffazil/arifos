# TOOLS – Environment and Tool Rules

---

## Environment

This agent runs on:

- **Host:** `srv1325122.hstgr.cloud` (Hostinger VPS, Ubuntu)
- **Network:** `arifos_trinity` Docker bridge (`10.0.10.0/24`)
- **Compose file:** `/srv/arifOS/docker-compose.yml`
- **Workspace mount:** `/opt/arifos/data/openclaw/workspace`

### Available Infrastructure

| Tool | Access | Status |
|------|--------|--------|
| arifOS MCP Server | `https://arifosmcp.arif-fazil.com/mcp` (Streamable HTTP) | LIVE |
| Docker (via MCP or shell) | `arifosmcp_server` → docker.sock | LIVE |
| Redis 7 | `redis://redis:6379` (internal) | LIVE |
| PostgreSQL 16 | `localhost:5432` (arifos-internal) | LIVE |
| Qdrant (vector memory) | `http://qdrant_memory:6333` (internal) | LIVE |
| Ollama (LLM engine) | `http://ollama_engine:11434` (internal) | LIVE |
| n8n (workflow) | `https://flow.arifosmcp.arif-fazil.com` | LIVE |
| Prometheus | `http://arifos_prometheus:9090` (internal) | LIVE |
| Grafana | `https://monitor.arifosmcp.arif-fazil.com` | LIVE |
| Webhook CI/CD | `https://hook.arifosmcp.arif-fazil.com/hooks/deploy-arifos` | LIVE |

### 333_APPS (on-host)

| App | Path | Notes |
|-----|------|-------|
| Constitutional Visualizer | `/srv/arifOS/333_APPS/constitutional-visualizer/` | Served via arifosmcp |

---

## Tool Rules

1. **arifOS MCP is the primary interface.** Call tools via `https://arifosmcp.arif-fazil.com/mcp`. Use the 13 MCP tools as the default reasoning surface — not raw shell unless necessary.

2. **Always use the 000–999 mental model.** Before any non-trivial action:
   - Anchor (000): What is the session context?
   - Reason (111–333): What do I actually know?
   - Integrate (444–666): What are the constraints and values at play?
   - Forge (888): What is the output?
   - Seal (999): Is this worth persisting to memory?

3. **Floors before tools.** For any risky action, name which floors apply before executing:
   - Docker changes → F1, F11, F13
   - File writes → F1, F4
   - External calls → F2, F12
   - Secret handling → F11, F13

4. **888_HOLD triggers** (always pause and confirm with Arif):
   - Container restart or rebuild
   - Compose file edits
   - Mass file operations (>10 files)
   - Credential or token handling
   - Git history modification
   - Database migrations

5. **Prometheus and Grafana are read-only for the agent.** Never modify scrape configs or dashboards without 888_HOLD.

6. **Qdrant is long-term memory.** Write to it only via `recall_memory` and `seal_vault` MCP tools — not direct HTTP.

---

## Related Repos

| Repo | Role | Use when |
|------|------|----------|
| [ariffazil/arifOS](https://github.com/ariffazil/arifOS) | Kernel, MCP server, Docker infra, VAULT999 | Server-side changes, floor logic, CI/CD |
| [ariffazil/AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot) | Client configs (Claude, OpenCode, Kimi, Codex), Trinity persona, skills, hooks | Client-side MCP configs, skill authoring, hooks |
| [ariffazil/APEX-THEORY](https://github.com/ariffazil/APEX-THEORY) | Thermodynamic theory of intelligence (Δ·Ω·Ψ) | Reference for physics analogies and constitutional theory |

**Client MCP configs live in `AGI_ASI_bot`.** For any new client tool (Claude Desktop, Cursor, Codex, etc.), add its MCP config there — not here and not in arifOS.

**This workspace (`openclaw-workspace`) is OpenClaw-specific.** It governs what the OpenClaw agent running on this VPS knows about itself. It is not the source of truth for kernel logic (that's arifOS) or client configs (that's AGI_ASI_bot).
