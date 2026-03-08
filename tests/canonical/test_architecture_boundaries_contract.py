"""Architecture boundary contract tests.

The Trinity Body restructure places the governance envelope, transport adapters,
REST routes, and tool-surface re-exports inside ``core/``.  The original
boundary — "kernel has zero transport deps" — now applies only to the pure
decision-logic sub-packages that lived in ``core/`` *before* the restructure.

New boundary map:
  - ``core/organs/``, ``core/physics/``, ``core/shared/``, ``core/enforcement/``,
    ``core/perception/``, ``core/recovery/``, ``core/scheduler/``, ``core/state/``,
    ``core/kernel/``, ``core/observability/``, ``core/workflow/`` and the top-level
    kernel modules (governance_kernel.py, judgment.py, pipeline.py, etc.)
    → MUST NOT import transport surface (fastmcp, fastapi, starlette, arifos_aaa_mcp).

  - ``core/server.py``, ``core/transport/``, ``core/governance.py``,
    ``core/rest_routes.py``, ``core/contracts.py``, ``core/l0_constitution/``,
    ``core/l1_cognition/``, ``core/l2_tools/``
    → Runtime / transport files; they are ALLOWED to import transport packages.
"""

from __future__ import annotations

import ast
from pathlib import Path

from aaa_mcp.protocol.aaa_contract import L5_COMPOSITE

ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = ROOT / "core"

# Top-level kernel .py files that must remain transport-clean.
_KERNEL_TOP_FILES = {
    "governance_kernel.py",
    "homeostasis.py",
    "judgment.py",
    "pipeline.py",
    "risk_engine.py",
    "telemetry.py",
    "uncertainty_engine.py",
}

# Sub-packages that must remain transport-clean (original kernel sub-packages).
_KERNEL_SUBDIRS = {
    "organs",
    "physics",
    "shared",
    "enforcement",
    "perception",
    "recovery",
    "scheduler",
    "state",
    "kernel",
    "observability",
    "workflow",
    "config",
    "tests",
}

# Transport-surface imports forbidden from kernel files.
FORBIDDEN_TRANSPORT_ROOTS = {
    "fastmcp",
    "fastapi",
    "starlette",
    "arifos_aaa_mcp",
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


def _is_kernel_path(path: Path) -> bool:
    """Return True if *path* is a transport-clean kernel file."""
    rel = path.relative_to(CORE_ROOT)
    parts = rel.parts

    # Top-level kernel .py files
    if len(parts) == 1 and parts[0] in _KERNEL_TOP_FILES:
        return True

    # Sub-package kernel directories
    if parts[0] in _KERNEL_SUBDIRS:
        return True

    return False


def test_core_kernel_has_no_transport_surface_imports() -> None:
    """Core kernel modules (pre-restructure) must not depend on transport surface."""
    violations: list[str] = []

    for path in CORE_ROOT.rglob("*.py"):
        if not _is_kernel_path(path):
            continue
        for root, lineno in _iter_import_roots(path):
            if root in FORBIDDEN_TRANSPORT_ROOTS:
                rel = path.relative_to(ROOT)
                violations.append(f"{rel}:{lineno} imports forbidden root '{root}'")

    assert not violations, "\n".join(violations)


def test_l5_composite_contract_is_exactly_metabolic_loop() -> None:
    assert L5_COMPOSITE == frozenset({"metabolic_loop"})
