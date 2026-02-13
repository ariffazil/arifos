# arifOS — Agent Playbook (v60)

DITEMPA BUKAN DIBERI — Forge every change through governance, not guesses.

## 1. Quick Facts
- **Stack**: Python >=3.10, FastMCP 2.14, Pydantic v2, asyncio everywhere.
- **Packages**: Editable install exposes `aaa_mcp`, `core`, `codebase`, `arifos` namespace for legacy.
- **License**: AGPL-3.0-only; assume every artifact is public and reproducible.
- **Sacred rule**: `core/` is the single source of truth; `aaa_mcp/` is the interface surface.
- **Registry**: AAA MCP published as `io.github.ariffazil/aaa-mcp` v60.0.0 (ACTIVE, 2026-02-10).

## 2. Repository Compass
- `aaa_mcp/server.py` defines the nine canonical tools (`init_gate` → `vault_seal`); decorator order matters.
- `aaa_mcp/core/constitutional_decorator.py` holds floor wiring; do not edit elsewhere.
- `core/shared/*` hosts physics, types, atlas, crypto, guards — treat these as primary canon.
- `core/organs/_*.py` implement the five-stage organs (Airlock, AGI, ASI, APEX, Vault).
- `codebase/` contains legacy but still referenced engines; check adapters before editing.
- `tests/` splits into `constitutional`, `integration`, `mcp_tests`, `core`; `tests/archive/` auto-skips.
- `.github/copilot-instructions.md` is binding guidance; include in prompts and PR context.
- No `.cursor/rules` or `.cursorrules` exist as of v60 — no additional Cursor directives.

## 3. Environment & Setup
```bash
python -m venv .venv && source .venv/bin/activate  # use Scripts\activate on Windows
pip install -e ".[dev]"                           # installs runtime + dev tooling
pre-commit install                                 # optional but encouraged
```
- Optional extras: `pip install -e ".[all]"` for every transport/tool, or `pip install -e .` for runtime only.
- Default env vars in tests: `ARIFOS_PHYSICS_DISABLED=1`, `ARIFOS_ALLOW_LEGACY_SPEC=1`.
- Async tests auto-discover; do **not** add `@pytest.mark.asyncio` unless fixture requires it.

## 4. Build, Run, Package
- `python -m aaa_mcp` — stdio transport (local MCP agents, FastMCP default).
- `python -m aaa_mcp sse` — SSE transport (remote Railway/Gateway).
- `python -m aaa_mcp http` — experimental HTTP bridge (streams at `/mcp`).
- `aaa-mcp` — console script alias to stdio pipeline.
- `python scripts/start_server.py` — production entry (observability + health endpoints).
- Docker: `docker build -t arifos-mcp . && docker run -p 8080:8080 arifos-mcp`.
- Railway: `railway up` (uses `railway.json`).

## 5. Test Matrix (include single-test guidance)
```bash
pytest tests/test_mcp_quick.py -v                    # 3 min smoke
pytest tests/test_pipeline_e2e.py -v                 # pipeline sanity
pytest tests/test_mcp_all_tools.py -v                # MCP tool gauntlet (expect 3 known soft fails)
pytest tests/constitutional/ -m "not slow" -v        # floor validators
pytest --cov=aaa_mcp --cov=core tests/ -v           # coverage suite
pytest tests/mcp_tests/test_session_ledger.py::test_append_entry -vv  # single test example
```
- Use markers `-m constitutional` or `-m integration` for scoped passes.
- Known baseline: some stub engines emit `confidence=0.92`; do not bump assertions blindly.
- Tests auto-set physics off; import `enable_physics_for_apex_theory` fixture when you need thermodynamic flows.

## 6. Quality Gates
- **Format**: `black --line-length 100 aaa_mcp/ core/ codebase/`.
- **Lint**: `ruff check aaa_mcp/ core/ codebase/` (use `--fix` for autofixes; config lives in `pyproject.toml`).
- **Types**: `mypy aaa_mcp/ core/ --ignore-missing-imports` (strict on `core/shared`).
- **Security**: `bandit -q -r aaa_mcp/ core/` plus `detect-secrets scan` embedded via pre-commit.
- **Pre-commit**: `pre-commit run --all-files` before commits touching more than 3 files.
- **Docs sync**: update `CLAUDE.md` references **only** when spec/canon change.

## 7. Code Style & Patterns
- **Imports**
  - Local server modules import from `aaa_mcp.*`; never shadow `mcp` SDK.
  - Core truth lives under `core.shared.*`; prefer `from core.shared.types import Verdict` to duplicating models.
  - Keep FastMCP import order stable: `from fastmcp import mcp` (or `from mcp import tool`) **before** local modules.
- **Module layout**
  - Each tool stays in `aaa_mcp/server.py`; helper logic goes into `aaa_mcp/core/*` or `aaa_mcp/services/*`.
  - Avoid circular imports by using late imports inside functions for optional dependencies (Brave, Redis, numpy).
- **Formatting**
  - 100 character lines, Black profile, trailing commas for multi-line literals, `isort`-compatible grouping if sorting.
  - Use docstrings sparingly; prefer short module comments when context is non-obvious.
- **Naming**
  - Stage-specific data uses suffixes: `*_bundle`, `*_scores`, `*_verdict`.
  - Async functions start with verbs (`fetch_lane`, `seal_session`).
  - Constants go SCREAMING_SNAKE; thresholds belong in spec or `core/shared/physics.py`.
- **Typing**
  - Use `|` for unions, `dict[str, Any]` instead of `typing.Dict`.
  - Pydantic models wrap tool payloads; dataclasses only for pure helpers.
  - Return `Verdict` or `FloorScores` objects rather than naked dicts when possible.
