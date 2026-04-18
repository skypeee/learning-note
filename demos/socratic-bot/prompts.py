import os
import re
import logging
from datetime import datetime, date
from pathlib import Path

logger = logging.getLogger(__name__)

# 学习仓库根目录
LEARNING_ROOT = Path(
    os.environ.get("LEARNING_NOTE_ROOT", "/Users/duanduanzi/workspace/my-project/learning-note")
)

def read_file(path: str) -> str:
    """读取文件内容，失败返回空字符串"""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to read {path}: {e}")
        return ""

def build_system_prompt() -> str:
    """组合完整的 system prompt"""
    # 基础模板
    base = read_file(str(LEARNING_ROOT / "demos/socratic-bot/prompts.md"))

    # 动态读取用户背景
    skill = read_file(str(LEARNING_ROOT / "SKILL.md"))
    milestones = read_file(str(LEARNING_ROOT / "assessment/milestones.md"))

    context_parts = []
    if skill:
        context_parts.append(f"## 用户技术栈和背景\n{skill}")
    if milestones:
        context_parts.append(f"## 当前里程碑\n{milestones}")

    context = "\n\n".join(context_parts) if context_parts else ""

    return f"{base}\n\n{context}" if context else base

def build_daily_prompt() -> str:
    """生成今日任务的 system prompt，包含 6 维度知识推送 + 到期复习提醒"""
    base = build_system_prompt()
    today_tasks = get_today_tasks()
    today_str = date.today().strftime("%Y-%m-%d")

    task_section = f"\n\n## 今天的任务（{today_str}）\n"
    if today_tasks:
        task_section += today_tasks
    else:
        task_section += "今天没有特定任务，自由引导用户讨论技术话题。"

    # 检查到期复习
    reviews = get_due_reviews()
    review_section = ""
    if reviews:
        review_section = "\n\n## 🔔 今日到期复习（优先完成）\n"
        for r in reviews:
            review_section += f"- **{r['type']}**：{r['content']}\n"

    # 追加 6 维度知识推送
    push_section = "\n\n## 今日知识推送（碎片时间用）\n"
    push_topics = get_week_push_topics()
    if push_topics:
        categories = [
            ("AI", push_topics.get("ai", "")),
            ("AU/ArduPilot", push_topics.get("au", "")),
            ("飞控", push_topics.get("fc", "")),
            ("全栈", push_topics.get("stack", "")),
            ("项目", push_topics.get("project", "")),
            ("项目技术知识", push_topics.get("proj_tech", "")),
        ]
        lines = []
        for cat, topic in categories:
            if topic:
                lines.append(f"- **{cat}**：{topic}")
        if lines:
            push_section += "\n".join(lines)
        else:
            push_section += "围绕当前周任务自由引导。"
    else:
        push_section += "围绕当前里程碑自由引导。"

    return base + task_section + review_section + push_section


def get_due_reviews() -> list[dict]:
    """检查今天到期需要复习的知识点"""
    today = date.today()
    reviews = []

    # 1. 检查英语词汇复习
    vocab_path = LEARNING_ROOT / "english/vocabulary.md"
    vocab_text = read_file(str(vocab_path))
    if vocab_text:
        # 查找 "下次复习：YYYY-MM-DD" 或 "下次复习：M/D"
        for line in vocab_text.split("\n"):
            if "下次复习" in line:
                # 提取日期
                date_match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", line)
                if date_match:
                    review_date = date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
                    if review_date <= today:
                        # 找到对应的词汇段落
                        reviews.append({
                            "type": "📖 英语词汇",
                            "content": "复习已学生词（共 13 词），逐个回忆含义和语境"
                        })
                        break

    # 2. 检查飞控知识点复习（EKF _meta.md）
    ekf_path = LEARNING_ROOT / "notes/topics/ekf/_meta.md"
    ekf_text = read_file(str(ekf_path))
    if ekf_text:
        due_items = []
        for line in ekf_text.split("\n"):
            if "📖 已读" in line and "⬜ 未实验" not in line and "⬜ 未读" not in line:
                # 提取知识点名
                item_match = re.match(r"\|\s*(.+?)\s*\|", line)
                if item_match:
                    due_items.append(item_match.group(1).strip())
        if due_items:
            reviews.append({
                "type": "🎯 飞控知识点",
                "content": f"EKF 知识点间隔复习：{', '.join(due_items[:3])}"
            })

    # 3. 检查每周计划中的间隔复习标记
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if plan_text:
        today_strs = [today.strftime("%-m/%-d"), today.strftime("%m/%d")]
        for ts in today_strs:
            if ts in plan_text:
                # 检查今天任务行是否有"复习"字样
                lines = plan_text.split("\n")
                for i, line in enumerate(lines):
                    if ts in line and ("复习" in line or "间隔复习" in line):
                        task_match = re.match(r"\|[^|]*\|[^|]*\|[^|]*\|[^|]*(飞控[^|]+)\|", line)
                        if task_match:
                            reviews.append({
                                "type": "🎯 飞控复习",
                                "content": task_match.group(1).strip()
                            })
                        break

    return reviews

