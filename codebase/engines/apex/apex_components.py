"""
Component-module for APEXRoom (Soul)
A1 Judiciary, A2 Consensus, A3 Governance

v55.5: Updated to use eigendecomposition-based Genius calculation.
Theory: 000_FOUNDATIONS.md §3.2 — The APEX 4 Dials
"""

import logging
from typing import Dict, Any, List, Optional
from codebase.bundles import DeltaBundle, OmegaBundle, EngineVote, TriWitnessConsensus
from codebase.floors import FloorScores, extract_dials, GeniusCalculator

logger = logging.getLogger(__name__)


class JudiciaryValidator:
    """A1: Judiciary Validator — Computes F8 Genius from floor eigendecomposition."""
    
    def calculate_genius_index(self, delta: DeltaBundle, omega: OmegaBundle) -> Dict[str, Any]:
        """
        F8: Genius Index calculation via eigendecomposition.
        
        Converts 13 floor scores → 4 APEX dials (A/P/X/E) → G = A×P×X×E²
        
        Returns:
            Dict with 'G' (genius score), 'dials' (A/P/X/E), and metadata
        """
        # Build FloorScores from Delta/Omega bundles
        # Map bundle fields to floor scores
        floors = FloorScores(
            f1_amanah=1.0 if delta.reversible else 0.0,
            f2_truth=delta.truth_score,
            f3_tri_witness=delta.tri_witness_score if hasattr(delta, 'tri_witness_score') else 0.95,
            f4_clarity=delta.clarity_delta if hasattr(delta, 'clarity_delta') else 0.0,
            f5_peace=omega.peace_squared if hasattr(omega, 'peace_squared') else 1.0,
            f6_empathy=omega.empathy_kappa,
            f7_humility=1.0 - omega.omega_0 if hasattr(omega, 'omega_0') else 0.96,
            f8_genius=delta.genius_score if hasattr(delta, 'genius_score') else 0.80,
            f9_antihantu=1.0 - omega.c_dark if hasattr(omega, 'c_dark') else 0.95,
            f10_ontology=1.0 if delta.typed else 0.0,
            f11_command=1.0 if delta.authority_verified else 0.0,
            f12_injection=1.0 - omega.injection_risk if hasattr(omega, 'injection_risk') else 0.99,
            f13_sovereign=1.0 if omega.human_present else 0.0,
        )
        
        # Extract dials via eigendecomposition
        dials = extract_dials(floors)
        
        # Calculate Genius
        A, P, X, E = dials['A'], dials['P'], dials['X'], dials['E']
        G = A * P * X * (E ** 2)
        
        return {
            'G': G,
            'dials': dials,
            'floor_scores': floors,
            'threshold': 0.80,
            'passed': G >= 0.80,
            'weakest_dial': min(dials, key=dials.get),
            'derivation': 'eigendecomposition_of_floors',
        }
    
    def get_simple_genius(self, delta: DeltaBundle, omega: OmegaBundle) -> float:
        """
        Backward-compatible method returning just the G score.
        
        DEPRECATED: Use calculate_genius_index() for full dial breakdown.
        """
        result = self.calculate_genius_index(delta, omega)
        return result['G']


class TrinityConsensusEngine:
    """A2: Consensus Engine - Independent vote aggregation."""
    
    def compute_consensus(self, delta: DeltaBundle, omega: OmegaBundle) -> TriWitnessConsensus:
        """
        Aggregate AGI and ASI votes.
        Enforces Trinity Dissent Law.
        """
        logger.info(f"[APEX-CONSENSUS] Aggregating Δ({delta.vote.value}) and Ω({omega.vote.value})")
        
        votes_agree = delta.vote == omega.vote
        
        # Min confidence for consensus score
        consensus_score = min(delta.truth_score, omega.empathy_kappa)
        
        dissent_reason = ""
        if not votes_agree:
            dissent_reason = f"DISSENT: AGI={delta.vote.value}, ASI={omega.vote.value}"
            
        return TriWitnessConsensus(
            agi_vote=delta.vote,
            asi_vote=omega.vote,
            votes_agree=votes_agree,
            consensus_score=consensus_score,
            dissent_reason=dissent_reason
        )


class APEXDialFormatter:
    """
    A3: Output Formatter — Renders 4-dial verdict display.
    
    Converts complex floor scores into human-readable 4-bar output.
    """
    
    @staticmethod
    def format_dials(dials: Dict[str, float], G: float, verdict: str) -> str:
        """
        Format 4 dials as ASCII bar chart.
        
        Example output:
            A (Mind):    0.94 ████████████░
            P (Peace):   0.87 ██████████░░░
            X (Explore): 0.82 █████████░░░░  ← Weakest
            E (Energy):  0.91 ███████████░░
            
            G = 0.556 (threshold: 0.80) → SABAR
        """
        def bar(value: float, width: int = 12) -> str:
            filled = int(value * width)
            return '█' * filled + '░' * (width - filled)
        
        weakest = min(dials, key=dials.get)
        
        lines = [
            f"  A (Mind):    {dials['A']:.2f} {bar(dials['A'])}",
            f"  P (Peace):   {dials['P']:.2f} {bar(dials['P'])}",
            f"  X (Explore): {dials['X']:.2f} {bar(dials['X'])}  {'← Weakest' if weakest == 'X' else ''}",
            f"  E (Energy):  {dials['E']:.2f} {bar(dials['E'])}",
            "",
            f"  G = {dials['A']:.2f} × {dials['P']:.2f} × {dials['X']:.2f} × {dials['E']:.2f}² = {G:.3f}",
            f"  Threshold: 0.80 → {verdict}",
        ]
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_compact(floors: FloorScores, G: float, verdict: str) -> Dict[str, Any]:
        """
        Return compact JSON-serializable output with 4 dials.
        
        Replaces the old 13-floor dump with clean 4-dial summary.
        """
        dials = extract_dials(floors)
        
        return {
            'verdict': verdict,
            'genius': {
                'G': round(G, 4),
                'threshold': 0.80,
                'passed': G >= 0.80,
            },
            'dials': {
                'A': {'name': 'Mind', 'value': round(dials['A'], 3)},
                'P': {'name': 'Peace', 'value': round(dials['P'], 3)},
                'X': {'name': 'Explore', 'value': round(dials['X'], 3)},
                'E': {'name': 'Energy', 'value': round(dials['E'], 3)},
            },
            'weakest': min(dials, key=dials.get),
            'derivation': 'eigendecomposition',
        }
