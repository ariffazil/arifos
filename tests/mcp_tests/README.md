# MCP & Trinity Tests

**Scope:** The Interface & Tools
**Target:** `arifos.mcp.*`

This directory tests the **governance spine tools** exposed to external agents:

1.  **`anchor_session`**:
    *   Session ignition.
    *   Authority validation (F11).
    *   Injection defense (F12).

2.  **`reason_mind` (Mind)**:
    *   Reasoning chains (SENSE/THINK/ATLAS).
    *   Truth threshold verification (F2).

3.  **`simulate_heart` (Heart)**:
    *   Empathy checks (F6).
    *   Safety gates (F5 Peace²).

4.  **`apex_judge` (Soul)**:
    *   Final verdict rendering (SEAL/VOID).
    *   Cryptographic sealing checks.

5.  **`seal_vault`**:
    *   Immutable ledger writing.
    *   Audit trail verification.

**Key Command:**
```bash
pytest -m mcp
```

Alias compatibility expectations:
- `judge_soul` should resolve to `apex_judge`
- `forge_hand` should resolve to `eureka_forge`
