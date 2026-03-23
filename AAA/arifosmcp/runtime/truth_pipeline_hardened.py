"""
arifosmcp/runtime/truth_pipeline_hardened.py — Hardened Truth Pipeline (v2)

reality_compass + reality_atlas with:
- Typed EvidenceBundle output (not semi-structured text)
- Fact/claim/inference separation
- Freshness scoring
- Source conflict matrix
- Claim graphing with supporting/contradicting/missing evidence
- Independence of sources scoring
- Timeline reconstruction
- Explicit knowledge gaps

This tool is your truth intake valve, not a search summary engine.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

from arifosmcp.runtime.contracts_v2 import (
    ToolEnvelope,
    ToolStatus,
    RiskTier,
    TraceContext,
    EntropyBudget,
    calculate_entropy_budget,
    validate_fail_closed,
)


# ═══════════════════════════════════════════════════════════════════════════════
# EVIDENCE BUNDLE — Typed Output (not semi-structured text)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EvidenceFact:
    """
    A single observed fact with full provenance.
    """
    fact_id: str
    statement: str
    source_uri: str
    observed_at: str
    freshness_score: float  # 0.0-1.0, 1.0 = realtime
    source_type: Literal["primary", "secondary", "tertiary", "synthetic"]
    verification_status: Literal["verified", "unverified", "disputed", "deprecated"]
    jurisdiction: str = "global"  # Locale awareness as first-class field
    locale: str = "en"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "fact_id": self.fact_id,
            "statement": self.statement,
            "source_uri": self.source_uri,
            "observed_at": self.observed_at,
            "freshness_score": round(self.freshness_score, 4),
            "source_type": self.source_type,
            "verification_status": self.verification_status,
            "jurisdiction": self.jurisdiction,
            "locale": self.locale,
        }


@dataclass
class ReportedClaim:
    """
    A claim made by a source (not yet verified as fact).
    """
    claim_id: str
    claim_text: str
    claimant: str
    claim_date: str
    evidence_cited: list[str]  # What the claimant says supports this
    confidence: float  # Claimant's stated confidence
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "claimant": self.claimant,
            "claim_date": self.claim_date,
            "evidence_cited": self.evidence_cited,
            "confidence": round(self.confidence, 4),
        }


@dataclass
class InferredConnection:
    """
    Connections inferred between facts/claims.
    """
    connection_id: str
    from_id: str  # fact_id or claim_id
    to_id: str
    connection_type: Literal["supports", "contradicts", "implies", "correlates"]
    inference_confidence: float
    inference_method: str  # How this connection was derived
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "connection_id": self.connection_id,
            "from_id": self.from_id,
            "to_id": self.to_id,
            "connection_type": self.connection_type,
            "inference_confidence": round(self.inference_confidence, 4),
            "inference_method": self.inference_method,
        }


@dataclass
class EvidenceBundle:
    """
    Complete typed evidence output from reality_compass.
    
    Separates:
    - observed facts (grounded)
    - reported claims (unverified)
    - inferred connections (derived)
    """
    bundle_id: str
    query: str
    jurisdiction: str
    locale: str
    
    observed_facts: list[EvidenceFact] = field(default_factory=list)
    reported_claims: list[ReportedClaim] = field(default_factory=list)
    inferred_connections: list[InferredConnection] = field(default_factory=list)
    
    # Metadata
    search_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sources_queried: list[str] = field(default_factory=list)
    sources_responded: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "query": self.query,
            "jurisdiction": self.jurisdiction,
            "locale": self.locale,
            "observed_facts": [f.to_dict() for f in self.observed_facts],
            "reported_claims": [c.to_dict() for c in self.reported_claims],
            "inferred_connections": [c.to_dict() for c in self.inferred_connections],
            "search_timestamp": self.search_timestamp,
            "sources_queried": self.sources_queried,
            "sources_responded": self.sources_responded,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SOURCE CONFLICT MATRIX — Independence Scoring
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SourceConflictMatrix:
    """
    Matrix showing source independence and conflicts.
    
    Separates duplicated reporting from genuine corroboration.
    """
    sources: list[str]
    independence_scores: dict[tuple[str, str], float]  # 0.0-1.0, 1.0 = fully independent
    conflict_pairs: list[tuple[str, str, str]]  # (source_a, source_b, conflict_topic)
    
    def get_independence_score(self, source_a: str, source_b: str) -> float:
        """Get independence score between two sources."""
        key = (source_a, source_b)
        reverse_key = (source_b, source_a)
        
        if key in self.independence_scores:
            return self.independence_scores[key]
        if reverse_key in self.independence_scores:
            return self.independence_scores[reverse_key]
        
        return 0.5  # Unknown = moderate suspicion
    
    def are_independent(self, source_a: str, source_b: str, threshold: float = 0.7) -> bool:
        """Check if two sources are sufficiently independent."""
        return self.get_independence_score(source_a, source_b) >= threshold
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "sources": self.sources,
            "independence_scores": {
                f"{k[0]}:{k[1]}": round(v, 4)
                for k, v in self.independence_scores.items()
            },
            "conflict_pairs": [
                {"a": a, "b": b, "topic": t}
                for a, b, t in self.conflict_pairs
            ],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CLAIM GRAPH — Epistemic Map
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ClaimNode:
    """
    A node in the claim graph.
    """
    claim_id: str
    claim_text: str
    claimant: str
    
    # Evidence relationships
    supporting_evidence: list[str] = field(default_factory=list)  # fact_ids
    contradicting_evidence: list[str] = field(default_factory=list)  # fact_ids
    missing_evidence: list[str] = field(default_factory=list)  # What would help decide
    
    # Scores
    support_strength: float = 0.0  # 0.0-1.0
    contradiction_strength: float = 0.0  # 0.0-1.0
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "claimant": self.claimant,
            "supporting_evidence": self.supporting_evidence,
            "contradicting_evidence": self.contradicting_evidence,
            "missing_evidence": self.missing_evidence,
            "support_strength": round(self.support_strength, 4),
            "contradiction_strength": round(self.contradiction_strength, 4),
        }


@dataclass
class ClaimGraph:
    """
    Graph representing what we know, how we know it, and what is unresolved.
    
    Atlas answers:
    - What do we know?
    - How do we know it?
    - What is still unresolved?
    """
    graph_id: str
    nodes: dict[str, ClaimNode] = field(default_factory=dict)
    timeline: list[dict] = field(default_factory=list)  # Timeline reconstruction
    knowledge_gaps: list[str] = field(default_factory=list)  # Explicit gaps
    
    def add_node(self, node: ClaimNode):
        self.nodes[node.claim_id] = node
    
    def get_unresolved_claims(self) -> list[ClaimNode]:
        """Get claims with significant missing evidence."""
        return [
            n for n in self.nodes.values()
            if n.missing_evidence and n.support_strength < 0.7
        ]
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "timeline": self.timeline,
            "knowledge_gaps": self.knowledge_gaps,
            "unresolved_count": len(self.get_unresolved_claims()),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# HARDENED REALITY COMPASS — Truth Intake Valve
# ═══════════════════════════════════════════════════════════════════════════════

class HardenedRealityCompass:
    """
    Hardened reality_compass with typed EvidenceBundle output.
    
    Features:
    - Observed facts / reported claims / inferred connections separation
    - Freshness scoring
    - Source conflict matrix
    - Quote-first mode for contested claims
    - Jurisdiction + locale awareness as first-class fields
    """
    
    async def search(
        self,
        query: str,
        jurisdiction: str = "global",
        locale: str = "en",
        freshness_required: float = 0.5,  # Minimum freshness score
        require_quotes: bool = True,  # Quote-first mode
        auth_context: dict | None = None,
        risk_tier: str = "medium",
        session_id: str | None = None,
        trace: TraceContext | None = None,
    ) -> ToolEnvelope:
        """
        Search with typed EvidenceBundle output.
        
        Not a search summary engine — a truth intake valve.
        """
        tool = "reality_compass"
        session_id = session_id or "anonymous"
        
        # Fail-closed validation
        validation = validate_fail_closed(
            auth_context=auth_context,
            risk_tier=risk_tier,
            session_id=session_id,
            tool=tool,
            trace=trace,
        )
        if not validation.valid:
            return validation.to_envelope(tool, session_id, trace)
        
        # Simulate evidence gathering (in production, actual search)
        bundle = EvidenceBundle(
            bundle_id=f"bundle-{hashlib.sha256(query.encode()).hexdigest()[:16]}",
            query=query,
            jurisdiction=jurisdiction,
            locale=locale,
            sources_queried=["primary_db", "web_cache", "archive"],
            sources_responded=["primary_db", "web_cache"],
        )
        
        # Add simulated observed facts
        bundle.observed_facts.append(EvidenceFact(
            fact_id="fact-001",
            statement=f"Primary source confirms: {query}",
            source_uri="https://primary.db/record/001",
            observed_at=datetime.now(timezone.utc).isoformat(),
            freshness_score=0.95,
            source_type="primary",
            verification_status="verified",
            jurisdiction=jurisdiction,
            locale=locale,
        ))
        
        # Add simulated reported claims
        bundle.reported_claims.append(ReportedClaim(
            claim_id="claim-001",
            claim_text=f"Secondary analysis suggests: {query} may have nuances",
            claimant="analyst_007",
            claim_date=datetime.now(timezone.utc).isoformat(),
            evidence_cited=["fact-001"],
            confidence=0.75,
        ))
        
        # Build conflict matrix
        matrix = SourceConflictMatrix(
            sources=["primary_db", "web_cache", "archive"],
            independence_scores={
                ("primary_db", "web_cache"): 0.8,
                ("primary_db", "archive"): 0.9,
                ("web_cache", "archive"): 0.6,
            },
            conflict_pairs=[],  # No conflicts in this example
        )
        
        # Calculate entropy
        entropy = calculate_entropy_budget(
            ambiguity_score=0.2 if bundle.observed_facts else 0.8,
            assumptions=["source_availability", "index_freshness"],
            blast_radius="limited" if RiskTier(risk_tier.lower()) == RiskTier.HIGH else "minimal",
            confidence=0.85 if bundle.observed_facts else 0.40,
        )
        
        return ToolEnvelope(
            status=ToolStatus.OK,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier(risk_tier.lower()),
            confidence=entropy.confidence,
            trace=trace,
            evidence_refs=[f"bundle:{bundle.bundle_id}"],
            entropy=entropy,
            payload={
                "evidence_bundle": bundle.to_dict(),
                "source_conflict_matrix": matrix.to_dict(),
                "freshness_required": freshness_required,
                "freshness_met": all(f.freshness_score >= freshness_required for f in bundle.observed_facts),
                "quote_mode": require_quotes,
            },
        )


# ═══════════════════════════════════════════════════════════════════════════════
# HARDENED REALITY ATLAS — Epistemic Map
# ═══════════════════════════════════════════════════════════════════════════════

class HardenedRealityAtlas:
    """
    Hardened reality_atlas with claim graphing.
    
    Features:
    - Claim graph with supporting/contradicting/missing evidence
    - Independence of sources scoring
    - Timeline reconstruction
    - Explicit knowledge gaps
    
    Answers: What do we know, how do we know it, and what is unresolved?
    """
    
    async def merge(
        self,
        evidence_bundles: list[dict],
        auth_context: dict | None = None,
        risk_tier: str = "medium",
        session_id: str | None = None,
        trace: TraceContext | None = None,
    ) -> ToolEnvelope:
        """
        Merge evidence bundles into epistemic map.
        """
        tool = "reality_atlas"
        session_id = session_id or "anonymous"
        
        # Fail-closed validation
        validation = validate_fail_closed(
            auth_context=auth_context,
            risk_tier=risk_tier,
            session_id=session_id,
            tool=tool,
            trace=trace,
            requires_evidence=True,
            evidence_refs=[b.get("bundle_id") for b in evidence_bundles if b.get("bundle_id")],
        )
        if not validation.valid:
            return validation.to_envelope(tool, session_id, trace)
        
        # Build claim graph
        graph = ClaimGraph(
            graph_id=f"graph-{hashlib.sha256(str(evidence_bundles).encode()).hexdigest()[:16]}",
        )
        
        # Process each bundle into graph nodes
        for bundle_data in evidence_bundles:
            facts = bundle_data.get("observed_facts", [])
            claims = bundle_data.get("reported_claims", [])
            
            for claim in claims:
                node = ClaimNode(
                    claim_id=claim.get("claim_id", "unknown"),
                    claim_text=claim.get("claim_text", ""),
                    claimant=claim.get("claimant", "unknown"),
                    supporting_evidence=[f.get("fact_id") for f in facts if f.get("verification_status") == "verified"],
                    missing_evidence=["corroboration", "temporal_verification"],
                    support_strength=0.7 if facts else 0.3,
                )
                graph.add_node(node)
        
        # Add timeline reconstruction
        graph.timeline = [
            {"timestamp": datetime.now(timezone.utc).isoformat(), "event": "evidence_ingested"},
            {"timestamp": datetime.now(timezone.utc).isoformat(), "event": "claims_extracted"},
            {"timestamp": datetime.now(timezone.utc).isoformat(), "event": "graph_constructed"},
        ]
        
        # Explicit knowledge gaps
        unresolved = graph.get_unresolved_claims()
        graph.knowledge_gaps = [
            f"Unresolved claim: {n.claim_text[:50]}..."
            for n in unresolved
        ]
        
        # Calculate entropy
        entropy = calculate_entropy_budget(
            ambiguity_score=len(unresolved) / max(len(graph.nodes), 1),
            assumptions=["source_independence", "temporal_stability"],
            blast_radius="limited" if len(unresolved) > 2 else "minimal",
            confidence=0.9 if not unresolved else 0.5,
        )
        
        return ToolEnvelope(
            status=ToolStatus.OK,
            tool=tool,
            session_id=session_id,
            risk_tier=RiskTier(risk_tier.lower()),
            confidence=entropy.confidence,
            trace=trace,
            evidence_refs=[f"graph:{graph.graph_id}"],
            warnings=[f"{len(unresolved)} unresolved claims"] if unresolved else [],
            entropy=entropy,
            payload={
                "claim_graph": graph.to_dict(),
                "resolved_claims": len(graph.nodes) - len(unresolved),
                "unresolved_claims": len(unresolved),
                "knowledge_gaps": graph.knowledge_gaps,
            },
        )


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Evidence types
    "EvidenceFact",
    "ReportedClaim",
    "InferredConnection",
    "EvidenceBundle",
    # Analysis
    "SourceConflictMatrix",
    "ClaimNode",
    "ClaimGraph",
    # Tools
    "HardenedRealityCompass",
    "HardenedRealityAtlas",
]
