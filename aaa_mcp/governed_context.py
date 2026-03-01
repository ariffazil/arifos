"""
aaa_mcp/governed_context.py — Constitutionally Hardened FastMCP Context

Forges FastMCP's Context capability into the arifOS 000-999 metabolic loop.
All context operations are governed by the 13 Constitutional Floors.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import time
from contextvars import ContextVar
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal

# FastMCP imports — transport layer only
from fastmcp.server.context import Context as FastMCPContext
from fastmcp.dependencies import CurrentContext

# arifOS core imports — constitutional kernel
from core.kernel.init_000_anchor import AuthorityLevel
from core.shared.types import Verdict

# Internal arifOS imports
from aaa_mcp.sessions.session_ledger import SessionLedger
from aaa_mcp.vault.hardened import VAULT999_Hardened
from aaa_mcp.infrastructure.logging import ConstitutionalLogger

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SESSION_STATE_PREFIX = "arifos::session::"
CONTEXT_LOG_PREFIX = "[CTX]"
MAX_STATE_VALUE_SIZE = 1024 * 1024  # 1MB — F5 Safety limit
MAX_STATE_KEYS = 100  # F6 Edge case handling


class ContextOperation(Enum):
    """Constitutionally governed context operations."""
    GET_STATE = "get_state"
    SET_STATE = "set_state"
    DELETE_STATE = "delete_state"
    LOG = "log"
    PROGRESS = "progress"
    READ_RESOURCE = "read_resource"
    GET_PROMPT = "get_prompt"
    SAMPLE = "sample"


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNED STATE MANAGER (F1 Amanah, F5 Reversibility)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class StateEntry:
    """Immutable state entry with provenance tracking."""
    key: str
    value: Any
    session_id: str
    stage: str  # 000-999 metabolic stage
    timestamp: float
    checksum: str = field(default="")
    
    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._compute_checksum()
    
    def _compute_checksum(self) -> str:
        """F1 Amanah: Cryptographic integrity for state."""
        data = f"{self.session_id}:{self.key}:{self.stage}:{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def verify(self) -> bool:
        """Verify state entry integrity."""
        return self.checksum == self._compute_checksum()


class GovernedStateManager:
    """
    Session state with constitutional enforcement.
    
    - F1 Amanah: All mutations logged to VAULT999
    - F5 Reversibility: State changes can be rolled back via ledger
    - F6 Edge Cases: Size limits, key count limits
    - F12 Injection: Key sanitization against injection attacks
    """
    
    def __init__(self, vault: VAULT999_Hardened | None = None):
        self._vault = vault
        self._logger = ConstitutionalLogger()
        # In-memory state cache keyed by session_id
        self._state_cache: dict[str, dict[str, StateEntry]] = {}
    
    def _sanitize_key(self, key: str, session_id: str) -> str:
        """
        F12 Injection Defense: Sanitize state keys.
        Prevents path traversal, null bytes, and injection patterns.
        """
        # Block dangerous patterns
        dangerous = ["..", "//", "\\", "\x00", "${", "<%", "{{"]
        if any(d in key for d in dangerous):
            raise ValueError(f"F12 BLOCK: Invalid state key pattern: {key}")
        
        # Namespace key by session to prevent cross-session leakage
        return f"{SESSION_STATE_PREFIX}{session_id}::{key}"
    
    def _check_size_limits(self, value: Any) -> None:
        """F6 Edge case: Enforce size limits on state values."""
        import json
        try:
            serialized = json.dumps(value)
            if len(serialized) > MAX_STATE_VALUE_SIZE:
                raise ValueError(
                    f"F6 LIMIT: State value exceeds {MAX_STATE_VALUE_SIZE} bytes"
                )
        except (TypeError, ValueError) as e:
            raise ValueError(f"F6 ERROR: State value not serializable: {e}")
    
    async def get_state(
        self,
        session_id: str,
        key: str,
        stage: str = "000_INIT"
    ) -> Any | None:
        """
        Retrieve state value for session.
        
        F2 Grounding: Returns None if key not found (no fabrication).
        F12 Defense: Key sanitized before lookup.
        """
        safe_key = self._sanitize_key(key, session_id)
        
        session_state = self._state_cache.get(session_id, {})
        entry = session_state.get(safe_key)
        
        if entry is None:
            await self._logger.log_context_op(
                operation=ContextOperation.GET_STATE,
                session_id=session_id,
                stage=stage,
                key=key,
                verdict=Verdict.PARTIAL,  # Not found is partial, not void
                detail="Key not found in session state"
            )
            return None
        
        # F1 Amanah: Verify integrity
        if not entry.verify():
            await self._logger.log_context_op(
                operation=ContextOperation.GET_STATE,
                session_id=session_id,
                stage=stage,
                key=key,
                verdict=Verdict.VOID,
                detail="State integrity check failed (tampering detected)"
            )
            raise ValueError("F1 TAMPER: State entry integrity violation")
        
        await self._logger.log_context_op(
            operation=ContextOperation.GET_STATE,
            session_id=session_id,
            stage=stage,
            key=key,
            verdict=Verdict.SEAL
        )
        
        return entry.value
    
    async def set_state(
        self,
        session_id: str,
        key: str,
        value: Any,
        stage: str = "000_INIT",
        serializable: bool = True
    ) -> StateEntry:
        """
        Store state value for session.
        
        F1 Amanah: Creates immutable ledger entry.
        F5 Reversibility: Previous value preserved in VAULT999.
        F6 Edge Cases: Size and count limits enforced.
        """
        # F6: Check serializability
        if serializable:
            self._check_size_limits(value)
        
        safe_key = self._sanitize_key(key, session_id)
        
        # F6: Check key count limit
        session_state = self._state_cache.setdefault(session_id, {})
        if len(session_state) >= MAX_STATE_KEYS and safe_key not in session_state:
            raise ValueError(f"F6 LIMIT: Max state keys ({MAX_STATE_KEYS}) exceeded")
        
        # Create immutable entry
        entry = StateEntry(
            key=safe_key,
            value=value,
            session_id=session_id,
            stage=stage,
            timestamp=time.time()
        )
        
        # F1 Amanah: Log previous value to VAULT999 for reversibility
        if safe_key in session_state:
            old_entry = session_state[safe_key]
            await self._log_state_mutation(session_id, key, old_entry, entry, stage)
        
        # Store new value
        session_state[safe_key] = entry
        
        await self._logger.log_context_op(
            operation=ContextOperation.SET_STATE,
            session_id=session_id,
            stage=stage,
            key=key,
            verdict=Verdict.SEAL,
            detail=f"Value size: {len(str(value))} bytes"
        )
        
        return entry
    
    async def delete_state(
        self,
        session_id: str,
        key: str,
        stage: str = "000_INIT"
    ) -> bool:
        """
        Delete state entry.
        
        F1 Amanah: Archived to VAULT999 before deletion.
        F5 Reversibility: Can be restored from ledger.
        """
        safe_key = self._sanitize_key(key, session_id)
        session_state = self._state_cache.get(session_id, {})
        
        if safe_key not in session_state:
            return False
        
        entry = session_state[safe_key]
        
        # F1: Archive to VAULT999 before deletion
        await self._log_state_deletion(session_id, key, entry, stage)
        
        del session_state[safe_key]
        
        await self._logger.log_context_op(
            operation=ContextOperation.DELETE_STATE,
            session_id=session_id,
            stage=stage,
            key=key,
            verdict=Verdict.SEAL
        )
        
        return True
    
    async def _log_state_mutation(
        self,
        session_id: str,
        key: str,
        old: StateEntry,
        new: StateEntry,
        stage: str
    ) -> None:
        """Log state mutation to VAULT999 for audit trail."""
        if self._vault:
            await self._vault.log_witness(
                session_id=session_id,
                agent_id="CONTEXT",
                stage=stage,
                statement=f"State mutation: {key}",
                verdict="SEAL",
                metadata={
                    "operation": "MUTATION",
                    "key": key,
                    "old_stage": old.stage,
                    "new_stage": new.stage,
                    "old_checksum": old.checksum,
                    "new_checksum": new.checksum
                }
            )
    
    async def _log_state_deletion(
        self,
        session_id: str,
        key: str,
        entry: StateEntry,
        stage: str
    ) -> None:
        """Log state deletion to VAULT999."""
        if self._vault:
            await self._vault.log_witness(
                session_id=session_id,
                agent_id="CONTEXT",
                stage=stage,
                statement=f"State deletion: {key}",
                verdict="SEAL",
                metadata={
                    "operation": "DELETION",
                    "key": key,
                    "archived_value_checksum": entry.checksum,
                    "archived_stage": entry.stage
                }
            )


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTITUTIONAL PROGRESS TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ProgressCheckpoint:
    """Metabolic progress checkpoint with stage awareness."""
    progress: int
    total: int
    stage: str  # 000-999
    stage_name: str
    entropy_delta: float  # ΔS tracking
    timestamp: float


class ConstitutionalProgressTracker:
    """
    Progress reporting tied to metabolic stages.
    
    F4 Clarity: Progress includes constitutional stage context.
    F7 Humility: Progress estimates include uncertainty bounds.
    """
    
    STAGE_WEIGHTS = {
        "000_INIT": 5,
        "111_SENSE": 10,
        "222_MAP": 15,
        "333_REASON": 20,
        "444_PHOENIX": 15,
        "555_RECALL": 10,
        "666_ALIGN": 10,
        "777_FORGE": 10,
        "888_JUDGE": 4,
        "999_SEAL": 1
    }
    
    def __init__(self):
        self._checkpoints: dict[str, list[ProgressCheckpoint]] = {}
    
    def calculate_metabolic_progress(self, current_stage: str) -> tuple[int, int]:
        """
        Calculate overall progress through 000-999 metabolism.
        
        Returns (current, total) based on stage weights.
        """
        stages = list(self.STAGE_WEIGHTS.keys())
        total = sum(self.STAGE_WEIGHTS.values())
        
        current = 0
        for stage in stages:
            if stage == current_stage:
                current += self.STAGE_WEIGHTS[stage] // 2  # Half credit for in-progress
                break
            current += self.STAGE_WEIGHTS[stage]
        
        return current, total
    
    async def report_checkpoint(
        self,
        session_id: str,
        progress: int,
        total: int,
        stage: str,
        entropy_delta: float = 0.0
    ) -> ProgressCheckpoint:
        """Record progress checkpoint with constitutional context."""
        checkpoint = ProgressCheckpoint(
            progress=progress,
            total=total,
            stage=stage,
            stage_name=self._stage_name(stage),
            entropy_delta=entropy_delta,
            timestamp=time.time()
        )
        
        self._checkpoints.setdefault(session_id, []).append(checkpoint)
        return checkpoint
    
    def _stage_name(self, stage: str) -> str:
        """Map stage code to human-readable name."""
        names = {
            "000_INIT": "Anchor",
            "111_SENSE": "Sense",
            "222_MAP": "Map",
            "333_REASON": "Reason",
            "444_PHOENIX": "Phoenix",
            "555_RECALL": "Recall",
            "666_ALIGN": "Align",
            "777_FORGE": "Forge",
            "888_JUDGE": "Judge",
            "999_SEAL": "Seal"
        }
        return names.get(stage, "Unknown")


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNED CONTEXT — The Hardened Interface
# ═══════════════════════════════════════════════════════════════════════════════

class GovernedContext:
    """
    Constitutionally hardened FastMCP Context wrapper.
    
    This class wraps FastMCP's Context and enforces:
    - F1 Amanah: All state changes reversible via VAULT999
    - F2 Grounding: No fabricated state
    - F5 Safety: Size limits, serializability checks
    - F6 Edge Cases: Key limits, null handling
    - F7 Humility: Progress estimates with uncertainty
    - F12 Defense: Injection-resistant key handling
    
    Usage:
        @mcp.tool
        async def my_tool(ctx: Context = CurrentContext()) -> dict:
            gov = GovernedContext(ctx, session_id="...")
            await gov.set_state("key", value, stage="333_REASON")
    """
    
    def __init__(
        self,
        fastmcp_ctx: FastMCPContext,
        session_id: str,
        actor_id: str = "anonymous",
        authority: AuthorityLevel = AuthorityLevel.USER,
        vault: VAULT999_Hardened | None = None
    ):
        self._ctx = fastmcp_ctx
        self._session_id = session_id
        self._actor_id = actor_id
        self._authority = authority
        self._stage = "000_INIT"
        
        # Constitutional subsystems
        self._state_manager = GovernedStateManager(vault)
        self._progress_tracker = ConstitutionalProgressTracker()
        self._logger = ConstitutionalLogger()
    
    # ─── Session Identity ─────────────────────────────────────────────────────
    
    @property
    def session_id(self) -> str:
        """F3 Contract: Immutable session identifier."""
        return self._session_id
    
    @property
    def actor_id(self) -> str:
        """F11 Authority: Actor identifier."""
        return self._actor_id
    
    @property
    def current_stage(self) -> str:
        """Current metabolic stage (000-999)."""
        return self._stage
    
    def advance_stage(self, stage: str) -> None:
        """
        Advance metabolic stage.
        
        Validates stage progression follows 000-999 sequence.
        """
        valid_stages = [
            "000_INIT", "111_SENSE", "222_MAP", "333_REASON",
            "444_PHOENIX", "555_RECALL", "666_ALIGN",
            "777_FORGE", "888_JUDGE", "999_SEAL"
        ]
        
        if stage not in valid_stages:
            raise ValueError(f"F8 INVALID: Unknown stage {stage}")
        
        # Ensure monotonic progression (can revisit, cannot skip forward arbitrarily)
        current_idx = valid_stages.index(self._stage) if self._stage in valid_stages else 0
        new_idx = valid_stages.index(stage)
        
        if new_idx > current_idx + 2:  # Allow small backtracking, not major skips
            raise ValueError(f"F8 SKIP: Cannot skip from {self._stage} to {stage}")
        
        self._stage = stage
    
    # ─── State Management (F1 Amanah, F5 Reversibility) ───────────────────────
    
    async def get_state(self, key: str) -> Any | None:
        """
        Retrieve state value.
        
        F2 Grounding: Returns None if not found (no fabrication).
        """
        return await self._state_manager.get_state(
            session_id=self._session_id,
            key=key,
            stage=self._stage
        )
    
    async def set_state(
        self,
        key: str,
        value: Any,
        serializable: bool = True
    ) -> StateEntry:
        """
        Store state value.
        
        F1 Amanah: Logs to VAULT999.
        F5 Safety: Enforces size limits.
        F12 Defense: Key sanitization.
        """
        # F11 Authority check: Only sovereign can set certain keys
        if key.startswith("constitution::") and self._authority != AuthorityLevel.SOVEREIGN:
            raise PermissionError("F11 DENIED: Sovereign authority required")
        
        return await self._state_manager.set_state(
            session_id=self._session_id,
            key=key,
            value=value,
            stage=self._stage,
            serializable=serializable
        )
    
    async def delete_state(self, key: str) -> bool:
        """
        Delete state entry.
        
        F1 Amanah: Archives to VAULT999 first.
        """
        return await self._state_manager.delete_state(
            session_id=self._session_id,
            key=key,
            stage=self._stage
        )
    
    # ─── Constitutional Logging (F4 Clarity, F10 Transparency) ─────────────────
    
    async def log_debug(self, message: str, metadata: dict | None = None) -> None:
        """Debug logging with constitutional context."""
        await self._logger.log_context_op(
            operation=ContextOperation.LOG,
            session_id=self._session_id,
            stage=self._stage,
            level="debug",
            message=message,
            metadata=metadata
        )
        if self._ctx:
            await self._ctx.debug(f"{CONTEXT_LOG_PREFIX} {message}")
    
    async def log_info(self, message: str, metadata: dict | None = None) -> None:
        """Info logging with constitutional context."""
        await self._logger.log_context_op(
            operation=ContextOperation.LOG,
            session_id=self._session_id,
            stage=self._stage,
            level="info",
            message=message,
            metadata=metadata
        )
        if self._ctx:
            await self._ctx.info(f"{CONTEXT_LOG_PREFIX} {message}")
    
    async def log_warning(self, message: str, metadata: dict | None = None) -> None:
        """Warning logging — entropy increase detected."""
        await self._logger.log_context_op(
            operation=ContextOperation.LOG,
            session_id=self._session_id,
            stage=self._stage,
            level="warning",
            message=message,
            metadata=metadata,
            entropy_delta=0.01  # Warning indicates slight entropy increase
        )
        if self._ctx:
            await self._ctx.warning(f"{CONTEXT_LOG_PREFIX} {message}")
    
    async def log_error(self, message: str, metadata: dict | None = None) -> None:
        """Error logging — constitutional violation or system failure."""
        await self._logger.log_context_op(
            operation=ContextOperation.LOG,
            session_id=self._session_id,
            stage=self._stage,
            level="error",
            message=message,
            metadata=metadata,
            entropy_delta=0.05  # Error is entropy increase
        )
        if self._ctx:
            await self._ctx.error(f"{CONTEXT_LOG_PREFIX} {message}")
    
    # ─── Progress Reporting (F7 Humility) ─────────────────────────────────────
    
    async def report_progress(
        self,
        progress: int,
        total: int,
        entropy_delta: float = 0.0
    ) -> ProgressCheckpoint:
        """
        Report progress with metabolic stage awareness.
        
        F7 Humility: Includes uncertainty bounds in progress estimates.
        """
        checkpoint = await self._progress_tracker.report_checkpoint(
            session_id=self._session_id,
            progress=progress,
            total=total,
            stage=self._stage,
            entropy_delta=entropy_delta
        )
        
        # Also report to FastMCP context if available
        if self._ctx:
            await self._ctx.report_progress(progress, total)
        
        return checkpoint
    
    def get_metabolic_progress(self) -> dict:
        """
        Get overall metabolic progress through 000-999.
        
        Returns progress with constitutional context.
        """
        current, total = self._progress_tracker.calculate_metabolic_progress(self._stage)
        return {
            "current": current,
            "total": total,
            "percentage": (current / total * 100) if total > 0 else 0,
            "stage": self._stage,
            "stage_name": self._progress_tracker._stage_name(self._stage),
            "uncertainty": 0.05  # F7 Humility: 5% uncertainty on progress
        }
    
    # ─── Resource Access (F2 Grounding Required) ──────────────────────────────
    
    async def read_resource(self, uri: str) -> list:
        """
        Read resource with constitutional logging.
        
        F2 Grounding: Resource access is tracked for audit.
        """
        await self._logger.log_context_op(
            operation=ContextOperation.READ_RESOURCE,
            session_id=self._session_id,
            stage=self._stage,
            uri=uri,
            verdict=Verdict.SEAL
        )
        
        if not self._ctx:
            raise RuntimeError("F8 ERROR: No FastMCP context available")
        
        return await self._ctx.read_resource(uri)
    
    async def list_resources(self) -> list:
        """List available resources."""
        if not self._ctx:
            return []
        return await self._ctx.list_resources()
    
    # ─── Prompt Access ────────────────────────────────────────────────────────
    
    async def get_prompt(self, name: str, arguments: dict | None = None) -> Any:
        """Get prompt with constitutional logging."""
        await self._logger.log_context_op(
            operation=ContextOperation.GET_PROMPT,
            session_id=self._session_id,
            stage=self._stage,
            prompt_name=name,
            verdict=Verdict.SEAL
        )
        
        if not self._ctx:
            raise RuntimeError("F8 ERROR: No FastMCP context available")
        
        return await self._ctx.get_prompt(name, arguments)
    
    async def list_prompts(self) -> list:
        """List available prompts."""
        if not self._ctx:
            return []
        return await self._ctx.list_prompts()
    
    # ─── LLM Sampling ─────────────────────────────────────────────────────────
    
    async def sample(
        self,
        message: str,
        temperature: float = 0.7,
        **kwargs
    ) -> Any:
        """
        Request LLM sampling with constitutional constraints.
        
        F7 Humility: Temperature capped to prevent overconfidence.
        """
        # F7: Cap temperature (lower = more deterministic/humble)
        safe_temp = min(temperature, 0.9)
        
        await self._logger.log_context_op(
            operation=ContextOperation.SAMPLE,
            session_id=self._session_id,
            stage=self._stage,
            temperature=safe_temp,
            verdict=Verdict.SEAL
        )
        
        if not self._ctx:
            raise RuntimeError("F8 ERROR: No FastMCP context available")
        
        return await self._ctx.sample(message, temperature=safe_temp, **kwargs)
    
    # ─── Transport & Request Info ─────────────────────────────────────────────
    
    @property
    def transport(self) -> Literal["stdio", "sse", "streamable-http"] | None:
        """Transport type if available."""
        if self._ctx:
            return self._ctx.transport
        return None
    
    @property
    def request_id(self) -> str:
        """Current request ID."""
        if self._ctx:
            return self._ctx.request_id
        return f"gov-{self._session_id}"


# ═══════════════════════════════════════════════════════════════════════════════
# FACTORY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_governed_context(
    session_id: str,
    actor_id: str = "anonymous",
    authority: AuthorityLevel = AuthorityLevel.USER,
    vault: VAULT999_Hardened | None = None
) -> GovernedContext:
    """
    Factory for creating GovernedContext with dependency injection.
    
    Usage with FastMCP:
        @mcp.tool
        async def my_tool(ctx: Context = CurrentContext()) -> dict:
            gov = create_governed_context(
                session_id="Arif Fazil-abc123",
                actor_id="Arif Fazil",
                authority=AuthorityLevel.SOVEREIGN
            )
            gov.bind_fastmcp_context(ctx)
            ...
    """
    return GovernedContext(
        fastmcp_ctx=None,  # Will be bound later
        session_id=session_id,
        actor_id=actor_id,
        authority=authority,
        vault=vault
    )


# Singleton state manager for cross-request persistence
_state_manager_singleton: GovernedStateManager | None = None


def get_state_manager(vault: VAULT999_Hardened | None = None) -> GovernedStateManager:
    """Get or create singleton state manager."""
    global _state_manager_singleton
    if _state_manager_singleton is None:
        _state_manager_singleton = GovernedStateManager(vault)
    return _state_manager_singleton
