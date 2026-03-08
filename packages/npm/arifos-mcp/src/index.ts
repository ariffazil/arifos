/**
 * @arifos/mcp — Main Entry Point
 * 
 * Constitutional AI Governance System — TypeScript Client Adapter
 * 
 * L2 Skills Layer: Cable, not Kernel.
 * Governance authority resides in PyPI arifos package ONLY.
 * 
 * @packageDocumentation
 * @module @arifos/mcp
 */

// ═══════════════════════════════════════════════════════════════════════════════
// Core Exports
// ═══════════════════════════════════════════════════════════════════════════════

export {
  // Client factory
  createClient,
  quickConnect,
  // Types from client
  type ArifOSMCPClient,
  type Transport,
} from './client.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Type Exports
// ═══════════════════════════════════════════════════════════════════════════════

export {
  // Verdicts
  type Verdict,
  type VerdictEnvelope,
  
  // Floors
  type FloorCode,
  type FloorType,
  type FloorResult,
  FLOOR_TYPES,
  
  // Stages
  type Stage,
  type StageMeta,
  STAGE_METADATA,
  
  // Truth & Evidence
  type TruthClaim,
  type Evidence,
  type Source,
  
  // Session & Config
  type ArifOSMetadata,
  type ArifOSClientConfig,
  
  // Tools
  type ArifOSToolName,
  type ToolMeta,
  
  // Errors
  type ArifOSErrorCode,
  ArifOSError,
} from './types.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Version
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Package version.
 * 0.3.0 — sync to arifos 2026.3.7: correct 13 tool names, python3, metabolic_loop added
 */
export const VERSION = '0.3.0';

/**
 * Compatible arifOS PyPI versions.
 */
export const ARIFOS_COMPATIBILITY = [
  '2026.2.17',    // Canonical stable
  '2026.2.28',    // Published
  '2026.3.1',     // Dev/Sync
  '2026.3.7',     // Current — ARCH-SEAL (13 tools verified)
] as const;

/**
 * Canonical arifOS MCP server endpoints.
 */
export const ENDPOINTS = {
  /** Official VPS endpoint */
  VPS: 'https://arifosmcp.arif-fazil.com/mcp',
  /** Health check endpoint */
  HEALTH: 'https://arifosmcp.arif-fazil.com/health',
  /** SSE fallback */
  SSE: 'https://arifosmcp.arif-fazil.com/sse',
} as const;
