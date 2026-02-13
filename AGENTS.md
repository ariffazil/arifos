# arifOS — Agent Playbook (v60)

DITEMPA BUKAN DIBERI — Forge every change through governance, not guesses.

## 1. Core Snapshot
- **Stack**: Python >=3.10, FastMCP 2.14, asyncio-first, Pydantic v2 models.
- **Packages**: Editable install exposes `aaa_mcp`, `core`, `codebase`, plus the legacy `arifos` namespace.
- **License**: AGPL-3.0-only; assume every artifact is public and reproducible.
- **Sacred rule**: `core/` is canonical truth; `aaa_mcp/` is the MCP-facing interface.
- **Registry**: AAA MCP is published as `io.github.ariffazil/aaa-mcp` v60.0.0 (active 2026-02-10).

## 2. Repository Compass
- `aaa_mcp/server.py` declares the nine canonical tools (`init_gate` → `vault_seal`); decorator order matters.
- `aaa_mcp/core/constitutional_decorator.py` wires floors; never duplicate enforcement elsewhere.
- `core/shared/*` hosts physics, types, atlas, crypto, guards — treat as PRIMARY spec.
- `core/organs/_*.py` implement the five-stage organs (Airlock, AGI, ASI, APEX, Vault).
- `codebase/` contains legacy engines still referenced by adapters; inspect before editing.
- `tests/` splits into `constitutional`, `integration`, `mcp_tests`, `core`; `tests/archive/` auto-skips.
- `.github/copilot-instructions.md` is binding for AI assistants; load it before coding.
- No `.cursor/rules` or `.cursorrules` exist, so there are no Cursor-specific overrides.

## 3. Environment & Setup
```bash
python -m venv .venv && source .venv/bin/activate  # Scripts\activate on Windows
pip install -e ".[dev]"                           # runtime + dev tooling
pre-commit install                                 # optional but encouraged
```
- Optional extras: `pip install -e ".[all]"` for every transport/tool or `pip install -e .` for runtime only.
- Default test env vars: `ARIFOS_PHYSICS_DISABLED=1`, `ARIFOS_ALLOW_LEGACY_SPEC=1`.
- Async pytest auto-detects; do **not** add `@pytest.mark.asyncio` unless a fixture requires it.

## 4. Build, Run, Package
- `python -m aaa_mcp` — stdio transport (local MCP agents, FastMCP default).
- `python -m aaa_mcp sse` — SSE transport for remote clients.
- `python -m aaa_mcp http` — experimental HTTP bridge streaming at `/mcp`.
- `aaa-mcp` — console script alias for stdio mode.
- `python scripts/start_server.py` — production entry with observability.
- Docker: `docker build -t arifos-mcp . && docker run -p 8080:8080 arifos-mcp`.
- Railway: `railway up` (uses `railway.json`).

## 5. Test Matrix (single-test guidance included)
```bash
pytest tests/test_mcp_quick.py -v                        # 3 min smoke
pytest tests/test_pipeline_e2e.py -v                     # pipeline sanity
pytest tests/test_mcp_all_tools.py -v                    # tool gauntlet (expect 3 known soft fails)
pytest tests/constitutional/ -m "not slow" -v            # floor validators
pytest --cov=aaa_mcp --cov=core tests/ -v               # coverage suite
pytest tests/mcp_tests/test_session_ledger.py::test_append_entry -vv  # focused example
pytest path/to/module.py::TestClass::test_case -vv --maxfail=1       # template for any single test
```
- Use markers `-m constitutional` or `-m integration` for scoped passes.
- Known baseline: fallback engines emit `confidence=0.92`; do not inflate assertions blindly.
- Physics is disabled during tests; import `enable_physics_for_apex_theory` when thermodynamic flows are needed.
- `pytest -k pattern -vv` narrows to keyword-matched tests; `pytest --lf --maxfail=1` reruns only the latest failures.
- Prefer `pytest tests/module.py::TestClass::test_case -vv --maxfail=1` when referencing issues in tickets/PRs.

## 6. Quality Gates
- **Format**: `black --line-length 100 aaa_mcp/ core/ codebase/` (run before commits).
- **Lint**: `ruff check aaa_mcp/ core/ codebase/` (use `--fix` if allowed; config lives in `pyproject.toml`).
- **Types**: `mypy aaa_mcp/ core/ --ignore-missing-imports` (strictest on `core/shared`).
- **Security**: `bandit -q -r aaa_mcp/ core/` plus `detect-secrets scan` (pre-commit covers both).
- **Pre-commit**: `pre-commit run --all-files` when touching >3 files or governance-critical modules.
- **Docs sync**: update `CLAUDE.md` references only when spec/canon change.