def get_week_push_topics() -> dict:
    """从 weekly-plan.md 提取当前周的推送主题，按 5 维度映射"""
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return {}

    # 周主题映射表：根据每周的技术栈描述，提取 5 维度内容
    week_patterns = [
        # Week 2: TypeScript + React + Docker Compose + JWT + WebSocket
        {
            "week_kw": "Week 2",
            "ai": "TS 类型系统在 AI 辅助编程中的价值（搜「TypeScript AI coding best practices」）",
            "au": "ArduPilot 目录结构和子模块（搜 `ArduPilot directory structure`），各模块如何协作",
            "fc": "EKF gpsGood/gpsGlitch/gpsInhibit 检测逻辑，结合 Pixhawk 实际飞行场景",
            "stack": "TypeScript + Vite + React 项目初始化，tsconfig 关键配置项",
            "project": "云平台 PRD 怎么写——目标用户、核心价值、MVP 范围界定",
            "proj_tech": "Docker Compose 多服务编排：前端/Nginx/后端/Redis/MySQL/MQTT 一键启动",
        },
        # Week 3: React 表单 + Redis + gRPC + MQTT
        {
            "week_kw": "Week 3",
            "ai": "AI 辅助写 React 组件——用 Copilot/Claude 快速生成列表/详情/表单",
            "au": "ArduPilot 飞行模式（AUTO/RTL/LOITER）状态机切换逻辑",
            "fc": "EKF innovation 是什么，GPS 融合拒绝的判定条件",
            "stack": "Redis 数据结构选型：String vs Hash vs ZSet 在设备状态场景下的选择",
            "project": "设备影子完整链路设计：MQTT → 后端 → Redis → gRPC → 前端",
            "proj_tech": "gRPC + Protobuf 跨语言 IDL 定义，服务间通信 vs REST 对比",
        },
        # Week 4: 多租户 + MySQL + Elasticsearch + Nginx
        {
            "week_kw": "Week 4",
            "ai": "RAG 中的 chunking 策略——设备日志怎么做最优切片",
            "au": "ArduPilot failsafe 机制（RTL/land/crash 触发条件）",
            "fc": "EKF GPS 融合前的"防御"机制——哪些校验在做",
            "stack": "MySQL 复合索引设计 + EXPLAIN 执行计划分析",
            "project": "多租户数据隔离方案选型：schema-per-tenant vs tenant_id",
            "proj_tech": "Elasticsearch + Kibana 日志采集聚合，Nginx 反向代理限流配置",
        },
        # Week 5: AI 日志分析 + K8s + Helm
        {
            "week_kw": "Week 5",
            "ai": "LLM 流式输出 + SSE 推送——怎么实现 AI 日志分析的实时反馈",
            "au": "ArduPilot HIL 仿真，怎么从 SITL 过渡到硬件在环",
            "fc": "Scheduler FAST_TASK vs SCHED_TASK 优先级对系统实时性的影响",
            "stack": "K8s Deployment vs StatefulSet 区别，StatefulSet 管理有状态服务",
            "project": "AI 日志分析 RAG 链路：日志采集 → 向量化 → 检索 → LLM 分析",
            "proj_tech": "Helm Chart 编写——全栈服务打包，ConfigMap/Secret/HPA 配置",
        },
        # Week 6: CI/CD + 可观测性 + 混沌工程
        {
            "week_kw": "Week 6",
            "ai": "AI 代码审查——用 LLM 做 PR 自动 review 的可行性",
            "au": "ArduPilot 日志系统 DataFlash/AP_Logger，二进制格式解析",
            "fc": "飞控初始化设置流程，AP_HAL 入口到各子系统初始化",
            "stack": "Prometheus 自定义 metrics 暴露，Jaeger 全链路追踪原理",
            "project": "混沌工程：Redis 宕机/DB 慢查询/MQ 断连的 RTO/RPO 测量",
            "proj_tech": "GitHub Actions CI/CD 流水线设计 + Docker multi-stage build 镜像优化",
        },
        # Week 7: 全链路压测 + 性能调优 + 架构总结
        {
            "week_kw": "Week 7",
            "ai": "LLM 输出质量评估——怎么建立 AI 日志分析的评估基准",
            "au": "ArduPilot 社区贡献指南，怎么给主线提 PR",
            "fc": "飞控全链路知识回顾口述：从入口到 EKF 到电机控制",
            "stack": "React 性能优化：bundle 分析 + 代码分割 + memo/useMemo/useCallback",
            "project": "云平台 MVP 全链路压测报告——端到端延迟 <500ms",
            "proj_tech": "架构总结文档怎么写——技术决策回顾 + 踩坑记录沉淀",
        },
    ]

    today = date.today()
    for pat in week_patterns:
        if pat["week_kw"] in plan_text:
            # 简单判断：如果当前日期在对应周的时间范围内
            week_ranges = {
                "Week 2": (date(2026, 4, 19), date(2026, 4, 25)),
                "Week 3": (date(2026, 4, 26), date(2026, 5, 2)),
                "Week 4": (date(2026, 5, 2), date(2026, 5, 8)),
                "Week 5": (date(2026, 5, 10), date(2026, 5, 16)),
                "Week 6": (date(2026, 5, 17), date(2026, 5, 23)),
                "Week 7": (date(2026, 5, 24), date(2026, 5, 30)),
            }
            wk_key = pat["week_kw"]
            if wk_key in week_ranges:
                start, end = week_ranges[wk_key]
                if start <= today <= end:
                    return {
                        "ai": pat["ai"],
                        "au": pat["au"],
                        "fc": pat["fc"],
                        "stack": pat["stack"],
                        "project": pat["project"],
                        "proj_tech": pat["proj_tech"],
                    }

    return {}

