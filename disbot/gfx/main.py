import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import traceback
import yaml
import io
from discord.ext import tasks
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from dhooks import Webhook as dhook
from aioconsole import ainput
import aioconsole

print(discord.__version__)
intents = discord.Intents.default() #sets up the intents obj
#intents.members = True #flips the member inperwhatever it is to true
TOKEN = None

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

with open('token.yaml') as file:
	documents = yaml.full_load(file)
	for key, value in documents.items():
		if key == 'token': TOKEN = value
	if TOKEN == None: raise ValueError(f'Token not found, please check the file {file}')


bot = commands.Bot(command_prefix='!', intents=intents) #initilizes the bot]
bot.token = TOKEN

global chn
global msg
chn = bot.get_channel(845745700867538997)
#flavorie text to make sure its working good
@bot.event
async def on_ready(): #initilization

    #guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    disp_guild = ''
    for x in bot.guilds:
        disp_guild += f'{x.name} ({x.member_count} members)\n'
        #await x.me.edit(nick = 'the amogus bot')
        await x.me.edit(nick='coded bot (probably)', reason="i added code, sfx -candycane")
        for y, z in x.me.guild_permissions:
            print(f"{y} - {z}")

    print(
    	f'{bot.user} is connected to the following guilds:\n'
        #f'{disp_guild}'
    )


    await bot.change_presence(activity=discord.Game(name='or candys bot lol')) #:)
    await some()


async def rel(ctx):
    channels = bot.get_all_channels()


@bot.command(name='tst')
async def tst(ctx, resp):
    await ctx.send(resp)

@bot.listen('on_message')
async def income(message):
    form = f'{str(message.author)}: {message.content}'
    if "staff" in str(message.channel): print(f'{message.channel} - {form}')

async def some():
    global chn
    global msg
    tmp = 0
    line = await aioconsole.ainput(f"#{chn}----------\n")
    if line[0] == "#":
        chanmatch = []

        for x in bot.get_all_channels(): #for every chanl
            if str(line[1:]) in str(x) and not isinstance(chanmatch, str): chanmatch.append(x)

        
        for x in chanmatch:
            if line[1:] == str(x): 
                chn = x
                tmp = 1
        if len(chanmatch) < 1 and not tmp: print("No channel found, try again..")
        elif len(chanmatch) == 1 and not tmp: chn = chanmatch[0]
        elif not tmp:
            for x in chanmatch:
                print(f"#{str(x)}")
            print("Multiple channels found, try again with one above..")

        #print(chn)
    elif line.startswith("e>"):
        await msg.edit(content = str(line[2:]))
    elif line == "del":
        await msg.delete()
    else:    
        temp = bot.get_channel(845745700867538997)
        #await temp.send(line)
        msg = await chn.send(line)
    await some()

bot.run(TOKEN)