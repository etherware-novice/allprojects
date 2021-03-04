#bot.py
import os

import discord
#from dotenv import load_dotenv

#load.dotenv()
TOKEN = 'ODE2ODI5NzkzMjIzNTczNTY0.YEAqBg.kHVrz3qaknP8EDBOWN9KySMBDds'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')

client.run(TOKEN)
