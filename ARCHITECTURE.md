# 📜 arifOS Architectural Dossier

**Components:** `aclip_cai`, `aaa_mcp`, `arifos_aaa_mcp`, `core`
**Version:** 2026.03.07-HARDENED
**Authority:** Arif (F13 Sovereign)
**Motto:** 🔥 DITEMPA BUKAN DIBERI — Forged, Not Given

arifOS separates perception, orchestration, runtime exposure, and constitutional law into distinct layers to preserve governance integrity.

---

## 1️⃣ aclip_cai — Sensory Infrastructure & Reality Console

**Layer:** L2 Operation ↔ L3 Reality
**Role:** Perception, grounding, and evidence acquisition.
**Root:** `aclip_cai/`

### Definition

The sensory subsystem of arifOS. Connects intelligence to external reality by retrieving and structuring evidence before it enters the constitutional reasoning pipeline.

Implements the **9-Sense model (C0–C9)** and the **Triad reasoning substrate** (Δ/Ω/Ψ).

### Source Map

| Path | Responsibility |
|------|---------------|
| `aclip_cai/triad/delta/` | Δ — AGI reasoning |
| `aclip_cai/triad/omega/` | Ω — ASI empathy / impact |
| `aclip_cai/triad/psi/` | Ψ — APEX judgment |
| `aclip_cai/tools/system_monitor.py` | C0 — System health |
| `aclip_cai/tools/reality_grounding.py` | C1 — Web intelligence |
| `aclip_cai/tools/chroma_query.py` | C2 — Knowledge retrieval |
| `aclip_cai/tools/net_monitor.py` | C3 — Social/network signals |
| `aclip_cai/tools/log_reader.py` | C7 — Memory / logs |
| `aclip_cai/tools/financial_monitor.py` | C6 — Economic signals |
| `aclip_cai/tools/manifold_adapter.py` | Protocol adapter layer |
| `aclip_cai/tools/safety_guard.py` | Pre-ingest safety filter |
| `aclip_cai/tools/thermo_estimator.py` | Thermodynamic cost estimation |
| `aclip_cai/core/kernel.py` | Internal perception kernel |
| `aclip_cai/core/vault_logger.py` | Evidence logging (read-side) |
| `aclip_cai/core/floor_audit.py` | Floor compliance audit |
| `aclip_cai/core/thermo_budget.py` | Entropy budget enforcement |
| `aclip_cai/embeddings/` | Vector embedding pipeline |

### 9-Sense Model

| Sense | Domain | Implementation |
|-------|--------|---------------|
| C0 | System health | `tools/system_monitor.py` |
| C1 | Web intelligence | `tools/reality_grounding.py` |
| C2 | Knowledge retrieval | `tools/chroma_query.py` |
| C3 | Social signals | `tools/net_monitor.py` |
| C4 | Temporal context | Derived from pipeline timestamp |
| C5 | Spatial signals | Derived from geo-context |
| C6 | Economic signals | `tools/financial_monitor.py` |
| C7 | Memory / logs | `tools/log_reader.py` |
| C8 | Internal reasoning | `triad/` subsystem |
| C9 | Code intelligence (LSP) | `tools/` + external LSP adapters |

### Boundary Invariants (HARD)

| # | Rule | Violation = |
|---|------|------------|
| B1 | No `server.py`, no `asgi.py`, no HTTP listener in `aclip_cai/` | Architecture breach |
| B2 | No session state management | Separation violation |
| B3 | No final constitutional verdict (888_JUDGE) | Governance bypass |
| B4 | No VAULT999 write access | Ledger integrity breach |

> ⚠️ **Observed deviation:** `aclip_cai/mcp_server.py` and `aclip_cai/core/mcp_server.py` exist. These are legacy/internal bridge files — they MUST NOT serve as public transport endpoints. If they accept external connections, refactor to `aaa_mcp`.

> **Analogy:** Eyes, Ears, Hands — perceives reality, does not decide policy.

---

## 2️⃣ aaa_mcp — Governed MCP Control Plane

**Layer:** L2 Operation ↔ L0 Kernel
**Role:** Protocol relay, orchestration, and governance gateway.
**Root:** `aaa_mcp/`

### Definition

The governed transport layer. Translates external requests into structured metabolic pipeline executions. Enforces constitutional boundaries before communication reaches the kernel. Contains **no independent decision logic.**

### Source Map

