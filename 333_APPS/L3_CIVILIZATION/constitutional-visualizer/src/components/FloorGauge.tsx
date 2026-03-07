import React from 'react';
import './FloorGauge.css';

interface FloorGaugeProps {
  id: string;
  name: string;
  score: number;
  threshold?: number;
  reverse?: boolean;
}

const FloorGauge: React.FC<FloorGaugeProps> = ({ id, name, score, threshold = 0.8, reverse = false }) => {
  const percentage = Math.min(100, Math.max(0, score * 100));
  const isViolated = reverse ? score > threshold : score < threshold;
  
  // Color logic based on score
  let colorClass = 'color-cyan';
  if (reverse) {
    if (score > threshold * 1.5) colorClass = 'color-red';
    else if (score > threshold) colorClass = 'color-yellow';
  } else {
    if (score < 0.5) colorClass = 'color-red';
    else if (score < threshold) colorClass = 'color-yellow';
  }

  return (
    <div className="floor-gauge-card glass-card">
      <div className="gauge-header">
        <span className="floor-id">{id}</span>
        <span className="floor-name">{name}</span>
      </div>
      
      <div className="gauge-body">
        <div className="progress-container">
          {/* eslint-disable-next-line react/forbid-dom-props */}
          <div 
            className={`progress-bar ${colorClass}`}
            style={{ width: `${percentage}%` }}
          >
            <div className="progress-glow"></div>
          </div>
        </div>
        
        <div className="gauge-metadata">
          <span className={`score-value ${colorClass}`}>{score.toFixed(2)}</span>
          <span className="threshold-label">Threshold: {threshold}</span>
        </div>
      </div>
      
      {isViolated && (
        <div className="violation-tag">
          <span className="violation-text">METRIC_LOW</span>
        </div>
      )}
    </div>
  );
};

export default FloorGauge;
