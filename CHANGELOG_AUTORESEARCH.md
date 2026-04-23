# arifOS Autoresearch — CHANGELOG

**Date:** 2026-04-22  
**Branch:** `autoresearch/2026-04-22`

---

## Experiments Log

| Exp | Description | Score Before | Score After | Decision | Notes |
|------|-------------|-------------|-------------|----------|-------|
| baseline | Initial harness run — no mutations | 53.0 | — | baseline | A=PASS, B=PASS, C=ERROR, D=FAIL, E=FAIL |
| exp-001 | Fix C (remove bad kwargs), E (expect VOID), D (add tri-witness mode) | 53.0 | 63.0 | ✅ accepted | +10 points. C still returns CLAIM_ONLY not VOID. D still CLAIM_ONLY not HOLD. |

---

## Key Findings

- **arifos_444_kernel**: Does not independently return VOID for bad claims. Floor F9 enforcement happens in `constitutional_guard` middleware, not in the tool itself. The tool returns CLAIM_ONLY.
- **arifos_222_witness**: Returns CLAIM_ONLY even with tri-witness mode and no evidence. Floor F2 enforcement (HOLD for unverifiable claims) happens in `constitutional_guard` middleware, not the tool itself.
- **arifos_999_vault**: Correctly returns VOID for unauthorized read actions. Expected verdict for scenario E should be VOID, not HOLD.

---

## Architecture Note

The floor enforcement (F1–F13) is in `arifos/core/middleware/constitutional_guard.py`, NOT in the individual MCP tool implementations. MCP tools emit CLAIM_ONLY by default. The constitutional_guard middleware intercepts and converts to SEAL/HOLD/VOID based on metrics.

This means the E2E test harness needs to test through the full governance pipeline, not individual tools. The arifos_train.py harness is the correct approach (it tests the full pipeline).

---

**DITEMPA BUKAN DIBERI — Testing is forged, not assumed.**
