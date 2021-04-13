import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import traceback
from discord.ext import tasks
intents = discord.Intents.default() #sets up the intents obj
intents.members = True #flips the member inperwhatever it is to true

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

bot = commands.Bot(command_prefix='am!', intents=intents) #initilizes the bot


#flavorie text to make sure its working good
@bot.event
async def on_ready(): #initilization

    guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    print(discord.utils.get(bot.guilds))

    print(
    	f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.command(name='test')
async def test(ctx):
    await ctx.send('post another channel')

    def check(m):
        return m.content == ctx.message.content and m.author == ctx.author and '#' in m.content

    msg = await bot.wait_for('message', check=check)
    print(msg)


bot.run(TOKEN)
