# Claim Tagging System — Epistemic Grounding

**Parent:** [[70_GOVERNANCE/Seals_and_Verdicts]]
**Floor:** F2 Truth | F7 Humility | F11 Auditability
**Epoch:** 2026-04-09

---

## 1. Overview

In GEOX, no statement is accepted as "Fact" without a declared proximity to source evidence. The Claim Tagging system forces the AI to declare the epistemic status of every subsurface assertion.

---

## 2. Taxonomy

| Tag | Meaning | Threshold / Basis |
| :--- | :--- | :--- |
| **CLAIM** | Verified Fact | Direct physical observation or Archie model on clean sand ($V_{cl} < 10\%$). |
| **PLAUSIBLE** | Probable | Supported by shaly-sand models or regional trends in calibrated basins. |
| **HYPOTHESIS** | Speculative | No direct well control; uncalibrated $R_w$; high $V_{cl} (> 40\%)$. |
| **UNKNOWN** | Missing | No data; parity between competing models. |

---

## 3. Governance Automata

The `geox_mcp_server.py` automatically injects these tags into the `meta` field of tool results.

- **F7 Veto**: If the AI attempts to present a **HYPOTHESIS** as a **CLAIM**, the system raises a constitutional warning.
- **888_HOLD**: Any **HYPOTHESIS** or **UNKNOWN** status in a critical prospect verdict triggers a mandatory HOLD for human witness.

---

## 4. 888_HOLD Examples

- $S_w > 1.0$ (Unphysical contrast).
- Vertical exaggeration $> 2\times$ undisclosed.
- Fault geometry not seismic-constrained.
- Interval of interest has zero well control.

---

**Audit Reference:** `VOID_20260409_074829`
