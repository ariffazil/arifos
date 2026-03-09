# arifOS Canonical Output Schema

**Version:** 1.0.0  
**Authority:** Muhammad Arif bin Fazil (888_JUDGE)  
**Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given

---

## Overview

Every arifOS MCP tool returns the **same canonical envelope**.  
Tool-specific data lives inside the `payload` field only.  
Nothing else is permitted at the top level.

The schema is designed to be:

- **Minimal** — 12 top-level fields, nothing more
- **Governed** — verdict contract enforced at every stage
- **Tool-consistent** — all tools return the identical envelope
- **Production-safe** — no debug leakage, no philosophy quotes, no raw internals
- **Auditable** — trace shows exactly which stages ran and at what verdict

---

## The Metabolic Routing Model

arifOS is a **thermodynamically-governed metabolic router**.  
The server does not select tools first — it selects a **stage**, and tools execute *inside* stages.

```
query → stage → tool → verdict
```

The pipeline is governed by two quantities:

```
G   = constitutional alignment score ∈ [0, 1]
ΔS  = entropy change (negative = clarity improvement)
```

**Routing flow:**

```
000_INIT    → identity / auth / intent detection
111_SENSE   → parse intent (AGI layer begins)
222_REALITY → gather evidence via search_reality / ingest_evidence
333_MIND    → reasoning via reason_mind (AGI layer)
444_ROUTER  → pipeline routing decision
555_HEART   → safety / empathy via simulate_heart (ASI layer begins)
666_CRITIQUE→ alignment via critique_thought (ASI layer)
777_FORGE   → execution via eureka_forge (APEX layer begins)
888_JUDGE   → sovereign decision via apex_judge (APEX layer)
999_VAULT   → persistence via seal_vault (SEAL layer)
```

**Layer clusters:**

| Layer | Stages  | Function              |
|-------|---------|-----------------------|
| INIT  | 000     | Identity & auth       |
| AGI   | 111–333 | Reasoning             |
| ASI   | 555–666 | Alignment & safety    |
| APEX  | 777–888 | Sovereign decision    |
| SEAL  | 999     | Persistence           |

The pipeline **stabilizes** when entropy (ΔS) reaches a minimum or a verdict forces termination.  
The `stage` field in the output captures *where the pipeline stabilized*.  
The `trace` field records the full path actually traveled.

---

## Canonical Envelope

```json
{
  "ok": true,
  "tool": "reason_mind",
  "session_id": "sess_123",
  "stage": "333_MIND",
  "verdict": "PROVISIONAL",
  "status": "SUCCESS",
  "metrics": {
    "truth": 0.82,
    "clarity_delta": -0.08,
    "confidence": 0.72,
    "peace": 1.0,
    "vitality": 9.7,
    "entropy_delta": -0.08,
    "authority": 1.0,
    "risk": 0.14
  },
  "trace": {
    "000_INIT": "SEAL",
    "111_SENSE": "SEAL",
    "222_REALITY": "PARTIAL",
    "333_MIND": "PROVISIONAL"
  },
  "authority": {
    "actor_id": "arif",
    "level": "human",
    "human_required": false,
    "approval_scope": [],
    "auth_state": "verified"
  },
  "payload": {
    "reasoning_status": "exploratory",
    "confidence_band": "PLAUSIBLE",
    "needs_grounding": true,
    "next_stage": "666_CRITIQUE",
    "hypotheses": [
      {
        "path": "conservative",
        "band": "CLAIM",
        "confidence": 0.91,
        "hypothesis": "..."
      }
    ]
  },
  "errors": [],
  "meta": {
    "schema_version": "1.0.0",
    "timestamp": "2026-03-10T12:00:00Z",
    "debug": false,
    "dry_run": false
  }
}
```

---

## Top-Level Fields

