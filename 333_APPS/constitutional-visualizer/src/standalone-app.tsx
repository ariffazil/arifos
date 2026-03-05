import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

const StandaloneApp = () => {
  const [sessionData, setSessionData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Poll the arifOS HTTP REST API
    const fetchGovernanceStatus = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/governance-status');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.status === 'success' && data.data) {
          setSessionData(data.data);
          setError(null);
        } else {
          setError(data.error || 'Unknown error from /api/governance-status');
        }
      } catch (err: any) {
        console.error('Failed to fetch governance status:', err);
        setError(err.message || String(err));
      }
    };

    fetchGovernanceStatus();
    const intervalId = setInterval(fetchGovernanceStatus, 2000); // Poll every 2 seconds

    return () => clearInterval(intervalId);
  }, []);

  return <App initialSession={sessionData} mcpApp={null} error={error} />;
};

const root = createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <StandaloneApp />
  </React.StrictMode>
);
