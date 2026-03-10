# VPS Architecture Map - arifOS

**Generated:** 2026.03.10
**Purpose:** Document current VPS state, identify chaos, propose clean architecture

---

## Disk Usage Summary

| Location | Size | Purpose | Status |
|----------|------|---------|--------|
| `/var/lib/docker` | 20G | Docker containers & volumes | Active |
| `/home/ariffazil` | 12G | User home | CHAOS |
| `/srv/arifosmcp` | 8.0G | Main codebase | Active |
| `/opt/arifos` | 5.4G | Data, git, APEX-THEORY | Mixed |
| `/srv/ariffazil` | 7.4M | Another repo | Redundant? |
| `/home/ai` | 136K | AI workspace | Clean |
| `/root` | 24K | Admin home | Has broken symlink |

**Total Used:** ~46G

---

## Root Filesystem Structure

```
/                           ← Linux root (DO NOT MODIFY)
├── bin -> usr/bin          ← System programs (symlink)
├── boot/                   ← Boot files
├── dev/                    ← Devices
├── docker/                 ← Docker config (empty)
├── etc/                    ← System configuration
├── home/                   ← User homes
├── lib -> usr/lib          ← System libraries
├── lib64 -> usr/lib64      ← 64-bit libraries
├── lost+found/             ← FS recovery
├── media/                  ← Removable media
├── mnt/                    ← Mounted drives
├── opt/                    ← Optional software
├── proc/                   ← Process info (virtual)
├── root/                   ← Root user home
├── run/                    ← Runtime data
├── sbin -> usr/sbin        ← System admin programs
├── snap/                   ← Snap packages
├── srv/                    ← Service data (HOSTED SERVICES)
├── swapfile                ← 4GB swap file
├── sys/                    ← System info (virtual)
├── tmp/                    ← Temporary (cleared on reboot)
├── usr/                    ← User programs
└── var/                    ← Variable data (logs, docker)
```

---

## `/root/` - Admin Home (24K)

```
/root/
├── .bash_history           ← Command history
├── .bashrc                 ← Shell config
├── .gitconfig              ← Git settings
├── .profile                ← Profile
├── .ssh/                   ← SSH keys (private!)
├── .config/                ← App configs
├── .local/                 ← Local installs
│   └── bin/                ← User binaries
├── .bun/                   ← Bun runtime cache
├── .npm/                   ← NPM cache
├── .cache/                 ← General cache
├── .docker/                ← Docker config
├── .openclaw/              ← OpenClaw sandboxes
│   └── sandboxes/          ← Isolated execution
└── arifOS/                 ⚠️ REDUNDANT - OLD FILES
    ├── aaa_mcp/            ← Old MCP files
    ├── core/               ← Old kernel copy
    └── arifOS -> /srv/arifOS  ⚠️ BROKEN SYMLINK (target deleted)
```

**Issues:**
- `/root/arifOS/` contains old files
- Broken symlink `arifOS -> /srv/arifOS`

---

## `/home/ariffazil/` - User Home (12G) - CHAOS ZONE

```
/home/ariffazil/
├── .bash_history           ← Command history
├── .bashrc                 ← Shell config
├── .bash_logout            ← Logout script
├── .profile                ← Profile
├── .zshrc                  ← Zsh config
├── .ssh/                   ← SSH keys (private!)
│
├── .claude/                ← Claude Code config
│   ├── agents/             ← Agent definitions
│   ├── commands/           ← Custom commands
│   ├── skills/             ← Skills
│   ├── tasks/              ← Tasks
│   ├── mcp.json            ← MCP config
│   ├── settings.json       ← Settings
│   ├── history.jsonl       ← History
│   └── plugins/            ← Plugins
│
├── .kimi/                  ← Kimi CLI config
│   ├── bin/                ← Kimi binary
│   ├── config.toml         ← Config
│   ├── kimi.json           ← Settings
│   ├── credentials/        ← Credentials
│   ├── sessions/           ← Session data
│   └── logs/               ← Logs
│
├── .gemini/                ← Gemini CLI config
│   ├── settings.json       ← Settings
│   ├── oauth_creds.json    ← OAuth (private!)
│   ├── google_accounts.json
│   └── history/            ← History
│
├── .opencode/              ← OpenCode config
├── .codex/                 ← Codex config
│
├── .config/                ← App configs
├── .local/                 ← Local installs
├── .bun/                   ← Bun runtime
├── .npm/                   ← NPM cache
├── .cache/                 ← General cache
├── .docker/                ← Docker config
│
├── agent_zero_config/      ← Agent Zero settings
├── agent_zero_work/        ← Agent Zero workspace
│   └── arifOS -> ???       ⚠️ BROKEN SYMLINK
│
├── arifosmcp/              ⚠️ REDUNDANT - OLD COPY OF CODEBASE
│   ├── .git/
│   ├── core/
│   ├── arifosmcp/
│   └── ... (duplicate of /srv/arifosmcp)
│
├── backup/                 ← Backups
├── xxx/                    ← Archive folder (chaos)
│   └── .env                ← Old env file
│
└── [Scattered .md files]   ⚠️ DOCS IN WRONG PLACE
    ├── AGENT_ZERO_READY.md
    ├── ARIFOSMCP_TOOLS_COMPLETE.md
    ├── ARIFOS_WORLD_DEPLOYMENT_SEALED.md
    ├── DEPLOYMENT_v2026.03.10-SEAL.md
    ├── MCP_TOOL_FIXES_COMPLETE.md
    └── OPENCLAW_ROOT_ACCESS_ACTIVE.md
```

