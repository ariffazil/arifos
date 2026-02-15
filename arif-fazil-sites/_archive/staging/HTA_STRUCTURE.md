# HUMAN THEORY APPS Sites — Hardened Structure

> **Status**: v55.1-SEAL | **Last Updated**: 2026-02-02

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           HUMAN THEORY APPS ECOSYSTEM                                  │
├─────────────┬─────────────┬─────────────┬─────────────────────────────────────┤
│    BODY     │    SOUL     │    DOCS     │               MIND                  │
│  (Frontend) │  (Frontend) │  (Frontend) │            (Backend)                │
├─────────────┼─────────────┼─────────────┼─────────────────────────────────────┤
│arif-fazil.  │apex.arif-   │arifos.arif- │        aaamcp.arif-fazil.com        │
│com          │fazil.com    │fazil.com    │         (arifOS repo)               │
├─────────────┼─────────────┼─────────────┼─────────────────────────────────────┤
│Portfolio +  │Constitutional│API Docs +  │         MCP Server (Python)         │
│Dashboard    │Canon         │MCP Tools   │         FastAPI + Railway           │
├─────────────┼─────────────┼─────────────┼─────────────────────────────────────┤
│ React 19    │ React 19    │ React 18    │                                     │
│ Vite 7      │ Vite 7      │ Vite 5      │                                     │
│ Tailwind 3  │ Tailwind 3  │ Tailwind 3  │                                     │
│ + shadcn    │ + KaTeX     │ + shadcn    │                                     │
└─────────────┴─────────────┴─────────────┴─────────────────────────────────────┘
```

---

## Directory Structure

```
arif-fazil-sites/
│
├── body/                          # BODY (arif-fazil.com)
│   ├── src/
│   │   ├── App.tsx               # Main portfolio application
│   │   ├── main.tsx              # Entry point
│   │   ├── index.css             # Global styles
│   │   ├── components/ui/        # 50+ shadcn/ui components
│   │   ├── hooks/use-mobile.ts   # Mobile detection
│   │   └── lib/utils.ts          # cn() helper
│   ├── public/                   # Static assets
│   │   ├── *.jpg                 # Hero images
│   │   ├── llms.txt              # LLM bootstrap
│   │   ├── robots.txt            # SEO
│   │   ├── sitemap.xml           # SEO
│   │   └── _headers              # Cloudflare headers
│   ├── package.json              # React 19, Vite 7
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── THEORY/                        # THEORY (apex.arif-fazil.com)
│   ├── src/
│   │   ├── App.tsx               # APEX canon application
│   │   ├── main.tsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── ui/               # shadcn/ui components
│   │   │   ├── TrinityDashboard.tsx      # System monitor
│   │   │   ├── FloorVisualizer.tsx       # 13-floor interactive
│   │   │   ├── EngineDiagram.tsx         # ΔΩΨ consensus
│   │   │   ├── MetabolicLoop.tsx         # 000-999 stages
│   │   │   └── CitationBlock.tsx         # Academic refs
│   │   └── lib/utils.ts
│   ├── public/
│   │   ├── floors.json           # Machine-readable spec
│   │   ├── references.json       # Academic citations
│   │   ├── api/v1/floors.json    # Static API endpoint
│   │   ├── *.jpg                 # Hero images
│   │   ├── llms.txt              # Constitutional prompt
│   │   ├── manifest.json
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   └── _headers
│   └── package.json              # +katex for math
│
├── docs/                          # DOCS (arifos.arif-fazil.com)
│   ├── src/
│   │   ├── App.tsx               # Documentation site
│   │   ├── main.tsx
│   │   ├── index.css
│   │   ├── components/ui/        # Minimal UI set
│   │   └── lib/utils.ts
│   ├── public/
│   │   ├── favicon.svg
│   │   ├── llms.txt
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   └── _headers
│   └── package.json              # React 18, Vite 5
│
├── shared/                        # Deduplicated assets
│   ├── 13-floors-geometric.jpg
│   ├── apex-geometric-hero.jpg
│   ├── arif-hero-og.jpg
│   ├── constitutional-floors.jpg
│   ├── entropy-cooling.jpg
│   ├── entropy-geometry.jpg
│   ├── forge-background.jpg
│   ├── mcp-pentagon.jpg
│   ├── mind-hero.jpg
│   ├── profile-avatar.jpg
│   ├── three-judges-geometric.jpg
│   └── three-judges.jpg
│
├── .github/workflows/
│   ├── deploy.yml                # Main deployment pipeline
│   ├── deploy-trinity.yml        # Alternative workflow
│   └── cleanup-deployments.yml   # Deployment cleanup
│
├── .gitignore
├── AGENTS.md                     # Agent guidelines
├── README.md                     # Human overview
├── FILE_MAPPING.md               # File organization guide
└── TRINITY_STRUCTURE.md          # This file
```

---

## 13 Constitutional Floors

| Floor | Name | Type | Threshold | Verdict |
|-------|------|------|-----------|---------|
| F1 | Amanah | Hard | LOCK | VOID |
| F2 | Truth | Hard | ≥0.99 | VOID |
| F3 | Tri-Witness | Soft | ≥0.95 | SABAR |
| F4 | Clarity | Soft | ≤0 | SABAR |
| F5 | Peace² | Hard | ≥1.0 | VOID |
| F6 | Empathy | Soft | ≥0.70 | SABAR |
| F7 | Humility | Soft | [0.03,0.05] | SABAR |
| F8 | Genius | Soft | ≥0.80 | SABAR |
| F9 | Anti-Hantu | Hard | ≤0.30 | VOID |
| F10 | Ontology | Hard | LOCK | VOID |
| F11 | Authority | Hard | LOCK | VOID |
| F12 | Hardening | Hard | ≥0.85 | VOID |
| F13 | Sovereign | Veto | ∞ | 888_HOLD |

---

## Deployment Mapping

| Site | Directory | Project Name | Domain | Build Command |
|------|-----------|--------------|--------|---------------|
| BODY | `body/` | ariffazil | arif-fazil.com | `npm install && npm run build` |
| THEORY | `THEORY/` | apex | apex.arif-fazil.com | `npm install && npm run build` |
| DOCS | `docs/` | arifos | arifos.arif-fazil.com | `npm install && npm run build` |

---

## MCP Tools (v55.1 Explicit Architecture)

| Tool | Stage | Engine | Description |
|------|-------|--------|-------------|
| init_reboot | 000 | ADAM | Gate & injection defense |
| agi_sense | 111 | ARIF | Input parsing & intent detection |
| agi_think | 222 | ARIF | Hypothesis generation |
| agi_reason | 333 | ARIF | Deep logic chains |
| asi_empathize | 444 | ADAM | Stakeholder modeling |
| asi_align | 555 | ADAM | Constitutional alignment |
| asi_insight | 666 | ADAM | Risk & impact foresight |
| apex_verdict | 888 | APEX | Final constitutional judgment |
| reality_search | Ext | ARIF | External fact-checking |

---

## Security Hardening Applied

✅ **Removed files with exposed API tokens:**
- `cleanup.js`
- `recreate.js`
- `wipe_deployments.js`
- `delete-arifos.ps1`
- `fix_pages.py`
- `restore_domains.js`

✅ **Collapsed all branches to main:**
- Deleted: `chore/llms-txt-trinity`, `flamboyant-cannon`, `recursing-kapitsa`, `stupefied-montalcini`, `wizardly-sinoussi`, `zen-bouman`

✅ **Removed stale directories:**
- `apex-old/`
- `soul-upgrade/`

⚠️ **Action Required:** Revoke Cloudflare API token `Sz46f5...` in dashboard if not already done.

---

## Development Commands

```bash
# BODY
cd body && npm install && npm run dev

# SOUL
cd soul && npm install && npm run dev

# DOCS
cd docs && npm install && npm run dev

# Build all
for dir in body soul docs; do cd $dir && npm run build && cd ..; done
```

---

## GitHub Actions Secrets Required

```
CLOUDFLARE_API_TOKEN      # API token with Pages:Edit permission
CLOUDFLARE_ACCOUNT_ID     # Cloudflare account ID
```

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
