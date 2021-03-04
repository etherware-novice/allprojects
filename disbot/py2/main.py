#bot.py
import os

import discord
from dotenv import load_dotenv

load.dotenv()
TOKEN = os.getenv('ODE2ODI5NzkzMjIzNTczNTY0.YEAqBg.kHVrz3qaknP8EDBOWN9KySMBDds')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{Client.user} has connected to discord!'')

client.run(TOKEN)
