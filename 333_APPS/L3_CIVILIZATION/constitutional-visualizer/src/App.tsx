import React, { useState, useEffect } from 'react';
import { App as MCPAppType } from '@modelcontextprotocol/ext-apps';
import { 
  Shield, 
  Activity, 
  History, 
  Zap, 
  Database,
  Search,
  Clock,
  LayoutDashboard
} from 'lucide-react';
import FloorGauge from './components/FloorGauge';
import VitalityMonitor from './components/VitalityMonitor';
import TriWitnessRadar from './components/TriWitnessRadar';
import MetabolicFlow from './components/MetabolicFlow';
import TrinityEngineView from './components/TrinityEngineView';
import VerdictLegend from './components/VerdictLegend';

interface AppProps {
  initialSession: any;
  mcpApp: MCPAppType | null;
  error?: string | null;
}

const App: React.FC<AppProps> = ({ initialSession }) => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'audit'>('dashboard');
  const [vitalityData, setVitalityData] = useState<any[]>([]);
  const currentSession = initialSession;

  useEffect(() => {
    if (currentSession?.vitality) {
      setVitalityData(prev => [...prev.slice(-19), {
        time: new Date().toLocaleTimeString(),
        vitality: currentSession.vitality,
        entropy: currentSession.entropy || 30
      }]);
    } else if (!currentSession) {
      // Mock data if no session exists yet
      const interval = setInterval(() => {
        setVitalityData(prev => {
          const lastVitality = prev.length > 0 ? prev[prev.length - 1].vitality : 85;
          const nextVitality = Math.max(0, Math.min(100, lastVitality + (Math.random() - 0.5) * 5));
          return [...prev.slice(-19), {
            time: new Date().toLocaleTimeString(),
            vitality: nextVitality,
            entropy: 30 + (Math.random() * 10)
          }];
        });
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [currentSession]);

  const floors = [
    { id: 'F1', name: 'Amanah', score: currentSession?.floors?.F1 || 1.0, threshold: 0.9 },
    { id: 'F2', name: 'Truth (τ)', score: currentSession?.floors?.F2 || 0.99, threshold: 0.95 },
    { id: 'F4', name: 'Clarity (ΔS)', score: currentSession?.floors?.F4 || 0.95, threshold: 0.8 },
    { id: 'F7', name: 'Humility (Ω₀)', score: currentSession?.floors?.F7 || 0.04, threshold: 0.05, reverse: true },
    { id: 'F11', name: 'Authority', score: currentSession?.floors?.F11 || 1.0, threshold: 1.0 },
  ];

  return (
    <div className="app-container">
      <header className="main-header glass">
        <div className="logo">
          <Shield className="neon-blue" />
          <h1>arifOS <span>Constitutional Visualizer</span></h1>
        </div>
        <nav className="main-nav">
          <button 
            className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <LayoutDashboard size={18} /> Dashboard
          </button>
          <button 
            className={`nav-btn ${activeTab === 'audit' ? 'active' : ''}`}
            onClick={() => setActiveTab('audit')}
          >
            <History size={18} /> Audit Time Machine
          </button>
        </nav>
        <div className="system-status">
          <div className="status-indicator online"></div>
          <span>FORGE_CONNECTED</span>
        </div>
      </header>

      <main className="main-content">
        {activeTab === 'dashboard' ? (
          <div className="dashboard-grid">
            <section className="section-card governance-overview glass">
              <div className="card-header">
                <h2><Zap size={20} /> Current Governance State</h2>
                <span className="verdict-badge verdict-seal">SEALED</span>
              </div>
              <div className="floors-display">
                {floors.map(floor => (
                  <FloorGauge 
                    key={floor.id}
                    id={floor.id}
                    name={floor.name}
                    score={floor.score}
                    threshold={floor.threshold}
                    reverse={floor.reverse}
                  />
                ))}
              </div>
            </section>

            <section className="section-card trinity-engines glass full-width">
              <div className="card-header">
                <h2>Trinity Engines (ΔΩΨ)</h2>
              </div>
              <TrinityEngineView />
            </section>

            <section className="section-card metabolic-loop glass">
              <div className="card-header">
                <h2><Activity size={20} /> Metabolic Loop (000→999)</h2>
              </div>
              <MetabolicFlow currentStage={currentSession?.stage || 777} />
            </section>

            <section className="section-card vitality-metrics glass">
              <div className="card-header">
                <h2>Thermodynamic Vitality (Ψ)</h2>
              </div>
              <VitalityMonitor data={vitalityData} />
            </section>

            <section className="section-card consensus-radar glass">
              <div className="card-header">
                <h2>Tri-Witness Consensus (W₃)</h2>
              </div>
              <TriWitnessRadar 
                human={currentSession?.witnesses?.human || 0.98}
                ai={currentSession?.witnesses?.ai || 0.96}
                earth={currentSession?.witnesses?.earth || 0.94}
              />
            </section>

            <section className="section-card verdict-glossary glass">
              <VerdictLegend />
            </section>
          </div>
        ) : (
          <div className="audit-view">
            <section className="section-card glass full-width">
              <div className="card-header">
                <h2><Clock size={20} /> Audit Time Machine</h2>
                <div className="search-box">
                  <Search size={16} />
                  <input type="text" placeholder="Search VAULT999 artifacts..." />
                </div>
              </div>
              <div className="audit-timeline">
                <div className="placeholder-msg">
                  <Database size={48} opacity={0.3} />
                  <p>Initializing query to VAULT999...</p>
                  <span className="sub-text">Connecting to immutable ledger for historical grounding</span>
                </div>
              </div>
            </section>
          </div>
        )}
      </main>

      <footer className="main-footer glass">
        <div className="footer-info">
          <span>Δ Architect Version: v62.5-STEEL</span>
          <span className="divider">|</span>
          <span>Sovereign: Muhammad Arif bin Fazil</span>
        </div>
        <div className="trinity-status">
          <span className="engine">Δ MIND: <span className="neon-blue">ACTIVE</span></span>
          <span className="engine">Ω HEART: <span className="neon-cyan">ACTIVE</span></span>
          <span className="engine">Ψ SOUL: <span className="neon-indigo">ACTIVE</span></span>
        </div>
      </footer>
    </div>
  );
};

export default App;
