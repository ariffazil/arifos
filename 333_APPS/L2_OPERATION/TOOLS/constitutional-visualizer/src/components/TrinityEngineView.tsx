import React from 'react';
import './TrinityEngineView.css';

interface TrinityEngineViewProps {
  mindStatus?: 'ACTIVE' | 'IDLE' | 'ERROR';
  heartStatus?: 'ACTIVE' | 'IDLE' | 'ERROR';
  soulStatus?: 'ACTIVE' | 'IDLE' | 'ERROR';
}

const TrinityEngineView: React.FC<TrinityEngineViewProps> = ({
  mindStatus = 'ACTIVE',
  heartStatus = 'ACTIVE',
  soulStatus = 'ACTIVE',
}) => {
  return (
    <div className="trinity-view">
      <div className={`engine-node mind ${mindStatus.toLowerCase()}`}>
        <div className="engine-icon">Δ</div>
        <div className="engine-details">
          <span className="engine-name">MIND</span>
          <span className="engine-status">{mindStatus}</span>
        </div>
      </div>
      <div className={`engine-node heart ${heartStatus.toLowerCase()}`}>
        <div className="engine-icon">Ω</div>
        <div className="engine-details">
          <span className="engine-name">HEART</span>
          <span className="engine-status">{heartStatus}</span>
        </div>
      </div>
      <div className={`engine-node soul ${soulStatus.toLowerCase()}`}>
        <div className="engine-icon">Ψ</div>
        <div className="engine-details">
          <span className="engine-name">SOUL</span>
          <span className="engine-status">{soulStatus}</span>
        </div>
      </div>
    </div>
  );
};

export default TrinityEngineView;
