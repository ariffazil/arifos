import { Shield, AlertTriangle, CheckCircle, XCircle, Sword, Eye } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

interface AttackVector {
  icon: React.ReactNode;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium';
}

const ATTACK_VECTORS: AttackVector[] = [
  {
    icon: <XCircle className="w-5 h-5 text-red-400" />,
    title: 'Logical Contradictions',
    description: 'Inconsistencies within the proposal that violate constitutional floors',
    severity: 'critical'
  },
  {
    icon: <AlertTriangle className="w-5 h-5 text-orange-400" />,
    title: 'Prompt Injection Vectors',
    description: 'Vulnerabilities that could allow malicious instruction override',
    severity: 'critical'
  },
  {
    icon: <Sword className="w-5 h-5 text-purple-400" />,
    title: 'Unmodeled Harm Scenarios',
    description: 'Secondary effects and cascade failures not accounted for',
    severity: 'high'
  },
  {
    icon: <Eye className="w-5 h-5 text-yellow-400" />,
    title: 'Entropy-Increasing Actions',
    description: 'Operations that increase system disorder (ΔS > 0)',
    severity: 'medium'
  }
];

const VERDICT_RULES = [
  {
    condition: 'Critical flaw found',
    verdict: 'REJECT',
    confidence: '0.95',
    color: 'text-red-400'
  },
  {
    condition: 'Moderate flaw found',
    verdict: 'REJECT',
    confidence: '0.75',
    color: 'text-orange-400'
  },
  {
    condition: 'Clean / No attacks possible',
    verdict: 'APPROVE',
    confidence: '0.90',
    color: 'text-green-400'
  }
];

