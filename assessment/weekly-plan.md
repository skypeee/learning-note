# 每周学习计划

> 排期范围：2026.04.18 - 2026.05.30
> 更新原则：每 6 周滚动更新一次，根据实际情况调整

## 固定节奏

| 时间段 | 内容 | 时长 |
|--------|------|------|
| 等 vibecoding | AI前沿 + AU/ArduPilot + 全栈/英语（多段碎片自由分配） | 5-15min × N 段 |
| 早上遛狗 | 飞控储备 / 英语听力（隔日轮换） | 20-30min |
| 晚上娃睡后 | 深度学习（全栈项目 + 飞控 + AI） | 30-60min |
| 周末（选半天） | 大块任务（架构设计/论文精读/AI实验/英语跟读） | 1.5-2h |

## 英语学习路线（四级退化 → 能读能听能说）

| 阶段 | 时间 | 目标 | 方式 |
|------|------|------|------|
| 词汇重建 | Week 1-4 | 恢复 2000 核心词 | Anki/扇贝，每天 10 词 |
| 阅读恢复 | Week 5-8 | 能慢速读官方文档 | 每天 1 段英文文档，逐句翻译+跟读 |
| 听力启动 | Week 9-12 | 能听懂慢速技术播客 | 每天 5 分钟，0.75 倍速 |
| 口语跟读 | Week 13+ | 能简单技术对话 | Shadowing 跟读，每天 3 句 |

**碎片时间分配：** 每天 AI + AU + 全栈/英语（多段碎片，自由分配），周日自由

## 进度判断规则

| 完成情况 | 判断 | 下周应对 |
|----------|------|----------|
| 周目标全部完成 | 正常/超前 | 周末加一个额外学习任务 |
| 周目标完成 70% | 正常 | 按计划走，周末补剩余 30% |
| 周目标完成 <50% | 落后 | 下周砍掉非核心任务，只保主线 |

---

## 4/18（今天，周六）

> 状态：⬜

| 时段 | 具体任务 | 状态 |
|------|----------|------|
| 碎片 | **英语**：搜 "vLLM documentation"，读第一段，逐句翻译 + 记 5 个生词 | ⬜ |
| 遛狗 | 口述练习：EKF 的完整调用链（Copter.cpp → read_AHRS → ahrs.update → EKF3.UpdateFilter → core.UpdateFilter → readGpsData），说不出来就再看一眼代码 | ⬜ |
| 晚上 | 地面站技术栈调研：QGC 二次开发 vs 自研（看 QGC GitHub 架构文档） | ⬜ |
| 下午/半天 | 写 5 条 QGC vs 自研的优缺点 | ⬜ |

---

## 历史：4/17（周五）

> 状态：✅ 已完成

| 时段 | 具体任务 | 状态 |
|------|----------|------|
| 碎片 | 搜索并阅读：「MCP (Model Context Protocol) 是什么」— 搜 `MCP Model Context Protocol 介绍 2025`，看 1-2 篇中文解读即可 | ✅ |
| 遛狗 | 打开 `notes/topics/ekf/_meta.md`，看 innovation、testRatio、FuseVelPosNED 三行，知道当前状态在哪 | ✅ |
| 晚上 | 全栈状态同步设计讨论（WebSocket + 离线缓存） | ✅ |
| 英语 | 读《七王国的骑士》第一段，记 7 个生词（hammer, carpenter, nail, joust, pavilion, revel, bacon） | ✅ |

---

## Week 2（4/19 - 4/25）— 云平台 PRD + 工程骨架 + React/TypeScript 入门

> 状态：⬜ 未开始
> 技术栈：TypeScript + React + Vite、Docker Compose、JWT/OAuth2、WebSocket、Nginx

