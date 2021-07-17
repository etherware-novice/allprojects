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
client.gif = im = Image.open("pico.gif")
client.giflen = client.gif.n_frames - 1

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

async def timer(loop, channel, target, multiplier = 1, tst = False):
    #time.sleep(minutes * 60)

    default = 30
    index = {
        6: [default, "Broken legs"],
        10: [10, "Beep Boop Talk"],
        15: [15, "Tupper dissapearing"],
        22: [22, "Chat filter"],
        27: [10, "Broken toe"],
        32: [5, "Rain"],
        41: [60, "SUS"]
    }

    try:
        index = index[client.gif.tell()]
        channel.send(client.gif.tell())
        mins = index[0]
        print(f"Timer for {mins} mins")
        await asyncio.sleep(mins * 60 * multiplier)
        print("Timer up")
        if tst: await channel.send("Timer done")
        else: await channel.send(f"{target.mention}, your curse [{index[1]}] has been lifted!")
    except: pass

global ovr
global trip
ovr = trip = 0

def imageget(gif):
    global trip
    buffer = io.BytesIO()
    rng = random.randint(0, gif.n_frames - 1)
    print(f"frame {rng}")
    gif.seek(rng)
    gif.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer   
    
async def special_char(argument, message):
    switcher = {
        17: random.choice([x for x in message.channel.category.text_channels if x != message.channel]).mention,
        41: random.choice([x for x in message.guild.channels if x != message.channel]).mention
    }
    return switcher.get(argument, "")


async def getrngif(message, reroll = False):
    loop = asyncio.get_running_loop()
    global ovr
    #print(type(message.author.status))
    #if message.author.bot: return
        #get_image()
        

    if random.randint(0, 1):
        target = random.choice(
            [x.author async for x in message.channel.history(limit=30)]
        )
    else: target = message.author
    if reroll: target = message.author

    buffer = await loop.run_in_executor(None, imageget, client.gif)
    asyncio.create_task(timer(loop, message.channel, target, 3 if trip else 1))
    if ovr: ovr = 0
    multi = "but tripled " if trip else ""
    cause = f" from user {message.author.mention}" if message.author != target else ""
    spec = await special_char(client.gif.tell(), message)
    spec = str(spec) + "\n"
    targetdisp = target.display_name if target.bot and target != client.user else target.mention
    tmp = await message.channel.send(f"{spec}{target.display_name}, you have been hit by pico's bad luck{multi}{cause}...", file=discord.File(buffer, filename="some_image.png"))
    if target == client.user:
        await message.channel.send("Wait, thats me..", delete_after=6)
        await asyncio.sleep(1)
        await message.channel.send("Ok that one doesnt count-", delete_after=5)
        await asyncio.sleep(5)
        await tmp.delete()
    multi = 0



@client.event
async def on_message(message):
    if message.content == "!ovr": await getrngif(message, True)
    elif (random.randint(0, 19) == 0): await getrngif(message) 
    if message.content == "!reload" and message.author.id == 661044029110091776:
        os.system(('git pull'))
        subprocess.call(['python3', 'main-pic.py'])

    


client.run(TOKEN)
