import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import './TriWitnessRadar.css';

interface TriWitnessRadarProps {
  human: number;
  ai: number;
  earth: number;
}

const TriWitnessRadar: React.FC<TriWitnessRadarProps> = ({ human, ai, earth }) => {
  const data = [
    { subject: 'Human', value: human * 100, fullMark: 100 },
    { subject: 'AI', value: ai * 100, fullMark: 100 },
    { subject: 'Earth', value: earth * 100, fullMark: 100 },
  ];
  return (
    <div className="tri-witness-radar glass-card">
      <div className="viz-header">
        <h3 className="viz-title">Tri-Witness Consensus (W₃)</h3>
      </div>
      
      <div className="radar-container">
        <ResponsiveContainer width="100%" height={260}>
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid stroke="rgba(255,255,255,0.1)" />
            <PolarAngleAxis 
              dataKey="subject" 
              tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 10 }}
            />
            <PolarRadiusAxis 
              angle={30} 
              domain={[0, 100]} 
              tick={false} 
              axisLine={false}
            />
            <Radar
              name="Consensus"
              dataKey="value"
              stroke="var(--neon-cyan)"
              fill="var(--neon-cyan)"
              fillOpacity={0.3}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      <div className="radar-legend">
        <div className="legend-item">
          <span className="dot dot-human"></span>
          <span className="label">Human</span>
        </div>
        <div className="legend-item">
          <span className="dot dot-ai"></span>
          <span className="label">AI</span>
        </div>
        <div className="legend-item">
          <span className="dot dot-earth"></span>
          <span className="label">Earth</span>
        </div>
      </div>
    </div>
  );
};

export default TriWitnessRadar;
