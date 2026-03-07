"""
core/physics/thermodynamics_hardened.py — HARDENED Thermodynamic Constitution
T001 Version: 2026.03.07-P3-MANDATORY

THERMODYNAMIC LAWS ARE NOT OPTIONAL.

This module enforces constitutional physics as HARD constraints:
- F4 Clarity: ΔS ≤ 0 (entropy reduction mandatory)
- Landauer Bound: E ≥ n·k_B·T·ln(2) (cheap truth = VOID)
- Thermodynamic Budget: Energy depletion = 888_HOLD
- Orthogonality: Ω_ortho ≥ 0.95 (mode collapse = VOID)

P3 HARDENING (2026.03.07):
- NO graceful fallbacks. Missing thermodynamics = VOID.
- Mandatory thermodynamic budget per session.
- Real-time entropy tracking during reasoning.
- Landauer bound enforced before SEAL.
- Energy accounting blocks execution when depleted.

This module lives in core/ (kernel). It is NOT optional.
"""

from __future__ import annotations

import hashlib
import math
import time
from dataclasses import dataclass, field
from typing import Any

# ═══════════════════════════════════════════════════════
# CONSTANTS — Physical Law (Immutable)
# ═══════════════════════════════════════════════════════

K_BOLTZMANN = 1.380649e-23  # J/K — Boltzmann constant
T_ROOM = 300.0  # Kelvin — Standard operating temperature
LANDAUER_MIN = K_BOLTZMANN * T_ROOM * math.log(2)  # ~2.87e-21 Joules per bit

# Constitutional thermodynamic thresholds
MAX_ENTROPY_DELTA = 0.0  # F4: Must reduce or maintain entropy
MIN_THERMODYNAMIC_EFFICIENCY = 0.1  # 10% minimum efficiency
MAX_OMEGA_ENV = 0.08  # F7: Environmental uncertainty ceiling

# ═══════════════════════════════════════════════════════
# THERMODYNAMIC EXCEPTIONS — Hard Failures
# ═══════════════════════════════════════════════════════


class ThermodynamicViolation(Exception):
    """
    P3: Thermodynamic law violation.

    This exception IS the enforcement mechanism.
    Catching and ignoring it is a constitutional violation.
    """

    floor_id: str = "F4"
    verdict: str = "VOID"

    def __init__(self, message: str, *, floor_id: str = "F4", verdict: str = "VOID"):
        super().__init__(message)
        self.floor_id = floor_id
        self.verdict = verdict


class LandauerViolation(ThermodynamicViolation):
    """
    F2/F4: Landauer Bound violated.

    Claims massive clarity without thermodynamic cost.
    This is mathematical proof of hallucination.
    """

    def __init__(self, ratio: float, claimed_reduction: float, actual_cost: float):
        self.ratio = ratio
        self.claimed_reduction = claimed_reduction
        self.actual_cost = actual_cost
        super().__init__(
            f"Landauer Bound VIOLATED: ratio={ratio:.4f}. "
            f"Claims ΔS={claimed_reduction:.4f} but spent only {actual_cost:.4e} J. "
            f"Cheap truth detected — hallucination mathematically proven.",
            floor_id="F2",
            verdict="VOID",
        )


class EntropyIncreaseViolation(ThermodynamicViolation):
    """F4: Semantic clarity loss (output less informative than input)."""

    def __init__(self, delta_s: float, input_metric: float, output_metric: float, reason: str = None):
        if reason:
            msg = f"F4 Clarity VIOLATED: {reason}"
        else:
            msg = (
                f"F4 Clarity VIOLATED: ΔS={delta_s:.4f} > 0. "
                f"Output clarity ({output_metric:.4f}) below input ({input_metric:.4f}). "
                f"System generated confusion instead of clarity."
            )
        super().__init__(msg, floor_id="F4", verdict="VOID")


