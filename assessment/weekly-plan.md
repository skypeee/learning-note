# 每周学习计划 — 任务池驱动

> 排期范围：2026.04.19 - 2026.05.30
> 更新原则：每 6 周滚动更新，按需领取任务
> 使用方式：说"继续学习"或"有时间了"，AI 从任务池列出各方向待领取任务，你挑一个执行

## 固定节奏

| 场景 | 内容 | 时长 |
|------|------|------|
| 等 vibecoding | AI前沿 + AU/ArduPilot + 技术调研 + 英语（多段碎片自由分配） | 5-15min × N 段 |
| 早上遛狗 | 飞控储备 / 英语听力（隔日轮换） | 20-30min |
| 晚上娃睡后 | 深度学习（全栈项目 + 飞控 + AI） | 30-60min |
| 周末（选半天） | 大块任务（架构设计/论文精读/AI实验/英语跟读） | 1.5-2h |

## 英语长线学习路线（S0 → S4）

> 核心目标：能直接读英文技术文档、听懂技术播客、参与 ArduPilot 社区英文讨论
> 不追求考试，追求**实用能力**。每个阶段有明确的"通过标准"，达到才能进入下一阶段。

| 阶段 | 周期 | 输入材料 | 每日任务 | 通过标准 | 状态 |
|------|------|---------|---------|---------|------|
| **S0 恢复** | 4-6 周 | 分级读物（Oxford L3-L5）、《七王国的骑士》 | 每天 2 页英文阅读 + 10 词 Anki | 不看词典慢读小说，生词率 <5% | ▶️ 进行中 |
| **S1 技术阅读** | 4-6 周 | ArduPilot wiki、React docs、Go 官方文档 | 每天读 1 篇技术文档，不依赖翻译 | 独立读懂 70%+ 技术文档 | ⬜ |
| **S2 技术听力** | 6-8 周 | Syntax/Go Time 播客、YouTube 教程（0.75x） | 每天 10min 精听（听写关键词） | 听懂 70%+ 慢速技术播客 | ⬜ |
| **S3 技术写作** | 持续 | GitHub issue、PR、Stack Overflow | 每周写 2 条英文 issue/PR/评论 | 能用英文清晰描述技术问题 | ⬜ |
| **S4 技术口语** | 持续 | Shadowing 跟读、自言自语技术描述 | 每天 5min 跟读 | 能口头用英文描述技术方案 | ⬜ |

**英语进度判断**：
- 生词数持续下降 → 正常进步
- 一周内阅读速度明显提升 → 可以进入 S1
- 断了一天不要紧，断三天以上需要补回

## 飞控长线学习路线（S0 → S3）

> 核心目标：从 SITL 使用者 → 能读懂源码、能做 HIL、能调参、能改代码
> 每个阶段有明确的"通过标准"，达到才能进入下一阶段。

| 阶段 | 名称 | 内容 | 通过标准 | 状态 |
|------|------|------|---------|------|
| **S0 系统理解** | 整体架构 | 目录结构、AP_HAL、初始化流程、Scheduler、参数系统 | 能口述从 main() 到飞行的完整启动流程 | ▶️ 进行中 |
| **S1 姿态估计** | EKF/AHRS | 传感器融合、EKF3、innovation/gating、GPS/磁力计/气压计融合 | 能口述 EKF predict-update 循环，知道 testRatio 含义 | ⬜ |
| **S2 控制与调参** | 飞控调参 | PID 调参、姿态/位置/速度环、failsafe、地理围栏、RTL | 能完成 SITL 调参（默认 → 优化） | ⬜ |
| **S3 源码级** | 改代码 | 写新模块、改调度、加 MAVLink 消息、Lua scripting | 能给 ArduPilot 社区提 PR | ⬜ |

## AI 长线学习路线（S0 → S3）

> 核心目标：从 AI 使用者 → 能搭 RAG pipeline、能调优 LLM、能做 Agent 系统
> 不追求发论文，追求**能用 AI 解决实际工程问题**。

