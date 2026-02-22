import os
from flask import Flask, request
import requests

TOKEN = os.environ.get("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/horn":
            requests.post(URL, json={
                "chat_id": chat_id,
                "text": "🔊 HORN AKTIVIERT"
            })

    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"
