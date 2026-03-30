# arifOS × arifosmcp ATLAS
**Purpose:** Clear boundary between Parent Kernel (arifOS) and MCP Implementation (arifosmcp)
**Generated:** 2026-03-31
**Status:** DRAFT - Needs Validation

---

## SECTION 1: CONTRAST (The Two Repos)

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│         arifOS (Parent)         │     │      arifosmcp (Child)          │
│         "The Brain"             │     │         "The Limbs"             │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ Role: GOVERNANCE & LAW          │     │ Role: PROTOCOL & CAPABILITY     │
│ Purpose: Sovereign Kernel        │     │ Purpose: MCP Server (deployable)│
│ Questions: "Is this allowed?"    │     │ Questions: "How do we do it?"  │
│ Foci: 13 Floors, VAULT999       │     │ Foci: Tools, Transport, Runtime │
│ Lifecycle: 000→333→999           │     │ Lifecycle: Serve tools via MCP  │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

---

## SECTION 2: WHAT BELONGS WHERE

### arifOS (Parent) — KEEP HERE

| Directory | Purpose | Status |
|-----------|---------|--------|
| `000/` | Init protocols, constitution | ✅ Already here |
| `333/` | Mind/Delta protocols | ✅ Already here |
| `AGENTS/` | Agent definitions (A-ARCHITECT, etc) | ✅ Already here |
| `core/` | Governance engine, kernel, physics | ❌ INCOMPLETE |
| `agentzero/` | Agent zero implementation | ❌ MISSING (in arifosmcp) |
| `intelligence/` | Intelligence triad | ❌ MISSING (in arifosmcp) |
| `init_000/` | DB, migrations | ❌ MISSING (in arifosmcp) |
| `helix/` | Inner organs | ❌ MISSING (in arifosmcp) |
| `tools/` | Non-MCP tools | ❌ MISSING (in arifosmcp) |
| `models/` | Provider configs | ❌ MISSING (in arifosmcp) |
| `VAULT999/` | Outcome ledger | ❌ MISSING (in arifosmcp) |
| `metadata/` | Schema snapshots | ❌ MISSING (in arifosmcp) |
| `sites/` | Dashboards, docs | ❌ MISSING (in arifosmcp) |
| `tests/` | All pytest tests | ✅ Already here |
| `skills/` | arifOS skills | ✅ Already here |
| `deployment/` | Docker configs | ✅ Already here |
| `infrastructure/` | VPS configs | ✅ Already here |

### arifosmcp (Child) — MCP SERVER ONLY

| Directory | Purpose | Status |
|-----------|---------|--------|
| `server.py` | Main entrypoint | ✅ KEEP |
| `server_horizon.py` | Horizon entrypoint | ✅ KEEP |
| `transport/` | ACP transport | ✅ KEEP |
| `runtime/fastmcp_compat.py` | MCP compat | ✅ KEEP |
| `runtime/server.py` | MCP server | ✅ KEEP |
| `runtime/mcp_utils.py` | MCP utils | ✅ KEEP |
| `runtime/capability_map.py` | MCP capability | ✅ KEEP |
| `runtime/tool_dials_map.json` | MCP config | ✅ KEEP |
| `runtime/tool_specs.py` | MCP specs | ✅ KEEP |
| `packages/npm/` | TypeScript MCP client | ✅ KEEP |
| `Dockerfile` | Container build | ✅ KEEP |
| `docker-compose.yml` | Container orchestration | ✅ KEEP |
| `requirements.txt` | Python deps | ✅ KEEP |
| `pyproject.toml` | Python project | ✅ KEEP |

---

## SECTION 3: FILES TO MOVE OUT OF arifosmcp → arifOS

