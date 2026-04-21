"""
Critical Fix 1: Identity Continuity Authority
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class IdentityStatus(str, Enum):
    ANONYMOUS = "anonymous"
    DECLARED = "declared"
    VERIFIED = "verified"
    DEGRADED = "degraded"

@dataclass
class IdentityAuthority:
    declared_actor_id: str = "anonymous"
    verified_actor_id: str | None = None
    effective_actor_id: str = "anonymous"
    status: IdentityStatus = IdentityStatus.ANONYMOUS
    session_id: str = "global"
    
    def to_contract(self) -> dict[str, Any]:
        return {
            "declared_actor_id": self.declared_actor_id,
            "verified_actor_id": self.verified_actor_id,
            "effective_actor_id": self.effective_actor_id,
            "identity_status": self.status.value,
            "session_id": self.session_id,
        }

    def declare(self, actor_id: str, context: dict = None) -> "IdentityAuthority":
        self.declared_actor_id = actor_id
        self.status = IdentityStatus.DECLARED if actor_id != "anonymous" else IdentityStatus.ANONYMOUS
        self.effective_actor_id = actor_id
        return self

_identity_registry: dict[str, IdentityAuthority] = {}

def get_identity(session_id: str) -> IdentityAuthority:
    if session_id not in _identity_registry:
        _identity_registry[session_id] = IdentityAuthority(session_id=session_id)
    return _identity_registry[session_id]

def set_identity(session_id: str, authority: IdentityAuthority) -> None:
    _identity_registry[session_id] = authority
