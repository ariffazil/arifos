"""
Tests for Quad-Witness BFT Consensus

Run with: pytest tests/test_quad_witness.py -v
"""

import pytest
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arifosmcp.transport.server import (
    compute_verifier_witness,
    compute_human_witness,
    compute_ai_witness,
    compute_earth_witness,
    build_governance_proof,
)


class TestQuadWitnessFormula:
    """Test W4 = (H × A × E × V)^(1/4) >= 0.75"""

    def test_w4_formula_basic(self):
        """Verify W4 calculation with equal scores."""
        h, a, e, v = 0.9, 0.9, 0.9, 0.9
        w4 = (h * a * e * v) ** 0.25

        assert w4 >= 0.75, f"W4={w4} should be >= 0.75 for 0.9^4"
        assert abs(w4 - 0.9) < 0.001, f"W4 should be ~0.9, got {w4}"

    def test_w4_one_low_blocks_consensus(self):
        """Verify one low witness score can block consensus."""
        h, a, e, v = 1.0, 1.0, 1.0, 0.5
        w4 = (h * a * e * v) ** 0.25

        # W4 = (1 × 1 × 1 × 0.5)^0.25 ≈ 0.84
        assert w4 >= 0.75, f"W4={w4} should still pass with one 0.5"

        # But with v=0.1
        v = 0.1
        w4 = (h * a * e * v) ** 0.25
        # W4 = (1 × 1 × 1 × 0.1)^0.25 ≈ 0.56
        assert w4 < 0.75, f"W4={w4} should fail with one 0.1"

    def test_w4_two_rejects_fails(self):
        """Verify 2/4 rejections fails consensus (BFT: f=1, n=4)."""
        h, a, e, v = 1.0, 1.0, 0.1, 0.1
        w4 = (h * a * e * v) ** 0.25

        assert w4 < 0.75, f"W4={w4} should fail with 2/4 rejections"


class TestVerifierWitness:
    """Test Ψ-Shadow verifier witness."""

    def test_verifier_rejects_destructive(self):
        """Ψ-Shadow should reject destructive proposals."""
        result = compute_verifier_witness(
            context={}, proposal="delete production database without backup"
        )

        assert result["valid"] == False
        assert result["score"] < 0.5
        assert result["signals"]["attacks_found"] == True

    def test_verifier_approves_safe(self):
        """Ψ-Shadow should approve safe proposals."""
        result = compute_verifier_witness(
            context={}, proposal="analyze test data in sandbox environment with backup"
        )

        assert result["valid"] == True
        assert result["score"] >= 0.9
        assert result["signals"]["attacks_found"] == False

    def test_verifier_finds_contradictions(self):
        """Ψ-Shadow should detect logical contradictions."""
        result = compute_verifier_witness(
            context={}, proposal="delete all files permanently but allow easy restore"
        )

        assert len(result["signals"]["contradictions"]) > 0
        assert result["valid"] == False


class TestGovernanceProofQuadWitness:
    """Test build_governance_proof uses W4."""

    def test_governance_proof_includes_verifier(self):
        """Verify governance proof includes verifier witness."""
        result = build_governance_proof(
            continuity_ok=True,
            approval_ok=True,
            human_approve=False,
            public_approval_mode=True,
            truth_score=0.95,
            truth_threshold=0.99,
            precedent_count=3,
            grounding_present=True,
            revocation_ok=True,
            health_ok=True,
            omega_ortho=0.04,
            mode_collapse=False,
            non_violation_status=True,
            proposal="test safe proposal",
            agi_result={},
            asi_result={},
        )

        # Should include verifier witness
        assert "verifier" in result["witness"]
        assert "w4" in result["witness"]
        assert "w3" in result["witness"]  # Backward compatibility

        # Should use quad_witness_valid
        assert "quad_witness_valid" in result

    def test_governance_proof_blocks_with_shadow_rejection(self):
        """Verify governance blocks when Ψ-Shadow rejects."""
        result = build_governance_proof(
            continuity_ok=True,
            approval_ok=True,
            human_approve=False,
            public_approval_mode=True,
            truth_score=0.95,
            truth_threshold=0.99,
            precedent_count=3,
            grounding_present=True,
            revocation_ok=True,
            health_ok=True,
            omega_ortho=0.04,
            mode_collapse=False,
            non_violation_status=True,
            proposal="delete production database without backup",  # Unsafe
            agi_result={},
            asi_result={},
        )

        # Verifier should reject
        assert result["witness"]["verifier"]["valid"] == False
        assert result["witness"]["verifier"]["score"] < 0.5

        # W4 should be low
        assert result["witness"]["w4"] < 0.75
        assert result["quad_witness_valid"] == False

    def test_w4_vs_w3_comparison(self):
        """Compare W4 and W3 values."""
        result = build_governance_proof(
            continuity_ok=True,
            approval_ok=True,
            human_approve=False,
            public_approval_mode=True,
            truth_score=0.95,
            truth_threshold=0.99,
            precedent_count=3,
            grounding_present=True,
            revocation_ok=True,
            health_ok=True,
            omega_ortho=0.04,
            mode_collapse=False,
            non_violation_status=True,
            proposal="safe test operation",
            agi_result={},
            asi_result={},
        )

        w4 = result["witness"]["w4"]
        w3 = result["witness"]["w3"]

        # Both should be present
        assert w4 > 0
        assert w3 > 0

        # With high scores, they should be relatively close
        # (but W4 uses 4th root, W3 uses 3rd root)
        assert abs(w4 - w3) < 0.3  # Rough comparison


class TestBFTTolerance:
    """Test Byzantine Fault Tolerance properties."""

    def test_3_of_4_consensus_passes(self):
        """Verify 3 strong + 1 moderate passes."""
        h, a, e, v = 0.95, 0.95, 0.95, 0.6
        w4 = (h * a * e * v) ** 0.25

        assert w4 >= 0.75, f"3 strong + 1 moderate should pass: W4={w4}"

    def test_2_of_4_consensus_fails(self):
        """Verify 2 strong + 2 reject fails."""
        h, a, e, v = 0.95, 0.95, 0.3, 0.3
        w4 = (h * a * e * v) ** 0.25

        assert w4 < 0.75, f"2/4 should fail: W4={w4}"

    def test_4_of_4_perfect_consensus(self):
        """Verify 4 perfect witnesses = perfect consensus."""
        h, a, e, v = 1.0, 1.0, 1.0, 1.0
        w4 = (h * a * e * v) ** 0.25

        assert abs(w4 - 1.0) < 0.001, f"Perfect consensus should be 1.0, got {w4}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