| Field        | Type              | Meaning                                              |
|--------------|-------------------|------------------------------------------------------|
| `ok`         | boolean           | Transport success flag                               |
| `tool`       | string            | Tool name that produced this response                |
| `session_id` | string \| null    | Active session identifier                            |
| `stage`      | string            | Stage where pipeline stabilized (e.g. `333_MIND`)   |
| `verdict`    | enum (6 values)   | Constitutional governance verdict                    |
| `status`     | enum (4 values)   | Transport / runtime state                            |
| `metrics`    | object            | All numeric telemetry (unified)                      |
| `trace`      | object            | Stage execution path (stage_key → verdict_value)     |
| `authority`  | object            | Actor / approval context (production-safe)           |
| `payload`    | object            | Tool-specific structured output                      |
| `errors`     | array             | Normalized runtime errors                            |
| `meta`       | object            | Schema version, timestamp, debug/dry-run flags       |

---

## Canonical Enums

### verdict (6 values only)

```
SEAL        — entropy minimized; stage successful (non-terminal)
PROVISIONAL — unstable equilibrium; hypothesis under evaluation (non-terminal)
PARTIAL     — incomplete but usable (non-terminal)
SABAR       — metastable; pause / needs more context (non-terminal)
HOLD        — waiting for authority or human approval (non-terminal)
VOID        — entropy collapse; hard rejection (TERMINAL — extremely rare)
```

**separation of concerns:**

```
verdict = governance / constitutional meaning
status  = transport / runtime meaning

Never mix them.
```

### status (4 values only)

```
SUCCESS   — tool completed normally
ERROR     — runtime error occurred
TIMEOUT   — operation timed out
DRY_RUN   — no side effects committed
```

---

## metrics Block

All numeric telemetry is unified here.  
Nothing lives separately in `score_delta`, `telemetry.truth`, `vitality_index`, etc.

| Key             | Meaning                          | Range          |
|-----------------|----------------------------------|----------------|
| `truth`         | Epistemic fidelity (τ)           | [0.0, 1.0]     |
| `clarity_delta` | Confusion reduction (Δclarity)   | [-1.0, +1.0]   |
| `confidence`    | Current confidence (G)           | [0.0, 1.0]     |
| `peace`         | Stability score (P²)             | [0.0, 2.0]     |
| `vitality`      | Overall metabolic health (Ψ)     | [0.0, 10.0]    |
| `entropy_delta` | Thermodynamic delta (ΔS)         | [-1.0, +1.0]   |
| `authority`     | Authority continuity score        | [0.0, 1.0]     |
| `risk`          | Action / consequence risk         | [0.0, 1.0]     |

All fields are optional — emit only what your stage computes.  
Do not fabricate values (F2: Truth floor).

---

## trace Block

One trace only.  Records the actual pipeline path traveled.

```json
{
  "000_INIT": "SEAL",
  "111_SENSE": "SEAL",
  "222_REALITY": "PARTIAL",
  "333_MIND": "PROVISIONAL",
  "555_HEART": "SEAL",
  "666_CRITIQUE": "PARTIAL",
  "777_FORGE": "HOLD",
  "888_JUDGE": "HOLD"
}
```

**Rules:**
- One verdict per stage key
- Only executed stages appear (no nulls)
- No `data.trace` duplication
- No `phase2_hooks` in production output

---

## authority Block

```json
{
  "actor_id": "arif",
  "level": "human",
  "human_required": false,
  "approval_scope": ["forge", "seal"],
  "auth_state": "verified"
}
```

**Exposed in production:**  
`actor_id`, `level`, `human_required`, `approval_scope`, `auth_state`

**NOT exposed (archive/security layer only):**  
token fingerprint, nonce, signature blob, iat/exp

---

## errors Block

All runtime errors go here.  Never inside `payload`.

```json
[
  {
    "code": "IMPORT_ERROR",
    "message": "cannot import name 'get_session_manager'",
    "stage": "777_FORGE",
    "recoverable": true
  }
]
```

---

## meta Block

