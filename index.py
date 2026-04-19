import discord
import threading
import chatwork
import os
import asyncio
from flask import Flask, request, jsonify

# Discord初期設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

app = Flask(__name__)
API_TOKEN = os.getenv("chatwork_api_token")
SECRET_TOKEN = None #シークレットトークンなしで（

DISCORD_CHANNEL_ID = 191945450721  # 転送先チャンネルID
bot_account_id = 11156582
CHATWORK_ROOM_ID = os.getenv("chatwork_room_id")

cw = chatwork.setup(CHATWORK_ROOM_ID, API_TOKEN)


#discordのコメをchatworkに転送
@client.event
async def on_message(message):  
    if message.author.bot:
        return
        #ネ 土 会 ェ 貝 南 犬 ☆ カ ゞ ん I よ " る ノ D A !!
    if message.content:
        cw.messagesend(f"[info][title]{message.author.display_name}さんのコメント[/title]{message.content}[/info]")


#cwからdiscorへ
def send_to_discord(content: str):

    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        print(f"{DISCORD_CHANNEL_ID}なんかねぇよ（")
        return
    asyncio.run_coroutine_threadsafe(channel.send(content), client.loop) # type: ignore


@app.route("/", methods=["POST", "GET"])
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


    if account_id == bot_account_id:
        return jsonify({"status": "ok"}), 200
    account_name = cw.get_account_name()
    # Discordへ転送
    discord_message = f"[Chatwork]{account_name}さんのメッセージ:\n{message}"
    send_to_discord(discord_message)

    return jsonify({"status": "ok"}), 200


def run_flask():
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    #Flaskを別スレッドで起動
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    #botをメインスレッドで起動
    discord_token = os.getenv("discord_token")
    client.run(str(discord_token))