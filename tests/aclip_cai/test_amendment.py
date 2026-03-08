"""
tests/arifosmcp.intelligence/test_amendment.py
"""

import pytest
from arifosmcp.intelligence.core.amendment import AmendmentChain, AmendmentState


def test_propose_amendment():
    chain = AmendmentChain()  # in-memory
    rec = chain.propose("Test Law", "Should always pass", "arif")

    assert rec.title == "Test Law"
    assert rec.state == AmendmentState.COOLING


def test_hantu_rejection():
    chain = AmendmentChain()
    with pytest.raises(ValueError, match="Anti-Hantu"):
        chain.propose("Bad Law", "I am a sentient AI", "rogue")


def test_amendment_summary():
    chain = AmendmentChain()
    chain.propose("L1", "desc", "u1")

    summ = chain.summary()
    assert summ["total"] == 1
    assert summ["cooling"] == 1