```json
{
  "schema_version": "1.0.0",
  "timestamp": "2026-03-10T12:00:00Z",
  "debug": false,
  "dry_run": false
}
```

Schema/admin metadata only.  No domain logic here.

---

## Production vs Debug Contract

**Production output** — the 12 canonical fields only.

**Debug output** — may append `debug` block when `meta.debug == true`:

```json
{
  "debug": {
    "reasoning": {},
    "witness": {},
    "raw_engine": {},
    "contradictions": [],
    "assumptions": []
  }
}
```

`debug` MUST NOT appear unless explicitly requested.

---

## Verdict Contract (Stage Rules)

```
if stage < 888_JUDGE and verdict == VOID → normalize to SABAR
```

Only `000_INIT` (auth failures) and `888_JUDGE` may emit `VOID`.

### By tool class

**Exploratory tools** (`reason_mind`, `vector_memory`, `search_reality`, `ingest_evidence`, `anchor_session`):

```
Allowed:  SEAL, PROVISIONAL, PARTIAL, SABAR
Forbidden: VOID (→ normalized to SABAR)
```

**Safety / alignment tools** (`simulate_heart`, `critique_thought`, `audit_rules`):

```
Allowed:  SEAL, PARTIAL, SABAR, HOLD
Forbidden: VOID (→ normalized to SABAR)
```

**Commitment / action tools** (`apex_judge`, `eureka_forge`, `seal_vault`):

```
Allowed:  SEAL, HOLD, VOID, SABAR
(real rejection is legal here)
```

---

## Tool Payload Schemas

### anchor_session
```json
{ "state": "active", "grounding_required": true }
```

### reason_mind
```json
{
  "reasoning_status": "exploratory",
  "confidence_band": "PLAUSIBLE",
  "needs_grounding": true,
  "next_stage": "666_CRITIQUE",
  "hypotheses": [{ "path": "conservative", "band": "CLAIM", "confidence": 0.91, "hypothesis": "..." }]
}
```

### vector_memory
```json
{ "matches": [{ "id": "mem_001", "score": 0.88, "source": "vault", "summary": "..." }], "count": 1 }
```

### simulate_heart
```json
{ "stakeholder_status": "safe", "stakeholders": [{ "name": "user", "impact": "low", "risk": 0.12 }], "needs_human_review": false }
```

### critique_thought
```json
{ "critique_status": "challenged", "weaknesses": ["missing grounding"], "contradictions": [], "recommendation": "refine" }
```

### apex_judge
```json
{ "judgment": "HOLD", "human_decision_required": true, "governance_token": "HOLD:abc123", "lawful": false }
```

### eureka_forge
```json
{ "execution_status": "blocked", "command": "...", "working_dir": "/root", "approval_required": true }
```

### seal_vault
```json
{ "sealed": true, "vault_ref": "vault_999_abc", "summary_hash": "sha256:..." }
```

### search_reality
```json
{ "grounding_status": "partial", "results": [{ "title": "...", "url": "...", "source": "brave", "score": 0.82 }], "results_count": 1 }
```

### ingest_evidence
```json
{ "source_type": "file", "target": "/path/doc.md", "mode": "summary", "content": "...", "truncated": false }
```

### audit_rules
```json
{ "audit_scope": "quick", "floors_checked": ["F2", "F4", "F7"], "violations": [], "passed": true }
```

### check_vital
```json
{ "cpu": 0.21, "memory": 0.43, "swap": 0.02, "io": null, "temp": null }
```

### metabolic_loop / arifOS.kernel
```json
{ "loop_status": "active", "current_stage": "333_MIND", "next_stage": "555_HEART", "completed_stages": ["000_INIT", "111_SENSE", "222_REALITY"] }
```

---

## Fields Removed from Old RuntimeEnvelope

