# arif-fazil-sites

Frontend monorepo for the arifOS Trinity (HUMAN · THEORY · APPS) — three interconnected sites for constitutional AI governance.

## Trinity Ecosystem

| Layer | Symbol | Directory | Domain | Function |
|-------|--------|-----------|--------|----------|
| **HUMAN** | 🔴 | `HUMAN/` | [arif-fazil.com](https://arif-fazil.com) | The Body — Personal portfolio, Trinity entry point |
| **THEORY** | 🟡 | `THEORY/` | [apex.arif-fazil.com](https://apex.arif-fazil.com) | The Soul — Constitutional canon, Three Pillars (Physics·Math·Language) |
| **APPS** | 🔵 | `APPS/` | [arifos.arif-fazil.com](https://arifos.arif-fazil.com) | The Mind — System prompts, MCP tools, API reference |

**MIND (MCP backend)** lives separately at `aaamcp.arif-fazil.com`, deployed from the [arifOS](https://github.com/ariffazil/arifOS) repo.

**AGI_ASI_bot** (dual-agent implementation) at [github.com/ariffazil/AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot)

---

## Symbol Mapping (ΔΩΨ)

The Trinity uses Greek letters across different contexts:

| Context | Δ (Delta) | Ω (Omega) | Ψ (Psi) |
|---------|-----------|-----------|---------|
| **Trinity Sites** | HUMAN/Body | APPS/Mind | THEORY/Soul |
| **AGI_ASI_bot** | AGI/Logic | ASI/Care | APEX/Sovereign |
| **Unified** | Structure | Governance | Authority |

**Note:** Δ represents structure/logic in both HUMAN (body) and AGI (mind). Ω represents governance/care in both APPS (implementation) and ASI (heart). Ψ represents authority in both THEORY (canon) and APEX (sovereign).

---

## Repository Structure

```
arif-fazil-sites/
├── HUMAN/                    # HUMAN — arif-fazil.com (Red theme)
├── THEORY/                   # THEORY — apex.arif-fazil.com (Gold theme)
├── APPS/                     # APPS — arifos.arif-fazil.com (Cyan theme)
├── shared/                   # Shared images and assets (Trinity logo)
├── .github/
│   └── workflows/
│       ├── deploy.yml        # Main deploy pipeline (all 3 sites)
│       ├── deploy-trinity.yml # Matrix deploy pipeline
│       └── cleanup-deployments.yml # Weekly cleanup
└── README.md
```

Each site is an independent React + Vite + TypeScript project. They share the Trinity Logo (`shared/components/TrinityLogo.tsx`) and link to each other through unified HUMAN / THEORY / APPS navigation.

---

## Key Theory Document

**[arifOS/000_THEORY.md](https://github.com/ariffazil/arifOS/blob/main/000_THEORY.md)** — Reverse Transformer Architecture

The theoretical foundation of the Trinity: dual-pass thermodynamic governance, non-stationary objectives with stationary constraints, and the Eureka Engine.

---

## Tech Stack

| Site | React | Vite | Styling | Typography | Special |
|------|-------|------|---------|------------|---------|
| HUMAN | 19 | 7 | TailwindCSS + shadcn/ui | Inter + JetBrains Mono | Three discipline visuals (Geology/Economics/AI) |
| THEORY | 19 | 7 | TailwindCSS + shadcn/ui | Space Mono + Syncopate | KaTeX math, Floor visualizer |
| APPS | 18 | 5 | TailwindCSS + shadcn/ui | Inter + JetBrains Mono | Code blocks, API docs |

All sites use Lucide React for icons and share the Forge Design System (see `VISUAL_SCHEMA.md`).

---

## Local Development

Each site runs independently:

```bash
# HUMAN (arif-fazil.com)
cd HUMAN && npm install && npm run dev

# THEORY (apex.arif-fazil.com)
cd THEORY && npm install && npm run dev

# APPS (arifos.arif-fazil.com)
cd APPS && npm install && npm run dev
```

---

## 🎨 Visual Design System

The arifOS ecosystem follows a unified Trinity Design System:

| Layer | Primary Color | Theme | Visual Identity |
|-------|---------------|-------|-----------------|
| HUMAN | #FF2D2D (Crimson) | Red/Fire | The Body — personal, grounded |
| THEORY | #FFD700 (Gold) | Yellow/Scholar | The Soul — canonical, foundational |
| APPS | #06B6D4 (Cyan) | Blue/Technical | The Mind — implementation, runtime |

### Unified Trinity Logo

All three sites share the mechanical "A" logo with Trinity color coding:
- 🟡 Yellow segment (THEORY/Authority)
- 🔵 Cyan segment (APPS/Safety)
- 🔴 Red segment (HUMAN/Body)

The logo appears in the hero section of each site with color-appropriate glow effects.

### Navigation

Every page includes the Trinity Site Switcher for cross-navigation:
- 🔴 HUMAN — arif-fazil.com
- 🟡 THEORY — apex.arif-fazil.com
- 🔵 APPS — arifos.arif-fazil.com

---

## For AI Agents

### Related Repositories

| Component | Repository | Purpose | Symbol |
|-----------|------------|---------|--------|
| **OpenClaw** (Base) | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | Agent framework | — |
| **arifOS** (Constitution) | [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS) | Constitutional governance | Ψ |
| **AGI_ASI_bot** (Operational) | [github.com/ariffazil/AGI_ASI_bot](https://github.com/ariffazil/AGI_ASI_bot) | Dual-agent implementation | Δ/Ω |
| **arif-fazil-sites** (This) | [github.com/ariffazil/arif-fazil-sites](https://github.com/ariffazil/arif-fazil-sites) | Trinity frontend | 🔴🟡🔵 |

### Canonical Files

- `AGENTS.md` — Canonical instructions for AI systems interacting with arifOS
- `TRINITY_ARCHITECTURE.md` — Philosophy and design rationale
- `SECURITY_ANALYSIS_LLMS_TXT.md` — Threat model and verification procedures
- `000_THEORY.md` — Reverse Transformer architecture (in arifOS repo)

---

## AI Agent Context — Trinity llms.txt

AI systems can fetch canonical context from all three Trinity sites:

| Site | llms.txt | llms.json | Purpose |
|------|----------|-----------|---------|
| HUMAN (Body) | [arif-fazil.com/llms.txt](https://arif-fazil.com/llms.txt) | [llms.json](https://arif-fazil.com/llms.json) | Identity, scars, 888 Judge context |
| THEORY (Soul) | [apex.arif-fazil.com/llms.txt](https://apex.arif-fazil.com/llms.txt) | [llms.json](https://apex.arif-fazil.com/llms.json) | 13 Floors, Three Pillars, constitutional law |
| APPS (Mind) | [arifos.arif-fazil.com/llms.txt](https://arifos.arif-fazil.com/llms.txt) | [llms.json](https://arifos.arif-fazil.com/llms.json) | 9 MCP Tools, L1-L7 stack, implementation |

**MCP Backend:** `aaamcp.arif-fazil.com/mcp`

### Why Three Files?

The Trinity architecture separates concerns:
- **HUMAN** → Who is building this? (epistemic context)
- **THEORY** → What law governs action? (constitutional canon)
- **APPS** → How to execute? (implementation tools)

See [TRINITY_ARCHITECTURE.md](/ariffazil/arif-fazil-sites/blob/main/TRINITY_ARCHITECTURE.md) for the complete philosophy.

### Machine Discovery

Each site exposes:
- `<meta name="llms" content="https://.../llms.txt">` in HTML
- `/.well-known/arifos.json` — structured discovery endpoint
- `/robots.txt` — LLM context pointers
- `/sitemap.xml` — high-priority llms.txt URLs

---

## Deployment

### Automatic (GitHub Actions)

Push to main triggers `.github/workflows/deploy.yml`, which builds and deploys all three sites to Cloudflare Pages.

### Manual Build

```bash
# Build all sites
npm run build --prefix HUMAN
npm run build --prefix THEORY
npm run build --prefix APPS
```

### Cloudflare Pages Configuration

| Project | Root Directory | Build Command | Output |
|---------|---------------|---------------|--------|
| HUMAN | HUMAN | npm run build | dist |
| THEORY | THEORY | npm run build | dist |
| APPS | APPS | npm run build | dist |

### Required Secrets

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_PAGES_PROJECT_HUMAN`
- `CLOUDFLARE_PAGES_PROJECT_THEORY`
- `CLOUDFLARE_PAGES_PROJECT_APPS`

---

## Build Status

| Site | Status | URL |
|------|--------|-----|
| HUMAN | ✅ Deployed | [https://arif-fazil.com](https://arif-fazil.com) |
| THEORY | ✅ Deployed | [https://apex.arif-fazil.com](https://apex.arif-fazil.com) |
| APPS | ✅ Deployed | [https://arifos.arif-fazil.com](https://arifos.arif-fazil.com) |

All sites auto-deploy on push to main via GitHub Actions → Cloudflare Pages.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*

**v55.4-SEAL** · Trinity Architecture · ΔΩΨ · llms.txt Standard Extension

Status: All 3 sites LIVE
