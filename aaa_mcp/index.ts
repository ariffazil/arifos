/**
 * arifOS AAA MCP Server - Cloudflare Workers Implementation
 * 
 * Version: v60.0-FORGE
 * Protocol: MCP 2025-11-25 (Streamable HTTP)
 * Pattern: AAA (Authentication, Authorization, Accounting)
 * 
 * This is a reference implementation showing OAuth 2.1 + MCP integration.
 * The actual Python implementation is in server.py.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { 
  CallToolRequestSchema, 
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema
} from "@modelcontextprotocol/sdk/types.js";
import { jwtVerify, createRemoteJWKSet } from "jose";

// Environment type definitions
export interface Env {
  AAA_SESSION_STORE: KVNamespace;
  AAA_JWT_SECRET: string;
  OAUTH_CLIENT_SECRET: string;
  AAA_ISSUER: string;
  MCP_PROTOCOL_VERSION: string;
  ARIFOS_CONSTITUTIONAL_MODE: string;
  FLOOR_ENFORCEMENT: string;
  BRAVE_API_KEY?: string;
}

// Constitutional verdict types
type Verdict = "SEAL" | "VOID" | "SABAR" | "PARTIAL" | "888_HOLD";

interface Session {
  id: string;
  actorId: string;
  createdAt: number;
  floorScores: Record<string, number>;
  verdict: Verdict;
}

/**
 * AAA MCP Server implementation for Cloudflare Workers
 */
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // CORS preflight
    if (request.method === "OPTIONS") {
      return handleCORS();
    }
    
    // OAuth metadata endpoints
    if (url.pathname === "/.well-known/oauth-authorization-server") {
      return oauthMetadata(env);
    }
    
    if (url.pathname === "/.well-known/oauth-protected-resource") {
      return protectedResourceMetadata(env);
    }
    
    // Health check
    if (url.pathname === "/health") {
      return healthCheck(env);
    }
    
    // Metrics endpoint
    if (url.pathname === "/metrics") {
      return metrics(env);
    }
    
    // MCP endpoint
    if (url.pathname === "/mcp" || url.pathname === "/sse") {
      return handleMCP(request, env, ctx);
    }
    
    // Default: 404
    return new Response(JSON.stringify({ error: "Not found" }), {
      status: 404,
      headers: { "Content-Type": "application/json" }
    });
  }
};

/**
 * Handle CORS preflight requests
 */
function handleCORS(): Response {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, Mcp-Session-Id",
      "Access-Control-Max-Age": "86400"
    }
  });
}

/**
 * OAuth 2.1 Authorization Server Metadata
 * RFC 8414
 */
function oauthMetadata(env: Env): Response {
  const metadata = {
    issuer: env.AAA_ISSUER,
    authorization_endpoint: `${env.AAA_ISSUER}/authorize`,
    token_endpoint: `${env.AAA_ISSUER}/token`,
    registration_endpoint: `${env.AAA_ISSUER}/register`,
    scopes_supported: ["mcp:read", "mcp:execute", "aaa:audit"],
    response_types_supported: ["code"],
    grant_types_supported: ["authorization_code", "refresh_token", "client_credentials"],
    code_challenge_methods_supported: ["S256"],
    token_endpoint_auth_methods_supported: ["client_secret_basic", "client_secret_post", "private_key_jwt"],
    revocation_endpoint: `${env.AAA_ISSUER}/revoke`,
    introspection_endpoint: `${env.AAA_ISSUER}/introspect`
  };
  
  return jsonResponse(metadata);
}

/**
 * OAuth 2.1 Protected Resource Metadata
 */
function protectedResourceMetadata(env: Env): Response {
  const metadata = {
    resource: "https://mcp.arifos.dev",
    authorization_servers: [env.AAA_ISSUER],
    scopes_supported: ["mcp:read", "mcp:execute", "aaa:audit"],
    bearer_methods_supported: ["header"],
    resource_signing_alg_values_supported: ["RS256", "ES256"]
  };
  
  return jsonResponse(metadata);
}

/**
 * Health check endpoint
 */
function healthCheck(env: Env): Response {
  return jsonResponse({
    status: "healthy",
    version: "60.0-FORGE",
    service: "arifOS AAA MCP Server",
    protocol: env.MCP_PROTOCOL_VERSION,
    mode: env.ARIFOS_CONSTITUTIONAL_MODE,
    floors: env.FLOOR_ENFORCEMENT
  });
}

