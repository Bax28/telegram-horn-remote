import os
import asyncio
from flask import Flask, request
from threading import Thread
import requests
import websockets

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

connected_clients = set()

# -------- WebSocket Server --------
async def websocket_handler(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def start_websocket():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        await asyncio.Future()

def run_websocket():
    asyncio.run(start_websocket())

Thread(target=run_websocket).start()

# -------- Telegram Webhook --------
@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/horn":
            asyncio.run(send_to_clients("horn"))
            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🔊 HORN AUSGELÖST"
            })

    return "ok"

async def send_to_clients(message):
    for ws in connected_clients:
        await ws.send(message)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"
