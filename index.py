import discord
import threading
import chatwork
import time
import discord
import os
from flask import Flask, request , jsonify

app = Flask(__name__)
cw = chatwork.setup(114514,"aa")
API_TOKEN = os.getenv("chatwork_api_token")

SECRET_TOKEN = None

bot_account_id = 11156582 
@app.route("/",methods=["POST"])
def root():
    return "ok"
@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN): # type: ignore
        return "invalid signature", 403
    
    data = request.json
    room_id    = chatwork.webhook_get_roomid(data)
    account_id = chatwork.webhook_get_account_id(data)
    message    = chatwork.webhook_get_message(data)
    message_id = chatwork.webhook_get_message_id(data)

    cw = chatwork.setup(room_id,API_TOKEN)
    
    return jsonify({"status": "ok"}),200
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)