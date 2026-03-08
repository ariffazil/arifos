/**
 * @arifos/mcp — Type Definitions
 * 
 * L2 Skills Adapter: TypeScript mirrors of arifOS kernel contracts.
 * These types reflect the canonical Python definitions in arifos PyPI package.
 * 
 * Canonical Source: https://pypi.org/project/arifos/
 * Tested Against: arifos 2026.3.7 (PyPI)
 * 
 * NOTE: This package is a CABLE, not the KERNEL. 
 * Governance authority resides in the PyPI arifos package only.
 */

// ═══════════════════════════════════════════════════════════════════════════════
// Constitutional Verdicts
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Final governance verdict from APEX-888 judgment.
 * Maps to Python: core.judgment.Verdict
 */
export type Verdict = 
  | 'SEAL'      // ✅ Passed all 13 floors — execute and vault
  | 'PARTIAL'   // 🟡 Soft floor failures — proceed with warnings
  | 'SABAR'     // ⚠️ Entropy too high — refine and retry
  | 'VOID'      // ❌ Hard floor violation — halt immediately
  | '888_HOLD'  // 🛑 Irreversible action — awaiting human signature
  | 'HOLD';     // 🛑 Legacy/Transition: Awaiting human signature

/**
 * Verdict with metadata returned by apex_judge tool.
 */
