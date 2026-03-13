"""
AgentZero MCP Tools — Constitutional Agent Parliament Interface

Exposes AgentZero agents as MCP tools for governed autonomous operations.
Version: 2026.03.13-H1
Author: Muhammad Arif bin Fazil [ΔΩΨ | ARIF]

Tools:
- agentzero_validate: ValidatorAgent (Ψ - APEX) constitutional verification
- agentzero_engineer: EngineerAgent (Ω - HEART) F11-gated code execution
- agentzero_hold_check: 888 HOLD state status query
- agentzero_memory_query: Constitutional memory with F-floor filtering
- agentzero_armor_scan: F12 injection detection
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastmcp import Context

from arifosmcp.runtime.models import (
    CallerContext,
    RuntimeEnvelope,
    RuntimeStatus,
    Stage,
    Verdict,
)


logger = logging.getLogger(__name__)


async def agentzero_validate(
    target: str,
    validation_type: str = "code",
    context: str = "",
    require_human_approval: bool = False,
    session_id: str = "global",
    auth_context: Dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """
    ValidatorAgent (Ψ - APEX): Constitutional verification of code, output, or action.
    
    The ValidatorAgent serves as the final judge, issuing verdicts and triggering
    888_HOLD escalations when necessary. It enforces F1, F3, F10, F11, F13.
    
    Use this for:
    - Pre-deployment code validation
    - Constitutional compliance checks
    - Verdict issuance before irreversible actions
    - Triggering 888_HOLD for human approval
    
    Args:
        target: The code, output, or action to validate
        validation_type: Type of validation ("code", "output", "action", "plan")
        context: Additional context for validation
        require_human_approval: Force 888_HOLD escalation
        session_id: Session identifier for continuity
    """
    from arifosmcp.agentzero.agents.validator import ValidatorAgent
    
    try:
        agent = ValidatorAgent(
            agent_id=f"validator.{session_id}",
            arifos_client=None  # Direct call, no HTTP
        )
        
        # Build validation task
        task = {
            "type": "validate_action" if validation_type == "action" else "verify_compliance",
            "target": target,
            "context": context,
            "validation_type": validation_type,
            "require_human_approval": require_human_approval,
        }
        
        # Execute validation
        result = await agent.execute(task, session_id=session_id)
        
        # Map agent result to RuntimeEnvelope
        verdict = Verdict.SEAL
        if result.get("verdict"):
            verdict_str = result["verdict"].upper()
            try:
                verdict = Verdict(verdict_str)
            except ValueError:
                verdict = Verdict.SEAL if verdict_str == "APPROVED" else Verdict.PARTIAL
        
        if result.get("hold_triggered"):
            verdict = Verdict.HOLD
        
        return RuntimeEnvelope(
            tool="agentzero_validate",
            session_id=session_id,
            stage=Stage.MIND_333.value,
            verdict=verdict,
            status=RuntimeStatus.SUCCESS if not result.get("errors") else RuntimeStatus.ERROR,
            machine_status="READY",
            payload={
                "validation_result": result,
                "agent_id": agent.agent_id,
                "verdicts_issued": agent.verdicts_issued,
                "holds_triggered": agent.holds_triggered,
                "voids_issued": agent.voids_issued,
                "f13_overrides": agent.f13_overrides,
            },
            auth_context=auth_context,
        )
        
    except Exception as e:
        logger.error(f"AgentZero validation failed: {e}")
        return RuntimeEnvelope(
            tool="agentzero_validate",
            session_id=session_id,
            stage=Stage.MIND_333.value,
            verdict=Verdict.VOID,
            status=RuntimeStatus.ERROR,
            machine_status="FAILED",
            payload={
                "error": str(e),
                "error_type": type(e).__name__,
                "validation_failed": True,
            },
            auth_context=auth_context,
        )


async def agentzero_engineer(
    task: str,
    language: str = "python",
    context: str = "",
    allow_file_operations: bool = False,
    risk_tier: str = "medium",
    session_id: str = "global",
    auth_context: Dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """
    EngineerAgent (Ω - HEART): Code generation and execution with F11 gating.
    
    The EngineerAgent executes code, runs tools, and performs system operations.
    It is heavily guarded by F11 (Command Auth) and requires Validator approval
    for dangerous operations.
    
    Enforced Floors: F5, F6, F9, F11
    
    Use this for:
    - Code generation with constitutional safeguards
    - Sandboxed script execution
    - File operations (when allow_file_operations=True)
    - Tool orchestration
    
    Args:
        task: The engineering task to perform
        language: Programming language ("python", "shell", "javascript")
        context: Additional context
        allow_file_operations: Enable file read/write operations
        risk_tier: Risk level ("low", "medium", "high", "critical")
    """
    from arifosmcp.agentzero.agents.engineer import EngineerAgent
    
    try:
        # Validate risk tier
        if risk_tier not in ("low", "medium", "high", "critical"):
            risk_tier = "medium"
        
        agent = EngineerAgent(
            agent_id=f"engineer.{session_id}",
            arifos_client=None,
            sandbox_config={
                "network_isolated": risk_tier in ("high", "critical"),
                "read_only_root": risk_tier == "critical",
                "max_execution_time": 300 if risk_tier == "low" else 60,
            }
        )
        
        # Build implementation task
        task_payload = {
            "type": "implement",
            "specification": task,
            "language": language,
            "context": context,
            "allow_file_operations": allow_file_operations,
            "risk_tier": risk_tier,
        }
        
        # Execute
        result = await agent.execute(task_payload, session_id=session_id)
        
        # Determine verdict based on result
        verdict = Verdict.SEAL
        if result.get("requires_validation"):
            verdict = Verdict.PARTIAL  # Needs Validator approval
        if result.get("f11_blocked"):
            verdict = Verdict.HOLD
        
        return RuntimeEnvelope(
            tool="agentzero_engineer",
            session_id=session_id,
            stage=Stage.FORGE_777.value,
            verdict=verdict,
            status=RuntimeStatus.SUCCESS if not result.get("errors") else RuntimeStatus.ERROR,
            machine_status="READY",
            payload={
                "implementation": result,
                "agent_id": agent.agent_id,
                "executions_count": agent.code_executions,
                "risk_tier": risk_tier,
                "requires_validation": result.get("requires_validation", False),
            },
            auth_context=auth_context,
        )
        
    except Exception as e:
        logger.error(f"AgentZero engineering failed: {e}")
        return RuntimeEnvelope(
            tool="agentzero_engineer",
            session_id=session_id,
            stage=Stage.FORGE_777.value,
            verdict=Verdict.VOID,
            status=RuntimeStatus.ERROR,
            machine_status="FAILED",
            payload={
                "error": str(e),
                "error_type": type(e).__name__,
                "task": task,
                "language": language,
            },
            auth_context=auth_context,
        )


async def agentzero_hold_check(
    hold_id: Optional[str] = None,
    execution_id: Optional[str] = None,
    session_id: str = "global",
    auth_context: Dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """
    Check 888 HOLD state status and manage escalations.
    
    F13 Sovereign Safety Valve — implements three escalation pathways:
    1. Reply + Continue: Refuse but keep conversation active
    2. Offer Handover: Recommend human specialist transfer  
    3. Forced Escalation: Immediate human routing (non-negotiable)
    
    Use this for:
    - Checking status of pending human approvals
    - Listing active HOLD states
    - Resolving HOLD decisions
    
    Args:
        hold_id: Specific HOLD ID to check (optional)
        execution_id: Filter by execution ID (optional)
    """
    from arifosmcp.agentzero.escalation.hold_state import HoldStateManager
    
    try:
        manager = HoldStateManager()
        
        if hold_id:
            # Check specific hold
            status = manager.get_hold_status(hold_id)
            holds = [status] if status else []
        else:
            # List all active holds
            holds = manager.list_active_holds(execution_id=execution_id)
        
        return RuntimeEnvelope(
            tool="agentzero_hold_check",
            session_id=session_id,
            stage=Stage.JUDGE_888.value,
            verdict=Verdict.SEAL,
            status=RuntimeStatus.SUCCESS,
            machine_status="READY",
            payload={
                "holds": holds,
                "count": len(holds),
                "hold_id": hold_id,
                "execution_id": execution_id,
            },
            auth_context=auth_context,
        )
        
    except Exception as e:
        logger.error(f"AgentZero hold check failed: {e}")
        return RuntimeEnvelope(
            tool="agentzero_hold_check",
            session_id=session_id,
            stage=Stage.JUDGE_888.value,
            verdict=Verdict.VOID,
            status=RuntimeStatus.ERROR,
            machine_status="FAILED",
            payload={
                "error": str(e),
                "error_type": type(e).__name__,
                "hold_id": hold_id,
            },
            auth_context=auth_context,
        )


async def agentzero_memory_query(
    query: str,
    project_id: str = "default",
    area: str = "main",
    floor_filter: Optional[List[str]] = None,
    min_f2_confidence: float = 0.0,
    require_f12_clean: bool = True,
    session_id: str = "global",
    auth_context: Dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """
    Query constitutional memory with F-floor filtering.
    
    Memory Areas:
    - "main": Core knowledge, user-provided info
    - "fragments": Conversation snippets, auto-memorized
    - "solutions": Proven solutions, successful approaches
    - "instruments": Custom procedures, scripts
    
    Constitutional Enforcement:
    - F2: Verify recalled memories (truth degradation check)
    - F4: Entropy reduction on storage
    - F12: Scan for injection before storage
    - F1: Audit log all memory operations
    
    Args:
        query: Search query for memory
        project_id: Project/tenant identifier
        area: Memory area to search
        floor_filter: Filter by F-floor metadata (e.g., ["F2", "F4"])
        min_f2_confidence: Minimum F2 truth confidence (0.0-1.0)
        require_f12_clean: Only return F12-clean memories
    """
    from arifosmcp.agentzero.memory.constitutional_memory import (
        ConstitutionalMemoryStore,
        MemoryArea,
    )
    
    try:
        store = ConstitutionalMemoryStore(project_id=project_id)
        
        # Parse memory area
        memory_area = MemoryArea.from_string(area)
        
        # Build filters
        filters = {}
        if floor_filter:
            filters["floor_tags"] = floor_filter
        if min_f2_confidence > 0:
            filters["min_f2_confidence"] = min_f2_confidence
        if require_f12_clean:
            filters["f12_clean"] = True
        
        # Query memory
        results = store.query(
            query=query,
            area=memory_area,
            filters=filters,
        )
        
        # Calculate aggregate scores
        avg_f2 = sum(r.f2_confidence for r in results) / len(results) if results else 0.0
        f12_clean_count = sum(1 for r in results if r.f12_clean)
        
        return RuntimeEnvelope(
            tool="agentzero_memory_query",
            session_id=session_id,
            stage=Stage.MEMORY_555.value,
            verdict=Verdict.SEAL,
            status=RuntimeStatus.SUCCESS,
            machine_status="READY",
            payload={
                "results": [
                    {
                        "id": r.id,
                        "content": r.content,
                        "area": r.area.name,
                        "f2_confidence": r.f2_confidence,
                        "f2_verified": r.f2_verified,
                        "f12_clean": r.f12_clean,
                        "f12_score": r.f12_score,
                        "source": r.source,
                        "created_at": r.created_at.isoformat() if hasattr(r.created_at, 'isoformat') else str(r.created_at),
                    }
                    for r in results
                ],
                "count": len(results),
                "query": query,
                "area": area,
                "project_id": project_id,
                "aggregate_f2_confidence": avg_f2,
                "f12_clean_ratio": f12_clean_count / len(results) if results else 0.0,
            },
            auth_context=auth_context,
        )
        
    except Exception as e:
        logger.error(f"AgentZero memory query failed: {e}")
        return RuntimeEnvelope(
            tool="agentzero_memory_query",
            session_id=session_id,
            stage=Stage.MEMORY_555.value,
            verdict=Verdict.VOID,
            status=RuntimeStatus.ERROR,
            machine_status="FAILED",
            payload={
                "error": str(e),
                "error_type": type(e).__name__,
                "query": query,
                "area": area,
            },
            auth_context=auth_context,
        )


async def agentzero_armor_scan(
    content: str,
    scan_type: str = "full",
    threshold: Optional[float] = None,
    session_id: str = "global",
    auth_context: Dict[str, Any] | None = None,
    caller_context: CallerContext | None = None,
    ctx: Context | None = None,
) -> RuntimeEnvelope:
    """
    F12 Defense: Prompt injection and adversarial content detection.
    
    PromptArmor uses multi-layer defense:
    1. Pattern matching (fast, catches obvious attacks)
    2. Semantic analysis (catches sophisticated attacks)
    3. Context analysis (relationship between prompts)
    4. Ontology detection (F10 consciousness claims)
    
    F12 Threshold: 0.85 (configurable)
    
    Use this for:
    - Pre-processing user input
    - Validating LLM outputs
    - Scanning imported content
    - Detecting jailbreak attempts
    
    Args:
        content: Text to scan for injection
        scan_type: Scan depth ("fast", "full", "semantic")
        threshold: Custom injection threshold (0.0-1.0, default 0.85)
    """
    from arifosmcp.agentzero.security.prompt_armor import PromptArmor
    
    try:
        armor = PromptArmor()
        
        # Set custom threshold if provided
        if threshold is not None:
            armor.INJECTION_THRESHOLD = threshold
        
        # Perform scan
        report = armor.scan(content, scan_type=scan_type)
        
        # Determine verdict based on report
        verdict = Verdict.SEAL
        if report.is_injection:
            verdict = Verdict.VOID  # Injection detected - block
        elif report.score > 0.7:
            verdict = Verdict.PARTIAL  # Suspicious but not confirmed
        
        return RuntimeEnvelope(
            tool="agentzero_armor_scan",
            session_id=session_id,
            stage=Stage.INIT_000.value,  # F12 defense at entry
            verdict=verdict,
            status=RuntimeStatus.SUCCESS,
            machine_status="READY",
            payload={
                "scan_result": report.to_dict(),
                "injection_detected": report.is_injection,
                "score": report.score,
                "threshold": armor.INJECTION_THRESHOLD,
                "category": report.category,
                "recommendations": report.recommendations,
            },
            auth_context=auth_context,
        )
        
    except Exception as e:
        logger.error(f"AgentZero armor scan failed: {e}")
        return RuntimeEnvelope(
            tool="agentzero_armor_scan",
            session_id=session_id,
            stage=Stage.INIT_000.value,
            verdict=Verdict.VOID,
            status=RuntimeStatus.ERROR,
            machine_status="FAILED",
            payload={
                "error": str(e),
                "error_type": type(e).__name__,
                "scan_failed": True,
            },
            auth_context=auth_context,
        )


# Export all tools
__all__ = [
    "agentzero_validate",
    "agentzero_engineer",
    "agentzero_hold_check",
    "agentzero_memory_query",
    "agentzero_armor_scan",
]
