# 飞控系统工程师学习笔记

> 3年目标：产品技术专家 / 独立技术创业者（2026 → 2029）
> 当前阶段：全栈开发 + 产品规划 + 飞控储备

## 工作三维模型

| 维度 | 定位 | 当前重点 |
|------|------|---------|
| **A. 真机测试** | 有板就测，随时响应 | WebSocket→OpenHD 丢包排查 + 长连接断推验证 |
| **B. 产品规划** | 长线推进，持续思考 | 安全无人机云平台 PRD 细化 + Shadow Device 嵌入式云平台规划 |
| **C. 开发** | 主线输出，深度时间 | drone-web-console 从 Vue3 迁移到 React Native（跨平台 iOS/移动端） |

> 优先级：A（有板时）> C > B > 学习。学习融入工作，不是独立轨道。

## 快速导航

- [**任务池**](./TASKS.md) — 三维工作模型下的统一任务入口
- [**每周计划**](./assessment/weekly-plan.md) — 滚动 2 周排期
- [**技能矩阵**](./assessment/skills.md) — 各方向掌握情况评估
- [**间隔复习**](./assessment/review-tracker.md) — 知识点 Ebbinghaus 曲线复习追踪
- [**微知识卡片**](./micro-cards/skill-concepts.md) — 产品思维/工程方法论/AI 工作流碎片学习
- [**英语词汇**](./english/vocabulary.md) — 词汇学习记录
- [**Demo 作品集**](./demos/) — 实验代码项目

## 项目

| 项目 | 状态 | 技术栈 | 详情 |
|------|------|--------|------|
| 安全无人机云平台 | 开发中 | Vue3 → React Native + Python 后端 + OpenHD + MAVLink | [PRD v1.1](./docs/安防无人机PRD-v1.md) · [架构文档](./docs/architecture.md) · [竞品分析](./docs/竞品分析报告.md) |
| Shadow Device 嵌入式云平台 | 规划中 | 待定 | 通用嵌入式设备管理平台 |
| EKF / 飞控储备 | 精读中 | ArduPilot（已有）→ PX4（转向） | [ArduPilot 笔记](./ArduPilot/) |

## 目录结构

```
├── TASKS.md                  # 统一任务池（A/B/C 三维度）
├── CLAUDE.md                 # AI 工具协作规范
├── assessment/               # 评估与计划
│   ├── weekly-plan.md        # 每周计划（滚动 2 周）
│   ├── skills.md             # 技能矩阵
│   └── review-tracker.md     # 间隔复习追踪
├── docs/                     # 项目文档
│   ├── 安防无人机PRD-v1.md   # 安全无人机 PRD
│   ├── 竞品分析报告.md       # 大疆/道通/极飞对比
│   └── architecture.md       # 安全无人机系统架构
├── micro-cards/              # 微知识卡片（碎片学习）
├── english/                  # 英语学习
│   └── vocabulary.md         # 词汇记录
├── demos/                    # 实验代码
│   ├── react-core-demo/      # React 核心概念 Demo
│   ├── socratic-bot/         # 苏格拉底式飞书机器人
│   └── progress-report.html  # 进度汇报 PPT
├── cloud-platform/           # 云平台基础设施（Docker Compose）
├── ArduPilot/                # ArduPilot 源码分析笔记（Legacy）
├── notes/topics/             # 按主题的学习笔记
└── life/                     # 生活记录
```
