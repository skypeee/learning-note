# 学习 Agent v2 — Iteration 1 设计文档

> 日期：2026-04-20
> 状态：待实现
> 范围：Prompt 动态构建 + 上下文窗口管理
> 不涉及：Flask/飞书部署、多模型切换（用户已否决）

## 目标

优化当前学习 agent 的对话体验：
1. prompt 不再加载冗余文件，精准注入用户当前状态（阶段/复习/任务）
2. 长对话自动管理上下文窗口，防止 token 耗尽
3. 用户说"完成了"时，自动标记 weekly-plan.md 中对应任务为 ✅

## 当前架构

```
socratic-bot/
├── main.py              # Flask app + APScheduler
├── bot.py               # 飞书消息收发 + session 管理
├── llm.py               # 单模型 LLM 调用
├── prompts.py           # system prompt 构建 + 任务/复习查询
├── schedule.py          # 定时推送
├── sessions/            # JSON 对话历史
└── prompts.md           # 苏格拉底模板（待重构）
```

## 设计

### 1. Prompt 动态构建（重构 prompts.py）

**现状**：`build_system_prompt()` 加载 prompts.md + SKILL.md 全文 + milestones.md，token 浪费。

**新逻辑**：

```python
def build_context_aware_prompt() -> str:
    """
    system prompt = 苏格拉底规则 + 用户精简背景 + 今日状态
    """
    parts = []
    
    # 1. 苏格拉底核心规则（来自 prompts.md，精简到 5 条）
    parts.append(SOCRATIC_RULES)  # 常量，不读文件
    
    # 2. 用户精简背景（从 SKILL.md 提取关键句）
    parts.append(build_user_context())
    
    # 3. 今日到期复习（从 review-tracker.md 读取）
    reviews = get_due_reviews()
    if reviews:
        parts.append(f"## 今日到期复习\n" + format_reviews(reviews))
    
    # 4. 当前任务（从 weekly-plan.md 读取各方向第一个 ⬜ 任务）
    tasks = get_today_tasks()
    parts.append(f"## 当前可领取任务\n{tasks}")
    
    return "\n\n".join(parts)

def build_user_context() -> str:
    """从 SKILL.md 提取关键信息，而非加载全文"""
    # 只提取：
    # - 当前阶段（SITL 后期 → HIL 前期）
    # - 优势（7 年系统经验，不是编程新手）
    # - 短板（C++/MCU 不足，React 零基础）
    # - 对 AI 的要求（不要当新手，用系统经验类比）
    return "...精简后的 4-5 行..."
```

**token 节省**：从 ~4000 tokens（全文）→ ~300 tokens（精简）

### 2. 上下文窗口管理（重构 bot.py session 逻辑）

**现状**：session JSON 无限增长，不控制 token 数。

**新逻辑**：

```python
class SessionManager:
    """管理单用户会话上下文"""
    
    MAX_TOKENS = 4000      # 历史上下文 token 上限
    MAX_MESSAGES = 20      # 最多保留 20 轮对话
    
    def get_messages(self, user_id: str) -> list[dict]:
        """获取当前对话历史"""
        messages = load_session(user_id)
        
        # 如果没有历史，返回 system prompt
        if not messages:
            return [{"role": "system", "content": build_context_aware_prompt()}]
        
        # 从后往前截取，确保 token 数不超限
        result = messages[-self.MAX_MESSAGES:]
        while self.estimate_tokens(result) > self.MAX_TOKENS and len(result) > 2:
            result.pop(0)  # 删除最旧的消息
        
        return result
    
    def mark_task_completed(self, user_id: str, task_name: str) -> None:
        """标记任务完成"""
        messages = load_session(user_id)
        messages.append({
            "role": "system", 
            "content": f"[任务完成标记] {task_name} ✅"
        })
        save_session(user_id, messages)
    
    @staticmethod
    def estimate_tokens(messages: list[dict]) -> int:
        """粗略估算 token 数（中文字符数 × 1.5 + 英文单词数 × 1.3）"""
        total = 0
        for msg in messages:
            content = msg.get("content", "")
            total += len(content.encode("utf-8"))  # 粗略估算
        return total // 3  # 3 bytes ≈ 1 token
```

### 3. 任务完成自动标记

**触发**：用户回复"完成了"、"✅"、"做完了"

**逻辑**：
1. 从最近 3 轮对话中提取当前正在讨论的任务名（agent 推送时已知）
2. 或如果无法推断，回复用户确认"你完成的是哪个任务？"
3. 确认后，在 weekly-plan.md 中将该任务状态从 ⬜ 改为 ✅
4. 如果该任务是新学的知识点，自动在 review-tracker.md 中添加复习条目（首次学习日期 = 今天）
5. 回复用户确认并推送下一步建议

**文件变更**：
- `bot.py`：识别完成关键词 → 调用 `SessionManager.mark_task_completed()`
- `weekly-plan.md`：更新任务状态
- `review-tracker.md`：添加新知识点到复习追踪

## 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `prompts.py` | 重构 | 新增 `build_context_aware_prompt()`，精简 `build_user_context()` |
| `bot.py` | 重构 | 引入 `SessionManager`，添加任务完成识别 |
| `llm.py` | 不变 | 保持现有单模型调用逻辑 |
| `schedule.py` | 不变 | 定时推送逻辑不变 |
| `prompts.md` | 删除 | 规则内嵌到 `prompts.py` 常量 |
| `review-tracker.md` | 使用 | 读取到期复习，写入新知识点 |
| `weekly-plan.md` | 使用 | 读取当前任务，更新完成状态 |

## 实施顺序

1. 重构 `prompts.py` — 动态 prompt 构建
2. 重构 `bot.py` — SessionManager + 上下文管理
3. 添加任务完成自动标记
4. 删除 `prompts.md`（内容已内嵌）

## 验收标准

- [ ] system prompt 不再加载 SKILL.md/milestones 全文
- [ ] 长对话（20+ 轮）不会 token 耗尽
- [ ] 说"完成了"能自动标记 weekly-plan 中对应任务 ✅
- [ ] 新学知识点自动加入 review-tracker，下次推送时能看到复习提醒
