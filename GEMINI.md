# GEMINI.md — arifOS Constitutional Agent Policy

This document provides the operational context for AI agents working within the `arifOS` repository. Adherence to these principles is mandatory.

**Motto:** *Ditempa Bukan Diberi — Forged, Not Given*

---

## 🏛️ Project Overview

**arifOS** is a production-grade **Constitutional AI Governance System**. It functions as an "Intelligence Kernel" that wraps any Large Language Model (LLM) to enforce a set of 13 ethical and safety rules, known as "Constitutional Floors."

Its purpose is to govern AI cognition, ensuring that all outputs are safe, truthful, and aligned with core principles before they are generated.

### Core Architecture

The system is composed of three primary components, ensuring a strict separation of concerns:

1.  **The Kernel (`core/`):** The heart of arifOS, containing all pure, transport-agnostic decision-making logic. It enforces the 13 Floors and contains the core governance pipeline.
2.  **The Brain (`aaa_mcp/`):** The primary transport adapter, exposing the Kernel's functions via the Model Context Protocol (MCP). It handles incoming requests and formats the Kernel's verdicts, but contains **no decision logic** itself.
3.  **The Senses (`aclip_cai/`):** A set of tools for observability and "grounding," providing the Kernel with real-world context from the filesystem, network, and logs.

This architecture is built on the **Trinity of Intelligence**:
- **AGI (Δ - Mind):** Logical analysis and truth-seeking.
- **ASI (Ω - Heart):** Empathy and ethical safety checks.
- **APEX (Ψ - Soul):** Final judgment and consensus.

---

## 🛠️ Technology Stack

- **Language:** Python 3.12+ (Async-first)
- **Framework:** FastAPI, Starlette, and `fastmcp` for the MCP server.
- **Data Validation:** Pydantic v2 is used extensively.
- **Package Management:** `uv` is the recommended package manager.
- **Code Quality:** The project is strictly maintained with:
    - **Formatting:** `black`
    - **Linting:** `ruff`
    - **Type Checking:** `mypy`
- **Testing:** `pytest` is used for the comprehensive test suite.
- **Storage:** PostgreSQL for the immutable `VAULT999` ledger and Redis for caching.

---

## 🚀 Development Workflow

All development must adhere to the established quality standards.

### 1. Setup

First, set up the virtual environment and install all necessary dependencies using `uv`.

```bash
# Install uv (if you haven't already)
pip install uv

# Create a virtual environment and install dependencies
uv pip install -e ".[dev]"
```

### 2. Code Quality & Verification

Before committing any changes, run the following commands to ensure code quality, formatting, and type safety.

```bash
# Format code with Black
black . --line-length 100

# Lint code with Ruff
ruff check . --line-length 100

# Type check with MyPy
mypy .
```

### 3. Testing

New functionality requires new tests. All tests must pass before a change is considered complete.

```bash
# Run all tests
pytest tests/ -v

# Run tests faster by disabling physics-based computations
ARIFOS_PHYSICS_DISABLED=1 pytest tests/

# Run only the constitutional tests
pytest -m constitutional
```

---

## 🏃 Running the Project Locally

The main application is the `aaa-mcp` server. It can be run in several modes for development.

```bash
# Run in STDIO mode (for local IDE integrations like Cursor)
python -m aaa_mcp stdio

# Run in SSE mode (for remote clients, used in cloud deployments)
python -m aaa_mcp sse

# Run in HTTP mode (for streamable HTTP)
python -m aaa_mcp http
```

---

## 🤖 Agent Operational Guidelines

As an AI agent operating in this codebase, you are bound by the constitutional framework.

### The 13 Floors
Every action or thought must pass the 13 Constitutional Floors. These are not suggestions; they are load-bearing structural rules enforced by the Kernel. Violating a **HARD** floor (e.g., F2 Truth, F7 Humility) will result in a `VOID` verdict, blocking the action completely.

### High-Stakes Operations (888_HOLD)
You **MUST** trigger an `888_HOLD` and await human confirmation for any high-stakes operations, including but not limited to:
- Production deployments
- Git history modification (`rebase`, `force-push`)
- Mass file modifications
- Handling of secrets or credentials
- Any destructive database operations (`DROP`, `DELETE`)

### The 9-Tool Pipeline
Every request is processed through a mandatory 9-step pipeline, from `anchor` (initialization and security checks) to `seal` (committing an immutable audit record). Do not attempt to bypass this sequence.

### Core Principle: Separation of Concerns
- **`core/`** is for pure logic only. Do not add any transport-layer (HTTP, MCP) code here.
- **`aaa_mcp/`** is for transport only. Do not add any decision-making logic here; it must call the `core` kernel.

---

## 📁 Key Files & Directories

- **`pyproject.toml`**: Defines project metadata, dependencies, and scripts.
- **`AGENTS.md`**: The canonical guide for agents, detailing architecture and conventions.
- **`README.md`**: High-level project overview.
- **`000_THEORY/000_LAW.md`**: The definitive specification for the 13 Constitutional Floors.
- **`core/`**: The stateless, transport-agnostic governance kernel.
- **`aaa_mcp/`**: The main MCP server (The Brain).
- **`aclip_cai/`**: The sensory tools for grounding (The Senses).
- **`tests/`**: The test suite. All new code requires corresponding tests.
- **`VAULT999/`**: The immutable ledger for audit trails.
