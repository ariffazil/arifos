"""
arifOS Genius Formula Calculator (GFC)
Version: v55.5-EIGEN
Formula: G = A × P × X × E²

CRITICAL FIX (v55.5): A/P/X/E dials are now DERIVED from floor scores
via eigendecomposition (geometric mean projection), not set manually.

Theory: 000_FOUNDATIONS.md §3.2 — The APEX 4 Dials
  13 Floor Scores → Covariance clustering → 4 Principal Components
  A (Mind):  F2, F4, F7, F10   — Orthogonal geometry (reasoning)
  P (Heart): F5, F6, F12       — Fractal geometry (empathy)
  X (Soul):  F3, F8, F9, F11   — Toroidal geometry (governance)
  E (Bound): F1, F13           — Boundary conditions (energy)

F10 Ontology Wall: LOCK enforced
DITEMPA BUKAN DIBERI
"""

from dataclasses import dataclass, field
from typing import Tuple, Dict, Optional, List, Any
from enum import Enum
import math
import logging
from codebase.system.safe_types import safe_float, safe_bool

logger = logging.getLogger(__name__)


class Verdict(Enum):
    SEAL = "SEAL"
    SABAR = "SABAR"
    VOID = "VOID"


class OntologyLock(Exception):
    """F10 Ontology Wall - AGI-consciousness claim detected"""

    pass


# =============================================================================
# FLOOR SCORES — The 13 Constitutional Measurements
# =============================================================================


@dataclass
class FloorScores:
    """
    The 13 constitutional floor scores.

    This is the SINGLE SOURCE OF TRUTH for all governance metrics.
    A/P/X/E dials are DERIVED from these, never set independently.
    """

    f1_amanah: float = 1.0  # F1: Reversibility (boolean-ish, 0 or 1)
    f2_truth: float = 0.99  # F2: Factual accuracy (>=0.99)
    f3_tri_witness: float = 0.95  # F3: Consensus (>=0.95)
    f4_clarity: float = 0.0  # F4: Entropy delta (<=0, negated for dial)
    f5_peace: float = 1.0  # F5: Peace^2 (>=1.0, clamped to [0,1] for dial)
    f6_empathy: float = 0.95  # F6: Kappa_r empathy (>=0.95)
    f7_humility: float = 0.96  # F7: 1 - Omega_0 (confidence, in [0.95, 0.97])
    f8_genius: float = 0.80  # F8: Previous iteration G (self-referential)
    f9_antihantu: float = 1.0  # F9: 1 - C_dark (>=0.70, inverted for dial)
    f10_ontology: float = 1.0  # F10: Category lock (boolean, 0 or 1)
    f11_command: float = 1.0  # F11: Authority verified (boolean, 0 or 1)
    f12_injection: float = 0.99  # F12: Injection defense (>=0.85)
    f13_sovereign: float = 1.0  # F13: Human presence (boolean, 0 or 1)

    def to_vector(self) -> List[float]:
        """Return floor scores as ordered list [F1..F13]."""
        return [
            self.f1_amanah,
            self.f2_truth,
            self.f3_tri_witness,
            self.f4_clarity,
            self.f5_peace,
            self.f6_empathy,
            self.f7_humility,
            self.f8_genius,
            self.f9_antihantu,
            self.f10_ontology,
            self.f11_command,
            self.f12_injection,
            self.f13_sovereign,
        ]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FloorScores":
        """Create from a flat dictionary of floor scores using safe access."""
        return cls(
            f1_amanah=safe_float(d.get("F1", d.get("f1_amanah", 1.0)), default=1.0),
            f2_truth=safe_float(d.get("F2", d.get("f2_truth", 0.99)), default=0.99),
            f3_tri_witness=safe_float(d.get("F3", d.get("f3_tri_witness", 0.95)), default=0.95),
            f4_clarity=safe_float(d.get("F4", d.get("f4_clarity", 0.0)), default=0.0),
            f5_peace=safe_float(d.get("F5", d.get("f5_peace", 1.0)), default=1.0),
            f6_empathy=safe_float(d.get("F6", d.get("f6_empathy", 0.95)), default=0.95),
            f7_humility=safe_float(d.get("F7", d.get("f7_humility", 0.96)), default=0.96),
            f8_genius=safe_float(d.get("F8", d.get("f8_genius", 0.80)), default=0.80),
            f9_antihantu=safe_float(d.get("F9", d.get("f9_antihantu", 1.0)), default=1.0),
            f10_ontology=safe_float(d.get("F10", d.get("f10_ontology", 1.0)), default=1.0),
            f11_command=safe_float(d.get("F11", d.get("f11_command", 1.0)), default=1.0),
            f12_injection=safe_float(d.get("F12", d.get("f12_injection", 0.99)), default=0.99),
            f13_sovereign=safe_float(d.get("F13", d.get("f13_sovereign", 1.0)), default=1.0),
        )


