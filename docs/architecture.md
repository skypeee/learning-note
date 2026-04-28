# 安全无人机系统 — 架构说明文档

> 版本：v1.0 | 更新时间：2026-04-25

---

## 一、系统总览

```
┌─────────────────────────────────────────────────────────────────┐
│                        安全无人机系统                            │
├──────────────┬──────────────────────┬──────────────────────────┤
│  drone-web   │  drone-control       │  drone-mobile            │
│  console     │  backend             │  (React Native)          │
│  (Vue 3)     │  (Python)            │  (Expo)                  │
├──────────────┼──────────────────────┼──────────────────────────┤
│ 桌面控制台   │ 板端服务 (OBC)       │ 移动端 App               │
│ 遥测/控制    │ 遥测广播/命令转发    │ 遥测/控制                │
│ 航点规划     │ MAVLink 解析         │ 视频流 (Phase 2)         │
│ WHEP 视频    │ OpenHD 配置          │ 地图 (Phase 2)           │
│ 链路监控     │ 心跳保活             │ 链路监控                 │
└──────┬───────┴──────────┬───────────┴──────────────┬───────────┘
       │                  │                          │
       │     WebSocket    │     MAVLink/UDP           │
       │     WHEP/HTTP    │                          │
       └────────┬─────────┘──────────┬───────────────┘
                │                    │
       ┌────────▼────────┐   ┌───────▼──────────────┐
       │  MediaMTX       │   │  mavlink-routerd      │
       │  (:8889)        │   │  (UDP 14550/14553)    │
       │                 │   │                       │
       │  WHEP Video     │   │  OpenHD ↔ FC          │
       │  (H.264/VP8)    │   │  (飞控链路)            │
       └─────────────────┘   └───────────────────────┘
```

---

## 二、项目仓库结构

```
my-project/
├── drone-web-console/       # Web 控制台 (lihe-ty/drone-web-console)
│   ├── src/
│   │   ├── composables/     # Vue 组合式函数
│   │   │   ├── useCloudBridge.ts   # WebSocket 遥测+命令
│   │   │   └── useWHEPPlayer.ts    # WHEP 视频播放
│   │   ├── components/      # UI 组件
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── views/           # 页面路由
│   │   └── config/          # 视频/连接配置
│   └── package.json
│
├── drone-control-backend/   # 板端服务 (lihe-ty/drone-control-backend)
│   └── backend/
│       ├── board_server.py  # 主入口 (WebSocket + MAVLink)
│       ├── config.py        # 配置 (端口/固件类型)
│       ├── firmware_adapter/# 固件适配层 (PX4/ArduPilot)
│       ├── mavlink_parser.py# MAVLink 原始数据解析
│       ├── commander.py     # MAVLink 命令发送器
│       └── telemetry.py     # 遥测状态模型
│
└── drone-mobile/            # 移动端 App (lihe-ty/drone-mobile)
    ├── src/
    │   ├── types/protocol.ts   # 共享协议类型定义
    │   ├── store/droneStore.ts # Zustand 状态管理
    │   └── hooks/useCloudBridge.ts # WebSocket Hook
    ├── App.tsx                # 主界面 (深色仪表盘)
    └── app.json               # Expo 配置
```

---

## 三、数据流架构

### 3.1 遥测数据上行（飞控 → 前端）

```
飞控 (Flight Controller)
    │
    ▼  MAVLink 串口/USB
OpenHD Air → OpenHD Ground (数字图传链路)
    │
    ▼  UDP 14550
mavlink-routerd (MAVLink 路由)
    │
    ├──▶ UDP 14553 ──▶ board_server.py (解析 + TelemetryState)
    │                      │
    │                      ▼  WebSocket 广播 (10Hz, 端口 8765)
    │                 ┌─────────────────┐
    │                 │  Web Console    │  ← useCloudBridge 接收
    │                 │  Mobile App     │  ← useCloudBridge 接收
    │                 └─────────────────┘
    │
    └──▶ UDP 14550 ──▶ board_server → pymavlink (命令回传)
```

### 3.2 视频流（独立通道）

```
摄像头 → 编码器 → MediaMTX (:8889)
                        │
                        ▼  WHEP (WebRTC over HTTP)
                   ┌─────────────┐
                   │ Web Console │  ← useWHEPPlayer.ts
                   └─────────────┘
                   Mobile App    │  ← react-native-webrtc (Phase 2)
```

### 3.3 控制指令下行（前端 → 飞控）

```
Web Console / Mobile App
    │
    ▼  WebSocket (端口 8765)
board_server.py
    │
    ▼  pymavlink → UDP 14550
mavlink-routerd
    │
    ▼  OpenHD Ground → OpenHD Air
飞控 (Flight Controller)
```

---

## 四、通信协议

### 4.1 WebSocket 消息格式

所有 WebSocket 通信均通过 `ws://<board-ip>:8765`。

| 消息类型 | 方向 | 格式 |
|---------|------|------|
| `telemetry` | 后端 → 前端 | `{ "type": "telemetry", "drone_id": "drone-001", "data": { TelemetryState } }` |
| `command` | 前端 → 后端 | `{ "type": "command", "drone_id": "drone-001", "command": "takeoff", "params": { "altitude": 10 } }` |
| `command-result` | 后端 → 前端 | `{ "type": "command-result", "command": "takeoff", "result": { "success": true } }` |
| `openhd_config` | 前端 → 后端 | `{ "type": "openhd_config", "command": "set-link", "params": { "frequency": 5800 } }` |
| `config_result` | 后端 → 前端 | `{ "type": "config_result", "command": "set-link", "success": true, "message": "Sent 3 param(s)" }` |
| `status` | 后端 → 前端 | `{ "type": "status", "message": "Board connected" }` |