| 阶段 | 名称 | 内容 | 通过标准 | 状态 |
|------|------|------|---------|------|
| **S0 认知与应用** | 知道能做什么 | 主流模型、Prompt、Function Calling、RAG 基本概念 | 能搭一个 RAG demo（向量库 + Embedding + LLM） | ⬜ |
| **S1 工程集成** | AI 融入项目 | vLLM 部署、SSE 流式、Agent 框架、AI 代码审查 | 云平台集成 AI 日志分析功能可用 | ⬜ |
| **S2 优化与调优** | 提升质量/性能 | RAG chunking、Prompt 优化、评估基准、向量库选型 | RAG 输出质量有可量化评估指标 | ⬜ |
| **S3 深度定制** | Fine-tuning/自研 | 模型微调、Multi-agent、自定义推理优化 | 能针对场景微调或定制 pipeline | ⬜ |

## 全栈项目路线（S0 → S3）

> 项目：通用嵌入式设备管理云平台
> 核心目标：从 0 到 1 搭建一个可展示、可部署、可扩展的 SaaS 平台
> 每个阶段有明确的验收标准，达到才能进入下一阶段。

| 阶段 | 名称 | 核心任务 | 验收标准 | 状态 |
|------|------|---------|---------|------|
| **S0 工程骨架** | 项目初始化 | React+TS 项目、Docker Compose 全栈编排、JWT 认证、WebSocket 基础 | `docker-compose up` 一键启动，登录页可注册登录，WebSocket 推送 demo | ▶️ 进行中 |
| **S1 核心功能** | 设备管理 | 设备列表/详情页、Redis 设备状态缓存、gRPC 设备影子、MQTT 设备接入、EMQX 部署 | 前端增删改查 + 设备上线/下线实时刷新 + 设备影子离线缓存 | ⬜ |
| **S2 生产级** | 多租户/高性能 | 多租户隔离、MySQL 分表+索引优化、Elasticsearch 日志检索、Nginx 反向代理 | 1000 设备并发 QPS 测试通过 + 慢查询 <100ms + 多租户数据隔离 | ⬜ |
| **S3 运维部署** | 可观测性/CI-CD | K8s 全栈部署、Helm Chart、Prometheus/Grafana 监控、CI/CD 流水线、Jaeger 追踪、混沌演练 | K8s 可访问 + Grafana 看板 + push 自动部署 + 混沌报告 | ⬜ |
| **S4 智能增强** | AI 集成 | AI 日志分析（RAG）、LLM 流式输出、全链路压测、性能调优 | AI 日志分析可用 + 端到端延迟 <500ms + 前端首屏 <2s | ⬜ |

## 进度判断规则

| 周完成率 | 判断 | 应对 |
|----------|------|------|
| 全部完成 | 正常/超前 | 周末加一个额外学习任务 |
| 70% | 正常 | 按计划走，周末补剩余 30% |
| <50% | 落后 | 下周砍掉非核心任务，只保主线 |

---

## 任务领取规则

1. **P0 主线**：全栈项目任务，按顺序领取，前置未完成不可领取
2. **P1 进阶**：英语/技术调研/项目思考，可并行
3. **P2 AI前沿**：LLM/vLLM/RAG/Agent，自由领取
4. **P3 探索**：飞控/AU 储备，自由领取

状态标记：`⬜ 待领取` `▶️ 进行中` `✅ 已完成`

---

## Week 2（4/19 - 4/25）— 云平台 PRD + 工程骨架 + React/TypeScript 入门

> 技术栈：TypeScript + React + Vite、Docker Compose、JWT/OAuth2、WebSocket、Nginx
> 当前周进度：4/24 完成