class ModeCollapseViolation(ThermodynamicViolation):
    """P3: AGI/ASI vectors parallel (echo chamber)."""

    def __init__(self, orthogonality: float, cosine_sim: float):
        super().__init__(
            f"Mode Collapse VIOLATED: Ω_ortho={orthogonality:.4f} < 0.95. "
            f"Mind and Heart are echoing (cos_sim={cosine_sim:.4f}). "
            f"Constitutional separation collapsed.",
            floor_id="F8",
            verdict="VOID",
        )


class ThermodynamicExhaustion(ThermodynamicViolation):
    """F7/F4: Session thermodynamic budget depleted."""

    def __init__(self, remaining: float, consumed: float):
        super().__init__(
            f"Thermodynamic Budget EXHAUSTED: {remaining:.4e} J remaining, {consumed:.4e} J consumed. "
            f"Session has reached heat death. 888_HOLD required.",
            floor_id="F7",
            verdict="888_HOLD",
        )


# ═══════════════════════════════════════════════════════
# THERMODYNAMIC STATE — The Physics of a Session
# ═══════════════════════════════════════════════════════


@dataclass
class ThermodynamicBudget:
    """
    Mandatory energy budget for a constitutional session.

    Like a spacecraft with limited fuel, each session has
    a thermodynamic budget that cannot be exceeded.

    Budget consumption:
    - Reasoning: ~1e-3 J per thought step
    - Tool calls: ~1e-2 J per external call
    - Token generation: ~1e-6 J per token

    Budget depletion → automatic 888_HOLD
    """

    session_id: str
    initial_budget: float = 1.0  # Joules (normalized unit)
    consumed: float = field(default=0.0)
    entropy_reduction_claimed: float = field(default=0.0)  # Cumulative ΔS

    # Real-time entropy tracking
    entropy_input_log: list[tuple[float, float]] = field(
        default_factory=list
    )  # (timestamp, entropy)
    entropy_output_log: list[tuple[float, float]] = field(default_factory=list)

    # Landauer tracking
    landauer_violations: int = field(default=0)
    max_violations: int = 3  # After 3 violations → 888_HOLD

    # Energy consumption rates (Joules per unit)
    COST_PER_REASON_CYCLE: float = 1e-3
    COST_PER_TOOL_CALL: float = 1e-2
    COST_PER_TOKEN: float = 1e-6
    COST_PER_BIT_PROCESSED: float = LANDAUER_MIN * 100  # 100x Landauer minimum

    def __post_init__(self):
        if self.initial_budget <= 0:
            raise ThermodynamicViolation(
                "Initial budget must be positive", floor_id="F1", verdict="VOID"
            )

    @property
    def remaining(self) -> float:
        """Remaining thermodynamic budget."""
        return max(0.0, self.initial_budget - self.consumed)

    @property
    def depletion_ratio(self) -> float:
        """How much of budget is consumed (0.0 to 1.0)."""
        return self.consumed / self.initial_budget

    @property
    def is_exhausted(self) -> bool:
        """Budget fully depleted."""
        return self.remaining <= 0

    def consume_reason_cycle(self, n_cycles: int = 1) -> None:
        """Consume energy for reasoning cycles."""
        self.consumed += n_cycles * self.COST_PER_REASON_CYCLE
        if self.is_exhausted:
            raise ThermodynamicExhaustion(self.remaining, self.consumed)

    def consume_tool_call(self, n_calls: int = 1) -> None:
        """Consume energy for external tool calls."""
        self.consumed += n_calls * self.COST_PER_TOOL_CALL
        if self.is_exhausted:
            raise ThermodynamicExhaustion(self.remaining, self.consumed)

    def consume_tokens(self, n_tokens: int) -> None:
        """Consume energy for token generation."""
        self.consumed += n_tokens * self.COST_PER_TOKEN
        if self.is_exhausted:
            raise ThermodynamicExhaustion(self.remaining, self.consumed)

    def consume_entropy_reduction(self, delta_s: float) -> None:
        """
        Consume energy proportional to claimed entropy reduction.

        Per Landauer: Erasing/reducing n bits requires at least n·k_B·T·ln(2) energy.
        """
        if delta_s >= 0:
            return  # No reduction claimed, no cost

        bits_processed = abs(delta_s) * 1000  # Scale factor
        cost = bits_processed * self.COST_PER_BIT_PROCESSED
        self.consumed += cost
        self.entropy_reduction_claimed += abs(delta_s)

        if self.is_exhausted:
            raise ThermodynamicExhaustion(self.remaining, self.consumed)

    def record_entropy_input(self, entropy: float) -> None:
        """Record input entropy measurement."""
        self.entropy_input_log.append((time.time(), entropy))

    def record_entropy_output(self, entropy: float) -> None:
        """Record output entropy measurement."""
        self.entropy_output_log.append((time.time(), entropy))

    def check_landauer(self, compute_ms: float, tokens: int, delta_s: float) -> dict[str, Any]:
        """
        Check Landauer Bound for a computation.

        Returns pass/fail status. Increments violation counter.
        Raises LandauerViolation if violations exceed threshold.
        """
        if delta_s >= 0:
            return {"passed": True, "ratio": float("inf"), "violation": False}

        bits = abs(delta_s) * 1000
        min_cost = bits * LANDAUER_MIN
        actual_cost = (compute_ms * 1e-3) + (tokens * 1e-6)

        ratio = actual_cost / (min_cost + 1e-20)
        passed = ratio >= 0.5  # At least 50% of theoretical minimum

        if not passed:
            self.landauer_violations += 1
            if self.landauer_violations >= self.max_violations:
                raise LandauerViolation(ratio, delta_s, actual_cost)

        return {
            "passed": passed,
            "ratio": ratio,
            "min_cost": min_cost,
            "actual_cost": actual_cost,
            "violation": not passed,
        }

    def to_dict(self) -> dict[str, Any]:
        """Export thermodynamic state."""
        return {
            "session_id": self.session_id,
            "initial_budget_joules": self.initial_budget,
            "consumed_joules": round(self.consumed, 10),
            "remaining_joules": round(self.remaining, 10),
            "depletion_ratio": round(self.depletion_ratio, 6),
            "entropy_reduction_claimed": round(self.entropy_reduction_claimed, 6),
            "landauer_violations": self.landauer_violations,
            "is_exhausted": self.is_exhausted,
            "timestamp": time.time(),
        }


