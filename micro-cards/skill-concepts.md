# 微知识卡片 — 全 Skill 核心理念提取

> 适合遛狗/碎片时间刷。每张卡片 3-5 句话，一个概念。
> 最后更新：2026-04-22
> 分类：产品思维 | 工程方法论 | 设计原则 | AI 工作流 | 架构与系统

---

## 📦 产品思维 (PM Skills)

### Card 001 — 用户故事 3C + INVEST
**来源**: `pm-skills/user-stories`

写用户故事的标准格式：
- **3C**: Card（一句话描述）、Conversation（讨论细节）、Confirmation（验收条件）
- **INVEST**: Independent、Negotiable、Valuable、Estimable、Small、Testable
- 反面教材："作为一个用户，我想用一个好用的系统" → 不可测试、不具体
- **C++类比**: 3C ≈ 函数声明 + 设计文档 + 单元测试

### Card 002 — Job Story 格式
**来源**: `pm-skills/job-stories`

比用户故事更好的格式：
- 格式：`When [情境]，I want to [动机]，so I can [预期结果]`
- 例子：`When 电量低于20%，I want to 自动规划最近降落点，so I can 避免坠机`
- 优势：聚焦**情境触发**而非抽象角色，天然适合嵌入式/自动化场景
- **与用户故事区别**: User Story = "谁要什么"，Job Story = "什么情况下触发什么需求"

### Card 003 — Opportunity Score（机会评分）
**来源**: `pm-skills/prioritize-features`

Dan Olsen 的公式：`Opportunity = Importance × (1 − Satisfaction)`
- 重要性高 + 满意度低 = 最佳机会
- 核心原则：**优先解决问题（problems），不要先想方案（solutions）**
- 你的 A 项目画圈巡飞功能就是高 Importance × 低 Satisfaction 的典型

### Card 004 — RICE 优先级框架
**来源**: `pm-skills/prioritization-frameworks`

`RICE = Reach × Impact × Confidence ÷ Effort`
- **Reach**（覆盖人数）: 多少用户/设备会用到
- **Impact**（影响程度）: 0.25=极小, 3=巨大
- **Confidence**（信心）: 100%=确定, 50%=猜的
- **Effort**（工作量）: 人月
- **用法**: 给任务池里每个 P0/P1 打分，排序后砍掉最低分的

### Card 005 — North Star Metric（北极星指标）
**来源**: `pm-skills/north-star-metric`

一个产品只应该有一个北极星指标：
- 定义：最能反映用户从产品中获得核心价值的**单一指标**
- 三个游戏类型：Attention（注意力）、Transaction（交易）、Productivity（效率）
- 安防无人机 → 可能是 "每周成功完成的自主巡检次数"
- 配套 3-5 个输入指标：设备在线率、任务成功率、用户活跃度

### Card 006 — Growth Loops（增长飞轮）
**来源**: `pm-skills/growth-loops`

5 种增长飞轮：
1. **Viral**: 用户邀请用户（Dropbox 分享得空间）
2. **Usage**: 用得越多产品越好用（Waze 用户越多路线越准）
3. **Collaboration**: 协作带来新用户（Google Docs 分享编辑）
4. **User-Generated Content**: 用户生产内容吸引用户（YouTube）
5. **Referral**: 推荐奖励（Uber 邀请码）
- **你的场景**: 安防无人机 → Usage Loop（飞行数据越多 AI 识别越准 → 用户更依赖）

### Card 007 — Pre-Mortem（事前验尸）
**来源**: `pm-skills/pre-mortem`

假设产品已经**失败**了，然后倒推原因：
- **Tigers（真老虎）**: 真实存在的致命风险 → 必须解决
- **Paper Tigers（纸老虎）**: 被过度担心的问题 → 可以忽略
- **Elephants（大象）**: 团队心照不宣但没人说的问题 → 必须摊开
- **和 Post-Mortem 区别**: 事后验尸是事故分析，事前验尸是预防

### Card 008 — WWA 格式（Why-What-Acceptance）
**来源**: `pm-skills/wwas`