### P0 主线（按顺序）

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 1 | 云平台 PRD v0.1：目标用户、核心价值、MVP 范围 + 技术选型 ADR | ✅ | — |
| 2 | TypeScript + React：项目初始化（Vite + TS 模板），理解 tsconfig、类型系统 | ⬜ | 1 |
| 3 | React 核心：JSX + 组件 + props/state + hooks（useState/useEffect/useRef） | ⬜ | 2 |
| 4 | Docker Compose：定义前端 + 后端 + Redis + MySQL + Nginx + MQTT broker | ⬜ | 1 |
| 5 | JWT 认证：登录/注册 + token 签发/验证 + 拦截器（Axios + React Context） | ⬜ | 3 |
| 6 | WebSocket：实时设备状态推送服务（后端 Go WebSocket + 前端订阅） | ⬜ | 3 |

### P1 进阶

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 7 | 英语 S0：读《七王国的骑士》2 页 + 记 10 词 | ⬜ | — |
| 8 | 英语 S0：读 Docker Compose docs 一段，记 5 词（不依赖翻译） | ⬜ | — |
| 9 | 技术调研：搜「Vite 是什么，为什么比 Webpack 快 10 倍」 | ⬜ | — |
| 10 | 技术调研：搜「JWT vs Session 认证，IoT 平台选哪种」 | ⬜ | — |
| 11 | 技术调研：搜「WebSocket 帧结构 + 握手升级流程」 | ⬜ | — |

### P2 AI前沿

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 12 | 搜「vLLM PagedAttention 原理，为什么吞吐量比原版快 24 倍」 | ⬜ | — |
| 13 | 搜「OpenAI Function Calling / Tool Use 机制，怎么让 LLM 调 API」 | ⬜ | — |
| 14 | 搜「RAG（检索增强生成）完整架构：向量库 + Embedding + LLM」 | ⬜ | — |
| 15 | 了解 wterm（Vercel Labs Web 终端） | ⬜ | — |
| 16 | 了解 browser-harness（LLM 自修复浏览器） | ⬜ | — |
| 17 | 了解 HTML PPT Skill（AI 生成 PPT） | ⬜ | — |
| 18 | 了解 xata（Postgres + copy-on-write 分支） | ⬜ | — |
| 19 | 了解 weft（AI 系统编程语言 Rust） | ⬜ | — |
| 20 | 了解 OpenMythos（Claude 架构第一性原理重建） | ⬜ | — |
| 21 | 了解 BuilderPulse（AI 独立开发者每日情报） | ⬜ | — |

### P3 探索（飞控/AU）

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 15 | EKF _meta.md 标记剩余知识点 | ⬜ | — |
| 16 | 搜「AP_HAL 抽象层，飞控怎么隔离硬件差异」 | ⬜ | — |
| 17 | 搜「ArduPilot 初始化流程，从 main() 到各子系统启动」 | ⬜ | — |
| 18 | 搜「MAVLink 协议设计，为什么飞控选它」 | ⬜ | — |

### P4 LLM 架构认知

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 22 | 搜「Attention Is All You Need 精读，QKV 矩阵怎么来的」 | ⬜ | — |
| 23 | 搜「Decoder-only vs Encoder-Decoder，GPT/Claude/Llama 为什么都用 Decoder」 | ⬜ | — |
| 24 | 搜「MoE 混合专家机制，GPT-4/Claude 的专家路由原理」 | ⬜ | — |
| 25 | 搜「MLA 多头潜注意力（DeepSeek），和标准 Attention 区别」 | ⬜ | — |
| 26 | 搜「循环深度 Transformer（RDT），OpenMythos 架构分析」 | ⬜ | — |
| 27 | 搜「KV Cache 原理，为什么推理时省显存」 | ⬜ | — |

**本周验收**：
- [ ] PRD v0.1 + 系统架构图 + ADR 技术选型文档 ✅
- [ ] docker-compose 一键启动全栈
- [ ] React + TypeScript 项目初始化
- [ ] JWT 认证链路

---

## Week 3（4/26 - 5/2）— 设备影子核心 + Redis 深度 + gRPC 微服务

> 技术栈：React 列表/详情/表单、Redis、gRPC + Protobuf、FastAPI、MQTT（EMQX）