| Directory | Files | Move to |
|-----------|-------|---------|
| `agentzero/` | ~15 | `arifOS/agentzero/` |
| `core/` | ~80 | `arifOS/core/` |
| `intelligence/` | ~50 | `arifOS/intelligence/` |
| `init_000/` | ~15 | `arifOS/init_000/` |
| `helix/` | ~10 | `arifOS/helix/` |
| `tools/` | ~25 | `arifOS/tools/` |
| `models/` | ~5 | `arifOS/models/` |
| `shared/` | ~20 | `arifOS/core/shared/` |
| `sites/` | ~50 | `arifOS/sites/` |
| `static/` | ~5 | `arifOS/static/` |
| `VAULT999/` | 1 | `arifOS/VAULT999/` |
| `metadata/` | ~5 | `arifOS/metadata/` |
| `integrations/prefect/` | ~5 | `arifOS/integrations/` |
| `docs/SOVEREIGN_ACTION_SYSTEM.md` | 1 | `arifOS/docs/` |
| `openai_bridge.py` | 1 | `arifOS/` |
| `999_SEAL.md` | 1 | `arifOS/` |

**Total files to move: ~280 files**

---

## SECTION 4: SUBMODULE CONNECTION

```
arifOS (Parent)
│
├── [SUBMODULE] arifosmcp/  ──────────────────────────┐
│   ├── server.py                                    │
│   ├── transport/                                   │
│   ├── runtime/fastmcp_compat.py                    │
│   ├── runtime/server.py                            │
│   ├── runtime/mcp_utils.py                         │
│   ├── runtime/capability_map.py                    │
│   ├── runtime/tool_dials_map.json                 │
│   ├── runtime/tool_specs.py                        │
│   ├── packages/npm/                                │
│   ├── Dockerfile                                   │
│   ├── docker-compose.yml                          │
│   ├── requirements.txt                             │
│   └── pyproject.toml                              │
│                                                    │
│   (~280 non-MCP files should be HERE in arifOS)   │
└────────────────────────────────────────────────────┘
                          ▲
                          │ imports
                          │
              arifOS uses arifosmcp as MCP server
```

---

## SECTION 5: FILE COUNT

| Repo | Current | After Cleanup |
|------|---------|--------------|
| arifOS | 1,126 | ~1,400 (+280) |
| arifosmcp | 549 | ~270 (-280) |

---

## SECTION 6: IMMEDIATE FIXES NEEDED

### 1. Broken Submodule Reference
```
Parent arifOS tracks commit 568bbb8 (DOES NOT EXIST)
Submodule actual HEAD: 83527ec
FIX: git submodule update --init arifosmcp
```

### 2. Staged Deletions in Submodule
```
~200 files staged for deletion in arifosmcp
FIX: cd arifosmcp && git reset HEAD
```

### 3. .gitmodules has conflict markers
```
Resolution needed in .gitmodules
```

---

## SECTION 7: MIGRATION STEPS

1. **Backup** (just in case)
2. **Fix submodule** issues (Section 6)
3. **Move files** from arifosmcp → arifOS (per Section 3)
4. **Commit in arifosmcp** (clean MCP-only state)
5. **Commit in arifOS** (add moved files, update submodule ref)
6. **Test deployment** before pushing

---

## SECTION 8: CONTEXT GRAPH

```
ariffazil (github.com/ariffazil/)
│
├── ariffazil/ (landing page repo)
│
├── arif-sites/ (static sites repo)
│   └── arif-fazil.com, apex.arif-fazil.com
│
├── GEOX/ (geoscience tools repo)
│
└── arifOS/ (main orchestration repo)
    │
    ├── [SUBMODULE] arifosmcp/ ← MCP SERVER (lean, deployable)
    │   └── What it does: Exposes arifOS tools via MCP protocol
    │
    ├── [SUBMODULE] arifOS-model-registry/ ← MODEL CONFIGS
    │
    ├── [SUBMODULE] geox/ ← GEOSCIENCE (linked, not same as GEOX repo)
    │
    └── core governance files:
        ├── 000/ 333/ 999/ (lifecycle docs)
        ├── AGENTS/ (agent definitions)
        ├── tests/ skills/ scripts/
        ├── deployment/ infrastructure/
        └── (etc)
```