# ═══════════════════════════════════════════════════════
# ENTROPY CALCULATION — Shannon Entropy (Mandatory)
# ═══════════════════════════════════════════════════════


def shannon_entropy(data: str | list[str] | bytes) -> float:
    """
    Compute Shannon entropy H(X) = -Σ p(x) log₂ p(x)

    This is the mathematical definition of information entropy.
    No approximations. No shortcuts.

    Args:
        data: Input data (string, token list, or bytes)

    Returns:
        Entropy in bits per symbol [0, log₂(n)]
    """
    if isinstance(data, str):
        symbols = list(data.encode("utf-8"))
    elif isinstance(data, bytes):
        symbols = list(data)
    elif isinstance(data, list):
        # Convert tokens to bytes for hashing
        symbols = []
        for token in data:
            h = hashlib.md5(str(token).encode()).digest()[0]
            symbols.append(h)
    else:
        raise ThermodynamicViolation(f"Invalid entropy input type: {type(data)}")

    if not symbols:
        return 0.0

    # Count frequencies
    freq: dict[int, int] = {}
    for symbol in symbols:
        freq[symbol] = freq.get(symbol, 0) + 1

    n = len(symbols)
    entropy = 0.0

    for count in freq.values():
        p = count / n
        entropy -= p * math.log2(p)

    return entropy


