import { useEffect, useState } from 'react';
import { Activity, Server, Cpu, Database, Shield, Zap, Users, Brain, AlertCircle, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

interface ServerStatus {
  name: string;
  port: number;
  status: 'healthy' | 'degraded' | 'failed' | 'unknown';
  latency: number;
  last_check: string;
}

interface ContainerStatus {
  id: string;
  name: string;
  status: string;
  state: string;
  uptime: string;
}

interface SystemMetrics {
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  load_avg: number[];
}

interface AggregatorHealth {
  status: string;
  timestamp: string;
  servers_total: number;
  servers_healthy: number;
  containers_total: number;
  containers_running: number;
  constitutional_metrics?: {
    truth: number;
    empathy: number;
    vitality: number;
    clarity: number;
    floor_scores: Record<string, number>;
  };
}

export function MonitoringDashboard() {
  const [health, setHealth] = useState<AggregatorHealth | null>(null);
  const [servers, setServers] = useState<ServerStatus[]>([]);
  const [containers, setContainers] = useState<ContainerStatus[]>([]);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [wsConnected, setWsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string>('');

  const fetchData = async () => {
    try {
      const [healthRes, serversRes, containersRes, metricsRes] = await Promise.all([
        fetch('/api/health'),
        fetch('/api/servers'),
        fetch('/api/containers'),
        fetch('/api/system'),
      ]);
      if (healthRes.ok) setHealth(await healthRes.json());
      if (serversRes.ok) setServers(await serversRes.json());
      if (containersRes.ok) setContainers(await containersRes.json());
      if (metricsRes.ok) setMetrics(await metricsRes.json());
    } catch (error) {
      console.error('Failed to fetch monitoring data', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const ws = new WebSocket(`ws://${window.location.host}/api/ws`);
    ws.onopen = () => {
      setWsConnected(true);
      console.log('WebSocket connected');
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'update') {
        setLastUpdate(new Date().toLocaleTimeString());
        if (data.payload) {
          // Update specific data based on payload type
          if (data.payload.servers) setServers(data.payload.servers);
          if (data.payload.containers) setContainers(data.payload.containers);
          if (data.payload.metrics) setMetrics(data.payload.metrics);
        }
      }
    };
    ws.onclose = () => {
      setWsConnected(false);
      console.log('WebSocket disconnected');
    };
    return () => ws.close();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'degraded': return <AlertCircle className="w-4 h-4 text-amber-400" />;
      case 'failed': return <XCircle className="w-4 h-4 text-red-400" />;
      default: return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'degraded': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'failed': return 'bg-red-500/20 text-red-400 border-red-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const formatLatency = (ms: number) => {
    if (ms < 100) return `${ms.toFixed(0)}ms`;
    if (ms < 1000) return `${ms.toFixed(1)}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading monitoring data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">arifOS Live Monitoring Dashboard</h2>
          <p className="text-gray-400">Real-time health of 22 servers, 9 containers, and constitutional metrics</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
            <span className="text-sm text-gray-400">WebSocket {wsConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
          <Button variant="outline" size="sm" onClick={fetchData} className="flex items-center gap-2">
            <RefreshCw className="w-3 h-3" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Overall Health Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gray-900/30 border-gray-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Servers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{health?.servers_healthy ?? 0}/{health?.servers_total ?? 0}</div>
                <p className="text-xs text-gray-500">Healthy / Total</p>
              </div>
              <Server className="w-8 h-8 text-cyan-400" />
            </div>
          </CardContent>
        </Card>
        <Card className="bg-gray-900/30 border-gray-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Containers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{health?.containers_running ?? 0}/{health?.containers_total ?? 0}</div>
                <p className="text-xs text-gray-500">Running / Total</p>
              </div>
              <Database className="w-8 h-8 text-cyan-400" />
            </div>
          </CardContent>
        </Card>
        <Card className="bg-gray-900/30 border-gray-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">System Load</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{metrics?.cpu_percent ? `${metrics.cpu_percent.toFixed(1)}%` : 'N/A'}</div>
                <p className="text-xs text-gray-500">CPU Usage</p>
              </div>
              <Cpu className="w-8 h-8 text-cyan-400" />
            </div>
          </CardContent>
        </Card>
        <Card className="bg-gray-900/30 border-gray-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-400">Constitutional Health</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">
                  {health?.constitutional_metrics ? 'Active' : 'N/A'}
                </div>
                <p className="text-xs text-gray-500">Floors Enforced</p>
              </div>
              <Shield className="w-8 h-8 text-cyan-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Server Status Grid */}
      <Card className="bg-gray-900/30 border-gray-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Server className="w-5 h-5" />
            Server Status (22 Services)
          </CardTitle>
          <CardDescription>Real-time health checks of all infrastructure services</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
            {servers.slice(0, 22).map((server) => (
              <div key={server.name} className={`p-3 rounded-lg border ${getStatusColor(server.status)}`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(server.status)}
                    <span className="text-sm font-medium truncate">{server.name}</span>
                  </div>
                  <Badge variant="outline" className="text-xs">{server.port}</Badge>
                </div>
                <div className="text-xs text-gray-400">Latency: {formatLatency(server.latency)}</div>
                <div className="text-xs text-gray-500">Last checked: {new Date(server.last_check).toLocaleTimeString()}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Container Health */}
      <Card className="bg-gray-900/30 border-gray-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5" />
            Docker Containers (9 Services)
          </CardTitle>
          <CardDescription>Status of containerized services with start/stop controls</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {containers.map((container) => (
              <div key={container.id} className="p-4 rounded-lg border border-gray-800 bg-gray-900/50">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${container.state === 'running' ? 'bg-green-400' : 'bg-red-400'}`} />
                    <span className="font-medium truncate">{container.name}</span>
                  </div>
                  <Badge className={container.state === 'running' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}>
                    {container.state}
                  </Badge>
                </div>
                <div className="text-sm text-gray-400 mb-2">ID: {container.id.slice(0, 12)}</div>
                <div className="text-xs text-gray-500">Uptime: {container.uptime}</div>
                <div className="flex gap-2 mt-4">
                  <Button size="sm" variant="outline" className="flex-1" disabled={container.state === 'running'}>
                    Start
                  </Button>
                  <Button size="sm" variant="outline" className="flex-1" disabled={container.state !== 'running'}>
                    Stop
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* System Metrics */}
      {metrics && (
        <Card className="bg-gray-900/30 border-gray-800">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Cpu className="w-5 h-5" />
              System Resources
            </CardTitle>
            <CardDescription>CPU, memory, disk, and load averages from netdata</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-lg border border-gray-800 bg-gray-900/50">
                <div className="flex items-center gap-2 mb-2">
                  <Cpu className="w-4 h-4 text-cyan-400" />
                  <span className="text-sm font-medium">CPU</span>
                </div>
                <div className="text-2xl font-bold text-white">{metrics.cpu_percent.toFixed(1)}%</div>
                <div className="h-2 bg-gray-800 rounded-full mt-2 overflow-hidden">
                  <div 
                    className="h-full bg-cyan-500" 
                    style={{ width: `${Math.min(metrics.cpu_percent, 100)}%` }}
                  />
                </div>
              </div>
              <div className="p-4 rounded-lg border border-gray-800 bg-gray-900/50">
                <div className="flex items-center gap-2 mb-2">
                  <Brain className="w-4 h-4 text-cyan-400" />
                  <span className="text-sm font-medium">Memory</span>
                </div>
                <div className="text-2xl font-bold text-white">{metrics.memory_percent.toFixed(1)}%</div>
                <div className="h-2 bg-gray-800 rounded-full mt-2 overflow-hidden">
                  <div 
                    className="h-full bg-cyan-500" 
                    style={{ width: `${Math.min(metrics.memory_percent, 100)}%` }}
                  />
                </div>
              </div>
              <div className="p-4 rounded-lg border border-gray-800 bg-gray-900/50">
                <div className="flex items-center gap-2 mb-2">
                  <Database className="w-4 h-4 text-cyan-400" />
                  <span className="text-sm font-medium">Disk</span>
                </div>
                <div className="text-2xl font-bold text-white">{metrics.disk_percent.toFixed(1)}%</div>
                <div className="h-2 bg-gray-800 rounded-full mt-2 overflow-hidden">
                  <div 
                    className="h-full bg-cyan-500" 
                    style={{ width: `${Math.min(metrics.disk_percent, 100)}%` }}
                  />
                </div>
              </div>
              <div className="p-4 rounded-lg border border-gray-800 bg-gray-900/50">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="w-4 h-4 text-cyan-400" />
                  <span className="text-sm font-medium">Load Avg</span>
                </div>
                <div className="text-2xl font-bold text-white">{metrics.load_avg[0].toFixed(2)}</div>
                <div className="text-xs text-gray-400 mt-1">
                  1m: {metrics.load_avg[0].toFixed(2)} | 5m: {metrics.load_avg[1].toFixed(2)} | 15m: {metrics.load_avg[2].toFixed(2)}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Constitutional Metrics Placeholder */}
      <Card className="bg-gray-900/30 border-gray-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Constitutional Metrics (τ, κᵣ, Ψ, ΔS)
          </CardTitle>
          <CardDescription>Real-time floor scores from arifOS AAA-MCP engine</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            <Shield className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>Constitutional metrics collection in progress. Integration with AAA-MCP engine pending.</p>
            <p className="text-sm mt-2">Endpoints: /metrics (MCP), /health (REST), /self_diagnose</p>
          </div>
        </CardContent>
      </Card>

      {/* Footer */}
      <div className="text-center text-xs text-gray-500 pt-4 border-t border-gray-800/30">
        <p>Dashboard last updated: {lastUpdate || new Date().toLocaleTimeString()}</p>
        <p className="mt-1">Data sourced from 22 servers, netdata (port 19999), uptime-kuma (port 3001), and Docker engine</p>
      </div>
    </div>
  );
}