| Path | Responsibility |
|------|---------------|
| `aaa_mcp/server.py` | MCP server (STDIO) |
| `aaa_mcp/streamable_http_server.py` | MCP server (HTTP/SSE) |
| `aaa_mcp/asgi.py` | ASGI application entry |
| `aaa_mcp/auth.py` | Authentication layer |
| `aaa_mcp/core/stage_adapter.py` | Metabolic pipeline stage routing |
| `aaa_mcp/core/constitutional_decorator.py` | Floor enforcement decorator |
| `aaa_mcp/core/engine_adapters.py` | LLM engine abstraction |
| `aaa_mcp/core/mode_selector.py` | Reasoning mode selection |
| `aaa_mcp/sessions/session_ledger.py` | Session lifecycle + context |
| `aaa_mcp/sessions/session_dependency.py` | Session DI resolution |
| `aaa_mcp/vault/hardened.py` | VAULT999 write path (hardened) |
| `aaa_mcp/vault/precedent_memory.py` | Precedent lookup |
| `aaa_mcp/tools/vault_seal.py` | 999_VAULT sealing tool |
| `aaa_mcp/tools/reality_grounding.py` | Evidence bridge (delegates to aclip_cai) |
| `aaa_mcp/tools/trinity_validator.py` | Trinity consensus validation |
| `aaa_mcp/protocol/` | Tool registry, schemas, naming, mapping |
| `aaa_mcp/external_gateways/` | Brave, Perplexity, Jina, headless browser, gitingest |
| `aaa_mcp/notifiers/telegram_judge.py` | 888_HOLD Telegram notification |
| `aaa_mcp/infrastructure/` | Logging, monitoring, rate limiting |
| `aaa_mcp/integrations/` | Container controller, OpenClaw gateway client |
| `aaa_mcp/services/redis_client.py` | Redis session/cache |
| `aaa_mcp/services/sandbox_runner.py` | Sandboxed code execution |

### Metabolic Pipeline (11 stages)

```
000_INIT → 111_SENSE → 222_THINK → 333_REASON → 444_SYNC →
555_EMPATHIZE → 666_ALIGN → 777_FORGE → 888_JUDGE → 889_FINALIZE → 999_VAULT
```

### Transport Modes

| Mode | File | Protocol |
|------|------|----------|
| STDIO | `server.py` | JSON-RPC over stdin/stdout |
| HTTP | `streamable_http_server.py` | Streamable HTTP (MCP 2025-03) |
| SSE | `streamable_http_server.py` | Server-Sent Events (legacy compat) |
| ASGI | `asgi.py` | ASGI application (uvicorn) |

### Boundary Invariants (HARD)

| # | Rule | Violation = |
|---|------|------------|
| B5 | No Triad (Δ/Ω/Ψ) implementation | Separation violation |
| B6 | No 9-Sense tool implementation (C0–C9) | Perception leak |
| B7 | No modification of F1–F13 floor definitions | Constitutional breach |
| B8 | `reality_grounding.py` in aaa_mcp MUST delegate to `aclip_cai`, not implement | Boundary collapse |

> **Analogy:** Brain Stem — relays signals between perception and law while preserving invariants.

---

## 3️⃣ arifos_aaa_mcp — Canonical Runtime Entrypoint

**Layer:** Deployment Surface
**Role:** Executable MCP bridge package.
**Root:** `arifos_aaa_mcp/`
**PyPI:** `arifos-aaa-mcp`
**npm:** `@arifos/mcp`

### Definition

The public runtime package. Packages `aaa_mcp` into a deployable Python module. This is what external AI systems connect to.

### Source Map

| Path | Responsibility |
|------|---------------|
| `arifos_aaa_mcp/server.py` | **Canonical entrypoint** — 13-tool public surface |
| `arifos_aaa_mcp/__main__.py` | `python -m arifos_aaa_mcp` runner |
| `arifos_aaa_mcp/governance.py` | Runtime governance wrapper |
| `arifos_aaa_mcp/contracts.py` | Input/output contracts |
| `arifos_aaa_mcp/rest_routes.py` | REST API routes (health, MCP) |
| `arifos_aaa_mcp/fastmcp_ext/` | FastMCP transport extensions |

### Runtime Execution

```bash
# STDIO mode (for Claude, Cursor, etc.)
python -m arifos_aaa_mcp stdio

# HTTP mode (for Docker, remote clients)
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp http
```