| 日期 | 碎片时间（多段，自由分配） | 遛狗时间 飞控/英语 | 晚上任务 | 状态 |
|------|--------------------------|-------------------|----------|------|
| 4/19 周一 | AI：搜「TypeScript vs JavaScript，为什么 React 项目推荐 TS」<br>AU：搜「ArduPilot 目录结构，各子模块作用」 | 飞控：EKF gpsGood/gpsGlitch/gpsInhibit | 云平台 PRD v0.1：目标用户、核心价值、MVP 范围 + 技术选型 ADR | ✅ |
| 4/20 周二 | **英语**：读 Docker Compose docs 一段，记 5 词<br>AU：搜「AP_HAL 抽象层，飞控怎么隔离硬件差异」 | 飞控：EKF _meta.md 标记剩余知识点 | Docker Compose：定义前端 + 后端 + Redis + MySQL + Nginx + MQTT broker 的 docker-compose.yml | ⬜ |
| 4/21 周三 | AI：搜「Vite 是什么，为什么比 Webpack 快 10 倍」<br>AU：搜「AP_Scheduler 调度机制，FAST_TASK vs SCHED_TASK」 | 飞控：复习 EKF 调用链（口述） | TypeScript + React：项目初始化（Vite + TS 模板），理解 tsconfig、类型系统 | ⬜ |
| 4/22 周四 | **英语**：读 React docs 一段，记 5 词<br>AU：搜「MAVLink 协议设计，为什么飞控选它」 | 飞控：MAVLink 基础协议 | React 核心：JSX + 组件 + props/state + hooks（useState/useEffect/useRef） | ⬜ |
| 4/23 周五 | AI：搜「JWT vs Session 认证，IoT 平台选哪种」<br>AU：搜「ArduPilot 初始化流程，从 main() 到各子系统启动」 | 飞控：MAVLink heartbeat | JWT 认证：设计登录/注册 + token 签发/验证 + 拦截器（Axios + React Context） | ⬜ |
| 4/24 周六 | **英语**：听 5 分钟英文技术播客（0.75x）<br>AU：读 ArduPilot wiki 一篇（搜 `ArduPilot Copter mode`） | 英语跟读：3 句 | WebSocket：实时设备状态推送服务（后端 FastAPI WebSocket + 前端订阅） | ⬜ |
| 4/25 周日 | 自由 | 自由 | 本周复盘 | ⬜ |
| 4/24-25 周末 | — | — | **大块任务**：1. EKF _meta.md 全部知识点标记 ✅ 2. PRD + 架构图 + ADR 3. docker-compose 全部组件启动 4. React + TS 项目跑通，登录页面 + WebSocket 实时状态 demo | ⬜ |

**本周验收**：
- [ ] PRD v0.1 + 系统架构图 + ADR 技术选型文档
- [ ] docker-compose 一键启动全栈（前端/Nginx/后端/Redis/MySQL/MQTT）
- [ ] React + TypeScript 项目初始化，登录页 + WebSocket 推送 demo
- [ ] JWT 认证链路（注册 → 登录 → 鉴权中间件 → 受保护路由）

---

## Week 3（4/26 - 5/2）— 设备影子核心 + Redis 深度 + gRPC 微服务

> 状态：⬜ 未开始
> 技术栈：React 列表/详情/表单、Redis（数据结构/管道/Lua/连接池/持久化）、gRPC + Protobuf、FastAPI、MQTT（EMQX）

| 日期 | 碎片时间（多段，自由分配） | 遛狗时间 飞控 | 晚上任务 | 状态 |
|------|--------------------------|---------------|----------|------|
| 4/26 周一 | AI：搜「React 列表渲染最佳实践，Ant Design Table 性能」<br>AU：搜「ArduPilot Mode 切换逻辑，AUTO 模式和手动模式区别」 | 复习 EKF（间隔复习第1次） | React：设备列表页（Ant Design Table + 状态标签 + 搜索过滤 + 分页） | ⬜ |
| 4/27 周二 | 搜：「React 表单受控 vs 非受控组件」<br>AU：搜「ArduPilot RC 遥控通道映射，PWM/PPM/SBus 区别」 | 复习 EKF：innovation 是什么 | React：设备详情页（状态卡片 + 遥测时间线 + 参数表格 + 编辑表单） | ⬜ |
| 4/28 周三 | AI：搜「Redis 持久化 RDB vs AOF，生产怎么选」<br>AU：搜「AP_InertialSensor IMU 数据读取，滤波流程」 | 看 scheduler 笔记 | Redis 深度：数据结构选型（String/Hash/ZSet/Bitmap 场景分析）+ 缓存策略 + 过期淘汰 | ⬜ |
| 4/29 周四 | 搜：「gRPC vs REST，微服务通信协议选型」<br>AU：搜「AP_Baro 气压计数据融合，怎么和 IMU 协同」 | 看 scheduler：FAST_TASK vs SCHED_TASK | gRPC 微服务：定义 device-shadow.proto，生成 Go/Python 客户端，服务间通信 | ⬜ |
| 4/30 周五 | AI：搜「MQTT QoS 0/1/2 区别，IoT 消息丢失怎么办」<br>AU：搜「AP_Compass 磁罗盘校准，declination 处理」 | 复习：priority 对实时性的影响 | MQTT 接入：EMQX broker + Python 订阅者 + 设备上线/下线事件 + 遗嘱消息 | ⬜ |
| 周末 | — | — | **大块任务**：设备影子完整链路（MQTT → 后端 → Redis 缓存 → gRPC → 前端实时刷新） | ⬜ |

