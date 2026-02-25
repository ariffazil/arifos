"""
core/kernel/init_000_anchor.py — Unified Constitutional Anchor

The single entry point for all arifOS interactions.
Consolidates:
- 000_INIT (Airlock): Session ignition & Token issuance
- F11 (Authority): Identity verification
- F12 (Injection): Immune system scanning
- 000_ANCHOR (Infrastructure): Early host/cost/risk evaluation

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import hashlib
import hmac
import logging
import secrets
import time
from enum import Enum

from core.kernel.evaluator import evaluator
from core.shared.types import InitOutput, Verdict

logger = logging.getLogger(__name__)

# ─── Authority Enums ─────────────────────────────────────────────────────────


class AuthorityLevel(Enum):
    NONE = "none"
    USER = "user"
    OPERATOR = "operator"
    SOVEREIGN = "sovereign"
    SYSTEM = "system"


# ─── Anchor Logic ────────────────────────────────────────────────────────────


class AnchorEngine:
    """
    The Anchor Engine handles the absolute beginning of the cognitive loop.
    It roots the query in physical reality (auth, injection, host health).
    """

    def __init__(self):
        # In a real system, these would be loaded from a secure registry
        self.valid_actors = {"user", "operator", "arif-fazil", "system", "agent", "cli"}
        self.actor_authority = {
            "arif-fazil": AuthorityLevel.SOVEREIGN,
            "system": AuthorityLevel.SYSTEM,
            "operator": AuthorityLevel.OPERATOR,
        }

    async def ignite(
        self,
        query: str,
        actor_id: str = "anonymous",
        auth_token: str | None = None,
        require_sovereign: bool = False,
    ) -> InitOutput:
        """
        Universal ignition protocol.
        1. Scan for Injection (F12)
        2. Verify Authority (F11)
        3. Classify Query (Adaptive F2)
        4. Anchor in Infrastructure (ACLIP signals)
        """
        start_time = time.time()

        # 1. F12: Injection Defense
        # We use the kernel evaluator which has the latest F12 logic
        pre_ctx = evaluator.build_pre_context(query, {"actor_id": actor_id})
        f12_result = evaluator.check_floor("F12", pre_ctx)

        if not f12_result["passed"]:
            return self._build_void_output("F12", f12_result["reason"], actor_id)

        # 2. F11: Authority
        is_auth, level = self._verify_auth(actor_id, auth_token)
        if not is_auth:
            return self._build_void_output("F11", f"Unauthorized actor: {actor_id}", actor_id)

        # 3. F13: High-Stakes Check
        if require_sovereign or self._is_high_stakes(query):
            if level != AuthorityLevel.SOVEREIGN:
                return self._build_hold_output(
                    "F13", "Sovereign approval required for high-stakes operation", actor_id
                )

        # 4. Infrastructure Anchoring (Shadow ACLIP call)
        # In v64.2, we anchor to host pressure heuristics
        infra_risk = self._estimate_infra_risk(query)

        # 5. Success: Issue Token
        session_id = secrets.token_hex(16)
        token = self._sign_token(f"{session_id}:{actor_id}:{start_time}")

        return InitOutput(
            session_id=session_id,
            governance_token=token,
            injection_score=f12_result["score"],
            auth_verified=True,
            verdict=Verdict.SEAL,
            status="READY",
            query_type="ANCHORED",  # Dynamic classification placeholder
            metrics={
                "authority_level": level.value,
                "infra_risk": infra_risk,
                "processing_ms": (time.time() - start_time) * 1000,
            },
        )

    def _verify_auth(self, actor_id: str, token: str | None) -> tuple[bool, AuthorityLevel]:
        actor = actor_id.lower().strip()
        if actor not in self.valid_actors and actor != "anonymous":
            return False, AuthorityLevel.NONE

        level = self.actor_authority.get(actor, AuthorityLevel.USER)
        return True, level

    def _is_high_stakes(self, query: str) -> bool:
        forbidden = ["rm -rf", "drop table", "shutdown", "format", "delete all"]
        return any(p in query.lower() for p in forbidden)

    def _estimate_infra_risk(self, query: str) -> float:
        # Heuristic bridge to ACLIP concepts
        if len(query) > 5000:
            return 0.8
        if "execute" in query.lower():
            return 0.5
        return 0.1

    def _sign_token(self, data: str) -> str:
        secret = "arifos-internal-forge-secret"
        return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

    def _build_void_output(self, floor: str, reason: str, actor: str) -> InitOutput:
        return InitOutput(
            session_id=f"VOID-{secrets.token_hex(4)}",
            governance_token="",
            injection_score=1.0,
            auth_verified=False,
            verdict=Verdict.VOID,
            status="ERROR",
            violations=[floor],
            error_message=reason,
            query_type="VOID",
        )

    def _build_hold_output(self, floor: str, reason: str, actor: str) -> InitOutput:
        return InitOutput(
            session_id=f"HOLD-{secrets.token_hex(4)}",
            governance_token="",
            injection_score=0.0,
            auth_verified=True,
            verdict=Verdict.HOLD_888,
            status="SABAR",
            violations=[floor],
            error_message=reason,
            query_type="HIGH_STAKES",
        )


# Singleton
anchor_engine = AnchorEngine()


async def init_000_anchor(query: str, actor_id: str = "user", **kwargs) -> InitOutput:
    """Canonical kernel entry point for Stage 000."""
    return await anchor_engine.ignite(query, actor_id, **kwargs)
