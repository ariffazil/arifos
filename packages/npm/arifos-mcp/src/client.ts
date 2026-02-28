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

// Type for text content items
type TextContent = { type: string; text: string };

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
  
  /** Current session ID (from last anchor_session) */
  readonly sessionId: string | null;
  
  /** Initialize connection */
  connect(): Promise<void>;
  
  /** Close connection */
  disconnect(): Promise<void>;
  
  /** Call any arifOS tool with type-safe parameters */
  callTool(
    name: ArifOSToolName, 
    params: Record<string, unknown>
  ): Promise<{ content: Array<{ type: string; text: string }>; metadata?: ArifOSMetadata; response?: unknown }>;
  
  /** Convenience: Start a new session */
  anchorSession(query: string, actor_id?: string): Promise<{ session_id: string; metadata: ArifOSMetadata; raw: unknown }>;
  
  /** Convenience: Execute reasoning */
  reasonMind(query: string): Promise<VerdictEnvelope>;
  
  /** Convenience: Get final judgment */
  apexJudge(query: string): Promise<VerdictEnvelope>;
  
  /** List available tools */
  listTools(): Promise<Array<{ name: string; description?: string; inputSchema?: unknown }>>;
}

// Helper to safely extract text from MCP content
function extractTextContent(content: unknown): TextContent[] {
  if (!Array.isArray(content)) return [];
  return content.filter((c): c is TextContent => 
    typeof c === 'object' && c !== null && 
    'type' in c && typeof c.type === 'string' &&
    'text' in c && typeof c.text === 'string'
  );
}

// Helper to parse arifOS response
type ArifOSResponse = {
  verdict: string;
  stage?: string;
  session_id?: string;
  data?: {
    session_id?: string;
    stage?: string;
    verdict?: string;
    floors?: unknown[];
    truth?: unknown;
    next_actions?: string[];
    governance_token?: string;
    [key: string]: unknown;
  };
  floors?: unknown[];
  truth?: unknown;
  next_actions?: string[];
  governance_token?: string;
  [key: string]: unknown;
};