**Issues:**
- Duplicate codebase at `/home/ariffazil/arifosmcp/`
- Scattered documentation files
- Broken symlink in `agent_zero_work/`
- `xxx/` archive folder with old `.env`

---

## `/home/ai/` - AI Workspace (136K) - CLEAN

```
/home/ai/
├── logs/                   ← AI agent logs
├── runtime/                ← AI runtime data
└── workspaces/             ← AI workspaces
```

**Status:** Clean, purposeful structure

---

## `/home/ubuntu/` - Default User (28K)

```
/home/ubuntu/
└── (default Ubuntu user files)
```

**Status:** Unused, can be removed if not needed

---

## `/srv/` - Service Data

```
/srv/
├── arifosmcp/              ← MAIN CODEBASE (8.0G) ✅
│   │
│   ├── core/               ← KERNEL (2.0M)
│   │   ├── governance_kernel.py   ← Runtime state
│   │   ├── judgment.py            ← Decision interface
│   │   ├── pipeline.py            ← Stage orchestration
│   │   ├── homeostasis.py         ← Metabolic regulation
│   │   ├── uncertainty_engine.py  ← Uncertainty calc
│   │   ├── telemetry.py           ← Metrics
│   │   ├── organs/                ← Trinity engines
│   │   │   ├── _0_init.py         ← Stage 000
│   │   │   ├── _1_agi.py          ← AGI Delta
│   │   │   ├── _2_asi.py          ← ASI Omega
│   │   │   └── _3_apex.py         ← APEX Psi
│   │   ├── shared/                ← Shared types
│   │   ├── theory/                ← Theory docs
│   │   │   ├── 000_LAW.md
│   │   │   └── 000_FOUNDATIONS.md
│   │   └── physics/               ← Thermodynamics
│   │
│   ├── arifosmcp/          ← MCP INTERFACE (15M)
│   │   ├── runtime/               ← Server entrypoint
│   │   │   ├── __main__.py
│   │   │   ├── server.py          ← FastMCP server
│   │   │   └── tools.py           ← Tool definitions
│   │   ├── intelligence/          ← Senses/tools
│   │   │   └── tools/
│   │   ├── transport/             ← External bridges
│   │   ├── data/                  ← Runtime data
│   │   │   └── VAULT999/          ← Immutable ledger
│   │   ├── sites/                 ← Web sites
│   │   │   └── docs/              ← Docusaurus docs
│   │   ├── packages/              ← NPM packages
│   │   └── static/                ← Static files
│   │
│   ├── docs/               ← Documentation (240K)
│   │   ├── 00_META/
│   │   ├── openclaw/
│   │   └── plans/
│   │
│   ├── spec/               ← Specs (40K)
│   │   ├── server.json
│   │   ├── mcp-clients.json
│   │   └── mcp-manifest.json
│   │
│   ├── tests/              ← Tests (920K)
│   │   ├── conftest.py
│   │   ├── constitutional/
│   │   ├── integration/
│   │   └── core/
│   │
│   ├── infrastructure/     ← Deployment (328K)
│   │   ├── config_root/           ← Agent configs
│   │   │   ├── server.json
│   │   │   ├── opencode.json
│   │   │   ├── mcp_config_qwen.json
│   │   │   ├── agentzero-integration.yml
│   │   │   └── openclaw-integration.yml
│   │   ├── deployment/
│   │   ├── grafana/
│   │   ├── prometheus/
│   │   └── nginx_config/
│   │
│   ├── scripts/            ← Utility scripts (472K)
│   ├── sessions/           ← Session data
│   ├── telemetry/          ← Telemetry
│   ├── deployment/         ← Deployment configs
│   ├── metadata/           ← Metadata
│   ├── static/             ← Static files
│   │
│   ├── .env                ← SECRETS (not in git)
│   ├── .env.example        ← Template
│   ├── .env.docker         ← Docker secrets
│   ├── .env.docker.example ← Docker template
│   ├── docker-compose.yml  ← Docker compose
│   ├── Dockerfile          ← Docker image
│   ├── pyproject.toml      ← Python project
│   ├── requirements.txt    ← Dependencies
│   ├── Makefile            ← Make commands
│   ├── AGENTS.md           ← Agent instructions
│   └── README.md           ← Project readme
│
├── ariffazil/              ← Another repo (7.4M)
│   ├── .git/
│   ├── src/                ← Web app source
│   ├── public/
│   └── package.json        ← Node.js project
│
└── backups/                ← Backups (32K)
```

