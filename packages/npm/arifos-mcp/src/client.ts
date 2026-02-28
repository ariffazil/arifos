/**
 * @arifos/mcp — MCP Client
 * 
 * Minimal, thin wrapper around @modelcontextprotocol/sdk Client.
 * This is a CABLE, not the KERNEL. All governance happens server-side.
 * 
 * Canonical Source: https://pypi.org/project/arifos/
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import type { Transport } from '@modelcontextprotocol/sdk/shared/transport.js';
import type { 
  ArifOSClientConfig, 
  ArifOSMetadata, 
  VerdictEnvelope,
  ArifOSToolName,
  ArifOSErrorCode,
  Stage 
} from './types.js';
import { ArifOSError } from './types.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Re-exports
// ═══════════════════════════════════════════════════════════════════════════════

export { Client } from '@modelcontextprotocol/sdk/client/index.js';
export type { Transport } from '@modelcontextprotocol/sdk/shared/transport.js';
export * from './types.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Transport Factory
// ═══════════════════════════════════════════════════════════════════════════════

function createTransport(config: ArifOSClientConfig): Transport {
  switch (config.transport) {
    case 'stdio': {
      if (!config.env) {
        throw new ArifOSError(
          'stdio transport requires env configuration',
          'TRANSPORT_ERROR'
        );
      }
      return new StdioClientTransport({
        command: 'python',
        args: ['-m', 'arifos_aaa_mcp', 'stdio'],
        env: config.env as Record<string, string>,
      });
    }
    
    case 'sse':
    case 'http': {
      if (!config.endpoint) {
        throw new ArifOSError(
          `${config.transport} transport requires endpoint`,
          'TRANSPORT_ERROR'
        );
      }
      // StreamableHTTPClientTransport handles both SSE and HTTP modes
      return new StreamableHTTPClientTransport(
        new URL(config.endpoint)
      );
    }
    
    default: {
      const exhaustive: never = config.transport;
      throw new ArifOSError(
        `Unknown transport: ${exhaustive}`,
        'TRANSPORT_ERROR'
      );
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ArifOS MCP Client Interface
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Typed MCP client for arifOS.
 * 
 * All methods return raw MCP responses. No client-side governance—
 * the arifOS server enforces all 13 floors (F1-F13).
 */
export interface ArifOSMCPClient {
  /** Underlying MCP client */
  readonly mcp: Client;
  
  /** Current session metadata (from last response) */
  readonly metadata: ArifOSMetadata | null;
  
  /** Initialize connection */
  connect(): Promise<void>;
  
  /** Close connection */
  disconnect(): Promise<void>;
  
  /** Call any arifOS tool with type-safe parameters */
  callTool<T = unknown>(
    name: ArifOSToolName, 
    params: Record<string, unknown>
  ): Promise<{ content: Array<{ type: string; text: string }>; metadata?: ArifOSMetadata }>;
  
  /** Convenience: Start a new session */
  anchorSession(context?: string): Promise<{ session_id: string; metadata: ArifOSMetadata }>;
  
  /** Convenience: Execute reasoning */
  reasonMind(query: string, context?: string): Promise<VerdictEnvelope>;
  
  /** Convenience: Get final judgment */
  apexJudge(action: string, risk_level?: 'LOW' | 'MODERATE' | 'CRITICAL'): Promise<VerdictEnvelope>;
  
