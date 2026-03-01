/**
 * @arifos/mcp — LangChain.js Integration (STUB)
 * 
 * Placeholder for LangChain.js/LangGraph integration.
 * Future: Full tool binding with proper schema conversion.
 * 
 * NOTE: This is a STUB. The full implementation will come in a later phase.
 * For now, use the MCP client directly via `createClient()`.
 * 
 * Canonical Source: https://pypi.org/project/arifos/
 */

import type { ArifOSMCPClient } from './client.js';
import type { ArifOSToolName } from './types.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Stub Implementation
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Placeholder for LangChain.js toolset wrapper.
 * 
 * This class will eventually expose arifOS tools as LangChain `StructuredTool`
 * instances with proper Zod schemas. For now, it just wraps the MCP client.
 * 
 * @example
 * ```typescript
 * import { ArifOSToolset } from '@arifos/mcp/langchain';
 * 
 * const client = await createClient({ transport: 'http', endpoint: '...' });
 * await client.connect();
 * 
 * // Stub: Just proxy to MCP client
 * const toolset = new ArifOSToolset(client);
 * const tools = await toolset.getTools();
 * 
 * // Use with LangChain (when implemented)
 * // const agent = createReactAgent({ llm, tools });
 * ```
 */
export class ArifOSToolset {
  // Client reserved for future implementation
  // @ts-expect-error Unused in stub phase
  constructor(private readonly _client: ArifOSMCPClient) {}
  
  /**
   * Get list of available tool names.
   * 
   * STUB: Currently just returns hardcoded canonical 13 tools.
   * Future: Dynamic tool discovery from MCP server.
   */
  async getToolNames(): Promise<ArifOSToolName[]> {
    return [
      'anchor_session',
      'reason_mind',
      'recall_memory',
      'simulate_heart',
      'critique_thought',
      'apex_judge',
      'eureka_forge',
      'seal_vault',
      'search_reality',
      'fetch_content',
      'inspect_file',
      'audit_rules',
      'check_vital',
    ];
  }
  
  /**
   * Get tools formatted for LangChain.
   * 
   * STUB: Currently returns empty array with warning.
   * Future: Returns array of `StructuredTool` instances.
   */
  async getTools(): Promise<[]> {
    console.warn(
      '[@arifos/mcp/langchain] STUB: getTools() not yet implemented.\n' +
      'Use client.callTool() directly for now.\n' +
      'See: https://github.com/ariffazil/arifOS/issues'
    );
    return [];
  }
  
  /**
   * Get a specific tool by name.
   * 
   * STUB: Returns null with warning.
   * Future: Returns `StructuredTool` instance.
   */
  async getTool(_name: ArifOSToolName): Promise<null> {
    console.warn(
      `[@arifos/mcp/langchain] STUB: getTool() not yet implemented.\n` +
      `Use client.callTool('${_name}', params) directly for now.`
    );
    return null;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Re-exports for convenience
// ═══════════════════════════════════════════════════════════════════════════════

export { createClient, type ArifOSMCPClient } from './client.js';
export * from './types.js';

/**
 * Future exports (when implemented):
 * 
 * export { ArifOSTool } from './langchain/tool.js';
 * export { createArifOSAgent } from './langchain/agent.js';
 * export type { ArifOSAgentConfig } from './langchain/types.js';
 */
