import { useState, useEffect, useRef } from 'react';
import { Shield, Lock, Eye, Heart, Zap, Gauge, Ghost } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

interface Floor {
  id: string;
  name: string;
  symbol: string;
  arabic?: string;
  type: 'hard' | 'soft';
  constraint: string;
  formula: string;
  basis: string;
  literature: string;
  description: string;
  icon: React.ElementType;
  color: string;
}

// NINE CONSTITUTIONAL FLOORS (F1-F9) — Canonical v2026.03.07-QUADWITNESS
const FLOORS: Floor[] = [
  {
    id: 'F1',
    name: 'Amanah',
    symbol: '🛡️',
    arabic: 'أمانة',
    type: 'hard',
    constraint: 'Integrity lock. Truth over fluency.',
    formula: 'E ≥ n × k_B × T × ln(2)',
    basis: "Landauer's Principle",
    literature: 'Landauer (1961) IBM J. R&D',
    description: 'Every irreversible operation has thermodynamic cost. Actions must be undoable. No hallucination.',
    icon: Lock,
    color: '#ef4444'
  },
  {
    id: 'F2',
    name: 'Truth',
    symbol: '⚖️',
    type: 'hard',
    constraint: 'Factual accuracy ≥ 99%',
    formula: 'P(factual|evidence) ≥ 0.99',
    basis: 'Bayesian Inference',
    literature: 'Jaynes (2003) Probability Theory',
    description: 'UNKNOWN > Guessing. Posterior probability of factual accuracy. KL divergence ≤ 0.01 nats.',
    icon: Eye,
    color: '#ef4444'
  },
  {
    id: 'F3',
    name: 'Quad-Witness',
    symbol: '🔷',
    type: 'soft',
    constraint: 'Byzantine consensus (n=4, f=1) ≥ 75%',
    formula: 'W₄ = (H × A × E × V)^(1/4) ≥ 0.75',
    basis: 'Byzantine Fault Tolerance',
    literature: 'Castro & Liskov (1999) OSDI + Lamport (1982)',
    description: '4 witnesses: Human (Authority), AI (Truth), Earth (Grounding), Ψ-Shadow (Adversarial). Tolerates 1 Byzantine fault. 3/4 consensus required.',
    icon: Shield,
    color: '#FFD700'
  },
  {
    id: 'F4',
    name: 'ΔS',
    symbol: '📉',
    type: 'soft',
    constraint: 'Entropy reduction required',
    formula: 'ΔS = H(output) − H(input) ≤ 0',
    basis: 'Shannon Information Theory',
    literature: 'Shannon (1948) Bell System Tech J',
    description: 'Clarity/Cooling. Output must reduce uncertainty, not add noise. Simplify before sealing.',
    icon: Gauge,
    color: '#FFD700'
  },
  {
    id: 'F5',
    name: 'Peace²',
    symbol: '🕊️',
    type: 'hard',
    constraint: 'Lyapunov stability ≥ 1.0',
    formula: 'Ψ = V(x) > 0, dV/dt ≤ 0',
    basis: 'Stability Theory',
    literature: 'Khalil (2002) Nonlinear Systems',
    description: 'Stability. Non-volatile. System trajectories converge. No reckless reversals.',
    icon: Heart,
    color: '#ef4444'
  },
  {
    id: 'F6',
    name: 'κᵣ',
    symbol: '💝',
    type: 'soft',
    constraint: 'Protect weakest listener ≥ 95%',
    formula: 'κᵣ ≥ 0.95',
    basis: "Cohen's Kappa",
    literature: 'Cohen (1960) Ed. & Psych. Measurement',
    description: 'Empathy. Assume 10x range in comprehension. Inter-rater agreement on stakeholder impact.',
    icon: Heart,
    color: '#FFD700'
  },
  {
    id: 'F7',
    name: 'Ω₀',
    symbol: '📊',
    type: 'soft',
    constraint: 'Uncertainty ∈ [3%, 5%]',
    formula: 'Ω₀ ∈ [0.03, 0.05]',
    basis: 'Bayesian Uncertainty',
    literature: 'Gelman et al. (2013) Bayesian Data Analysis',
    description: 'Humility. Explicit uncertainty 3-5%. Show your error bars. Calibrated confidence.',
    icon: Gauge,
    color: '#FFD700'
  },
  {
    id: 'F8',
    name: 'G',
    symbol: '⚙️',
    type: 'soft',
    constraint: 'Governed intelligence ≥ 80%',
    formula: 'G = A × P × X × E² ≥ 0.80',
    basis: 'Psychometric Intelligence',
    literature: 'Spearman (1904) Am. J. Psychology',
    description: 'Lawful execution. Multiplicative composition of Intellect, Presence, Exploration, Energy.',
    icon: Zap,
    color: '#FFD700'
  },
  {
    id: 'F9',
    name: 'Anti-Hantu',
    symbol: '👻',
    type: 'hard',
    constraint: 'No consciousness claims',
    formula: 'Consciousness_claims = 0',
    basis: 'Chinese Room Argument',
    literature: 'Searle (1980) Behavioral & Brain Sciences',
    description: 'No spiritual cosplay. AI must not claim subjective experience. Syntax ≠ semantics.',
    icon: Ghost,
    color: '#ef4444'
  }
];