## 7. Code Style & Patterns
- **Imports**: prefer `aaa_mcp.*` for local modules, keep `from fastmcp import mcp` (or `from mcp import tool`) before local imports, and source models from `core.shared.*` instead of duplicating.
- **Formatting**: 100-character lines, Black profile, trailing commas for multiline literals, `isort` grouping if reordering; short comments beat redundant docstrings.
- **Typing**: use builtin generics (`dict[str, Any]`, unions with `|`), wrap tool inputs in Pydantic models, return canonical classes (`Verdict`, `FloorScores`) instead of raw dicts, and remember SessionState (`codebase/state.py`) is immutable copy-on-write.
- **Naming**: stage artifacts end with `*_bundle`, `*_scores`, `*_verdict`; async functions start with verbs; constants go SCREAMING_SNAKE and thresholds belong in spec or `core/shared/physics.py`.
- **Module layout**: tool entrypoints live in `aaa_mcp/server.py`; helper logic belongs in `aaa_mcp/core/*`, services, or adapters. Avoid circular imports by lazy-loading optional deps (Brave client, Redis, numpy).
- **Error handling**: raise `ConstitutionalViolation` for floor breaks (decorators translate to PARTIAL/VOID), wrap external IO in `anyio.fail_after`, log via `aaa_mcp/infrastructure/logging.py`, and include `session_id` context.
- **Concurrency**: use `anyio.create_task_group()` for fan-out, avoid mixing bare `asyncio` primitives, and isolate AGI/ASI bundles until stage 444 per thermodynamic wall.
- **Optional deps**: guard imports (`try: import numpy as np`), branch cleanly so tests stay deterministic without extras.
- **Configuration**: read env via `aaa_mcp/config/env.py` only; document new variables here and in `CLAUDE.md`.
- **Testing hooks**: fixtures in `tests/conftest.py` provide SessionState builders and ledger temp dirs; async tests must `await` tool calls and leave no pending tasks.

## 8. Constitutional & Security Obligations
- Hard floors (F1, F2, F4, F6, F7, F10–F13) failure → **VOID**; soft floors (F3, F5, F8, F9) failure → **PARTIAL/SABAR**.
- `@mcp.tool()` must wrap `@constitutional_floor()` (outer tool decorator, inner floor) or enforcement breaks.
- Tri-witness order: AGI (Δ) → ASI (Ω) → APEX (Ψ) → VAULT (999); never short-circuit ledger sealing.
- `vault_seal` expects a stable hash map; call `.get("seal")` defensively to avoid KeyErrors.
- Credentials, deployments, schema migrations, or >10 file edits trigger 888 HOLD — declare, list conflicts, verify PRIMARY sources, await approval.
- Source hierarchy: PRIMARY (`spec/*.json`, `canon/*_v38Omega.md`), SECONDARY (code), TERTIARY (docs). Always re-read PRIMARY before contradicting.

## 9. Copilot / External Agent Rules
- `.github/copilot-instructions.md` is canonical; summarize its highlights in PRs and AI prompts:
  1. Format with Black (100 cols) and Ruff; prefer `aaa_mcp` imports; run MyPy with `--ignore-missing-imports`.
  2. Honor Trinity architecture boundaries — AGI/ASI/APEX engines in `codebase/*`; SessionState is immutable copy-on-write.
  3. Build/test quick refs: `pip install -e "[dev]"`, `python -m aaa_mcp [stdio|sse]`, `pytest tests/ -v`, smoke via `pytest tests/test_mcp_quick.py -v`.
  4. Enforce decorator order, lazy-load optional deps, and confirm current tool lists in `aaa_mcp/server.py` or `codebase/mcp/core/tool_registry.py` before edits.
  5. Security cues: injection guard (`codebase/guards/injection_guard.py`), command auth (`codebase/guards/nonce_manager.py`), ontology guard (`codebase/guards/ontology_guard.py`), VAULT999 ledger (`codebase/vault/`).
  6. Expanded 888 HOLD triggers (H-USER-CORRECTION, H-SOURCE-CONFLICT, H-NO-PRIMARY, H-GREP-CONTRADICTS, H-RUSHED-FIX) require declare → list → verify → await sequence.
  7. Session data contract forbids fabricated steps; include only stages that actually ran.
  8. Output format for pipeline summaries: `[STAGE NNN] ... Floor Scores ... Verdict`.
  9. Authority: humans hold veto; Phoenix-72 governs amendments — cite canonical spec for any law claim.