**本周验收**：
- [ ] 前端：设备列表 + 详情页可用，表单增删改查
- [ ] Redis：缓存策略文档，连接池/管道/Lua 脚本实战
- [ ] gRPC：设备影子 proto 定义 + 跨服务调用
- [ ] MQTT：EMQX 部署 + 设备上线/下线事件驱动

---

## Week 4（5/2 - 5/8）— 多租户 + MySQL 深度 + Elasticsearch 日志检索

> 状态：⬜ 未开始
> 技术栈：MySQL（索引/慢查询/分表/事务隔离/锁）、Elasticsearch + Kibana、Nginx 反向代理、React 数据可视化

| 日期 | 碎片时间（多段，自由分配） | 遛狗时间 飞控 | 晚上任务 | 状态 |
|------|--------------------------|---------------|----------|------|
| 5/2 周一 | AI：搜「多租户 SaaS 架构，数据隔离方案对比」<br>AU：搜「ArduPilot 飞行模式（RTL/LOITER/AUTO）状态机」 | MAVLink：看 MAVLink 消息类型 | 多租户隔离：schema-per-tenant vs tenant_id 列，写 ADR 对比文档 | ⬜ |
| 5/3 周二 | 搜：「MySQL RANGE 分区 vs 按量分表，时序数据怎么存」<br>AU：搜「AP_RangeFinder 测距仪，怎么用在前视避障」 | MAVLink：看 QGC 怎么解析 MAVLink | MySQL 深度：遥测时序数据分表（按月 RANGE 分区）+ 复合索引设计 | ⬜ |
| 5/4 周三 | AI：搜「MySQL EXPLAIN 详解，怎么看执行计划」<br>AU：搜「AP_OpticalFlow 光流，室内无 GPS 定位方案」 | 看飞控参数文档 | MySQL 优化：EXPLAIN 分析慢查询 + 索引优化 + 事务隔离级别调优（RR vs RC） | ⬜ |
| 5/6 周四 | 搜：「Elasticsearch vs MySQL，什么时候该用 ES」<br>AU：搜「AP_NavEKF 源码结构，core/state/fusion 目录关系」 | 复习 EKF：GPS 融合前的"防御" | Elasticsearch：设备操作日志采集 + Kibana 检索 + 聚合分析（错误类型分布） | ⬜ |
| 5/7 周五 | AI：搜「Nginx rate limiting 配置，怎么防 CC 攻击」<br>AU：搜「ArduPilot failsafe 机制（RTL/land/crash 触发条件）」 | 看 EKF status flags 含义 | Nginx 反向代理：HTTPS 终端、gzip 压缩、WebSocket 升级、限流（rate limiting） | ⬜ |
| 周末 | — | — | **大块任务**：1. 多租户 + 分表上线 2. 慢查询优化前后对比 3. ELK 日志检索看板 4. wrk/JMeter 压力测试报告 | ⬜ |

**本周验收**：
- [ ] 多租户隔离生效（不同 tenant 数据隔离）
- [ ] 遥测数据分区 + 索引优化（慢查询 <100ms）
- [ ] Elasticsearch 日志检索可用（Kibana 看板）
- [ ] Nginx 反向代理配置完整（HTTPS/gzip/限流）
- [ ] 压力测试报告（1000 设备并发 QPS/延迟）

---

## Week 5（5/10 - 5/16）— AI 日志分析 + K8s 全栈部署 + Helm