比 PRD 更轻量的需求格式：
- **Why**: 为什么做这个（战略上下文 + 用户痛点）
- **What**: 做什么（具体功能描述，不写实现细节）
- **Acceptance**: 怎么算做完了（可验证的验收标准）
- 适合快速验证阶段，不需要完整 PRD 时用它

### Card 009 — Opportunity Solution Tree（机会解法树）
**来源**: `pm-skills/opportunity-solution-tree`

Teresa Torres 的框架，四层结构：
1. **Desired Outcome**（目标）: 如 "降低用户首次使用门槛"
2. **Opportunities**（机会）: 痛点/需求/期望
3. **Solutions**（解法）: 可能的实现方案
4. **Experiments**（实验）: 怎么验证解法有效
- **核心理念**: 先穷举机会，再穷解答，再设计实验验证。不要跳到第一个解法就开始做。

### Card 019 — "No one at the wheel"（没人在开车）
**来源**: `gstack/plan-ceo-review`

世界上的很多规则是人定的，不是物理定律。好的创始人/工程师敢于质疑"行业惯例"。
- 你做的安防无人机云平台，为什么一定要有传统地面站那种复杂的操作界面？
- 因为"一直如此"还是因为"用户需要"？
- **行动**: 每次看到"行业标准"时，问一句"是谁定的？为什么？现在还有道理吗？"

### Card 020 — 3 个创新 Token（Boring by Default）
**来源**: `gstack/plan-eng-review`

每个公司只有约 3 个创新额度（Innovation Tokens）。其他全部用成熟技术。
- 你的项目：创新 token 用在飞控算法和 AI 巡检上
- 其他用 React/Go/Docker 这些成熟技术
- **不要每个层都造轮子**——创新 token 花完就该 boring 了

### Card 021 — 为凌晨 3 点疲惫的人设计（Systems over Heroes）
**来源**: `gstack/plan-eng-review`

系统设计目标不是让你最好的工程师在最好的那天能搞定，而是让一个刚入职、没睡醒的人也能安全操作。
- 对应你的无人机：不是飞手也能一键完成巡检
- 对应你的云平台：半夜设备离线，系统自动处理，不需要人介入

### Card 022 — Make Something People Want
**来源**: `gstack/office-hours`

这是 Y Combinator 的核心 motto，也是所有产品决策的终极检验标准：
- 你的功能上线后，会有人说"哇，这正是我需要的"吗？
- 还是只会说"哦，又一个无人机管理工具"？
- **测试方法**: 找到 5 个目标用户，给他们看 prototype，观察他们的反应

### Card 023 — Narrowest Wedge（最窄切入点）
**来源**: `gstack/office-hours`

不要做一个通用平台，先做一个"只有 100 个人但这些人会尖叫"的功能。
- 通用平台："无人机管理云平台" → 没人关心
- 最窄切入："美国郊区房主的一键院子巡检" → 具体、有痛点、有用户画像
- **先窄后宽**: 先用楔子撬开市场，再扩展功能

---

## 🔧 工程方法论 (Dev Skills)

### Card 010 — Boil the Lake（煮湖理论）
**来源**: `gstack`

当 AI 的边际成本趋近于零时，做完整的事，不要做一半。
- 反面：手动做一次 QA → 让 AI 跑完整回归测试
- 反面：写 2 个测试用例 → 让 AI 生成全套 test scenarios
- 正面：写 API 契约时，让 AI 一次性生成完整 Swagger
- **AI 时代的压缩比**: 人类团队 2 天的 boilerplate → Claude Code 15 分钟 (~100x)

### Card 011 — Dogfooding（吃狗粮）
**来源**: `dogfood`

开发者自己用自己开发的产品，像真实用户一样操作。
- 流程：打开页面 → 截图 → 模拟操作 → 对比前后差异 → 检查控制台错误
- 核心：**你的第一个用户是你自己**。如果你自己都懒得用，用户更不会用
- 你的场景：云平台前端开发中，每次改完代码自己走一遍完整用户流程

### Card 012 — Diff-Driven QA（差异驱动测试）
**来源**: `gstack/browse`

操作前截一个 baseline snapshot → 执行操作 → 自动 diff → 只看变化部分。
- **C++类比**: 类似 git diff，只关注变更行
- 好处：快速定位问题，不用肉眼对比整个页面
- 延伸：每次部署后用 diff 对比 staging 和 prod