### 4.2 支持的控制命令

| 命令 | 参数 | 固件适配 |
|------|------|---------|
| `arm` | `{ force?: boolean }` | PX4/ArduPilot |
| `disarm` | — | PX4/ArduPilot |
| `takeoff` | `{ altitude: number }` | PX4→OFFBOARD, ArduPilot→GUIDED |
| `land` | — | PX4/ArduPilot |
| `rtl` | — | PX4/ArduPilot |
| `loiter` | — | PX4/ArduPilot |
| `set_mode` | `{ mode: string }` | PX4/ArduPilot 模式映射 |
| `goto` | `{ lat, lng, alt }` | PX4/ArduPilot |
| `set_home` | `{ lat, lng, alt }` | PX4/ArduPilot |
| `upload_mission` | `{ waypoints: [...] }` | PX4/ArduPilot |
| `start_mission` | — | PX4/ArduPilot |
| `clear_mission` | — | PX4/ArduPilot |
| `mission_status` | — | PX4/ArduPilot |
| `set_speed` | `{ speed: number }` | PX4/ArduPilot |
| `change_altitude` | `{ altitude: number }` | PX4/ArduPilot |

---

## 五、技术栈

### 5.1 drone-web-console

| 层级 | 技术 |
|------|------|
| 框架 | Vue 3 (Composition API, `<script setup>`) |
| 构建 | Vite 7 |
| 语言 | TypeScript 5.9 |
| 状态 | Pinia 3 |
| 路由 | Vue Router 5 |
| UI | Element Plus 2 |
| 地图 | Leaflet 1.9 + Esri 卫星图 |
| 视频 | WHEP (MediaMTX) |
| 实时通信 | WebSocket (`useCloudBridge`) |

### 5.2 drone-control-backend

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.x |
| WebSocket | `websockets` (asyncio) |
| MAVLink | `pymavlink` + 自定义解析器 |
| 固件适配 | Adapter 模式 (PX4 / ArduPilot) |
| 视频 | MediaMTX (独立进程, WHEP 协议) |
| 图传链路 | OpenHD (数字图传系统) |

### 5.3 drone-mobile

| 层级 | 技术 |
|------|------|
| 框架 | React Native (Expo SDK 52+) |
| 语言 | TypeScript |
| 状态 | Zustand 5 |
| 路由 | Expo Router (文件系统路由) |
| 实时通信 | WebSocket (内置) |
| 视频 | `react-native-webrtc` (Phase 2) |
| 地图 | `@rnmapbox/maps` (Phase 2) |

---

## 六、部署架构

### 6.1 板端 (OBC)

```
Raspberry Pi / Jetson Nano (机载计算机)
├── board_server.py          # 端口 8765 (WebSocket)
├── MediaMTX                 # 端口 8889 (WHEP)
├── mavlink-routerd          # UDP 14550/14553
└── OpenHD Ground            # 数字图传地面端
```

### 6.2 客户端

| 客户端 | 部署方式 | 访问地址 |
|--------|---------|---------|
| Web Console | Vite 静态文件 (Nginx/Docker) | `http://<ip>:5173` |
| Mobile App | APK / IPA 安装 | 直连 `ws://<board-ip>:8765` |

---

## 七、协议类型定义

核心共享类型（`src/types/protocol.ts`），双端共用：

```typescript
interface TelemetryState {
  // 位置
  lat: number; lng: number; alt: number;
  // 速度/姿态
  speed: number; heading: number;
  pitch: number; roll: number; climb: number;
  // GPS
  gps_fix_type: number; satellites: number;
  // 电池
  battery_voltage: number; battery_current: number; battery_remaining: number;
  // 状态
  armed: boolean; flight_mode: string;
  gcs_connection_lost: boolean;
  pre_flight_checks_pass: boolean; ready_to_arm: boolean;
  // 链路
  ohd: OpenHDState;
}
```

---

## 八、开发规范

### 8.1 分支策略

| 分支 | 用途 |
|------|------|
| `main` | 稳定分支，可部署 |
| `fix/*` | 缺陷修复 |
| `feat/*` | 新功能开发 |
| `docs/*` | 文档更新 |

### 8.2 提交规范

```
<type>: <description>

type: feat | fix | docs | chore | refactor
```

示例：
```
fix: make subscribeOnConnect configurable, default false
feat: add waypoint mission planning panel
docs: update architecture diagram
```

---

## 九、已知问题与注意事项

### 9.1 Chrome mDNS 隐私

Chrome 会将局域网 IP 替换为 `.local` 域名，导致 WHEP 视频连接失败。

**解决**：`chrome://flags/#enable-webrtc-hide-local-ips-with-mdns` → Disabled

### 9.2 Safari 视频兼容性

Safari 仅支持 H.264 编码，MediaMTX 默认推 VP8 会导致黑屏。

**解决**：MediaMTX 配置推流端使用 H.264，前端加 SDP munge 强制 H.264 协商。

### 9.3 固件模式差异

| 操作 | PX4 | ArduPilot |
|------|-----|-----------|
| 起飞模式 | OFFBOARD | GUIDED |
| 模式 ID | MAVLink 标准格式 | 左移 16 位自定义映射 |
| 航点 seq=0 | HOME 点 | HOME 点 |

---

## 十、快速开始

### 10.1 Web 控制台

```bash
cd drone-web-console
npm install
npm run dev          # http://localhost:5173
```

### 10.2 板端服务

```bash
cd drone-control-backend
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=. python -m backend.board_server
```

### 10.3 移动端

```bash
cd drone-mobile
npm install
npx expo start       # Expo Go 扫码开发

# 本地编译 APK
npx expo prebuild --platform android
cd android && ./gradlew assembleDebug
```
