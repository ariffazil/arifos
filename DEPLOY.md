# DEPLOY.md — arifOS MCP Production Deployment Guide

> **For Claude Code agent. Full context, issues, and unresolved problems.**

---

## MISSION

Harden the arifOS MCP implementation to match canonical architecture (K_FORGE, K_FOUNDATIONS), create a 27-zone philosophy atlas with real human quotes mapped to S×G×Ω coordinates, and ensure the Docker container actually runs the new code.

---

## WHAT WAS ACCOMPLISHED

### 1. Philosophy Atlas (`data/philosophy_atlas.json`)
- **27-zone orthogonal philosophy cube** with orthogonal contrast pairs (S×H×G axes)
- **81 real human quotes** from Marcus Aurelius, Lao Tzu, Nietzsche, Kafka, Shakespeare, Rumi, Sun Tzu, Epictetus, Heraclitus, etc.
- Quotes mapped to 3D S×G×Ω coordinate space:
  - **S** (Survival): +1 (entropy-reducing/clarifying) or -1 (entropy-increasing/confusing)
  - **G** (Genius): 0/0.5/1 based on g_score
  - **Ω** (Humility): High/Medium/Low from F7 band

### 2. Philosophy Selection (`arifosmcp/runtime/philosophy.py`)
- 3D Euclidean distance-based quote selection from atlas
- INIT/SEAL sessions → "DITEMPA, BUKAN DIBERI." motto + Z01 (Humble Sovereign)
- Normal sessions → 3D coordinate-based nearest-neighbor selection

### 3. Wisdom Integration (`arifosmcp/intelligence/tools/wisdom_quotes.py`)
- Atlas-based quote selection wired to delta_s and omega_score

### 4. Constitutional Hardening
- `init_anchor_hardened.py` — constitutional_context AI prompt, telos_manifold, godel_lock
- `_1_agi.py` — constitutional_context prepended to all 3 Ollama phases
- `tools_hardened_dispatch.py` — pass constitutional_context through pipeline
- `tools_hardened_v2.py` — Explorer/Conservator dual-process, Goodhart resistance, Landauer checks, forge_pipeline
- `_3_apex.py` Stage 777 — Real pressure tests (stability, adversarial, scarcity, telos_drift)
- `tools_internal.py` — delta_s, omega_score wired to philosophy selection
- `thermo_estimator.py` — coherence_score, shannon_entropy, landauer_limit functions

### 5. Canonical Docs
- `000/ROOT/K_FORGE.md` — Pre-deployment evolutionary architecture
- `000/ROOT/K_FOUNDATIONS.md` — 99-domain rigorous math foundations

### 6. Docker Rebuild
- Image rebuilt: `docker build --no-cache -t arifos/arifosmcp:latest -f Dockerfile .`
- Container recreated: `docker compose up -d --force-recreate arifosmcp`

---

## CRITICAL UNRESOLVED ISSUE: Python Path Conflict

### The Problem
Despite rebuilding the Docker image, the running container **still imports the OLD pip-installed site-packages version** instead of the new `/usr/src/app/` code.

**Evidence:**
```
# Running container:
Module file: /usr/local/lib/python3.12/site-packages/arifosmcp/runtime/init_anchor_hardened.py

# Fresh image:
Module file: /usr/src/app/arifosmcp/runtime/init_anchor_hardened.py
```

When we run `docker run --rm arifos/arifosmcp:latest python3 -c "import ..."` → correct path.

When we run `docker compose exec arifosmcp python3 -c "import ..."` → OLD site-packages path.

### Root Cause
The `pip install .` in the Dockerfile (line 32) installs the old package to `/usr/local/lib/python3.12/site-packages/arifosmcp/`. The volume mounts in `docker-compose.yml` try to mount `/srv/arifosmcp/arifosmcp:/usr/src/app/arifosmcp:ro` but this path is broken (symlink chain creates non-existent `arifosmcp/arifosmcp`).

### Symlink Chain
```
/srv/arifosmcp → /srv/arifOS/arifosmcp (symlink)
/srv/arifOS/arifosmcp/arifosmcp/runtime/ (THIS DOES NOT EXIST)
```

The actual structure is:
```
/srv/arifOS/arifosmcp/runtime/       ← contains updated files
/srv/arifOS/arifosmcp/arifosmcp/   ← broken, doesn't exist
/srv/arifOS/arifosmcp/core/
```

### Files That Were Copied (but to wrong location)
We copied new files to `/srv/arifOS/arifosmcp/arifosmcp/runtime/` but Docker mounts expect them at `/srv/arifOS/arifosmcp/runtime/`.