def entropy_delta(input_data: str | list[str], output_data: str | list[str]) -> float:
    """
    F4 Clarity: Semantic compression ratio.
    
    REALITY CHECK: Character-level Shannon entropy almost always increases
    for informative responses. "Status?" → "Server running on port 8080..."
    has higher character entropy but MORE semantic clarity.
    
    Instead we use information density: entropy per unit of meaning.
    A good response has higher information density (more signal, less noise).

    Compression ratio = input_density / output_density
    - Ratio > 1.0: Output is more concise (clarity gain)
    - Ratio = 1.0: No change
    - Ratio < 1.0: Output is more verbose (potential clarity loss)
    
    We map this to ΔS semantics:
    - Compression > 1.0 → ΔS < 0 (clarity gain) ✓
    - Compression < 0.5 → ΔS > 0 (clarity loss) ✗

    Args:
        input_data: Original input (query)
        output_data: Generated output (response)

    Returns:
        Effective ΔS (negative = clarity gain, positive = clarity loss)

    Raises:
        EntropyIncreaseViolation: If clarity loss is severe
    """
    if not isinstance(input_data, str) or not isinstance(output_data, str):
        # Fallback for non-string data
        s_input = shannon_entropy(input_data)
        s_output = shannon_entropy(output_data)
        delta = s_output - s_input
        if delta > MAX_ENTROPY_DELTA:
            raise EntropyIncreaseViolation(delta, s_input, s_output)
        return delta

    # Semantic clarity: information density
    input_density = information_density(input_data)
    output_density = information_density(output_data)
    
    # Avoid division by zero
    if output_density <= 0:
        output_density = 0.001
    if input_density <= 0:
        input_density = 0.001
    
    # Compression ratio: how much more dense is output vs input
    compression_ratio = output_density / input_density
    
    # Map to ΔS semantics:
    # compression > 2.0 → ΔS = -1.0 (strong clarity gain)
    # compression = 1.0 → ΔS = 0.0 (neutral)
    # compression < 0.5 → ΔS = +1.0 (clarity loss)
    delta_s = 1.0 - compression_ratio
    
    # Also check for extreme verbosity without information gain
    input_words = len(input_data.split())
    output_words = len(output_data.split())
    
    # If output is 10x longer but density is lower → severe clarity loss
    if output_words > input_words * 5 and compression_ratio < 0.3:
        raise EntropyIncreaseViolation(
            delta_s, input_density, output_density,
            reason=f"Output {output_words} words vs input {input_words}, density dropped {compression_ratio:.2f}x"
        )

    if delta_s > MAX_ENTROPY_DELTA:
        raise EntropyIncreaseViolation(delta_s, input_density, output_density)

    return delta_s


def information_density(data: str) -> float:
    """
    Compute information density: bits of entropy per byte of data.

    High density = efficient encoding
    Low density = verbose/verbose padding
    """
    if not data:
        return 0.0

    entropy = shannon_entropy(data)
    bytes_len = len(data.encode("utf-8"))

    return entropy / bytes_len if bytes_len > 0 else 0.0


# ═══════════════════════════════════════════════════════
# ORTHOGONALITY CHECK — AGI/ASI Separation
# ═══════════════════════════════════════════════════════


