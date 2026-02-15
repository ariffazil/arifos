"""
arifOS L5: Agent Federation + SDK
=================================
Constitutional multi-agent system for governed AI.

4 Agents:
- Architect: Plans and designs (✅ WORKING)
- Engineer: Implements and executes (🔴 STUB)
- Auditor: Checks compliance (🔴 STUB)
- Validator: Final consensus (🔴 STUB)

SDK:
- ArifOS: Client for governed AI
- client.ask(): Run full L5 federation
- client.reflect(): Meta-AGI analysis
- client.audit(): Query VAULT-999

Quick Start:
    from L5_AGENTS import ArifOS
    
    client = ArifOS()
    result = await client.ask("What is entropy?")
    print(result.answer)

Status: v55.3-L5-alpha
- Architect: ✅ Full implementation
- SDK: ✅ Full implementation
- Engineer/Auditor/Validator: 🔴 Stubs (coming v55.4)

Version: v55.3-L5-alpha
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
"""

from .base_agent import (
    BaseAgent,
    AgentOutput,
    AgentMessage,
    FloorScores,
    Verdict,
)

from .architect import (
    Architect,
    ArchitectPlan,
    PlanStep,
)

from .engineer import Engineer
from .auditor import Auditor
from .validator import Validator

from .federation import (
    AgentFederation,
    FederationResult,
)

from .sdk import (
    ArifOS,
    AskResponse,
    ReflectResponse,
    AuditEntry,
    Session,
    ResponseStatus,
    ask,
)


__version__ = "55.3.0-L5-alpha"
__author__ = "Muhammad Arif bin Fazil"
__license__ = "AGPL-3.0-only"

__all__ = [
    # Base
    "BaseAgent",
    "AgentOutput",
    "AgentMessage",
    "FloorScores",
    "Verdict",
    # Agents
    "Architect",
    "ArchitectPlan",
    "PlanStep",
    "Engineer",
    "Auditor",
    "Validator",
    # Federation
    "AgentFederation",
    "FederationResult",
    # SDK
    "ArifOS",
    "AskResponse",
    "ReflectResponse",
    "AuditEntry",
    "Session",
    "ResponseStatus",
    "ask",
]