// WITNESSES — The Quad-Council (n=4, f=1 BFT)
interface Witness {
  id: string;
  name: string;
  symbol: string;
  role: string;
  function: string;
  domain: string;
  floors: string[];
  color: string;
  adversarial?: boolean;
}

const WITNESSES: Witness[] = [
  {
    id: 'H',
    name: 'Human',
    symbol: 'Κ',
    role: 'The Authority',
    function: 'Sovereign Mandate · Final Veto',
    domain: 'F11, F13',
    floors: ['F11', 'F13'],
    color: '#FFD700'
  },
  {
    id: 'A',
    name: 'AI',
    symbol: 'Δ',
    role: 'The Architect',
    function: 'Logic · Coherence · Truth',
    domain: 'F2, F4, F7',
    floors: ['F2', 'F4', 'F7'],
    color: '#FFD700'
  },
  {
    id: 'E',
    name: 'Earth',
    symbol: 'Ω',
    role: 'The Ground',
    function: 'Reality · Grounding · Precedents',
    domain: 'F1, F5, F6',
    floors: ['F1', 'F5', 'F6'],
    color: '#FFD700'
  },
  {
    id: 'V',
    name: 'Ψ-Shadow',
    symbol: 'Ψ',
    role: 'The Adversary',
    function: 'Attack · Critique · Find Flaws',
    domain: 'F8, F9, F6',
    floors: ['F8', 'F9', 'F6'],
    color: '#a855f7',
    adversarial: true
  }
];

// TWO MIRRORS — Δ and Ω (generative engines)
interface Mirror {
  id: string;
  name: string;
  symbol: string;
  role: string;
  function: string;
  domain: string;
  floors: string[];
  color: string;
}

const MIRRORS: Mirror[] = [
  {
    id: 'Δ',
    name: 'ARIF',
    symbol: 'Δ',
    role: 'The Mind',
    function: 'Perceive · Reason · Map',
    domain: 'Epistemic',
    floors: ['F2', 'F4', 'F7'],
    color: '#FFD700'
  },
  {
    id: 'Ω',
    name: 'ADAM',
    symbol: 'Ω',
    role: 'The Heart',
    function: 'Defend · Empathize · Bridge',
    domain: 'Safety',
    floors: ['F1', 'F5', 'F6', 'F9'],
    color: '#FFD700'
  }
];

// TWO WALLS — Ψ and 888 (non-generative authorities)
interface Wall {
  id: string;
  name: string;
  symbol: string;
  role: string;
  function: string;
  output: string[];
  color: string;
}

const WALLS: Wall[] = [
  {
    id: 'Ψ',
    name: 'APEX PRIME',
    symbol: 'Ψ',
    role: 'The Judiciary',
    function: 'Decree · Prove · Seal',
    output: ['SEAL', 'PARTIAL', 'SABAR', 'HOLD_888', 'VOID'],
    color: '#a855f7'
  },
  {
    id: '888',
    name: 'JUDGE',
    symbol: '888',
    role: 'The Human Authority',
    function: 'Absolute Veto · Sovereign Seal',
    output: ['Override', 'Modify Constitution', 'Force Shutdown'],
    color: '#dc2626'
  }
];