  /** List available tools */
  listTools(): Promise<Array<{ name: string; description?: string; inputSchema?: unknown }>>;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Client Factory
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Create an arifOS MCP client.
 * 
 * @param config - Transport and connection configuration
 * @returns Typed arifOS client
 * 
 * @example
 * ```typescript
 * // stdio mode (local arifOS)
 * const client = await createClient({
 *   transport: 'stdio',
 *   env: {
 *     ARIFOS_GOVERNANCE_SECRET: '...',
 *     DATABASE_URL: '...'
 *   }
 * });
 * 
 * // HTTP mode (remote VPS)
 * const client = await createClient({
 *   transport: 'http',
 *   endpoint: 'https://arifosmcp.arif-fazil.com/mcp'
 * });
 * 
 * // Use it
 * await client.connect();
 * const result = await client.reasonMind('What is the capital of France?');
 * console.log(result.verdict); // 'SEAL' | 'PARTIAL' | 'SABAR' | 'VOID' | '888_HOLD'
 * await client.disconnect();
 * ```
 */
export async function createClient(config: ArifOSClientConfig): Promise<ArifOSMCPClient> {
  const transport = createTransport(config);
  
  const mcp = new Client(
    {
      name: '@arifos/mcp-client',
      version: '0.1.0',
    },
    {
      capabilities: {},
    }
  );
  
  let currentMetadata: ArifOSMetadata | null = null;
  
  const client: ArifOSMCPClient = {
    mcp,
    get metadata() { return currentMetadata; },
    
    async connect(): Promise<void> {
      try {
        await mcp.connect(transport);
      } catch (cause) {
        throw new ArifOSError(
          'Failed to connect to arifOS MCP server',
          'CONNECTION_FAILED',
          undefined,
          undefined,
          cause
        );
      }
    },
    
    async disconnect(): Promise<void> {
      await mcp.close();
    },
    
    async callTool<T>(
      name: ArifOSToolName,
      params: Record<string, unknown>
    ): Promise<{ content: Array<{ type: string; text: string }>; metadata?: ArifOSMetadata }> {
      try {
        const result = await mcp.callTool(
          { name, arguments: params },
          undefined,  // No progress token for now
          { timeout: config.timeout ?? 60000 }
        );
        
        // Extract metadata from response if present
        const textContent = result.content
          .filter(c => c.type === 'text')
          .map(c => c.text)
          .join('');
        
        try {
          const parsed = JSON.parse(textContent);
          if (parsed.session_id && parsed.stage && parsed.verdict) {
            currentMetadata = {
              session_id: parsed.session_id,
              version: parsed.version || 'unknown',
              stage: parsed.stage as Stage,
              verdict: parsed.verdict,
              floors_evaluated: parsed.floors || [],
              timestamp: parsed.timestamp || new Date().toISOString(),
              governance_token: parsed.governance_token,
            };
          }
        } catch {
          // Not JSON or missing fields—ignore
        }
        
        return { content: result.content as Array<{ type: string; text: string }>, metadata: currentMetadata ?? undefined };
      } catch (cause) {
        throw new ArifOSError(
          `Tool call failed: ${name}`,
          'INVALID_RESPONSE',
          currentMetadata?.stage,
          undefined,
          cause
        );
      }
    },
    
    async anchorSession(context?: string): Promise<{ session_id: string; metadata: ArifOSMetadata }> {
      const result = await client.callTool('anchor_session', { context: context ?? '' });
      const text = result.content.find(c => c.type === 'text')?.text ?? '{}';
      
      try {
        const parsed = JSON.parse(text);
        if (!parsed.session_id) {
          throw new ArifOSError('anchor_session returned no session_id', 'INVALID_RESPONSE');
        }
        return { 
          session_id: parsed.session_id,
          metadata: result.metadata ?? {
            session_id: parsed.session_id,
            version: 'unknown',
            stage: '000_INIT',
            verdict: 'SEAL',
            floors_evaluated: ['F11', 'F12', 'F13'],
            timestamp: new Date().toISOString(),
          }
        };
      } catch (cause) {
        if (cause instanceof ArifOSError) throw cause;
        throw new ArifOSError('Failed to parse anchor_session response', 'INVALID_RESPONSE', undefined, undefined, cause);
      }
    },
    
    async reasonMind(query: string, context?: string): Promise<VerdictEnvelope> {
      const result = await client.callTool('reason_mind', { query, context: context ?? '' });
      const text = result.content.find(c => c.type === 'text')?.text ?? '{}';
      
      try {
        return JSON.parse(text) as VerdictEnvelope;
      } catch (cause) {
        throw new ArifOSError('Failed to parse reason_mind response', 'INVALID_RESPONSE', '333_MIND', undefined, cause);
      }
    },
    
    async apexJudge(action: string, risk_level?: 'LOW' | 'MODERATE' | 'CRITICAL'): Promise<VerdictEnvelope> {
      const result = await client.callTool('apex_judge', { 
        action, 
        risk_level: risk_level ?? 'LOW',
        require_human: risk_level === 'CRITICAL'
      });
      const text = result.content.find(c => c.type === 'text')?.text ?? '{}';
      
      try {
        return JSON.parse(text) as VerdictEnvelope;
      } catch (cause) {
        throw new ArifOSError('Failed to parse apex_judge response', 'INVALID_RESPONSE', '888_APEX', undefined, cause);
      }
    },
    
    async listTools(): Promise<Array<{ name: string; description?: string; inputSchema?: unknown }>> {
      try {
        const result = await mcp.listTools();
        return result.tools.map(t => ({
          name: t.name,
          description: t.description,
          inputSchema: t.inputSchema,
        }));
      } catch (cause) {
        throw new ArifOSError('Failed to list tools', 'INVALID_RESPONSE', undefined, undefined, cause);
      }
    },
  };
  
  return client;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Convenience Exports
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Quick-connect helper for common configurations.
 */
export const quickConnect = {
  /** Connect to local stdio arifOS (requires Python env) */
  local(env: Record<string, string>): Promise<ArifOSMCPClient> {
    return createClient({ transport: 'stdio', env });
  },
  
  /** Connect to arifOS VPS endpoint */
  vps(endpoint: string = 'https://arifosmcp.arif-fazil.com/mcp'): Promise<ArifOSMCPClient> {
    return createClient({ transport: 'http', endpoint });
  },
};