---

## `/opt/` - Optional Software (5.4G)

```
/opt/
├── containerd/             ← Container runtime (12K)
│
├── arifOS/                 ⚠️ BROKEN SYMLINK
│   └── deploy.sh -> /srv/arifOS/scripts/deploy-auto.sh
│
└── arifos/                 ← Data & repos (5.4G)
    ├── APEX-THEORY/        ← Theory papers
    │   ├── 000_CONSTITUTION.md
    │   ├── 000_MANIFESTO.md
    │   ├── 000_THEORY.md
    │   ├── docs/
    │   └── site/
    │
    ├── data/               ← Data storage
    │   ├── agent_zero/     ← Agent Zero data
    │   ├── core/           ← Core data
    │   ├── grafana/        ← Grafana data
    │   ├── n8n/            ← n8n data
    │   ├── ollama/         ← Ollama models
    │   ├── openclaw/       ← OpenClaw data
    │   ├── postgres/       ← Postgres data
    │   ├── prometheus/     ← Metrics
    │   ├── qdrant/         ← Vector DB
    │   └── redis/          ← Redis data
    │
    ├── git/                ← Git repos
    │   └── AGI_ASI_bot/
    │
    ├── letsencrypt/        ← SSL certificates
    └── traefik/            ← Traefik config
```

**Issues:**
- `/opt/arifOS/` has broken symlink
- `/opt/arifos/` mixes data, git, ssl (confusing)

---

## `/var/lib/docker/` - Docker (20G)

```
/var/lib/docker/
├── containers/             ← Running containers
├── volumes/                ← Persistent volumes
│   ├── arifos_postgres_data/   ← PostgreSQL data
│   ├── arifos_redis_data/      ← Redis data
│   ├── arifos_openclaw_config/ ← OpenClaw config
│   └── openclaw_gateway/       ← OpenClaw gateway
├── image/                  ← Docker images
├── buildkit/               ← Build cache
├── network/                ← Docker networks
├── plugins/                ← Docker plugins
└── runtimes/               ← Container runtimes
```

---

## Running Docker Containers

| Container | Image | Purpose | Status |
|-----------|-------|---------|--------|
| `openclaw_gateway` | ghcr.io/openclaw/openclaw | Sandboxed execution | Healthy |
| `arifosmcp_server` | local | MCP server | RESTARTING (broken!) |
| `arifos_postgres` | postgres:16-alpine | Database | Healthy |
| `arifos_redis` | redis:7-alpine | Cache | Healthy |
| `qdrant_memory` | qdrant/qdrant | Vector memory | Running |
| `headless_browser` | ghcr.io/browserless/chromium | Browser | Healthy |
| `arifos_n8n` | n8nio/n8n | Workflows | Running |
| `traefik_router` | traefik:v3.6.9 | Reverse proxy | Running |
| `ollama_engine` | ollama/ollama | Local LLM | Running |
| `agent_zero_reasoner` | agent0ai/agent-zero | Agent Zero | Running |

---

## Environment Files (.env) Locations

| Location | Purpose | Status |
|----------|---------|--------|
| `/srv/arifosmcp/.env` | Main secrets | Active |
| `/srv/arifosmcp/.env.docker` | Docker secrets | Active |
| `/srv/arifosmcp/infrastructure/.env.*` | Templates | OK |
| `/home/ariffazil/arifosmcp/.env.*` | Duplicate templates | Redundant |
| `/home/ariffazil/xxx/.env` | Old env | Should delete |

---

## REDUNDANCY & CHAOS MAP

### Critical Issues