### Card 013 — 系统化调试四阶段
**来源**: `systematic-debugging`

铁律：**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**
1. **Root Cause**: 读错误信息、复现、查近期变更、追踪数据流
2. **Pattern Analysis**: 找到同类工作的代码，对比差异
3. **Hypothesis**: 提出假设，最小改动测试
4. **Implementation**: 写回归测试、修根因、验证
- **关键**: 每次修 bug 前先写一个失败的测试来复现它

### Card 014 — TDD: RED-GREEN-REFACTOR
**来源**: `test-driven-development`

先写失败的测试 → 写最少代码通过 → 清理代码保持测试绿色。
- **核心**: "如果你没看到测试失败，你不知道它测试的是不是正确的东西"
- 测试之后写 vs 之前写的区别：测试之后 = "这段代码做了什么"；测试之前 = "这段代码应该做什么"
- ** sunk cost fallacy**: "删掉 X 小时的工作太浪费"——时间已经没了，选择是：重写（高信心）vs 加测试（低信心）

### Card 015 — Rule of Three（三次失败法则）
**来源**: `systematic-debugging`

如果一个 bug 你尝试了 3 次修复都失败了，**STOP**。
- 这不是假设错误，这是**架构问题**
- 模式：每次修复都在不同的地方暴露新问题 → 说明共享状态/耦合太严重
- 下一步：质疑整个设计模式，不要继续修症状

### Card 016 — Baseline-Aware Quality Gate（基线感知质量门）
**来源**: `requesting-code-review`

提交前的自动验证流水线：
1. 静态安全扫描（硬编码密钥、SQL 注入、命令注入）
2. 基线测试对比（stash 变更 → 跑测试得 baseline → pop → 只 count NEW failures）
3. 独立 reviewer subagent（没有实现者上下文，fresh eyes）
4. 最多 2 轮 auto-fix 循环
- **关键**: 如果基线已经有 10 个失败，你的变更引入了 2 个新的 → 只有这 2 个 blocking

### Card 017 — Bite-Sized Tasks（咬一口大小的任务）
**来源**: `writing-plans`

每个任务 = 2-5 分钟的工作量。
- 反面："搭建认证系统"（跨 5 个文件，50 行代码）
- 正面："创建 User model 带 email 字段" → "添加 password_hash 字段" → "创建密码哈希工具"
- **原则**: 如果一个人需要猜下一步做什么，计划就不完整

### Card 018 — Fresh Context Per Task（每个任务独立上下文）
**来源**: `subagent-driven-development`

每个子任务派发给全新的 subagent，而不是在同一个 session 里累积状态。
- **为什么**: 防止上下文污染（context pollution）——前面的代码/推理干扰后面的判断
- **两阶段 review**: Spec Compliance（是否按规格做）→ Code Quality（做得好不好）
- 顺序不能颠倒：先确认做对了，再确认做得好

### Card 024 — YAGNI（你不会需要它）
**来源**: `writing-plans`

**You Aren't Gonna Need It** —— 不要为未来的需求添加"灵活性"。
- 反面：User 类加 `preferences = {}` 和 `metadata = {}`，"以后可能用到"
- 正面：只加现在需要的 `name` 和 `email`
- **成本**: 每一个多余的字段/函数/类，都是未来的技术债和维护负担

### Card 025 — Test Anti-Patterns（测试反模式）
**来源**: `test-driven-development`

四种常见错误：
1. **测 mock 不测真实行为**: mock 只验证交互，不能替代系统测试
2. **测实现细节**: 测行为/结果，不测内部方法调用
3. **只测 happy path**: 必须测边界条件、错误处理
4. **脆测试（Brittle tests）**: 测试行为而非结构——重构不应该 break 测试

### Card 026 — 独立 Reviewer（No agent should verify its own work）
**来源**: `requesting-code-review`

任何代码都应该被一个**没有参与实现的上下文**审查。
- 原理：实现者有盲点，他们知道"为什么这么写"，但不知道"这么写有没有问题"
- 方法：只给 diff，不给实现过程的上下文
- **类比**: 你不能自己批自己的作业

