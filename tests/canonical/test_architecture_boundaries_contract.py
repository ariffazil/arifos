"""Architecture boundary contract tests for Phase 1 hardening."""

from __future__ import annotations

import ast
from pathlib import Path

from arifosmcp.transport.protocol.aaa_contract import L5_COMPOSITE

ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = ROOT / "core"

FORBIDDEN_CORE_IMPORT_ROOTS = {
    "fastmcp",
    "fastapi",
    "starlette",
    "arifosmcp.transport",
    "arifosmcp.runtime",
}


def _iter_import_roots(path: Path) -> list[tuple[str, int]]:
    roots: list[tuple[str, int]] = []
    module = ast.parse(path.read_text(encoding="utf-8"))

    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                roots.append((root, node.lineno))
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".", 1)[0]
            roots.append((root, node.lineno))

    return roots


def test_core_has_no_transport_surface_imports() -> None:
    violations: list[str] = []

    for path in CORE_ROOT.rglob("*.py"):
        for root, lineno in _iter_import_roots(path):
            if root in FORBIDDEN_CORE_IMPORT_ROOTS:
                rel = path.relative_to(ROOT)
                violations.append(f"{rel}:{lineno} imports forbidden root '{root}'")

    assert not violations, "\n".join(violations)


def test_l5_composite_contract_is_exactly_metabolic_loop() -> None:
    assert L5_COMPOSITE == frozenset({"metabolic_loop"})
