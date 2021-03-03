import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print("ready")
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
      await message.channel.send(message.content[::-1])
    
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)