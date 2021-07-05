#why do i spend so much time on this useless stuff lol

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

print(discord.__version__)
#flavor text
now = datetime.now()
curtime = now.strftime("%B %d, %Y\n%H:%M")
print(f"Hello, user. Today's datetime is {curtime}")
intents = discord.Intents.default() #sets up the intents obj
intents.members = True #flips the member inperwhatever it is to true
TOKEN = None
cls = "\u001B[2J"

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
        if ":)" not in x.name: disp_guild += f'{x.name} ({x.member_count} members)\n'
        else: 
            disp_guild += f'[rpserver] ({x.member_count} members)\n'
            print(0)
            client.server = x #more flavor text yay
        #await x.me.edit(nick = 'the amogus bot')

    
    notepad = client.get_channel(861348653113540628)
    client.channel = notepad
    client.nick = "notepad.exe"

    client.log = [[], []]
    print(
        f'{client.user} is connected to the following guilds:\n'
        f'{disp_guild}'
    )

    asyncio.ensure_future(start_server('127.0.0.1', 5000))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    

    #the chatroom prints
    usrc = message.author.colour
    date = datetime.now().strftime("%m/%d - %H:%M:%S")
    bel = "\a"
    ath = ""
    if len(message.attachments) >= 1:
        ath = "\n"
        for x in message.attachments:
            ath += f"[attachment] {x.filename} ({x.url})\n"

    try:
        x = message.author.roles
        dispn = color(message.author.display_name, fore=(usrc.r, usrc.g, usrc.b))
    except:
        if message.author.display_name == client.nick: 
            dispn = color(message.author.display_name, fore=(60, 31, 128))
            dispn += "(client)"
            bel = ""
        else: dispn = f"{message.author.display_name}(tup)"
    
    rng = random.randint(0, 50)
    print(f'{bel}{rng}[{date} in #{color (message.channel, fore=(34, 245, 87))}] {dispn}: {message.content}{ath}')
    if rng <= 3:
        await generate(message)


async def generate(dmes): #database of the clippy addon i will never remove lol
    message = "Hello!"
    nick = "clippy.exe"
    delay = 20
    good = 1
    effect = "null"
    file = "https://cdn.discordapp.com/attachments/859551131717730304/860589709306232842/unknown.png" #normal.png

    rng = random.randint(0, 700)

    if rng < 400: message = "clippy forgot what he was going to say"
    if rng < 230: 
        message = "I have a present!"
        nick = "clippyevil.exe"
        delay = 10
        good = 0
        effect = "1/3 hp"
        file = "https://cdn.discordapp.com/attachments/859551131717730304/860589986340274186/unknown.png" #dynamite.png
    if rng < 100:
        message = "Lets restart your ~~system~~ life~"
        delay = 15
        good = 0
        nick = "restartexe.exe"
        effect = "death"
    if rng < 50:
        message = "is not responding"
        nick = "clippy.exe is not responding"
        delay = 10
        file = "https://cdn.discordapp.com/attachments/859551131717730304/860590334492147722/unknown.png" #error.png
        good = 1
    if rng == 1: 
        message = "You are lucky! Here's a gift: "
        message += random.choice(["magic stick", "atk up", "def up", "speed up", "ability up", "oof extremely unlucky"])
    if rng == 420 | rng == 69:
        message = "69420 nice"
        nick = "blaze it"
        delay = 7
        good = 1
    if rng == 98:
        message = "progressDOS bonus!"
        nick = "cmd.exe"
        file = "https://cdn.discordapp.com/attachments/859551131717730304/860590870201630750/ico_dos.png"
    if rng == 11:
        message = "clippy has been replaced by the macOS version"
        nick = "macbox.exe"
        delay = 5
        good = 1
        file = "https://cdn.discordapp.com/attachments/859551131717730304/860591298448457728/unknown.png" #macos
    print(f"rng {rng}, which reffers to message: {message}")
    #print(f"message: {message}\nnick: {nick}\ndelay: {delay}\ngood: {good}\nfile: {file}\neffect: {effect}")
    await websend(dmes,file, message, nick, delay, good, effect)

async def websend(dmes, avatar, message, nick, delay, good = 0, effect = None):
    x = 0
    sendout = None
    for x in await dmes.channel.webhooks():
        if x.user == client.user: sendout = x
    if sendout == None: sendout = await dmes.channel.create_webhook(name="clippy", reason="semi tupper lol")
    msg = await sendout.send(message, wait=True, username=nick, avatar_url=avatar)
    await msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
    if good: await msg.delete(delay=delay)
    else:
        await asyncio.sleep(delay)
        try:
            await msg.edit(content=effect)
            await msg.delete(delay=5)
        except:
            x = x

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.me:
        await reaction.message.delete(delay=1)


async def echo_server(reader, writer): #the start of hell
    data = ""
    writer.write("a\n".encode('utf-8'))
    while True:
        instream = await reader.read(100)  # Max number of bytes to read
        
        #print(instream)
        if not instream:
            break
        instream = str(instream)[2:-1]
        if instream == "\\x08": data = data[:-1]
        elif instream == "\\x0": data = data[:-1]
        elif instream != "\\r\\n":
             data += instream
        else:
            if data[0] == "#":
                out = []
                for x in client.server.channels:
                    if data[1:] in x.name: out.append(x)
                    if data[1:] == x.name:
                        out = [x]
                        break
                if len(out) == 1: 
                    client.channel = out[0]
                    print(f"message delivery channel switched to {client.channel}")
                elif len(out) > 1:
                    
                    writer.write(b"----------\n")
                    for x in out:
                        writer.write(f"{x}\r\n".encode('utf-8'))
                    writer.write(b"----------")
                    writer.write("Please specify what channel to go to\n".encode('utf-8'))
                else:
                    writer.write("Channel not found, try again".encode('utf-8'))
                
            elif data[0] == "$":
                if len(data) == 1: client.nick = "notepad.exe"
                else: client.nick = data[1:]
                print(f"nickname switched to {client.nick}")
                writer.write("Nickname changed".encode('utf-8'))
            
            else:
                webh = discord.utils.find(lambda m: m.name == "notepad", await client.channel.webhooks())
                if not webh: webh = await client.channel.create_webhook(name="notepad", reason="candy lol")
                try:
                    await webh.send(data, username = client.nick, file=discord.File('upload.png'))
                except:
                    await webh.send(data, username = client.nick)
            #writer.write(data)
            data = ""
            await writer.drain()  # Flow control, see later
    writer.close()
async def start_server(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()
    
async def append_scr(disp:str, id:int):
    client.log[0].append(disp)
    client.log[1].append(id)
    if len(client.log[0]) > 30:
        client.log[0].pop(0)
        client.log[1].pop(0)
    await upd_scr()

async def upd_scr():
    os.system('cls')
    for x in client.log[0]:
        print(x)

client.run(TOKEN)
#error: discord.notFound
