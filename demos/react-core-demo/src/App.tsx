import { useState, useEffect } from 'react';
import DeviceCard from './components/DeviceCard';

interface Device {
  id: string;
  name: string;
  status: 'online' | 'offline';
  battery: number;
}

export default function App() {
  // 1. useState: List of devices (Global state for the panel)
  const [devices, setDevices] = useState<Device[]>([
    { id: 'dev-001', name: '无人机 Alpha', status: 'online', battery: 80 },
    { id: 'dev-002', name: '地面站 Beta', status: 'offline', battery: 45 },
  ]);

  // 2. useEffect: Simulate WebSocket Heartbeat (Charging logic)
  useEffect(() => {
    console.log('⚡ WebSocket connected. Starting heartbeat...');
    const interval = setInterval(() => {
      setDevices(prevDevices => 
        prevDevices.map(d => ({
          ...d,
          battery: Math.min(100, d.battery + 2) // Simulate charging +2% every 3s
        }))
      );
    }, 3000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  const addDevice = () => {
    const id = `dev-${Math.floor(Math.random() * 1000)}`;
    setDevices([...devices, { id, name: `新设备 ${id}`, status: 'online', battery: 100 }]);
  };

  return (
    <div style={{ padding: '24px', fontFamily: 'system-ui, sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <header style={{ marginBottom: '24px', borderBottom: '2px solid #333', paddingBottom: '16px' }}>
        <h1 style={{ margin: 0 }}>🛰️ IoT 设备控制面板</h1>
        <p style={{ color: '#666' }}>React Core Demo: Props, State, Effects</p>
      </header>

      <button onClick={addDevice} style={{ 
        padding: '10px 20px', fontSize: '16px', marginBottom: '24px', cursor: 'pointer',
        background: '#3182ce', color: 'white', border: 'none', borderRadius: '4px'
      }}>
        + 添加模拟设备
      </button>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '16px' }}>
        {devices.map(device => (
          <DeviceCard 
            key={device.id}
            deviceId={device.id}
            name={device.name}
            initialStatus={device.status}
            initialBattery={device.battery}
          />
        ))}
      </div>
      
      <p style={{ marginTop: '32px', fontSize: '12px', color: '#999' }}>
        💡 提示：打开浏览器控制台 (F12) 查看 useEffect 的日志输出。
      </p>
    </div>
  );
}
