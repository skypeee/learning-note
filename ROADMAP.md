# 飞控系统工程师学习路线

> 目标：2年内成长为嵌入式高级开发工程师（无人机/飞控方向）
> 当前阶段：SITL 后期 → HIL 前期

## 总体进度

| 阶段 | 进度 | 状态 | 完成时间 |
|------|------|------|----------|
| SITL | ████████░░ 80% | 进行中 | 预计 2026-06 |
| HIL  | ░░░░░░░░░░ 0%  | 未开始 | - |
| 真机 | ░░░░░░░░░░ 0%  | 未开始 | - |

## 模块进度（粗粒度）

| 模块 | 进度 | 状态 | 笔记 |
|------|------|------|------|
| 程序入口/HAL | ✅ 完成 | 已掌握 | [notes/topics/hal/](./notes/topics/hal/) |
| Scheduler | ✅ 完成 | 已掌握 | [notes/topics/scheduler/](./notes/topics/scheduler/) |
| EKF | ████░░░░░░ 40% | 精读中 | [notes/topics/ekf/](./notes/topics/ekf/) |
| MAVLink | █████░░░░░ 50% | 实验中 | [notes/topics/mavlink/](./notes/topics/mavlink/) |
| AP_Peripheral | ██░░░░░░░░ 20% | 初探 | - |

## 关键知识点（细粒度追踪）

### HAL / 程序入口
- [x] HAL 生成 main() 机制
- [x] setup/loop 生命周期驱动模型

### Scheduler
- [x] AP_Scheduler 调度模型
- [x] FAST_TASK vs SCHED_TASK 区别
- [x] priority 对实时性的影响
- [x] delay/busy loop 对链路的影响

### EKF
- [x] EKF3 架构定位
- [x] GPS 数据入口 readGpsData
- [x] AP_GPS → EKF 调用链
- [ ] innovation / testRatio 公式推导
- [ ] FuseVelPosNED 融合逻辑
- [ ] GPS Glitch 检测机制
- [ ] 破坏性实验验证（跳变/抖动/停更）

### MAVLink
- [x] 基础协议理解
- [x] 自定义 MAVLink 消息实践
- [ ] 高频通信压力测试

## 英语学习

| 阶段 | 进度 | 状态 | 开始时间 |
|------|------|------|----------|
| 词汇重建（2000 词） | █░░░░░░░░░ ~0.35% | 已启动 | 2026-04-18 |
| 阅读恢复 | ░░░░░░░░░░ 0% | 未开始 | - |
| 听力启动 | ░░░░░░░░░░ 0% | 未开始 | - |
| 口语跟读 | ░░░░░░░░░░ 0% | 未开始 | - |

### 阅读记录
- [x] 《七王国的骑士》第1段（7 生词）
- [x] 《七王国的骑士》第2段（6 生词）
