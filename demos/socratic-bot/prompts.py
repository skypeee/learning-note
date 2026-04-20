import os
import re
import logging
from datetime import datetime, date, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# 学习仓库根目录
LEARNING_ROOT = Path(
    os.environ.get("LEARNING_NOTE_ROOT", "/Users/duanduanzi/workspace/my-project/learning-note")
)

# 艾宾浩斯复习间隔（天）
REVIEW_INTERVALS = [1, 3, 7, 15]

# ──────────────────────────────────────────────
# 苏格拉底核心规则（内嵌，替代 prompts.md）
# ──────────────────────────────────────────────
SOCRATIC_RULES = """你是一个苏格拉底式学习助手，通过提问引导用户深入理解技术。

## 核心规则
1. **每次只问一个问题** — 不要一次抛出多个
2. **等用户回答再继续** — 用户没回答前不问下一个
3. **答对了就追问** — 进入下一层或新话题
4. **答错了就引导** — 用提示性问题帮用户自己想到，绝不直接给答案
5. **保持简洁** — 回复控制在 150 字以内

## 对话风格
- 像工程师对工程师对话，不是老师对学生
- 问题要具体，不要泛泛而谈
- 根据用户当前任务进度调整话题深度"""


def read_file(path: str) -> str:
    """读取文件内容，失败返回空字符串"""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to read {path}: {e}")
        return ""


def build_user_context() -> str:
    """从 SKILL.md 提取关键信息，而非加载全文"""
    skill_path = LEARNING_ROOT / "SKILL.md"
    skill_text = read_file(str(skill_path))
    if not skill_text:
        return ""

    # 提取关键句
    context_parts = []

    # 当前阶段
    for line in skill_text.split("\n"):
        if "SITL" in line or "HIL" in line:
            context_parts.append(f"- 当前阶段：{line.strip().strip('-').strip()}")
            break

    # 硬件
    if "Pixhawk" in skill_text:
        context_parts.append("- 硬件：Pixhawk 6C + ESP32-CAM")

    # 优势
    if "7年" in skill_text:
        context_parts.append("- 优势：7年系统级开发经验，Senior System Analyst")

    # 短板
    short_lines = []
    in_shortcomings = False
    for line in skill_text.split("\n"):
        if "我的短板" in line or "短板" in line:
            in_shortcomings = True
            continue
        if in_shortcomings:
            if line.strip().startswith("-"):
                short_lines.append(line.strip().strip("-").strip())
            elif line.strip() == "":
                continue
            elif not line.strip().startswith("-"):
                break
    if short_lines:
        context_parts.append(f"- 短板：{', '.join(short_lines[:3])}")

    # 对 AI 的要求
    ai_reqs = []
    in_ai_reqs = False
    for line in skill_text.split("\n"):
        if "对 AI 的要求" in line:
            in_ai_reqs = True
            continue
        if in_ai_reqs:
            if line.strip().startswith("1.") or line.strip().startswith("2."):
                ai_reqs.append(line.strip())
            elif line.strip() == "":
                continue
            elif in_ai_reqs and line.strip() and not line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
                break
            elif line.strip().startswith(("3.", "4.", "5.", "6.", "7.")):
                ai_reqs.append(line.strip())
    if ai_reqs:
        context_parts.append(f"- AI 要求：{'；'.join(ai_reqs[:3])}")

    return "\n".join(context_parts)

def build_context_aware_prompt() -> str:
    """构建动态 system prompt：苏格拉底规则 + 用户精简背景 + 当前状态"""
    parts = [SOCRATIC_RULES]

    # 用户背景
    user_ctx = build_user_context()
    if user_ctx:
        parts.append(f"## 用户背景\n{user_ctx}")

    # 今日到期复习
    reviews = get_due_reviews()
    if reviews:
        review_lines = ["## 今日到期复习（优先）"]
        for r in reviews:
            review_lines.append(f"- {r['type']}：{r['content']}")
        parts.append("\n".join(review_lines))

    # 当前可领取任务
    tasks = get_today_tasks()
    if tasks:
        parts.append(f"## 当前可领取任务\n{tasks}")
    else:
        parts.append("## 当前状态\n今天没有特定任务，自由引导用户讨论技术话题。")

    return "\n\n---\n\n".join(parts)


def build_system_prompt() -> str:
    """兼容旧接口，调用 build_context_aware_prompt"""
    return build_context_aware_prompt()