### Current State
- Docker image is correct (verified with `docker run --rm`)
- Container is using old site-packages code because `pip install .` was run in the image build
- Volume mounts are misconfigured — `arifosmcp/arifosmcp` double-nesting doesn't exist

---

## DOCKER-COMPOSE.YML VOLUME MOUNT ISSUE (lines 335-347)

```yaml
volumes:
  - /opt/arifos/data/core:/usr/src/app/data:rw
  - /proc:/host/proc:ro
  - /sys:/host/sys:ro
  - /srv/arifosmcp/arifosmcp:/usr/src/app/arifosmcp:ro      # BROKEN SYMLINK
  - /srv/arifosmcp/server.py:/usr/src/app/server.py:ro    # BROKEN SYMLINK
  - /srv/arifosmcp/stdio_server.py:/usr/src/app/stdio_server.py:ro
  - /srv/arifosmcp/fastmcp.json:/usr/src/app/fastmcp.json:ro
  - /srv/arifosmcp/mcp.json:/usr/src/app/mcp.json:ro
  - /srv/arifosmcp/core:/usr/src/app/core:ro               # BROKEN SYMLINK
  - /srv/arifosmcp/000:/usr/src/app/000:ro                # BROKEN SYMLINK
  - /srv/arifosmcp/333:/usr/src/app/333:ro                # BROKEN SYMLINK
  - /srv/arifosmcp/spec:/usr/src/app/spec:ro              # BROKEN SYMLINK
```

