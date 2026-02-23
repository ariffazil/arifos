---
name: arifos-visual-law
description: Trinity visual design system (v55.5) — Red (HUMAN), Gold (THEORY), Cyan (APPS) palette. Use for arifOS site theming, TrinityLogo components, VOID Guard UI.
metadata:
  arifos:
    version: 55.5
    site_colors:
      HUMAN: {primary: "#FF2D2D", base: "#0f172a", contrast: "4.8:1"}
      THEORY: {primary: "#FFD700", base: "#0f172a", contrast: "4.3:1"}
      APPS: {primary: "#06B6D4", base: "#0f172a", contrast: "5.2:1"}
---

# arifOS Visual Law

**Trinity Design System:** HUMAN (Red), THEORY (Gold), APPS (Cyan)

## Color Tokens

| Site | Primary | Hex | Contrast |
|------|---------|-----|----------|
| HUMAN | Crimson | #FF2D2D | 4.8:1 ✅ |
| THEORY | Gold | #FFD700 | 4.3:1 ✅ |
| APPS | Cyan | #06B6D4 | 5.2:1 ✅ |

Base: #0f172a (desaturated dark)

## Visual Hooks

**HUMAN (Red):**
- Scar blocks: `border-left: 4px solid #FF2D2D`
- Seismic strata: 8% opacity horizontal lines
- Font: Inter Black, 720px max-width

**THEORY (Gold):**
- VOID Guard: Gold overlay on interaction
- Floor pyramid: 13-step static diagram
- Font: Space Mono, 680px max-width

**APPS (Cyan):**
- Live Pulse: Animated gradient (2s cycle)
- Metric cards: G-score, Ω₀ badges
- Font: JetBrains Mono, 800px max-width

## TrinityLogo SVG

```html
<svg viewBox="0 0 48 48" width="48" height="48">
  <path d="M12 40 L24 12 L36 40" stroke="#FF2D2D" stroke-width="2.5" fill="none"/>
  <path d="M24 12 L24 8" stroke="#FF2D2D" stroke-width="2.5" fill="none"/>
</svg>
```

## Constitutional Mapping

| Visual | Floor | Function |
|--------|-------|----------|
| Crimson Scar | F13 | Sovereign indicator |
| Gold Guard | F9 | Anti-Hantu block |
| Cyan Pulse | F7 | Ω₀ real-time display |
| Thermodynamic A | — | Epistemic plane signal |