> 状态：⬜ 未开始
> 技术栈：K8s（Deployment/StatefulSet/Service/Ingress/ConfigMap/Secret/HPA）、Helm Chart、Terraform/IaC、vLLM

| 日期 | 碎片时间（多段，自由分配） | 遛狗时间 飞控 | 晚上任务 | 状态 |
|------|--------------------------|---------------|----------|------|
| 5/10 周一 | AI：搜「RAG 检索增强生成，怎么构建知识库」<br>AU：搜「ArduPilot 电机驱动模型，PWM 输出到物理电机」 | 复习 EKF + MAVLink（间隔复习第2次） | AI 日志分析：收集 SITL 日志，设计 prompt 模板 + RAG 检索增强 | ⬜ |
| 5/11 周二 | 搜：「SSE vs WebSocket，流式输出用哪个」<br>AU：搜「ArduPilot 姿态估计 AHRS vs EKF 的区别」 | 看飞控参数调优指南 | AI 日志分析：后端集成 DashScope/vLLM，流式输出 + SSE 推送 | ⬜ |
| 5/12 周三 | AI：搜「K8s Deployment vs StatefulSet 区别」<br>AU：搜「ArduPilot 参数系统 AP_Params，怎么持久化和热加载」 | 继续参数调优指南 | K8s 基础：minikube/kind 本地集群 + 手写 Deployment/StatefulService YAML | ⬜ |
| 5/13 周四 | 搜：「K8s NetworkPolicy 是什么，怎么做微服务隔离」<br>AU：搜「ArduPilot GCS_MAVLink 地面站通信模块源码结构」 | 看 AP_Params 源码结构 | K8s 网络：Service + Ingress + 跨命名空间通信 + NetworkPolicy | ⬜ |
| 5/14 周五 | AI：搜「Helm Chart 编写教程，K8s 包管理」<br>AU：搜「ArduPilot scripting Lua API，能调用哪些飞控功能」 | 复习 scheduler 笔记 | Helm + K8s 运维：写 Helm Chart 打包全栈 + ConfigMap/Secret + HPA 自动扩容 | ⬜ |
| 周末 | — | — | **大块任务**：全栈部署到 K8s（前端 + 后端 + Redis + MySQL + Elasticsearch + EMQX + AI 服务） | ⬜ |

**本周验收**：
- [ ] AI 日志分析能工作（输入日志 → RAG 检索 → LLM 分析 → 流式输出）
- [ ] Helm Chart 打包全栈组件
- [ ] K8s 全栈部署可访问
- [ ] HPA 配置生效（模拟流量触发扩容）

---

## Week 6（5/17 - 5/23）— CI/CD + 可观测性 + 故障演练

> 状态：⬜ 未开始
> 技术栈：GitHub Actions、Docker 镜像优化、Prometheus + Grafana + AlertManager、Jaeger 分布式追踪、自动化测试、混沌工程

| 日期 | 碎片时间（多段，自由分配） | 遛狗时间 飞控 | 晚上任务 | 状态 |
|------|--------------------------|---------------|----------|------|
| 5/17 周一 | AI：搜「GitHub Actions CI/CD 最佳实践」<br>AU：搜「ArduPilot 电池监控 AP_BattMonitor，电压/电流/剩余容量计算」 | 飞控参数调优指南继续 | CI/CD：GitHub Actions 流水线（lint → test → Docker build → push → K8s deploy） | ⬜ |
| 5/18 周二 | 搜：「Docker multi-stage build，怎么把镜像做到 50MB 以内」<br>AU：搜「ArduPilot GPS 驱动 AP_GPS 多协议支持（UBLOX/MTR/MAV）」 | 看 ArduPilot 飞控初始化流程 | Docker 镜像优化：multi-stage build + 镜像大小优化（<50MB） | ⬜ |
| 5/19 周三 | AI：搜「React Testing Library 最佳实践」<br>AU：搜「ArduPilot RC 遥控器输入处理 AP_RC */RC_Channel」 | 复习：飞控初始化设置 | 自动化测试：前端（Vitest + React Testing Library）+ 后端（pytest + 集成测试） | ⬜ |
| 5/20 周四 | 搜：「Prometheus 自定义 metrics，怎么暴露业务指标」<br>AU：搜「ArduPilot 地理围栏 AP_Fence 实现」 | 看 ESP32 入门资料 | Prometheus：自定义 metrics（API 延迟/错误率/Redis hit rate/MQTT 连接数） | ⬜ |
| 5/21 周五 | AI：搜「Jaeger 分布式追踪，怎么定位慢请求」<br>AU：搜「ArduPilot 日志系统 DataFlash/AP_Logger，二进制格式解析」 | ESP32 继续，看 GPIO/中断基础 | 全链路可观测：Grafana 看板 + AlertManager 告警 + Jaeger 分布式追踪 | ⬜ |
| 周末 | — | — | **大块任务**：混沌工程演练（Redis 宕机/DB 慢查询/MQ 断连/Pod 驱逐），记录 RTO/RPO | ⬜ |

