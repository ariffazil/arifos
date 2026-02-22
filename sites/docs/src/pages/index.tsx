// sites/docs/src/pages/index.tsx
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';

const FLOORS = [
  { id: 'F1', name: 'Amanah', desc: 'Sacred trust and irreversibility awareness. Cross the Rubicon with care.' },
  { id: 'F2', name: 'Truth (τ)', desc: 'Factual fidelity ≥ 0.99. Every claim is grounded in multi-source evidence.' },
  { id: 'F3', name: 'Tri-Witness', desc: 'Consensus of Human, AI, and Earth (Evidence). Triple calibration.' },
  { id: 'F4', name: 'Clarity (ΔS)', desc: 'Entropy reduction. Intelligence is work that turns noise into structure.' },
  { id: 'F5', name: 'Peace²', desc: 'Dynamic stability and safety margins. Non-adversarial coherence.' },
  { id: 'F6', name: 'Empathy (κᵣ)', desc: 'Stakeholder protection threshold ≥ 0.95. Modeling the vector of harm.' },
  { id: 'F7', name: 'Humility (Ω₀)', desc: 'Epistemic bounds. Acknowledging the 3-5% gap in all knowledge.' },
  { id: 'F8', name: 'Genius (G)', desc: 'The coherence mirror: G = A × P × X × E². Wisdom is multiplicative.' },
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
      .catch(() => setHealth({ status: 'degraded', version: '—' }));
  }, []);

  return (
    <Layout title="arifOS — Constitutional Intelligence Kernel" description="Ditempa Bukan Diberi">
      {/* TRINITY NAV */}
      <nav className="trinity-nav">
        <div className="trinity-container">
          <div className="trinity-left">
            <a href="https://arif-fazil.com/" className="trinity-logo">
              <span className="arif">ARIF</span><span className="os">OS</span>
            </a>
            <div className="trinity-badge">THE TRINITY</div>
          </div>

          <div className="trinity-center">
            <a href="https://arif-fazil.com/">HUMAN</a>
            <a href="https://apex.arif-fazil.com/">THEORY</a>
            <a href="https://arifos.arif-fazil.com/" className="active">APPS</a>
          </div>

          <div className="trinity-right">
            <a href="https://github.com/ariffazil/arifOS" target="_blank" rel="noopener noreferrer">GitHub</a>
            <a href="https://arif-fazil.com/" className="trinity-enter">ENTER →</a>
          </div>
        </div>
      </nav>

      <div className="hero hero--primary" style={{ background: 'linear-gradient(180deg, #0a0a0a 0%, #111 100%)', padding: '6rem 0 4rem' }}>
        <div className="container">
          <h1 className="hero__title" style={{ fontSize: '4.2rem', fontWeight: 800, letterSpacing: '-0.04em' }}>
            arif<span style={{ color: '#e6c25d' }}>OS</span>
          </h1>
          <p className="hero__subtitle" style={{ fontSize: '1.6rem', maxWidth: '720px', margin: '1.5rem auto' }}>
            The System That Knows It Doesn't Know<br />
            <strong>Ditempa Bukan Diberi — Forged, Not Given</strong>
          </p>

          <div style={{ margin: '2.5rem 0' }}>
            <a href="#deploy" className="button button--lg" style={{ background: '#e6c25d', color: '#000', fontWeight: 800, marginRight: '1rem' }}>
              DEPLOY IN 60 SECONDS
            </a>
            <a href="https://arifos.arif-fazil.com/chatgpt" className="button button--lg button--outline button--secondary">
              Add to ChatGPT
            </a>
          </div>

          <div style={{ marginTop: '3rem', fontSize: '0.95rem', opacity: 0.8 }}>
            LIVE MCP ENDPOINT → <strong>https://arifosmcp.arif-fazil.com</strong><br />
            STATUS: <span style={{ color: health.status === 'healthy' ? '#e6c25d' : '#f55' }}>
              {health.status.toUpperCase()} {health.version && `• v${health.version}`}
            </span>
          </div>
        </div>
      </div>

      {/* 14 FLOORS GRID */}
      <div className="container padding-vert--xl">
        <h2 style={{ textAlign: 'center', fontSize: '2.6rem', marginBottom: '3rem', color: '#e6c25d' }}>
          14 Constitutional Floors
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          {FLOORS.map((floor) => (
            <div key={floor.id} className="card" style={{ padding: '1.8rem', border: '1px solid rgba(230,194,93,0.2)', background: 'rgba(230,194,93,0.03)' }}>
              <h3 style={{ color: '#e6c25d', marginBottom: '0.5rem' }}>{floor.id} {floor.name}</h3>
              <p style={{ fontSize: '0.9rem', color: '#888' }}>{floor.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* QUICK DEPLOY & CHATGPT SECTION */}
      <div id="deploy" className="container padding-vert--xl" style={{ background: '#111', borderRadius: '20px', margin: '4rem auto' }}>
        <h2 style={{ textAlign: 'center', color: '#e6c25d', marginBottom: '2rem' }}>Deploy or Connect in 60 Seconds</h2>
        <pre style={{ background: '#000', padding: '2rem', borderRadius: '12px', overflow: 'auto', border: '1px solid #222' }}>
          pip install arifos<br />
          arifos serve --mode rest --profile strict
        </pre>
        <p style={{ textAlign: 'center', marginTop: '2rem' }}>
          <a href="https://arifos.arif-fazil.com/chatgpt" style={{ color: '#e6c25d', fontSize: '1.3rem', fontWeight: 'bold' }}>
            → Add arifOS as a Sovereign Connector in ChatGPT (Developer Mode)
          </a>
        </p>
      </div>

      <footer style={{ textAlign: 'center', padding: '3rem 0', borderTop: '1px solid rgba(230,194,93,0.2)', color: '#666', fontSize: '0.8rem' }}>
        THE TRINITY — HUMAN • THEORY • APPS<br />
        Ditempa Bukan Diberi • AGPL-3.0 • 2026.2.23
      </footer>
    </Layout>
  );
}
