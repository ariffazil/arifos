# arifOS VPS — Capabilities Map

**Last verified:** 2026-03-14 by Codex (GPT-5)  
**Reference:** [VPS_ARCHITECTURE.md](/srv/arifosmcp/infrastructure/VPS_ARCHITECTURE.md)

> This file maps what the VPS can actually do right now, and which tools are truly reachable by agents. It distinguishes installed, mounted, and working.

---

## 1. Core Agent Stack

| Component | State | Reachability | Notes |
|-----------|-------|--------------|-------|
| `arifosmcp_server` | healthy | public + internal | canonical MCP brain |
| OpenClaw | healthy | internal + Telegram path | main executive agent gateway |
| Agent Zero | running | internal only in practice | public usage unproven |
| n8n | running | internal | workflow automation |
| Ollama | healthy | internal | local model runtime |
| Qdrant | up | internal | vector memory |
| Browserless | healthy | internal | browser automation |
| Prometheus | up | internal | metrics |
| Grafana | healthy | routed | dashboards |

---

## 2. Public MCP Capabilities

Live `arifosmcp` reports:
- status: `healthy`
- version: `2026.03.12-FORGED`
- transport: `streamable-http`
- tools loaded: `9`
- authentication: `none`

### Public MCP Tools

| Tool | Purpose |
|------|---------|
| `arifOS_kernel` | full constitutional orchestrator |
| `search_reality` | web grounding |
| `ingest_evidence` | fetch / extract evidence |
| `session_memory` | memory read/write/forget |
| `audit_rules` | inspect governance floors |
| `check_vital` | live health and capability snapshot |
| `init_anchor_state` | onboarding + continuity anchor |
| `open_apex_dashboard` | open dashboard asset |
| `verify_vault_ledger` | Merkle-chain vault verification |

### Capability Map Exposed by MCP

| Capability | Live state |
|------------|------------|
| governed continuity | enabled |
| vault persistence | enabled |
| vector memory | enabled |
| external grounding | enabled |
| model provider access | enabled |
| local model runtime | enabled |
| auto deploy | enabled |

### Provider Classes Reported by MCP

| Provider | State |
|----------|-------|
| OpenAI | configured |
| Anthropic | configured |
| Google | configured |
| OpenRouter | configured |
| Venice | configured |
| Ollama local | configured |
| Brave | configured |
| Jina | configured |
| Perplexity | configured |
| Firecrawl | configured |
| Browserless | configured |

Important boundary:
- the MCP capability map is redacted by design
- it proves configuration classes, not raw secret values

---

## 3. Host Toolchain Inventory

### 3.1 Host CLIs Present

| Tool | Version | Host status |
|------|---------|-------------|
| `claude` | `2.1.74` | present |
| `codex` | `0.114.0` | present |
| `gemini` | `0.33.0` | present |
| `kimi` | `1.18.0` | present |
| `opencode` | `1.2.24` | present |
| `docker` | `29.3.0` | present |
| `node` | `v20.19.4` | present |
| `npm` | `9.2.0` | present |
| `python3` | `3.13.7` | present |
| `uv` | `0.10.9` | present |

### 3.2 Host CLIs Missing as Global Commands

These are not normal host-global commands from `/root` right now:
- `gh`
- `mcporter`
- `oracle`
- `oracle-mcp`
- `xurl`
- `bun`

That does not stop OpenClaw from using some of them, because OpenClaw has mounted wrappers and custom paths.

---

## 4. OpenClaw Access Matrix

### 4.1 OpenClaw Runtime Facts

| Item | State |
|------|-------|
| health endpoint | `ok` |
| live agent model | `kimi/kimi-k2-5` |
| MCP bridge | healthy |
| `mcporter` inventory | `arifos` healthy with `9 tools`; `context7` healthy with `2 tools`; `codegraphcontext` offline |
| Telegram provider | starts for `@arifOS_bot` |

### 4.2 OpenClaw Reachability to Infrastructure

| Resource | Reachable from OpenClaw | Notes |
|----------|-------------------------|-------|
| Docker socket | yes | can inspect and control containers |
| `/mnt/arifos` | yes | repo mounted |
| `/mnt/apex` | yes | APEX repo mounted |
| arifosmcp MCP | yes | verified via `arifos health` |
| Browserless | yes | internal service |
| Ollama | yes | previously proven by direct generation |
| Redis / Postgres / Qdrant network path | yes | available on Docker network |
| Git on mounted repo | yes | safe-directory fix applied |

### 4.3 OpenClaw CLI Availability

