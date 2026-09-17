import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
FASTAPI_URL = "http://localhost:8000/api/channel-created"

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[Bot Logged In] {client.user} (ID: {client.user.id})")

@client.event
async def on_guild_channel_create(channel):
    data = {
        "channel_id": str(channel.id),
        "channel_name": channel.name,
        "guild_id": str(channel.guild.id)
    }
    try:
        response = requests.post(FASTAPI_URL, json=data)
        if response.status_code == 200:
            print(f"[Sync Success] 새 채널 생성 알림 전송됨: {channel.name}")
    except Exception as e:
        print(f"[Sync Error] 백엔드 전송 실패: {e}")

if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)