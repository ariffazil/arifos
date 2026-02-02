# Repository Guidelines

## Project Structure & Module Organization
- `arifos/` and `arifos_core/`: primary Python source packages; keep domain logic in these modules.
- `tests/`: automated test suite (pytest).
- `docs/` and `L1_THEORY/`: product/spec documentation and theory references.
- `scripts/`: verification utilities and one-off helpers.
- `vault_999/` and `.codex/`: governance artifacts, ledgers, and agent tooling (treat as sensitive).

## Build, Test, and Development Commands
- `python -m pytest -q tests/` runs the full test suite quietly.
- `pytest tests/test_pipeline_routing.py` runs a single test module.
- `python -c "import arifos_core.system.pipeline as p; print('pipeline-import-ok')"` sanity-checks core imports.
- `rg --files` lists repository files quickly (preferred search tool in this repo).
- No separate build step is required for local development; run tests after changes.

## Coding Style & Naming Conventions
- Python with 4-space indentation; keep lines concise and readable.
- `snake_case` for modules, functions, and variables; `PascalCase` for classes.
- Prefer explicit imports over wildcard imports.
- Keep comments minimal and focused on non-obvious logic or invariants.

## Testing Guidelines
- Framework: `pytest`.
- Naming: `test_*.py` files and `test_*` functions.
- Add tests in `tests/` adjacent to the behavior being changed.
- Run targeted tests for the files you touched before running the full suite.

## Commit & Pull Request Guidelines
- Use short, scoped commit messages (example: `fix(v46): align aCLIP bridge SEAL verdict`).
- PRs should include: purpose/summary, test commands + results, and linked issues when available.
- Include screenshots only for UI-facing changes (rare in this repo).

## Security & Configuration Tips
- Do not commit secrets; use environment variables for tokens and credentials.
- Treat `vault_999/` artifacts as sensitive and ensure changes are intentional.
