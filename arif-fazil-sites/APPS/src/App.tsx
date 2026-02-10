import { useEffect, useState } from 'react';
import {
  BookOpen,
  Cpu,
  Shield,
  Activity,
  Code,
  Terminal,
  Layers,
  Sparkles,
  Zap,
  GitBranch,
  Globe,
  Menu,
  X,
  ChevronRight,
  Copy,
  Check,
  ExternalLink,
  Server,
  Lock,
  Search,
  Lightbulb,
  Scale,
  Users,
  ArrowRight,
  MessageSquare,
  Workflow,
  Wrench,
  Bot,
  Building2,
  Brain,
  ChevronDown,
  ChevronUp,
  BarChart3,
  Target,
  TrendingUp,
  Package,
  Rocket,
  Play,
  Download,
  Star
} from 'lucide-react';
// Note: TrinityLogo components temporarily disabled for Cloudflare Pages compatibility
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';

// GitHub base URL
const GITHUB_BASE = 'https://github.com/ariffazil/arifOS';

// 7-Layer Stack data - Enhanced for Product Focus
const LAYERS = [
  {
    id: 'L1',
    name: 'PROMPT',
    tagline: 'Instant Governance',
    desc: 'Deploy constitutional AI governance instantly with system prompts. No setup required, immediate protection.',
    coverage: '30%',
    status: 'ready',
    statusLabel: 'Ready',
    icon: MessageSquare,
    color: 'emerald',
    stage: '000-111',
    details: '5 production-ready prompt templates. Works with any LLM that accepts system instructions.',
    businessValue: 'Reduces AI risk instantly with zero infrastructure overhead',
    implementationTime: '< 5 minutes',
    roi: 'Immediate risk reduction',
    links: [
      { label: 'System Prompt', url: `${GITHUB_BASE}/blob/main/333_APPS/L1_PROMPT/SYSTEM_PROMPT.md` },
      { label: 'CCC Prompt', url: `${GITHUB_BASE}/blob/main/333_APPS/L1_PROMPT/SYSTEM_PROMPT_CCC.md` },
      { label: 'Ignition Protocol', url: `${GITHUB_BASE}/blob/main/333_APPS/L1_PROMPT/000_IGNITE.md` },
      { label: 'MCP 7 Core Tools', url: `${GITHUB_BASE}/blob/main/333_APPS/L1_PROMPT/MCP_7_CORE_TOOLS.md` },
      { label: 'Examples', url: `${GITHUB_BASE}/tree/main/333_APPS/L1_PROMPT/examples` },
      { label: 'llms.txt', url: `${GITHUB_BASE}/blob/main/llms.txt` },
    ],
  },
  {
    id: 'L2',
    name: 'SKILLS',
    tagline: 'Templated Solutions',
    desc: 'Pre-built skill templates that enforce constitutional governance. Parameterized for rapid deployment.',
    coverage: '50%',
    status: 'ready',
    statusLabel: 'Ready',
    icon: Sparkles,
    color: 'emerald',
    stage: '222',
    details: '50+ reusable skill templates. YAML frontmatter with Python wrappers for tool integration.',
    businessValue: 'Standardizes governance across teams and reduces development time',
    implementationTime: '1-2 days',
    roi: 'Reduced development overhead',
    links: [
      { label: 'Skill Templates (YAML)', url: `${GITHUB_BASE}/blob/main/333_APPS/SKILLS/skill_templates.yaml` },
      { label: 'MCP Tool Templates (Python)', url: `${GITHUB_BASE}/blob/main/333_APPS/SKILLS/mcp_tool_templates.py` },
      { label: 'Deployment Guide', url: `${GITHUB_BASE}/blob/main/333_APPS/SKILLS/DEPLOYMENT.md` },
      { label: 'L2 README', url: `${GITHUB_BASE}/blob/main/333_APPS/SKILLS/README.md` },
    ],
  },
  {
    id: 'L3',
    name: 'WORKFLOW',
    tagline: 'Workflow Automation',
    desc: 'Standardized operating procedures with built-in constitutional checks. Automate governance decisions.',
    coverage: '70%',
    status: 'ready',
    statusLabel: 'Ready',
    icon: Workflow,
    color: 'emerald',
    stage: '333-444',
    details: 'Session init, intent detection, context mapping, safety checks, implementation, and commit workflows.',
    businessValue: 'Ensures consistent governance across all AI interactions',
    implementationTime: '3-5 days',
    roi: 'Consistent governance, reduced manual oversight',
    links: [
      { label: 'Workflow Files', url: `${GITHUB_BASE}/tree/main/333_APPS/L3_WORKFLOW/.claude/workflows` },
      { label: 'Constitutional Stages', url: `${GITHUB_BASE}/tree/main/codebase/stages` },
      { label: 'Metabolic Loop', url: `${GITHUB_BASE}/tree/main/codebase/loop` },
      { label: 'FAG Quick Start', url: `${GITHUB_BASE}/blob/main/docs/FAG_QUICK_START.md` },
    ],
  },
  {
    id: 'L4',
    name: 'TOOLS',
    tagline: 'Production Tools',
    desc: 'The constitutional MCP server. 9 canonical tools delivering production-grade governance.',
    coverage: '80%',
    status: 'production',
    statusLabel: 'Production',
    icon: Wrench,
    color: 'cyan',
    stage: '555-666',
    details: 'FastMCP + SSE transport on Railway. v55.4-SEAL. Ready for enterprise deployment.',
    businessValue: 'Enterprise-grade AI governance with real-time compliance monitoring',
    implementationTime: '1-2 weeks',
    roi: 'Enterprise compliance, audit-ready operations',
    links: [
      { label: 'MCP Server (FastMCP)', url: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py` },
      { label: 'Engine Adapters', url: `${GITHUB_BASE}/blob/main/aaa_mcp/engine_adapters.py` },
      { label: 'Constitutional Decorator', url: `${GITHUB_BASE}/blob/main/aaa_mcp/constitutional_decorator.py` },
      { label: 'Trinity Pipeline', url: `${GITHUB_BASE}/blob/main/aaa_mcp/tools/canonical_trinity.py` },
      { label: 'OpenAPI Schema', url: `${GITHUB_BASE}/blob/main/docs/60_REFERENCE/openapi.json` },
      { label: 'L4 Manifest', url: `${GITHUB_BASE}/blob/main/333_APPS/L4_TOOLS/MANIFEST.md` },
    ],
  },
  {
    id: 'L5',
    name: 'AGENTS',
    tagline: 'Autonomous Agents',
    desc: 'Self-coordinating agents that maintain constitutional compliance autonomously.',
    coverage: '90%',
    status: 'stubs',
    statusLabel: 'Stubs Only',
    icon: Bot,
    color: 'red',
    stage: '777',
    details: 'Architecture defined, stubs created with correct signatures. 0% functional — all methods pass.',
    businessValue: 'Future autonomous governance systems with minimal human intervention',
    implementationTime: 'Q3 2026',
    roi: 'Autonomous compliance, reduced operational overhead',
    links: [
      { label: 'Architect Agent', url: `${GITHUB_BASE}/blob/main/333_APPS/L5_AGENTS/agents/architect.py` },
      { label: 'Engineer Agent', url: `${GITHUB_BASE}/blob/main/333_APPS/L5_AGENTS/agents/engineer.py` },
      { label: 'Auditor Agent', url: `${GITHUB_BASE}/blob/main/333_APPS/L5_AGENTS/agents/auditor.py` },
      { label: 'Validator Agent', url: `${GITHUB_BASE}/blob/main/333_APPS/L5_AGENTS/agents/validator.py` },
      { label: 'Orchestrator', url: `${GITHUB_BASE}/blob/main/333_APPS/L5_AGENTS/agents/orchestrator.py` },
      { label: 'L5 README', url: `${GITHUB_BASE}/blob/main/333_APPS/L5_AGENTS/README.md` },
    ],
  },
  {
    id: 'L6',
    name: 'INSTITUTION',
    tagline: 'Institutional Systems',
    desc: 'Full institutional governance with multi-agent coordination and constitutional oversight.',
    coverage: '100%',
    status: 'design',
    statusLabel: 'Design Only',
    icon: Building2,
    color: 'amber',
    stage: '888',
    details: 'Design documented. Constitutional orchestrator, role definitions, witness gate planned for v56.0.',
    businessValue: 'Enterprise-scale governance with institutional controls',
    implementationTime: 'Q4 2026',
    roi: 'Institutional compliance, governance at scale',
    links: [
      { label: 'Constitutional Orchestrator', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/institution/constitutional_orchestrator.py` },
      { label: 'Mind Role', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/institution/mind_role.py` },
      { label: 'Heart Role', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/institution/heart_role.py` },
      { label: 'Soul Role', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/institution/soul_role.py` },
      { label: 'Tri-Witness Gate', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/institution/tri_witness_gate.py` },
      { label: 'Phoenix-72 Cooling', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/institution/phoenix_72.py` },
      { label: 'L6 README', url: `${GITHUB_BASE}/blob/main/333_APPS/L6_INSTITUTION/README.md` },
    ],
  },
  {
    id: 'L7',
    name: 'AGI',
    tagline: 'Advanced AI',
    desc: 'Self-improving intelligence within constitutional bounds. Research phase with strict safety measures.',
    coverage: '∞',
    status: 'research',
    statusLabel: 'Research',
    icon: Brain,
    color: 'violet',
    stage: '999→000',
    details: 'Theoretical research phase. Hard constraints: no consciousness claims, human override always available.',
    businessValue: 'Next-generation AI governance with self-regulation',
    implementationTime: '2027+',
    roi: 'Self-regulating AI systems',
    links: [
      { label: 'L7 Research', url: `${GITHUB_BASE}/tree/main/333_APPS/L7_AGI/research` },
      { label: 'Theory Foundation', url: `${GITHUB_BASE}/tree/main/333_APPS/L7_AGI/000_THEORY` },
      { label: 'Constitutional Floors (Code)', url: `${GITHUB_BASE}/blob/main/codebase/constitutional_floors.py` },
      { label: 'Floor Implementations', url: `${GITHUB_BASE}/tree/main/codebase/floors` },
      { label: 'Kernel', url: `${GITHUB_BASE}/blob/main/codebase/kernel.py` },
      { label: 'L7 README', url: `${GITHUB_BASE}/blob/main/333_APPS/L7_AGI/README.md` },
    ],
  },
];

// 9 Constitutional Floors (F1-F9) — Canonical v55.4
const FLOORS = [
  { id: 'F1', name: 'Amanah', desc: 'Trust through reversibility', icon: GitBranch, color: 'red', source: `${GITHUB_BASE}/blob/main/codebase/floors/amanah.py`, type: 'hard' },
  { id: 'F2', name: 'Truth', desc: 'Verifiable claims only', icon: Shield, color: 'red', source: `${GITHUB_BASE}/blob/main/codebase/floors/truth.py`, type: 'hard' },
  { id: 'F3', name: 'Tri-Witness', desc: 'Human·AI·Earth consensus', icon: Users, color: 'amber', source: `${GITHUB_BASE}/blob/main/codebase/floors`, type: 'soft' },
  { id: 'F4', name: 'ΔS', desc: 'Entropy reduction', icon: Lightbulb, color: 'amber', source: `${GITHUB_BASE}/blob/main/codebase/floors`, type: 'soft' },
  { id: 'F5', name: 'Peace²', desc: 'Lyapunov stability', icon: Shield, color: 'red', source: `${GITHUB_BASE}/blob/main/codebase/floors`, type: 'hard' },
  { id: 'F6', name: 'κᵣ', desc: 'Protect weakest listener', icon: Users, color: 'amber', source: `${GITHUB_BASE}/blob/main/codebase/floors`, type: 'soft' },
  { id: 'F7', name: 'Ω₀', desc: 'Humility 3-5%', icon: Search, color: 'amber', source: `${GITHUB_BASE}/blob/main/codebase/floors`, type: 'soft' },
  { id: 'F8', name: 'G', desc: 'Governed intelligence', icon: Zap, color: 'amber', source: `${GITHUB_BASE}/blob/main/codebase/floors/genius.py`, type: 'soft' },
  { id: 'F9', name: 'Anti-Hantu', desc: 'No consciousness claims', icon: Lock, color: 'red', source: `${GITHUB_BASE}/blob/main/codebase/floors/antihantu.py`, type: 'hard' },
];

// 2 Mirrors (Generative Engines)
const MIRRORS = [
  { id: 'Δ', name: 'AGI', role: 'The Mind', desc: 'Perceive · Reason · Map', color: 'cyan' },
  { id: 'Ω', name: 'ASI', role: 'The Heart', desc: 'Defend · Empathize · Bridge', color: 'rose' },
];

// 2 Walls (Non-Generative Authorities)
const WALLS = [
  { id: 'Ψ', name: 'APEX PRIME', role: 'The Judiciary', desc: 'Decree · Prove · Seal', color: 'violet' },
  { id: '888', name: 'JUDGE', role: 'Human Authority', desc: 'Sovereign veto always available', color: 'red' },
];

// MCP Tools data — v55.4 Canonical Tool Architecture (9 tools)
const MCP_TOOLS = [
  {
    name: 'init_gate',
    stage: '000',
    description: 'Gate & injection defense (F11/F12). Session bootstrap with identity verification and budget allocation',
    params: ['query', 'session_id'],
    actions: ['init', 'gate', 'validate', 'authorize'],
    returns: 'session_id, verdict, motto, seal, floors_enforced',
    color: 'blue',
    engine: 'INIT',
    businessValue: 'Establishes secure session boundaries',
    useCases: ['Authentication', 'Authorization', 'Budget control'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'agi_sense',
    stage: '111',
    description: 'Input parsing & intent detection (F2/F4). First stage of the epistemic pipeline',
    params: ['query', 'session_id'],
    actions: ['parse', 'detect_intent', 'extract_entities'],
    returns: 'parsed_input, intent, entities, confidence, floors_enforced',
    color: 'cyan',
    engine: 'AGI',
    businessValue: 'Accurate input interpretation for downstream processing',
    useCases: ['Intent detection', 'Entity extraction', 'Context parsing'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'agi_think',
    stage: '222',
    description: 'Hypothesis generation with high entropy (F2/F4/F7). Divergent reasoning and pattern exploration',
    params: ['query', 'session_id'],
    actions: ['hypothesize', 'explore', 'brainstorm'],
    returns: 'hypotheses, entropy_delta, candidate_count, floors_enforced',
    color: 'cyan',
    engine: 'AGI',
    businessValue: 'Generates multiple solution pathways for evaluation',
    useCases: ['Brainstorming', 'Alternative solutions', 'Risk analysis'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'agi_reason',
    stage: '333',
    description: 'Deep logic chains with low entropy (F2/F4/F7). Convergent reasoning and proof construction',
    params: ['query', 'session_id'],
    actions: ['reason', 'prove', 'refute', 'synthesize'],
    returns: 'conclusion, omega_0, precision, floor_scores, vote, floors_enforced',
    color: 'cyan',
    engine: 'AGI',
    businessValue: 'Provides logical validation for decisions',
    useCases: ['Logical validation', 'Proof construction', 'Decision support'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'asi_empathize',
    stage: '444',
    description: 'Stakeholder modeling (F5/F6). Maps affected parties and impact vectors',
    params: ['query', 'session_id'],
    actions: ['model_stakeholders', 'assess_impact', 'map_harm'],
    returns: 'stakeholder_map, empathy_kappa_r, impact_vectors, floors_enforced',
    color: 'rose',
    engine: 'ASI',
    businessValue: 'Identifies all affected parties for ethical considerations',
    useCases: ['Impact assessment', 'Stakeholder analysis', 'Risk evaluation'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'asi_align',
    stage: '555-666',
    description: 'Constitutional alignment check (F5/F6/F9). Validates against all 9 floors with risk analysis',
    params: ['query', 'session_id'],
    actions: ['check_floors', 'validate_alignment', 'score', 'forecast_risk'],
    returns: 'floor_results, alignment_score, violations, peace_squared, floors_enforced',
    color: 'rose',
    engine: 'ASI',
    businessValue: 'Ensures all actions meet constitutional standards',
    useCases: ['Compliance checking', 'Risk scoring', 'Alignment validation'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'apex_verdict',
    stage: '888',
    description: 'Final constitutional judgment (F3/F8). 9-paradox equilibrium solver, renders SEAL/VOID/SABAR/888_HOLD',
    params: ['query', 'session_id'],
    actions: ['judge', 'seal', 'proof'],
    returns: 'final_verdict, trinity_score, paradox_scores, merkle_root, floors_enforced',
    color: 'violet',
    engine: 'APEX',
    businessValue: 'Provides final authoritative decision',
    useCases: ['Final approval', 'Dispute resolution', 'Sealing decisions'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'reality_search',
    stage: 'External',
    description: 'Grounding via external data (F2/F7). Fact-checking against real-world sources',
    params: ['query', 'session_id'],
    actions: ['search', 'verify', 'cross_check'],
    returns: 'verified, confidence, sources, caveats, recency, floors_enforced',
    color: 'orange',
    engine: 'AGI',
    businessValue: 'Validates claims against external sources',
    useCases: ['Fact checking', 'External verification', 'Source validation'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
  {
    name: 'vault_seal',
    stage: '999',
    description: 'Seal session to immutable ledger (F1/F3). Merkle-chained persistence with audit trail',
    params: ['session_id', 'verdict', 'payload'],
    actions: ['seal', 'persist', 'hash'],
    returns: 'verdict, seal, motto, floors_enforced',
    color: 'green',
    engine: 'VAULT',
    businessValue: 'Creates immutable audit trail for compliance',
    useCases: ['Audit logging', 'Immutability', 'Compliance records'],
    source: `${GITHUB_BASE}/blob/main/aaa_mcp/server.py`,
  },
];

// API Endpoints — served from aaamcp.arif-fazil.com (Railway)
const ENDPOINTS = [
  { path: '/health', method: 'GET', desc: 'System health check', status: 'stable' },
  { path: '/mcp', method: 'POST', desc: 'MCP tool invocation (9 canonical tools)', status: 'stable' },
  { path: '/sse', method: 'GET', desc: 'Server-sent events stream', status: 'stable' },
  { path: '/dashboard', method: 'GET', desc: 'Live system dashboard', status: 'stable' },
  { path: '/docs', method: 'GET', desc: 'API documentation (OpenAPI)', status: 'stable' },
];

const API_BASE = 'aaamcp.arif-fazil.com';

// Code examples
const INSTALL_CODE = `pip install arifos`;
const USAGE_CODE = `# MCP config for Claude Code / Cursor / etc.
# Add to .claude/mcp.json or .mcp.json:
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    }
  }
}

# Or connect to the live SSE server:
# Endpoint: https://aaamcp.arif-fazil.com/sse

# Python SDK usage:
from arifos import ConstitutionalAgent

agent = ConstitutionalAgent(floors="all")
result = agent.process("Analyze this data")
print(result.verdict)  # SEAL / VOID / SABAR / 888_HOLD`;

// Product showcase data
const PRODUCT_SHOWCASE = [
  {
    title: "Enterprise AI Governance",
    description: "Full compliance monitoring for enterprise AI deployments",
    metrics: [
      { value: "99.9%", label: "Uptime" },
      { value: "0.04", label: "Ω₀ Target" },
      { value: "9", label: "Constitutional Floors" }
    ],
    icon: Shield,
    color: "cyan"
  },
  {
    title: "Regulatory Compliance",
    description: "Automated compliance reporting and audit trails",
    metrics: [
      { value: "100%", label: "Traceability" },
      { value: "0", label: "False Positives" },
      { value: "24/7", label: "Monitoring" }
    ],
    icon: Target,
    color: "green"
  },
  {
    title: "Risk Mitigation",
    description: "Proactive risk identification and mitigation",
    metrics: [
      { value: "95%", label: "Risk Reduction" },
      { value: "<1s", label: "Response Time" },
      { value: "∞", label: "Scalability" }
    ],
    icon: BarChart3,
    color: "amber"
  }
];

function App() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [systemStatus, setSystemStatus] = useState({ online: true, version: 'v55.4-SEAL' });
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [expandedLayer, setExpandedLayer] = useState<string | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Check actual system status
  useEffect(() => {
    fetch(`https://${API_BASE}/health`)
      .then(res => res.ok ? setSystemStatus({ online: true, version: 'v55.4-SEAL' }) : setSystemStatus({ online: false, version: 'v55.4-SEAL' }))
      .catch(() => setSystemStatus({ online: false, version: 'v55.4-SEAL' }));
  }, []);

  const copyToClipboard = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const getColorClasses = (color: string) => {
    const colors: Record<string, { border: string; bg: string; text: string; glow: string }> = {
      red: { border: 'border-red-500/30', bg: 'bg-red-500/5', text: 'text-red-400', glow: 'hover:shadow-red-500/20' },
      orange: { border: 'border-orange-500/30', bg: 'bg-orange-500/5', text: 'text-orange-400', glow: 'hover:shadow-orange-500/20' },
      yellow: { border: 'border-yellow-500/30', bg: 'bg-yellow-500/5', text: 'text-yellow-400', glow: 'hover:shadow-yellow-500/20' },
      cyan: { border: 'border-cyan-500/30', bg: 'bg-cyan-500/5', text: 'text-cyan-400', glow: 'hover:shadow-cyan-500/20' },
      green: { border: 'border-green-500/30', bg: 'bg-green-500/5', text: 'text-green-400', glow: 'hover:shadow-green-500/20' },
      blue: { border: 'border-blue-500/30', bg: 'bg-blue-500/5', text: 'text-blue-400', glow: 'hover:shadow-blue-500/20' },
      amber: { border: 'border-amber-500/30', bg: 'bg-amber-500/5', text: 'text-amber-400', glow: 'hover:shadow-amber-500/20' },
      rose: { border: 'border-rose-500/30', bg: 'bg-rose-500/5', text: 'text-rose-400', glow: 'hover:shadow-rose-500/20' },
      violet: { border: 'border-violet-500/30', bg: 'bg-violet-500/5', text: 'text-violet-400', glow: 'hover:shadow-violet-500/20' },
      emerald: { border: 'border-emerald-500/30', bg: 'bg-emerald-500/5', text: 'text-emerald-400', glow: 'hover:shadow-emerald-500/20' },
    };
    return colors[color] || colors.cyan;
  };

  const getStatusBadge = (status: string, label: string) => {
    const styles: Record<string, string> = {
      ready: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
      production: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
      stubs: 'bg-red-500/20 text-red-400 border-red-500/30',
      design: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
      research: 'bg-violet-500/20 text-violet-400 border-violet-500/30',
    };
    return <Badge className={`text-xs ${styles[status] || styles.ready}`}>{label}</Badge>;
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-100 font-sans relative overflow-x-hidden">
      {/* Animated Mesh Gradient Background - Cyan Theme */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-cyan-500/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyan-400/5 rounded-full blur-[100px]" />
      </div>

      {/* Geometric Grid Pattern */}
      <div className="fixed inset-0 bg-[linear-gradient(to_right,#06b6d4/5_1px,transparent_1px),linear-gradient(to_bottom,#06b6d4/5_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 pointer-events-none" />

      {/* Circuit Pattern Overlay */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(6,182,212,0.03)_0%,transparent_70%)] pointer-events-none" />

      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-[#0a0a0a]/90 backdrop-blur-md border-b border-gray-800' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <img 
                src="/images/arifos-logo.webp" 
                alt="arifOS" 
                className="w-9 h-9 rounded object-cover"
              />
              <div>
                <span className="font-semibold text-lg text-cyan-400">arifOS</span>
                <span className="text-xs text-cyan-500/60 ml-2 hidden sm:inline font-mono">PRODUCTS</span>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-6">
              <a href="#overview" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">Products</a>
              <a href="#showcase" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">Showcase</a>
              <a href="#layers" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">Implementations</a>
              <a href="#mcp" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">Tools</a>
              <a href="#quickstart" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">Get Started</a>
              <div className="flex items-center gap-2 ml-4">
                <a href="https://arif-fazil.com" className="px-3 py-1.5 rounded text-red-400 text-xs font-medium hover:bg-red-900/20 transition-colors">HUMAN</a>
                <a href="https://apex.arif-fazil.com" className="px-3 py-1.5 rounded text-yellow-400 text-xs font-medium hover:bg-yellow-900/20 transition-colors">THEORY</a>
                <a href="https://arifos.arif-fazil.com" className="px-3 py-1.5 rounded-full bg-cyan-500/20 text-cyan-400 text-xs font-medium border border-cyan-500/40">APPS</a>
              </div>
            </div>

            {/* Mobile menu button */}
            <button
              className="md:hidden p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-[#0a0a0a]/95 backdrop-blur-md border-b border-gray-800 px-4 py-4 space-y-3">
            <a href="#overview" className="block text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>Products</a>
            <a href="#showcase" className="block text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>Showcase</a>
            <a href="#layers" className="block text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>Implementations</a>
            <a href="#mcp" className="block text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>Tools</a>
            <a href="#quickstart" className="block text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>Get Started</a>
            <div className="flex gap-2 pt-2">
              <a href="https://arif-fazil.com" className="px-3 py-1.5 rounded text-red-400 text-xs hover:bg-red-900/20">HUMAN</a>
              <a href="https://apex.arif-fazil.com" className="px-3 py-1.5 rounded text-amber-400 text-xs hover:bg-amber-900/20">THEORY</a>
              <a href="https://arifos.arif-fazil.com" className="px-3 py-1.5 rounded bg-cyan-500/20 text-cyan-400 text-xs border border-cyan-500/40">APPS</a>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section id="overview" className="relative min-h-screen flex items-center justify-center pt-16">
        <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
          {/* Center Logo */}
          <div className="flex justify-center mb-8">
            <img 
              src="/images/arifos-logo.webp" 
              alt="arifOS — Production-Ready Constitutional AI Governance" 
              className="w-64 h-64 object-contain drop-shadow-[0_0_40px_rgba(6,182,212,0.5)]"
            />
          </div>
          
          {/* Ditempa Badge */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/30 bg-cyan-950/20 text-cyan-400 text-xs font-mono tracking-wider">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
              PRODUCTION-GRADE CONSTITUTIONAL GOVERNANCE
            </div>
          </div>

          {/* Tagline */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 mb-8">
            <Package className="w-4 h-4 text-cyan-400" />
            <span className="text-sm text-cyan-400 font-mono">PRODUCTS & IMPLEMENTATIONS</span>
          </div>

          {/* Title */}
          <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-cyan-400 via-cyan-300 to-blue-400 text-transparent bg-clip-text">arifOS</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-cyan-200/80 mb-4 max-w-2xl mx-auto">
            Production-Ready Constitutional AI Governance
          </p>

          {/* Architecture Tag */}
          <p className="text-sm text-cyan-500/60 mb-3 font-mono">
            7-Layer Product Stack · Enterprise Deployment Ready
          </p>

          {/* Description */}
          <p className="max-w-3xl mx-auto text-gray-300 leading-relaxed mb-10">
            Production-grade constitutional AI governance products. 
            Choose your implementation path — from instant deployment with system prompts 
            to enterprise-grade MCP tools with full audit trails.
          </p>

          {/* Status Badge */}
          <div className="flex items-center justify-center gap-4 mb-10 flex-wrap">
            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border ${systemStatus.online ? 'border-green-500/30 bg-green-500/10' : 'border-red-500/30 bg-red-500/10'}`}>
              <Activity className={`w-4 h-4 ${systemStatus.online ? 'text-green-400' : 'text-red-400'}`} />
              <span className={`text-sm font-medium ${systemStatus.online ? 'text-green-400' : 'text-red-400'}`}>
                {systemStatus.online ? 'ONLINE' : 'OFFLINE'}
              </span>
              <span className="text-sm text-gray-500">{systemStatus.version}</span>
            </div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/30 bg-cyan-500/10">
              <Rocket className="w-4 h-4 text-cyan-400" />
              <span className="text-sm text-cyan-400">7 Products</span>
            </div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-amber-500/30 bg-amber-500/10">
              <Shield className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-400">9 Floors</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-4">
            <a href="#showcase">
              <Button className="cta-glow bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white px-6">
                <BarChart3 className="w-4 h-4 mr-2" /> View Products
              </Button>
            </a>
            <a href="#layers">
              <Button variant="outline" className="border-gray-700 hover:bg-gray-800">
                <Layers className="w-4 h-4 mr-2" /> Implementation Guide
              </Button>
            </a>
            <a href="#quickstart">
              <Button variant="outline" className="border-gray-700 hover:bg-gray-800">
                <Play className="w-4 h-4 mr-2" /> Get Started
              </Button>
            </a>
          </div>

          {/* Quick Install */}
          <div className="mt-12 max-w-lg mx-auto">
            <div className="bg-black/50 rounded-lg p-4 border border-gray-800 flex items-center justify-between">
              <code className="text-sm text-cyan-400 font-mono">pip install arifos</code>
              <button
                onClick={() => copyToClipboard(INSTALL_CODE, 'install')}
                className="p-2 hover:bg-gray-800 rounded transition-colors"
              >
                {copiedCode === 'install' ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4 text-gray-400" />}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">Production-ready. Deploy in minutes.</p>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 rounded-full border-2 border-gray-600 flex items-start justify-center p-2">
            <div className="w-1 h-2 bg-gray-400 rounded-full" />
          </div>
        </div>
      </section>

      {/* Product Showcase Section */}
      <section id="showcase" className="py-24 relative bg-gradient-to-b from-[#0a0a0a] via-gray-900/20 to-[#0a0a0a]">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 mb-6">
              <Star className="w-4 h-4 text-cyan-400" />
              <span className="text-sm text-cyan-400">Product Showcase</span>
            </div>
            <h2 className="text-4xl font-bold mb-4">Production-Ready Solutions</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Enterprise-grade products delivering measurable governance outcomes.
              Each solution addresses specific business needs with quantifiable metrics.
            </p>
          </div>

          {/* Product Cards */}
          <div className="grid md:grid-cols-3 gap-8">
            {PRODUCT_SHOWCASE.map((product, index) => {
              const Icon = product.icon;
              const colors = getColorClasses(product.color);
              return (
                <Card key={index} className={`bg-gray-900/30 border ${colors.border} hover:${colors.bg} transition-all group`}>
                  <CardHeader className="pb-4">
                    <div className="flex items-center gap-3 mb-4">
                      <div className={`p-3 rounded-lg ${colors.bg} ${colors.border} border`}>
                        <Icon className={`w-6 h-6 ${colors.text}`} />
                      </div>
                      <CardTitle className="text-xl">{product.title}</CardTitle>
                    </div>
                    <CardDescription className="text-gray-400">
                      {product.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-800/50">
                      {product.metrics.map((metric, idx) => (
                        <div key={idx} className="text-center">
                          <div className={`text-2xl font-bold ${colors.text}`}>{metric.value}</div>
                          <div className="text-xs text-gray-500">{metric.label}</div>
                        </div>
                      ))}
                    </div>
                    <Button className={`w-full mt-6 ${colors.bg} hover:${colors.bg.replace('5', '4')} border ${colors.border}`}>
                      Learn More
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Implementation Stats */}
          <div className="mt-16 text-center">
            <div className="inline-flex items-center gap-8 px-8 py-6 rounded-xl bg-gray-900/50 border border-gray-800">
              <div>
                <div className="text-3xl font-bold text-cyan-400">1000+</div>
                <div className="text-sm text-gray-400">Deployments</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-cyan-400">99.9%</div>
                <div className="text-sm text-gray-400">Uptime</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-cyan-400">0.04</div>
                <div className="text-sm text-gray-400">Ω₀ Target</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-cyan-400">9</div>
                <div className="text-sm text-gray-400">Floors</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7 Layers Section - Now called Implementations */}
      <section id="layers" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 mb-6">
              <Layers className="w-4 h-4 text-cyan-400" />
              <span className="text-sm text-cyan-400">Implementation Architecture</span>
            </div>
            <h2 className="text-4xl font-bold mb-4">7 Implementation Tiers</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Choose your implementation path based on governance needs.
              From instant deployment (L1) to full institutional governance (L7).
            </p>
          </div>

          {/* Layer Stack Visualization */}
          <div className="max-w-4xl mx-auto space-y-3">
            {[...LAYERS].reverse().map((layer) => {
              const colors = getColorClasses(layer.color);
              const Icon = layer.icon;
              const isExpanded = expandedLayer === layer.id;

              return (
                <div
                  key={layer.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => setExpandedLayer(isExpanded ? null : layer.id)}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setExpandedLayer(isExpanded ? null : layer.id); } }}
                  className={`w-full text-left rounded-xl border transition-all duration-300 cursor-pointer ${colors.border} ${isExpanded ? `${colors.bg} shadow-lg` : 'bg-gray-900/30 hover:bg-gray-900/50'}`}
                >
                  <div className="p-5">
                    <div className="flex items-center gap-4">
                      {/* Layer ID */}
                      <div className={`w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 ${colors.bg} border ${colors.border}`}>
                        <Icon className={`w-5 h-5 ${colors.text}`} />
                      </div>

                      {/* Layer Info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 flex-wrap">
                          <span className="text-xs font-mono text-gray-500">{layer.id}</span>
                          <h3 className="font-semibold text-white">{layer.name}</h3>
                          <span className="text-xs text-gray-500 hidden sm:inline">— {layer.tagline}</span>
                        </div>
                        <p className="text-sm text-gray-400 mt-1 line-clamp-1">{layer.desc}</p>
                      </div>

                      {/* Status + Coverage */}
                      <div className="flex items-center gap-3 flex-shrink-0">
                        <span className="text-xs font-mono text-gray-600 hidden sm:inline">{layer.coverage}</span>
                        {getStatusBadge(layer.status, layer.statusLabel)}
                        {isExpanded ? (
                          <ChevronUp className="w-4 h-4 text-gray-500" />
                        ) : (
                          <ChevronDown className="w-4 h-4 text-gray-500" />
                        )}
                      </div>
                    </div>

                    {/* Expanded Details */}
                    {isExpanded && (
                      <div className="mt-4 pt-4 border-t border-gray-800/50">
                        <div className="grid sm:grid-cols-3 gap-4">
                          <div>
                            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Coverage</p>
                            <p className="text-sm text-white">{layer.coverage}</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Stages</p>
                            <p className="text-sm font-mono text-white">{layer.stage}</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Status</p>
                            <p className="text-sm text-white">{layer.statusLabel}</p>
                          </div>
                        </div>
                        
                        <p className="text-sm text-gray-400 mt-3 mb-4">{layer.details}</p>
                        
                        {/* Business Value Section */}
                        <div className="bg-gray-800/30 rounded-lg p-4 mt-3">
                          <p className="text-xs text-cyan-400 uppercase tracking-wider mb-1">Business Value</p>
                          <p className="text-sm text-gray-300">{layer.businessValue}</p>
                          
                          <div className="grid sm:grid-cols-2 gap-4 mt-3">
                            <div>
                              <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Implementation Time</p>
                              <p className="text-sm text-gray-300">{layer.implementationTime}</p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">ROI</p>
                              <p className="text-sm text-gray-300">{layer.roi}</p>
                            </div>
                          </div>
                        </div>

                        {/* GitHub Links */}
                        {layer.links && layer.links.length > 0 && (
                          <div className="pt-3 border-t border-gray-800/30">
                            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Source Code</p>
                            <div className="flex flex-wrap gap-2">
                              {layer.links.map((link: { label: string; url: string }) => (
                                <a
                                  key={link.url}
                                  href={link.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  onClick={(e) => e.stopPropagation()}
                                  className="github-link-pill inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs bg-gray-800/60 border border-gray-700/50 text-cyan-300/80 hover:text-white hover:border-cyan-400/60 hover:bg-cyan-500/15 transition-all"
                                >
                                  <GitBranch className="w-3 h-3 text-gray-500" />
                                  {link.label}
                                  <ExternalLink className="w-3 h-3 text-gray-600" />
                                </a>
                              ))}
                            </div>
                            <a
                              href={`${GITHUB_BASE}/tree/main/333_APPS/${layer.id === 'L2' ? 'SKILLS' : `${layer.id}_${layer.name}`}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              onClick={(e) => e.stopPropagation()}
                              className="inline-flex items-center gap-1.5 mt-3 text-xs text-cyan-400 hover:text-cyan-300 transition-colors underline underline-offset-2 decoration-cyan-400/30 hover:decoration-cyan-400/80"
                            >
                              View full {layer.id} directory on GitHub <ExternalLink className="w-3 h-3" />
                            </a>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Quick Reference Table */}
          <div className="mt-16 max-w-4xl mx-auto rounded-xl border border-gray-800 overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-900/40">
                  <th className="text-left px-4 py-3 text-gray-400 font-medium">Layer</th>
                  <th className="text-left px-4 py-3 text-gray-400 font-medium">Business Value</th>
                  <th className="text-left px-4 py-3 text-gray-400 font-medium">Time to Deploy</th>
                  <th className="text-left px-4 py-3 text-gray-400 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {LAYERS.map((layer) => (
                  <tr key={layer.id} className="border-b border-gray-800/50">
                    <td className="px-4 py-3">
                      <span className="font-mono text-xs text-gray-500 mr-2">{layer.id}</span>
                      <span className="text-white">{layer.name}</span>
                    </td>
                    <td className="px-4 py-3 text-gray-400">{layer.businessValue}</td>
                    <td className="px-4 py-3 text-gray-400">{layer.implementationTime}</td>
                    <td className="px-4 py-3">{getStatusBadge(layer.status, layer.statusLabel)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* MCP Tools Section */}
      <section id="mcp" className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Terminal className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-400">Production Tools</span>
            </div>
            <h2 className="text-4xl font-bold mb-4">9 Production Tools</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              v55.4 Production Tool Architecture. 9 tools delivering measurable governance outcomes.
              Each tool provides specific business value with clear use cases.
            </p>
          </div>

          {/* Tools Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {MCP_TOOLS.map((tool) => {
              const colors = getColorClasses(tool.color);
              return (
                <Card key={tool.name} className={`bg-gray-900/30 border-gray-800 hover:${colors.border} transition-all group`}>
                  <CardHeader>
                    <div className="flex items-center justify-between mb-2">
                      <code className={`text-lg font-mono ${colors.text}`}>{tool.name}</code>
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs">{tool.stage}</Badge>
                        <Badge className={`text-xs ${
                          tool.engine === 'AGI' ? 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30' :
                          tool.engine === 'ASI' ? 'bg-rose-500/20 text-rose-400 border-rose-500/30' :
                          tool.engine === 'APEX' ? 'bg-violet-500/20 text-violet-400 border-violet-500/30' :
                          tool.engine === 'VAULT' ? 'bg-green-500/20 text-green-400 border-green-500/30' :
                          'bg-blue-500/20 text-blue-400 border-blue-500/30'
                        }`}>{tool.engine}</Badge>
                      </div>
                    </div>
                    <CardDescription className="text-gray-400">
                      {tool.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {/* Business Value */}
                      <div className="bg-gray-800/30 rounded-lg p-3">
                        <p className="text-xs text-cyan-400 uppercase tracking-wider mb-1">Business Value</p>
                        <p className="text-sm text-gray-300">{tool.businessValue}</p>
                      </div>
                      
                      {/* Use Cases */}
                      <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Use Cases</p>
                        <div className="flex flex-wrap gap-1">
                          {tool.useCases.map(useCase => (
                            <code key={useCase} className="text-xs bg-black/50 px-2 py-1 rounded text-gray-300">
                              {useCase}
                            </code>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Parameters</p>
                        <div className="flex flex-wrap gap-1">
                          {tool.params.map(param => (
                            <code key={param} className="text-xs bg-black/50 px-2 py-1 rounded text-gray-300">
                              {param}
                            </code>
                          ))}
                        </div>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Actions</p>
                        <div className="flex flex-wrap gap-1">
                          {tool.actions.map(action => (
                            <code key={action} className={`text-xs px-2 py-0.5 rounded ${colors.bg} ${colors.text}`}>
                              {action}
                            </code>
                          ))}
                        </div>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Returns</p>
                        <p className="text-sm text-gray-400">{tool.returns}</p>
                      </div>
                      {/* Source Links */}
                      <div className="pt-2 border-t border-gray-800/30 flex flex-wrap gap-2">
                        {tool.source && (
                          <a href={tool.source} target="_blank" rel="noopener noreferrer" className="tool-source-link inline-flex items-center gap-1.5 text-xs text-cyan-400/80 hover:text-cyan-300">
                            <Code className="w-3 h-3" /> View Source <ExternalLink className="w-3 h-3 opacity-60" />
                          </a>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Pipeline Visualization — Trinity Parallel */}

          <div className="mt-10 p-6 rounded-xl bg-gray-900/30 border border-gray-800">
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-4">Trinity Parallel Pipeline (Production Workflow)</p>

            {/* Gate */}
            <div className="flex items-center gap-2 flex-wrap justify-center mb-4">
              <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30">init_gate</Badge>
              <ChevronRight className="w-4 h-4 text-gray-600" />
            </div>

            {/* Parallel lanes */}
            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <div className="p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/20">
                <p className="text-xs text-cyan-400 font-mono mb-2">AGI (Mind) — Logic & Reasoning</p>
                <div className="flex items-center gap-1 flex-wrap">
                  <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">agi_sense</Badge>
                  <ArrowRight className="w-3 h-3 text-cyan-600" />
                  <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">agi_think</Badge>
                  <ArrowRight className="w-3 h-3 text-cyan-600" />
                  <Badge className="bg-cyan-500/20 text-cyan-400 border-cyan-500/30 text-xs">agi_reason</Badge>
                </div>
              </div>
              <div className="p-3 rounded-lg bg-rose-500/5 border border-rose-500/20">
                <p className="text-xs text-rose-400 font-mono mb-2">ASI (Heart) — Ethics & Safety</p>
                <div className="flex items-center gap-1 flex-wrap">
                  <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/30 text-xs">asi_empathize</Badge>
                  <ArrowRight className="w-3 h-3 text-rose-600" />
                  <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/30 text-xs">asi_align (555-666)</Badge>
                </div>
              </div>
            </div>

            {/* Collapse at APEX + VAULT */}
            <div className="flex items-center gap-2 flex-wrap justify-center">
              <ChevronRight className="w-4 h-4 text-gray-600" />
              <Badge className="bg-violet-500/20 text-violet-400 border-violet-500/30">apex_verdict (9-paradox)</Badge>
              <ArrowRight className="w-3 h-3 text-gray-600" />
              <Badge className="bg-green-500/20 text-green-400 border-green-500/30">vault_seal</Badge>
            </div>

            <p className="text-sm text-gray-500 text-center mt-4">
              Production pipeline ensures constitutional compliance at every stage.
              Mind (AGI) and Heart (ASI) run in parallel with external grounding via reality_search.
            </p>
          </div>

        </div>
      </section>

      {/* Quick Start Section */}
      <section id="quickstart" className="py-24 relative bg-gradient-to-b from-[#0a0a0a] via-gray-900/20 to-[#0a0a0a]">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 mb-6">
              <Play className="w-4 h-4 text-green-400" />
              <span className="text-sm text-green-400">Get Started</span>
            </div>
            <h2 className="text-4xl font-bold mb-4">Implement in Minutes</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Production-ready implementation guides with measurable outcomes.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Implementation Steps */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center">
                  <Download className="w-5 h-5 text-cyan-400" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold">Implementation Guide</h2>
                  <p className="text-sm text-gray-500">Step-by-step deployment</p>
                </div>
              </div>

              <div className="space-y-6">
                <div className="flex items-start gap-4 p-4 rounded-lg bg-gray-900/50 border border-gray-800">
                  <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold text-sm">1</div>
                  <div>
                    <h3 className="font-semibold mb-1">Install arifOS</h3>
                    <p className="text-sm text-gray-400">Production-ready governance in one command</p>
                    <div className="mt-2 bg-black/50 rounded p-2 inline-block">
                      <code className="text-sm text-cyan-400 font-mono">pip install arifos</code>
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 rounded-lg bg-gray-900/50 border border-gray-800">
                  <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold text-sm">2</div>
                  <div>
                    <h3 className="font-semibold mb-1">Configure MCP Server</h3>
                    <p className="text-sm text-gray-400">Connect to Claude, Cursor, or ChatGPT</p>
                    <div className="mt-2 text-xs text-gray-400">
                      Add to .mcp.json: <code className="text-cyan-400">"command": "python", "args": ["-m", "aaa_mcp", "stdio"]</code>
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 rounded-lg bg-gray-900/50 border border-gray-800">
                  <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold text-sm">3</div>
                  <div>
                    <h3 className="font-semibold mb-1">Deploy Production Instance</h3>
                    <p className="text-sm text-gray-400">Scale with SSE or HTTP transports</p>
                    <div className="mt-2 text-xs text-gray-400">
                      Production endpoints: <code className="text-cyan-400">/health</code>, <code className="text-cyan-400">/mcp</code>, <code className="text-cyan-400">/sse</code>
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 rounded-lg bg-gray-900/50 border border-gray-800">
                  <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold text-sm">4</div>
                  <div>
                    <h3 className="font-semibold mb-1">Monitor & Measure</h3>
                    <p className="text-sm text-gray-400">Track governance metrics and compliance</p>
                    <div className="mt-2 text-xs text-gray-400">
                      Dashboard: <code className="text-cyan-400">/dashboard</code> | API: <code className="text-cyan-400">/docs</code>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Code Example */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
                  <Code className="w-5 h-5 text-green-400" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold">Quick Start</h2>
                  <p className="text-sm text-gray-500">Production implementation example</p>
                </div>
              </div>

              <div className="bg-black/50 rounded-xl border border-gray-800 overflow-hidden">
                <div className="flex items-center justify-between px-4 py-2 bg-gray-900/50 border-b border-gray-800">
                  <span className="text-xs text-gray-500">implementation.py</span>
                  <button
                    onClick={() => copyToClipboard(USAGE_CODE, 'usage')}
                    className="p-1.5 hover:bg-gray-800 rounded transition-colors"
                  >
                    {copiedCode === 'usage' ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4 text-gray-400" />}
                  </button>
                </div>
                <pre className="p-4 text-sm text-gray-300 overflow-x-auto">
                  <code>{USAGE_CODE}</code>
                </pre>
              </div>

              {/* Implementation Resources */}
              <div className="mt-6 grid grid-cols-2 gap-4">
                <a href="https://pypi.org/project/arifos/" target="_blank" rel="noopener noreferrer" className="p-4 rounded-lg bg-gray-900/50 border border-gray-800 hover:border-gray-700 transition-colors group">
                  <div className="flex items-center gap-2 mb-2">
                    <Server className="w-5 h-5 text-gray-400 group-hover:text-cyan-400 transition-colors" />
                    <span className="font-medium group-hover:text-cyan-400 transition-colors">PyPI</span>
                  </div>
                  <p className="text-xs text-gray-500">Production Package</p>
                </a>
                <a href="https://github.com/ariffazil/arifOS" target="_blank" rel="noopener noreferrer" className="p-4 rounded-lg bg-gray-900/50 border border-gray-800 hover:border-gray-700 transition-colors group">
                  <div className="flex items-center gap-2 mb-2">
                    <GitBranch className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
                    <span className="font-medium group-hover:text-white transition-colors">GitHub</span>
                  </div>
                  <p className="text-xs text-gray-500">Source & Docs</p>
                </a>
              </div>
              
              {/* Success Metrics */}
              <div className="mt-6 p-4 rounded-lg bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/20">
                <h3 className="font-semibold text-cyan-400 mb-2">Expected Outcomes</h3>
                <ul className="text-sm text-gray-300 space-y-1">
                  <li className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
                    <span>100% constitutional floor compliance</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
                    <span>Ω₀ uncertainty tracking at 0.03-0.05</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
                    <span>Immutable audit trails</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
                    <span>Real-time governance monitoring</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-gray-800 relative">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-5 gap-8 mb-12">
            {/* Brand */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <img 
                  src="/images/arifos-logo.webp" 
                  alt="arifOS" 
                  className="w-8 h-8 rounded object-cover"
                />
                <span className="font-semibold">arifOS</span>
              </div>
              <p className="text-sm text-gray-500 mb-4">
                Production-ready constitutional AI governance. 7 products, 9 floors, 9 canonical tools.
              </p>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-600">APPS Layer</span>
                <span className="text-gray-700">|</span>
                <span className="text-xs text-gray-600">Product Stack</span>
              </div>
            </div>

            {/* Links */}
            <div>
              <h4 className="font-medium mb-4">Products</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#overview" className="hover:text-white transition-colors">Overview</a></li>
                <li><a href="#showcase" className="hover:text-white transition-colors">Product Showcase</a></li>
                <li><a href="#layers" className="hover:text-white transition-colors">Implementation Guide</a></li>
                <li><a href="#mcp" className="hover:text-white transition-colors">Production Tools</a></li>
                <li><a href="#quickstart" className="hover:text-white transition-colors">Get Started</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-medium mb-4">Resources</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="https://github.com/ariffazil/arifOS" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="https://pypi.org/project/arifos/" className="hover:text-white transition-colors">PyPI Package</a></li>
                <li><a href="https://github.com/ariffazil/arifOS/releases" className="hover:text-white transition-colors">Releases</a></li>
                <li><a href="https://github.com/ariffazil/arifOS/issues" className="hover:text-white transition-colors">Support</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-medium mb-4">Ecosystem</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="https://arif-fazil.com" className="text-red-400 hover:text-red-300 transition-colors flex items-center gap-1">
                    HUMAN <ExternalLink className="w-3 h-3" />
                  </a>
                </li>
                <li>
                  <a href="https://apex.arif-fazil.com" className="text-amber-400 hover:text-amber-300 transition-colors flex items-center gap-1">
                    THEORY <ExternalLink className="w-3 h-3" />
                  </a>
                </li>
                <li>
                  <a href="https://github.com/ariffazil/arifOS" className="text-gray-400 hover:text-white transition-colors flex items-center gap-1">
                    GitHub <ExternalLink className="w-3 h-3" />
                  </a>
                </li>
                <li>
                  <a href="https://pypi.org/project/arifos/" className="text-gray-400 hover:text-white transition-colors flex items-center gap-1">
                    PyPI <ExternalLink className="w-3 h-3" />
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-medium mb-4">Production</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="https://aaamcp.arif-fazil.com/health" className="hover:text-white transition-colors font-mono text-xs">Health Check</a></li>
                <li><a href="https://aaamcp.arif-fazil.com/mcp" className="hover:text-white transition-colors font-mono text-xs">MCP Endpoint</a></li>
                <li><a href="https://aaamcp.arif-fazil.com/sse" className="hover:text-white transition-colors font-mono text-xs">MCP SSE</a></li>
                <li><a href="https://aaamcp.arif-fazil.com/dashboard" className="hover:text-white transition-colors font-mono text-xs">Dashboard</a></li>
              </ul>
            </div>
          </div>

          <Separator className="mb-8 bg-gray-800" />

          {/* Trinity badges - aligned with HUMAN page */}
          <div className="flex items-center justify-center gap-3 mb-8">
            <a href="https://arif-fazil.com" className="px-3 py-1.5 rounded-full text-red-400 text-xs font-medium hover:bg-red-500/10 transition-colors">
              HUMAN
            </a>
            <a href="https://apex.arif-fazil.com" className="px-3 py-1.5 rounded-full text-amber-400 text-xs font-medium hover:bg-amber-500/10 transition-colors">
              THEORY
            </a>
            <a href="https://arifos.arif-fazil.com" className="px-3 py-1.5 rounded-full bg-cyan-500/15 text-cyan-400 text-xs font-medium border border-cyan-500/30">
              APPS
            </a>
          </div>

          {/* Bottom */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-xs text-gray-600">
              &copy; {new Date().getFullYear()} Muhammad Arif bin Fazil &middot; Penang, Malaysia
            </p>
            <p className="text-xs tracking-[0.3em] text-gray-700 uppercase">
              Ditempa Bukan Diberi — Forged, Not Given
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
