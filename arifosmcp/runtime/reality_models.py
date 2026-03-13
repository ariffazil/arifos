from __future__ import annotations
import uuid
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

StatusState = Literal["SUCCESS", "PARTIAL", "SABAR", "VOID", "ERROR"]
Stage = Literal["111_SENSE", "222_REALITY", "333_MIND"]
Verdict = Literal["SEAL", "SABAR", "VOID"]

ErrorCode = Literal[
    "DNS_FAIL", "TLS_FAIL", "TIMEOUT", "WAF_BLOCK",
    "HTTP_4XX", "HTTP_5XX",
    "ENGINE_422", "NO_RESULTS",
    "SCHEMA_FAIL", "PARSE_FAIL",
    "COERCED_MODE", "RENDER_FAIL"
]

class StatusError(BaseModel):
    code: ErrorCode
    detail: str
    recoverable: bool = True
    hint: str = ""

class BundleStatus(BaseModel):
    state: StatusState
    stage: Stage
    verdict: Verdict
    message: str = ""
    errors: List[StatusError] = Field(default_factory=list)

class Policy(BaseModel):
    obey_robots: bool = True
    allow_paywalls: bool = False
    allow_login: bool = False
    max_redirects: int = 10
    max_hops: int = 3

class BundleInput(BaseModel):
    type: Literal["query", "url"]
    value: str
    mode: Literal["auto", "search", "fetch"] = "auto"
    top_k: int = 5
    fetch_top_k: int = 2
    render: Literal["auto", "never", "always"] = "auto"
    budget_ms: int = 15000
    policy: Policy = Field(default_factory=Policy)

class Actor(BaseModel):
    actor_id: str = "anonymous"
    role: str = "user"
    auth_state: Literal["unverified", "verified"] = "unverified"
    authority_level: Literal["anonymous", "user", "admin", "apex"] = "anonymous"
    token_fingerprint: Optional[str] = None

class Claim(BaseModel):
    type: str = "statement"
    text: str
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: float = 1.0

class SearchResult(BaseModel):
    engine: str
    query: str
    status_code: int = 200
    results: List[Dict[str, Any]] = Field(default_factory=list)
    error: Optional[str] = None
    latency_ms: float = 0.0
    request_params: Dict[str, Any] = Field(default_factory=dict)
    response_diagnostics: Dict[str, Any] = Field(default_factory=dict)

class FetchResult(BaseModel):
    url: str
    status_code: Optional[int] = None
    content_type: Optional[str] = None
    content_length: int = 0
    raw_content: Optional[str] = None
    structured_data: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: Dict[str, float] = Field(default_factory=dict) # dns, connect, ttfb, total
    exception_class: Optional[str] = None
    error_message: Optional[str] = None
    redirects: int = 0
    final_url: Optional[str] = None
    headers_subset: Dict[str, str] = Field(default_factory=dict)
    render_fallback_used: bool = False

class EvidenceBundle(BaseModel):
    id: str = Field(default_factory=lambda: f"eb-{uuid.uuid4().hex[:8]}")
    status: BundleStatus
    input: BundleInput
    actor: Actor
    claims: List[Claim] = Field(default_factory=list)
    results: List[Union[SearchResult, FetchResult]] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)

class AtlasNode(BaseModel):
    id: str
    type: Literal["URL", "DOCUMENT", "CLAIM", "ENTITY", "TOPIC", "ENGINE"]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AtlasEdge(BaseModel):
    source: str
    target: str
    type: Literal["DERIVED_FROM", "SUPPORTS", "CONTRADICTS", "MENTIONS", "SAME_AS"]
    weight: float = 1.0

class RealityAtlas(BaseModel):
    nodes: List[AtlasNode] = Field(default_factory=list)
    edges: List[AtlasEdge] = Field(default_factory=list)
    delta: Optional[Dict[str, Any]] = None

class DuplexReport(BaseModel):
    search_health: Dict[str, Any] = Field(default_factory=dict)
    search_winner: Optional[str] = None
    fetch_recommendation: Optional[str] = None