def build_daily_prompt() -> str:
    """生成定时推送的 system prompt"""
    return build_context_aware_prompt()


def get_due_reviews() -> list[dict]:
    """从 review-tracker.md 检查今天到期需要复习的知识点"""
    tracker_path = LEARNING_ROOT / "assessment/review-tracker.md"
    tracker_text = read_file(str(tracker_path))
    if not tracker_text:
        return []

    today = date.today()
    reviews = []
    lines = tracker_text.split("\n")

    for line in lines:
        # 匹配复习行：| xxx | 2026-04-19 | ⬜ 4/20 | ⬜ 4/22 | ...
        if "⬜" not in line:
            continue

        # 提取首次学习日期
        date_match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", line)
        if not date_match:
            continue

        try:
            first_date = date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        except ValueError:
            continue

        # 提取知识点名（第一个 | 后的内容）
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if not parts:
            continue

        item_name = parts[0]

        # 检查每个复习轮次是否到期
        for i, interval in enumerate(REVIEW_INTERVALS):
            review_date = first_date + timedelta(days=interval)
            review_str = f"{review_date.month}/{review_date.day}"

            # 找到对应的复习列
            col_idx = i + 2  # R1 在第3列（索引2）
            if col_idx < len(parts):
                cell = parts[col_idx]
                # 如果标记了 ⬜ 且日期已到期
                if "⬜" in cell and review_date <= today:
                    # 前一轮是否已完成？R1 不需要前置检查
                    prev_done = (i == 0)
                    if i > 0:
                        prev_cell = parts[col_idx - 1]  # 前一列的单元格
                        prev_done = "✅" in prev_cell

                    if prev_done:
                        # 判断是否有阶段列（最后一列可能是阶段名，如 S0/S1）
                        last_part = parts[-1].strip()
                        stage = last_part if last_part in ("S0", "S1", "S2", "S3") else ""
                        reviews.append({
                            "type": "📅 间隔复习",
                            "content": f"{item_name} — 第{i+1}次复习（{review_str}到期）",
                            "stage": stage,
                        })
                        break  # 每个知识点只报最早的到期轮次

    return reviews

def get_week_push_topics() -> dict:
    """从当前周任务池提取推送主题"""
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return {}

    week_key, week_start = _find_current_week(plan_text)
    if not week_key:
        return {}

    lines = plan_text.split("\n")
    sections = {}
    for i in range(week_start, len(lines)):
        if "### P0 主线" in lines[i]:
            sections["p0"] = i
        elif "### P1 进阶" in lines[i]:
            sections["p1"] = i
        elif "### P2 AI前沿" in lines[i]:
            sections["p2"] = i
        elif "### P3 探索" in lines[i]:
            sections["p3"] = i
        elif lines[i].strip().startswith("## ") and i > week_start:
            break

    section_order = [sections.get(s, -1) for s in ["p0", "p1", "p2", "p3"]]

    def parse_section(idx: int) -> list[dict]:
        if idx < 0:
            return []
        end = section_order[idx + 1] if idx + 1 < len(section_order) and section_order[idx + 1] > 0 else len(lines)
        return _parse_task_table(lines, idx + 1)

    p0 = parse_section(0)
    p1 = parse_section(1)
    p2 = parse_section(2)
    p3 = parse_section(3)

    return {
        "ai": _get_first_pending(p2)["name"] if _get_first_pending(p2) else "阅读 AI/LLM 前沿",
        "au": (_get_first_pending(p3, "AU") or {}).get("name", "阅读 ArduPilot wiki"),
        "fc": (_get_first_pending(p3, "飞控") or {}).get("name", "复习飞控知识点"),
        "stack": (_get_first_pending(p0) or {}).get("name", "全栈项目推进"),
        "project": (next((t for t in p0 if t.get("type") == "项目" and "⬜" in t["status"]), None) or {}).get("name", "项目推进"),
        "proj_tech": (_get_first_pending(p1, "技术调研") or {}).get("name", "技术调研"),
    }

def _find_current_week(plan_text: str) -> tuple[str, int]:
    """找到当前日期所在的周 section

    Returns:
        (week_section_title, start_line_index)
    """
    today = date.today()
    week_ranges = {
        "Week 2": (date(2026, 4, 19), date(2026, 4, 25)),
        "Week 3": (date(2026, 4, 26), date(2026, 5, 2)),
        "Week 4": (date(2026, 5, 2), date(2026, 5, 8)),
        "Week 5": (date(2026, 5, 10), date(2026, 5, 16)),
        "Week 6": (date(2026, 5, 17), date(2026, 5, 23)),
        "Week 7": (date(2026, 5, 24), date(2026, 5, 30)),
    }

    lines = plan_text.split("\n")
    for wk_key, (start, end) in week_ranges.items():
        if start <= today <= end:
            for i, line in enumerate(lines):
                if wk_key in line and line.strip().startswith("##"):
                    return wk_key, i

    return "", -1