### Card 027 — Fail-Closed（失败时关闭）
**来源**: `requesting-code-review`

安全审查的核心原则：如果审查结果不可解析或有安全 concerns → 默认不通过。
- 不是"可能没问题吧"，而是"有疑虑就不放行"
- 对应你的无人机：失联保护 → 不是"可能还能连上"，而是"超时 3 秒就 RTH"

---

## 🎨 设计原则 (UI/UX)

### Card 028 — Design Tokens 三层架构
**来源**: `ui-ux-pro-max`, `ckm:design-system`

1. **Primitive**（原始）: `blue-500: #3B82F6`, `spacing-md: 16px`
2. **Semantic**（语义）: `color-primary: var(--blue-500)`, `color-error: var(--red-500)`
3. **Component**（组件）: `button-bg: var(--color-primary)`
- **好处**: 改主题只需改 Primitive 层，语义和组件自动跟随
- **C++类比**: typedef / using 别名 → 改底层类型，上层全部更新

### Card 029 — 可用性 7 原则（Nielsen）
**来源**: `ui-ux-pro-max` (ux domain)

交互设计的经典原则：
1. **Visibility**: 系统状态应该始终可见
2. **Match**: 系统语言应该匹配用户的真实世界
3. **User Control**: 用户应该能撤销操作（你的"手动接管"按钮就是这原则）
4. **Consistency**: 相同操作应该有相同结果
5. **Error Prevention**: 比错误恢复更好的是预防错误
6. **Recognition over Recall**: 让用户认出来，而不是想起来
7. **Flexibility**: 新手和专家都应该高效使用

### Card 030 — 时间到首次价值（Time to First Value）
**来源**: `pm-skills/pm-product-strategy`

用户从注册/开机到第一次体验到核心价值的耗时。
- 你的 A 项目策略："傻瓜式操作" = TTFV < 60 秒
- 如果用户注册后要配置 10 个参数才能飞第一次，90% 的人会放弃
- **优化方法**: 预配置默认值，引导式首次体验，跳过不必要的配置

### Card 031 — 渐进式披露（Progressive Disclosure）
**来源**: `ui-ux-pro-max` (ux domain)

不要一次把所有功能展示给用户。按需逐步展示。
- 第一层：一键起飞（核心功能）
- 第二层：调整高度和速度（进阶）
- 第三层：手动接管（专家模式）
- **原则**: 80% 的用户只需要第一层，不要让他们看到第三层

### Card 032 — 无障碍设计（Accessibility）
**来源**: `gstack/browse`

前端不是"好看就行"，要考虑所有用户：
- 颜色对比度 ≥ 4.5:1（WCAG AA 标准）
- 所有交互元素可通过键盘访问
- 图片必须有 alt 文本
- 表单元素必须有 label
- **你的场景**: 安防无人机 App 是给普通家庭用户用的，不是飞手

---

## 🤖 AI 工作流

### Card 033 — C++ 到 React 概念映射
**来源**: `learning-agent`

| 新概念 | C++ 类比 | 一句话解释 |
|--------|---------|-----------|
| Component | class/struct | UI 复用单元，.tsx ≈ .h + .cpp |
| Props | const 函数参数 | 父传子，只读不可变 |
| State | 成员变量 + notify() | 数据变 → 界面自动刷新 |
| useEffect | 回调注册/信号槽 | 当 X 变化时执行 Y |
| JSX | DSL | 编译为对象树，不是 HTML |
| Virtual DOM | 双缓冲/帧缓冲 | 内存 Diff → 批量更新 |
| Hooks | 超能力注入 | 让纯函数也有状态和生命周期 |

### Card 034 — Skill Routing（技能路由）
**来源**: `gstack`

CLAUDE.md 中定义路由规则，让 AI 自动选择专业 workflow：
- 产品想法 → office-hours | Bug 调试 → investigate
- 代码审查 → review | 部署上线 → ship
- **核心思想**: 不要让 AI 回答所有问题，让它调用有结构化工作流的 skill

