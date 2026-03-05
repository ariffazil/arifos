import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { App as McpAppSdk } from "@modelcontextprotocol/ext-apps";
import App from './App';
import './index.css';

const mcpAppSdk = new McpAppSdk({
  id: "constitutional-visualizer",
  name: "arifOS Constitutional Visualizer",
  icon: "ui-card"
});

const McpAppWrapper = () => {
  const [sessionData, setSessionData] = useState<any>(null);

  useEffect(() => {
    const initMcp = async () => {
      await mcpAppSdk.connect();

      // Set up listener for live updates
      mcpAppSdk.ontoolresult = (result) => {
        if (result.name === 'apex_judge' || result.name === 'metabolic_loop') {
          try {
            const data = JSON.parse(result.output);
            setSessionData(data);
          } catch (e) {
            console.error("Error parsing tool result", e);
          }
        }
      };

      // Fetch initial state
      try {
        const history = await mcpAppSdk.callServerTool({
          name: "recall_memory",
          arguments: { limit: 1 }
        }) as any;
        
        if (history && Array.isArray(history) && history.length > 0) {
          setSessionData(history[0]);
        }
      } catch (error) {
        console.error("Failed to fetch initial session data:", error);
      }
    };

    initMcp();
  }, []);

  return <App initialSession={sessionData} mcpApp={mcpAppSdk} error={null} />;
};

const root = createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <McpAppWrapper />
  </React.StrictMode>
);