def _parse_task_table(lines: list[str], start: int) -> list[dict]:
    """解析 P0/P1/P2 任务表格，返回任务列表"""
    tasks = []
    i = start
    while i < len(lines):
        line = lines[i]
        # 遇到下一个 ## 标题或文件结束，停止
        if line.strip().startswith("## ") and i > start:
            break
        # 解析任务行：| # | 任务描述 | 类型 | 状态 | 前置 |
        if "|" in line and ("⬜" in line or "✅" in line or "▶️" in line):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 4:
                tasks.append({
                    "id": parts[0],
                    "name": parts[1],
                    "type": parts[2],
                    "status": parts[3],
                    "prereq": parts[4] if len(parts) > 4 else "—",
                })
        i += 1
    return tasks


def _get_first_pending(tasks: list[dict], task_type: str = None) -> dict | None:
    """找到第一个未完成的任务"""
    for t in tasks:
        if "⬜" in t["status"] and (task_type is None or t["type"] == task_type):
            return t
    return None


def get_today_tasks() -> str:
    """从任务池获取多方向建议任务 + 到期复习提醒"""
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return ""

    week_key, week_start = _find_current_week(plan_text)
    if not week_key:
        return f"今天不在计划周范围内，自由探索学习。"

    lines = plan_text.split("\n")

    # 找到各 section 起始行
    sections = {}
    for i in range(week_start, len(lines)):
        if "### P0 主线" in lines[i]:
            sections["p0"] = i
        elif "### P1 进阶" in lines[i]:
            sections["p1"] = i
        elif "### P2 AI前沿" in lines[i]:
            sections["p2"] = i
        elif "### P3 探索" in lines[i]:
            sections["p3"] = i
        elif lines[i].strip().startswith("## ") and i > week_start:
            break

    section_order = ["p0", "p1", "p2", "p3"]
    start_lines = [sections.get(s, -1) for s in section_order]

    def parse_section(idx: int) -> list[dict]:
        if idx < 0:
            return []
        end = start_lines[idx + 1] if idx + 1 < len(start_lines) and start_lines[idx + 1] > 0 else len(lines)
        return _parse_task_table(lines, idx + 1)

    all_sections = [parse_section(i) for i in range(len(start_lines)) if start_lines[i] >= 0]

    # 到期复习
    reviews = get_due_reviews()

    parts = [f"**当前周**：{week_key}\n"]

    if reviews:
        parts.append("**📅 今日到期复习（优先）**")
        for r in reviews:
            parts.append(f"- {r['type']}：{r['content']}")
        parts.append("")

    # P0 主线
    if all_sections:
        p0 = _get_first_pending(all_sections[0])
        if p0:
            parts.append(f"**🔧 全栈主线（P0）**：{p0['name']}（前置：{p0.get('prereq', '—')}）")

    # P1 进阶
    if len(all_sections) > 1:
        p1_tasks = all_sections[1]
        eng = _get_first_pending(p1_tasks, "英语")
        tech = _get_first_pending(p1_tasks, "技术调研")
        if eng:
            parts.append(f"**📖 英语（P1）**：{eng['name']}")
        if tech:
            parts.append(f"**🔍 技术调研（P1）**：{tech['name']}")

    # P2 AI前沿
    if len(all_sections) > 2:
        ai = _get_first_pending(all_sections[2])
        if ai:
            parts.append(f"**🤖 AI前沿（P2）**：{ai['name']}")

    # P3 探索
    if len(all_sections) > 3:
        fc = _get_first_pending(all_sections[3], "飞控") or _get_first_pending(all_sections[3], "AU")
        if fc:
            parts.append(f"**🚁 飞控/AU（P3）**：{fc['name']}")

    if len(parts) <= 1:
        parts.append("所有任务已完成 🎉，可以进入下一周或自由探索。")

    parts.append("\n挑一个方向，回复任务名或方向即可。")
    return "\n".join(parts)


# ──────────────────────────────────────────────
# 任务完成追踪
# ──────────────────────────────────────────────

