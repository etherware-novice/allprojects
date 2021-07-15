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
client.gif = im = Image.open("image0.gif")
client.giflen = 0
try:
    while True:
        im.seek(im.tell()+1)
        client.giflen += 1
except EOFError:
    pass

defaultime = 30
client.timerindex = {
    1: [60, "Caps-lock"],
    3: [defaultime, "Tricky Impersonating"],
    4: [defaultime, "3AM CHALLENGE"],
    8: [defaultime, "Light Mode"],
    18: [10, "Do not speak"],
    19: [15, "Heckclown Music"],
    24: [60, "Volume 100%"],
    26: [defaultime, "Opposite Talk"],
    28: [180, "Weeb Speak"],
    29: [120, "Beep Boop Speak"],
    30: [10, "1 Handed"],
    32: [60, "Swap Pfps"], #custom timer
    33: [30, "Swearing"],
    34: [defaultime, "Keyboard Swap"],
    35: [defaultime, "Double Letters"],
    37: [5, "1-Eyed"],
    38: [15, "No Top Row Letters"],
    40: [10, "Tricky Death"],
    42: [60, "No Discord"],
    43: [60, "Phone Camera Screenshots"]
}

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
global trip
ovr = trip = 0

async def timer(loop, channel, target, multiplier = 1, tst = False):
    #time.sleep(minutes * 60)
    try:
        index = client.timerindex[client.gif.tell()]
        mins = index[0]
        print(f"Timer for {mins} mins")
        if tst: asyncio.sleep(5)
        else: asyncio.sleep(mins * 60 * multiplier)
        print("Timer up")
        if tst: await channel.send("Timer done")
        await channel.send(f"{target.mention}, your curse [{index[1]}] has been lifted!")
    except: pass

def imageget():
    global trip
    buffer = io.BytesIO()
    rng = random.randint(0, client.giflen)
    if rng == 46: trip = 1 #special case for the triple effect
    if rng == 48: imageget()
    print(f"frame {rng}")
    client.gif.seek(rng)
    client.gif.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer   

@client.event
async def on_message(message):
    if message.content == "!ovr": await getrngif(message, True)
    elif (random.randint(0, 19) == 0): await getrngif(message) 
    if message.content == "!timer": asyncio.create_task(timer(0, message.channel, message.author, 1, True))
    if message.content == "!reload" and message.author.id == 661044029110091776:
        os.system(('git pull'))
        subprocess.call('python3 main.py')
    

async def getrngif(message, reroll = False):
    loop = asyncio.get_running_loop()
    global ovr
    #print(type(message.author.status))
    if message.author.bot: return
    if message.webhook_id != None:
        ovr = 1
        return
        #get_image()
        

    if random.randint(0, 1):
        target = random.choice([
            x for x in message.guild.members if x.raw_status in ("online", "dnd") and not x.bot
        ] + [
            [x.author async for x in message.channel.history(limit=30) if x is not x.author.bot]
        ]
        )
    else: target = message.author
    if reroll: target = message.author

    buffer = await loop.run_in_executor(None, imageget)
    asyncio.create_task(timer(loop, message.channel, target, 3 if trip else 0))
    if ovr: ovr = 0
    multi = "TRIPLED " if trip else ""
    cause = f" brought upon you by {message.author.mention}" if message.author != target else ""
    await message.channel.send(f"{target.mention}, face the wheel of {multi}DOOOOM{cause}!", file=discord.File(buffer, filename="some_image.png"))
    multi = 0




    


client.run(TOKEN)
