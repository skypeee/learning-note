# 学习笔记仓库改造设计文档

> 日期：2026-04-17
> 状态：待实现

## 目标
将 `learning-note` 仓库改造为结构化的学习管理平台，包含学习笔记、进度追踪、能力评估、Demo作品集，并提供 SKILL.md 让多个 AI 工具都能读取统一背景。

## 目录结构

```
learning-note/
├── README.md                  # 项目入口，个人简介 + 快速导航
├── ROADMAP.md                 # 总进度看板（粗粒度模块进度 + 细粒度关键点）
├── SKILL.md                   # AI 工具共享 Skill 规范
├── notes/
│   ├── timeline/              # 按日期的学习笔记（YYYY-MM-DD.md）
│   └── topics/                # 按主题的系统笔记
│       ├── _index.md          # 主题索引 + 各主题完成度
│       └── <topic>/
│           ├── _meta.md       # 主题进度（知识点清单）
│           └── <NN-title>.md  # 具体笔记
├── demos/
│   ├── sitl/                  # SITL 阶段作品
│   ├── hil/                   # HIL 阶段作品
│   └── flight/                # 真机阶段作品
├── assessment/
│   ├── skills.md              # 技能维度评估表
│   └── milestones.md          # 阶段里程碑评估
└── reviews/                   # 间隔复习索引
    └── _index.md
```

## 设计要点

### 1. 双维度笔记
- **时间线**（`notes/timeline/`）：按日期归档，用于间隔复习节奏
- **主题线**（`notes/topics/`）：按知识体系组织，用于系统学习和查漏补缺

### 2. 双粒度进度追踪
- **粗粒度**：`ROADMAP.md` 按模块标记进度（如 EKF 40%、MAVLink 50%）
- **细粒度**：每个主题 `_meta.md` 列出知识点清单，逐条标记状态（未读/已读/已验证/已掌握）

### 3. 能力评估体系
- **技能维度**（`assessment/skills.md`）：6 级评定（零基础/入门/实践/熟练/精通），附证据和更新时间
- **阶段里程碑**（`assessment/milestones.md`）：按 Level 1→2→3 阶段，列出标准和完成状态

### 4. Demo 作品集
- 按学习阶段分目录（sitl/hil/flight）
- 每个 demo 自包含：README + code/ + results/ + notes.md
- README 固定模板：目的、日期、环境、结论

### 5. SKILL.md
- 统一背景规范，所有 AI 工具读取后自动对齐角色和约束
- 内容：个人背景、优势、短板、对 AI 的要求

### 6. 间隔复习（reviews/）
- `_index.md` 记录各笔记的复习状态和下次复习时间