| # | Location | Issue | Risk | Action |
|---|----------|-------|------|--------|
| 1 | `/root/arifOS/` | Old folder with broken symlink | Confusion | **DELETE** |
| 2 | `/opt/arifOS/` | Broken symlink to deleted path | Confusion | **DELETE** |
| 3 | `/home/ariffazil/arifosmcp/` | Duplicate codebase (old) | Wasted space | **DELETE** |
| 4 | `/home/ariffazil/*.md` | Scattered docs | Disorganized | **MOVE** |
| 5 | `/home/ariffazil/xxx/` | Archive with old .env | Security risk | **DELETE** |
| 6 | `/home/ariffazil/agent_zero_work/arifOS` | Broken symlink | Confusion | **DELETE** |
| 7 | `/srv/ariffazil/` | Duplicate repo | Wasted space | **REVIEW** |
| 8 | `/opt/arifos/` | Mixed content (data, git, ssl) | Confusing | **REORGANIZE** |

### Space Recovery Potential

| Location | Size | Action |
|----------|------|--------|
| `/home/ariffazil/arifosmcp/` | ~8G | Delete (duplicate) |
| `/home/ariffazil/xxx/` | Unknown | Delete |
| `/home/ariffazil/.cache/` | Unknown | Clear |
| `/home/ariffazil/.npm/` | Unknown | Clear |
| **Potential savings** | **~8-10G** | |

---

## PROPOSED CLEAN ARCHITECTURE

### Option A: Minimal Change (Recommended)

Keep current structure, just clean up:

```
/srv/arifosmcp/              ← MAIN CODEBASE (keep)
│   └── (no changes)

/home/ariffazil/
├── .claude/                 ← Keep
├── .kimi/                   ← Keep
├── .gemini/                 ← Keep
├── .config/                 ← Keep
├── .local/                  ← Keep
├── .ssh/                    ← Keep
├── agent_zero_config/       ← Keep
├── arifosmcp/               ← DELETE (duplicate)
├── xxx/                     ← DELETE
└── *.md                     ← MOVE to /srv/arifosmcp/docs/

/root/
└── arifOS/                  ← DELETE (old, broken)

/opt/
├── arifOS/                  ← DELETE (broken symlink)
└── arifos/                  ← Keep (has data)
```

### Option B: Full Reorganization

```
/srv/arifos/                 ← ONE SOURCE OF TRUTH
├── code/                    ← arifosmcp code
│   ├── core/
│   ├── arifosmcp/
│   └── ...
├── config/                  ← All configs
│   ├── .env
│   ├── docker-compose.yml
│   └── agents/
│       ├── claude/
│       ├── kimi/
│       └── gemini/
├── data/                    ← All data
│   ├── vault999/
│   ├── postgres/
│   └── redis/
└── logs/                    ← All logs

/home/ariffazil/             ← USER HOME (configs only)
├── .claude/
├── .kimi/
├── .gemini/
└── .ssh/

/opt/arifos/                 ← DATA ONLY
├── APEX-THEORY/
└── data/
```

---

## Cleanup Commands (Run with caution)

```bash
# 1. Delete broken/old folders
rm -rf /root/arifOS/
rm -rf /opt/arifOS/

# 2. Delete duplicate codebase
rm -rf /home/ariffazil/arifosmcp/

# 3. Delete archive folder
rm -rf /home/ariffazil/xxx/

# 4. Move scattered docs
mv /home/ariffazil/*.md /srv/arifosmcp/docs/user/

# 5. Fix broken symlink
rm /home/ariffazil/agent_zero_work/arifOS

# 6. Clear caches (optional)
rm -rf /home/ariffazil/.cache/*
rm -rf /home/ariffazil/.npm/_cacache
```

---

## VPS Users

| User | Purpose | Home |
|------|---------|------|
| `root` | System admin | `/root` |
| `ariffazil` | Human operator | `/home/ariffazil` |
| `ai` | AI workspace | `/home/ai` |
| `ubuntu` | Default (unused) | `/home/ubuntu` |

---

## Network Ports

| Port | Service | Container |
|------|---------|-----------|
| 80 | HTTP | traefik_router |
| 443 | HTTPS | traefik_router |
| 5432 | PostgreSQL | arifos_postgres |
| 6379 | Redis | arifos_redis |
| 18789 | OpenClaw | openclaw_gateway |

---

## Next Steps

1. [ ] Fix `arifosmcp_server` container (currently restarting)
2. [ ] Execute cleanup commands
3. [ ] Review `/srv/ariffazil/` - keep or delete?
4. [ ] Consolidate `.env` files
5. [ ] Create backup before major changes

---

**Version:** 2026.03.10-SEAL
**Author:** arifOS Agent
**Status:** ACTIVE
