import pytest

from arifosmcp.runtime.governance import wrap_tool_output
from core.organs._0_init import init
from core.organs._1_agi import agi
from core.organs._2_asi import asi
from core.organs._3_apex import apex
from core.organs._4_vault import vault
from core.shared.physics import (
    ConstitutionalTensor,
    GeniusDial,
    PeaceSquared,
    TrinityTensor,
    UncertaintyBand,
)
from core.shared.types import (
    AgiOutput,
    ApexOutput,
    AsiOutput,
    InitOutput,
    VaultOutput,
    Verdict,
)


# Helper to create a valid mock tensor
def create_mock_tensor():
    return ConstitutionalTensor(
        witness=TrinityTensor(H=0.95, A=0.95, S=0.95),
        entropy_delta=-0.1,
        humility=UncertaintyBand(omega_0=0.04),
        genius=GeniusDial(A=0.9, P=0.9, X=0.9, E=1.0),
        peace=PeaceSquared(stakeholder_harms={}),
        empathy=0.96,
        truth_score=0.99,
    )


@pytest.mark.asyncio
async def test_init_output_standardization():
    res = await init("test query", actor_id="user")
    assert isinstance(res, InitOutput)
    assert res.status == "READY"
    assert res.verdict == Verdict.SEAL


@pytest.mark.asyncio
async def test_agi_output_standardization():
    res = await agi("test query", "test-sid")
    assert isinstance(res, AgiOutput)
    assert res.status == "SUCCESS"


@pytest.mark.asyncio
async def test_asi_output_standardization():
    res = await asi(action="full", session_id="test-sid", scenario="test query")
    assert isinstance(res, AsiOutput)
    assert res.status == "SUCCESS"


@pytest.mark.asyncio
async def test_apex_output_standardization():
    res = await apex(action="full", session_id="test-sid", verdict_candidate="SEAL")
    assert isinstance(res, ApexOutput)
    assert res.status == "SUCCESS"


@pytest.mark.asyncio
async def test_vault_output_standardization():
    res = await vault(
        operation="seal",
        session_id="test-sid",
        summary="test query",
        verdict="SEAL",
    )
    assert isinstance(res, VaultOutput)
    assert res.status == "SUCCESS"


def test_governance_apex_output_math_and_meaning_are_aligned():
    payload = {
        "session_id": "s1",
        "verdict": "SEAL",
        "dS": -0.25,
        "peace2": 1.05,
        "kappa_r": 0.96,
        "omega0": 0.04,
        "truth": {"score": 0.98},
        "energy": 0.8,
        "tokens": 240,
        "compute_ms": 180,
        "steps": 3,
        "tool_calls": 2,
        "evidence": ["a"],
        "actor": "user",
        "auth": "token",
        "human_witness": 0.98,
        "ai_witness": 0.97,
        "earth_witness": 0.96,
    }
    apex_output = wrap_tool_output("reason_mind", payload)["apex_output"]
    capacity = apex_output["capacity_layer"]
    effort = apex_output["effort_layer"]
    entropy = apex_output["entropy_layer"]
    efficiency = apex_output["efficiency_layer"]
    governed = apex_output["governed_intelligence"]
    governance = apex_output["governance_layer"]
    diagnostics = apex_output["diagnostics"]

    assert capacity["capacity_product"] == pytest.approx(
        capacity["A"] * capacity["P"] * capacity["X"], abs=1e-4
    )
    assert effort["effort_amplifier"] == pytest.approx(effort["E"] ** 2, abs=1e-4)
    assert entropy["delta_S"] == pytest.approx(entropy["H_before"] - entropy["H_after"], abs=1e-4)
    assert efficiency["eta"] == pytest.approx(
        efficiency["entropy_removed"] / efficiency["C"], abs=1e-6
    )
    assert governed["G_dagger"] == pytest.approx(
        governed["G_star"] * efficiency["eta"], abs=1e-4
    )

    assert governance["status"] == "attested"
    assert diagnostics["primary_constraint"] == "effort"
    assert "Structural headroom is strong" in capacity["meaning"]
    assert "Very little reasoning effort" in effort["meaning"]
    assert "Entropy fell" in entropy["meaning"]
    assert "Compute spend is outpacing clarity gain" in efficiency["meaning"]
    assert "Governance is aligned" in governance["meaning"]
    assert "governance is attested" in diagnostics["runtime_story"]
