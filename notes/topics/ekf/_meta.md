# EKF 主题进度

> 状态：精读中 | 开始：2026-04-10 | 预计完成：2026-05-15

## 知识点清单

| 知识点 | 状态 | 关联笔记 | 验证方式 |
|--------|------|----------|----------|
| EKF3 架构定位 | ✅ 已掌握 | [00-architecture](./00-architecture.md) | 能画出调用图 |
| GPS 数据入口 readGpsData | ✅ 已掌握 | [01-gps-fusion](./01-gps-fusion.md) | 能说出完整调用链 |
| AP_GPS → EKF 数据结构 | 📖 已读 | [01-gps-fusion](./01-gps-fusion.md) | gps_elements 结构体 |
| innovation 计算逻辑 | 📖 已读 | | 能说清 EKF/innovation/testRatio 关系 |
| testRatio 与 gating | 📖 已读 | | 理解归一化和拒绝逻辑 |
| FuseVelPosNED 融合函数 | ⬜ 未读 | | |
| GPS Glitch 检测 | ⬜ 未读 | | |
| 破坏性实验（跳变/抖动/停更） | ⬜ 未实验 | | Lua/SITL 验证 |

## 状态说明
- ⬜ 未读
- 📖 已读（看过代码/笔记）
- 🔬 已验证（做过实验或能推导）
- ✅ 已掌握（能不看资料口述 + 能回答追问）
