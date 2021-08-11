import os #import hell
import discord
import random
from discord import guild
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
import warnings
warnings.filterwarnings("error")

from array import *
import getpass
from discord_slash import SlashCommand 
from discord_slash.utils.manage_commands import create_option, create_choice
import requests, jsonify
import sys
from PIL import Image
import time
import subprocess
import traceback
from discord_slash import SlashCommand 
import itertools

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


bot = commands.Bot(intents=intents, command_prefix="w!") #initilizes the bot (its not a full bot bot bc i dont need the command stuff)
bot.token = TOKEN



def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

#flavorie text to make sure its working good
@bot.listen("on_ready")
async def init(): #initilization

    #flavor text
    now = datetime.now()
    curtime = now.strftime("%B %d, %Y at %H:%M")
    print(f"\nHello, user <{getpass.getuser()}>. Today's datetime is {curtime}.")
    print(f"\n{bot.user} is connected to the following guilds:")
    print(*[ #this little star means to decompress the list
        f"{x.name} ({x.member_count} members)" #format of each entry
        for x in bot.guilds #getting each entry in the loop
        ], sep = "\n") #making sure its on a newline

    #bot.exc = lambda n, e: f"ERROR ```{n[0].__name__}: [{e}] on line {n[2].tb_lineno}``` was thrown, talk to {bot.get_user(661044029110091776).mention}"
    bot.logchn = bot.get_channel(873631822318297098)
    bot.cwd = os.getcwd()

@commands.check_any(commands.check(lambda m: m.author.id == 661044029110091776))
@bot.command(name="bash")
async def call(ctx, *args):
    print(args)
    if args[0] == "cd": os.chdir(args[1])
    else: 
        output = subprocess.check_output(args, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

        if args[-1] == "!long": 
            chunks = [output[i:i+1950] for i in range(0, len(output), 1950)]
            for x in chunks:
                #print(body)
                print(x)
                await ctx.send(x)
        else: await ctx.send(textwrap.shorten(output, 50, placeholder="..."))

@commands.check_any(commands.check(lambda m: m.author.id == 661044029110091776))
@bot.command(name="^C")
async def exit(ctx):
    exit()

@call.error
async def pas(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    else: raise(error)



@bot.event
async def on_error(event, *args, **kwargs):
    *_, error = sys.exc_info()
    
    print(traceback.format_exc(limit=2))
    await bot.logchn.send(f"ERROR ```{traceback.format_exc(limit=2)}```{bot.get_user(661044029110091776).mention}")

@bot.event
async def on_command_error(ctx, exception):

    if ctx.author == bot.user: return
    atype, object, traceb = sys.exc_info()

    if isinstance(exception, discord.ext.commands.errors.CommandNotFound): return
    await ctx.send(f"ERROR ```{atype.__name__}: [{object}] on line {traceb.tb_lineno}``` was thrown, talk to {bot.get_user(661044029110091776).mention}")


bot.run(TOKEN)