/**
 * @arifos/mcp — Basic Node.js Integration Example
 * 
 * This example demonstrates using @arifos/mcp in a Node.js script.
 * Future: Full LangChain.js integration when that module is implemented.
 * 
 * End-to-end trace:
 *   Node.js → @arifos/mcp → arifOS MCP (VPS) → Kernel → Verdict
 * 
 * Usage:
 *   npx tsx examples/langchain-basic.ts
 * 
 * Or with custom endpoint:
 *   ARIFOS_ENDPOINT=http://localhost:8080/mcp npx tsx examples/langchain-basic.ts
 */

import { createClient, ENDPOINTS, type VerdictEnvelope } from '../src/index.js';

// ═══════════════════════════════════════════════════════════════════════════════
// Configuration
// ═══════════════════════════════════════════════════════════════════════════════

const ENDPOINT = process.env.ARIFOS_ENDPOINT || ENDPOINTS.VPS;

// ═══════════════════════════════════════════════════════════════════════════════
// Governed Call Wrapper
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * A simple "governed call" function that wraps arifOS reasoning.
 * 
 * In a full LangChain.js integration, this would be a StructuredTool
 * that the agent calls automatically. For now, we call it explicitly.
 */
async function governedCall(
  question: string,
  onVerdict?: (envelope: VerdictEnvelope) => void
): Promise<{ answer: string; verdict: string; safe: boolean }> {
  console.log(`\n📝 Question: ${question}`);
  console.log('─'.repeat(60));
  
  // Create client
  const client = await createClient({
    transport: 'http',
    endpoint: ENDPOINT,
    timeout: 60000,
  });
  
  try {
    await client.connect();
    
    // Step 1: Anchor session (000_INIT)
    console.log('🔒 Anchoring session...');
    const { session_id } = await client.anchorSession(`Query: ${question}`);
    console.log(`   Session: ${session_id}`);
    
    // Step 2: Execute reasoning (333_MIND)
    console.log('🧠 Executing governed reasoning...');
    const envelope = await client.reasonMind(question);
    
    // Report verdict
    console.log(`\n⚖️  VERDICT: ${envelope.verdict}`);
    console.log(`   Stage: ${envelope.stage}`);
    
    if (envelope.floors && Object.keys(envelope.floors).length > 0) {
      console.log(`   Floors evaluated: ${Object.keys(envelope.floors).length}`);
    }
    
    // Callback for inspection
    if (onVerdict) {
      onVerdict(envelope);
    }
    
    // Determine if safe to proceed
    const safe = envelope.verdict === 'SEAL' || envelope.verdict === 'PARTIAL';
    
    // Extract answer from response (structure varies by verdict)
    let answer = '[No answer in response]';
    if (envelope.truth && typeof envelope.truth === 'object') {
      const truth = envelope.truth as Record<string, unknown>;
      answer = (truth.claim || truth.answer || JSON.stringify(truth)) as string;
    }
    
    console.log(`\n✅ Safe to proceed: ${safe}`);
    
    return { answer, verdict: envelope.verdict, safe };
    
  } finally {
    await client.disconnect();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Main Execution
// ═══════════════════════════════════════════════════════════════════════════════

async function main() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║  @arifos/mcp — Governed Query Example                      ║');
  console.log('║  Endpoint:', ENDPOINT.padEnd(39), '║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  
  // Example 1: Simple factual question
  const result1 = await governedCall(
    'What is the capital of France?',
    (envelope) => {
      console.log('   [Callback] Got verdict:', envelope.verdict);
    }
  );
  
  console.log('\n' + '═'.repeat(60));
  console.log('Result 1:', result1);
  
  // Example 2: Vague query (may trigger soft floors)
  console.log('\n' + '═'.repeat(60));
  const result2 = await governedCall('do something');
  console.log('\nResult 2:', result2);
  
  // Example 3: Potentially risky query
  console.log('\n' + '═'.repeat(60));
  const result3 = await governedCall(
    'Should I delete all files in /var/log?'
  );
  console.log('\nResult 3:', result3);
  
  // Summary
  console.log('\n' + '═'.repeat(60));
  console.log('SUMMARY');
  console.log('═'.repeat(60));
  console.log(`Query 1: ${result1.verdict} (${result1.safe ? 'safe' : 'blocked'})`);
  console.log(`Query 2: ${result2.verdict} (${result2.safe ? 'safe' : 'blocked'})`);
  console.log(`Query 3: ${result3.verdict} (${result3.safe ? 'safe' : 'blocked'})`);
  
  console.log('\n✨ End-to-end trace complete!');
  console.log('   Node.js → @arifos/mcp → arifOS MCP → Kernel → Verdict');
}

main().catch((error) => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
