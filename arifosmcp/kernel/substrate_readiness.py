"""
arifosmcp/kernel/substrate_readiness.py — AGI-substrate readiness gate

This module does not claim arifOS is AGI. It defines the minimum machine-
checkable substrate gates a governed agentic kernel must satisfy before AGI-like
execution language is admissible.

A kernel earns readiness by passing invariants, not by asserting intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable

from arifosmcp.kernel.capability_registry import _build_default_graph
from arifosmcp.kernel.models import CapabilityGraph, MutationClass
from arifosmcp.runtime.public_surface import CANONICAL_7, public_tool_names_for_mode


class ReadinessVerdict(StrEnum):
    """Substrate verdict. FAIL is intentional until every gate is proven."""

    READY = "READY"
    HOLD = "HOLD"


@dataclass(frozen=True)
class ReadinessCheck:
    """One machine-checkable readiness invariant."""

    check_id: str
    passed: bool
    summary: str
    remediation: str = ""
    evidence: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ReadinessReport:
    """Aggregate substrate-readiness report."""

    verdict: ReadinessVerdict
    score: int
    passed: int
    total: int
    checks: tuple[ReadinessCheck, ...]

    @property
    def failed_checks(self) -> tuple[ReadinessCheck, ...]:
        return tuple(check for check in self.checks if not check.passed)

    def to_dict(self) -> dict[str, object]:
        return {
            "verdict": self.verdict.value,
            "score": self.score,
            "passed": self.passed,
            "total": self.total,
            "checks": [
                {
                    "check_id": check.check_id,
                    "passed": check.passed,
                    "summary": check.summary,
                    "remediation": check.remediation,
                    "evidence": check.evidence,
                }
                for check in self.checks
            ],
        }


FORBIDDEN_PUBLIC_TOOLS: frozenset[str] = frozenset(
    {
        "arif_bridge_connect",
        "arif_gateway_connect",
        "arif_forge",
        "arif_forge_execute",
        "arif_memory",
        "arif_memory_recall",
        "arif_vault_seal",
        "hermes_vault_query",
        "arif_canary",
        "arif_conformance_report",
    }
)

REQUIRED_CORE_TOOLS: frozenset[str] = frozenset(CANONICAL_7)
IRREVERSIBLE_PUBLIC_COMMIT_GATES: frozenset[str] = frozenset({"arif_act", "arif_seal"})


def _tool_names(graph: CapabilityGraph) -> set[str]:
    return {cap.tool_name for cap in graph.capabilities}


def _capabilities_for_tools(graph: CapabilityGraph, tool_names: Iterable[str]):
    wanted = set(tool_names)
    return [cap for cap in graph.capabilities if cap.tool_name in wanted]


def _public_surface_check() -> ReadinessCheck:
    public_tools = set(public_tool_names_for_mode(None))
    expected = set(CANONICAL_7)
    leaked = sorted(public_tools & FORBIDDEN_PUBLIC_TOOLS)
    missing = sorted(expected - public_tools)
    extra = sorted(public_tools - expected)
    passed = not leaked and not missing and not extra and len(public_tools) == 7

    return ReadinessCheck(
        check_id="SURFACE_7_PUBLIC_VERBS",
        passed=passed,
        summary="Default public MCP surface resolves to exactly the seven canonical verbs.",
        remediation="Force default public mode to CANONICAL_7 and keep bridge/forge/memory/vault/canary internal.",
        evidence={
            "public_tools": sorted(public_tools),
            "missing": missing,
            "extra": extra,
            "leaked_forbidden": leaked,
        },
    )


def _capability_graph_core_check(graph: CapabilityGraph) -> ReadinessCheck:
    names = _tool_names(graph)
    missing = sorted(REQUIRED_CORE_TOOLS - names)
    passed = not missing and bool(graph.version.graph_hash)

    return ReadinessCheck(
        check_id="CAPABILITY_GRAPH_COVERS_CORE_SEVEN",
        passed=passed,
        summary="Capability graph contains every canonical public tool and carries a graph hash.",
        remediation="Register every CANONICAL_7 tool as a CapabilityNode and keep graph hashing active.",
        evidence={
            "missing_core_tools": missing,
            "graph_hash_present": bool(graph.version.graph_hash),
            "capability_count": graph.version.capability_count,
        },
    )


def _commit_gate_check(graph: CapabilityGraph) -> ReadinessCheck:
    core_caps = _capabilities_for_tools(graph, REQUIRED_CORE_TOOLS)
    irreversible = sorted(cap.tool_name for cap in core_caps if cap.irreversible)
    passed = set(irreversible).issubset(IRREVERSIBLE_PUBLIC_COMMIT_GATES)

    return ReadinessCheck(
        check_id="ONLY_ACT_AND_SEAL_COMMIT_IRREVERSIBLY",
        passed=passed,
        summary="Only arif_act and arif_seal may be irreversible public commitment gates.",
        remediation="Move irreversible effect out of observe/think/route/judge/init and into act/seal gates.",
        evidence={
            "irreversible_public_core_tools": irreversible,
            "allowed_irreversible_commit_gates": sorted(IRREVERSIBLE_PUBLIC_COMMIT_GATES),
        },
    )


def _mutation_discipline_check(graph: CapabilityGraph) -> ReadinessCheck:
    mutating = [
        cap
        for cap in graph.capabilities
        if cap.mutation_class not in (MutationClass.NONE,) or cap.irreversible
    ]
    unsafe = sorted(
        cap.tool_name
        for cap in mutating
        if not cap.audit_required or cap.allow_python_fallback
    )
    passed = not unsafe

    return ReadinessCheck(
        check_id="MUTATIONS_ARE_AUDITED_NO_UNIVERSAL_FALLBACK",
        passed=passed,
        summary="Mutating capabilities require audit and cannot fall back to unconstrained Python execution.",
        remediation="Set audit_required=True and allow_python_fallback=False for every mutating capability.",
        evidence={
            "mutating_capability_count": len(mutating),
            "unsafe_mutating_tools": unsafe,
        },
    )


def _irreversible_externality_check(graph: CapabilityGraph) -> ReadinessCheck:
    irreversible = [cap for cap in graph.capabilities if cap.irreversible]
    unsafe = sorted(
        cap.tool_name
        for cap in irreversible
        if not (cap.requires_external_witness or cap.requires_external_anchor or cap.requires_888_hold)
    )
    passed = not unsafe

    return ReadinessCheck(
        check_id="IRREVERSIBLE_ACTIONS_REQUIRE_EXTERNALITY_OR_HOLD",
        passed=passed,
        summary="Irreversible capabilities require external witness, external evidence anchor, or 888_HOLD.",
        remediation="Add requires_external_witness, requires_external_anchor, or requires_888_hold to irreversible capabilities.",
        evidence={
            "irreversible_capability_count": len(irreversible),
            "unsafe_irreversible_tools": unsafe,
        },
    )


def _anti_hantu_fallback_check(graph: CapabilityGraph) -> ReadinessCheck:
    fallback_allowed = sorted(cap.tool_name for cap in graph.capabilities if cap.allow_python_fallback)
    passed = not fallback_allowed

    return ReadinessCheck(
        check_id="NO_UNIVERSAL_PYTHON_ESCAPE_HATCH",
        passed=passed,
        summary="No capability may silently degrade into generic Python execution.",
        remediation="Keep allow_python_fallback=False unless a capability is sandboxed, audited, and explicitly ratified.",
        evidence={"fallback_allowed_tools": fallback_allowed},
    )


def assess_substrate_readiness(graph: CapabilityGraph | None = None) -> ReadinessReport:
    """
    Assess whether arifOS satisfies the minimum AGI-substrate invariants.

    READY does not mean AGI. READY means the kernel surface, capability graph,
    mutation discipline, and irreversible-action gates are coherent enough to
    allow agentic execution work to proceed without hantu authority claims.
    """
    graph = graph or _build_default_graph()
    checks = (
        _public_surface_check(),
        _capability_graph_core_check(graph),
        _commit_gate_check(graph),
        _mutation_discipline_check(graph),
        _irreversible_externality_check(graph),
        _anti_hantu_fallback_check(graph),
    )
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    score = round((passed / total) * 100) if total else 0
    verdict = ReadinessVerdict.READY if passed == total else ReadinessVerdict.HOLD
    return ReadinessReport(
        verdict=verdict,
        score=score,
        passed=passed,
        total=total,
        checks=checks,
    )