function parseArifOSResponse(text: string): { parsed: ArifOSResponse; textContent: string } {
  const trimmed = text.trim();
  
  // Check if response starts with validation error
  if (trimmed.startsWith('1 validation error') || trimmed.startsWith('2 validation error')) {
    throw new Error(`MCP validation error: ${trimmed.substring(0, 200)}`);
  }
  
  const parsed = JSON.parse(trimmed) as ArifOSResponse;
  return { parsed, textContent: trimmed };
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
 * const { session_id } = await client.anchorSession('test session');
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
  let currentSessionId: string | null = null;
  
  const client: ArifOSMCPClient = {
    mcp,
    get metadata() { return currentMetadata; },
    get sessionId() { return currentSessionId; },
    
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
    
    async callTool(
      name: ArifOSToolName,
      params: Record<string, unknown>
    ): Promise<{ content: TextContent[]; metadata?: ArifOSMetadata; response?: unknown }> {
      try {
        const result = await mcp.callTool(
          { name, arguments: params },
          undefined,
          { timeout: config.timeout ?? 60000 }
        );
        
        const contentItems = extractTextContent(result.content);
        
        // Join all text content for parsing
        const fullText = contentItems.map(c => c.text).join('');
        
        // Try to parse as arifOS response
        let response: ArifOSResponse | undefined;
        try {
          const { parsed } = parseArifOSResponse(fullText);
          response = parsed;
          
          // Extract metadata if this looks like a verdict envelope
          const sessionId = parsed.data?.session_id || parsed.session_id;
          const stage = parsed.data?.stage || parsed.stage;
          const verdict = parsed.data?.verdict || parsed.verdict;
          
          if (sessionId && stage && verdict) {
            currentSessionId = sessionId;
            currentMetadata = {
              session_id: sessionId,
              version: parsed.kernel_version as string || 'unknown',
              stage: stage as Stage,
              verdict: verdict as ArifOSMetadata['verdict'],
              floors_evaluated: (parsed.data?.floors || parsed.floors || []) as ArifOSMetadata['floors_evaluated'],
              timestamp: new Date().toISOString(),
              governance_token: parsed.data?.governance_token || parsed.governance_token,
            };
          }
        } catch {
          // Not a parseable arifOS response—ignore
        }
        
        return { content: contentItems, metadata: currentMetadata ?? undefined, response };
      } catch (cause) {
        if (cause instanceof ArifOSError) throw cause;
        throw new ArifOSError(
          `Tool call failed: ${name}`,
          'INVALID_RESPONSE',
          currentMetadata?.stage,
          undefined,
          cause
        );
      }
    },
    
    async anchorSession(query: string, actor_id?: string): Promise<{ session_id: string; metadata: ArifOSMetadata; raw: unknown }> {
      const params: Record<string, unknown> = { query };
      if (actor_id) params.actor_id = actor_id;
      
      const result = await client.callTool('anchor_session', params);
      
      if (!result.response) {
        throw new ArifOSError('anchor_session returned no parseable response', 'INVALID_RESPONSE');
      }
      
      const parsed = result.response as ArifOSResponse;
      const sessionId = parsed.data?.session_id;
      
      if (!sessionId) {
        throw new ArifOSError('anchor_session returned no session_id', 'INVALID_RESPONSE');
      }
      
      const metadata: ArifOSMetadata = {
        session_id: sessionId,
        version: parsed.kernel_version as string || 'unknown',
        stage: (parsed.data?.stage || '000_INIT') as Stage,
        verdict: (parsed.data?.verdict || parsed.verdict || 'SEAL') as ArifOSMetadata['verdict'],
        floors_evaluated: (parsed.data?.floors || []) as ArifOSMetadata['floors_evaluated'],
        timestamp: new Date().toISOString(),
        governance_token: parsed.data?.governance_token,
      };
      
      return { session_id: sessionId, metadata, raw: parsed };
    },
    
    async reasonMind(query: string): Promise<VerdictEnvelope> {
      if (!currentSessionId) {
        throw new ArifOSError('No active session. Call anchorSession() first.', 'INVALID_RESPONSE');
      }
      
      const result = await client.callTool('reason_mind', { 
        query, 
        session_id: currentSessionId 
      });
      
      if (!result.response) {
        throw new ArifOSError('reason_mind returned no parseable response', 'INVALID_RESPONSE', '333_MIND');
      }
      
      const parsed = result.response as ArifOSResponse;
      
      // Map arifOS response to VerdictEnvelope
      return {
        verdict: (parsed.data?.verdict || parsed.verdict) as VerdictEnvelope['verdict'],
        stage: (parsed.data?.stage || parsed.stage || '333_MIND') as Stage,
        session_id: currentSessionId,
        floors: (parsed.data?.floors || parsed.floors || []) as unknown as VerdictEnvelope['floors'],
        truth: (parsed.data?.truth || parsed.truth) as VerdictEnvelope['truth'],
        next_actions: (parsed.data?.next_actions || parsed.next_actions) as string[],
        governance_token: (parsed.data?.governance_token || parsed.governance_token) as string,
      };
    },
    
    async apexJudge(query: string): Promise<VerdictEnvelope> {
      if (!currentSessionId) {
        throw new ArifOSError('No active session. Call anchorSession() first.', 'INVALID_RESPONSE');
      }
      
      const result = await client.callTool('apex_judge', { 
        query,
        session_id: currentSessionId
      });
      
      if (!result.response) {
        throw new ArifOSError('apex_judge returned no parseable response', 'INVALID_RESPONSE', '888_APEX');
      }
      
      const parsed = result.response as ArifOSResponse;
      
      return {
        verdict: (parsed.data?.verdict || parsed.verdict) as VerdictEnvelope['verdict'],
        stage: (parsed.data?.stage || parsed.stage || '888_APEX') as Stage,
        session_id: currentSessionId,
        floors: (parsed.data?.floors || parsed.floors || []) as unknown as VerdictEnvelope['floors'],
        truth: (parsed.data?.truth || parsed.truth) as VerdictEnvelope['truth'],
        next_actions: (parsed.data?.next_actions || parsed.next_actions) as string[],
        governance_token: (parsed.data?.governance_token || parsed.governance_token) as string,
      };
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