### P0 主线

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 1 | React：设备列表页（Ant Design Table + 状态标签 + 搜索 + 分页） | ⬜ | — |
| 2 | React：设备详情页（状态卡片 + 遥测时间线 + 参数表格 + 编辑表单） | ⬜ | 1 |
| 3 | Redis 深度：数据结构选型 + 缓存策略 + 过期淘汰 + 管道/Lua | ⬜ | — |
| 4 | gRPC：定义 device-shadow.proto，生成 Go/Python 客户端 | ⬜ | 3 |
| 5 | MQTT：EMQX broker + 订阅者 + 设备上线/下线事件 + 遗嘱消息 | ⬜ | 3 |

### P1 进阶

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 6 | 英语 S0/S1：读 React docs 一段，记 5 词 | ⬜ | — |
| 7 | 英语 S2：听 5 分钟英文技术播客（0.75x） | ⬜ | — |
| 8 | 技术调研：搜「Redis 持久化 RDB vs AOF，生产怎么选」 | ⬜ | — |
| 9 | 技术调研：搜「gRPC vs REST，微服务通信协议选型」 | ⬜ | — |
| 10 | 技术调研：搜「MQTT QoS 0/1/2 区别，IoT 消息丢失怎么办」 | ⬜ | — |

### P2 AI前沿

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 11 | 搜「AI Agent 框架对比：LangChain vs CrewAI vs AutoGen」 | ⬜ | — |
| 12 | 搜「LLM 结构化输出：JSON schema / function calling 实践」 | ⬜ | 11 |

### P3 探索

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 13 | 复习 EKF（间隔复习第1次） | ⬜ | — |
| 14 | 搜「ArduPilot Mode 切换逻辑，AUTO 和手动模式区别」 | ⬜ | — |
| 15 | 搜「ArduPilot RC 遥控通道映射，PWM/PPM/SBus」 | ⬜ | — |
| 16 | 搜「AP_InertialSensor IMU 数据读取，滤波流程」 | ⬜ | — |
| 17 | 搜「AP_Baro 气压计数据融合，怎么和 IMU 协同」 | ⬜ | — |
| 18 | 搜「AP_Compass 磁罗盘校准，declination 处理」 | ⬜ | — |

**大块任务**：设备影子完整链路（MQTT → 后端 → Redis → gRPC → 前端）

---

## Week 4（5/2 - 5/8）— 多租户 + MySQL 深度 + Elasticsearch

> 技术栈：MySQL、Elasticsearch + Kibana、Nginx 反向代理

### P0 主线

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 1 | 多租户隔离：schema-per-tenant vs tenant_id，写 ADR | ⬜ | — |
| 2 | MySQL：遥测时序数据分表（RANGE 分区）+ 复合索引设计 | ⬜ | — |
| 3 | MySQL 优化：EXPLAIN 分析 + 索引优化 + 事务隔离级别 | ⬜ | 2 |
| 4 | Elasticsearch：日志采集 + Kibana 检索 + 聚合分析 | ⬜ | — |
| 5 | Nginx：HTTPS + gzip + WebSocket 升级 + 限流 | ⬜ | — |

### P1 进阶

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 6 | 英语 S0/S1：读 MySQL 或 ES 官方文档一段 | ⬜ | — |
| 7 | 技术调研：搜「多租户 SaaS 数据隔离方案对比」 | ⬜ | — |
| 8 | 技术调研：搜「MySQL EXPLAIN 详解」 | ⬜ | — |
| 9 | 技术调研：搜「Elasticsearch vs MySQL 选型」 | ⬜ | — |
| 10 | 技术调研：搜「Nginx rate limiting 配置」 | ⬜ | — |

### P2 AI前沿

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 11 | 搜「LLM Fine-tuning vs RAG，什么时候用哪个」 | ⬜ | — |
| 12 | 搜「向量数据库对比：Milvus vs Pinecone vs FAISS」 | ⬜ | — |

