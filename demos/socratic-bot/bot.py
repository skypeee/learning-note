import os
import re
import json
import logging
from pathlib import Path
from datetime import datetime

import lark_oapi as lark
from lark_oapi.api.im.v1 import (
    CreateMessageRequest, CreateMessageRequestBody,
    P2ImMessageReceiveV1,
)

from llm import chat
from prompts import (
    build_system_prompt,
    build_daily_prompt,
    find_task_by_name,
    mark_task_done,
    add_review_entry,
    get_due_reviews,
    get_acceptance_question,
    mark_review_done,
    generate_weekly_report,
)

logger = logging.getLogger(__name__)

# 飞书客户端
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

if APP_ID and APP_SECRET:
    client = lark.Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()
else:
    client = None

SESSIONS_DIR = Path(__file__).parent / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)


class SessionManager:
    """管理会话上下文窗口"""

    MAX_TOKENS = 4000       # 历史上下文 token 上限（粗略估算）
    MAX_MESSAGES = 20       # 最多保留 20 轮对话

    @staticmethod
    def get_messages(user_id: str) -> list[dict]:
        """获取当前对话历史"""
        path = SESSIONS_DIR / f"{user_id}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            messages = data.get("messages", [])
        else:
            messages = []

        # 如果没有历史，返回 system prompt
        if not messages:
            return [{"role": "system", "content": build_system_prompt()}]

        # 从后往前截取，确保 token 数不超限
        result = messages[-SessionManager.MAX_MESSAGES:]
        while SessionManager._estimate_tokens(result) > SessionManager.MAX_TOKENS and len(result) > 2:
            result.pop(0)  # 删除最旧的消息

        # 如果系统 prompt 过期（不在历史中），重新注入
        has_system = any(m.get("role") == "system" for m in result)
        if not has_system:
            result.insert(0, {"role": "system", "content": build_system_prompt()})

        return result

    @staticmethod
    def add_message(user_id: str, role: str, content: str) -> list[dict]:
        """添加一条消息到 session 并保存"""
        messages = SessionManager.get_messages(user_id)
        messages.append({"role": role, "content": content})
        SessionManager._save(user_id, messages)
        return messages

    @staticmethod
    def mark_task_completed(user_id: str, task_name: str) -> str:
        """标记任务完成，返回确认消息 + 验收问题"""
        # 先查找任务类型
        task = find_task_by_name(task_name)
        task_type = task["type"] if task else ""

        success = mark_task_done(task_name)
        if success:
            # 添加复习追踪
            add_review_entry(task_name)
            SessionManager.add_message(user_id, "system", f"[任务完成] {task_name} ✅")

            # 生成验收问题
            question = get_acceptance_question(task_type)
            return f"已标记「{task_name}」为完成 ✅。\n\n🔍 **验收**：{question}"
        return f"未找到任务「{task_name}」，请确认任务名称。"

    @staticmethod
    def _save(user_id: str, messages: list[dict]):
        path = SESSIONS_DIR / f"{user_id}.json"
        data = {
            "user_id": user_id,
            "messages": messages,
            "updated_at": datetime.now().isoformat(),
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _estimate_tokens(messages: list[dict]) -> int:
        """粗略估算 token 数"""
        total_bytes = 0
        for msg in messages:
            content = msg.get("content", "")
            total_bytes += len(content.encode("utf-8"))
        return total_bytes // 3  # ~3 bytes per token (rough estimate for mixed CJK/EN)


# ──────────────────────────────────────────────
# 任务完成检测
# ──────────────────────────────────────────────
COMPLETION_KEYWORDS = ["完成了", "做完了", "完成啦", "搞定了", "搞定了", "✅", "搞完", "搞定", "done"]
REVIEW_KEYWORDS = ["复习完了", "复习过了", "复习完成", "复习了", "recalled", "记住了"]
REPORT_KEYWORDS = ["周报", "本周进度", "进度报告", "本周复盘", "进度怎么样"]


def detect_task_completion(user_text: str, recent_messages: list[dict]) -> str | None:
    """检测用户是否表示任务完成，返回任务名或 None"""
    text = user_text.strip().lower()

    # 检查是否包含完成关键词
    has_completion = any(kw in text for kw in COMPLETION_KEYWORDS)
    if not has_completion:
        return None

    # 从用户消息中提取任务名
    for kw in COMPLETION_KEYWORDS:
        task_hint = text.replace(kw, "").strip()
        if len(task_hint) > 2:
            return task_hint

    # 如果用户只说"完成了"，从最近的 agent 推送中推断任务
    for msg in reversed(recent_messages[-5:]):
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            # 查找任务名（如 "🔧 全栈主线（P0）：xxx"）
            match = re.search(r"[**]*[🔧📖🔍🤖🚁][^**]*[**]*[：:][**]*(.*?)[**]*[\n（]", content)
            if match:
                return match.group(1).strip()

    return None


def detect_review_completion(user_text: str) -> str | None:
    """检测用户是否表示复习完成，返回知识点名或 None"""
    has_review = any(kw in user_text for kw in REVIEW_KEYWORDS)
    if not has_review:
        return None

    # 从消息中提取知识点名
    for kw in REVIEW_KEYWORDS:
        hint = user_text.replace(kw, "").strip()
        if len(hint) > 2:
            return hint

    # 如果只说"复习完了"，从到期复习中取第一个
    reviews = get_due_reviews()
    if reviews:
        return reviews[0]["content"].split("—")[0].strip()

    return None


# ──────────────────────────────────────────────
# 飞书消息处理
# ──────────────────────────────────────────────

def handle_user_message(user_id: str, user_text: str) -> str:
    """处理用户消息，返回 LLM 回复"""
    messages = SessionManager.get_messages(user_id)

    # 1. 周报查询
    if any(kw in user_text for kw in REPORT_KEYWORDS):
        return generate_weekly_report()

    # 2. 复习完成检测
    review_item = detect_review_completion(user_text)
    if review_item:
        success = mark_review_done(review_item)
        if success:
            return f"复习已记录 ✅。继续加油！"
        # 没匹配到具体知识点，走正常对话

    # 3. 任务完成检测
    task_name = detect_task_completion(user_text, messages)
    if task_name:
        reply = SessionManager.mark_task_completed(user_id, task_name)
        return reply

    # 正常对话
    messages.append({"role": "user", "content": user_text})
    reply = chat(messages)
    messages.append({"role": "assistant", "content": reply})
    SessionManager._save(user_id, messages)

    return reply


def send_feishu_message(user_id: str, content: str):
    """发送消息到飞书"""
    if not client:
        logger.warning("Feishu client not initialized, skipping message send")
        return

    try:
        request = CreateMessageRequest.builder() \
            .receive_id_type("open_id") \
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(user_id)
                .msg_type("text")
                .content(json.dumps({"text": content}))
                .build()
            ) \
            .build()

        response = client.im.v1.message.create(request)
        if not response.success():
            logger.error(f"Failed to send feishu message: {response.code} {response.msg}")
    except Exception as e:
        logger.error(f"Exception sending feishu message: {e}")


def handle_event(data: P2ImMessageReceiveV1):
    """处理飞书事件回调"""
    header = data.header
    event = data.event

    if not event or not event.message:
        return

    message = event.message
    if message.message_type != "text":
        return

    user_id = message.sender.sender_id.open_id
    content = json.loads(message.content).get("text", "").strip()

    if not content:
        return

    logger.info(f"User {user_id}: {content}")
    reply = handle_user_message(user_id, content)
    logger.info(f"Bot: {reply}")

    send_feishu_message(user_id, reply)


def send_daily_prompt(user_id: str):
    """定时任务：发送今日学习任务"""
    messages = SessionManager.get_messages(user_id)

    # 更新 system prompt
    system_prompt = build_daily_prompt()
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = system_prompt
    else:
        messages.insert(0, {"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": "开始今天的学习"})
    reply = chat(messages)
    messages.append({"role": "assistant", "content": reply})
    SessionManager._save(user_id, messages)

    send_feishu_message(user_id, reply)
    logger.info(f"Daily push to {user_id}: {reply[:50]}...")