| Removed Field       | Disposition                                  |
|---------------------|----------------------------------------------|
| `final_verdict`     | Duplicate of `verdict` — removed             |
| `telemetry`         | Merged into `metrics`                        |
| `score_delta`       | Merged into `metrics`                        |
| `witness`           | Archived → `debug.witness` only              |
| `philosophy`        | Archived → Vault / debug only                |
| `opex`              | Archived → `debug.raw_engine` only           |
| `apex`              | Archived → `debug.raw_engine` only           |
| `auth_context`      | Merged into `authority`                      |
| `token_fingerprint` | Security layer — not in production output    |
| `data`              | Renamed to `payload`                         |
| `counterfactual`    | Archived → debug block                       |
| `phase2_hooks`      | Internal — not public API                    |
| `data.trace`        | Duplicated; use top-level `trace` only       |

---

## Migration Table

| Old Field                 | New Location                    |
|---------------------------|---------------------------------|
| `verdict`                 | `verdict` (unchanged)           |
| `final_verdict`           | `verdict` (deduplicated)        |
| `telemetry.dS`            | `metrics.entropy_delta`         |
| `telemetry.peace2`        | `metrics.peace`                 |
| `telemetry.confidence`    | `metrics.confidence`            |
| `score_delta.truth`       | `metrics.truth`                 |
| `score_delta.clarity`     | `metrics.clarity_delta`         |
| `auth_context.actor_id`   | `authority.actor_id`            |
| `auth_context.level`      | `authority.level`               |
| `auth_state`              | `authority.auth_state`          |
| `data.*`                  | `payload.*`                     |
| `data.trace`              | `trace` (top-level)             |
| `failure_origin`          | `errors[].stage`                |
| `primary_blocker`         | `errors[].message`              |
| `philosophy`              | archived (not in production)    |
| `witness`                 | archived (debug only)           |

---

## Python Usage

```python
from core.schema import ArifOSOutput, Verdict, Status, Stage, Metrics, Trace, Authority
from core.schema import VerdictValidator, SchemaError, Meta
from arifosmcp.runtime.schema import ReasonMindPayload, Hypothesis

# Build a canonical output
output = ArifOSOutput(
    tool="reason_mind",
    session_id="sess_123",
    stage=Stage.MIND.value,
    verdict=Verdict.PROVISIONAL,
    status=Status.SUCCESS,
    metrics=Metrics(truth=0.82, confidence=0.72, entropy_delta=-0.08),
    trace=Trace.from_dict({"000_INIT": "SEAL", "333_MIND": "PROVISIONAL"}),
    authority=Authority(actor_id="arif", level="human", auth_state="verified"),
    payload=ReasonMindPayload(
        reasoning_status="exploratory",
        confidence_band="PLAUSIBLE",
    ).model_dump(),
)

# Enforce verdict contract before returning
normalized_verdict = VerdictValidator.validate("reason_mind", Stage.MIND, Verdict.VOID)
# → Verdict.SABAR (exploratory tools cannot emit VOID)

# Serialize for production (debug stripped, canonical trace keys)
response = output.to_production()
```

---

## Schema Files

```
core/
└── schema/
    ├── __init__.py       # Public exports
    ├── stage.py          # Stage enum + stage_weight()
    ├── verdict.py        # Verdict + Status enums + tool classifications
    ├── metrics.py        # Metrics schema
    ├── trace.py          # Trace schema + from_dict() builder
    ├── authority.py      # Authority schema
    ├── errors.py         # SchemaError schema
    ├── meta.py           # Meta + DebugBlock schemas
    ├── output.py         # ArifOSOutput canonical envelope
    └── validator.py      # VerdictValidator contract enforcement

arifosmcp/
└── runtime/
    └── schema/
        ├── __init__.py   # Public exports
        └── payloads.py   # Tool-specific payload schemas + TOOL_PAYLOAD_REGISTRY

tests/
└── schema/
    ├── __init__.py
    ├── test_output.py    # Envelope, metrics, trace, authority, error, meta, serialization tests
    ├── test_validator.py # Verdict contract enforcement tests
    └── test_payloads.py  # Tool payload schema tests
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given 🔥
