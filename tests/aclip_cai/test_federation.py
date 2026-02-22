"""
tests/aclip_cai/test_federation.py
"""

import pytest
from aclip_cai.core.federation import FederationCoordinator, AgentStatus, AgentHealth

def test_federation_registration():
    coord = FederationCoordinator()
    coord.register("agent-1", lambda: AgentHealth(agent_id="agent-1", status=AgentStatus.HEALTHY, last_check="now"))
    
    report = coord.federation_report()
    assert report["total_agents"] == 1
    assert report["agents"]["agent-1"] == "healthy"

def test_earth_witness_score():
    coord = FederationCoordinator()
    coord.register("a1", lambda: AgentHealth(agent_id="a1", status=AgentStatus.HEALTHY, last_check="now"))
    coord.register("a2", lambda: AgentHealth(agent_id="a2", status=AgentStatus.OFFLINE, last_check="now"))
    
    # E = fraction healthy = 1/2 = 0.5
    score = coord.earth_witness_score()
    assert score == 0.5
