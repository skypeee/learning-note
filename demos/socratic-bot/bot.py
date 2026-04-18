import os
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
from prompts import build_system_prompt, build_daily_prompt

logger = logging.getLogger(__name__)

# 飞书客户端
APP_ID = os.environ["FEISHU_APP_ID"]
APP_SECRET = os.environ["FEISHU_APP_SECRET"]

client = lark.Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()

SESSIONS_DIR = Path(__file__).parent / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

def get_session_path(user_id: str) -> Path:
    return SESSIONS_DIR / f"{user_id}.json"

def load_session(user_id: str) -> list[dict]:
    """加载用户对话历史"""
    path = get_session_path(user_id)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("messages", [])
    return []

def save_session(user_id: str, messages: list[dict]):
    """保存对话历史"""
    path = get_session_path(user_id)
    data = {
        "user_id": user_id,
        "messages": messages,
        "updated_at": datetime.now().isoformat(),
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def handle_user_message(user_id: str, user_text: str) -> str:
    """处理用户消息，返回 LLM 回复

    Args:
        user_id: 飞书 open_id
        user_text: 用户发送的文本

    Returns:
        LLM 回复内容
    """
    messages = load_session(user_id)

    # 如果没有历史，加入 system prompt
    if not messages:
        system_prompt = build_system_prompt()
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_text})

    reply = chat(messages)
    messages.append({"role": "assistant", "content": reply})
    save_session(user_id, messages)

    return reply

def send_feishu_message(user_id: str, content: str):
    """发送消息到飞书

    Args:
        user_id: 飞书 open_id
        content: 消息内容
    """
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
    """处理飞书事件回调

    这是 Flask webhook 会调用的函数。
    """
    header = data.header
    event = data.event

    if not event or not event.message:
        return

    message = event.message
    # 只处理文本消息
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
    messages = load_session(user_id)

    if not messages:
        system_prompt = build_daily_prompt()
        messages.append({"role": "system", "content": system_prompt})
    else:
        # 有历史对话，注入今日任务到 system prompt
        system_prompt = build_daily_prompt()
        # 替换或添加 system message
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = system_prompt
        else:
            messages.insert(0, {"role": "system", "content": system_prompt})

    # 生成今日第一个问题
    messages.append({"role": "user", "content": "开始今天的学习"})
    reply = chat(messages)
    messages.append({"role": "assistant", "content": reply})
    save_session(user_id, messages)

    send_feishu_message(user_id, reply)
    logger.info(f"Daily push to {user_id}: {reply[:50]}...")