The `/srv/arifosmcp` symlink → `/srv/arifOS/arifosmcp`, so:
- `/srv/arifosmcp/arifosmcp` → `/srv/arifOS/arifosmcp/arifosmcp` (doesn't exist!)
- Should be: `/srv/arifOS/arifosmcp` directly

---

## FILES CREATED/UPDATED

### New Files
| File | Purpose |
|------|---------|
| `data/philosophy_atlas.json` | 27-zone, 81 quotes |
| `arifosmcp/runtime/philosophy.py` | Atlas-based 3D selection |
| `arifosmcp/intelligence/tools/wisdom_quotes.py` | Atlas integration |
| `000/ROOT/K_FORGE.md` | Pre-deployment architecture |
| `000/ROOT/K_FOUNDATIONS.md` | 99-domain math foundations |

### Updated Files
| File | Changes |
|------|---------|
| `arifosmcp/runtime/init_anchor_hardened.py` | constitutional_context, telos_manifold, godel_lock |
| `arifosmcp/core/organs/_1_agi.py` | Constitutional prefix on prompts |
| `arifosmcp/runtime/tools_hardened_dispatch.py` | Pass constitutional_context |
| `arifosmcp/runtime/tools_hardened_v2.py` | Forge pipeline, explorer/conservator |
| `arifosmcp/core/organs/_3_apex.py` | Stage 777 pressure tests |
| `arifosmcp/runtime/tools_internal.py` | Wire delta_s/omega_score |
| `arifosmcp/intelligence/tools/thermo_estimator.py` | New functions |

---

## ENVIRONMENT

- **VPS**: `srv1325122` (already on machine, no SSH needed)
- **Working dir**: `/root/arifOS/`
- **Docker compose**: `/root/arifOS/docker-compose.yml`
- **Dockerfile**: `/root/arifOS/Dockerfile`
- **Symlinks**: `/srv/arifosmcp` → `/srv/arifOS/arifosmcp`

---

## GIT STATUS

- Main repo (`/root/arifOS/`): Branch main, clean working tree (only infra/openclaw/Dockerfile modified)
- Submodule (`/root/arifOS/arifosmcp/`): Branch main, HEAD at `8caa30d` ("FORGE: Philosophy Atlas + Input Hardening + Forge Pipeline"), clean

---

## KEY CONTAINERS

```bash
# All running:
arifos_postgres       healthy
arifos_redis         healthy
ollama_engine        running
qdrant_memory        running
arifosmcp_server     running  ← THE PROBLEMATIC ONE

# Check status:
docker compose -f /root/arifOS/docker-compose.yml ps

# View logs:
docker compose -f /root/arifOS/docker-compose.yml logs --tail=30 arifosmcp
```

---

## HOW TO FIX THE VOLUME MOUNT ISSUE

### Option 1: Fix docker-compose.yml (RECOMMENDED)
Change all `/srv/arifosmcp/` volume mounts to `/srv/arifOS/arifosmcp/`:

```yaml
volumes:
  - /srv/arifOS/arifosmcp:/usr/src/app/arifosmcp:ro
  - /srv/arifOS/arifosmcp/server.py:/usr/src/app/server.py:ro
  # etc.
```

But note: the submodule itself has `server.py`, `mcp.json`, etc. at its ROOT, not in subdirs.

Actually, verify the actual structure:
```
/srv/arifOS/arifosmcp/         ← git submodule root (this IS the arifosmcp package)
  server.py
  mcp.json
  fastmcp.json
  runtime/
  core/
  000/
  333/
  spec/
```

So the mounts should be:
- `/srv/arifOS/arifosmcp:/usr/src/app/arifosmcp:ro`  ← correct
- But then server.py, mcp.json are at package root, not `/usr/src/app/`

Wait - the server.py that runs IS `/usr/src/app/server.py` (the uvicorn entrypoint). If we mount the whole submodule to `/usr/src/app/arifosmcp`, we lose the server.py at `/usr/src/app/`.

### Option 2: Remove pip install from Dockerfile
Since the volume mounts override `/usr/src/app/`, we could skip the `pip install .` in the Dockerfile to avoid the site-packages conflict. But then we'd lose the package if mounts fail.

### Option 3: Add PYTHONPATH override
Set `PYTHONPATH=/usr/src/app:$PYTHONPATH` in the container environment to prioritize `/usr/src/app` over site-packages. But sys.path ordering may still fail due to how Python caches imports.

---

## WHAT NEEDS TO HAPPEN

1. **Fix volume mounts** so `/usr/src/app/arifosmcp/` actually contains the new code
2. **OR remove pip-installed package** from site-packages so `/usr/src/app/` wins
3. **Test init_anchor** to verify philosophy, telos_manifold, godel_lock, constitutional_context are returned
4. **Push to HORIZON** (GitHub remote)

---

## TESTING COMMANDS

```bash
# Test from INSIDE container (currently fails with site-packages conflict):
docker compose -f /root/arifOS/docker-compose.yml exec -T arifosmcp python3 /dev/stdin << 'PYEOF'
import sys
sys.path.insert(0, '/usr/src/app')
from arifosmcp.runtime.init_anchor_hardened import init_anchor_hardened
import asyncio
async def test():
    result = await init_anchor_hardened(
        mode='status',
        thermodynamic_budget={'enthalpy': 100, 'entropy': 50},
        architect_registry={'resources': [], 'agents': []}
    )
    print('philosophy:', result.get('philosophy')[:200] if result.get('philosophy') else None)
    print('telos_manifold:', result.get('telos_manifold'))
    print('godel_lock:', result.get('godel_lock'))
    print('constitutional_context present:', result.get('constitutional_context') is not None)
    print('DITEMPA motto:', 'DITEMPA' in str(result.get('philosophy', '')))
asyncio.run(test())
PYEOF

# Test from FRESH image (works):
docker run --rm arifos/arifosmcp:latest python3 -c "
import sys
sys.path.insert(0, '/usr/src/app')
from arifosmcp.runtime.init_anchor_hardened import init_anchor_hardened
import asyncio
async def test():
    result = await init_anchor_hardened(
        mode='status',
        thermodynamic_budget={'enthalpy': 100, 'entropy': 50},
        architect_registry={'resources': [], 'agents': []}
    )
    print('philosophy:', result.get('philosophy')[:200] if result.get('philosophy') else None)
asyncio.run(test())
"

# Health check:
curl -s https://arifosmcp.arif-fazil.com/health | python3 -m json.tool
```

---

## REFERENCE: docker-compose.yml line 339

The problematic mount:
```yaml
- /srv/arifosmcp/arifosmcp:/usr/src/app/arifosmcp:ro
```

Since `/srv/arifosmcp` → `/srv/arifOS/arifosmcp`, this resolves to:
`/srv/arifOS/arifosmcp/arifosmcp` which **DOES NOT EXIST**.

The actual submodule is at `/srv/arifOS/arifosmcp/` (not nested).

---

## NOTES

- The `pip install .` in Dockerfile installs the package to site-packages
- Volume mounts try to mount from a broken symlink path
- Even with correct volume mounts, site-packages may still take precedence due to Python import caching
- The NEW CODE is correct in `/usr/src/app/arifosmcp/runtime/` inside the image (verified)
- The PROBLEM is the running container is somehow still using old cached site-packages code

---

## CLAUDE CODE INSTRUCTIONS

1. Diagnose why `docker compose exec` uses site-packages while `docker run --rm` uses /usr/src/app
2. Fix docker-compose.yml volume mounts OR Python path so new code runs
3. Verify init_anchor returns philosophy, telos_manifold, godel_lock, constitutional_context
4. Commit and push to HORIZON (GitHub)
