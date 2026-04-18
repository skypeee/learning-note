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
