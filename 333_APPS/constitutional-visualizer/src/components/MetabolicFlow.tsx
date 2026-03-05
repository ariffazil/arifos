import React from 'react';
import './MetabolicFlow.css';

interface MetabolicFlowProps {
  currentStage: number; // e.g., 0, 111, 444, 555, 666, 777, 888, 999
}

const stages = [
  { id: 0, label: 'INIT', desc: 'Airlock' },
  { id: 111, label: 'AGI', desc: 'Mind' },
  { id: 444, label: 'RECALL', desc: 'Context' },
  { id: 555, label: 'ASI', desc: 'Heart' },
  { id: 777, label: 'APEX', desc: 'Soul' },
  { id: 888, label: 'FORGE', desc: 'Hands' },
  { id: 999, label: 'VAULT', desc: 'Memory' },
];

const MetabolicFlow: React.FC<MetabolicFlowProps> = ({ currentStage }) => {
  return (
    <div className="metabolic-flow-container">
      <div className="pipeline">
        {stages.map((stage, index) => {
          const isActive = currentStage >= stage.id;
          const isCurrent = currentStage === stage.id;
          
          return (
            <React.Fragment key={stage.id}>
              <div className={`stage-node ${isActive ? 'active' : ''} ${isCurrent ? 'current' : ''}`}>
                <div className="node-circle">
                  <span className="node-id">{stage.id}</span>
                </div>
                <div className="node-info">
                  <span className="node-label">{stage.label}</span>
                  <span className="node-desc">{stage.desc}</span>
                </div>
              </div>
              {index < stages.length - 1 && (
                <div className={`stage-connector ${currentStage > stage.id ? 'active' : ''}`}>
                  <div className="connector-line"></div>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default MetabolicFlow;