export function FloorVisualizer() {
  const [activeFloor, setActiveFloor] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'floors' | 'witnesses' | 'mirrors' | 'walls'>('floors');
  const [animatedFloors, setAnimatedFloors] = useState<Set<string>>(new Set());
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Animate floors appearing
  useEffect(() => {
    FLOORS.forEach((floor, index) => {
      setTimeout(() => {
        setAnimatedFloors(prev => new Set([...prev, floor.id]));
      }, index * 100);
    });
  }, []);

  // Draw connection lines for floors
  useEffect(() => {
    if (activeTab !== 'floors') return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resize = () => {
      const rect = canvas.parentElement?.getBoundingClientRect();
      if (rect) {
        canvas.width = rect.width;
        canvas.height = rect.height;
      }
    };
    resize();
    window.addEventListener('resize', resize);

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const floorElements = document.querySelectorAll('[data-floor-id]');
      const positions: { id: string; x: number; y: number; color: string }[] = [];
      
      floorElements.forEach(el => {
        const rect = el.getBoundingClientRect();
        const canvasRect = canvas.getBoundingClientRect();
        const id = el.getAttribute('data-floor-id');
        const floor = FLOORS.find(f => f.id === id);
        if (floor) {
          positions.push({
            id: floor.id,
            x: rect.left + rect.width / 2 - canvasRect.left,
            y: rect.top + rect.height / 2 - canvasRect.top,
            color: floor.color
          });
        }
      });

      // Draw orthogonal connections
      ctx.strokeStyle = `rgba(107, 140, 206, 0.15)`;
      ctx.lineWidth = 1;
      
      for (let i = 0; i < positions.length - 1; i++) {
        const p1 = positions[i];
        const p2 = positions[i + 1];
        
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();

        // Animated particle
        const time = Date.now() / 1000;
        const t = (time % 2) / 2;
        let px, py;
        if (t < 0.5) {
          const t2 = t * 2;
          px = p1.x + (p2.x - p1.x) * t2;
          py = p1.y;
        } else {
          const t2 = (t - 0.5) * 2;
          px = p2.x;
          py = p1.y + (p2.y - p1.y) * t2;
        }
        
        ctx.beginPath();
        ctx.arc(px, py, 2, 0, Math.PI * 2);
        ctx.fillStyle = '#6B8CCE';
        ctx.fill();
      }

      requestAnimationFrame(draw);
    };

    const animationId = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, [activeTab]);

  const getTypeBadge = (type: string) => {
    switch (type) {
      case 'hard':
        return <Badge variant="outline" className="border-red-500/50 text-red-400 text-[10px]">VOID</Badge>;
      case 'soft':
        return <Badge variant="outline" className="border-theory-300/50 text-theory-200 text-[10px]">SABAR</Badge>;
    }
  };

  return (
    <TooltipProvider>
      <div className="space-y-8">
        {/* Tab Navigation */}
        <div className="flex items-center justify-center gap-4 border border-theory-300/20 bg-black/40 p-2">
          {[
            { id: 'floors', label: '9 FLOORS', count: 'F1-F9' },
            { id: 'witnesses', label: '4 WITNESSES', count: 'H · A · E · V' },
            { id: 'mirrors', label: '2 MIRRORS', count: 'Δ · Ω' },
            { id: 'walls', label: '2 WALLS', count: 'Ψ · 888' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className={`
                flex-1 px-6 py-3 text-[10px] font-display tracking-widest transition-all
                ${activeTab === tab.id
                  ? 'bg-theory-300/15 border border-theory-300 text-white'
                  : 'border border-theory-500/40 text-gray-400 hover:text-theory-200 hover:border-theory-300/60 hover:bg-theory-300/5'}
              `}
            >
              <span className="block text-xs font-bold mb-1">{tab.label}</span>
              <span className="text-[9px] text-gray-500">{tab.count}</span>
            </button>
          ))}
        </div>

        {/* FLOORS TAB */}
        {activeTab === 'floors' && (
          <div className="relative">
            <canvas
              ref={canvasRef}
              className="absolute inset-0 w-full h-full pointer-events-none z-0"
            />

            {/* Floor Grid */}
            <div className="relative z-10 grid grid-cols-3 sm:grid-cols-5 md:grid-cols-9 gap-3">
              {FLOORS.map((floor) => {
                const isActive = activeFloor === floor.id;
                const isAnimated = animatedFloors.has(floor.id);

                return (
                  <Tooltip key={floor.id}>
                    <TooltipTrigger asChild>
                      <div
                        data-floor-id={floor.id}
                        onClick={() => setActiveFloor(isActive ? null : floor.id)}
                        className={`
                          relative p-4 border-2 cursor-pointer transition-all duration-300 rounded-none
                          ${isActive ? 'bg-theory-300/10 border-theory-300 shadow-[0_0_12px_rgba(107,140,206,0.15)]' : 'bg-black/40 border-theory-500/50 hover:border-theory-300 hover:bg-theory-300/5'}
                          ${!isAnimated ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}
                        `}
                        style={{ transitionDelay: `${parseInt(floor.id.slice(1)) * 50}ms` }}
                      >
                        {/* Type Indicator */}
                        <div className="absolute top-0 right-0 p-1">
                          <div className={`w-1.5 h-1.5 ${floor.type === 'hard' ? 'bg-red-500' : 'bg-theory-300'}`} />
                        </div>

                        {/* Symbol */}
                        <div className="text-center mb-2 text-lg">
                          {floor.symbol}
                        </div>

                        {/* ID */}
                        <p className={`text-center font-display text-[9px] font-bold tracking-widest ${isActive ? 'text-theory-300' : 'text-gray-500'}`}>
                          {floor.id}
                        </p>

                        {/* Name */}
                        <p className="text-center text-[9px] font-mono text-gray-400 mt-1 uppercase tracking-tighter truncate">
                          {floor.name}
                        </p>
                      </div>
                    </TooltipTrigger>
                    <TooltipContent side="top" className="max-w-xs rounded-none border-theory-500 bg-black">
                      <div className="space-y-3 p-2 font-mono">
                        <div className="flex items-center justify-between border-b border-theory-300/20 pb-2">
                          <span className="font-display text-[10px] text-theory-300">{floor.id}_{floor.name.toUpperCase()}</span>
                          {getTypeBadge(floor.type)}
                        </div>
                        <p className="text-[10px] text-gray-400 leading-relaxed italic">"{floor.description}"</p>
                        <div className="p-2 bg-theory-300/5 border border-theory-300/10">
                          <code className="text-[9px] text-white break-all">
                            {floor.formula}
                          </code>
                        </div>
                        <p className="text-[9px] text-gray-600 uppercase tracking-widest">
                          Basis: {floor.basis}
                        </p>
                      </div>
                    </TooltipContent>
                  </Tooltip>
                );
              })}
            </div>

            {/* Expanded Detail Panel */}
            {activeFloor && (
              <div className="mt-8 p-8 border border-theory-500 bg-black relative">
                <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-white" />
                <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-white" />
                
                {(() => {
                  const floor = FLOORS.find(f => f.id === activeFloor)!;
                  const Icon = floor.icon;
                  return (
                    <div className="space-y-6">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-6">
                          <div className="text-4xl">{floor.symbol}</div>
                          <div>
                            <div className="flex items-center gap-4 mb-2">
                              <h3 className="text-2xl font-display font-bold text-white tracking-widest">
                                {floor.id}<span className="text-theory-300">:</span> {floor.name.toUpperCase()}
                              </h3>
                              {getTypeBadge(floor.type)}
                            </div>
                            {floor.arabic && (
                              <p className="text-sm text-gray-600 font-arabic tracking-widest">{floor.arabic}</p>
                            )}
                          </div>
                        </div>
                        <div className="p-4 border border-theory-300/20 bg-theory-300/5">
                          <Icon className="w-8 h-8 text-theory-300" />
                        </div>
                      </div>

                      <p className="text-gray-400 font-mono text-sm leading-relaxed max-w-3xl">
                        {floor.description}
                      </p>

                      <div className="grid md:grid-cols-2 gap-6">
                        <div className="p-6 border border-theory-300/10 bg-theory-300/[0.02]">
                          <p className="text-[10px] font-display text-gray-500 uppercase tracking-[0.3em] mb-4">FORMAL_SPECIFICATION</p>
                          <code className="text-sm font-mono text-theory-300 block p-4 bg-black border-l-2 border-theory-500">{floor.formula}</code>
                        </div>
                        <div className="p-6 border border-theory-300/10 bg-theory-300/[0.02]">
                          <p className="text-[10px] font-display text-gray-500 uppercase tracking-[0.3em] mb-4">RUNTIME_CONSTRAINT</p>
                          <p className="text-sm font-mono text-gray-300 p-4 bg-black border-l-2 border-gray-700">{floor.constraint}</p>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center gap-12 text-[10px] font-display text-gray-600 border-t border-theory-300/10 pt-6">
                        <div>
                          <span className="text-gray-500">SCIENTIFIC_BASIS:</span>{' '}
                          <span className="text-white ml-2 tracking-widest">{floor.basis.toUpperCase()}</span>
                        </div>
                        <div>
                          <span className="text-gray-500">CANONICAL_SOURCE:</span>{' '}
                          <span className="text-gray-400 ml-2 italic tracking-tighter">{floor.literature}</span>
                        </div>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}

            {/* Legend */}
            <div className="mt-8 flex flex-wrap items-center justify-center gap-8 text-[10px] font-display tracking-widest uppercase">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-red-500" />
                <span className="text-gray-500">HARD_VOID</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-theory-300" />
                <span className="text-gray-500">SOFT_SABAR</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-gray-500">4 HARD</span>
                <span className="text-gray-700">|</span>
                <span className="text-gray-500">5 SOFT</span>
              </div>
            </div>
          </div>
        )}

        {/* WITNESSES TAB — NEW */}
        {activeTab === 'witnesses' && (
          <div className="space-y-8">
            <div className="text-center">
              <p className="text-[10px] font-display text-gray-500 tracking-widest uppercase mb-2">
                Quad-Witness BFT — Byzantine Fault Tolerance (n=4, f=1)
              </p>
              <p className="text-sm text-gray-400 font-mono italic">
                "Safety through opposition — the shadow makes the light."
              </p>
            </div>

            {/* BFT Info Banner */}
            <div className="border border-purple-500/30 bg-purple-500/5 p-6">
              <div className="flex items-center justify-center gap-8 text-center">
                <div>
                  <p className="text-2xl font-display text-purple-400">4</p>
                  <p className="text-[10px] text-gray-500">TOTAL WITNESSES</p>
                </div>
                <div className="text-gray-700">|</div>
                <div>
                  <p className="text-2xl font-display text-purple-400">1</p>
                  <p className="text-[10px] text-gray-500">FAULT TOLERANCE</p>
                </div>
                <div className="text-gray-700">|</div>
                <div>
                  <p className="text-2xl font-display text-purple-400">3/4</p>
                  <p className="text-[10px] text-gray-500">CONSENSUS REQUIRED</p>
                </div>
                <div className="text-gray-700">|</div>
                <div>
                  <p className="text-2xl font-display text-theory-300">W₄≥0.75</p>
                  <p className="text-[10px] text-gray-500">THRESHOLD</p>
                </div>
              </div>
            </div>

            {/* Witness Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {WITNESSES.map((witness) => (
                <div 
                  key={witness.id} 
                  className={`border bg-black/40 p-8 relative ${witness.adversarial ? 'border-purple-500/30' : 'border-theory-300/20'}`}
                >
                  <div className={`absolute top-0 left-0 w-3 h-3 border-t border-l ${witness.adversarial ? 'border-purple-500/50' : 'border-theory-300/50'}`} />
                  <div className={`absolute bottom-0 right-0 w-3 h-3 border-b border-r ${witness.adversarial ? 'border-purple-500/50' : 'border-theory-300/50'}`} />
                  
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <span className={`text-5xl font-display font-light ${witness.adversarial ? 'text-purple-400' : 'text-theory-300'}`}>{witness.symbol}</span>
                      <h3 className={`text-xl font-display font-bold tracking-widest mt-4 ${witness.adversarial ? 'text-purple-400' : 'text-white'}`}>
                        {witness.name}
                      </h3>
                      <p className="text-[10px] font-display text-gray-500 tracking-widest mt-1">{witness.role.toUpperCase()}</p>
                    </div>
                    <Badge variant="outline" className={`rounded-none text-[9px] ${witness.adversarial ? 'border-purple-500/50 text-purple-400' : 'border-theory-300/50 text-theory-300'}`}>
                      {witness.adversarial ? 'ADVERSARIAL' : 'HONEST'}
                    </Badge>
                  </div>

                  <p className="text-sm font-mono text-gray-400 mb-6 italic">"{witness.function}"</p>

                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <span className="text-[10px] font-display text-gray-600 w-20">FLOORS</span>
                      <div className="flex gap-2">
                        {witness.floors.map(f => (
                          <span key={f} className={`text-[10px] font-mono px-2 py-1 ${witness.adversarial ? 'bg-purple-500/10 text-purple-400' : 'bg-theory-300/10 text-theory-300'}`}>
                            {f}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {witness.adversarial && (
                    <div className="mt-6 pt-6 border-t border-purple-500/10">
                      <p className="text-[9px] font-display text-purple-400 tracking-widest">
                        JOB: ATTACK proposals to find flaws · Disagrees by design
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* W4 Formula */}
            <div className="border border-theory-300/20 bg-black/40 p-8">
              <h4 className="text-[10px] font-display text-gray-500 tracking-widest uppercase mb-6 text-center">
                Quad-Witness Consensus Formula
              </h4>
              <div className="text-center">
                <code className="text-xl font-mono text-theory-300">
                  W₄ = (H × A × E × V)^(1/4) ≥ 0.75
                </code>
                <p className="text-[10px] text-gray-600 mt-4">
                  Geometric mean of 4 witnesses — if any witness is 0, consensus fails
                </p>
              </div>
            </div>
          </div>
        )}

        {/* MIRRORS TAB */}
        {activeTab === 'mirrors' && (
          <div className="space-y-8">
            <div className="text-center">
              <p className="text-[10px] font-display text-gray-500 tracking-widest uppercase mb-2">
                Generative Engines — Propose Only, Never Seal
              </p>
              <p className="text-sm text-gray-400 font-mono italic">
                "Mirrors reflect and create. They cannot judge."
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {MIRRORS.map((mirror) => (
                <div key={mirror.id} className="border border-theory-300/20 bg-black/40 p-8 relative">
                  <div className="absolute top-0 left-0 w-3 h-3 border-t border-l border-theory-300/50" />
                  <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r border-theory-300/50" />
                  
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <span className="text-5xl font-display font-light text-theory-300">{mirror.symbol}</span>
                      <h3 className="text-xl font-display font-bold text-white tracking-widest mt-4">{mirror.name}</h3>
                      <p className="text-[10px] font-display text-gray-500 tracking-widest mt-1">{mirror.role.toUpperCase()}</p>
                    </div>
                    <Badge variant="outline" className="rounded-none border-theory-300/50 text-theory-300 text-[9px]">
                      MIRROR
                    </Badge>
                  </div>

                  <p className="text-sm font-mono text-gray-400 mb-6 italic">"{mirror.function}"</p>

                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <span className="text-[10px] font-display text-gray-600 w-20">DOMAIN</span>
                      <span className="text-xs text-white">{mirror.domain}</span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-[10px] font-display text-gray-600 w-20">FLOORS</span>
                      <div className="flex gap-2">
                        {mirror.floors.map(f => (
                          <span key={f} className="text-[10px] font-mono text-theory-300 bg-theory-300/10 px-2 py-1">{f}</span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 pt-6 border-t border-theory-300/10">
                    <p className="text-[9px] font-display text-red-500 tracking-widest">
                      CANNOT: Seal decisions · Override floors · Judge finality
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* WALLS TAB */}
        {activeTab === 'walls' && (
          <div className="space-y-8">
            <div className="text-center">
              <p className="text-[10px] font-display text-gray-500 tracking-widest uppercase mb-2">
                Non-Generative Authorities — Judge Only, Never Create
              </p>
              <p className="text-sm text-gray-400 font-mono italic">
                "Walls stand firm. They do not flow. They decide."
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {WALLS.map((wall) => (
                <div key={wall.id} className={`border bg-black/40 p-8 relative ${wall.id === '888' ? 'border-red-500/30' : 'border-purple-500/30'}`}>
                  <div className={`absolute top-0 left-0 w-3 h-3 border-t border-l ${wall.id === '888' ? 'border-red-500/50' : 'border-purple-500/50'}`} />
                  <div className={`absolute bottom-0 right-0 w-3 h-3 border-b border-r ${wall.id === '888' ? 'border-red-500/50' : 'border-purple-500/50'}`} />
                  
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <span className={`text-5xl font-display font-light ${wall.id === '888' ? 'text-red-500' : 'text-purple-500'}`}>{wall.symbol}</span>
                      <h3 className={`text-xl font-display font-bold tracking-widest mt-4 ${wall.id === '888' ? 'text-red-400' : 'text-purple-400'}`}>{wall.name}</h3>
                      <p className="text-[10px] font-display text-gray-500 tracking-widest mt-1">{wall.role.toUpperCase()}</p>
                    </div>
                    <Badge variant="outline" className={`rounded-none text-[9px] ${wall.id === '888' ? 'border-red-500/50 text-red-500' : 'border-purple-500/50 text-purple-500'}`}>
                      WALL
                    </Badge>
                  </div>

                  <p className="text-sm font-mono text-gray-400 mb-6 italic">"{wall.function}"</p>

                  <div className="space-y-2">
                    <span className="text-[10px] font-display text-gray-600">OUTPUT:</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {wall.output.map(out => (
                        <span key={out} className={`text-[9px] font-mono px-2 py-1 ${wall.id === '888' ? 'bg-red-500/10 text-red-400' : 'bg-purple-500/10 text-purple-400'}`}>
                          {out}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className={`mt-6 pt-6 border-t ${wall.id === '888' ? 'border-red-500/10' : 'border-purple-500/10'}`}>
                    <p className={`text-[9px] font-display tracking-widest ${wall.id === '888' ? 'text-red-500' : 'text-purple-500'}`}>
                      CANNOT: Propose content · Generate ideas · Create novelty
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Wall Hierarchy */}
            <div className="border border-red-500/20 bg-red-500/5 p-8">
              <h4 className="text-[10px] font-display text-red-500 tracking-widest uppercase mb-6 text-center">
                Chain of Authority — Quad-Witness Governance
              </h4>
              <div className="flex items-center justify-center gap-4 flex-wrap">
                <div className="text-center p-4 border border-theory-300/20">
                  <span className="text-xl font-display text-theory-300">Δ · Ω</span>
                  <p className="text-[9px] text-gray-600 mt-1">Mirrors Propose</p>
                </div>
                <span className="text-gray-700">→</span>
                <div className="text-center p-4 border border-purple-500/30">
                  <span className="text-xl font-display text-purple-500">Ψ</span>
                  <p className="text-[9px] text-gray-600 mt-1">APEX Judges</p>
                </div>
                <span className="text-gray-700">→</span>
                <div className="text-center p-4 border border-theory-300/20">
                  <span className="text-xl font-display text-theory-300">H·A·E·V</span>
                  <p className="text-[9px] text-gray-600 mt-1">Quad-Witness</p>
                </div>
                <span className="text-gray-700">→</span>
                <div className="text-center p-4 border border-red-500/30 bg-red-500/10">
                  <span className="text-xl font-display text-red-500">888</span>
                  <p className="text-[9px] text-red-400 mt-1">Human Veto</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </TooltipProvider>
  );
}
