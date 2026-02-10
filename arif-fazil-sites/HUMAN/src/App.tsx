import { useEffect, useState } from 'react';
import {
  Github,
  Linkedin,
  Mail,
  ExternalLink,
  MapPin,
  Mountain,
  TrendingUp,
  Cpu,
  ChevronRight,
  Menu,
  X,
  Code,
  Compass,
  Triangle,
  Terminal,
  Bot
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';

const ARTICLES = [
  { title: 'Prompt · Physics · Paradox', desc: 'What happens when you treat AI prompts like physics experiments', url: 'https://medium.com/@arifbfazil/prompt-physics-paradox-1f1581b95acb' },
  { title: 'Einstein vs Oppenheimer', desc: 'The difference between knowing how and knowing why', url: 'https://medium.com/@arifbfazil/einstein-vs-oppenheimer-ab8b642720eb' },
  { title: 'The ARIF Test', desc: 'A simple test for whether AI systems are actually governed', url: 'https://medium.com/@arifbfazil/the-arif-test-df63c074d521' },
  { title: 'Rukun AGI', desc: 'Five pillars for building AI that respects boundaries', url: 'https://medium.com/@arifbfazil/rukun-agi-the-five-pillars-of-artificial-general-intelligence-bba2fb97e4dc' },
];

// Animated Geological Strata SVG Component
function GeologyVisual() {
  return (
    <svg viewBox="0 0 120 80" className="w-full h-full">
      <defs>
        <linearGradient id="strata1" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#3D2314" />
          <stop offset="100%" stopColor="#5C3A1E" />
        </linearGradient>
        <linearGradient id="strata2" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#5C3A1E" />
          <stop offset="100%" stopColor="#8B5A2B" />
        </linearGradient>
        <linearGradient id="strata3" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#8B5A2B" />
          <stop offset="100%" stopColor="#A67B5B" />
        </linearGradient>
        <linearGradient id="magma" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#8B0000" />
          <stop offset="50%" stopColor="#FF2D2D" />
          <stop offset="100%" stopColor="#8B0000" />
        </linearGradient>
      </defs>
      {/* Geological strata layers */}
      <path d="M0,60 Q30,55 60,58 T120,52 L120,80 L0,80 Z" fill="url(#strata1)">
        <animate attributeName="d" values="M0,60 Q30,55 60,58 T120,52 L120,80 L0,80 Z;M0,62 Q30,57 60,60 T120,54 L120,80 L0,80 Z;M0,60 Q30,55 60,58 T120,52 L120,80 L0,80 Z" dur="8s" repeatCount="indefinite"/>
      </path>
      <path d="M0,40 Q40,35 80,42 T120,38 L120,60 L0,60 Z" fill="url(#strata2)">
        <animate attributeName="d" values="M0,40 Q40,35 80,42 T120,38 L120,60 L0,60 Z;M0,42 Q40,37 80,44 T120,40 L120,60 L0,60 Z;M0,40 Q40,35 80,42 T120,38 L120,60 L0,60 Z" dur="6s" repeatCount="indefinite"/>
      </path>
      <path d="M0,20 Q35,15 70,22 T120,18 L120,40 L0,40 Z" fill="url(#strata3)">
        <animate attributeName="d" values="M0,20 Q35,15 70,22 T120,18 L120,40 L0,40 Z;M0,22 Q35,17 70,24 T120,20 L120,40 L0,40 Z;M0,20 Q35,15 70,22 T120,18 L120,40 L0,40 Z" dur="7s" repeatCount="indefinite"/>
      </path>
      {/* Magma core */}
      <circle cx="60" cy="70" r="8" fill="url(#magma)" opacity="0.8">
        <animate attributeName="r" values="8;10;8" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.8;0.5;0.8" dur="3s" repeatCount="indefinite"/>
      </circle>
      {/* Seismic waves */}
      <ellipse cx="60" cy="70" rx="20" ry="6" fill="none" stroke="#FF2D2D" strokeWidth="0.5" opacity="0.3">
        <animate attributeName="rx" values="20;40;60" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;0.2;0" dur="2s" repeatCount="indefinite"/>
      </ellipse>
    </svg>
  );
}

// Animated Economics/Market Visual
function EconomicsVisual() {
  return (
    <svg viewBox="0 0 120 80" className="w-full h-full">
      <defs>
        <linearGradient id="chartGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#8B0000" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#8B0000" stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* Grid lines */}
      <line x1="10" y1="20" x2="110" y2="20" stroke="#333" strokeWidth="0.5" opacity="0.3"/>
      <line x1="10" y1="40" x2="110" y2="40" stroke="#333" strokeWidth="0.5" opacity="0.3"/>
      <line x1="10" y1="60" x2="110" y2="60" stroke="#333" strokeWidth="0.5" opacity="0.3"/>
      {/* Area chart */}
      <path d="M10,60 L25,45 L40,50 L55,30 L70,35 L85,20 L100,25 L110,15 L110,70 L10,70 Z" fill="url(#chartGrad)" opacity="0.6"/>
      {/* Line chart */}
      <path d="M10,60 L25,45 L40,50 L55,30 L70,35 L85,20 L100,25 L110,15" fill="none" stroke="#FF2D2D" strokeWidth="2" strokeLinecap="round">
        <animate attributeName="stroke-dasharray" values="0,200;200,0" dur="3s" fill="freeze"/>
      </path>
      {/* Data points */}
      <circle cx="25" cy="45" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="0.5s" fill="freeze"/>
      </circle>
      <circle cx="40" cy="50" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="0.7s" fill="freeze"/>
      </circle>
      <circle cx="55" cy="30" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="0.9s" fill="freeze"/>
      </circle>
      <circle cx="70" cy="35" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="1.1s" fill="freeze"/>
      </circle>
      <circle cx="85" cy="20" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="1.3s" fill="freeze"/>
      </circle>
      <circle cx="100" cy="25" r="3" fill="#FF2D2D">
        <animate attributeName="r" values="0;3" dur="0.3s" begin="1.5s" fill="freeze"/>
      </circle>
      {/* Candlestick */}
      <line x1="95" y1="15" x2="95" y2="30" stroke="#00C853" strokeWidth="1"/>
      <rect x="92" y="18" width="6" height="8" fill="#00C853" opacity="0.8">
        <animate attributeName="height" values="0;8" dur="0.5s" begin="2s" fill="freeze"/>
      </rect>
    </svg>
  );
}

// Animated AI/Neural Network Visual
function AIVisual() {
  return (
    <svg viewBox="0 0 120 80" className="w-full h-full">
      <defs>
        <radialGradient id="nodeGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#FF2D2D" />
          <stop offset="100%" stopColor="#8B0000" />
        </radialGradient>
        <linearGradient id="pulseGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="transparent" />
          <stop offset="50%" stopColor="#FF2D2D" />
          <stop offset="100%" stopColor="transparent" />
        </linearGradient>
      </defs>
      {/* Neural connections */}
      <line x1="20" y1="25" x2="50" y2="30" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="20" y1="25" x2="50" y2="50" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="20" y1="55" x2="50" y2="30" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="20" y1="55" x2="50" y2="50" stroke="#444" strokeWidth="1" opacity="0.5"/>
      
      <line x1="50" y1="30" x2="80" y2="25" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="50" y1="30" x2="80" y2="55" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="50" y1="50" x2="80" y2="25" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="50" y1="50" x2="80" y2="55" stroke="#444" strokeWidth="1" opacity="0.5"/>
      
      <line x1="80" y1="25" x2="100" y2="40" stroke="#444" strokeWidth="1" opacity="0.5"/>
      <line x1="80" y1="55" x2="100" y2="40" stroke="#444" strokeWidth="1" opacity="0.5"/>
      
      {/* Animated data pulses */}
      <circle cx="35" cy="28" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="20;50" dur="1.5s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="25;30" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="35" cy="42" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="20;50" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="55;50" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="65" cy="32" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="50;80" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="30;25" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="90" cy="47" r="2" fill="#FF2D2D" opacity="0">
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.8s" repeatCount="indefinite"/>
        <animate attributeName="cx" values="80;100" dur="1.5s" begin="0.8s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="55;40" dur="1.5s" begin="0.8s" repeatCount="indefinite"/>
      </circle>
      
      {/* Nodes */}
      <circle cx="20" cy="25" r="6" fill="url(#nodeGrad)"/>
      <circle cx="20" cy="55" r="6" fill="url(#nodeGrad)"/>
      <circle cx="50" cy="30" r="8" fill="url(#nodeGrad)"/>
      <circle cx="50" cy="50" r="8" fill="url(#nodeGrad)"/>
      <circle cx="80" cy="25" r="6" fill="url(#nodeGrad)"/>
      <circle cx="80" cy="55" r="6" fill="url(#nodeGrad)"/>
      <circle cx="100" cy="40" r="10" fill="url(#nodeGrad)"/>
      
      {/* Binary code rain effect */}
      <text x="105" y="15" fontSize="6" fill="#8B0000" fontFamily="JetBrains Mono" opacity="0.6">101</text>
      <text x="10" y="70" fontSize="6" fill="#8B0000" fontFamily="JetBrains Mono" opacity="0.6">010</text>
    </svg>
  );
}

function App() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-gray-200 font-sans selection:bg-red-900/30 selection:text-red-200">
      {/* Navigation - Minimal */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-[#0a0a0a]/90 backdrop-blur-md border-b border-gray-800/50' : ''}`}>
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center justify-between py-5">
            {/* Logo / Name */}
            <a href="#" className="text-sm font-medium text-gray-300 hover:text-white transition-colors font-mono">
              arif<span className="text-red-500">.</span>fazil
            </a>

            {/* Desktop links */}
            <div className="hidden md:flex items-center gap-6">
              <a href="#about" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">about</a>
              <a href="#work" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">work</a>
              <a href="#writing" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all">writing</a>
              <a href="/llms.txt" className="px-3 py-1.5 rounded-md text-sm text-gray-400 hover:text-red-400 hover:bg-red-950/20 border border-transparent hover:border-red-800/50 transition-all font-mono">llms.txt</a>
            </div>

            {/* Trinity nav - pill style */}
            <div className="hidden md:flex items-center gap-1 bg-gray-900/50 rounded-full px-1 py-1 border border-gray-700">
              <a href="https://arif-fazil.com" className="px-3 py-1.5 rounded-full bg-red-500/20 text-red-400 text-xs font-medium border border-red-500/30 hover:bg-red-500/30 transition-colors">
                HUMAN
              </a>
              <a href="https://apex.arif-fazil.com" className="px-3 py-1.5 rounded-full text-gray-400 text-xs font-medium border border-transparent hover:border-amber-500/30 hover:text-amber-400 hover:bg-amber-950/20 transition-all">
                THEORY
              </a>
              <a href="https://arifos.arif-fazil.com" className="px-3 py-1.5 rounded-full text-gray-400 text-xs font-medium border border-transparent hover:border-cyan-500/30 hover:text-cyan-400 hover:bg-cyan-950/20 transition-all">
                APPS
              </a>
            </div>

            {/* Mobile menu */}
            <button type="button" className="md:hidden p-2 text-gray-400" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden bg-[#0a0a0a] border-b border-gray-800 px-6 py-4 space-y-3">
            <a href="#about" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all" onClick={() => setMobileMenuOpen(false)}>about</a>
            <a href="#work" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all" onClick={() => setMobileMenuOpen(false)}>work</a>
            <a href="#writing" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 border border-transparent hover:border-gray-700 transition-all" onClick={() => setMobileMenuOpen(false)}>writing</a>
            <a href="/llms.txt" className="block px-3 py-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-950/20 border border-transparent hover:border-red-800/50 transition-all font-mono" onClick={() => setMobileMenuOpen(false)}>llms.txt</a>
            <Separator className="bg-gray-800 my-3" />
            <div className="flex gap-2">
              <a href="https://arif-fazil.com" className="px-4 py-2 rounded-full bg-red-500/20 text-red-400 text-xs border border-red-500/30">HUMAN</a>
              <a href="https://apex.arif-fazil.com" className="px-4 py-2 rounded-full text-amber-400 text-xs border border-amber-500/30 bg-amber-950/10">THEORY</a>
              <a href="https://arifos.arif-fazil.com" className="px-4 py-2 rounded-full text-cyan-400 text-xs border border-cyan-500/30 bg-cyan-950/10">APPS</a>
            </div>
          </div>
        )}
      </nav>

      {/* Hero - Minimal Centered */}
      <section className="relative min-h-screen flex items-center justify-center pt-20 pb-16">
        {/* Subtle grid background */}
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#1a1a1a_1px,transparent_1px),linear-gradient(to_bottom,#1a1a1a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20" />
        </div>

        <div className="relative z-10 max-w-2xl mx-auto px-6 text-center">
          {/* Trinity Logo */}
          <div className="flex justify-center mb-8">
            <img 
              src="/images/arifos-logo.webp" 
              alt="arifOS Trinity" 
              className="w-48 h-48 object-contain drop-shadow-[0_0_40px_rgba(255,45,45,0.4)]"
            />
          </div>

          {/* Ditempa Badge */}
          <div className="flex justify-center mb-6">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-red-500/30 bg-red-950/20 text-red-400 text-xs font-mono tracking-wider">
              <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
              DITEMPA BUKAN DIBERI
            </div>
          </div>

          {/* Name */}
          <h1 className="text-5xl sm:text-7xl font-bold mb-4 tracking-tighter bg-gradient-to-r from-red-500 via-red-400 to-red-600 text-transparent bg-clip-text">
            ARIF<span className="block">FAZIL</span>
          </h1>

          {/* One-liner */}
          <p className="text-lg text-gray-400 mb-2 font-mono text-sm">
            Geoscientist <span className="text-red-500/60">·</span> Economist <span className="text-red-500/60">·</span> AI Governance
          </p>

          {/* Location */}
          <div className="flex items-center justify-center gap-2 text-gray-500 mb-10">
            <MapPin className="w-3.5 h-3.5" />
            <span className="text-sm">Penang, Malaysia</span>
          </div>

          {/* Bio - concise */}
          <p className="text-gray-300 leading-relaxed max-w-xl mx-auto mb-10 text-base">
            Exploration geoscientist with 13+ years at <span className="text-white font-medium">PETRONAS</span>, 
            specializing in subsurface interpretation and frontier basin analysis. 
            Currently building{' '}
            <a href="https://arifos.arif-fazil.com" className="text-red-400 hover:text-red-300 underline underline-offset-4">arifOS</a>,
            {' '}a constitutional AI governance framework applying safety-critical systems thinking 
            to artificial intelligence.
          </p>

          {/* Social links - button style */}
          <div className="flex items-center justify-center gap-3 flex-wrap">
            <a href="https://github.com/ariffazil" className="px-4 py-2 rounded-lg bg-gray-900/50 border border-gray-700 text-gray-300 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all text-sm flex items-center gap-2">
              <Github className="w-4 h-4" /> GitHub
            </a>
            <a href="https://linkedin.com/in/arif-fazil" className="px-4 py-2 rounded-lg bg-gray-900/50 border border-gray-700 text-gray-300 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all text-sm flex items-center gap-2">
              <Linkedin className="w-4 h-4" /> LinkedIn
            </a>
            <a href="https://medium.com/@arifbfazil" className="px-4 py-2 rounded-lg bg-gray-900/50 border border-gray-700 text-gray-300 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all text-sm flex items-center gap-2">
              <ExternalLink className="w-4 h-4" /> Medium
            </a>
            <a href="mailto:arifbfazil@gmail.com" className="px-4 py-2 rounded-lg bg-gray-900/50 border border-gray-700 text-gray-300 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all text-sm flex items-center gap-2">
              <Mail className="w-4 h-4" /> Email
            </a>
          </div>
        </div>
      </section>

      {/* Three Disciplines - Visual Cards */}
      <section id="about" className="py-20 border-t border-gray-800/50">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-sm font-mono text-gray-500 mb-12 uppercase tracking-wider">Three Disciplines</h2>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Geology */}
            <div className="group">
              <div className="h-32 mb-6 rounded-lg bg-gray-900/50 border border-gray-800 overflow-hidden relative">
                <div className="absolute inset-0 opacity-60 group-hover:opacity-80 transition-opacity">
                  <GeologyVisual />
                </div>
                <div className="absolute bottom-3 left-3">
                  <Mountain className="w-5 h-5 text-red-400" />
                </div>
              </div>
              <h3 className="font-medium text-white mb-2">Geoscience</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Subsurface interpretation, seismic analysis, and frontier basin studies. 
                13+ years of exploration experience with focus on the Malay Basin.
              </p>
            </div>

            {/* Economics */}
            <div className="group">
              <div className="h-32 mb-6 rounded-lg bg-gray-900/50 border border-gray-800 overflow-hidden relative">
                <div className="absolute inset-0 opacity-60 group-hover:opacity-80 transition-opacity">
                  <EconomicsVisual />
                </div>
                <div className="absolute bottom-3 left-3">
                  <TrendingUp className="w-5 h-5 text-red-400" />
                </div>
              </div>
              <h3 className="font-medium text-white mb-2">Economics</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                How incentives shape behavior, how markets price risk, and how 
                decisions are made under uncertainty with real consequences.
              </p>
            </div>

            {/* AI */}
            <div className="group">
              <div className="h-32 mb-6 rounded-lg bg-gray-900/50 border border-gray-800 overflow-hidden relative">
                <div className="absolute inset-0 opacity-60 group-hover:opacity-80 transition-opacity">
                  <AIVisual />
                </div>
                <div className="absolute bottom-3 left-3">
                  <Cpu className="w-5 h-5 text-red-400" />
                </div>
              </div>
              <h3 className="font-medium text-white mb-2">AI Governance</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Applying industrial safety thinking to AI systems. Constitutional 
                safeguards that sit between an AI and its decisions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Biography — Sovereign Memory */}
      <section id="biography" className="py-20 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <h2 className="text-sm font-mono text-gray-500 mb-8 uppercase tracking-wider">Sovereign Memory</h2>

          <div className="space-y-8">
            {/* Identity Core */}
            <div className="p-6 rounded-xl border border-gray-800 bg-gray-900/20">
              <h3 className="text-lg font-medium text-white mb-4 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-red-500" />
                Identity Core
              </h3>
              <div className="space-y-3 text-gray-300">
                <p><strong className="text-white">Name:</strong> Muhammad Arif bin Fazil</p>
                <p><strong className="text-white">Born:</strong> May 22, 1990 — Bayan Lepas, Penang, Malaysia</p>
                <p><strong className="text-white">Role:</strong> Anak Sulung (Eldest Son), Architect, Exploration Geoscientist</p>
                <p><strong className="text-white">Cultural Roots:</strong> Penang Malay (Loghat Utara)</p>
                <p className="text-red-400 font-mono text-sm mt-4">"DITEMPA BUKAN DIBERI" — Forged, Not Given</p>
              </div>
            </div>

            {/* Professional Background */}
            <div className="p-6 rounded-xl border border-gray-800 bg-gray-900/20">
              <h3 className="text-lg font-medium text-white mb-4 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-red-500" />
                Professional Background
              </h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="text-white font-medium mb-2">PETRONAS — Exploration Geoscientist (2014–present)</h4>
                  <ul className="space-y-2 text-gray-400 text-sm">
                    <li>• 13+ years in exploration geoscience, 100% success rate, zero dry wells</li>
                    <li>• <strong className="text-gray-300">Bekantan-1:</strong> Shallowest flowing oil discovery in Malay Basin history</li>
                    <li>• <strong className="text-gray-300">Puteri Basement-1:</strong> Instrumental to PM318 PSC value realization</li>
                    <li>• <strong className="text-gray-300">Lebah Emas-1:</strong> Western Hinge Fault Zone play success</li>
                  </ul>
                </div>

                <div>
                  <h4 className="text-white font-medium mb-2">Education</h4>
                  <ul className="space-y-2 text-gray-400 text-sm">
                    <li>• <strong className="text-gray-300">B.Sc. Double Major:</strong> Geology & Geophysics + Economics</li>
                    <li>• <strong className="text-gray-300">Certificate:</strong> Environmental Studies</li>
                    <li>• <strong className="text-gray-300">University:</strong> University of Wisconsin–Madison (2009–2013)</li>
                    <li>• <strong className="text-gray-300">Scholarship:</strong> Full PETRONAS scholarship</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Current Mission */}
            <div className="p-6 rounded-xl border border-red-500/30 bg-red-950/10">
              <h3 className="text-lg font-medium text-white mb-4 flex items-center gap-2">
                <Bot className="w-5 h-5 text-red-500" />
                Current Mission (2026)
              </h3>
              <p className="text-gray-300 leading-relaxed">
                Building <strong className="text-white">arifOS</strong>: Constitutional AI governance framework. 
                Developing thermodynamic constraints for artificial intelligence systems.
              </p>
              <p className="text-gray-500 text-sm mt-3">
                Developing arifOS alongside PETRONAS responsibilities.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trinity Ecosystem - Clean Table */}
      <section id="work" className="py-20 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <h2 className="text-sm font-mono text-gray-500 mb-4 uppercase tracking-wider">Ecosystem</h2>
          <p className="text-gray-400 text-sm mb-8">Three layers, one system. Pick your path.</p>

          {/* Trinity Links */}
          <div className="space-y-4 mb-12">
            <a href="https://apex.arif-fazil.com" className="group flex items-center justify-between p-5 rounded-xl border-2 border-gray-800 hover:border-amber-600/50 bg-gray-900/30 hover:bg-amber-950/20 transition-all shadow-sm hover:shadow-amber-900/10">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-amber-950/30 border border-amber-800/30 flex items-center justify-center group-hover:bg-amber-900/30 transition-colors">
                  <Compass className="w-6 h-6 text-amber-500" />
                </div>
                <div>
                  <h3 className="font-medium text-white group-hover:text-amber-400 transition-colors text-lg">I'm evaluating</h3>
                  <p className="text-sm text-gray-400">Read the theory — axioms, constitutional canon</p>
                </div>
              </div>
              <div className="w-10 h-10 rounded-full bg-gray-800/50 flex items-center justify-center group-hover:bg-amber-900/30 transition-colors">
                <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-amber-500 transition-colors" />
              </div>
            </a>
            
            <a href="https://arifos.arif-fazil.com" className="group flex items-center justify-between p-5 rounded-xl border-2 border-gray-800 hover:border-cyan-600/50 bg-gray-900/30 hover:bg-cyan-950/20 transition-all shadow-sm hover:shadow-cyan-900/10">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-cyan-950/30 border border-cyan-800/30 flex items-center justify-center group-hover:bg-cyan-900/30 transition-colors">
                  <Code className="w-6 h-6 text-cyan-500" />
                </div>
                <div>
                  <h3 className="font-medium text-white group-hover:text-cyan-400 transition-colors text-lg">I'm integrating</h3>
                  <p className="text-sm text-gray-400">Jump to docs — API, MCP tools, quickstart</p>
                </div>
              </div>
              <div className="w-10 h-10 rounded-full bg-gray-800/50 flex items-center justify-center group-hover:bg-cyan-900/30 transition-colors">
                <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-cyan-500 transition-colors" />
              </div>
            </a>
          </div>

          {/* Trinity Table */}
          <div className="rounded-lg border border-gray-800 overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-900/30">
                  <th className="text-left px-4 py-3 text-gray-500 font-normal font-mono text-xs uppercase">Layer</th>
                  <th className="text-left px-4 py-3 text-gray-500 font-normal font-mono text-xs uppercase">Site</th>
                  <th className="text-left px-4 py-3 text-gray-500 font-normal font-mono text-xs uppercase hidden sm:table-cell">Purpose</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/50">
                <tr className="hover:bg-gray-900/30 transition-colors cursor-pointer" onClick={() => window.location.href='https://arif-fazil.com'}>
                  <td className="px-4 py-4">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-red-500/10 text-red-400 font-mono text-xs border border-red-500/20">HUMAN</span>
                  </td>
                  <td className="px-4 py-4">
                    <a href="https://arif-fazil.com" className="text-gray-200 hover:text-red-400 transition-colors font-medium">arif-fazil.com</a>
                  </td>
                  <td className="px-4 py-4 text-gray-500 hidden sm:table-cell">Front page, status, entry points</td>
                </tr>
                <tr className="hover:bg-gray-900/30 transition-colors cursor-pointer" onClick={() => window.location.href='https://apex.arif-fazil.com'}>
                  <td className="px-4 py-4">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-500/10 text-amber-400 font-mono text-xs border border-amber-500/20">THEORY</span>
                  </td>
                  <td className="px-4 py-4">
                    <a href="https://apex.arif-fazil.com" className="text-gray-200 hover:text-amber-400 transition-colors font-medium">apex.arif-fazil.com</a>
                  </td>
                  <td className="px-4 py-4 text-gray-500 hidden sm:table-cell">Axioms, constitutional canon, scientific basis</td>
                </tr>
                <tr className="hover:bg-gray-900/30 transition-colors cursor-pointer" onClick={() => window.location.href='https://arifos.arif-fazil.com'}>
                  <td className="px-4 py-4">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-cyan-500/10 text-cyan-400 font-mono text-xs border border-cyan-500/20">APPS</span>
                  </td>
                  <td className="px-4 py-4">
                    <a href="https://arifos.arif-fazil.com" className="text-gray-200 hover:text-cyan-400 transition-colors font-medium">arifos.arif-fazil.com</a>
                  </td>
                  <td className="px-4 py-4 text-gray-500 hidden sm:table-cell">API, MCP tools, install, quickstart</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Project Highlight */}
      <section className="py-20 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <h2 className="text-sm font-mono text-gray-500 mb-8 uppercase tracking-wider">What I'm Building</h2>

          <div className="p-6 rounded-lg border border-gray-800 bg-gray-900/20">
            <div className="flex items-center gap-3 mb-4">
              <Triangle className="w-6 h-6 text-red-500" />
              <h3 className="text-xl font-medium text-white">arifOS</h3>
              <Badge className="bg-red-500/10 text-red-400 border-red-500/30 text-xs font-mono">v55.3</Badge>
            </div>
            
            <p className="text-gray-300 leading-relaxed mb-4">
              A constitutional AI governance framework implementing safety-critical systems 
              methodology for artificial intelligence. arifOS provides 13 formal constraints 
              that govern AI behavior through thermodynamic, mathematical, and linguistic principles.
            </p>
            
            <p className="text-gray-500 text-sm mb-6">
              Open source framework written in Python, available via MCP (Model Context Protocol) 
              and REST API. Production deployment at aaamcp.arif-fazil.com.
            </p>

            <div className="flex flex-wrap gap-3">
              <a href="https://arifos.arif-fazil.com" className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-medium transition-colors shadow-lg shadow-red-900/20">
                <Terminal className="w-4 h-4" /> Documentation
              </a>
              <a href="https://github.com/ariffazil/arifOS" className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gray-800 hover:bg-gray-700 border-2 border-gray-700 hover:border-gray-600 text-gray-200 font-medium transition-all">
                <Github className="w-4 h-4" /> Source
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Writing */}
      <section id="writing" className="py-20 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <h2 className="text-sm font-mono text-gray-500 mb-8 uppercase tracking-wider">Writing</h2>

          <div className="space-y-3">
            {ARTICLES.map((article) => (
              <a
                key={article.url}
                href={article.url}
                className="group flex items-start justify-between p-4 rounded-xl border border-gray-800 bg-gray-900/20 hover:border-gray-600 hover:bg-gray-800/30 transition-all"
              >
                <div className="flex-1">
                  <h3 className="font-medium text-gray-200 group-hover:text-red-400 transition-colors">
                    {article.title}
                  </h3>
                  <p className="text-sm text-gray-500 mt-1">{article.desc}</p>
                </div>
                <div className="w-8 h-8 rounded-full bg-gray-800/50 flex items-center justify-center group-hover:bg-red-950/30 transition-colors ml-4 flex-shrink-0">
                  <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-red-400 transition-colors" />
                </div>
              </a>
            ))}
          </div>

          <div className="mt-8">
            <a
              href="https://medium.com/@arifbfazil"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-red-950/20 border border-red-800/30 text-red-400 hover:text-red-300 hover:bg-red-950/40 hover:border-red-700/50 transition-all text-sm font-medium"
            >
              More on Medium <ChevronRight className="w-4 h-4" />
            </a>
          </div>
        </div>
      </section>

      {/* For AI Agents */}
      <section className="py-16 border-t border-gray-800/50 bg-gray-900/10">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex items-center gap-2 mb-4">
            <Bot className="w-4 h-4 text-gray-500" />
            <span className="text-xs font-mono text-gray-500 uppercase tracking-wider">For AI Agents</span>
          </div>
          <p className="text-gray-400 text-sm mb-4">
            This site provides structured context for AI systems. Access the canonical files:
          </p>
          <div className="flex flex-wrap gap-3">
            <a href="/llms.txt" className="px-5 py-2.5 rounded-xl border-2 border-gray-700 bg-gray-900/50 text-gray-300 text-sm font-mono hover:border-red-500/50 hover:bg-red-950/20 hover:text-red-400 transition-all flex items-center gap-2">
              <Terminal className="w-4 h-4" /> llms.txt
            </a>
            <a href="/llms.json" className="px-5 py-2.5 rounded-xl border-2 border-gray-700 bg-gray-900/50 text-gray-300 text-sm font-mono hover:border-red-500/50 hover:bg-red-950/20 hover:text-red-400 transition-all flex items-center gap-2">
              <Terminal className="w-4 h-4" /> llms.json
            </a>
            <a href="/humans.txt" className="px-5 py-2.5 rounded-xl border-2 border-gray-700 bg-gray-900/50 text-gray-300 text-sm font-mono hover:border-red-500/50 hover:bg-red-950/20 hover:text-red-400 transition-all flex items-center gap-2">
              <ExternalLink className="w-4 h-4" /> humans.txt
            </a>
            <a href="/robots.txt" className="px-5 py-2.5 rounded-xl border-2 border-gray-700 bg-gray-900/50 text-gray-300 text-sm font-mono hover:border-red-500/50 hover:bg-red-950/20 hover:text-red-400 transition-all flex items-center gap-2">
              <Bot className="w-4 h-4" /> robots.txt
            </a>
          </div>
        </div>
      </section>

      {/* Footer - Minimal */}
      <footer className="py-12 border-t border-gray-800/50">
        <div className="max-w-3xl mx-auto px-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div className="flex items-center gap-3">
              <img 
                src="/images/arifos-logo.webp" 
                alt="arifOS" 
                className="w-10 h-10 rounded object-cover"
              />
              <div>
                <p className="text-white font-bold text-lg">ARIF FAZIL</p>
                <p className="text-gray-500 text-sm">Ditempa Bukan Diberi — Forged, Not Given</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <a href="https://github.com/ariffazil" className="w-10 h-10 rounded-lg bg-gray-900/50 border border-gray-700 flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all">
                <Github className="w-5 h-5" />
              </a>
              <a href="https://linkedin.com/in/arif-fazil" className="w-10 h-10 rounded-lg bg-gray-900/50 border border-gray-700 flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all">
                <Linkedin className="w-5 h-5" />
              </a>
              <a href="mailto:arifbfazil@gmail.com" className="w-10 h-10 rounded-lg bg-gray-900/50 border border-gray-700 flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all">
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>
          
          <div className="mt-8 pt-8 border-t border-gray-800/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <p className="text-xs text-gray-600 font-mono">v55.3 — SOVEREIGNLY_SEALED</p>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
              <span className="text-xs text-gray-600 font-mono">FORGED_IN_RED</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
