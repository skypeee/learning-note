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