def get_today_tasks() -> str:
    """从 weekly-plan.md 解析今天任务

    搜索 markdown 表格中匹配今天的日期行。
    """
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return ""

    today = date.today()
    today_strs = [
        today.strftime("%-m/%-d"),   # 4/18
        today.strftime("%m/%d"),     # 04/18
        today.strftime("%Y-%m-%d"),  # 2026-04-18
    ]

    lines = plan_text.split("\n")
    tasks = []
    in_task_section = False

    for i, line in enumerate(lines):
        # 找到包含今天日期的标题行
        for ts in today_strs:
            if ts in line and line.strip().startswith("##"):
                in_task_section = True
                tasks.append(f"### {line.strip().lstrip('#').strip()}")
                break

        if in_task_section:
            # 收集后续行直到下一个同级标题
            if line.strip().startswith("## ") and i > 0:
                # 检查是否已经是下一个周/天的标题
                for ts in today_strs:
                    if ts in line:
                        continue
                # 遇到下一个 ## 标题就停止
                if not any(ts in line for ts in today_strs):
                    break

            # 提取任务表格中今天的行
            if "|" in line and "任务" in line or "|" in line and "状态" in line:
                tasks.append(line)
            elif "|" in line and "⬜" in line:
                tasks.append(line)

    if not tasks:
        # 降级：搜索包含今天日期的行
        for i, line in enumerate(lines):
            for ts in today_strs:
                if ts in line:
                    # 取该行前后各 3 行
                    start = max(0, i - 2)
                    end = min(len(lines), i + 4)
                    return "\n".join(lines[start:end])

    return "\n".join(tasks) if tasks else ""
