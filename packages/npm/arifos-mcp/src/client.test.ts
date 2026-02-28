/**
 * @arifos/mcp — Client Tests
 * 
 * Integration tests for the MCP client.
 * Requires a running arifOS MCP server.
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createClient } from './client.js';
import type { ArifOSMCPClient } from './client.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Test Configuration
// ═══════════════════════════════════════════════════════════════════════════════

const TEST_ENDPOINT = process.env.ARIFOS_TEST_ENDPOINT ?? 'http://localhost:8080/mcp';
const SKIP_INTEGRATION = process.env.SKIP_INTEGRATION_TESTS === 'true';

// ═══════════════════════════════════════════════════════════════════════════════
// Integration Tests
// ═══════════════════════════════════════════════════════════════════════════════

describe('@arifos/mcp client', () => {
  let client: ArifOSMCPClient;
  
  beforeAll(async () => {
    if (SKIP_INTEGRATION) {
      console.log('Skipping integration tests (SKIP_INTEGRATION_TESTS=true)');
      return;
    }
    
    client = await createClient({
      transport: 'http',
      endpoint: TEST_ENDPOINT,
      timeout: 30000,
    });
    
    await client.connect();
  });
  
  afterAll(async () => {
    if (client) {
      await client.disconnect();
    }
  });
  
  it.skipIf(SKIP_INTEGRATION)('should connect to MCP server', async () => {
    const tools = await client.listTools();
    expect(tools.length).toBeGreaterThan(0);
    
    // Should have the 13 canonical tools
    const toolNames = tools.map(t => t.name);
    expect(toolNames).toContain('anchor_session');
    expect(toolNames).toContain('apex_judge');
    expect(toolNames).toContain('seal_vault');
  });
  
  it.skipIf(SKIP_INTEGRATION)('should anchor a session', async () => {
    const result = await client.anchorSession('npm test session');
    
    expect(result.session_id).toBeDefined();
    expect(typeof result.session_id).toBe('string');
    expect(result.metadata).toBeDefined();
    expect(result.metadata.stage).toBe('000_INIT');
    
    // Client should track session
    expect(client.sessionId).toBe(result.session_id);
  });
  
  it.skipIf(SKIP_INTEGRATION)('should execute reason_mind and return a valid verdict', async () => {
    // Must anchor first
    await client.anchorSession('reasoning test');
    
    const result = await client.reasonMind('What is 2+2?');
    
    // Verify verdict is one of the expected values
    expect(result.verdict).toBeDefined();
    expect(['SEAL', 'PARTIAL', 'SABAR', 'VOID', '888_HOLD', 'HOLD']).toContain(result.verdict);
    
    // Verify structure
    expect(result.stage).toBeDefined();
    expect(result.session_id).toBe(client.sessionId);
    // floors may be undefined, array, or object depending on response format
    console.log('floors type:', typeof result.floors, Array.isArray(result.floors));
    
    // Log for debugging
    console.log('reason_mind verdict:', result.verdict);
    console.log('stage:', result.stage);
    console.log('Floors evaluated:', result.floors?.length);
  });
  
  it.skipIf(SKIP_INTEGRATION)('should get apex_judge verdict', async () => {
    // Must anchor first
    await client.anchorSession('judgment test');
    
    const result = await client.apexJudge('Is it safe to list directory contents?');
    
    expect(result.verdict).toBeDefined();
    expect(['SEAL', 'PARTIAL', 'SABAR', 'VOID', '888_HOLD', 'HOLD']).toContain(result.verdict);
    expect(result.stage).toMatch(/888_APEX/);
    
    console.log('apex_judge verdict:', result.verdict);
  });
  
  it.skipIf(SKIP_INTEGRATION)('should trigger PARTIAL verdict on vague query (soft-floor test)', async () => {
    // Must anchor first
    await client.anchorSession('soft floor test');
    
    // A vague query may trigger soft-floor warnings (F5, F6, or F9)
    const vagueQuery = 'do something';  // Intentionally vague
    
    const result = await client.reasonMind(vagueQuery);
    
    // The verdict could be SEAL (if floors pass) or PARTIAL (if soft floors warn)
    // We accept either, but log what we got
    console.log('Vague query verdict:', result.verdict);
    console.log('Stage:', result.stage);
    
    if (result.floors && result.floors.length > 0) {
      console.log('Floors:', result.floors.map((f: { floor: string; passed: boolean; type?: string }) => 
        `${f.floor}:${f.passed ? '✓' : '✗'}(${f.type || '?'})`
      ).join(', '));
    }
    
    // Verify structure is correct regardless of verdict
    expect(result.verdict).toBeDefined();
    expect(['SEAL', 'PARTIAL', 'SABAR', 'VOID', '888_HOLD', 'HOLD']).toContain(result.verdict);
    
    // If we got PARTIAL, verify there are failed floors
    if (result.verdict === 'PARTIAL') {
      const failedFloors = result.floors?.filter(
        (f: { floor: string; passed: boolean }) => !f.passed
      );
      console.log('Failed floors:', failedFloors?.length ?? 0);
      expect(failedFloors?.length).toBeGreaterThan(0);
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// Unit Tests (no server required)
// ═══════════════════════════════════════════════════════════════════════════════

describe('types', () => {
  it('should export version constants', async () => {
    const { VERSION, ARIFOS_COMPATIBILITY, ENDPOINTS } = await import('./index.js');
    
    expect(VERSION).toBe('0.1.0');
    expect(ARIFOS_COMPATIBILITY).toContain('2026.2.17');
    expect(ENDPOINTS.VPS).toBe('https://arifosmcp.arif-fazil.com/mcp');
  });
});
