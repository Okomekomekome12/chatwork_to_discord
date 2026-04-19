import discord
import threading
import chatwork
import time
import discord
import os
from flask import Flask, request , jsonify
#discord.py初期設定
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

app = Flask(__name__)
API_TOKEN = os.getenv("chatwork_api_token")
cw = chatwork.setup(114514,API_TOKEN)
SECRET_TOKEN = None

bot_account_id = 11156582
@client.event
async def get_messages(message):
    if message.author.bot:
        return
    if message.content:
       cw.messagesend(f"[info][title]{message.author.display_name}さんのコメント[/title]{message.content}[/info]")

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
    discord_token = str(os.getenv("discord_token"))
    client.run(discord_token)