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

bot = commands.Bot(command_prefix='!', intents=intents) #initilizes the bot


#flavorie text to make sure its working good
@bot.event
async def on_ready(): #initilization

    guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    print(discord.utils.get(bot.guilds))

    print(
    	f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_message(message):
    def check(m):
        return m.author != bot.me and (m.channel == bot.get_channel(813468817308778508) or m.channel == bot.get_channel(831173741958266910))

    try:
        msg = await client.for("message", check = check, timeout=1)
        msg.add_reaction(u"\U0001F44D")

    except:
        x = x


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel == bot.get_channel(813468817308778508) or reaction.message.channel == bot.get_channel(831173741958266910):
        print('you did it')

@bot.command(name='test')
async def test(ctx):
    await ctx.send('post another channel')

    def check(m):
        return m.author == ctx.author and '#' in m.content and m.channel == ctx.channel

    msg = await bot.wait_for('message', check=check)
    print(msg)




bot.run(TOKEN)