### Card 035 — Print Mode vs Interactive（两种 AI 代理模式）
**来源**: `claude-code`

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| **Print Mode** (`-p`) | 一炮打完就退出 | 单任务、CI/CD、脚本自动化 |
| **Interactive PTY** | 多轮对话，tmux 管理 | 复杂重构、需要 human-in-the-loop |
- **成本**: print mode 可控（--max-turns, --max-budget-usd）
- **上下文**: interactive mode 需要监控 context window（>85% 幻觉风险大增）

### Card 036 — Context Window Health（上下文窗口健康度）
**来源**: `claude-code`

- **< 70%**: 正常运作，全精度
- **70-85%**: 精度开始下降，考虑压缩（/compact）
- **> 85%**: 幻觉风险显著增加，必须压缩或清空
- **实战**: 长 session 中定期检查 `/context`，不要等到 AI 开始胡说才处理

### Card 037 — 子代理 vs 独立进程（delegate_task vs Spawn）
**来源**: `hermes-agent`

| | delegate_task | 独立进程 (hermes -q) |
|-|---------------|---------------------|
| 隔离性 | 独立对话，共享进程 | 完全独立进程 |
| 持续时间 | 几分钟（受父循环限制） | 几小时/几天 |
| 工具访问 | 父进程的工具子集 | 完整工具访问 |
| 适用场景 | 快速并行子任务 | 长期自主任务 |

### Card 038 — 技能是持久记忆（Skills are Persistent Memory）
**来源**: `hermes-agent`

- 当 AI 解决复杂问题、发现工作流、或被纠正时，保存为 skill
- Skill 不是笔记——是**可执行的工作流程**
- 随着时间积累，AI 会越来越适应你的特定任务和环境
- **类比**: 笔记是"我知道什么"，Skill 是"我知道怎么做"

### Card 039 —  Credential Pool（凭证池）
**来源**: `hermes-agent`

Hermes 支持多个 API key 轮换使用：
- 一个 key 达到 rate limit 时自动切换到下一个
- 自动标记"耗尽"状态的 key，冷却后恢复
- **类比**: 多个出口的路由器，一个堵了自动走另一个

### Card 040 — Profile 隔离（Profile Isolation）
**来源**: `hermes-agent`

Hermes 支持多个独立 profile，每个有独立的 config/session/skill/memory。
- 适用场景：工作 profile vs 学习 profile
- 工作 profile 加载 pm-skills + gstack
- 学习 profile 加载 learning-agent
- **类比**: 浏览器多 profile，工作账号和个人账号完全隔离

---

## 🏗️ 架构与系统思维

### Card 041 — 爆炸半径（Blast Radius）
**来源**: `gstack/plan-eng-review`

每次决策问：**最坏情况影响多少人/系统？**
- 改一个配置文件 vs 改一个核心服务
- 前端按钮颜色 vs 后端认证逻辑
- **你的无人机**: 失联保护改错 → 爆炸半径 = 所有设备 → 必须极端谨慎

### Card 042 — 可逆性优先（Reversibility）
**来源**: `gstack/plan-eng-review`

Feature flag、灰度发布、渐进式发布。让犯错的成本尽可能低。
- 不可逆决策（删数据库、换底层协议）需要更多审查
- 可逆决策（加个按钮、调个参数）快速验证
- **原则**: 如果可以回滚，就快速前进。如果不能，慢慢走。

### Card 043 — 本质 vs 偶然复杂度
**来源**: `gstack/plan-eng-review`

Brooks 的经典区分（No Silver Bullet）：
- **本质复杂度**: 问题本身固有的（飞控的姿态估计就是复杂的）
- **偶然复杂度**: 我们自己制造的（用错了框架、写了重复代码、没有自动化测试）
- **行动**: 添加任何东西前问："这是解决真实问题，还是我们制造的问题？"

### Card 044 — 两周气味测试（Two-Week Smell Test）
**来源**: `gstack/plan-eng-review`

如果一个合格的工程师 2 周内发不出一个小功能，你有入职/架构问题。
- 不是工程师能力问题，是系统问题
- 常见原因：文档缺失、环境搭建困难、代码库耦合严重
- **你的项目**: 如果新同事加入，能在 2 周内完成第一个 PR 吗？

### Card 045 — 康威定律（Org Structure IS Architecture）
**来源**: `gstack/plan-eng-review`

