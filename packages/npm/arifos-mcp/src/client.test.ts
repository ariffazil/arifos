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
    const result = await client.anchorSession('Test session');
    
    expect(result.session_id).toBeDefined();
    expect(result.session_id).toMatch(/^ses_/);
    expect(result.metadata).toBeDefined();
    expect(result.metadata.stage).toBe('000_INIT');
  });
  
  it.skipIf(SKIP_INTEGRATION)('should execute reason_mind', async () => {
    const result = await client.reasonMind('What is 2+2?');
    
    expect(result.verdict).toBeDefined();
    expect(['SEAL', 'PARTIAL', 'SABAR', 'VOID', '888_HOLD']).toContain(result.verdict);
    expect(result.stage).toBe('333_MIND');
    expect(result.session_id).toBeDefined();
    expect(Array.isArray(result.floors)).toBe(true);
  });
  
  it.skipIf(SKIP_INTEGRATION)('should get apex_judge verdict', async () => {
    const result = await client.apexJudge('List files in current directory', 'LOW');
    
    expect(result.verdict).toBeDefined();
    expect(result.stage).toBe('888_APEX');
    expect(result.governance_token).toBeDefined();
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
