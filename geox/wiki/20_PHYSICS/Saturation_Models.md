# Saturation Models — Physical Governing Equations

**Parent:** [[20_PHYSICS/EARTH_CANON_9]]
**Status:** ✅ HARDENED · Phase B
**Epoch:** 2026-04-09

---

## 1. Overview

Water saturation ($S_w$) is the most critical derived variable in GEOX petrophysics. It determines the prospectivity of a formation. GEOX implements a multi-model approach to handle varying rock types and clay distributions.

---

## 2. Canonical Models

### 2.1 Archie (1942) — Clean Formations

Used for clean, non-conductive matrix sands.

$$S_w = \sqrt[n]{\frac{a \cdot R_w}{\Phi^m \cdot R_t}}$$

- **Assumption**: All conductivity is via the pore water.
- **Veto Condition**: $V_{cl} > 15\%$ triggers a switch to Simandoux or Indonesia.

### 2.2 Simandoux (1963) — Dispersed Shaly Sands

Corrects for conductive clay minerals.

$$\frac{1}{R_t} = \frac{\Phi^m \cdot S_w^{n}}{a \cdot R_w \cdot (1 - V_{cl})} + \frac{V_{cl} \cdot S_w}{R_{sh}}$$

- **Assumption**: Clay is dispersed within the pore space.

### 2.3 Indonesia (Poupon & Leveaux, 1971) — Complex/Laminated

Optimized for the low-resistivity pay zones common in SE Asian basins (e.g., Malay Basin).

$$\frac{1}{\sqrt{R_t}} = \left[ \frac{V_{cl}^{(1 - 0.5V_{cl})}}{\sqrt{R_{sh}}} + \frac{\Phi^{m/2}}{\sqrt{a \cdot R_w}} \right] \cdot S_w^{n/2}$$

---

## 3. Epistemic Claim Tagging

Saturation results are automatically tagged based on formation quality:

- **CLAIM**: Archie on clean sand ($V_{cl} < 10\%$).
- **PLAUSIBLE**: Shaly sand models in calibrated intervals.
- **HYPOTHESIS**: High $V_{cl} (> 40\%)$ or uncalibrated $R_w$.

---

## 4. Uncertainty Propagation (F7 Humility)

Every $S_w$ result must be accompanied by a P10-P90 confidence band derived from a **Monte Carlo Engine** ($n=1000$).

- **Veto Gate (F13)**: Zero uncertainty is prohibited.
- **888_HOLD**: $S_w > 1.0$ (unphysical) or $S_w < 0.0$ triggers an immediate halt.

---

**Audit Reference:** `VOID_20260409_074829`