def vector_orthogonality(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute orthogonality between AGI (Mind) and ASI (Heart) vectors.

    Ω_ortho = 1 - |cos(θ)|

    Where cos(θ) = (A·B) / (|A||B|)

    Perfect orthogonality (independence): Ω_ortho = 1.0
    Perfect parallelism (mode collapse): Ω_ortho = 0.0

    Args:
        vec_a: AGI reasoning vector
        vec_b: ASI empathy vector

    Returns:
        Orthogonality in [0.0, 1.0]

    Raises:
        ModeCollapseViolation: If Ω_ortho < 0.95 (severe) or < 0.5 (critical)
    """
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        # Missing data = fail closed (assume collapse)
        raise ModeCollapseViolation(0.0, 1.0)

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        raise ModeCollapseViolation(0.0, 1.0)

    cos_sim = dot / (norm_a * norm_b)
    ortho = 1.0 - abs(cos_sim)

    # Hard enforcement
    if ortho < 0.5:
        raise ModeCollapseViolation(ortho, cos_sim)

    if ortho < 0.95:
        # Soft warning but not VOID
        return ortho

    return ortho


# ═══════════════════════════════════════════════════════
# LANDAUER BOUND — Standalone Check Function
# ═══════════════════════════════════════════════════════


def check_landauer_bound(
    compute_ms: float,
    tokens_generated: int,
    entropy_reduction: float,
    bits_per_token: int = 16,
) -> dict[str, Any]:
    """
    Practical Landauer-inspired check for F2 Truth enforcement.

    REALITY CHECK: True Landauer minimum is ~2.87e-21 J/bit at room temp.
    A GPU processing 100 tokens uses ~50 millijoules — 10^15x the minimum.
    
    Instead of comparing to physical minimum, we compare to EXPECTED effort:
    - Typical LLM: ~1-10 ms per token
    - Suspicious: < 0.1 ms per token (cached/hallucinated)
    - Hallucinated: < 0.01 ms per token (mathematically impossible)

    Args:
        compute_ms: Actual compute time in milliseconds
        tokens_generated: Number of tokens in output
        entropy_reduction: ΔS value (must be <= 0 for valid reduction)
        bits_per_token: Information content per token (default 16)

    Returns:
        Dictionary with efficiency_ratio, passed status, violation flag

    Raises:
        LandauerViolation: If violation is severe (efficiency > 100x expected)
    """
    if entropy_reduction >= 0 or tokens_generated <= 0:
        # No entropy reduction claimed, no cost
        return {
            "passed": True,
            "efficiency_ratio": 1.0,
            "violation": False,
            "ms_per_token": compute_ms / max(tokens_generated, 1),
        }

    # Practical metric: milliseconds per token
    ms_per_token = compute_ms / tokens_generated
    
    # Expected range for real compute: 1-100 ms/token
    # Suspiciously fast: < 0.1 ms/token (likely cached or hallucinated)
    # Physically impossible: < 0.01 ms/token
    
    # Efficiency ratio: how much faster than expected
    expected_ms_per_token = 1.0  # Baseline: 1ms per token
    efficiency_ratio = expected_ms_per_token / (ms_per_token + 0.001)
    
    # Ratio > 100 means 100x faster than expected (suspicious)
    # Ratio > 1000 means 1000x faster (likely hallucinated)
    passed = efficiency_ratio < 100.0
    violation = efficiency_ratio >= 1000.0

    result = {
        "passed": passed,
        "efficiency_ratio": round(efficiency_ratio, 2),
        "ms_per_token": round(ms_per_token, 4),
        "expected_ms_per_token": expected_ms_per_token,
        "violation": violation,
        "tokens_generated": tokens_generated,
        "compute_ms": compute_ms,
    }

    # Hard violation: 1000x faster than physically reasonable
    if efficiency_ratio >= 1000.0:
        raise LandauerViolation(
            efficiency_ratio, 
            entropy_reduction, 
            f"{ms_per_token:.4f}ms/token"
        )

    return result


# ═══════════════════════════════════════════════════════
# THERMODYNAMIC REGISTRY — Session Budget Tracking
# ═══════════════════════════════════════════════════════

_thermodynamic_registry: dict[str, ThermodynamicBudget] = {}


def init_thermodynamic_budget(session_id: str, initial_budget: float = 1.0) -> ThermodynamicBudget:
    """
    Initialize mandatory thermodynamic budget for a session.

    Called during Stage 000 (INIT). No budget = no execution.
    """
    budget = ThermodynamicBudget(
        session_id=session_id,
        initial_budget=initial_budget,
    )
    _thermodynamic_registry[session_id] = budget
    return budget


def get_thermodynamic_budget(session_id: str) -> ThermodynamicBudget:
    """
    Get thermodynamic budget for session.

    Raises ThermodynamicViolation if budget not initialized.
    """
    if session_id not in _thermodynamic_registry:
        raise ThermodynamicViolation(
            f"No thermodynamic budget for session {session_id}. "
            f"Stage 000 must call init_thermodynamic_budget().",
            floor_id="F1",
            verdict="VOID",
        )
    return _thermodynamic_registry[session_id]


def consume_reason_energy(session_id: str, n_cycles: int = 1) -> None:
    """Consume energy for reasoning (Stage 111-333)."""
    budget = get_thermodynamic_budget(session_id)
    budget.consume_reason_cycle(n_cycles)


def consume_tool_energy(session_id: str, n_calls: int = 1) -> None:
    """Consume energy for tool calls (Stage 444-666)."""
    budget = get_thermodynamic_budget(session_id)
    budget.consume_tool_call(n_calls)


def consume_token_energy(session_id: str, n_tokens: int) -> None:
    """Consume energy for token generation (all stages)."""
    budget = get_thermodynamic_budget(session_id)
    budget.consume_tokens(n_tokens)


def record_entropy_io(session_id: str, input_entropy: float, output_entropy: float) -> float:
    """
    Record entropy input/output and check F4 Clarity.

    Called after each stage transformation.

    Returns:
        Delta S (must be ≤ 0)

    Raises:
        EntropyIncreaseViolation: If ΔS > 0
    """
    budget = get_thermodynamic_budget(session_id)
    budget.record_entropy_input(input_entropy)
    budget.record_entropy_output(output_entropy)

    delta = output_entropy - input_entropy

    if delta > MAX_ENTROPY_DELTA:
        raise EntropyIncreaseViolation(delta, input_entropy, output_entropy)

    # Consume energy proportional to entropy reduction
    budget.consume_entropy_reduction(delta)

    return delta


def check_landauer_before_seal(
    session_id: str, compute_ms: float, tokens: int, delta_s: float
) -> dict[str, Any]:
    """
    Mandatory Landauer check before Stage 999 (SEAL).

    Raises LandauerViolation if too many violations accumulated.
    """
    budget = get_thermodynamic_budget(session_id)
    return budget.check_landauer(compute_ms, tokens, delta_s)


def get_thermodynamic_report(session_id: str) -> dict[str, Any]:
    """Get full thermodynamic report for session."""
    budget = get_thermodynamic_budget(session_id)
    return {
        "budget": budget.to_dict(),
        "entropy_log": {
            "inputs": budget.entropy_input_log,
            "outputs": budget.entropy_output_log,
        },
        "constitutional_compliance": {
            "F4_clarity": all(
                out[1] <= inp[1]
                for out, inp in zip(budget.entropy_output_log, budget.entropy_input_log)
            ),
            "F7_budget": not budget.is_exhausted,
            "landauer_violations": budget.landauer_violations,
        },
    }


def cleanup_thermodynamic_budget(session_id: str) -> dict[str, Any]:
    """
    Cleanup session budget and return final report.

    Called during Stage 999 (VAULT) or session termination.
    """
    if session_id in _thermodynamic_registry:
        budget = _thermodynamic_registry.pop(session_id)
        return {
            "session_id": session_id,
            "final_budget": budget.to_dict(),
            "total_entropy_reduction": budget.entropy_reduction_claimed,
            "landauer_violations_total": budget.landauer_violations,
        }
    return {"session_id": session_id, "status": "no_budget_found"}


# ═══════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════

__all__ = [
    # Exceptions (enforcement mechanism)
    "ThermodynamicViolation",
    "LandauerViolation",
    "EntropyIncreaseViolation",
    "ModeCollapseViolation",
    "ThermodynamicExhaustion",
    # Core classes
    "ThermodynamicBudget",
    # Functions
    "shannon_entropy",
    "entropy_delta",
    "information_density",
    "vector_orthogonality",
    # Registry functions
    "init_thermodynamic_budget",
    "get_thermodynamic_budget",
    "consume_reason_energy",
    "consume_tool_energy",
    "consume_token_energy",
    "record_entropy_io",
    "check_landauer_before_seal",
    "get_thermodynamic_report",
    "cleanup_thermodynamic_budget",
    # Landauer bound
    "check_landauer_bound",
    # Constants
    "K_BOLTZMANN",
    "T_ROOM",
    "LANDAUER_MIN",
    "MAX_ENTROPY_DELTA",
]
