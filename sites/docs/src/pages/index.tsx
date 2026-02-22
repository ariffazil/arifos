import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

// Floor definitions for arifOS v65.0-FORGE
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

function HealthIndicator() {
  const [status, setStatus] = useState('FETCHING');

  useEffect(() => {
    fetch('https://arifosmcp.arif-fazil.com/health')
      .then(res => res.json())
      .then(data => setStatus(data.status.toUpperCase()))
      .catch(() => setStatus('OFFLINE'));
  }, []);

  const color = status === 'HEALTHY' ? '#00ff88' : status === 'DEGRADED' ? '#ffeb3b' : '#ff3e3e';

  return (
    <div className="healthWidget" style={{ borderColor: `${color}33`, color }}>
      <div className="healthDot" style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }}></div>
      <span>SYSTEM STATUS: {status}</span>
    </div>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  
  return (
    <Layout
      title={`Sovereign Intelligence | ${siteConfig.title}`}
      description="Constitutional intelligence kernel that governs AI cognition via 13+1 floors and a 000→999 metabolic pipeline.">
      
      <main>
        {/* HERO SECTION */}
        <section className="heroBanner">
          <div className="container">
            <h1 className="heroTitle">arifOS</h1>
            <p className="heroSubtitle">
              The first production-grade constitutional governance system for AGI-scale intelligence. 
              <strong> Forged, not given.</strong>
            </p>
            
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <Link className="button ctaButton" to="/intro">
                Ignite Discovery
              </Link>
              <Link className="button button--outline button--lg" style={{ color: '#fff', borderColor: '#333' }} to="/mcp-server">
                Connect MCP
              </Link>
            </div>

            <HealthIndicator />
            
            <div className="installBox">
              <span className="installCommand">$ gemini install arifos --server=aaa-mcp</span>
              <button 
                className="button button--link" 
                onClick={() => navigator.clipboard.writeText('gemini install arifos --server=aaa-mcp')}
                style={{ color: '#888' }}
              >
                Copy
              </button>
            </div>
          </div>
        </section>

        {/* 14 FLOORS SECTION */}
        <section style={{ padding: '6rem 0', background: '#070707' }}>
          <div className="container">
            <h2 style={{ textAlign: 'center', marginBottom: '4rem', fontSize: '2.5rem' }}>
              The 14 Floors of Governance
            </h2>
            
            <div className="floorsGrid">
              {FLOORS.map((floor) => (
                <div key={floor.id} className="floorCard">
                  <div className="floorNumber">{floor.id}</div>
                  <div className="floorName">{floor.name}</div>
                  <div className="floorDescription">{floor.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* TRINITY SECTION */}
        <section style={{ padding: '6rem 0', background: '#000', borderTop: '1px solid #111' }}>
          <div className="container">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '3rem' }}>
              <div>
                <h3 style={{ color: '#fff', fontSize: '1.5rem', marginBottom: '1rem' }}>Δ Mind (Architect)</h3>
                <p style={{ color: '#888' }}>Cognition, mapping, and truth-seeking. Stages 111–333. Reduces entropy via agi_reason.</p>
              </div>
              <div>
                <h3 style={{ color: '#fff', fontSize: '1.5rem', marginBottom: '1rem' }}>Ω Heart (Guardian)</h3>
                <p style={{ color: '#888' }}>Safety, empathy, and stakeholder protection. Stages 555–666. Enforces κᵣ thresholds.</p>
              </div>
              <div>
                <h3 style={{ color: '#fff', fontSize: '1.5rem', marginBottom: '1rem' }}>Ψ Soul (Judge)</h3>
                <p style={{ color: '#888' }}>Final judgment and consensus. Stages 888–999. Issues SEAL or VOID verdicts.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