**本周验收**：
- [ ] CI/CD 流水线自动跑通（push → 测试 → 部署）
- [ ] Docker 镜像 <50MB（multi-stage build）
- [ ] Grafana 全栈看板 + AlertManager P0/P1 告警
- [ ] Jaeger 追踪全链路请求
- [ ] 混沌演练报告（每种故障的 RTO/RPO + 改进措施）

---

## Week 7（5/24 - 5/30）— MVP 收官 + 架构总结 + 下期规划

> 状态：⬜ 未开始
> 技术深度：全链路回顾、性能调优、架构文档输出、下期规划

| 日期 | 碎片时间（多段，自由分配） | 遛狗时间 飞控 | 晚上任务 | 状态 |
|------|--------------------------|---------------|----------|------|
| 5/24 周一 | AI：搜「端到端全链路压测，怎么设计压测场景」<br>AU：搜「ArduPilot HIL 仿真，怎么从 SITL 过渡到硬件在环」 | 复习全部飞控储备（间隔复习第3次） | 全链路压测：端到端从设备接入 → MQTT → 后端 → DB → WebSocket → 前端 | ⬜ |
| 5/25 周二 | 搜：「React bundle 分析，代码分割怎么做」<br>AU：搜「ArduPilot 避障系统 AP_Avoidance，怎么检测和处理障碍物」 | 复习 EKF：口述 GPS 融合完整流程 | 性能调优：前端 bundle 分析 + 代码分割 + Redis pipeline 优化 + MySQL 连接池调优 | ⬜ |
| 5/26 周三 | AI：搜「ADR 架构决策文档怎么写」<br>AU：搜「ArduPilot 任务脚本系统 AP_Script（Lua），能做什么」 | 复习 Scheduler：口述调度流程 | 架构总结：从 0 到 1 的技术决策回顾 + 踩坑记录 | ⬜ |
| 5/27 周四 | 搜：「React 性能优化，useMemo/useCallback 什么时候用」<br>AU：搜「ArduPilot 地形数据库 AP_Terrain，数据格式和加载」 | 复习 MAVLink：口述消息类型 | React 进阶：性能优化（React.memo/useMemo/useCallback/virtual list） | ⬜ |
| 5/28 周五 | AI：搜「如何写技术博客，把踩坑经验沉淀下来」<br>AU：搜「ArduPilot 社区贡献指南，怎么给主线提 PR」 | 复习 HAL：口述程序入口 | 月度复盘：技术收获清单 + 技能矩阵更新 + 下期 6 周计划 | ⬜ |
| 周末 | — | — | **大块任务**：1. 输出可展示 demo 2. 技术博客 1 篇 3. 月度复盘 4. 下期计划 | ⬜ |

**本周验收**：
- [ ] 全链路压测报告（端到端延迟 <500ms）
- [ ] 前端性能优化（bundle size、首屏加载 <2s）
- [ ] 架构总结文档 + 踩坑记录
- [ ] 技能矩阵更新（skills.md 评级提升）
- [ ] 可展示 demo + 技术博客 1 篇

---

## 使用方式

1. **每天打开这个文件**，找到今天的日期，按表格执行
2. **完成后把 ⬜ 改成 ✅**
3. **周日晚上花 5 分钟**，看本周 ✅ 数量 / 总任务数，对照进度判断规则
4. **每 6 周结束后**，根据实际情况排下一期 6 周计划