| Tool inside OpenClaw | Path exists | Smoke test | Status |
|----------------------|-------------|------------|--------|
| `arifos` | yes | passed | usable |
| `mcporter` | yes | passed | usable |
| `docker` | yes | passed | usable |
| `claude` | yes | passed | usable |
| `codex` | yes | passed | usable |
| `gemini` | yes | passed | usable |
| `gh` | yes | passed | usable |
| `jq` | yes | passed | usable |
| `rg` | yes | passed | usable |
| `oracle` | yes | passed | usable |
| `xurl` | yes | passed | usable |
| `kimi` | yes | passed | usable natively inside the forged OpenClaw image |
| `opencode` | yes | passed | usable natively inside the forged OpenClaw image |
| `aider` | no | removed | no longer exposed to OpenClaw |
| `oracle-mcp` | yes | not smoke-tested separately | assumed available if wrapper remains intact |

### 4.4 Exact Broken States

`kimi` inside OpenClaw:
- fixed by baking `kimi-cli 1.18.0` into the custom `arifos/openclaw-forged:2026.03.14` image
- avoids host/container runtime mismatch and removes Docker indirection

`opencode` inside OpenClaw:
- fixed by baking `opencode-linux-x64 1.2.24` into the custom `arifos/openclaw-forged:2026.03.14` image
- the exposed `opencode` command now resolves directly to the native Linux binary, not the hanging JS launcher

`aider` inside OpenClaw:
- intentionally removed from the exposed tool surface

Implication:
- OpenClaw can now use the core preferred CLI set without the previous false-positive/broken entries

---

## 5. Model and Memory Capabilities

### 5.1 arifosmcp Memory / Intelligence

| Capability | State |
|------------|-------|
| VAULT persistence | configured |
| session cache | configured |
| vector memory | configured |
| Merkle ledger | configured |
| local runtime | configured |

Discovery reports:
- `vault999 = postgresql + redis + merkle`
- `vector_memory = qdrant + bge-m3-1024dim`

### 5.2 OpenClaw Memory State

| Item | State |
|------|-------|
| memory backend | `builtin` |
| semantic memory search | not proven from current JSON parse |
| embeddings expectation | previously configured around Ollama embedding models |
| authoritative live runtime signal | OpenClaw gateway log confirms current model, not a full memory dump |

Operationally:
- arifosmcp has proven vector memory capability
- OpenClaw has working MCP access into arifosmcp memory tools
- OpenClaw-native memory config should be treated as partially verified unless re-inspected in depth

---

## 6. Office / Utility Tooling

The old dossier overstated several utilities without a fresh live proof. Current truth:

### Proven available now
- Docker control
- Node / npm
- Python / uv
- browser automation via Browserless
- Git on host and in OpenClaw-mounted repo
- MCP orchestration via `arifos` and `mcporter`

### Not freshly proven in this pass
- Marp CLI
- Mermaid CLI
- ImageMagick
- Syncthing
- Tailscale
- Caddy
- office-generation Python packages

Those may still exist on the VPS, but they were not revalidated in this live sweep and should not be claimed as hardened capability until checked again.

---

## 7. Agent Reachability Summary

| Agent | Can reach MCP | Can reach Docker | Can reach browser | Can use host CLIs | Confidence |
|-------|---------------|------------------|-------------------|------------------|------------|
| arifosmcp | native | indirect ops path | via provider stack | not a shell agent | high |
| OpenClaw | yes | yes | yes | partial, mixed quality | high |
| Agent Zero | unknown from this pass | likely internal | unknown | unknown | low |
| n8n | not verified | not verified | not verified | not verified | low |

Interpretation:
- OpenClaw is currently your strongest agent shell
- arifosmcp is your strongest governed MCP brain
- Agent Zero exists, but is not yet a proven production-grade reachable agent in this topology

---

## 8. Hard Limits and Risks

| Item | Severity | Why it matters |
|------|----------|----------------|
| Git divergence | High | docs and code may describe different realities |
| OpenClaw container-name drift | Medium | automation may target stale container names |
| custom-image maintenance | Medium | native CLI reliability is higher, but the forged image now needs to be maintained intentionally |
| Agent Zero route uncertainty | Medium | running is not the same as reachable or used |
| MCP auth disabled | Medium | public endpoint is still unauthenticated |
| Ollama memory pressure | Medium | local runtime is operating very close to its memory cap |

---

## 9. Bottom Line

What is truly hardened right now:
- `arifosmcp` public MCP brain
- OpenClaw as the main executive agent
- Docker, Browserless, and internal service reachability
- core provider secret injection into OpenClaw

What is not yet fully hardened:
- keeping the forged OpenClaw image versioned and rebuilt when upstream OpenClaw or native CLI pins change
- Agent Zero as a proven externally usable agent
- any claim that the VPS exactly matches GitHub `main`

