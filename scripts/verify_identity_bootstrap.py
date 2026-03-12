import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parents[1]))

from core.organs._0_init import init
from core.shared.types import Verdict


async def test_identity_inference():
    print("Testing Identity Inference...")

    # CASE 1: Basic introduction
    res = await init(query="I am Arif", actor_id="anonymous")
    print(
        f"Query: 'I am Arif' -> Actor: {res.governance.actor_id}, Level: {res.governance.authority_level}, Verdict: {res.verdict}"
    )
    assert res.governance.actor_id == "arif"
    assert res.governance.authority_level == "declared"
    assert res.verdict == Verdict.SEAL

    # CASE 2: Malay introduction
    res = await init(query="Saya adalah ariffazil", actor_id="guest")
    print(
        f"Query: 'Saya adalah ariffazil' -> Actor: {res.governance.actor_id}, Level: {res.governance.authority_level}, Verdict: {res.verdict}"
    )
    assert res.governance.actor_id == "ariffazil"
    assert res.governance.authority_level == "declared"
    assert res.verdict == Verdict.SEAL

    # CASE 3: No introduction
    res = await init(query="Hello there", actor_id="anonymous")
    print(
        f"Query: 'Hello there' -> Actor: {res.governance.actor_id}, Level: {res.governance.authority_level}, Verdict: {res.verdict}"
    )
    assert res.governance.actor_id == "anonymous"
    assert res.governance.authority_level == "anonymous"
    assert res.verdict == Verdict.SEAL

    print("✅ Identity Inference Passed!")


async def test_bootstrap_identity():
    print("\nTesting Bootstrap Identity Tool...")
    from arifosmcp.runtime.tools import bootstrap_identity

    res = await bootstrap_identity(declared_name="Arif-The-Sovereign")
    auth = res.authority
    print(
        f"Declared: 'Arif-The-Sovereign' -> Actor: {auth.actor_id}, Level: {auth.level}, Verdict: {res.verdict}"
    )
    assert auth.actor_id == "arif-the-sovereign"
    assert auth.level == "declared"
    assert res.verdict == Verdict.SEAL

    print("✅ Bootstrap Identity Passed!")


if __name__ == "__main__":
    asyncio.run(test_identity_inference())
    asyncio.run(test_bootstrap_identity())
