import os
from flask import Flask, request
from flask_socketio import SocketIO
import requests

TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/", methods=["GET"])
def home():
    return "Bot läuft!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/horn"):
            parts = text.split()

            # Standard: sehr lange laufen
            duration = 9999  

            # Wenn Zahl angegeben wurde → Dauer setzen
            if len(parts) > 1 and parts[1].isdigit():
                duration = int(parts[1])

            socketio.emit("horn_signal", {"duration": duration})

            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": f"🔊 HORN für {duration} Sekunden"
            })

    return "ok"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
