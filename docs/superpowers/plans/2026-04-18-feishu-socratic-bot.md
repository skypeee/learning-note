# 飞书苏格拉底学习机器人 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在飞书上搭建苏格拉底式学习机器人，被动回应用户提问 + 主动推送每日学习任务，背景信息从 SKILL.md/milestones.md/weekly-plan.md 动态读取。

**Architecture:** Flask 接收飞书 webhook 事件 → 读取用户 session → 组合 prompt（含动态进度）→ 调百炼 API → 回复飞书。APScheduler 定时触发主动推送。

**Tech Stack:** Python 3.12, Flask, lark-oapi (飞书 SDK), openai (百炼兼容接口), APScheduler, python-dotenv, requests

---

## File Structure

| 文件 | 职责 | 创建/修改 |
|------|------|-----------|
| `demos/socratic-bot/.env.example` | 环境变量模板 | 创建 |
| `demos/socratic-bot/requirements.txt` | Python 依赖 | 创建 |
| `demos/socratic-bot/llm.py` | 百炼 API 调用封装 | 创建 |
| `demos/socratic-bot/prompts.py` | Prompt 管理（读 markdown 文件组合） | 创建 |
| `demos/socratic-bot/bot.py` | 飞书消息收发 | 创建 |
| `demos/socratic-bot/schedule.py` | APScheduler 定时推送 | 创建 |
| `demos/socratic-bot/main.py` | 入口（Flask + Scheduler） | 创建 |
| `demos/socratic-bot/sessions/` | 用户会话目录 | 创建目录 |
| `demos/socratic-bot/.env` | 实际密钥（不提交 git） | 创建 |

**依赖的外部文件（只读）：**
- `SKILL.md` — 用户背景
- `assessment/milestones.md` — 里程碑
- `assessment/weekly-plan.md` — 每周计划
- `prompts.md` — prompt 模板（已存在）

---

### Task 1: 项目骨架 — 依赖、环境、目录

**Files:**
- Create: `demos/socratic-bot/requirements.txt`
- Create: `demos/socratic-bot/.env.example`
- Create: `demos/socratic-bot/sessions/` (directory)

- [ ] **Step 1: 创建 requirements.txt**

```
flask>=3.0
lark-oapi>=1.4
openai>=1.30
apscheduler>=3.10
python-dotenv>=1.0
```

- [ ] **Step 2: 创建 .env.example**

```
# 飞书开放平台
FEISHU_APP_ID=cli_a94779fd76381cba
FEISHU_APP_SECRET=你的AppSecret
FEISHU_VERIFICATION_TOKEN=你的VerificationToken

# 百炼 API (DashScope OpenAI 兼容接口)
DASHSCOPE_API_KEY=你的APIKey
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_MODEL=codingplan

# 服务配置
FLASK_PORT=8000
SCHEDULE_MORNING_HOUR=8
SCHEDULE_EVENING_HOUR=21

# 学习仓库根目录（SKILL.md 等文件的位置）
LEARNING_NOTE_ROOT=/Users/duanduanzi/workspace/my-project/learning-note
```

- [ ] **Step 3: 创建 sessions 目录**

```bash
mkdir -p demos/socratic-bot/sessions
```

- [ ] **Step 4: 安装依赖**

```bash
cd demos/socratic-bot
pip3 install -r requirements.txt
```

---

### Task 2: LLM 模块 — 百炼 API 调用

**Files:**
- Create: `demos/socratic-bot/llm.py`

- [ ] **Step 1: 创建 llm.py**

```python
import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

def get_client() -> OpenAI:
    """创建百炼 OpenAI 兼容客户端"""
    return OpenAI(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url=os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    )

def chat(messages: list[dict], model: str | None = None) -> str:
    """调用 LLM，返回 assistant 回复内容

    Args:
        messages: 完整对话历史，格式 [{"role": "system|user|assistant", "content": "..."}]
        model: 模型名，默认取环境变量 DASHSCOPE_MODEL

    Returns:
        LLM 的回复文本
    """
    model = model or os.environ.get("DASHSCOPE_MODEL", "codingplan")
    client = get_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return "我正在思考这个问题，请稍等，我会继续我们的讨论。"
```

- [ ] **Step 2: 快速测试**

创建临时测试文件验证 API 连通性：

```bash
cd demos/socratic-bot
python3 -c "
from llm import chat
result = chat([{'role': 'user', 'content': '你好'}])
print(result)
"
```

Expected: 输出 LLM 回复"你好"或类似内容。

---

### Task 3: Prompt 管理模块

**Files:**
- Create: `demos/socratic-bot/prompts.py`

- [ ] **Step 1: 创建 prompts.py**

```python
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
    """生成今日任务的 system prompt"""
    base = build_system_prompt()
    today_tasks = get_today_tasks()
    today_str = date.today().strftime("%Y-%m-%d")

    task_section = f"\n\n## 今天的任务（{today_str}）\n"
    if today_tasks:
        task_section += today_tasks
    else:
        task_section += "今天没有特定任务，自由引导用户讨论技术话题。"

    return base + task_section

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
```

- [ ] **Step 2: 测试 prompt 生成**

```bash
cd demos/socratic-bot
python3 -c "
from prompts import build_daily_prompt
print(build_daily_prompt()[:500])
"
```

Expected: 输出包含 prompts.md 模板 + SKILL.md 内容 + 今天任务的文本。

---

### Task 4: 飞书 Bot 模块

**Files:**
- Create: `demos/socratic-bot/bot.py`

