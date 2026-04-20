import { z } from 'zod';

/**
 * GEOX Contract Pack v1 — Sovereign Witness Schemas
 * ═══════════════════════════════════════════════════════════════════════════════
 * DITEMPA BUKAN DIBERI
 */

// ═══════════════════════════════════════════════════════════════════════════════
// Dimensions & App Contracts
// ═══════════════════════════════════════════════════════════════════════════════

export const DimensionEnum = z.enum([
  'PROSPECT',  // Basin/Play scale, ranking, economics
  'WELL',      // Borehole scale, logs, markers, petrophysics
  'SECTION',   // 2D interpretation on Seismic/Transects
  'EARTH_3D',  // Volumetric interpretation, attributes, surfaces
  'TIME_4D',   // 4D seismic, production dynamics, reservoir history
  'PHYSICS',   // Governance, thermodynamic audit, constitutional reality
  'MAP',       // Transversal: Geospatial reference, CRS, navigation
]);

export type Dimension = z.infer<typeof DimensionEnum>;

export const AppDomainEnum = z.enum([
  'seismic',
  'petrophysics',
  'geology',
  'economics',
  'governance',
  'general',
]);

// ═══════════════════════════════════════════════════════════════════════════════
// Foundational Primitives
// ═══════════════════════════════════════════════════════════════════════════════

export const UnitRefSchema = z.object({
  name: z.string(),   // e.g. "millisecond"
  symbol: z.string(), // e.g. "ms"
  quantity: z.string() // e.g. "time", "length"
});

export const XYPointSchema = z.object({
  x: z.number(),
  y: z.number(),
});

export const XYZPointSchema = z.object({
  x: z.number(),
  y: z.number(),
  z: z.number(),
});

export const BoundingBoxSchema = z.object({
  min: XYZPointSchema,
  max: XYZPointSchema,
  crs: z.string().optional(),
});

// ═══════════════════════════════════════════════════════════════════════════════
// GeoContext — Spatial Laws
// ═══════════════════════════════════════════════════════════════════════════════

export const GeoContextSchema = z.object({
  crsName: z.string(),
  crsEpsg: z.number().int().positive(),
  verticalDomain: z.enum(['twt_ms', 'tvdss_m', 'md_m', 'tvd_m']),
  isTimeDomain: z.boolean(),
  units: z.object({
    horizontal: UnitRefSchema,
    vertical: UnitRefSchema,
  }),
});

// ═══════════════════════════════════════════════════════════════════════════════
// Evidence — Observation References
// ═══════════════════════════════════════════════════════════════════════════════

export const EvidenceRefSchema = z.object({
  id: z.string(),
  kind: z.enum(['well', 'seismic', 'map', 'log', 'top', 'verdict']),
  sourceUri: z.string(), // e.g. "opendtect://Well/A1" or "geox://storage/prospect_alpha"
  timestamp: z.string().datetime(),
  version: z.string().optional(),
});

export const EvidenceObjectSchema = z.object({
  ref: EvidenceRefSchema,
  context: GeoContextSchema,
  payload: z.any(), // Specific app-side parsing per kind
  metadata: z.record(z.string(), z.any()).optional(),
});

// ═══════════════════════════════════════════════════════════════════════════════
// Transform — Spatial Movements
// ═══════════════════════════════════════════════════════════════════════════════

export const TransformRequestSchema = z.object({
  requestId: z.string(),
  sourceContext: GeoContextSchema,
  targetContext: GeoContextSchema,
  dataToTransform: z.array(XYZPointSchema),
  method: z.string().default('bilinear'),
});

export const TransformResultSchema = z.object({
  requestId: z.string(),
  transformedData: z.array(XYZPointSchema),
  errorRms: z.number().optional(),
  status: z.enum(['SUCCESS', 'PARTIAL', 'FAILED']),
});

// ═══════════════════════════════════════════════════════════════════════════════
// Governance — The 888_JUDGE Kernel
// ═══════════════════════════════════════════════════════════════════════════════

export const ConstraintSetSchema = z.object({
  laws: z.array(z.string()), // e.g. ["F2_TRUTH", "F7_HUMILITY"]
  thresholds: z.record(z.string(), z.number()),
});

export const RiskAssessmentSchema = z.object({
  score: z.number().min(0).max(1), // 0 is safe, 1 is VOID
  factors: z.array(z.object({
    key: z.string(),
    impact: z.number(),
    reason: z.string(),
  })),
});

export const VerdictSchema = z.object({
  verdictId: z.string(),
  intentId: z.string(),
  status: z.enum(['SEAL', 'PARTIAL', 'SABAR', 'VOID', '888_HOLD']),
  confidence: z.number().min(0).max(1),
  author: z.string(),
  rationale: z.string(),
  risk: RiskAssessmentSchema,
  auditTraceId: z.string(),
  timestamp: z.string().datetime(),
});

export const AuditEventSchema = z.object({
  eventId: z.string(),
  actor: z.string(),
  tool: z.string(),
  evidenceRefs: z.array(z.string()),
  verdictId: z.string().optional(),
  inputSnapshot: z.any(),
  outputSnapshot: z.any(),
  timestamp: z.string().datetime(),
});

export const AppManifestSchema = z.object({
  appId: z.string().regex(/^geox\.[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$/),
  version: z.string(),
  dimension: DimensionEnum,
  domain: AppDomainEnum,
  title: z.string(),
  description: z.string(),
  uiEntry: z.object({
    resourceUri: z.string(),
    mode: z.enum(['inline', 'external', 'inline-or-external']),
    visibility: z.enum(['model', 'app', 'both']),
  }),
  toolsRequired: z.array(z.string()),
  eventsPublished: z.array(z.string()),
  eventsSubscribed: z.array(z.string()),
  metadata: z.record(z.string(), z.any()).optional(),
});

// ═══════════════════════════════════════════════════════════════════════════════
// TypeScript Types (Derived)
// ═══════════════════════════════════════════════════════════════════════════════

export type GeoContext = z.infer<typeof GeoContextSchema>;
export type EvidenceRef = z.infer<typeof EvidenceRefSchema>;
export type EvidenceObject = z.infer<typeof EvidenceObjectSchema>;
export type Verdict = z.infer<typeof VerdictSchema>;
export type AuditEvent = z.infer<typeof AuditEventSchema>;
export type XYPoint = z.infer<typeof XYPointSchema>;
export type XYZPoint = z.infer<typeof XYZPointSchema>;
export type BoundingBox = z.infer<typeof BoundingBoxSchema>;
export type AppManifest = z.infer<typeof AppManifestSchema>;
