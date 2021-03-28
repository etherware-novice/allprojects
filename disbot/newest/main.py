import upd
import os

import discord
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
    	f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await inloop()

async def inloop():

	upd.commands(client)


client.run(TOKEN)