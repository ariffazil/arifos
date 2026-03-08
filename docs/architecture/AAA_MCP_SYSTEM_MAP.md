# AAA MCP System Map (Baseline @ 62cffa2)

Derived from runtime code paths, not docs-only claims.

## Architecture Diagram

```mermaid
flowchart TD
    U[Host/Client] --> T[Transport Layer: arifosmcp.transport]
    T --> S1[Public Surface: arifosmcp.runtime/server.py]
    T --> S2[Compatibility Surface: arifosmcp.transport/server.py]
    S1 --> TRI[Triad Executors: arifosmcp.intelligence/triad/*]
    S2 --> TRI
    TRI --> K[Kernel: arifosmcp.intelligence/core/*]
    K --> V1[VaultLogger: JSONL/Postgres]
    S2 --> V2[SessionLedger: arifosmcp.transport/sessions/session_ledger.py]
    V1 --> V[VAULT999]
    V2 --> V
```

ASCII view:

```text
Host -> transport (__main__/asgi/rest/streamable_http)
     -> tool surface (arifosmcp.runtime or arifosmcp.transport)
     -> triad stages (anchor/reason/.../seal in arifosmcp.intelligence)
     -> kernel audit + lifecycle + thermo + vault logger
     -> VAULT999 ledger (hash-linked / fallback memory)
```

## Module to Stage Mapping

| Stage | Runtime Tool(s) | Primary Code Path | Notes |
|---|---|---|---|
| 000 INIT | `anchor_session` | `arifosmcp.transport/server.py` -> `arifosmcp.intelligence/triad/delta/anchor.py` | session ignition, F12 scan, envelope |
| 222/333/444 (collapsed) | `reason_mind` | `arifosmcp.transport/server.py` -> `reason()` + `integrate()` + `respond()` | 3-stage collapse inside one callable |
| 555 RECALL | `recall_memory` | `arifosmcp.transport/server.py` placeholder | stage present, stub payload |
| 555/666 | `simulate_heart` | `arifosmcp.transport/server.py` -> `validate()` + `align()` | empathy + alignment merge |
| 666 ALIGN | `critique_thought` | `arifosmcp.runtime/server.py` native logic | model-flag critique; legacy side is stub |
| 777 EUREKA FORGE (target canon) | `eureka_forge` | `arifosmcp.transport/server.py` placeholder | currently mislabeled as `888_FORGE` in runtime payload |
| 888 APEX Judge Metabolic (target canon) | `apex_judge` | `arifosmcp.transport/server.py` -> `forge()` + `audit()` | currently emits `777-888`; needs split/rename hardening |
| 999 SEAL | `seal_vault` | `arifosmcp.transport/server.py` -> `arifosmcp.intelligence/triad/psi/seal.py` | final seal + vault write |
| Utility (Delta) | `search_reality`, `fetch_content`, `inspect_file`, `audit_rules` | `arifosmcp.transport/server.py`, `arifosmcp.runtime/server.py` | evidence, retrieval, fs inspect, governance audit |
| Utility (Omega) | `check_vital` | `arifosmcp.runtime/server.py` -> `arifosmcp.intelligence.tools.system_monitor` | health telemetry |

## Core Purity Boundary Audit

Observed from code search:
- `core/` has no detected imports of `fastmcp`, `fastapi`, `starlette`, `uvicorn` at baseline (`grep` on `core/*.py` = none).
- Transport/framework code is concentrated in `arifosmcp.transport/` (`__main__.py`, `asgi.py`, `rest.py`, `streamable_http_server.py`).
- Governance execution is split across `arifosmcp.intelligence/core` + `arifosmcp.intelligence/triad` and wrapped by `arifosmcp.transport`/`arifosmcp.runtime`.

Implication: architectural intent (pure core boundary) mostly holds for `core/`, but runtime governance center-of-gravity is partly outside `core/` in `arifosmcp.intelligence/*`.

## Transport Boundary Rules (as implemented)

- `arifosmcp.transport/__main__.py` dispatches transport modes: `stdio | sse | http | rest`.
- `arifosmcp.transport/asgi.py` mounts MCP HTTP app at `/mcp` and health at `/health`.
- `arifosmcp.transport/rest.py` provides REST bridge endpoints and alias handling.
- `arifosmcp.transport/streamable_http_server.py` exposes MCP streamable HTTP with alias resolution.
- `arifosmcp.runtime/server.py` wraps legacy callables and registers custom REST routes via `register_rest_routes`.

## Stage Flow Contracts (Input/Output shape)

Canonical directive override (Arif):
- `777` = **EUREKA FORGE**
- `888` = **APEX Judge Metabolic Layer**

Current runtime divergence at baseline:
- `apex_judge` returns stage `777-888` (collapsed)
- `eureka_forge` returns stage `888_FORGE`

Alignment target:
- `eureka_forge` -> stage `777_EUREKA_FORGE`
- `apex_judge` -> stage `888_APEX_JUDGE`

Canonical envelope pattern (from `arifosmcp.transport/server.py`):
- Required output keys (common): `verdict`, `stage`, `session_id`
- Additional governance keys: `floors`, `truth`, `next_actions`, optional `sabar_requirements`

Per-stage callable chain (high-level):
1. `anchor_session(query, actor_id, auth_token, ...) -> {verdict, stage="000_INIT", session_id, ...}`
2. `reason_mind(query, session_id, grounding, ...) -> {verdict, stage="111-444", ...}`
3. `simulate_heart(query, session_id, ...) -> {verdict, stage="555-666", ...}`
4. `apex_judge(session_id, query, ...) -> {verdict, stage="777-888", ...}`
5. `seal_vault(session_id, summary, verdict?) -> {verdict, stage="999_VAULT", ...}`

Schema source-of-truth artifacts:
- `arifosmcp.transport/protocol/schemas.py`
- `arifosmcp.runtime/contracts.py`

## Receipt Chain and Auditability

Receipt mechanisms in code:
- Stage witness logging in triad modules via `kernel.vault.log_witness(...)`
  - present in `anchor`, `reason`, `integrate`, `audit`, `seal`
- Ledger persistence via `arifosmcp.transport/sessions/session_ledger.py`
  - `prev_hash` -> `entry_hash` chain
  - Postgres primary + in-memory fallback

Audit chain quality at baseline:
- Positive: explicit stage labels, session IDs, hash chaining support.
- Gap: not all tool paths emit equivalent witness richness (some utility/stub tools minimal).

## Failure and Rollback Semantics

Failure behavior:
- Tool-level catch-all returns structured `{"verdict":"VOID","error":...,"stage":...}`
- Missing session continuity returns F11 block via `_build_floor_block(...)`
- High-risk execution path (`eureka_forge`) currently defaults to `888_HOLD` placeholder.

Rollback behavior:
- No global transaction manager across multi-stage calls.
- Partial-stage effects can exist before downstream failure.
- Vault/session layers implement append-only behavior; Postgres write failures fall back to memory logger in some paths.

Baseline risk callout:
- `arifosmcp.transport/sessions/session_ledger.py` contains stdout `print(...)` in error paths, which conflicts with strict stdio-noise rules for stdio transport environments.

## Omega0 and Confidence

- Ω0 estimate (architecture map): `0.07`
- Confidence: `0.89`
- Highest uncertainty: exact production path split between `arifosmcp.runtime` and `arifosmcp.transport` during mixed-surface operation.