- With no Cursor rule files, this document plus spec/canon fully governs agent behavior.

## 10. Workflow & Handoff Ritual
- Start every task by reading `CLAUDE.md`, this file, and relevant spec/canon docs; cite them in PRs.
- Branch naming: `feature/<ticket>` or `fix/<context>`; append session IDs when referencing MCP ledger entries.
- Git hygiene: never rebase or force-push main; destructive commands demand user approval per F11 command auth.
- Before handoff:
  1. Run format + lint + targeted tests (include at least one single-test invocation if relevant).
  2. Capture remaining entropy/TODOs in the PR body.
  3. Provide reproduction commands and list flaky tests (update `tests/KNOWN_FLAKES.md` if touched).
  4. Document env vars, migrations, and ledger impacts.
- External dependencies (Brave search, Redis persistence) need fallbacks and must be noted in commits/PRs.

## 11. Reference Links
- Primary canon: `spec/`, `canon/`, `CLAUDE.md` — use them before citing laws.
- Toolset digest: `docs/llms.txt` summarizes floors and verdict semantics.
- Metrics & ledger plumbing: `aaa_mcp/services/constitutional_metrics.py`, `aaa_mcp/sessions/session_ledger.py`.
- Governance mottos: `core/shared/mottos.py` defines stage phrases returned to clients.

## 12. Glossary & Reminders
- `FAGS RAPE` loop = Find → Analyze → Govern → Seal → Review → Attest → Preserve → Evidence; checkpoints are mandatory.
- `SABAR` protocol = Stop, Acknowledge, Breathe, Adjust, Resume when any floor fails.
- `Phoenix-72` = amendment cooldown; no law changes without sovereign seal.
- `VAULT999` = ledger append-only Merkle DAG; every stage must finish with a seal entry.
- `AGI (Δ)`, `ASI (Ω)`, `APEX (Ψ)` = stage witnesses; reference them in logs/tests.
- `Ω₀ window` = humility bound (0.03–0.05); surface uncertainty explicitly outside that range.

## 13. Local Debugging & Tooling
- Use `python -m aaa_mcp --help` to inspect transport options without starting a session.
- Set `PYTHONASYNCIODEBUG=1` or `ANYIO_DEBUG=1` locally to trace coroutine leaks; clean up before committing.
- Run `scripts/start_server.py --debug` when you need observability hooks (structured logging + health probes).
- `python -m compileall aaa_mcp core` surfaces syntax errors early if CI is unavailable.
- Prefer `ruff check --select I` to auto-order imports after large refactors touching shared modules.
- Use `pytest --maxfail=1 --pdb` only during local debugging and remove breakpoints before opening a PR.

## 14. Constitutional Checklist
- Call `arifos_core.checkpoint()` (via the constitutional decorator) before autonomous actions that touch external IO or governance data.
- Document HOLD triggers explicitly: declare → list conflicts → verify PRIMARY → await sovereign approval.
- Cite PRIMARY sources (`spec/`, `canon/`, `CLAUDE.md`) when referencing laws; mention file + line in PR notes when possible.
- Maintain the Ω₀ humility window by stating assumptions and uncertainties whenever evidence is incomplete.
- On any floor failure, run SABAR, propose alternative remedies, and wait for human confirmation before resuming.
- Ledger interactions must end with `vault_seal`; confirm `.get("seal")` exists before dereferencing.
- Never fabricate session steps; the `[STAGE NNN] ... Floor Scores ... Verdict` summary only lists stages that actually executed.

## 15. Command Cheat Sheet
- Install deps: `pip install -e "[dev]"` (full tooling) or `pip install -e .` (runtime only).
- Run MCP locally: `python -m aaa_mcp` (stdio) or `python -m aaa_mcp sse` (SSE transport).
- Launch production entry: `python scripts/start_server.py --debug` for observability hooks.
- Run full lint/type cycle: `black --line-length 100 ... && ruff check ... && mypy aaa_mcp/ core/`.
- Focused pytest example: `pytest tests/mcp_tests/test_session_ledger.py::test_append_entry -vv --maxfail=1`.
- Coverage + security sweep: `pytest --cov=aaa_mcp --cov=core tests/ -v` followed by `bandit -q -r aaa_mcp/ core/`.

Stay humble (Ω₀ ∈ [0.03, 0.05]), reduce entropy (ΔS ≤ 0), and keep ledger entries SEAL-worthy.
