
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


intents = discord.Intents.default() #sets up the intents obj
intents.members = True #flips the member inperwhatever it is to true
TOKEN = None
cls = "\u001B[2J"


#sys.stderr = open("err.txt", 'w')

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

with open('token.yaml') as file:
    documents = yaml.full_load(file)
    for key, value in documents.items():
        if key == 'token': TOKEN = value
    if TOKEN == None: raise ValueError(f'Token not found, please check the file {file}') #where the bot token comes from


client = discord.Client(intents=intents) #initilizes the bot (its not a full bot bot bc i dont need the command stuff)
client.token = TOKEN

#flavorie text to make sure its working good
@client.event
async def on_ready(): #initilization

    #guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    disp_guild = ''
    for x in client.guilds:
        if "RP" not in x.name: disp_guild += f'{x.name} ({x.member_count} members)\n'
        else: 
            disp_guild += f'[rpserver] ({x.member_count} members)\n'
            print(0)
            client.server = x #more flavor text yay
        #await x.me.edit(nick = 'the amogus bot')

    client.log = []
    print(f"Discord version {discord.__version__}")
    #flavor text
    now = datetime.now()
    curtime = now.strftime("%B %d, %Y at %H:%M")
    print(f"\n{client.user} is connected to the following guilds:\n{disp_guild}")
    
    client.connlist = [x for x in client.get_all_channels() if x.name == "connect-chnl"]

global lastmsg
lastmsg = None
@client.event
async def on_message(message):
    global lastmsg

    if message.author == client.user:
        return

    form = ""
    if message.channel in client.connlist:
        try:
            if lastmsg.guild != message.guild: form = f"**{message.guild}**\n{message.author.display_name}: "
            elif lastmsg.author != message.guild: form = f"{message.author.display_name}: "
        except:
            form = f"**{message.guild}**\n{message.author.display_name}: "

        form += message.content

        [await x.send(form) for x in client.connlist if message.channel != x]

        lastmsg = message

client.run(TOKEN)