### P3 探索

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 13 | 复习 EKF：GPS 融合前的"防御"机制 | ⬜ | — |
| 14 | 看 EKF status flags 含义 | ⬜ | — |
| 15 | 搜「ArduPilot 飞行模式（RTL/LOITER/AUTO）状态机」 | ⬜ | — |
| 16 | 搜「AP_RangeFinder 前视避障」 | ⬜ | — |
| 17 | 搜「AP_OpticalFlow 光流，室内无 GPS」 | ⬜ | — |
| 18 | 搜「AP_NavEKF 源码结构」 | ⬜ | — |

---

## Week 5（5/10 - 5/16）— AI 日志分析 + K8s 全栈部署 + Helm

> 技术栈：K8s、Helm Chart、vLLM、SSE

### P0 主线

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 1 | AI 日志分析：SITL 日志 → prompt 模板 + RAG 检索 | ⬜ | — |
| 2 | AI 日志分析：后端集成 DashScope/vLLM，流式输出 + SSE | ⬜ | 1 |
| 3 | K8s 基础：minikube/kind + Deployment/StatefulService YAML | ⬜ | — |
| 4 | K8s 网络：Service + Ingress + 跨 ns 通信 + NetworkPolicy | ⬜ | 3 |
| 5 | Helm：写 Chart 打包全栈 + ConfigMap/Secret + HPA | ⬜ | 4 |

### P1 进阶

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 6 | 英语 S1：读 K8s 官方文档一段 | ⬜ | — |
| 7 | 技术调研：搜「RAG chunking 策略」 | ⬜ | — |
| 8 | 技术调研：搜「SSE vs WebSocket，流式输出用哪个」 | ⬜ | — |
| 9 | 技术调研：搜「K8s Deployment vs StatefulSet」 | ⬜ | — |
| 10 | 技术调研：搜「Helm Chart 编写教程」 | ⬜ | — |

### P2 AI前沿

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 11 | 搜「vLLM 部署实践：P0 精度推理服务搭建」 | ⬜ | — |
| 12 | 搜「Multi-modal LLM：图片+文本联合理解」 | ⬜ | — |

### P3 探索

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 13 | 复习 EKF + MAVLink（间隔复习第2次） | ⬜ | — |
| 14 | 搜「ArduPilot 电机驱动模型，PWM 输出」 | ⬜ | — |
| 15 | 搜「AHRS vs EKF 的区别」 | ⬜ | — |
| 16 | 搜「AP_Params 持久化和热加载」 | ⬜ | — |
| 17 | 搜「GCS_MAVLink 地面站通信模块源码」 | ⬜ | — |
| 18 | 搜「ArduPilot scripting Lua API」 | ⬜ | — |

---

## Week 6（5/17 - 5/23）— CI/CD + 可观测性 + 故障演练

> 技术栈：GitHub Actions、Prometheus + Grafana、Jaeger、混沌工程

### P0 主线

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 1 | CI/CD：GitHub Actions（lint → test → build → deploy） | ⬜ | — |
| 2 | Docker 镜像优化：multi-stage build <50MB | ⬜ | 1 |
| 3 | 自动化测试：前端 Vitist + 后端 pytest 集成测试 | ⬜ | — |
| 4 | Prometheus：自定义 metrics（API 延迟/错误率/Redis hit rate） | ⬜ | — |
| 5 | 全链路可观测：Grafana + AlertManager + Jaeger | ⬜ | 4 |

### P1 进阶

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 6 | 英语 S1：读 Prometheus 官方文档一段 | ⬜ | — |
| 7 | 技术调研：搜「GitHub Actions CI/CD 最佳实践」 | ⬜ | — |
| 8 | 技术调研：搜「Prometheus 自定义 metrics」 | ⬜ | — |
| 9 | 技术调研：搜「Jaeger 分布式追踪原理」 | ⬜ | — |
| 10 | 技术调研：搜「混沌工程 RTO/RPO 测量」 | ⬜ | — |

### P2 AI前沿

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 11 | 搜「AI 代码审查：用 LLM 做 PR 自动 review」 | ⬜ | — |
| 12 | 搜「LLM 可观测性：怎么评估 RAG pipeline 质量」 | ⬜ | — |

