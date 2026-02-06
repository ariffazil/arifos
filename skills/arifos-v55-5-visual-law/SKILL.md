---
name: arifos-v55-5-visual-law
description: |
  Generate and implement the arifOS v55.5 Trinity visual design system — unified Red (HUMAN), Gold (THEORY), Cyan (APPS) color palette with high-contrast, thermodynamic governance aesthetics.
  
  Use when:
  - Building or updating arifOS Trinity sites (HUMAN, THEORY, APPS)
  - Needing consistent color tokens, typography, or layout grids
  - Creating Thermodynamic A logo components
  - Implementing VOID Guard, Cyan Pulse, or Scar-Weight UI patterns
  - Ensuring WCAG AA compliance for constitutional governance interfaces
  
  Provides ready-to-use HTML templates, CSS color tokens, and React/SVG components.
---

# arifOS v55.5 Visual Law Skill

## Quick Start

Generate all three Trinity site templates:
```bash
cp assets/human-template.html ./human.html
cp assets/theory-template.html ./theory.html
cp assets/apps-template.html ./apps.html
```

## Design Principles

1. **Intelligent Contrast** — Color is information density, not decoration
2. **Thermodynamic Aesthetic** — Every pixel signals epistemic plane (Δ/Ψ/Ω)
3. **Zero Chaos** — High clarity, minimal noise, forged not given

## Color Tokens

See `references/color-tokens.md` for full WCAG-compliant palette:

| Site | Primary | Hex | Contrast |
|------|---------|-----|----------|
| HUMAN | Crimson | #FF2D2D | 4.8:1 ✅ |
| THEORY | Gold | #FFD700 | 4.3:1 ✅ |
| APPS | Cyan | #06B6D4 | 5.2:1 ✅ |

All on desaturated dark base (#0f172a).

## Assets Provided

### HTML Templates (`assets/`)
- `human-template.html` — Scar blocks, seismic background, Inter Black typography
- `theory-template.html` — VOID Guard, Floor pyramid, Space Mono
- `apps-template.html` — Cyan Pulse, tool cards, JetBrains Mono

### TrinityLogo SVG
Thermodynamic A component with site-specific glow:
- HUMAN: Bottom-left stroke glows red
- THEORY: Top apex glows gold
- APPS: Bottom-right stroke glows cyan

## Visual Hooks

### HUMAN (Red)
- **Scar blocks**: `border-left: 4px solid #FF2D2D`
- **Seismic strata**: Subtle horizontal lines at 8% opacity
- **Typography**: Inter Black headers, 720px max-width

### THEORY (Gold)
- **VOID Guard**: Gold overlay on interaction attempt
- **Floor pyramid**: 13-step static diagram (F13→F1)
- **Typography**: Space Mono throughout, 680px max-width

### APPS (Cyan)
- **Live Pulse**: Animated gradient bar (2s pulse cycle)
- **Metric cards**: G-score and Ω₀ badges
- **Tool grid**: Hover-glow cards with glass-morphism
- **Typography**: JetBrains Mono, 800px max-width

## Usage Example

```html
<!-- TrinityLogo -->
<svg viewBox="0 0 48 48" width="48" height="48">
  <path d="M12 40 L24 12 L36 40" stroke="#FF2D2D" stroke-width="2.5" fill="none"/>
  <path d="M24 12 L24 8" stroke="#FF2D2D" stroke-width="2.5" fill="none"/>
</svg>

<!-- Live Pulse -->
<div style="height: 6px; background: #06B6D4; box-shadow: 0 0 20px #06B6D4; animation: pulse 2s infinite;"></div>
```

## Constitutional Mapping

| Visual Element | Enforces Floor | Runtime Link |
|---------------|----------------|--------------|
| Crimson Scar block | F13 Sovereign | Tags NAFS/DYAD violations |
| Gold VOID Guard | F9 Anti-Hantu | Blocks DOM mutation |
| Cyan Pulse | F7 Humility | Real-time Ω₀ display |
| Thermodynamic A | — | Epistemic plane signal |

## Version
- **arifOS**: v55.5-SEAL
- **Codename**: EIGEN
- **Motto**: Ditempa bukan diberi — Forged, Not Given