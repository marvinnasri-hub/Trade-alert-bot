from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT  = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_API   = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send_telegram(msg: str):
    payload = {"chat_id": TELEGRAM_CHAT, "text": msg, "parse_mode": "Markdown"}
    r = requests.post(TELEGRAM_API, json=payload, timeout=10)
    return r.ok, r.text

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    symbol  = data.get("symbol") or data.get("ticker") or "N/A"
    price   = data.get("price") or ""
    volume  = data.get("volume") or ""
    message = data.get("message") or ""

    alert_msg = (
        f"🚨 *MARKET ALERT*\n"
        f"*Asset:* `{symbol}`\n"
        f"*Price:* {price}\n"
        f"*Volume:* {volume}\n"
        f"*Info:* {message}"
    )
    ok, resp = send_telegram(alert_msg)
    if ok:
        return jsonify({"status": "sent"}), 200
    else:
        return jsonify({"status": "error", "detail": resp}), 500

@app.route("/")
def home():
    return "Telegram alert bot is running ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