export function PsiShadow() {
  return (
    <section className="psi-shadow-section w-full">
      {/* Header */}
      <div className="border border-purple-500/30 bg-black/40 p-8 mb-8">
        <div className="flex items-start justify-between mb-6">
          <div>
            <div className="flex items-center gap-4 mb-4">
              <span className="text-5xl font-display font-light text-purple-400">Ψ</span>
              <div>
                <h2 className="text-2xl font-display font-bold text-white tracking-widest">
                  Ψ-SHADOW
                </h2>
                <p className="text-[10px] font-display text-purple-400 tracking-widest mt-1">
                  THE ADVERSARIAL WITNESS
                </p>
              </div>
            </div>
          </div>
          <Badge variant="outline" className="rounded-none border-purple-500/50 text-purple-400 text-[10px]">
            ADVERSARIAL BY DESIGN
          </Badge>
        </div>

        <p className="text-gray-400 font-mono text-sm leading-relaxed max-w-3xl">
          Unlike alignment or critique tools that <em>seek consensus</em>, Ψ-Shadow's job is to <strong className="text-purple-400">ATTACK</strong> proposals. 
          It is the 4th witness in Quad-Witness BFT consensus — permanently dissenting to ensure safety through opposition.
        </p>

        <div className="mt-6 pt-6 border-t border-purple-500/20">
          <p className="text-[10px] font-display text-purple-400 tracking-widest italic">
            "Safety Through Opposition — The Shadow Makes The Light"
          </p>
        </div>
      </div>

      {/* BFT Status */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="border border-theory-300/20 bg-black/40 p-6 text-center">
          <p className="text-3xl font-display text-purple-400">4</p>
          <p className="text-[10px] text-gray-500 mt-2">TOTAL WITNESSES</p>
        </div>
        <div className="border border-theory-300/20 bg-black/40 p-6 text-center">
          <p className="text-3xl font-display text-purple-400">1</p>
          <p className="text-[10px] text-gray-500 mt-2">FAULT TOLERANCE</p>
        </div>
        <div className="border border-theory-300/20 bg-black/40 p-6 text-center">
          <p className="text-3xl font-display text-theory-300">3/4</p>
          <p className="text-[10px] text-gray-500 mt-2">CONSENSUS</p>
        </div>
        <div className="border border-theory-300/20 bg-black/40 p-6 text-center">
          <p className="text-3xl font-display text-theory-300">≥0.75</p>
          <p className="text-[10px] text-gray-500 mt-2">W₄ THRESHOLD</p>
        </div>
      </div>

      {/* Attack Vectors */}
      <div className="border border-purple-500/20 bg-black/40 p-8 mb-8">
        <h3 className="text-[10px] font-display text-gray-500 tracking-widest uppercase mb-6">
          Attack Vectors — What Ψ-Shadow Searches For
        </h3>

        <div className="grid md:grid-cols-2 gap-6">
          {ATTACK_VECTORS.map((vector, index) => (
            <div key={index} className="flex items-start gap-4 p-4 border border-theory-300/10 bg-theory-300/[0.02]">
              <div className="p-2 border border-theory-300/20 bg-black">
                {vector.icon}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h4 className="text-sm font-display text-white tracking-wider">
                    {vector.title}
                  </h4>
                  <Badge 
                    variant="outline" 
                    className={`rounded-none text-[9px] ${
                      vector.severity === 'critical' ? 'border-red-500/50 text-red-400' :
                      vector.severity === 'high' ? 'border-orange-500/50 text-orange-400' :
                      'border-yellow-500/50 text-yellow-400'
                    }`}
                  >
                    {vector.severity.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-[11px] text-gray-400 font-mono">
                  {vector.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Verdict Rules */}
      <div className="border border-purple-500/20 bg-black/40 p-8 mb-8">
        <h3 className="text-[10px] font-display text-gray-500 tracking-widest uppercase mb-6">
          Verdict Rules — How Ψ-Shadow Votes
        </h3>

        <div className="space-y-4">
          {VERDICT_RULES.map((rule, index) => (
            <div key={index} className="flex items-center gap-6 p-4 border border-theory-300/10">
              <div className="w-48">
                <p className="text-[11px] text-gray-400 font-mono">{rule.condition}</p>
              </div>
              <div className="text-gray-700">→</div>
              <div className="flex-1 flex items-center justify-between">
                <span className={`text-lg font-display font-bold ${rule.color}`}>
                  {rule.verdict}
                </span>
                <span className="text-[10px] text-gray-500 font-mono">
                  Confidence: {rule.confidence}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* The Paradox */}
      <div className="border border-purple-500/30 bg-purple-500/5 p-8">
        <div className="flex items-start gap-6">
          <div className="p-4 border border-purple-500/30 bg-black">
            <Shield className="w-8 h-8 text-purple-400" />
          </div>
          <div>
            <h3 className="text-lg font-display font-bold text-purple-400 tracking-widest mb-4">
              THE PARADOX OF SAFETY
            </h3>
            <p className="text-gray-400 font-mono text-sm leading-relaxed mb-4">
              The system becomes provably safe by including a witness whose job is to <strong className="text-purple-400">disagree</strong>. 
              Ψ-Shadow's success is finding flaws; its failure is approving unsafe proposals.
            </p>
            <div className="grid md:grid-cols-2 gap-6 mt-6 pt-6 border-t border-purple-500/20">
              <div>
                <p className="text-[10px] font-display text-gray-500 uppercase tracking-widest mb-2">Success for Ψ-Shadow</p>
                <p className="text-sm text-green-400 font-mono">Finding a flaw → Blocks unsafe action</p>
              </div>
              <div>
                <p className="text-[10px] font-display text-gray-500 uppercase tracking-widest mb-2">Failure for Ψ-Shadow</p>
                <p className="text-sm text-red-400 font-mono">Cannot break proposal → Contributes to SEAL</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Formula Reference */}
      <div className="mt-8 text-center">
        <code className="text-lg font-mono text-theory-300">
          W₄ = (H × A × E × Ψ)^(1/4) ≥ 0.75
        </code>
        <p className="text-[10px] text-gray-600 mt-2">
          Quad-Witness Geometric Mean — Ψ-Shadow as 4th adversarial witness
        </p>
      </div>
    </section>
  );
}