### P3 探索

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 13 | 飞控参数调优指南 | ⬜ | — |
| 14 | 搜「ArduPilot AP_Fence 地理围栏」 | ⬜ | — |
| 15 | 搜「DataFlash/AP_Logger 二进制格式」 | ⬜ | — |
| 16 | ESP32 入门：GPIO/中断基础 | ⬜ | — |

---

## Week 7（5/24 - 5/30）— MVP 收官 + 架构总结 + 下期规划

### P0 主线

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 1 | 全链路压测：设备接入 → MQTT → DB → WebSocket → 前端 | ⬜ | — |
| 2 | 性能调优：前端 bundle + Redis pipeline + MySQL 连接池 | ⬜ | 1 |
| 3 | 架构总结：技术决策回顾 + 踩坑记录 | ⬜ | 1 |
| 4 | React 性能：memo/useMemo/useCallback/virtual list | ⬜ | — |
| 5 | 月度复盘：技能矩阵更新 + 下期计划 | ⬜ | 3 |

### P1 进阶

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 6 | 英语 S2：听 10 分钟技术播客，记录关键词 | ⬜ | — |
| 7 | 技术调研：搜「端到端全链路压测设计」 | ⬜ | — |
| 8 | 技术调研：搜「React bundle 分析 + 代码分割」 | ⬜ | — |
| 9 | 技术调研：搜「ADR 架构决策文档写法」 | ⬜ | — |
| 10 | 技术调研：搜「如何写技术博客」 | ⬜ | — |

### P2 AI前沿

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 11 | 搜「LLM 输出质量评估：建立 RAG 评估基准」 | ⬜ | — |
| 12 | 搜「AI 前沿：Agentic workflow / multi-agent 系统设计」 | ⬜ | — |

### P3 探索

| # | 任务 | 状态 | 前置 |
|---|------|------|------|
| 13 | 复习全部飞控储备（间隔复习第3次） | ⬜ | — |
| 14 | 搜「ArduPilot HIL 仿真，SITL → HIL」 | ⬜ | — |
| 15 | 复习 EKF：口述 GPS 融合完整流程 | ⬜ | — |
| 16 | 复习 Scheduler：口述调度流程 | ⬜ | — |
| 17 | 复习 MAVLink：口述消息类型 | ⬜ | — |
| 18 | 复习 HAL：口述程序入口 | ⬜ | — |
| 19 | 搜「ArduPilot 避障系统 AP_Avoidance」 | ⬜ | — |
| 20 | 搜「ArduPilot 社区贡献指南」 | ⬜ | — |

---

## 已完成任务历史

| 日期 | 任务 | 状态 |
|------|------|------|
| 4/19 | 云平台 PRD v0.1 | ✅ |
| 4/19 | 英语：读《七王国的骑士》第一段 + 7 词 | ✅ |
| 4/19 | AI前沿：搜「TypeScript vs JavaScript」 | ✅ |
| 4/19 | AU：ArduPilot 目录结构 | ✅ |
| 4/19 | 飞控：EKF gpsGood/gpsGlitch/gpsInhibit | ✅ |
| 4/19 | 飞控复习：FAST_TASK vs SCHED_TASK 区别 | ✅ |
| 4/19 | 技术调研：Vite 是什么，为什么比 Webpack 快 | ✅ |
| 4/19 | 英语：前端构建 5 词复习（bundle/transpile/dependency graph/HMR/on-demand） | ✅ |
| 4/19 | 技术调研：JWT vs Session，IoT 平台选哪种 | ✅ |
| 4/19 | 英语：认证 5 词复习（stateless/revoke/payload/intermittent/horizontal scaling） | ✅ |
| 4/19 | 技术调研：SSO 单点登录原理 + PRD 补充认证架构 | ✅ |
| 4/19 | 英语：SSO 5 词复习（credential/redirect/authentication/authorization/callback） | ✅ |
