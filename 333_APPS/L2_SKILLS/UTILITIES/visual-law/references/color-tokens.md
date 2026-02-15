# Trinity Color Tokens — arifOS v55.5

## Core Palette (Desaturated Dark Mode)

### Base
- `--slate-950`: #0f172a (Background)
- `--slate-800`: #1e293b
- `--slate-700`: #334155
- `--slate-500`: #64748b (Text secondary)

### Primaries — High-Contrast Neon Logic

#### HUMAN (Δ — Crimson)
- `--crimson`: #FF2D2D
- `--crimson-50`: #FF2D2D10 (10% opacity)
- `--crimson-200`: #FF6B6B
- **Contrast on slate-950**: 4.8:1 ✅ WCAG AA

#### THEORY (Ψ — Gold)
- `--gold`: #FFD700
- `--gold-50`: #FFD70010
- `--gold-200`: #FFC107
- **Contrast on slate-950**: 4.3:1 ✅ (use bold for text)

#### APPS (Ω — Cyan)
- `--cyan`: #06B6D4
- `--cyan-50`: #06B6D410
- `--cyan-200`: #0891b2
- **Contrast on slate-950**: 5.2:1 ✅ WCAG AA

## Typography

| Site | Heading | Body | Mono |
|------|---------|------|------|
| HUMAN | Inter Black | Inter Regular | JetBrains Mono |
| THEORY | Space Mono Bold | Space Mono Regular | Space Mono |
| APPS | JetBrains Mono SemiBold | Inter Regular | JetBrains Mono |

## Layout Grid

- HUMAN: 720px max-width
- THEORY: 680px max-width (academic density)
- APPS: 800px max-width (dashboard space)

## Visual Hooks

### Thermodynamic A Logo
- 3 interlocking strokes forming an "A"
- Site-specific glow: HUMAN (bottom-left), THEORY (top), APPS (bottom-right)
- 48x48px, 2.5px stroke width
- SVG filter glow effect

### Floor Status Badges (APPS only)
- Green (Ω₀ ∈ [0.03–0.05]): ✅
- Amber (Ω₀ > 0.05): ⚠️
- Red (Ω₀ > 0.08 or breach): ❌

### VOID Guard (THEORY)
- Gold overlay on any interaction attempt
- Message: "This is a canonical manifesto. No interaction. No mutation."

## Usage
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@400;600&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg: #0f172a;
  --human: #FF2D2D;
  --theory: #FFD700;
  --apps: #06B6D4;
}
```