依赖: Task 2 (llm.py), Task 3 (prompts.py)

- [ ] **Step 1: 创建 bot.py**

```python
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

    # 忽略机器人自己的消息
    if message.chat_type == "p2p" and message.sender and message.sender.sender_id:
        # 检查是否是 bot 自己的 app_id（通过 header 判断）
        pass

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
```

- [ ] **Step 2: 测试飞书 SDK 导入**

```bash
cd demos/socratic-bot
python3 -c "
import lark_oapi
from lark_oapi.api.im.v1 import CreateMessageRequest
print('lark-oapi OK')
"
```

Expected: `lark-oapi OK`

---

### Task 5: Flask Webhook 入口

**Files:**
- Create: `demos/socratic-bot/main.py`

依赖: Task 4 (bot.py)

- [ ] **Step 1: 创建 main.py**

```python
import os
import json
import logging

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

from bot import handle_event, send_feishu_message, send_daily_prompt
from schedule import init_scheduler

app = Flask(__name__)

# 飞书事件回调
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    # 处理 challenge 验证（首次配置 webhook 时飞书会发）
    if body and "challenge" in body:
        return jsonify({"challenge": body["challenge"]})

    # 解析事件
    try:
        sdk_event = lark.UnmarshalEvent(body, event_cls=P2ImMessageReceiveV1)
        if sdk_event.event and sdk_event.event.message:
            handle_event(sdk_event.event)
    except Exception as e:
        logging.error(f"Event parse error: {e}")

    return jsonify({"code": 0})

# 健康检查
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 8000))
    scheduler = init_scheduler(app)
    logging.info(f"Starting socratic-bot on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
```

- [ ] **Step 2: 启动测试（不接飞书）**

```bash
cd demos/socratic-bot
# 先不启动 scheduler，只测试 Flask
python3 -c "
from main import app
print('Flask app created')
"
```

Expected: `Flask app created`

---

### Task 6: 定时推送模块

**Files:**
- Create: `demos/socratic-bot/schedule.py`

依赖: Task 4 (bot.py)

- [ ] **Step 1: 创建 schedule.py**

```python
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from bot import send_daily_prompt

logger = logging.getLogger(__name__)

# 需要推送的用户列表（目前只有自己）
# 后续从配置文件读取
TARGET_USERS = os.environ.get(
    "TARGET_USERS",
    "替换为你的飞书open_id",  # 首次对话后从 session 文件或飞书后台获取
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
    logger.info(f"Scheduler started: morning={morning_hour}:00, evening={evening_hour}:00")
    return scheduler

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
```

- [ ] **Step 2: 测试 scheduler 初始化**

```bash
cd demos/socratic-bot
python3 -c "
from flask import Flask
from schedule import init_scheduler
app = Flask(__name__)
s = init_scheduler(app)
print('Scheduler initialized')
s.shutdown()
"
```

Expected: `Scheduler initialized` 后自动退出。

---

### Task 7: 完整启动测试

**Files:**
- 创建 `.env`（从 `.env.example` 复制，填入真实密钥）
- 修改: `schedule.py` 中的 TARGET_USERS

- [ ] **Step 1: 复制 .env 并填写**

```bash
cd demos/socratic-bot
cp .env.example .env
# 编辑 .env，填入真实的 FEISHU_APP_SECRET、DASHSCOPE_API_KEY 等
```

- [ ] **Step 2: 获取飞书 open_id**

首次与机器人对话后，从 `sessions/` 目录下会自动生成 `<open_id>.json` 文件。或者从飞书管理后台获取。

拿到 open_id 后更新 `.env`:
```
TARGET_USERS=你的open_id
```

- [ ] **Step 3: 本地启动**

```bash
cd demos/socratic-bot
python3 main.py
```

Expected: 日志显示 `Starting socratic-bot on port 8000` 和 `Scheduler started`。

- [ ] **Step 4: 测试 webhook 端点**

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok"}`

- [ ] **Step 5: 配置飞书事件回调地址**

在飞书开放平台 → 你的应用 → 事件订阅 → 配置请求地址。
需要公网地址，可以用 ngrok:

```bash
ngrok http 8000
```

拿到 ngrok URL 后填入飞书后台，格式: `https://xxx.ngrok-free.app/webhook`

- [ ] **Step 6: 订阅事件**

在飞书开放平台 → 事件订阅，添加事件:
- `im.message.receive_v1` — 接收消息

- [ ] **Step 7: 在飞书中给机器人发消息测试**

Expected: 机器人回复苏格拉底式问题。

---

## 部署清单

| 步骤 | 命令/操作 |
|------|-----------|
| 1. 安装依赖 | `pip3 install -r requirements.txt` |
| 2. 配置 .env | 从 `.env.example` 复制并填写真实密钥 |
| 3. 启动服务 | `python3 main.py` |
| 4. 配置 ngrok（如需公网） | `ngrok http 8000` |
| 5. 飞书配置 webhook URL | `https://xxx.ngrok-free.app/webhook` |
| 6. 订阅事件 | `im.message.receive_v1` |
| 7. 发布应用 | 飞书开放平台 → 版本管理与发布 → 创建版本 |

## 已知限制（V1）

1. 单用户 — `TARGET_USERS` 写死，后续可改为自动发现
2. 无鉴权 — Flask webhook 未加签名验证（生产环境需要加）
3. 本地部署 — 需要 ngrok 或云服务器
4. prompt 文件读取路径写死 — 通过 `LEARNING_NOTE_ROOT` 环境变量可配
