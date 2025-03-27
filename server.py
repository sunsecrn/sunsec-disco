import discord
from discord.ext import tasks
import aiohttp
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

announced_events = set()

async def fetch_events(limit=5):
    url = f"https://ctftime.org/api/v1/events/?limit={limit}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            return []

def format_event(event):
    start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S%z")
    end = datetime.strptime(event["finish"], "%Y-%m-%dT%H:%M:%S%z")
    return (
        f"📣 **Novo CTF chegando!**\n"
        f"🏷️ **{event['title']}**\n"
        f"🌐 {event['url']}\n"
        f"🕒 {start.strftime('%d/%m %H:%M')} → {end.strftime('%d/%m %H:%M')} (UTC)\n"
        f"<@&{ROLE_ID}> preparem-se!"
    )

@client.event
async def on_ready():
    print(f"✅ Bot online como {client.user}")
    await tree.sync()
    print("📡 Slash commands sincronizados.")

    print(f"🎯 Procurando canal com ID: {CHANNEL_ID}")
    found_channel = None

    for guild in client.guilds:
        print(f"🔎 Servidor: {guild.name} (ID: {guild.id})")
        for ch in guild.text_channels:
            print(f"  → {ch.name} (ID: {ch.id})")
            if ch.id == CHANNEL_ID:
                found_channel = ch
                print(f"✅ Canal encontrado: {ch.name} (ID: {ch.id})")
                break

    if found_channel:
        try:
            await found_channel.send("👋 Estou online e consigo acessar este canal!")
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem no canal: {e}")
    else:
        print("⚠️ Canal não encontrado ou bot sem permissão.")

    if not check_for_new_events.is_running():
        check_for_new_events.start()

@tree.command(name="prox_ctf", description="Mostra os próximos eventos do CTFTime")
async def prox_ctf_command(interaction: discord.Interaction):
    events = await fetch_events(limit=3)
    now = datetime.now(tz=pytz.utc)
    msg = ""

    for event in events:
        start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S%z")
        if start > now:
            msg += (
                f"🏁 **{event['title']}** - {event['url']}\n"
                f"📅 Início: {start.strftime('%d/%m %H:%M')} UTC\n\n"
            )

    if msg == "":
        msg = "Nenhum CTF encontrado nos próximos dias."

    await interaction.response.send_message(msg)

@tasks.loop(minutes=60)
async def check_for_new_events():
    channel = client.get_channel(CHANNEL_ID)
    now = datetime.now(tz=pytz.utc)
    soon = now + timedelta(hours=24)

    events = await fetch_events(limit=10)

    for event in events:
        start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S%z")
        if now < start < soon and event["id"] not in announced_events:
            message = format_event(event)
            await channel.send(message)
            announced_events.add(event["id"])

client.run(TOKEN)