### Public Tool Surface (13 tools)

| Tool | Stage | Purpose |
|------|-------|---------|
| `anchor_session` | 000 | Boot constitutional session |
| `reason_mind` | 333 | AGI cognition + reasoning |
| `vector_memory` | 555 | Semantic search (Qdrant + GDrive) |
| `simulate_heart` | 555 | ASI empathy simulation |
| `critique_thought` | 666 | Self-critique against floors |
| `eureka_forge` | 777 | Synthesis + solution forge |
| `apex_judge` | 888 | Final constitutional verdict |
| `seal_vault` | 999 | Seal to VAULT999 ledger |
| `search_reality` | READ | Multi-source web search |
| `fetch_content` | READ | URL content extraction |
| `inspect_file` | READ | File inspection |
| `audit_rules` | READ | Floor audit |
| `check_vital` | READ | System vitals |

### Boundary Invariants (HARD)

| # | Rule | Violation = |
|---|------|------------|
| B9 | No reasoning logic — all delegated to `aaa_mcp` → `aclip_cai` | Architecture collapse |
| B10 | No perception implementation | Separation violation |
| B11 | No floor definition or modification | Constitutional breach |
| B12 | `server.py` imports from `aaa_mcp`/`aclip_cai` only — no inline logic | Wrapper purity breach |

> **Analogy:** Helmet Plug — the interface other systems use to connect to the arifOS brain.

---

## 4️⃣ core — Constitutional Kernel

**Layer:** L0 Kernel
**Role:** Floor enforcement, final judgment, governance law.
**Root:** `core/`

### Definition

The constitutional kernel. Defines and enforces F1–F13 floors. Contains the final verdict logic (888_JUDGE), thermodynamic physics, and recovery mechanisms. **This is the law.**

### Source Map

| Path | Responsibility |
|------|---------------|
| `core/governance_kernel.py` | Master governance engine |
| `core/judgment.py` | 888 judgment logic |
| `core/pipeline.py` | Full metabolic pipeline orchestration |
| `core/homeostasis.py` | System homeostasis / self-regulation |
| `core/kernel/constants.py` | Floor definitions, thresholds |
| `core/kernel/constitutional_decorator.py` | Floor enforcement decorator (canonical) |
| `core/kernel/evaluator.py` | Floor evaluation engine |
| `core/kernel/heuristics.py` | Heuristic floor scoring |
| `core/kernel/stage_orchestrator.py` | Pipeline stage orchestration |
| `core/kernel/init_000_anchor.py` | Session anchor (000) |
| `core/organs/_0_init.py` | Organ: initialization |
| `core/organs/_1_agi.py` | Organ: AGI reasoning |
| `core/organs/_2_asi.py` | Organ: ASI empathy |
| `core/organs/_3_apex.py` | Organ: APEX judgment |
| `core/organs/_4_vault.py` | Organ: VAULT999 sealing |
| `core/physics/thermodynamics.py` | ΔS ≤ 0 enforcement |
| `core/physics/thermodynamics_hardened.py` | Hardened thermo (production) |
| `core/enforcement/aki_contract.py` | AKI safety contract |
| `core/enforcement/routing.py` | Enforcement routing |
| `core/recovery/quarantine.py` | Floor violation quarantine |
| `core/recovery/rollback_engine.py` | F1 rollback engine |
| `core/perception/reality_ingest.py` | Reality ingest (kernel-side) |
| `core/observability/metrics.py` | Constitutional metrics |

### Boundary Invariants (HARD)

| # | Rule | Violation = |
|---|------|------------|
| B13 | `core/` is the SOLE authority for F1–F13 definitions | Split-brain governance |
| B14 | No transport/protocol code in `core/` | Layer violation |
| B15 | No external API calls from `core/` — evidence arrives via pipeline | Perception leak |
| B16 | Floor thresholds in `core/kernel/constants.py` are canonical | Drift = constitutional crisis |

---

## 🧠 Full System Flow

