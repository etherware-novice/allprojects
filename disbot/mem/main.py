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

print(discord.__version__)
intents = discord.Intents.default() #sets up the intents obj
intents.members = True #flips the member inperwhatever it is to true
TOKEN = None

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

with open('token.yaml') as file:
    documents = yaml.full_load(file)
    for key, value in documents.items():
        if key == 'token': TOKEN = value
    if TOKEN == None: raise ValueError(f'Token not found, please check the file {file}')

try:
    with open('blk.yaml') as file:
        bot.blklist = yaml.full_load(file)
except:
    bot.blklist = []

bot.blklist = [y for x in bot.blklist if (y := bot.get_channel(x)) != None]

bot = commands.Bot(command_prefix=prfx, intents=intents) #initilizes the bot]
bot.token = TOKEN

    #flavorie text to make sure its working good
@bot.listen("on_ready")
async def init(): #initilization

    #guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

disp_guild = ''
for x in bot.guilds:
    disp_guild += f'{x.name} ({x.member_count} members)\n'
    #await x.me.edit(nick = 'the amogus bot')

print(
	f'{bot.user} is connected to the following guilds:\n'
	f'{disp_guild}'
)

@bot.listen("on_message")
async def blocker(message):
    del = 0
    if message.channel in bot.blklist:
       if len(message.attachments) >= 1: 
            for x in message.attachments:
                if x.filename.split(".")[-1] in ("png", "jpg", "jpeg"): del = 1

       #insert part testing for link to png

       if del:
           message.delete()
           message.channel.send("No memes")

bot.run(TOKEN)