Conway's Law：系统架构会反映组织的沟通结构。
- 一个人做全栈 → 模块边界模糊但沟通零成本
- 团队分工 → 必须有清晰的 API 契约
- **你的场景**: 你和陈继舜分工 → 界面显示和飞行模式之间需要明确的接口定义
- **设计启示**: 先想清楚谁来维护哪个模块，再设计接口

### Card 046 — 胶水工作（Glue Work Awareness）
**来源**: `gstack/plan-eng-review`

看不见的协调工作——文档编写、环境搭建、CI 配置、代码审查。
- 有价值，但不要让一个人**只**做胶水工作
- 胶水工作积累 → 技能退化 → 没有人想做
- **个人项目中的体现**: 不要花一天时间搭 CI，却没时间写核心功能

### Card 047 — 先让变更容易，再做变更
**来源**: `gstack/plan-eng-review`

Kent Beck 的原则：**Make the change easy, then make the easy change.**
- 先重构，再实现。不要同时做结构和行为变更。
- 例子：要加新功能但现有代码耦合严重 → 先解耦 → 再加功能
- 两步分开做，每步都有测试保护

### Card 048 — 拥有生产中的代码（Own Your Code in Production）
**来源**: `gstack/plan-eng-review`

没有开发和运维的墙。谁写谁负责。
- 你的无人机云平台：你写的后端，设备半夜出问题你也要能排查
- **启示**: 写代码时就想好怎么监控、怎么排查、怎么回滚
- "在本地跑通了"不是完成标准，"在生产中稳定运行"才是

### Card 049 — 错误预算（Error Budgets over Uptime Targets）
**来源**: `gstack/plan-eng-review`

SLO 99.9% = 0.1% 的 downtime 是你可以花的预算。
- 可靠性不是越高越好，是**资源分配问题**
- 99.99% 的成本可能是 99.9% 的 10 倍，但对用户体验的差异很小
- **你的项目**: 无人机云平台需要多少可用性？99.9% 可能够了，不要追求 99.999%

### Card 050 — 增量 vs 革命（Incremental over Revolutionary）
**来源**: `gstack/plan-eng-review`

绞杀藤模式（Strangler Fig），不大爆炸。
- 不要重写整个系统 → 逐步替换模块
- 灰度发布 → 先 1% 流量，再 10%，再 100%
- **你的项目**: 不要等所有功能做完才发布。先发布一个能飞的 MVP，再加功能

---

## 🧠 认知与元认知

### Card 051 — 沉没成本谬误（Sunk Cost Fallacy）
**来源**: `test-driven-development`

"删掉 X 小时的工作太浪费"——时间已经没了。
- 选择是：删掉重写（高信心）vs 加测试保留（低信心）
- **延伸**: 一个方向做了 3 天发现走错了 → 继续走下去不会让前 3 天回来
- **决策方法**: 从现在往前看，不是从开始往后看

### Card 052 — 理性化陷阱（Rationalization Trap）
**来源**: `systematic-debugging` + `test-driven-development`

工程师最常见的自欺模式：
- "这次很简单，不用走流程"
- "先快速修一下，回头再调查"
- "TDD 太教条了，我要务实一点"
- **识别方法**: 当你开始用"just this once"、"for now"、"pragmatic"时，STOP
- 这些是 shortcuts，不是 pragmatism

### Card 053 — 测试难 = 设计有问题
**来源**: `test-driven-development`

如果一个功能的测试很难写，说明设计本身有问题。
- 需要 mock 一切 → 代码耦合太严重
- 测试 setup 巨大 → 职责不单一
- 测不出具体行为 → 函数做了太多事
- **听测试的**: 测试在告诉你设计需要简化

### Card 054 — 第一个用户是你自己
**来源**: `dogfood`

- 你自己都不愿意用的功能，用户更不会用
- 每次开发完新功能，**作为真实用户完整走一遍流程**
- 不要用"我知道哪里有 bug，我会避开"的心态——用户不知道
- **行动**: 每次部署后，先自己用 5 分钟，再告诉别人"去试试吧"

---

## 📊 完整索引

