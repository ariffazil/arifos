import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './VitalityMonitor.css';

interface VitalityMonitorProps {
  data: Array<{ time: string; value: number }>;
}

const VitalityMonitor: React.FC<VitalityMonitorProps> = ({ data }) => {
  return (
    <div className="vitality-monitor glass-card">
      <div className="viz-header">
        <h3 className="viz-title">Thermodynamic Vitality (Ψ)</h3>
        <div className="live-indicator">
          <span className="pulse-dot"></span>
          LIVE_STREAM
        </div>
      </div>
      
      <div className="viz-container">
        <ResponsiveContainer width="100%" height={200}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis 
              dataKey="time" 
              hide={true}
            />
            <YAxis 
              domain={[0, 2.5]} 
              stroke="rgba(255,255,255,0.3)" 
              fontSize={10}
              tickFormatter={(val) => val.toFixed(1)}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                fontSize: '12px',
                color: '#fff'
              }}
              itemStyle={{ color: '#60a5fa' }}
            />
            <Area 
              type="monotone" 
              dataKey="value" 
              stroke="#3b82f6" 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#colorValue)" 
              animationDuration={500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="viz-footer">
        <div className="metric-status">
          <span className="label">Entropy State:</span>
          <span className="value color-blue">STABLE</span>
        </div>
        <div className="metric-status">
          <span className="label">ZRAM Usage:</span>
          <span className="value">14.2%</span>
        </div>
      </div>
    </div>
  );
};

export default VitalityMonitor;
