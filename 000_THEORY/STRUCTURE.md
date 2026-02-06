# 000_THEORY/STRUCTURE.md — Canonical Repository Architecture

```text
      Δ       
     / \      document:   STRUCTURE.md
    /   \     version:    v55.5-HARDENED
   /  🏛️  \    status:     CONSTITUTIONAL
  /_______\   floor:      F4 (Clarity)
```

**Author:** Antigravity (Δ) | **Date:** 2026-02-06 | **Status:** PROPOSED

---

## 🎯 Purpose

This document defines the **canonical structure** of the arifOS repository. It serves as the architectural source of truth for:
1. Where files should live
2. Why each directory exists
3. How to maintain structural integrity (F5)

> **Principle:** *Structure is Truth. To break structure is to break truth.*

---

## 📐 The Structural Hierarchy

arifOS uses a **hybrid naming convention**:
- **Numbered prefixes** (000, 333, 999) for Constitutional directories (encode metabolic stage)
- **Semantic names** for operational directories (industry standard)

### Tier 0: Root Level (~30 items max)

The root should contain **only essential files**. Industry best practice: <15 files per directory.
arifOS target: **≤30 visible items** at root.

---

## 🏗️ Constitutional Directories (PROTECTED)

These directories are **architecturally significant** and MUST remain at root:

| Directory | Stage | Role | Purpose |
|:---|:---:|:---|:---|
| `000_THEORY/` | 000 | **The Mind (Δ)** | Constitutional Law, Philosophy, Architecture |
| `333_APPS/` | 333 | **The Body** | Applications, Skills, Actions (L1-L7) |
| `VAULT999/` | 999 | **The Ledger** | Immutable Audit Trail |
| `ROADMAP/` | — | **The Future** | Planning, TODO, Releases |

### 000_THEORY/ — The Constitutional Canon

The **read-only source of truth** for all laws and philosophy.

```
000_THEORY/
├── 000_LAW.md              # The 13 Constitutional Floors (F1-F13)
├── 000_ARCHITECTURE.md     # The Metabolic Loop (000-999)
├── 000_FOUNDATIONS.md      # Philosophical Axioms
├── 010_TRINITY.md          # ΔΩΨ Architecture
├── 111_MIND_GENIUS.md      # The Physics of Thought
├── 333_MIND_ATLAS.md       # The Map of Paradoxes
├── 555_HEART_EMPATHY.md    # The Physics of Empathy
├── 777_SOUL_APEX.md        # Constitutional Physics Deep Dive
├── 888_SOUL_VERDICT.md     # Verdict Logic
├── 999_SOVEREIGN_VAULT.md  # Human Authority Protocol
├── _OUTLINE.md             # Canon Table of Contents
├── STRUCTURE.md            # This file
└── archive/                # Archived theory docs
```

### 333_APPS/ — The Application Layer

The **7-layer application stack** implementing Genius.

```
333_APPS/
├── L1_PROMPT/              # Layer 1: System Prompts
├── L2_SKILLS/              # Layer 2: Skills & Actions
│   ├── ACTIONS/            # Atomic skills (reason, perceive, etc.)
│   └── BUNDLES/            # Compound skills
├── L3_WORKFLOW/            # Layer 3: Workflows
├── L4_TOOLS/               # Layer 4: MCP Tools
├── L5_AGENTS/              # Layer 5: Multi-Agent Protocols
├── L6_INSTITUTION/         # Layer 6: Governance
├── L7_AGI/                 # Layer 7: AGI Protocols
├── ATLAS_NAVIGATION.md     # Navigation guide
├── README.md               # Layer overview
└── STATUS.md               # Implementation status
```

### VAULT999/ — The Immutable Ledger

The **cryptographic audit trail** for all sealed decisions.

```
VAULT999/
├── YYYY-MM-DD/             # Date-organized entries
│   └── seal_<hash>.json    # Individual seal records
├── merkle_root.json        # Current Merkle root
└── README.md               # Vault protocol
```