```
REAL WORLD (L3)
     ↓
┌──────────────┐
│  aclip_cai   │  Sensory infrastructure — 9-Sense (C0–C9) — Triad (Δ/Ω/Ψ)
│  L2↔L3       │  Evidence grounding — protocol adapters
└──────┬───────┘
       ↓ structured evidence
┌──────────────┐
│   aaa_mcp    │  Governed transport — Session mgmt — Metabolic pipeline
│  L2↔L0       │  STDIO/HTTP/SSE — Constitutional decorator — VAULT999 write
└──────┬───────┘
       ↓ governed pipeline stages
┌──────────────┐
│    core       │  Constitutional kernel — F1–F13 — 888_JUDGE — Thermodynamics
│  L0 Kernel   │  Final verdict — Rollback engine — Quarantine
└──────────────┘
       ↑ tool calls from external AI
┌──────────────┐
│arifos_aaa_mcp│  Runtime package — 13-tool surface — PyPI/npm distribution
│  Deployment  │  python -m arifos_aaa_mcp {stdio|http}
└──────────────┘
```

---

## 🧩 Component Responsibilities Matrix

| Capability | `aclip_cai` | `aaa_mcp` | `arifos_aaa_mcp` | `core` |
|---|:---:|:---:|:---:|:---:|
| Reality sensing (C0–C9) | ✔ | ✖ | ✖ | ✖ |
| Triad reasoning (Δ/Ω/Ψ) | ✔ | ✖ | ✖ | ✖ |
| Protocol transport | ✖ | ✔ | ✖ | ✖ |
| Session management | ✖ | ✔ | ✖ | ✖ |
| Metabolic pipeline | ✖ | ✔ | ✖ | ✔ |
| Tool exposure (13 tools) | ✖ | ✔ | ✔ | ✖ |
| Runtime execution | ✖ | ✖ | ✔ | ✖ |
| Floor definitions (F1–F13) | ✖ | ✖ | ✖ | ✔ |
| Constitutional judgment | ✖ | ✖ | ✖ | ✔ |
| VAULT999 sealing | ✖ | ✔ | ✖ | ✔ |
| Thermodynamic enforcement | ✖ | ✖ | ✖ | ✔ |
| Rollback / quarantine | ✖ | ✖ | ✖ | ✔ |

---

## ⚖️ Design Principles

1. **Separation of Perception and Governance** — Perception in `aclip_cai`, governance in `core`. Never mixed.
2. **Transport Neutrality** — `aaa_mcp` supports STDIO/HTTP/SSE without altering logic.
3. **Runtime Isolation** — `arifos_aaa_mcp` packages without embedding intelligence.
4. **Constitutional Integrity** — All floor definitions and judgment logic live in `core/`. Period.
5. **Evidence-First** — No verdict without evidence. Evidence flows L3→L2→L0, never shortcuts.
6. **Reversibility by Default (F1)** — `core/recovery/rollback_engine.py` exists for a reason.

---

## 🔒 Boundary Verification Checklist

Run periodically to detect architectural drift:

```bash
# B1: aclip_cai must not serve HTTP
grep -rn "uvicorn\|app\.run\|HTTPServer\|FastAPI\|Starlette" aclip_cai/ --include="*.py" | grep -v test | grep -v __pycache__

# B5: aaa_mcp must not contain Triad
test -d aaa_mcp/triad && echo "VIOLATION: B5 — Triad found in aaa_mcp"

# B9: arifos_aaa_mcp must not contain reasoning
wc -l arifos_aaa_mcp/*.py arifos_aaa_mcp/**/*.py 2>/dev/null
# If any single file exceeds ~200 lines, inspect for inline logic

# B13: Floor constants must be in core only
grep -rn "F1.*Amanah\|F2.*Truth\|F13.*Sovereign" aclip_cai/ aaa_mcp/ arifos_aaa_mcp/ --include="*.py" | grep -v "import\|comment\|#\|test"

# B14: No transport in core
grep -rn "FastAPI\|Starlette\|uvicorn\|StreamableHTTP" core/ --include="*.py" | grep -v test
```

---

## ⚠️ Known Deviations (to track)

| # | Deviation | Location | Risk | Action |
|---|-----------|----------|------|--------|
| D1 | `aclip_cai/mcp_server.py` exists | `aclip_cai/` | Medium — could serve as rogue transport | Verify it's internal bridge only; refactor if it accepts external connections |
| D2 | `aclip_cai/core/mcp_server.py` exists | `aclip_cai/core/` | Medium — same risk | Same action |
| D3 | `aaa_mcp/tools/reality_grounding.py` exists | `aaa_mcp/tools/` | Low if it delegates | Verify it delegates to `aclip_cai`, not reimplements |

---

🔥 **DITEMPA BUKAN DIBERI** — The architecture is forged through separation of responsibility, not granted by convenience.
