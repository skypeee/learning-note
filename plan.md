第一周任务已完成、
---

# 🛩️ **1 年 ArduPilot 飞控工程师成长路线图（全年规划）**

## 🟥 **Q1（第 1–12 周）：基础能力 + ArduPilot 入门**

目标：

* 补齐嵌入式 C/C++
* 掌握 Linux + 编译系统
* 跑通 ArduPilot SITL
* 能看懂 Mode 基本代码结构

核心成果：
✔ 能编译启动 ArduPilot
✔ 能用 MAVLink 控制飞行
✔ 能读懂 Mode / Scheduler 代码

---

## 🟧 **Q2（第 13–24 周）：Mode / Mission / MAVLink 深度**

目标：

* 看懂所有 Mode 架构
* 做一个简单自定义 Mode
* 学会扩展 MAVLink 消息
* 能修改 mission 行为

核心成果：
✔ 自己的第一个“自定义飞行模式”
✔ 自己定义的 MAVLink 消息能跑通 GCS

---

## 🟨 **Q3（第 25–36 周）：控制器 + 传感器 + EKF 基础**

目标：

* 掌握姿态/速度/位置控制
* 能读懂 IMU/GPS/Baro 管线
* 理解 EKF 融合流程
* 能调参和调试控制

核心成果：
✔ 理解飞控控制链路
✔ 能调试 IMU、GPS、Baro
✔ 能解释 EKF 工作流程

---

## 🟩 **Q4（第 37–52 周）：真实项目开发（Mode / Mission / MAVLink 全链路）**

目标：

* 完成一个可展示的飞控完整功能
* 或者开发外部电脑（Companion）系统控制
* 输出 demo / 视频 / 文档

核心成果：
✔ 你的第一份可展示的飞控“作品”
✔ 模式 + MAVLink + GCS 全链路
✔ 达到企业可用的工程师水平

---

# 🗓️ **完整 52 周详细计划（每周可执行）**

---

# 🟥 **Q1（第 1–12 周）：嵌入式 + ArduPilot 入门**

---

## **第 1 周：环境搭建 + Linux 基础**

* 安装 Ubuntu 
* 熟悉 Git / VSCode
* 熟悉基本 Linux 命令
* 克隆 ArduPilot
* 安装依赖

📝成果：能运行 `sim_vehicle.py`

---

## **第 2 周：第一次运行 ArduCopter SITL**

* 跑：
  `sim_vehicle.py -v copter --map --console`
* 学 mavproxy 基本指令（arm、mode、takeoff）
* 尝试 set parameter
* 试完整航点任务（Guided → Auto）

📝成果：能通过 MAVProxy 完整起飞 + 执行任务

---

## **第 3 周：C 基础补齐**

* 指针、结构体
* 内存模型
* volatile / static
* C 编程题练习

📝成果：理解 ArduPilot HAL 中 C 部分

---

## **第 4 周：C++ 专项（飞控代码核心语言）**

* 类、继承、多态
* 模板使用
* 智能指针
* 函数指针、回调

📝成果：能阅读 ArduPilot C++ 文件结构

---

## **第 5 周：编译系统 + 工程构建**

* waf 编译系统
* 模块组织方式
* 学会增量编译
* 了解 AP_HAL 抽象层

📝成果：修改一个文件 → 成功编译通过

---

## **第 6 周：飞控基本原理**

* 姿态角、欧拉角
* 惯性系 ↔ body 系
* PID 基础
* 飞控执行循环（Scheduler）

📝成果：画出 ArduPilot 主循环流程图

---

## **第 7 周：阅读 Mode 架构（重点）**

阅读以下文件：

* `ArduCopter/mode.cpp`
* `mode_stabilize.cpp`
* `mode_loiter.cpp`

📝成果：能说出 Mode 切换流程

---

## **第 8 周：使用 pymavlink 控制 SITL**

写脚本实现：

* 读取 GPS
* 设置模式
* 自动起飞
* 自动移动 / 降落

📝成果：第一个无人机控制脚本

---

## **第 9 周：数据 Log 分析**

学习：

* `.BIN` 文件
* `mavlogdump.py`
* 飞控消息记录工具

📝成果：能分析高度、GPS、IMU 数据

---

## **第 10 周：HAL 框架理解**

阅读：

* AP_HAL
* AP_Scheduler
* AP_Param（重要）

📝成果：了解 ArduPilot 模块组织方式

---

## **第 11–12 周：第一次小改动（Hello Mode）**

任务：

* clone Stabilize 模式
* 做一个简单模式：进入后自动上升 20cm
* 能切换该模式

📝成果：你的第一个“自定义 Mode”