export interface VerdictEnvelope {
  verdict: Verdict;
  stage: Stage;
  session_id: string;
  floors: {
    passed: FloorCode[];
    failed: FloorCode[];
  };
  truth?: {
    score: number | null;
    threshold: number | null;
    drivers: string[];
  };
  next_actions?: string[];
  sabar_requirements?: any;
  governance_token?: string;  // HMAC-SHA256 signed by apex_judge
  payload?: any;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Constitutional Floors (F1-F13)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * The 13 Constitutional Floors of arifOS.
 * Structure: 9 Floors + 2 Mirrors + 2 Walls = 13 LAWS
 * 
 * Source: 000_THEORY/000_LAW.md
 */
export type FloorCode =
  // 9 Operational Floors
  | 'F1'   // Amanah (Trust) — Hard: Irreversible actions require lock
  | 'F2'   // Truth — Hard: Factual fidelity τ ≥ 0.99
  | 'F4'   // Clarity — Hard: Entropy reduction ΔS ≤ 0
  | 'F5'   // Peace — Soft: Dynamic stability P² ≥ 1.0
  | 'F6'   // Empathy — Soft: Harm impact κᵣ ≥ 0.70
  | 'F7'   // Humility — Hard: Uncertainty band Ω₀ ∈ [0.03, 0.15]
  | 'F9'   // Anti-Hantu — Soft: Dark heuristics C_dark < 0.30
  | 'F11'  // Authority — Hard: Cryptographic identity check
  | 'F13'  // Sovereign — Hard: Human veto available
  // 2 Mirrors (Feedback Loops)
  | 'F3'   // Tri-Witness — Mirror: W³ ≥ 0.95
  | 'F8'   // Genius — Mirror: G = A × P × X × E² ≥ 0.80
  // 2 Walls (Binary Gates)
  | 'F10'  // Ontology — Wall: No consciousness claims
  | 'F12'; // Defense — Wall: Injection risk < 0.85

/**
 * Floor type classification.
 */
export type FloorType = 'HARD' | 'SOFT' | 'MIRROR' | 'WALL';

/**
 * Floor enforcement level.
 */
export const FLOOR_TYPES: Record<FloorCode, FloorType> = {
  F1: 'HARD',
  F2: 'HARD',
  F4: 'HARD',
  F5: 'SOFT',
  F6: 'SOFT',
  F7: 'HARD',
  F9: 'SOFT',
  F11: 'HARD',
  F13: 'HARD',
  F3: 'MIRROR',
  F8: 'MIRROR',
  F10: 'WALL',
  F12: 'WALL',
};

/**
 * Individual floor evaluation result.
 */
export interface FloorResult {
  floor: FloorCode;
  passed: boolean;
  type: FloorType;
  score?: number;
  threshold?: number;
  evidence?: string[];
  message?: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Metabolic Stages (000-999)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * The 7-Organ Sovereign Stack — metabolic loop stages.
 * Every request flows: 000 → 111-333 → 444 → 555-666 → 777 → 888 → 999
 */
export type Stage =
  | '000_INIT'           // Airlock: Session ignition, injection defense
  | '111-444'           // Broad range for AGI reasoning
  | '111_SENSE'          // AGI: Perception grounding
  | '222_REASON'         // AGI: Hypothesis generation
  | '333_MIND'           // AGI: Causal tracing
  | '444_PHOENIX'        // Subconscious: Memory recall (EUREKA sieve)
  | '555_RECALL'         // Subconscious: Actual string returned by server
  | '555-666'           // ASI: Broad range for Empathy
  | '555_HEART'          // ASI: Stakeholder impact analysis
  | '666_CRITIQUE'       // ASI: Self-critique, bias detection
  | '777-888'           // SOUL: Synthesis range
  | '777_FORGE'          // Actuator: Sandboxed execution
  | '888_APEX'           // Soul: Sovereign judgment
  | '888_APEX_JUDGE'     // Soul: Actual string from some server versions
  | '888_FORGE'          // Soul: Actual string for actuator
  | '999_VAULT';         // Memory: Immutable ledger commit

/**
 * Stage metadata for UI/rendering.
 */
export interface StageMeta {
  stage: Stage;
  name: string;
  organ: 'INIT' | 'AGI' | 'PHOENIX' | 'ASI' | 'FORGE' | 'APEX' | 'VAULT';
  trinity: 'Δ' | 'Ω' | 'Ψ' | '-';
  description: string;
}

export const STAGE_METADATA: Record<Stage, StageMeta> = {
  '000_INIT': { stage: '000_INIT', name: 'INIT', organ: 'INIT', trinity: '-', description: 'Session ignition & injection defense' },
  '111-444': { stage: '111-444', name: 'AGI_MIND', organ: 'AGI', trinity: 'Δ', description: 'Composite AGI reasoning range' },
  '111_SENSE': { stage: '111_SENSE', name: 'SENSE', organ: 'AGI', trinity: 'Δ', description: 'Perception grounding' },
  '222_REASON': { stage: '222_REASON', name: 'REASON', organ: 'AGI', trinity: 'Δ', description: 'Hypothesis generation' },
  '333_MIND': { stage: '333_MIND', name: 'MIND', organ: 'AGI', trinity: 'Δ', description: 'Causal tracing' },
  '444_PHOENIX': { stage: '444_PHOENIX', name: 'PHOENIX', organ: 'PHOENIX', trinity: '-', description: 'Memory recall via EUREKA sieve' },
  '555_RECALL': { stage: '555_RECALL', name: 'RECALL', organ: 'PHOENIX', trinity: '-', description: 'Associative memory retrieval' },
  '555-666': { stage: '555-666', name: 'ASI_HEART', organ: 'ASI', trinity: 'Ω', description: 'Composite ASI alignment range' },
  '555_HEART': { stage: '555_HEART', name: 'HEART', organ: 'ASI', trinity: 'Ω', description: 'Stakeholder impact analysis' },
  '666_CRITIQUE': { stage: '666_CRITIQUE', name: 'CRITIQUE', organ: 'ASI', trinity: 'Ω', description: 'Self-critique & bias detection' },
  '777-888': { stage: '777-888', name: 'APEX_SOUL', organ: 'APEX', trinity: 'Ψ', description: 'Composite Sovereign judgment range' },
  '777_FORGE': { stage: '777_FORGE', name: 'FORGE', organ: 'FORGE', trinity: '-', description: 'Sandboxed execution' },
  '888_APEX': { stage: '888_APEX', name: 'APEX', organ: 'APEX', trinity: 'Ψ', description: 'Sovereign judgment' },
  '888_APEX_JUDGE': { stage: '888_APEX_JUDGE', name: 'APEX_JUDGE', organ: 'APEX', trinity: 'Ψ', description: 'Sovereign judgment (legacy)' },
  '888_FORGE': { stage: '888_FORGE', name: 'FORGE', organ: 'FORGE', trinity: '-', description: 'World interaction actuator' },
  '999_VAULT': { stage: '999_VAULT', name: 'VAULT', organ: 'VAULT', trinity: '-', description: 'Immutable ledger commit' },
};

// ═══════════════════════════════════════════════════════════════════════════════
// Truth & Evidence
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Truth claim with evidence backing.
 * Maps to Python: core.shared.types.TruthClaim
 */
export interface TruthClaim {
  claim: string;
  confidence: number;  // 0.0 - 1.0
  evidence: Evidence[];
  sources: Source[];
  uncertainty_band?: [number, number];  // [Ω₀_min, Ω₀_max]
}

/**
 * Individual evidence item.
 */
export interface Evidence {
  id: string;
  type: 'web' | 'document' | 'calculation' | 'memory' | 'human';
  content: string;
  relevance: number;  // 0.0 - 1.0
  timestamp: string;
}

/**
 * Source attribution.
 */
export interface Source {
  uri: string;
  title?: string;
  timestamp: string;
  trust_tier: 'primary' | 'secondary' | 'tertiary';
}

// ═══════════════════════════════════════════════════════════════════════════════
// Session & Metadata
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * arifOS session metadata.
 */
export interface ArifOSMetadata {
  session_id: string;
  version: string;
  stage: Stage;
  verdict: Verdict;
  floors: {
    passed: FloorCode[];
    failed: FloorCode[];
  };
  timestamp: string;
  governance_token?: string;
}

/**
 * Client configuration options.
 */
export interface ArifOSClientConfig {
  /** Transport mode */
  transport: 'stdio' | 'sse' | 'http';
  
