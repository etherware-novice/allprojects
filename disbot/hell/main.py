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


intents = discord.Intents.all() #sets up the intents obj
#intents.members = True #flips the member inperwhatever it is to true
#intents.presences = True
TOKEN = None
cls = "\u001B[2J"


#sys.stderr = open("err.txt", 'w')

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

with open('token.yaml') as file:
    documents = yaml.full_load(file)
    try:
        TOKEN = documents['token']
    except KeyError:
        raise KeyError(f'Token not found, please check the file {file}') #where the bot token comes from


client = discord.Client(intents=intents) #initilizes the bot (its not a full bot bot bc i dont need the command stuff)
client.token = TOKEN
client.gif = im = Image.open("image0.gif")
client.giflen = 0
try:
    while True:
        im.seek(im.tell()+1)
        client.giflen += 1
except EOFError:
    pass


#flavorie text to make sure its working good
@client.event
async def on_ready(): #initilization

    #flavor text
    now = datetime.now()
    curtime = now.strftime("%B %d, %Y at %H:%M")
    print(f"\nHello, user <{getpass.getuser()}>. Today's datetime is {curtime}.")
    print(f"\n{client.user} is connected to the following guilds:")
    print(*[ #this little star means to decompress the list
        f"{x.name} ({x.member_count} members)" #format of each entry
        for x in client.guilds #getting each entry in the loop
        ], sep = "\n") #making sure its on a newline

global ovr
ovr = 0
@client.event
async def on_message(message):
    global ovr
    #print(type(message.author.status))
    if message.author.bot: return
    rng = random.randint(1, 19)
    print(rng)
    ovr = rnd = 0
    if message.content == "!ovr": ovr = 1
    if message.content == "!rnd": rnd = 1 #debug stuf
    if rng <= 1 or ovr or rnd:
        if message.webhook_id != None:
            ovr = 1
            return
        #get_image()
        buffer = await asyncio.get_running_loop().run_in_executor(None, imageget)

        if random.randint(0, 1) or rnd or not ovr:
            target = random.choice([
                x for x in message.guild.members if x.raw_status in ("online", "dnd") and not x.bot
            ])
        else: target = message.author

        if ovr: ovr = 0
        cause = f" brought upon you by {message.author.mention}" if message.author != target else ""
        await message.channel.send(f"{target.mention}, face the wheel of DOOOOM{cause}!", file=discord.File(buffer, filename="some_image.png"))

def imageget():
        buffer = io.BytesIO()
        rng = random.randint(0, client.giflen)
        print(rng)
        client.gif.seek(rng)
        client.gif.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer   


client.run(TOKEN)
