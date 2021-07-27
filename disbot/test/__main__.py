import os #import hell
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import traceback
import re
import yaml
import io
import socket
from discord.ext import tasks
from datetime import datetime
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from dhooks import Webhook as dhook
from aioconsole import ainput
from colr import color
from array import *
import getpass
import sys
from PIL import Image
import time
import subprocess

from PIL import Image, ImageDraw, ImageFont
import io, math, textwrap



intents = discord.Intents.all() #sets up the intents obj
#intents.members = True #flips the member inperwhatever it is to true
#intents.presences = True
TOKEN = None

#sys.stderr = open("err.txt", 'w')

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

with open('token.yaml') as file:
    documents = yaml.full_load(file)
    try:
        TOKEN = documents['token']
    except KeyError:
        raise KeyError(f'Token not found, please check the file {file}') #where the bot token comes from


bot = commands.Bot(command_prefix="!", intents=intents) #initilizes the bot (its not a full bot bot bc i dont need the command stuff)
bot.token = TOKEN

global multi, ovr
ovr = 0
multi = 1

#flavorie text to make sure its working good
@bot.listen("on_ready")
async def start(): #initilization

    #flavor text
    now = datetime.now()
    curtime = now.strftime("%B %d, %Y at %H:%M")
    print(f"\nHello, user <{getpass.getuser()}>. Today's datetime is {curtime}."
        f"\n{bot.user} is connected to the following guilds:")
    print(*[ #this little star means to decompress the list
        f"{x.name} ({x.member_count} members)" #format of each entry
        for x in bot.guilds #getting each entry in the loop
        ], sep = "\n") #making sure its on a newline

@bot.listen("on_message")
async def disprole(message):
    rol = message.author.roles
    formatting = (lambda m: f"Role {color(m.name, fore=m.colour.value)}:"
    f"pos {m.position}, mentionab: {m.mentionable}, seperateed: {m.hoist}\nid - {m.id}\n")

    print(f"Member {color(message.author.display_name, fore=message.author.colour.value)}\'s roles")
    print(*[formatting(x) for x in rol])

bot.run(TOKEN)