import { useState, useEffect } from 'react';

interface DeviceProps {
  deviceId: string;
  name: string;
  initialStatus: 'online' | 'offline';
  initialBattery: number;
  onCharge?: () => void; // Callback for charging effect
}

export default function DeviceCard({ 
  deviceId, name, initialStatus, initialBattery, onCharge 
}: DeviceProps) {
  // 1. useState: Local state for this specific device card
  const [status, setStatus] = useState<'online' | 'offline'>(initialStatus);
  const [battery, setBattery] = useState(initialBattery);

  // 2. useEffect: Side effect - Log status changes and trigger external charge logic
  useEffect(() => {
    console.log(`[Device ${deviceId}] Status changed to: ${status}`);
    if (onCharge) onCharge();
  }, [status]);

  // 3. useEffect: Side effect - Watch battery level
  useEffect(() => {
    if (battery < 20) {
      console.warn(`[Device ${deviceId}] Low battery warning!`);
    }
  }, [battery]);

  const toggleStatus = () => setStatus(s => s === 'online' ? 'offline' : 'online');
  const drainBattery = () => setBattery(b => Math.max(0, b - 10));

  // 4. JSX: UI definition
  return (
    <div style={{
      border: '1px solid #ddd', padding: '16px', borderRadius: '8px',
      background: status === 'online' ? '#f0fff4' : '#fff5f5',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{ margin: '0 0 8px' }}>{name}</h3>
      <p>ID: <code>{deviceId}</code></p>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
        <span style={{ 
          padding: '2px 8px', borderRadius: '12px', fontSize: '12px',
          background: status === 'online' ? '#48bb78' : '#f56565', color: 'white' 
        }}>
          {status === 'online' ? '🟢 在线' : '🔴 离线'}
        </span>
        <span>⚡ {battery}%</span>
      </div>

      <div style={{ display: 'flex', gap: '8px' }}>
        <button onClick={toggleStatus} style={{ cursor: 'pointer' }}>
          {status === 'online' ? '断开连接' : '重连'}
        </button>
        <button onClick={drainBattery} style={{ cursor: 'pointer' }}>
          耗电模拟 (-10%)
        </button>
      </div>
    </div>
  );
}
