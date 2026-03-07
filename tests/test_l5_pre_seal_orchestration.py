"""Focused tests for the L5 pre-seal orchestration contract."""

import importlib
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

PACKAGE_ALIAS = "l5_power_testpkg"
_L5_POWER_PATH = Path(__file__).resolve().parents[1] / "333_APPS" / "L5_AGENTS" / "POWER"
_L5_MISSING = not _L5_POWER_PATH.exists()


def _load_power_package():
    cached = sys.modules.get(PACKAGE_ALIAS)
    if cached is not None:
        return cached

    package_dir = Path(__file__).resolve().parents[1] / "333_APPS" / "L5_AGENTS" / "POWER"
    init_file = package_dir / "__init__.py"
    spec = spec_from_file_location(
        PACKAGE_ALIAS,
        init_file,
        submodule_search_locations=[str(package_dir)],
    )
    assert spec is not None and spec.loader is not None

    package_module = module_from_spec(spec)
    sys.modules[PACKAGE_ALIAS] = package_module
    spec.loader.exec_module(package_module)
    return package_module


def _load_orchestrator_module():
    _load_power_package()
    return importlib.import_module(f"{PACKAGE_ALIAS}.orchestrator")


@pytest.mark.skipif(_L5_MISSING, reason="L5_AGENTS/POWER not present")
async def test_l5_pre_seal_happy_path_returns_seal_and_cycle_complete_true() -> None:
    orchestrator_module = _load_orchestrator_module()

    result = await orchestrator_module.Orchestrator().run(
        "Implement focused contract test coverage"
    )

    assert result["verdict"] == "SEAL"
    assert result["cycle_complete"] is True
    assert result["artifacts"]["validator"]["validated"] is True


@pytest.mark.skipif(_L5_MISSING, reason="L5_AGENTS/POWER not present")
async def test_l5_pre_seal_halts_at_auditor_when_evidence_marker_missing(monkeypatch) -> None:
    orchestrator_module = _load_orchestrator_module()
    agent_result = importlib.import_module(f"{PACKAGE_ALIAS}.base_agent").AgentResult

    class ArchitectWithoutEvidenceMarker:
        async def execute(self, context: dict):
            query = str(context.get("query", "")).strip()
            return agent_result(
                verdict="SEAL",
                data={
                    "query": query,
                    "source": "user_query",
                    "plan": {
                        "scope": {"objective": query},
                        "invariants": ["deterministic behavior"],
                        "handoff": {"owner": "implementation_agent", "next_steps": []},
                        "evidence": [f"query: {query}"],
                    },
                },
            )

    monkeypatch.setattr(orchestrator_module, "ARCHITECT", ArchitectWithoutEvidenceMarker)

    result = await orchestrator_module.Orchestrator().run("Keep orchestrator chain guarded")

    assert result["verdict"] == "SABAR"
    assert result["source"] == "A-AUDITOR"
    assert result["cycle_complete"] is False
    assert "Missing evidence marker: source: user_query" in str(result.get("error", ""))


@pytest.mark.skipif(_L5_MISSING, reason="L5_AGENTS/POWER not present")
async def test_l5_pre_seal_validator_rejects_engineer_objective_mismatch(monkeypatch) -> None:
    orchestrator_module = _load_orchestrator_module()
    agent_result = importlib.import_module(f"{PACKAGE_ALIAS}.base_agent").AgentResult

    class EngineerWithMismatchedObjective:
        async def execute(self, context: dict):
            query = str(context.get("query", "")).strip()
            return agent_result(
                verdict="SEAL",
                data={
                    "query": query,
                    "architect_handoff": {"owner": "implementation_agent", "next_steps": []},
                    "build": {
                        "objective": "different objective",
                        "trace": {
                            "architect_query": query,
                            "architect_source": "user_query",
                        },
                    },
                },
            )

    monkeypatch.setattr(orchestrator_module, "ENGINEER", EngineerWithMismatchedObjective)

    result = await orchestrator_module.Orchestrator().run("Objective to preserve from architect")

    assert result["verdict"] == "SABAR"
    assert result["cycle_complete"] is False
    assert (
        "Engineer build objective does not match architect objective"
        in result["artifacts"]["validator"]["errors"]
    )
