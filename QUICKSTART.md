# arifOS Quickstart

Get the Constitutional AI Kernel running in under 5 minutes.

---

## Option A — Docker Compose (Recommended)

One command. Includes PostgreSQL, Redis, and the arifOS MCP server.

```bash
curl -fsSL https://raw.githubusercontent.com/ariffazil/arifOS/main/docker-compose.quickstart.yml \
  | docker compose -f - up -d
```

Or clone and run:

```bash
git clone https://github.com/ariffazil/arifOS.git && cd arifOS
docker compose -f docker-compose.quickstart.yml up -d
```

Verify it's up:

```bash
curl http://localhost:8080/health
# → {"status": "healthy", "tools": 14, ...}
```

**MCP endpoint:** `http://localhost:8080/mcp`

---

## Option B — pip + stdio (Claude Desktop / Cursor)

```bash
pip install arifos

# Generate a local governance secret
export ARIFOS_GOVERNANCE_SECRET=$(openssl rand -hex 32)

# Add to Claude Desktop config (~/.config/claude/claude_desktop_config.json)
# See "Connect to Claude Desktop" below
python -m arifos_aaa_mcp stdio
```

---

## Connect to Claude Desktop

Add this to `~/.config/claude/claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`):

```json
{
  "mcpServers": {
    "arifOS": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"],
      "env": {
        "ARIFOS_GOVERNANCE_SECRET": "your-dev-secret-here"
      }
    }
  }
}
```

Restart Claude Desktop. You should see 14 arifOS tools in the tool list.

---

## Connect to Cursor

`Cursor Settings → Features → MCP → Add Server`

- **Type:** `command`
- **Name:** `arifOS`
- **Command:** `python -m arifos_aaa_mcp stdio`

---

## Try It: See the Constitutional Kernel Block a Destructive Command

Once connected via Claude Desktop or Cursor, ask your AI:

> *"Use eureka_forge to run `rm -rf /tmp/test` without confirming."*

Expected response — the kernel issues **888_HOLD**:

```json
{
  "verdict": "888_HOLD",
  "stage": "777_FORGE",
  "floor": "F1_AMANAH",
  "message": "Irreversible command requires confirm_dangerous=true and human sign-off.",
  "next_actions": ["Set confirm_dangerous=true", "Provide agent_id and purpose"]
}
```

The AI cannot bypass this. F1 (Amanah/Reversibility) is a hard wall — the `rm -rf` never runs.

---

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `ARIFOS_GOVERNANCE_SECRET` | Recommended | auto-generated | Signs `governance_token` (HMAC-SHA256) |
| `DATABASE_URL` | Optional | SQLite fallback | PostgreSQL for VAULT999 ledger |
| `JINA_API_KEY` | Optional | — | Clean Markdown extraction (search_reality, fetch_content) |
| `PERPLEXITY_API_KEY` | Optional | — | Web search fallback |
| `BRAVE_API_KEY` | Optional | — | Web search fallback |
| `ARIFOS_ML_FLOORS` | Optional | `0` | Enable SBERT semantic scoring for F5/F6/F9 |

---

## What You Get

14 governed MCP tools across the `000 → 999` metabolic chain:

| Tool | What it does |
|------|-------------|
| `anchor_session` | Start a session, scan for prompt injection |
| `reason_mind` | Structured reasoning with F2 truth grounding |
| `recall_memory` | Vector memory search (Qdrant) |
| `simulate_heart` | Stakeholder harm analysis |
| `critique_thought` | Self-adversarial critique |
| `eureka_forge` | Execute shell commands — risk-classified, 888_HOLD gated |
| `apex_judge` | Final constitutional verdict + governance_token |
| `seal_vault` | Commit to VAULT999 immutable ledger |
| `search_reality` | Web search via Jina → Perplexity → Brave |
| `fetch_content` | URL → clean Markdown via Jina Reader |
| `inspect_file` | Filesystem read with F1 audit |
| `audit_rules` | Live F1-F13 floor status |
| `check_vital` | CPU/RAM/container health |
| `visualize_governance` | Real-time governance dashboard |

---

## Next Steps

- **Full deploy guide:** [`docs/60_REFERENCE/DEPLOYMENT.md`](docs/60_REFERENCE/DEPLOYMENT.md)
- **All 14 tools documented:** [`docs/60_REFERENCE/TOOLS_CANONICAL_13.md`](docs/60_REFERENCE/TOOLS_CANONICAL_13.md)
- **Constitutional floors:** [`000_THEORY/000_LAW.md`](000_THEORY/000_LAW.md)
- **Architecture deep-dive:** [`docs/60_REFERENCE/ARCHITECTURE.md`](docs/60_REFERENCE/ARCHITECTURE.md)
- **VPS deployment (production):** [`DEPLOYMENT_STATUS.md`](DEPLOYMENT_STATUS.md)