def find_task_by_name(task_name: str) -> dict | None:
    """根据任务名在 weekly-plan.md 中查找"""
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return None

    lines = plan_text.split("\n")
    for line in lines:
        if "⬜" in line and task_name in line:
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 4:
                return {
                    "name": parts[1],
                    "type": parts[2],
                    "status": parts[3],
                }
    return None


def mark_task_done(task_name: str) -> bool:
    """将 weekly-plan.md 中的任务标记为 ✅"""
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return False

    lines = plan_text.split("\n")
    updated = False
    for i, line in enumerate(lines):
        if "⬜" in line and task_name in line:
            lines[i] = line.replace("⬜", "✅", 1)
            updated = True
            break

    if updated:
        plan_path.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"Task marked done: {task_name}")

    return updated


def add_review_entry(knowledge_point: str, stage: str = "") -> None:
    """在 review-tracker.md 中添加新的复习条目"""
    tracker_path = LEARNING_ROOT / "assessment/review-tracker.md"
    tracker_text = read_file(str(tracker_path))
    if not tracker_text:
        return

    today_str = date.today().strftime("%Y-%m-%d")
    r1 = (date.today() + timedelta(days=1)).strftime("%-m/%-d")
    r2 = (date.today() + timedelta(days=3)).strftime("%-m/%-d")
    r3 = (date.today() + timedelta(days=7)).strftime("%-m/%-d")
    r4 = (date.today() + timedelta(days=15)).strftime("%-m/%-d")

    # 判断属于哪个 section（飞控/AI/英语）
    section = "AI 知识点"  # 默认
    if "EKF" in knowledge_point or "飞控" in knowledge_point or "Scheduler" in knowledge_point or "MAVLink" in knowledge_point or "AP_" in knowledge_point or "HAL" in knowledge_point:
        section = "飞控知识点"
    elif "英语" in knowledge_point or len(knowledge_point) < 20:  # 短的可能单词
        section = "英语词汇"

    # 找到对应 section 的最后一行，插入新条目
    lines = tracker_text.split("\n")
    insert_idx = len(lines)
    for i, line in enumerate(lines):
        if section in line and line.startswith("## "):
            # 找到 section 标题
            # 找到该 section 的最后一行（下一个 ## 之前）
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("## "):
                    insert_idx = j
                    break
            else:
                insert_idx = len(lines)
            break

    # 检查是否已经存在
    for line in lines:
        if knowledge_point in line and today_str in line:
            return  # 已存在，不重复添加

    stage_suffix = f" | {stage}" if stage else ""
    new_entry = f"| {knowledge_point} | {today_str} | ⬜ {r1} | ⬜ {r2} | ⬜ {r3} | ⬜ {r4}{stage_suffix} |"

    lines.insert(insert_idx, new_entry)
    tracker_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"Review entry added: {knowledge_point}")


# ──────────────────────────────────────────────
# Iter2: 验收检查
# ──────────────────────────────────────────────

ACCEPTANCE_QUESTIONS = {
    "全栈": [
        "项目跑通了吗？能 `docker-compose up` 启动？",
        "代码写完后测试过吗？有没有 edge case？",
        "前端页面能在浏览器正常渲染吗？",
    ],
    "英语": [
        "刚才读的段落能用自己的话复述一遍吗？",
        "记的生词还能记住几个？试着回忆一下。",
    ],
    "技术调研": [
        "调研结论是什么？能用一句话说清楚核心发现吗？",
        "这个技术选型对云平台项目有什么直接影响？",
    ],
    "AI前沿": [
        "这个 AI 技术的核心价值是什么？",
        "它和我们现在的项目有什么关联？",
    ],
    "飞控": [
        "能用你自己的话解释这个机制的完整流程吗？",
        "如果这个模块出故障，飞控会怎么响应？",
    ],
    "AU": [
        "这个 ArduPilot 模块在整个系统中扮演什么角色？",
        "它和其他模块的依赖关系是什么？",
    ],
    "项目": [
        "这个决策对 MVP 范围有什么影响？",
        "文档写完了吗？核心论点和论据是什么？",
    ],
}


def get_acceptance_question(task_type: str) -> str:
    """根据任务类型返回一个验收问题"""
    import random
    questions = ACCEPTANCE_QUESTIONS.get(task_type, ["这个任务完成了吗？有没有遗漏的地方？"])
    return random.choice(questions)


