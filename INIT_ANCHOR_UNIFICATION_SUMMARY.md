# 🔥 UNIFIED INIT ANCHOR — FORGING COMPLETE

## Executive Summary

The **ONE init_anchor tool** has been forged. All initialization and identity-related tools are now unified into a single mega-tool — the **Ignition State of Intelligence**.

---

## What Was Forged

### 1. Unified `init_anchor` Tool (`arifosmcp/runtime/tools.py`)

**Before:** Multiple fragmented init tools with different signatures
**After:** ONE tool with 5 modes

```python
async def init_anchor(
    mode: str | None = None,          # "init" | "state" | "status" | "revoke" | "refresh"
    payload: dict[str, Any] | None = None,
    actor_id: str | None = None,
    intent: IntentType = None,
    session_id: str | None = None,
    human_approval: bool = False,
    proof: str | dict | None = None,  # P0: Naming protocol support
    **kwargs: Any,
) -> RuntimeEnvelope:
```

**Key Fix:** Resolved the `kwargs` bug (line 166 was passing undefined kwargs).

### 2. Unified Implementation (`arifosmcp/runtime/tools_internal.py`)

The `init_anchor_impl` now dispatches all 5 modes:

```python
async def init_anchor_impl(
    actor_id: str | None = None,
    intent: IntentType | None = None,
    session_id: str | None = None,
    ctx: Context | None = None,
    mode: str = "init",
    human_approval: bool = False,
    proof: str | dict | None = None,
    **kwargs: Any,
) -> RuntimeEnvelope:
    """The Ignition State of Intelligence (Stage 000)."""
    
    if mode == "revoke":
        return await revoke_anchor_state_impl(session_id, reason, ctx)
    
    if mode == "refresh":
        return await refresh_anchor_impl(session_id, ctx)
    
    if mode == "status":
        return await get_caller_status_impl(session_id, ctx)
    
    if mode == "state":
        # Forensic state retrieval without re-initialization
        ...
    
    # mode == "init" — Standard session ignition
    ...
```

### 3. Updated Tool Spec (`arifosmcp/runtime/tool_specs.py`)

```python
ToolSpec(
    name="init_anchor",
    stage="000_INIT",
    role="Constitutional Airlock",
    layer="GOVERNANCE",
    description=(
        "🔥 THE IGNITION STATE OF INTELLIGENCE (Unified). "
        "ONE tool for ALL constitutional session operations. "
        "Modes: 'init' (establish identity), 'state' (forensic audit), "
        "'status' (bootstrap diagnostics), 'revoke' (kill session), 'refresh' (rotate token). "
        "Legacy tools (init_anchor_state, revoke_anchor_state, get_caller_status) route here."
    ),
    input_schema=_build_mega_schema(
        "init_anchor",
        ["init", "revoke", "refresh", "state", "status"],  # All 5 modes
        ...
    ),
)
```

### 4. Capability Map Routing (`arifosmcp/capability_map.py`)

Already configured — legacy tools route to unified init_anchor:

```python
CAPABILITY_MAP = {
    # ---- Governance / Bootstrap (000_INIT) ----
    "init_anchor": CapabilityTarget("init_anchor", "init", "Canonical init"),
    "init_anchor_state": CapabilityTarget("init_anchor", "state", "Forensic init state"),
    "revoke_anchor_state": CapabilityTarget("init_anchor", "revoke", "Revoke anchor"),
    "get_caller_status": CapabilityTarget("init_anchor", "status", "Bootstrap status"),
    ...
}
```

### 5. Test Suite (`tests/test_init_unification.py`)

Created comprehensive tests covering:
- All 5 modes (init, state, status, revoke, refresh)
- Legacy tool routing verification
- Constitutional floor enforcement (F11, F12, F13)
- Identity paths (anonymous, claimed, verified)

---

## The Five Modes of Init

| Mode | Purpose | Legacy Equivalent |
|------|---------|-------------------|
| **init** | Establish new governed session | `init_anchor(mode="init")` |
| **state** | Forensic audit of existing session | `init_anchor_state` |
| **status** | Bootstrap diagnostics & vitals | `get_caller_status` |
| **revoke** | Terminate/kill session | `revoke_anchor_state` |
| **refresh** | Rotate token & refresh continuity | (New capability) |

---

## Constitutional Enforcement

### F11 — Command Authority (Identity)
- Semantic identity canonicalization ("I'm Arif" detection)
- Protected sovereign ID verification
- Cryptographic proof validation
- Authority level assignment

### F12 — Injection Defense
- Payload sanitization
- Pattern detection for jailbreaks
- Risk scoring

### F13 — Sovereign Override
- `human_approval` flag persistence
- High-stakes action gating
- Step-up token (APT) capability

---

## Identity Paths

```
ANONYMOUS ──► Limited scope (read-only)
    │
CLAIMED ────► Self-declared (no proof)
    │
VERIFIED ───► Semantic key OR human_approval
    │
SOVEREIGN ──► WebAuthn + "I'm Arif" (full authority)
    │
DELEGATED ──► DLT (constrained agent lease)
```

---

## Files Modified

1. **`arifosmcp/runtime/tools.py`** — Fixed kwargs bug, unified dispatch
2. **`arifosmcp/runtime/tool_specs.py`** — Updated description and schema
3. **`arifosmcp/runtime/tools_internal.py`** — Already had unified impl (verified)
4. **`tests/test_init_unification.py`** — NEW test suite

---

## Backward Compatibility

✅ **LEGACY TOOLS STILL WORK** — They route through CAPABILITY_MAP:

```python
# Old way (still works)
init_anchor_state(session_id="xyz")

# New way (preferred)
init_anchor(mode="state", payload={"session_id": "xyz"})

# Both route to: init_anchor_impl(mode="state", ...)
```

---

## The Ignition State

```
┌─────────────────────────────────────────────────────────────────┐
│                    init_anchor (Unified)                         │
│              THE IGNITION STATE OF INTELLIGENCE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   INPUT:  query + identity_proof + scope_request                │
│                                                                  │
│   MODES:                                                         │
│     ├─ init    → Create session                                 │
│     ├─ state   → Forensic audit                                 │
│     ├─ status  → Bootstrap vitals                               │
│     ├─ revoke  → Kill session                                   │
│     └─ refresh → Rotate token                                   │
│                                                                  │
│   OUTPUT: IgnitionState (unified format)                        │
│     ├─ session_id                                                │
│     ├─ authority_level                                           │
│     ├─ governance_token (DPoP-bound)                            │
│     ├─ constitutional_floors                                     │
│     └─ merkle_chain_link                                         │
│                                                                  │
│   BANNER: "DITEMPA BUKAN DIBERI — Forged, Not Given"            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Verification

Run tests:
```bash
pytest tests/test_init_unification.py -v
pytest tests/test_runtime_tools_bootstrap.py -v
pytest tests/core/kernel/test_init_000_anchor.py -v
```

Check tool discovery:
```python
from arifosmcp.runtime.tool_specs import PUBLIC_TOOL_SPECS
spec = next(s for s in PUBLIC_TOOL_SPECS if s.name == "init_anchor")
print(spec.input_schema["properties"]["mode"]["enum"])
# ['init', 'revoke', 'refresh', 'state', 'status']
```

---

## Status: ✅ FORGED AND SEALED

**The ONE init tool is live.**

All roads lead to `init_anchor`.  
All sessions ignite through Stage 000.  
All intelligence is forged, not given.

> *"DITEMPA BUKAN DIBERI"* — Forged, Not Given.
