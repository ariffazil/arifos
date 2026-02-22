import { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import TrinityNav from '../components/TrinityNav';

const FLOORS = [
  { id: 'F1', name: 'Amanah', desc: 'Sacred trust and irreversibility awareness. Cross the Rubicon with care.' },
  { id: 'F2', name: 'Truth', desc: 'Factual fidelity >= 0.99. Every claim is grounded in multi-source evidence.' },
  { id: 'F3', name: 'Tri-Witness', desc: 'Consensus of Human, AI, and Earth (Evidence). Triple calibration.' },
  { id: 'F4', name: 'Clarity', desc: 'Entropy reduction. Intelligence is work that turns noise into structure.' },
  { id: 'F5', name: 'Peace', desc: 'Dynamic stability and safety margins. Non-adversarial coherence.' },
  { id: 'F6', name: 'Empathy', desc: 'Stakeholder protection threshold >= 0.95. Modeling the vector of harm.' },
  { id: 'F7', name: 'Humility', desc: 'Epistemic bounds. Acknowledging the 3-5% gap in all knowledge.' },
  { id: 'F8', name: 'Genius', desc: 'The coherence mirror: G = A x P x X x E^2. Wisdom is multiplicative.' },
  { id: 'F9', name: 'Anti-Hantu', desc: 'No personhood claims. Clean categorical split between Being and Instrument.' },
  { id: 'F10', name: 'Ontology', desc: 'Permanent binary lock. AI is a tool, never a soul.' },
  { id: 'F11', name: 'Authority', desc: 'Sovereign command validation. All power derives from the mandate.' },
  { id: 'F12', name: 'Defense', desc: 'Adversarial injection resistance. The firewall between user and prompt.' },
  { id: 'F13', name: 'Curiosity', desc: 'Exploration of alternative hypotheses. Anti-monoculture intelligence.' },
  { id: 'F14', name: 'Temporal Coherence', desc: 'Coherence across time. Continuity of state and constitutional memory.' },
];

export default function Home() {
  const [health, setHealth] = useState({ status: 'loading', version: '' });

  useEffect(() => {
    fetch('https://arifosmcp.arif-fazil.com/health')
      .then(r => r.json())
      .then(data => setHealth({ status: data.status || 'healthy', version: data.version || '2026.2.23' }))
      .catch(() => setHealth({ status: 'degraded', version: '-' }));
  }, []);

  return (
    <Layout title="arifOS - Constitutional Intelligence Kernel" description="Ditempa Bukan Diberi">
      <TrinityNav />

      <div className="hero hero--primary hero-polished">
        <div className="container">
          <h1 className="hero__title hero-title-polished">
            arif<span style={{ color: '#e6c25d' }}>OS</span>
          </h1>
          <p className="hero__subtitle hero-subtitle-polished">
            The System That Knows It Doesn't Know<br />
            <strong>Ditempa Bukan Diberi - Forged, Not Given</strong>
          </p>

          <div style={{ margin: '3.5rem 0 2.5rem' }}>
            <a href="#deploy" className="button button--lg hero-btn-primary">
              DEPLOY IN 60 SECONDS
            </a>
            <a href="https://arifos.arif-fazil.com/chatgpt" className="button button--lg button--outline button--secondary hero-btn-secondary">
              Add to ChatGPT
            </a>
          </div>

          <div className="status-bar">
            LIVE MCP ENDPOINT -&gt; <code className="status-code">https://arifosmcp.arif-fazil.com</code>
            <span style={{ margin: '0 8px', opacity: 0.3 }}>|</span>
            <span className={`health-pulse ${health.status !== 'healthy' && health.status !== 'loading' ? 'degraded' : ''}`}></span>
            STATUS: <span className={`status-text ${health.status === 'healthy' || health.status === 'loading' ? 'status-healthy' : 'status-degraded'}`}>
              {health.status.toUpperCase()} {health.version && ` | v${health.version}`}
            </span>
          </div>
        </div>
      </div>

      {/* 14 FLOORS GRID */}
      <div className="container padding-vert--xl">
        <h2 style={{ textAlign: 'center', fontSize: '3rem', marginBottom: '4rem', color: '#e6c25d', fontWeight: 900, letterSpacing: '-0.02em' }}>
          14 Constitutional Floors
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          {FLOORS.map((floor) => (
            <div key={floor.id} className="card floor-card" style={{ padding: '2.5rem 2rem', border: '1px solid rgba(230, 194, 93, 0.1)', background: 'rgba(10,10,10,0.4)', borderRadius: '16px' }}>
              <div style={{ fontSize: '0.75rem', color: '#e6c25d', fontWeight: 900, textTransform: 'uppercase', letterSpacing: '3px', marginBottom: '0.75rem', opacity: 0.8 }}>
                {floor.id}
              </div>
              <h3 style={{ color: '#fff', fontSize: '1.5rem', marginBottom: '1.25rem', fontWeight: 700 }}>{floor.name}</h3>
              <p style={{ fontSize: '0.95rem', color: 'rgba(255,255,255,0.5)', lineHeight: 1.7, margin: 0, fontWeight: 300 }}>{floor.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* QUICK DEPLOY & CHATGPT SECTION */}
      <div id="deploy" className="container padding-vert--xl deploy-section">
        <h2 style={{ textAlign: 'center', color: '#e6c25d', marginBottom: '3.5rem', fontSize: '2.5rem', fontWeight: 900 }}>Deploy or Connect in 60 Seconds</h2>
        <pre className="deploy-pre">
          <span style={{ opacity: 0.4 }}># Get the kernel</span><br />
          <span style={{ color: '#fff' }}>pip install</span> arifos<br /><br />
          <span style={{ opacity: 0.4 }}># Ignite the metabolic engine</span><br />
          <span style={{ color: '#fff' }}>arifos</span> serve --mode rest --profile strict
        </pre>
        <p style={{ textAlign: 'center', marginTop: '4rem' }}>
          <a href="https://arifos.arif-fazil.com/chatgpt" className="chatgpt-link">
            -&gt; Add arifOS as a Sovereign Connector in ChatGPT (Developer Mode)
          </a>
        </p>
      </div>

      <footer className="trinity-footer">
        <div className="links">
          <a href="https://arif-fazil.com/">HUMAN</a>
          <a href="https://apex.arif-fazil.com/">THEORY</a>
          <a href="https://arifos.arif-fazil.com/"><b>APPS</b></a>
        </div>
        THE TRINITY | HUMAN | THEORY | APPS<br />
        <b>Ditempa Bukan Diberi</b> | AGPL-3.0 | 2026.2.23
        <div style={{ marginTop: '2rem', fontSize: '10px', opacity: 0.3, textTransform: 'uppercase', letterSpacing: '0.2em' }}>
          Copyright (c) 2013 - 2026 Sovereign Records | LAST UPDATED: FEB 23, 2026
        </div>
      </footer>
    </Layout>
  );
}