---

---

# 🟧 **Q2（第 13–24 周）：Mode / Mission / MAVLink 深度**

---

## **第 13–14 周：阅读所有 Mode 文件**

目标：
了解所有模式的差异：

* Stabilize / AltHold / Loiter / PosHold / Auto / RTL

📝成果：画一张 Mode 调用关系图

---

## **第 15–16 周：完善你的自定义 Mode**

* 添加参数（AP_Param）
* 添加 MAVLink 状态上报
* 增加机体运动（例如上下锯齿波）

📝成果：一个可演示的 Mode V1

---

## **第 17–18 周：Mission（任务系统）**

阅读：

* `libraries/AP_Mission`
* 命令执行流程
* 航点任务执行代码

📝成果：能解释航点执行顺序

---

## **第 19–20 周：修改 Mission 行为**

任务：

* 修改“航点到达判定半径”
* 添加一个新的 Mission command（例如“Hover for X seconds”）

📝成果：你的自定义 Mission 指令

---

## **第 21–22 周：深入 MAVLink 协议**

学习：

* message 格式
* CRC、校验
* message 流向（飞控 → GCS）

📝成果：能修改并重新生成 MAVLink 消息

---

## **第 23–24 周：自定义 MAVLink（全链路）**

任务：

* 新增一个 message
* 飞控发送
* 地面站 / MAVProxy 显示

📝成果：你的自定义 MAVLink V1

---

---

# 🟨 **Q3（第 25–36 周）：控制器 + 传感器 + EKF**

---

## **第 25–27 周：飞控控制器（核心）**

学习：

* AC_AttitudeControl
* AC_PosControl
* 陀螺仪 → 姿态控制链路
* 微分 / 积分抑制

📝成果：画出完整控制链路图

---

## **第 28–29 周：控制参数实验**

任务：

* 调整姿态控制 PID
* 比较不同 PID 的飞行行为（仿真）
* 记录 Log 数据差异

📝成果：PID 调参理解

---

## **第 30–31 周：传感器驱动（GPS/IMU/Baro）**

阅读：

* gps.cpp
* AP_InertialSensor
* baro.cpp
* 了解数据流向 EKF

📝成果：能定位 IMU 代码的更新点

---

## **第 32–33 周：EKF 数学基础**

学习：

* 卡尔曼滤波
* 扩展卡尔曼滤波（EKF）
* 噪声模型（Q/R）

📝成果：你能解释 EKF 为什么要线性化

---

## **第 34–36 周：阅读 ArduPilot EKF2/3**

重点：

* 状态向量定义
* IMU 预测
* GPS 更新
* Baro 更新
* Reset 机制

📝成果：你能用白板画出 ArduPilot EKF 数据流

---

---

# 🟩 **Q4（第 37–52 周）：完整飞控功能开发（作品阶段）**

---

## **第 37 周：选择你的项目方向**

可选题：

1. 新飞行模式
2. 新 Mission 指令
3. 自定义 MAVLink + GCS
4. Companion computer 智能控制
5. 自动降落改进
6. 智能跟随

📝成果：选题 + 需求文档

---

## **第 38–40 周：实现模式基础骨架**

任务：

* 建文件
* 注册 mode
* 增加参数
* 增加 run loop

📝成果：Mode V1

---

## **第 41–44 周：加入控制逻辑**

任务：

* 加入高度控制
* 加入水平运动逻辑
* 加入 failsafe
* 进行 SITL 飞行测试

📝成果：Mode V2（可飞）

---

## **第 45–46 周：自定义 MAVLink + GCS 展示**

任务：

* 飞控上报自定义状态
* 在 MAVProxy / MissionPlanner 显示
* 加 UI 界面（可用 PyQt）

📝成果：GCS 展示界面

---

## **第 47–48 周：联调**

任务：

* MAVLink 指令控制 Mode
* 参数调试
* 问题记录 + 修复

---

## **第 49–51 周：性能优化**

任务：

* 控制器优化
* 加参数限制
* 重构部分代码
* 性能分析（profiler）

---

## **第 52 周：最后交付**

任务：

* 写文档
* 录一段视频
* 做项目总结

📝成果：
🎉 你的第一个真正可展示的 ArduPilot 扩展功能！

---

# ✅ 现在你可以告诉我：

**需要我把这一整套内容做成可视化技能路线图（Canvas）吗？**
我可以为你生成：

* 技能树
* 时间线看板
* 学习路线图
* 项目路线图

也可以继续帮你：
📍 制定 **每日计划**
📍 制定 **课程清单（含资源）**
📍 制定 **嵌入式补课专题图**

你想继续哪个？
