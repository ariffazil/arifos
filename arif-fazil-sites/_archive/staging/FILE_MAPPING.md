# HUMAN THEORY APPS Sites — File Mapping & Organization Guide (Updated v55.2)

## Architecture Overview

| Layer | Site | Domain | Directory | Purpose |
|-------|------|--------|-----------|---------|
| **BODY** | Portfolio | arif-fazil.com | `body/` | Personal portfolio, status dashboard |
| **THEORY** | APEX Canon | apex.arif-fazil.com | `THEORY/` | Constitutional framework, 13-floor theory |
| **DOCS** | arifOS Docs | arifos.arif-fazil.com | `docs/` | API documentation, MCP reference |
| **MIND** | MCP Backend | aaamcp.arif-fazil.com | `arifOS repo` | ⚠️ NOT IN THIS REPO - Python FastAPI backend |

---

## Current File Structure

### BODY (`body/`)
- Directory: `body/`
- `public/llms.txt`: Site identity and links for LLMs.

### THEORY (`THEORY/`)
- Directory: `THEORY/`
- Upgraded to v55.2 Trinity.
- `src/components/`: Contains upgraded TrinityDashboard, FloorVisualizer, etc.
- `public/llms.txt`: Constitutional canon links.

### DOCS (`docs/`)
- Directory: `docs/`
- `public/llms.txt`: Documentation links.
- `AGENTS.md`: Contributor and agent guidelines.
- `MANUAL_CONFIG_GUIDE.md`: Manual deployment configuration.

### SHARED Assets (`shared/`)
- Directory: `shared/`
- Common media used across all sites.

### SCRIPTS (`scripts/`)
- Directory: `scripts/`
- `collapse.js`: Utility for branch management.

---

## Deployment Mapping

| GitHub Action | Source Dir | Project Name | Domain |
|---------------|------------|--------------|--------|
| deploy-body | `body/` | ariffazil | arif-fazil.com |
| deploy-theory | `THEORY/` | apex | apex.arif-fazil.com |
| deploy-docs | `docs/` | arifos | arifos.arif-fazil.com |

---

**Ditempa Bukan Diberi** — Forged, Not Given