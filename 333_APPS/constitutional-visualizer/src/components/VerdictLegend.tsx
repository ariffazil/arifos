import React from 'react';
import './VerdictLegend.css';

const verdicts = [
  { type: 'SEAL', label: 'SEALED', color: 'verdict-seal', desc: 'Immutable ledger entry. Decision ratified.' },
  { type: 'SABAR', label: 'SABAR', color: 'verdict-sabar', desc: 'Hold for further context or time threshold.' },
  { type: 'VOID', label: 'VOID', color: 'verdict-void', desc: 'Constitutional violation. Execution blocked.' },
  { type: '888_HOLD', label: '888_HOLD', color: 'verdict-hold', desc: 'Awaiting Sovereign manual ratification.' },
];

const VerdictLegend: React.FC = () => {
  return (
    <div className="verdict-legend">
      <h3>Verdict Glossary</h3>
      <div className="legend-items">
        {verdicts.map(v => (
          <div key={v.type} className="legend-item">
            <span className={`verdict-badge ${v.color}`}>{v.label}</span>
            <span className="verdict-desc">{v.desc}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VerdictLegend;
