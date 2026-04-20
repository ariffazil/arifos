# Seismic Section Viewer — APP SPEC

> **DITEMPA BUKAN DIBERI**
> **Domain:** Seismic | **ID:** geox.seismic.viewer

## 1. Overview
Interactive visual mode for high-resolution seismic cross-sections. Enforces the Theory of Anomalous Contrast (ToAC).

## 2. Capabilities
- **Visual Transforms:** Multi-colormap support, vertical exaggeration, gain control.
- **Physical Grounding:** Vertical axis mapping (Time/Depth), borehole ties.
- **Governance:** Integrated `888_HOLD` overlay for unphysical interpretations.

## 3. Tool Requirements
- `geox_load_seismic_line`
- `geox_build_structural_candidates`

## 4. Event Strategy
- Emits `ui.action` on every contrast change.
- Emits `ui.state.sync` with current viewport depth.
- Subscribes to `app.context.patch` to focus on specific well-ties.

---

*Entry Point: arifos/geox/apps/seismic_viewer/index.html*