### ROADMAP/ — The Planning Layer

The **future vision** and current priorities.

```
ROADMAP/
├── ROADMAP.md              # Version roadmap
├── TODO.md                 # Current priorities
├── INTEGRATION_MASTERPLAN.md
└── archive/                # Historical plans
```

---

## ⚙️ Operational Directories

| Directory | Purpose | Content |
|:---|:---|:---|
| `codebase/` | **The Engine** | Python implementation of arifOS |
| `aaa_mcp/` | **API Layer** | MCP Server (FastMCP) |
| `tests/` | **Quality** | Test suite |
| `docs/` | **Documentation** | All non-constitutional docs |
| `scripts/` | **Operations** | Utility scripts |
| `config/` | **Configuration** | Environment configs |
| `archive/` | **Entropy Sink** | Historical/deprecated files |
| `examples/` | **Usage** | Example implementations |

### codebase/ — The Python Engine

```
codebase/
├── __init__.py             # Package init
├── agi/                    # AGI modules (Mind)
├── asi/                    # ASI modules (Heart)
├── apex/                   # APEX kernel (Soul)
├── floors/                 # Floor implementations
├── vault/                  # Vault logic
├── stages/                 # Metabolic stages
├── engines/                # Engine implementations
├── federation/             # Multi-agent federation
├── init/                   # Initialization (000)
├── guards/                 # Safety guards
├── system/                 # System utilities
└── tests/                  # Unit tests
```

### docs/ — Documentation Hub

```
docs/
├── assets/                 # Images, diagrams
├── manifesto/              # PDF manifestos
├── deployment/             # Deploy guides
├── development/            # Dev guides
├── mcp/                    # MCP documentation
├── integrations/           # Integration guides
├── setup/                  # Setup guides
└── reports/                # Generated reports
```

### scripts/ — Operational Scripts

```
scripts/
├── setup/                  # Setup scripts
├── manifesto/              # Manifesto generators
├── deployment/             # Deploy scripts
└── maintenance/            # Maintenance scripts
```

---

## 📄 Essential Root Files

### Agent Codices (PROTECTED)

| File | Agent | Purpose |
|:---|:---:|:---|
| `GEMINI.md` | **Δ** | Architect's Operational Codex |
| `CLAUDE.md` | **Ω** | Engineer's Operational Codex |
| `SOUL.md` | **Ψ** | Auditor's Operational Codex |

### Standard OSS Files (Required)

| File | Purpose |
|:---|:---|
| `README.md` | Human entry point |
| `LICENSE` | GPL-3.0 legal framework |
| `CHANGELOG.md` | Version history (F1 Amanah) |
| `CONTRIBUTING.md` | Contributor guide |
| `SECURITY.md` | Security policy (F12 Defense) |

### System Identity Files

| File | Purpose |
|:---|:---|
| `AGENTS.md` | Agent discovery (industry standard) |
| `IDENTITY.md` | System identity declaration |
| `USER.md` | User profile |
| `llms.txt` | AI discovery protocol |

### Build & Deployment Files

| File | Purpose |
|:---|:---|
| `pyproject.toml` | Python build configuration |
| `requirements.txt` | Dependencies (fallback) |
| `Dockerfile` | Container definition |
| `railway.toml` | Railway deployment |
| `MANIFEST.in` | Python package manifest |
| `uv.lock` | UV lock file |

### Configuration Files

| File | Purpose |
|:---|:---|
| `.gitignore` | VCS ignore rules |
| `.mcp.json` | MCP client configuration |
| `.env.example` | Environment template |
| `.pre-commit-config.yaml` | Code quality hooks |
| `.dockerignore` | Docker ignore rules |

---

## 📁 Hidden Directories (Agent Workspaces)

These are hidden (dot-prefixed) and managed by agents:

| Directory | Purpose |
|:---|:---|
| `.agent/` | Gemini workflows |
| `.agents/` | Multi-agent configs |
| `.antigravity/` | Architect workspace |
| `.gemini/` | Gemini memory/cache |
| `.claude/` | Claude memory |
| `.kimi/` | Kimi agent config |
| `.github/` | CI/CD workflows |
| `.vscode/` | VSCode configuration |
| `.vs/` | Visual Studio config |
| `.cache/` | Build cache |
| `.venv/`, `venv/` | Virtual environments |

---

## 🎯 The Ideal Root Structure

```
arifOS/                         # ~30 visible items
│
├── 📜 000_THEORY/              # Constitutional Law [PROTECTED]
├── 📦 333_APPS/                # Applications [PROTECTED]
├── 🔒 VAULT999/                # Audit Ledger [PROTECTED]
├── 🗺️ ROADMAP/                 # Planning [PROTECTED]
├── ⚙️ codebase/                # Python Engine
├── 🤖 aaa_mcp/                 # MCP Server
├── 🧪 tests/                   # Test Suite
├── 📚 docs/                    # Documentation
├── 🔧 scripts/                 # Scripts
├── ⚙️ config/                  # Configuration
├── 📁 archive/                 # Entropy Sink
├── 📁 examples/                # Examples
│
├── 📄 README.md                # Entry Point
├── 📄 LICENSE                  # GPL-3.0
├── 📄 GEMINI.md                # Δ Codex
├── 📄 CLAUDE.md                # Ω Codex
├── 📄 SOUL.md                  # Ψ Codex
├── 📄 AGENTS.md                # Agent Discovery
├── 📄 IDENTITY.md              # System Identity
├── 📄 USER.md                  # User Profile
├── 📄 CHANGELOG.md             # History
├── 📄 CONTRIBUTING.md          # Contribution
├── 📄 SECURITY.md              # Security
├── 📄 llms.txt                 # AI Discovery
│
├── 📦 pyproject.toml           # Build
├── 📦 requirements.txt         # Deps
├── 🐳 Dockerfile               # Container
├── 🚂 railway.toml             # Deploy
├── 📦 MANIFEST.in              # Package
├── 🔒 uv.lock                  # Lock
│
├── 🔧 .gitignore               # VCS
├── 🔧 .mcp.json                # MCP
├── 🔧 .env.example             # Env
├── 🔧 .dockerignore            # Docker
├── 🔧 .pre-commit-config.yaml  # Hooks
│
└── 📁 .<agent>/                # Hidden workspaces
```

---

## ⚖️ Constitutional Alignment

| Floor | Requirement | How Structure Satisfies |
|:---:|:---|:---|
| **F1 Amanah** | Auditability | `VAULT999/` + `CHANGELOG.md` |
| **F2 Truth** | Factual Source | `000_THEORY/` as canonical |
| **F4 Clarity** | Entropy ≤ 0 | 95 → 30 items (68% reduction) |
| **F5 Peace²** | Safety Margins | Clear separation of concerns |
| **F11 Authority** | Governance | Agent codices define behavior |
| **F12 Defense** | Security | `SECURITY.md` + `.gitignore` |

---

## 🚫 Anti-Patterns (What NOT to Do)

1. **Don't put temporary files at root** → Use `archive/` or `.antigravity/`
2. **Don't create new root directories** without constitutional justification
3. **Don't move Constitutional directories** (000_THEORY, 333_APPS, VAULT999, ROADMAP)
4. **Don't delete Agent codices** (GEMINI.md, CLAUDE.md, SOUL.md)
5. **Don't put separate repos in root** → Use git submodules

---

## 📋 Maintenance Protocol

### Before Adding Files to Root

1. **Check if it fits in existing directories** (docs/, scripts/, archive/)
2. **Verify constitutional necessity** — Does it need root visibility?
3. **Update this STRUCTURE.md** if adding permanent root items

### Before Moving Files

1. **Run dependency audit** — `git grep <filename>` to find references
2. **Update imports** in Python files
3. **Update links** in Markdown files
4. **Log the change** in CHANGELOG.md

---

**DITEMPA BUKAN DIBERI** — Structure is forged with intention, not accumulated by accident.