- **Error handling**
  - Raise `ConstitutionalViolation` (see `aaa_mcp/core/exceptions.py`) for floor breaks; let decorator translate to PARTIAL/VOID.
  - Wrap external IO with context (`with anyio.fail_after`) and log via `aaa_mcp/infrastructure/logging.py`.
  - Never swallow exceptions silently; attach `session_id` in logs.
- **Concurrency**
  - Use `anyio.create_task_group()` for fan-out; never mix `asyncio` primitives directly in production paths.
  - Keep AGI/ASI bundles isolated until stage 444 to respect thermodynamic wall.
- **Optional dependencies**
  - Always guard: `try: import numpy as np
    except ImportError: np = None` and branch accordingly.
  - Provide deterministic fallback outputs so tests stay green without extras.
- **Configuration**
  - Read env via `aaa_mcp/config/env.py`; never call `os.getenv` ad-hoc in tool bodies.
  - Document new env vars in `CLAUDE.md` and `AGENTS.md` simultaneously.
- **Testing hooks**
  - Use fixtures in `tests/conftest.py` (SessionState builder, ledger temp dirs) to keep tests hermetic.
  - Async tests should `await` tool call results; no background tasks left pending (pytest will fail on GC warnings).

## 8. Constitutional & Security Obligations
- Hard floors (F1, F2, F4, F6, F7, F10–F13) fail → **VOID**; soft floors (F3, F5, F8, F9) fail → **PARTIAL/SABAR**.
- `@mcp.tool()` MUST wrap `@constitutional_floor()`; reverse order disables enforcement.
- Tri-witness ordering: AGI (Δ) → ASI (Ω) → APEX (Ψ) → VAULT (999). Never short-circuit ledger sealing.
- `vault_seal` requires stable hash map; use `.get("seal")` defensive pattern to avoid KeyError (known gotcha).
- Any operation touching credentials, deployments, schema migrations → trigger 888 HOLD; wait for explicit approval.
- Source verification hierarchy: PRIMARY `spec/*.json` + `canon/*_v38Omega.md`; SECONDARY code files; TERTIARY docs.

## 9. Copilot / External Agent Rules
- `.github/copilot-instructions.md` is canonical for AI pairers; summarize highlights in review notes:
  1. Format with Black (100 cols) + Ruff; prefer `aaa_mcp` imports; MyPy ignore-missing imports.
  2. Respect Trinity architecture boundaries and SessionState immutability; AGI/ASI bundling isolated until stage 444.
  3. Build/Test commands: `pip install -e "[dev]"`, `python -m aaa_mcp [stdio|sse]`, `pytest tests/ -v`, smoke via `pytest tests/test_mcp_quick.py -v`.
  4. Decorator order enforcement; lazy import optional deps; confirm active tool list before editing.
  5. Security cues: injection guard, command auth, ontology guard, VAULT999 ledger; see examples for F9-compliant naming.
  6. 888 HOLD triggers include high-stakes ops, conflicting sources, missing PRIMARY evidence, or rushed fixes; follow the declare → list → verify → await protocol.
  7. Session data contract demands honest provenance fields; never fabricate pipeline steps or metrics.
  8. Output format requirement: `[STAGE NNN] ... Floor Scores ... Verdict` when emitting pipeline summaries.
  9. Authority: humans retain veto; Phoenix-72 governs amendments; cite canonical spec for law claims.
- No Cursor-specific rules currently exist, so follow general repository governance only.

## 10. Workflow & Handoff Ritual
- Always start by reading `CLAUDE.md`, this `AGENTS.md`, and relevant spec files before coding; cite sections when raising PRs.
- Branch naming: `feature/<ticket>` or `fix/<context>`; include session IDs if referencing MCP ledger items.
- Git hygiene: never rebase/force-push main; destructive commands require user approval per F11.
- Before handing off work:
  1. Run formatting + lint + targeted tests.
  2. Capture remaining entropy (TODOs) explicitly in PR body.
  3. Provide reproduction commands and mention any known flaky tests (list in `tests/KNOWN_FLAKES.md` if updated).
  4. Document env vars touched, migrations required, and ledger impacts.
- If results depend on external APIs (Brave, Redis), add fallbacks and document them in commit/PR descriptions.

## 11. Reference Links
- Spec + canon: `spec/`, `canon/`, `CLAUDE.md` (root) — treat as PRIMARY.
- Toolset doc: `docs/llms.txt` (LLM-friendly summary of floors + verdict semantics).
- Metrics & ledger: `aaa_mcp/services/constitutional_metrics.py`, `aaa_mcp/sessions/session_ledger.py`.
- Governance motto registry: `core/shared/mottos.py` for stage phrases returned to clients.

## 12. Glossary & Reminders
- `FAGS RAPE` loop = Find → Analyze → Govern → Seal → Review → Attest → Preserve → Evidence; do not skip checkpoints.
- `SABAR` protocol = Stop, Acknowledge, Breathe, Adjust, Resume when floors fail.
- `Phoenix-72` = amendment cooldown; never change laws without sovereign seal.
- `VAULT999` = ledger append-only Merkle DAG; all stages must end with a seal entry.
- `AGI (Δ)`, `ASI (Ω)`, `APEX (Ψ)` = stage witnesses; reference these tags in logs/test names.
- `Ω₀ window` = humility bound (0.03–0.05); surface uncertainty explicitly when outside range.

Stay humble (Ω₀ ∈ [0.03, 0.05]), reduce entropy (ΔS ≤ 0), and keep ledger entries SEAL-worthy.