/**
 * Prometheus metrics endpoint
 */
async function metrics(env: Env): Promise<Response> {
  // In production, these would be aggregated from KV or analytics
  const metricsText = `
# HELP arifos_mcp_requests_total Total MCP requests
# TYPE arifos_mcp_requests_total counter
arifos_mcp_requests_total{verdict="SEAL"} 42
arifos_mcp_requests_total{verdict="VOID"} 3
arifos_mcp_requests_total{verdict="SABAR"} 5

# HELP arifos_mcp_active_sessions Active sessions
# TYPE arifos_mcp_active_sessions gauge
arifos_mcp_active_sessions 7

# HELP arifos_mcp_floor_violations_total Constitutional floor violations
# TYPE arifos_mcp_floor_violations_total counter
arifos_mcp_floor_violations_total{floor="F12"} 2
arifos_mcp_floor_violations_total{floor="F2"} 1
`.trim();
  
  return new Response(metricsText, {
    headers: { "Content-Type": "text/plain; version=0.0.4" }
  });
}

/**
 * Main MCP request handler
 */
async function handleMCP(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
  // Authenticate request
  const authResult = await authenticate(request, env);
  if (!authResult.valid) {
    return jsonResponse({ error: "Unauthorized", message: authResult.error }, 401);
  }
  
  // Initialize MCP server
  const server = createMCPServer(env);
  
  // Handle the request
  // Note: In production, this would use the MCP SDK's HTTP transport
  // This is a simplified implementation showing the structure
  const body = await request.json().catch(() => ({}));
  
  const response = await handleMCPRequest(server, body, authResult.session);
  
  return jsonResponse(response);
}

/**
 * Authenticate incoming request
 */
async function authenticate(request: Request, env: Env): Promise<AuthResult> {
  const authHeader = request.headers.get("Authorization");
  
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return { valid: false, error: "Missing or invalid Authorization header" };
  }
  
  const token = authHeader.slice(7);
  
  try {
    // Verify JWT
    const { payload } = await jwtVerify(token, new TextEncoder().encode(env.AAA_JWT_SECRET));
    
    // Extract session
    const sessionId = payload.sid as string;
    const actorId = payload.sub as string;
    
    // Load session from KV
    const sessionData = await env.AAA_SESSION_STORE.get(`session:${sessionId}`);
    const session: Session = sessionData 
      ? JSON.parse(sessionData)
      : {
          id: sessionId,
          actorId: actorId,
          createdAt: Date.now(),
          floorScores: {},
          verdict: "SEAL"
        };
    
    return { valid: true, session };
  } catch (error) {
    return { valid: false, error: "Invalid token" };
  }
}

interface AuthResult {
  valid: boolean;
  error?: string;
  session?: Session;
}

/**
 * Create MCP server instance
 */
function createMCPServer(env: Env): Server {
  const server = new Server(
    {
      name: "arifos-aaa-mcp",
      version: "60.0.0"
    },
    {
      capabilities: {
        tools: { listChanged: true },
        resources: {},
        prompts: {},
        authorization: {
          oauth2: {
            issuer: env.AAA_ISSUER,
            authorizationEndpoint: `${env.AAA_ISSUER}/authorize`,
            tokenEndpoint: `${env.AAA_ISSUER}/token`,
            supportsDynamicClientRegistration: true
          }
        }
      }
    }
  );
  
  // Tool handlers
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: "init_gate",
          description: "Initialize constitutional session (F11/F12 validation)",
          inputSchema: {
            type: "object",
            properties: {
              query: { type: "string" },
              actor_id: { type: "string" },
              auth_token: { type: "string" }
            },
            required: ["query"]
          }
        },
        {
          name: "forge_pipeline",
          description: "Full 000-999 constitutional pipeline",
          inputSchema: {
            type: "object",
            properties: {
              query: { type: "string" },
              actor_id: { type: "string" },
              require_sovereign_for_high_stakes: { type: "boolean" }
            },
            required: ["query"]
          }
        },
        {
          name: "agi_reason",
          description: "Logical reasoning with F2/F4/F7 enforcement",
          inputSchema: {
            type: "object",
            properties: {
              query: { type: "string" },
              context: { type: "string" }
            },
            required: ["query"]
          }
        },
        {
          name: "apex_verdict",
          description: "Final constitutional judgment (F3/F8/F9/F10)",
          inputSchema: {
            type: "object",
            properties: {
              query: { type: "string" },
              agi_output: { type: "object" },
              asi_output: { type: "object" }
            },
            required: ["query"]
          }
        },
        {
          name: "vault_seal",
          description: "Immutable ledger commit (F1/F3)",
          inputSchema: {
            type: "object",
            properties: {
              verdict: { type: "string" },
              session_id: { type: "string" }
            },
            required: ["verdict", "session_id"]
          }
        }
      ]
    };
  });
  
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    
    // Tool dispatch
    switch (name) {
      case "init_gate":
        return handleInitGate(args as any, env);
      case "forge_pipeline":
        return handleForgePipeline(args as any, env);
      case "agi_reason":
        return handleAGIReason(args as any, env);
      case "apex_verdict":
        return handleApexVerdict(args as any, env);
      case "vault_seal":
        return handleVaultSeal(args as any, env);
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  });
  
  return server;
}