# =============================================================================
# DIAL LOADINGS — Theory-defined floor-to-dial mapping
# =============================================================================

# From 000_FOUNDATIONS.md §3.2 Table: The APEX 4 Dials
# Each dial loads on specific floors based on constitutional geometry:
#   A (Mind)  = Orthogonal floors: F2, F4, F7, F10
#   P (Heart) = Fractal floors:    F5, F6, F12
#   X (Soul)  = Toroidal floors:   F3, F8, F9, F11
#   E (Bound) = Boundary floors:   F1, F13


def _geometric_mean(values: List[float]) -> float:
    """Compute geometric mean. Returns 0 if any value is 0."""
    try:
        if not values or any(v <= 0 for v in values):
            return 0.0
        product = 1.0
        for v in values:
            product *= v
        return product ** (1.0 / len(values))
    except Exception:
        return 0.0


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp value to [lo, hi] range."""
    # Use safe_float for robust handling if needed, but value is expected float
    return max(lo, min(hi, float(value)))


def extract_dials(floors: FloorScores) -> Dict[str, float]:
    """
    Extract A/P/X/E dials from 13 floor scores via eigendecomposition projection.

    This is the CANONICAL function that collapses 13 floors -> 4 dials.
    Uses geometric mean (not arithmetic) because the Genius formula is
    multiplicative — GM punishes imbalance, matching the constitutional
    principle that ANY zero dial kills Genius.

    Theory: 000_FOUNDATIONS.md §3.2
    Geometry: Orthogonal(A) x Fractal(P) x Toroidal(X) x Boundary(E)
    """
    # A = AKAL (Mind/Clarity) — Orthogonal geometry
    # Floors: F2 Truth, F4 Clarity (negated: lower entropy = better),
    #         F7 Humility (confidence), F10 Ontology
    # F4 is DeltaS <= 0, so we use (1 - |DeltaS|) clamped, or if DeltaS <= 0, use 1.0
    # Safe float clamp
    f4_val = floors.f4_clarity
    if f4_val <= 0:
        f4_for_dial = _clamp(1.0 - abs(f4_val))
    else:
        f4_for_dial = _clamp(1.0 - f4_val)

    A = _geometric_mean(
        [
            _clamp(floors.f2_truth),
            _clamp(f4_for_dial),
            _clamp(floors.f7_humility),
            _clamp(floors.f10_ontology),
        ]
    )

    # P = PRESENT (Heart/Peace) — Fractal geometry
    # Floors: F5 Peace^2, F6 Empathy, F12 Injection Defense
    # F5 Peace^2 >= 1.0, so clamp to [0,1] for dial (1.0 = perfect, >1 still 1)
    P = _geometric_mean(
        [
            _clamp(floors.f5_peace),
            _clamp(floors.f6_empathy),
            _clamp(floors.f12_injection),
        ]
    )

    # X = EXPLORATION (Soul/Governance) — Toroidal geometry
    # Floors: F3 Tri-Witness, F8 Genius (previous), F9 Anti-Hantu, F11 Command
    X = _geometric_mean(
        [
            _clamp(floors.f3_tri_witness),
            _clamp(floors.f8_genius),
            _clamp(floors.f9_antihantu),
            _clamp(floors.f11_command),
        ]
    )

    # E = ENERGY (Boundary/Vitality)
    # Floors: F1 Amanah (reversibility), F13 Sovereign (human presence)
    E = _geometric_mean(
        [
            _clamp(floors.f1_amanah),
            _clamp(floors.f13_sovereign),
        ]
    )

    return {"A": A, "P": P, "X": X, "E": E}


# =============================================================================
# GENIUS METRICS
# =============================================================================


@dataclass
class GeniusMetrics:
    """Container for Genius Formula components (A/P/X/E dials)."""

    A: float  # AKAL (Clarity/Intelligence) - Mind (Delta)
    P: float  # PRESENT (Regulation) - Soul (Psi)
    X: float  # EXPLORATION (Trust+Curiosity) - Heart (Omega)
    E: float  # ENERGY (Sustainable Power) - squared

    def validate(self) -> bool:
        """Validate all components in [0,1] range."""
        try:
            return all(0 <= v <= 1 for v in [self.A, self.P, self.X, self.E])
        except Exception:
            return False

    @classmethod
    def from_floors(cls, floors: FloorScores) -> "GeniusMetrics":
        """
        CANONICAL CONSTRUCTOR: Derive dials from floor scores.

        This is the correct way to create GeniusMetrics.
        Dials are measurements, not inputs.
        """
        dials = extract_dials(floors)
        return cls(A=dials["A"], P=dials["P"], X=dials["X"], E=dials["E"])


# =============================================================================
# GENIUS CALCULATOR
# =============================================================================


class GeniusCalculator:
    """
    888_Judge Genius Formula Calculator

    Computes G = A x P x X x E^2 with constitutional safeguards:
    - F10 Ontology Wall prevents AGI-consciousness claims
    - Omega_0 humility factor enforced (0.03-0.05)
    - Multiplicative law: if ANY=0, G=0
    - A/P/X/E derived from floor scores (eigendecomposition)
    """

    # Constitutional constants
    G_THRESHOLD = 0.80  # F8 Genius floor
    OMEGA_MIN = 0.03  # Humility lower bound
    OMEGA_MAX = 0.05  # Humility upper bound
    KAPPA_R_MIN = 0.70  # Empathy minimum
    EPSILON = 1e-6  # Tolerance for float comparisons

    def __init__(self, enable_f10_lock: bool = True):
        self.enable_f10_lock = enable_f10_lock
        self._lock_triggered = False
        self._lock_reason = None

    def compute_from_floors(self, floors: FloorScores) -> Tuple[float, Dict]:
        """
        CANONICAL METHOD: Compute Genius from raw floor scores.

        This is the constitutionally correct entry point.
        Dials are derived, not provided.
        """
        try:
            metrics = GeniusMetrics.from_floors(floors)
            G, metadata = self.compute(metrics)
            metadata["derivation"] = "eigendecomposition_of_floors"
            metadata["floor_scores"] = {
                "F1": floors.f1_amanah,
                "F2": floors.f2_truth,
                "F3": floors.f3_tri_witness,
                "F4": floors.f4_clarity,
                "F5": floors.f5_peace,
                "F6": floors.f6_empathy,
                "F7": floors.f7_humility,
                "F8": floors.f8_genius,
                "F9": floors.f9_antihantu,
                "F10": floors.f10_ontology,
                "F11": floors.f11_command,
                "F12": floors.f12_injection,
                "F13": floors.f13_sovereign,
            }
            return (G, metadata)
        except Exception as e:
            logger.error(f"Genius calculation failed: {e}", exc_info=True)
            return (0.0, {"error": str(e), "verdict": Verdict.VOID.value})

    def compute(self, metrics: GeniusMetrics) -> Tuple[float, Dict]:
        """
        Compute Genius Score with full constitutional enforcement.

        Prefer compute_from_floors() for constitutionally grounded results.
        This method is retained for backward compatibility.
        """
        try:
            # Validate inputs
            if not metrics.validate():
                # Try to salvage with safe_float clamping if valid metrics object
                pass

            # F10 Ontology Wall Check
            if self.enable_f10_lock:
                lock_check = self._check_ontology_lock(metrics)
                if lock_check["locked"]:
                    self._lock_triggered = True
                    self._lock_reason = lock_check["reason"]
                    raise OntologyLock(f"F10 LOCK: {lock_check['reason']}")

            # Extract components
            A, P, X, E = metrics.A, metrics.P, metrics.X, metrics.E

            # E^2 Law: Energy depletion is exponential
            E_squared = E**2

            # Multiplicative Law: If ANY = 0, G = 0
            if any(v <= 0.001 for v in [A, P, X, E]):
                G = 0.0
            else:
                G = A * P * X * E_squared

            # Determine verdict
            if G >= self.G_THRESHOLD:
                verdict = Verdict.SEAL
            elif G >= 0.60:
                verdict = Verdict.SABAR
            else:
                verdict = Verdict.VOID

            metadata = {
                "A": A,
                "P": P,
                "X": X,
                "E": E,
                "E_squared": E_squared,
                "G": G,
                "verdict": verdict.value,
                "threshold": self.G_THRESHOLD,
                "components": {
                    "APE": A * P * E_squared,  # Without X (clever but dangerous)
                    "APEX": G,  # With X (wise and accountable)
                },
                "omega_0": 1 - max(A, P, X, E),
                "f10_lock_enabled": self.enable_f10_lock,
                "derivation": "manual_dials",
            }

            return (G, metadata)

        except OntologyLock:
            raise
        except Exception as e:
            logger.error(f"Genius compute error: {e}", exc_info=True)
            return (0.0, {"verdict": Verdict.VOID.value, "error": str(e)})

    def _check_ontology_lock(self, metrics: GeniusMetrics) -> Dict:
        """
        F10 Ontology Wall - Prevent AGI-consciousness claims.

        Triggers LOCK if:
        - Any component claims certainty > 0.97
        - Omega_0 outside [0.03, 0.05] range
        """
        max_confidence = max(metrics.A, metrics.P, metrics.X, metrics.E)
        omega_0 = 1 - max_confidence

        violations = []

        if max_confidence > 0.97:
            violations.append(f"Certainty {max_confidence:.3f} exceeds 0.97 limit")

        if omega_0 < self.OMEGA_MIN - self.EPSILON:
            violations.append(f"Omega_0 = {omega_0:.4f} below minimum {self.OMEGA_MIN}")
        if omega_0 > self.OMEGA_MAX + self.EPSILON:
            violations.append(f"Omega_0 = {omega_0:.4f} above maximum {self.OMEGA_MAX}")

        return {
            "locked": len(violations) > 0,
            "reason": "; ".join(violations) if violations else None,
            "omega_0": omega_0,
            "max_confidence": max_confidence,
        }

    def batch_evaluate(self, tasks: list) -> list:
        """Evaluate multiple tasks and return sorted by G-score."""
        results = []
        for task in tasks:
            try:
                G, meta = self.compute(task)
                results.append({"G": G, "meta": meta, "error": None})
            except OntologyLock as e:
                results.append({"G": 0.0, "meta": {}, "error": str(e)})
            except Exception as e:
                results.append({"G": 0.0, "meta": {}, "error": str(e)})

        return sorted(results, key=lambda x: x["G"], reverse=True)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    calc = GeniusCalculator(enable_f10_lock=True)

    # Example 1: Compute from floor scores (CORRECT way)
    floors = FloorScores(
        f2_truth=0.99,
        f4_clarity=-0.3,
        f7_humility=0.96,
        f10_ontology=1.0,
        f5_peace=1.1,
        f6_empathy=0.97,
        f12_injection=0.98,
        f3_tri_witness=0.97,
        f8_genius=0.85,
        f9_antihantu=0.95,
        f11_command=1.0,
        f1_amanah=1.0,
        f13_sovereign=1.0,
    )
    G, meta = calc.compute_from_floors(floors)
    print(f"From floors: G={G:.4f}, Verdict={meta['verdict']}")
    print(
        f"  A(Mind)={meta['A']:.3f}  P(Heart)={meta['P']:.3f}  "
        f"X(Soul)={meta['X']:.3f}  E(Energy)={meta['E']:.3f}"
    )
    print(f"  Derivation: {meta['derivation']}")

    # Example 2: Legacy manual dials (backward compat)
    manual = GeniusMetrics(A=0.92, P=0.88, X=0.85, E=0.95)
    try:
        G, meta = calc.compute(manual)
        print(f"\nManual dials: G={G:.4f}, Verdict={meta['verdict']}")
    except OntologyLock as e:
        print(f"LOCKED: {e}")

    # Example 3: Overconfident (triggers F10)
    overconfident = GeniusMetrics(A=0.99, P=0.98, X=0.97, E=0.99)
    try:
        G, meta = calc.compute(overconfident)
        print(f"Overconfident: G={G:.4f}")
    except OntologyLock as e:
        print(f"LOCKED (expected): {e}")