| 编号 | 概念 | 分类 | 难度 |
|------|------|------|------|
| 001 | 3C + INVEST | 产品思维 | ⭐ |
| 002 | Job Story | 产品思维 | ⭐ |
| 003 | Opportunity Score | 产品思维 | ⭐⭐ |
| 004 | RICE 优先级 | 产品思维 | ⭐ |
| 005 | North Star Metric | 产品思维 | ⭐⭐ |
| 006 | Growth Loops | 产品思维 | ⭐⭐ |
| 007 | Pre-Mortem | 产品思维 | ⭐ |
| 008 | WWA 格式 | 产品思维 | ⭐ |
| 009 | Opportunity Solution Tree | 产品思维 | ⭐⭐⭐ |
| 010 | Boil the Lake | 工程方法 | ⭐ |
| 011 | Dogfooding | 工程方法 | ⭐ |
| 012 | Diff-Driven QA | 工程方法 | ⭐⭐ |
| 013 | 系统化调试四阶段 | 工程方法 | ⭐ |
| 014 | TDD: RED-GREEN-REFACTOR | 工程方法 | ⭐⭐ |
| 015 | Rule of Three | 工程方法 | ⭐ |
| 016 | Baseline-Aware Quality Gate | 工程方法 | ⭐⭐ |
| 017 | Bite-Sized Tasks | 工程方法 | ⭐ |
| 018 | Fresh Context Per Task | 工程方法 | ⭐⭐ |
| 019 | No one at the wheel | 产品思维 | ⭐⭐ |
| 020 | 3 个创新 Token | 工程方法 | ⭐ |
| 021 | Systems over Heroes | 工程方法 | ⭐ |
| 022 | Make Something People Want | 产品思维 | ⭐ |
| 023 | Narrowest Wedge | 产品思维 | ⭐ |
| 024 | YAGNI | 工程方法 | ⭐ |
| 025 | Test Anti-Patterns | 工程方法 | ⭐ |
| 026 | 独立 Reviewer | 工程方法 | ⭐ |
| 027 | Fail-Closed | 工程方法 | ⭐ |
| 028 | Design Tokens 三层架构 | 设计原则 | ⭐⭐ |
| 029 | Nielsen 7 原则 | 设计原则 | ⭐⭐ |
| 030 | Time to First Value | 产品思维 | ⭐ |
| 031 | 渐进式披露 | 设计原则 | ⭐ |
| 032 | Accessibility | 设计原则 | ⭐ |
| 033 | C++→React 映射 | AI 工作流 | ⭐ |
| 034 | Skill Routing | AI 工作流 | ⭐ |
| 035 | Print Mode vs Interactive | AI 工作流 | ⭐⭐ |
| 036 | Context Window Health | AI 工作流 | ⭐ |
| 037 | delegate_task vs Spawn | AI 工作流 | ⭐⭐ |
| 038 | 技能是持久记忆 | AI 工作流 | ⭐ |
| 039 | Credential Pool | AI 工作流 | ⭐ |
| 040 | Profile 隔离 | AI 工作流 | ⭐ |
| 041 | 爆炸半径 | 架构思维 | ⭐⭐ |
| 042 | 可逆性优先 | 架构思维 | ⭐ |
| 043 | 本质 vs 偶然复杂度 | 架构思维 | ⭐⭐ |
| 044 | 两周气味测试 | 架构思维 | ⭐ |
| 045 | 康威定律 | 架构思维 | ⭐⭐ |
| 046 | 胶水工作 | 架构思维 | ⭐ |
| 047 | Make the change easy | 架构思维 | ⭐ |
| 048 | Own Code in Production | 架构思维 | ⭐ |
| 049 | 错误预算 | 架构思维 | ⭐⭐ |
| 050 | 增量 vs 革命 | 架构思维 | ⭐ |
| 051 | 沉没成本谬误 | 认知 | ⭐ |
| 052 | 理性化陷阱 | 认知 | ⭐⭐ |
| 053 | 测试难=设计有问题 | 认知 | ⭐⭐ |
| 054 | 第一个用户是你自己 | 认知 | ⭐ |

**总计: 54 张卡片 | 产品思维 13 | 工程方法 17 | 设计原则 5 | AI 工作流 8 | 架构思维 10 | 认知 4**
