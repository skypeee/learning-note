import os
import logging
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

from bot import send_daily_prompt, send_feishu_message

logger = logging.getLogger(__name__)

# 需要推送的用户列表（目前只有自己）
# 后续从配置文件读取
TARGET_USERS = os.environ.get(
    "TARGET_USERS",
    "替换为你的飞书open_id",
).split(",")

def init_scheduler(app) -> BackgroundScheduler:
    """初始化定时任务

    Args:
        app: Flask app 实例

    Returns:
        配置好的 scheduler
    """
    scheduler = BackgroundScheduler()

    morning_hour = int(os.environ.get("SCHEDULE_MORNING_HOUR", 8))
    evening_hour = int(os.environ.get("SCHEDULE_EVENING_HOUR", 21))

    # 早间推送 — 飞控储备
    scheduler.add_job(
        _morning_push,
        "cron",
        hour=morning_hour,
        minute=0,
        id="morning_push",
        replace_existing=True,
    )

    # 午间推送 — AI/全栈碎片知识（5 维度推送）
    scheduler.add_job(
        _noon_push,
        "cron",
        hour=12,
        minute=30,
        id="noon_push",
        replace_existing=True,
    )

    # 晚间推送 — 项目任务
    scheduler.add_job(
        _evening_push,
        "cron",
        hour=evening_hour,
        minute=0,
        id="evening_push",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        f"Scheduler started: morning={morning_hour}:00, "
        f"noon=12:30, evening={evening_hour}:00"
    )
    return scheduler

def _build_5d_push_message() -> str:
    """构建 6 维度碎片知识推送消息（含到期复习提醒）"""
    from prompts import get_week_push_topics, get_due_reviews

    today_str = date.today().strftime("%Y-%m-%d")
    parts = []

    # 检查到期复习
    reviews = get_due_reviews()
    if reviews:
        parts.append(f"**🔔 今日复习（{today_str}）**")
        for r in reviews:
            parts.append(f"- **{r['type']}**：{r['content']}")
        parts.append("")

    topics = get_week_push_topics()
    if not topics:
        return ""

    categories = {
        "ai": "🤖 AI",
        "au": "🚁 AU/ArduPilot",
        "fc": "🎯 飞控",
        "stack": "🔧 全栈",
        "project": "📋 项目",
        "proj_tech": "⚙️ 技术知识",
    }

    if parts:
        parts.append(f"**今日碎片知识（6 维度）**")
    else:
        parts.append(f"**今日碎片知识（{today_str}）**")

    for key, label in categories.items():
        topic = topics.get(key, "")
        if topic:
            parts.append(f"**{label}**：{topic}")

    parts.append("\n挑一个感兴趣的搜一搜，5-15 分钟即可。")
    return "\n".join(parts)

def _morning_push():
    """早间推送：飞控储备"""
    logger.info("Morning push triggered")
    for user_id in TARGET_USERS:
        user_id = user_id.strip()
        if not user_id or user_id == "替换为你的飞书open_id":
            continue
        try:
            send_daily_prompt(user_id)
        except Exception as e:
            logger.error(f"Morning push failed for {user_id}: {e}")

def _noon_push():
    """午间推送：6 维度碎片知识（AI/AU/飞控/全栈/项目/技术知识）"""
    logger.info("Noon push triggered")
    message = _build_5d_push_message()
    if not message:
        logger.info("No week topics found, skipping noon push")
        return
    for user_id in TARGET_USERS:
        user_id = user_id.strip()
        if not user_id or user_id == "替换为你的飞书open_id":
            continue
        try:
            send_feishu_message(user_id, message)
        except Exception as e:
            logger.error(f"Noon push failed for {user_id}: {e}")

def _evening_push():
    """晚间推送：项目任务"""
    logger.info("Evening push triggered")
    for user_id in TARGET_USERS:
        user_id = user_id.strip()
        if not user_id or user_id == "替换为你的飞书open_id":
            continue
        try:
            send_daily_prompt(user_id)
        except Exception as e:
            logger.error(f"Evening push failed for {user_id}: {e}")
