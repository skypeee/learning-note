# 飞书苏格拉底学习机器人设计文档

> 日期：2026-04-18
> 状态：待实现

## 目标
在飞书上搭建一个苏格拉底式学习机器人，被动回应用户提问 + 主动推送每日学习任务。背景信息从 `SKILL.md` 和 `milestones.md` 动态读取，随用户进度自动更新。

## 架构

```
socratic-bot/
├── main.py              # 入口：Flask app + APScheduler 初始化
├── bot.py               # 飞书消息收发（接收事件、发消息、加解密）
├── llm.py               # 百炼 API 调用（OpenAI 兼容接口）
├── prompts.py           # 苏格拉底 prompt + 每日任务 prompt
├── schedule.py          # 定时推送（早8点飞控，晚9点项目任务）
├── sessions/            # 每用户对话历史（user_id.json）
├── .env                 # 密钥（百炼 API key、飞书凭证）
└── requirements.txt
```

## 模块职责

### bot.py — 飞书消息收发
- 接收飞书事件回调（POST `/webhook`）
- 验证签名、解密消息
- 发送回复到飞书
- 提供 `send_message(user_id, content)` 接口供 schedule 调用

### llm.py — 百炼 API 调用
- 封装 OpenAI 兼容接口（base_url、model、api_key）
- 提供 `chat(messages)` 接口，传入完整对话历史
- 重试 1 次，失败返回错误提示

### prompts.py — Prompt 管理
- 读取 `prompts.md` 作为基础 prompt 模板
- 动态读取 `SKILL.md`、`milestones.md`、`weekly-plan.md`
- 从 `weekly-plan.md` 解析当天任务
- 组合成完整的 system prompt

### schedule.py — 定时推送
- APScheduler 定时触发（早 8:00 飞控储备、晚 21:00 项目任务）
- 读当天任务 → 生成 prompt → 调 llm.py → 通过 bot.py 推送

### sessions/ — 对话历史
- 每用户一个 JSON 文件
- 记录消息历史、当前任务索引、最后更新时间

## 数据流

```
用户发消息 → 飞书事件回调 → Flask /webhook
    ↓
bot.py 验证签名 + 解密消息
    ↓
读取 sessions/<user_id>.json
    ↓
prompts.py 组合 prompt（含最新进度）
    ↓
llm.py 调百炼 API
    ↓
回复飞书 → 更新 session 文件
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 飞书事件验证失败 | 返回 200，记录日志 |
| 百炼 API 超时 | 重试 1 次，失败回"思考中，稍后再试" |
| session 文件不存在 | 自动创建 |
| weekly-plan 当天无任务 | 跳过主动推送 |

## 配置项（.env）

```
FEISHU_APP_ID=cli_a94779fd76381cba
FEISHU_APP_SECRET=
DASHSCOPE_API_KEY=
DASHSCOPE_BASE_URL=
DASHSCOPE_MODEL=codingplan
```

## 部署方式
本地运行，`python main.py` 启动。飞书 webhook 需要公网地址（ngrok 或云服务器）。