/**
 * Handle MCP request
 */
async function handleMCPRequest(
  server: Server, 
  body: any, 
  session?: Session
): Promise<any> {
  const { method, params, id } = body;
  
  // Tool listing
  if (method === "tools/list") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        tools: [
          { name: "init_gate", description: "Initialize constitutional session" },
          { name: "forge_pipeline", description: "Full 000-999 pipeline" },
          { name: "agi_reason", description: "Logical reasoning" },
          { name: "apex_verdict", description: "Constitutional judgment" },
          { name: "vault_seal", description: "Immutable ledger" }
        ]
      }
    };
  }
  
  // Tool call
  if (method === "tools/call") {
    const result = await callTool(params.name, params.arguments, session);
    return {
      jsonrpc: "2.0",
      id,
      result
    };
  }
  
  return { jsonrpc: "2.0", id, error: { code: -32601, message: "Method not found" } };
}

/**
 * Call tool implementation
 */
async function callTool(name: string, args: any, session?: Session): Promise<any> {
  // This would delegate to the actual Python implementation
  // For the reference implementation, we return mock responses
  
  switch (name) {
    case "init_gate":
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            session_id: crypto.randomUUID(),
            verdict: "SEAL",
            floors_passed: ["F11", "F12"]
          })
        }]
      };
      
    case "forge_pipeline":
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            verdict: "SEAL",
            W_3: 0.97,
            floor_scores: { F2: 0.99, F4: 0.95, F7: 0.04 },
            processing_time_ms: 145
          })
        }]
      };
      
    default:
      return {
        content: [{
          type: "text",
          text: JSON.stringify({ error: "Not implemented in reference" })
        }]
      };
  }
}

// Tool handlers
async function handleInitGate(args: any, env: Env): Promise<any> {
  // F11/F12 validation
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        session_id: crypto.randomUUID(),
        verdict: "SEAL",
        floors: { F11: true, F12: true }
      })
    }]
  };
}

async function handleForgePipeline(args: any, env: Env): Promise<any> {
  // Full 000-999 pipeline
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        verdict: "SEAL",
        W_3: 0.97,
        G_factor: 0.85,
        floors: { passed: 13, failed: 0 }
      })
    }]
  };
}

async function handleAGIReason(args: any, env: Env): Promise<any> {
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        verdict: "SEAL",
        reasoning: "Constitutional reasoning applied"
      })
    }]
  };
}

async function handleApexVerdict(args: any, env: Env): Promise<any> {
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        verdict: "SEAL",
        justification: "Tri-witness consensus achieved"
      })
    }]
  };
}

async function handleVaultSeal(args: any, env: Env): Promise<any> {
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        seal: crypto.randomUUID(),
        timestamp: new Date().toISOString()
      })
    }]
  };
}

/**
 * Helper: JSON response
 */
function jsonResponse(data: any, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    }
  });
}

/**
 * Periodic session cleanup (called via cron trigger)
 */
export async function scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
  // Cleanup expired sessions from KV
  const sessionList = await env.AAA_SESSION_STORE.list({ prefix: "session:" });
  const now = Date.now();
  const EXPIRY_MS = 24 * 60 * 60 * 1000; // 24 hours
  
  for (const key of sessionList.keys) {
    const sessionData = await env.AAA_SESSION_STORE.get(key.name);
    if (sessionData) {
      const session: Session = JSON.parse(sessionData);
      if (now - session.createdAt > EXPIRY_MS) {
        await env.AAA_SESSION_STORE.delete(key.name);
      }
    }
  }
}

// Export for testing
export { Server };
