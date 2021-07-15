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

bot = commands.Bot(command_prefix="!", intents=intents) #initilizes the bot]
bot.token = TOKEN




#bot.blklist = {825807971917365272: bot.get_channel(825807971917365272)}


    #flavorie text to make sure its working good
@bot.listen("on_ready")
async def init(): #initilization

    #guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    try:
        with open('blk.yaml') as file:
            file = yaml.full_load(file)
            bot.blklist = [y for x in file['list'] if (y := bot.get_channel(x)) != None]

    except:
        bot.blklist = []

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
    if message.author == bot.user or message.content.startswith("!"):
        return




    filename = ("png", "jpg", "jpeg", "webp")
    delchar = 0
    if message.channel in bot.blklist:
       if len(message.attachments) >= 1: 
            for x in message.attachments:
                if x.filename.split(".")[-1] in filename: delchar = 1

       #insert part testing for link to png
       if len(message.embeds) >= 1:
           for x in message.embeds:
               if x.image.url != None: delchar = 1

       if delchar:
           await message.delete()
           await message.channel.send("rule 6 No memes")

@bot.command()
async def add_r9(ctx):
    if await perms_adrm(ctx.channel, ctx.author):
        if ctx.channel in bot.blklist: await ctx.send("This channel is already registered!")
        else:
            bot.blklist.append(ctx.channel)
            upd_file()

            await ctx.send("Added successfully")
    else: await ctx.send("you dont have perms")

@bot.command()
async def rem_r9(ctx):
    if await perms_adrm(ctx.channel, ctx.author):
        if ctx.channel in bot.blklist:
            bot.blklist.remove(ctx.channel)

            upd_file()
        else: await ctx.send("This channel isnt registered yet!")
    else: await ctx.send("You dont have perms")

@bot.command()
async def list_r9(ctx):
    y = "List of channels:\n"
    [y := y + f"{x.mention}\n" for x in bot.blklist]
    await ctx.send(y)
    upd_file()

def upd_file():
    with open('blk.yaml', 'w') as file:
        tmp = {"list": [x.id for x in bot.blklist]}
        yaml.dump(tmp, file)


async def perms_adrm(channel, member):
    return channel.permissions_for(member).manage_channels

bot.run(TOKEN)
