import asyncio
from typing import Any, Dict, List

import pytest

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
    FloorScores,
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
    assert res.status == "SUCCESS"
    assert res.verdict == Verdict.SEAL


@pytest.mark.asyncio
async def test_agi_output_standardization():
    res = await agi("test query", "test-sid")
    assert isinstance(res, AgiOutput)
    assert res.status == "SUCCESS"


@pytest.mark.asyncio
async def test_asi_output_standardization():
    agi_tensor = create_mock_tensor()
    res = await asi("empathize", agi_tensor, "test-sid", query="test query")
    assert isinstance(res, AsiOutput)
    assert res.status == "SUCCESS"


@pytest.mark.asyncio
async def test_apex_output_standardization():
    # Mock data
    agi_tensor = create_mock_tensor()
    asi_output = {"peace_squared": 1.0, "kappa_r": 0.8}
    res = await apex(agi_tensor, asi_output, "test-sid", action="full")
    assert isinstance(res, ApexOutput)
    assert res.status == "SUCCESS"


@pytest.mark.asyncio
async def test_vault_output_standardization():
    agi_tensor = create_mock_tensor()
    judge_out = {"verdict": "SEAL", "W_3": 0.98, "genius_G": 0.85}
    asi_out = {"peace_squared": 1.0}
    res = await vault("seal", judge_out, agi_tensor, asi_out, "test-sid", "test query")
    assert isinstance(res, VaultOutput)
    assert res.status == "SUCCESS"