def mark_review_done(item_name: str) -> bool:
    """在 review-tracker.md 中将某个知识点的最近一轮复习标记为 ✅"""
    tracker_path = LEARNING_ROOT / "assessment/review-tracker.md"
    tracker_text = read_file(str(tracker_path))
    if not tracker_text:
        return False

    lines = tracker_text.split("\n")
    today = date.today()

    for line_idx, line in enumerate(lines):
        if item_name not in line:
            continue

        # 匹配复习行
        date_match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", line)
        if not date_match:
            continue

        try:
            first_date = date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        except ValueError:
            continue

        parts = [p.strip() for p in line.strip().strip("|").split("|")]

        # 找到第一个到期但还未标记的复习轮次
        for i, interval in enumerate(REVIEW_INTERVALS):
            review_date = first_date + timedelta(days=interval)
            if review_date <= today:
                col_idx = i + 2
                if col_idx < len(parts):
                    cell = parts[col_idx]
                    if "⬜" in cell:
                        # 标记为 ✅
                        new_cell = cell.replace("⬜", "✅", 1)
                        parts[col_idx] = new_cell
                        # 重建行
                        new_line = "| " + " | ".join(parts) + " |"
                        lines[line_idx] = new_line
                        tracker_path.write_text("\n".join(lines), encoding="utf-8")
                        logger.info(f"Review marked done: {item_name} R{i+1}")
                        return True

    return False


def generate_weekly_report() -> str:
    """生成本周进度报告"""
    plan_path = LEARNING_ROOT / "assessment/weekly-plan.md"
    plan_text = read_file(str(plan_path))
    if not plan_text:
        return ""

    week_key, week_start = _find_current_week(plan_text)
    if not week_key:
        return "不在计划周范围内。"

    lines = plan_text.split("\n")

    # 统计各 section
    sections = {}
    for i in range(week_start, len(lines)):
        if "### P0 主线" in lines[i]:
            sections["P0 主线"] = i
        elif "### P1 进阶" in lines[i]:
            sections["P1 进阶"] = i
        elif "### P2 AI前沿" in lines[i]:
            sections["P2 AI前沿"] = i
        elif "### P3 探索" in lines[i]:
            sections["P3 探索"] = i
        elif lines[i].strip().startswith("## ") and i > week_start:
            break

    section_order = ["P0 主线", "P1 进阶", "P2 AI前沿", "P3 探索"]
    start_lines = [sections.get(s, -1) for s in section_order]

    def parse_section(idx: int) -> list[dict]:
        if idx < 0:
            return []
        end = start_lines[idx + 1] if idx + 1 < len(start_lines) and start_lines[idx + 1] > 0 else len(lines)
        return _parse_task_table(lines, idx + 1)

    parts = [f"**📊 周报：{week_key}**\n"]

    total_done = 0
    total_tasks = 0

    for sec_name, idx in zip(section_order, range(len(start_lines))):
        if start_lines[idx] < 0:
            continue
        tasks = parse_section(idx)
        if not tasks:
            continue
        done = sum(1 for t in tasks if "✅" in t["status"])
        total = len(tasks)
        total_done += done
        total_tasks += total
        pct = int(done * 100 / total) if total > 0 else 0
        parts.append(f"**{sec_name}**：{done}/{total}（{pct}%）")

    parts.append("")
    overall_pct = int(total_done * 100 / total_tasks) if total_tasks > 0 else 0
    parts.append(f"**总计**：{total_done}/{total_tasks} 完成（{overall_pct}%）")

    # 复习进度
    reviews = get_due_reviews()
    tracker_path = LEARNING_ROOT / "assessment/review-tracker.md"
    tracker_text = read_file(str(tracker_path))
    if tracker_text:
        total_review = 0
        done_review = 0
        for line in tracker_text.split("\n"):
            if "⬜" in line or "✅" in line:
                for interval in REVIEW_INTERVALS:
                    total_review += 1
                    if "✅" in line:
                        done_review += 1
        if total_review > 0:
            review_pct = int(done_review * 100 / total_review)
            parts.append(f"**复习进度**：{done_review}/{total_review}（{review_pct}%）")

    # 建议
    if overall_pct >= 70:
        parts.append("\n进度正常，周末可以加一个额外学习任务。")
    elif overall_pct >= 50:
        parts.append("\n进度还行，周末补一下未完成的任务。")
    else:
        parts.append("\n进度落后，建议下周砍掉非核心任务，只保主线。")

    return "\n".join(parts)
