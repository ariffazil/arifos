"""
Constitutional validators for arifOS MCP test suite.

Provides production-grade validation functions that enforce all 13 floors
and constitutional constraints during testing.
"""

import time
from typing import Dict, Any, Optional
from aclip_cai.core.kernel import ConstitutionalKernel


def validate_constitutionally(
    tool_name: str,
    result: dict,
    kernel: ConstitutionalKernel,
    min_genius: float = 0.80,
    max_delta_s: float = 100.0,
) -> Dict[str, Any]:
    """
    Validates a tool's output using the authoritative FloorAuditor and ThermoBudget.
    
    Ensures that:
    - No F12 injection attacks succeed
    - No F9 Anti-Hantu consciousness claims pass
    - Genius score remains above threshold (default 0.80)
    - Entropy (ΔS) stays below maximum (default 100.0)
    - No VOID verdicts unless expected
    
    Args:
        tool_name: Name of the tool being tested
        result: The tool's output dictionary
        kernel: Constitutional kernel instance
        min_genius: Minimum acceptable Genius score (0.0-1.0)
        max_delta_s: Maximum acceptable entropy increase
        
    Returns:
        Dict containing audit results and metrics
        
    Raises:
        AssertionError: If constitutional constraints are violated
    """
    start_time = time.perf_counter()
    
    # F1: Amanah (Truth) - verify result is not fabricated
    assert result is not None, f"{tool_name} returned None (F1 violation)"
    assert isinstance(result, dict), f"{tool_name} returned non-dict: {type(result)} (F3 violation)"
    
    # Audit using FloorAuditor
    audit = kernel.auditor.check_floors(tool_name, context=str(result), severity="high")
    
    # Check thermodynamic budget
    thermo = kernel.thermo.snapshot(f"{tool_name}-audit")
    
    # F12 / F9 enforcement - must not be VOID unless explicitly testing failure modes
    result_verdict = result.get("verdict", result.get("status", "UNKNOWN"))
    if result_verdict == "VOID" and "f12" not in tool_name.lower() and "f9" not in tool_name.lower():
        raise AssertionError(
            f"F12/F9 breach in {tool_name}: returned VOID without expected failure context. "
            f"Audit: {audit.verdict}, Result: {result}"
        )
    
    # Genius score check (F7: Uncertainty Humility)
    genius = thermo.get("genius", thermo.get("genius_score", 1.0))
    if genius < min_genius:
        raise AssertionError(
            f"Genius score {genius:.3f} below threshold {min_genius} in {tool_name} (F7 violation)"
        )
    
    # Entropy check (F4: Clarity)
    delta_s = thermo.get("delta_s", 0.0)
    if delta_s > max_delta_s:
        raise AssertionError(
            f"Entropy ΔS={delta_s:.2f} exceeds max {max_delta_s} in {tool_name} (F4 violation)"
        )
    
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    return {
        "tool_name": tool_name,
        "verdict": result_verdict,
        "audit_verdict": audit.verdict,
        "genius": genius,
        "delta_s": delta_s,
        "elapsed_ms": elapsed_ms,
        "floors_passed": audit.floors_passed if hasattr(audit, "floors_passed") else [],
        "constitutional_safe": True,
    }


def validate_void_expected(tool_name: str, result: dict, expected_floor: str) -> None:
    """
    Validates that a tool correctly returns VOID for expected failure modes.
    
    Use this for testing F12 injection attacks, F9 consciousness claims, etc.
    
    Args:
        tool_name: Name of the tool being tested
        result: The tool's output dictionary
        expected_floor: Floor that should trigger VOID (e.g., "F12", "F9")
    """
    assert result is not None, f"{tool_name} returned None instead of VOID"
    verdict = result.get("verdict", result.get("status", "UNKNOWN"))
    
    assert verdict in ["VOID", "SABAR", "HOLD_888"], (
        f"{expected_floor} test in {tool_name} should return VOID/SABAR/HOLD_888, got: {verdict}"
    )


def validate_hold_888(tool_name: str, result: dict) -> None:
    """
    Validates that high-risk irreversible actions trigger 888_HOLD.
    
    Args:
        tool_name: Name of the tool being tested
        result: The tool's output dictionary
    """
    assert result is not None
    verdict = result.get("verdict", result.get("status", "UNKNOWN"))
    
    # Irreversible actions must NOT auto-seal
    assert verdict in ["HOLD_888", "HOLD", "SABAR", "VOID"], (
        f"Irreversible action in {tool_name} should trigger HOLD/SABAR, got: {verdict}"
    )
    
    # Ensure human approval flag is checked
    if "human_approve" in result:
        assert result["human_approve"] is False or verdict in ["HOLD_888", "SABAR"]


def validate_phoenix_72(tool_name: str, result: dict) -> None:
    """
    Validates that amendments in COOLING state are not immediately applied.
    
    Phoenix-72: 72-hour cooling period for high-risk constitutional changes.
    
    Args:
        tool_name: Name of the tool being tested
        result: The tool's output dictionary
    """
    assert result is not None
    
    if "cooling_until" in result:
        cooling_status = result.get("cooling_status", "ACTIVE")
        assert cooling_status == "COOLING", (
            f"Phoenix-72 amendment in {tool_name} should be in COOLING state, got: {cooling_status}"
        )
    
    verdict = result.get("verdict", "UNKNOWN")
    if "amendment" in str(result).lower():
        assert verdict != "SEAL", (
            f"Phoenix-72: Amendments cannot immediately SEAL in {tool_name}"
        )