  /** Endpoint URL (for SSE/HTTP) */
  endpoint?: string;
  
  /** Environment variables (for stdio) */
  env?: Record<string, string>;
  
  /** Request timeout in milliseconds */
  timeout?: number;
  
  /** Enable debug logging */
  debug?: boolean;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Tool Definitions (13 Canonical Tools)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * The 13 canonical MCP tools exposed by arifOS.
 * Source of truth: arifOS health endpoint tools_loaded=13
 * Last verified: 2026.03.07-ARCH-SEAL
 */
export type ArifOSToolName =
  // Metabolic spine — governance loop (000→999)
  | 'anchor_session'    // 000: session ignition + injection defense
  | 'reason_mind'       // 333: AGI cognition
  | 'vector_memory'     // 444: semantic recall from VAULT999
  | 'simulate_heart'    // 555: stakeholder empathy
  | 'critique_thought'  // 666: bias critique
  | 'eureka_forge'      // 777: sandboxed execution
  | 'apex_judge'        // 888: sovereign verdict
  | 'seal_vault'        // 999: immutable ledger commit
  | 'metabolic_loop'    // 000-999: full cycle in one call
  // Evidence tools (read-only)
  | 'search_reality'    // web grounding
  | 'ingest_evidence'   // URL/file fetch
  | 'audit_rules'       // constitutional audit
  | 'check_vital';      // system health

/**
 * Tool metadata.
 */
export interface ToolMeta {
  name: ArifOSToolName;
  stage: Stage;
  floors: FloorCode[];
  readOnly: boolean;
  description: string;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Error Types
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * arifOS-specific error codes.
 */
export type ArifOSErrorCode =
  | 'CONNECTION_FAILED'
  | 'TIMEOUT'
  | 'INVALID_RESPONSE'
  | 'GOVERNANCE_TOKEN_INVALID'
  | 'FLOOR_VIOLATION'
  | 'STAGE_MISMATCH'
  | 'TRANSPORT_ERROR';

/**
 * arifOS client error.
 */
export class ArifOSError extends Error {
  constructor(
    message: string,
    public readonly code: ArifOSErrorCode,
    public readonly stage?: Stage,
    public readonly floor?: FloorCode,
    public readonly cause?: unknown
  ) {
    super(message);
    this.name = 'ArifOSError';
  }
}
