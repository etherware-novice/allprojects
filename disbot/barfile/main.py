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
client.supress = False

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

    
    notepad = client.get_channel(861348653113540628)
    client.channel = notepad
    client.nick = "notepad.exe"
    client.lastmg = None

    client.log = []
    strup = f"Discord version {discord.__version__}"
    strup += "\nTEXT-BASED-INTERFACE-CLIENT.exe starting..."
    #flavor text
    now = datetime.now()
    curtime = now.strftime("%B %d, %Y at %H:%M")
    strup += f"\nHello, user <{getpass.getuser()}>. Today's datetime is {curtime}.\n"
    strup += f"\n{client.user} is connected to the following guilds:\n{disp_guild}"

    if not client.supress: await append_scr(strup, 0)

    asyncio.ensure_future(start_server('127.0.0.1', 5000))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    mentions = []
    mentions = message.mentions
    mentionsrole = message.role_mentions
    mentionschn = message.channel_mentions

    if len(message.mentions) > 0 or len(message.role_mentions) > 0 or (len(message.channel_mentions)) > 0:
        x = 0
        def getping(m):
            #asyncio.ensure_future(append_scr(m, 0))
            m = m.group()
            #asyncio.ensure_future(append_scr(m, 0))
            number = re.findall(r'\d+', m)
            number = int(number[0])
            print(number)
            #asyncio.ensure_future(append_scr(m, 0))
            if m.startswith("<@") or m.startswith("@"):
                #asyncio.ensure_future(append_scr(0, 0))
                name = client.get_user(number)
                return color(f"@{name.display_name}", fore=(90, 126, 224))
            if m.startswith("<@&") or m.startswith("&") or m.startswith("@&"):
                #asyncio.ensure_future(append_scr(1, 0))
                name = message.guild.get_role(number)
                return color(f"{name.name}(role)", fore=(90, 126, 224))
            if m.startswith("<#") or m.startswith("#"):
                #asyncio.ensure_future(append_scr, 0)
                name = client.get_channel(number)
                return color(f"#{name.name}", fore=(90, 126, 224))
#re.search("^<#.>$", m).group()

        message.content = re.sub("([@#!])\w+", getping, message.content)
        #asyncio.ensure_future(append_scr(message.content, 0))

    rng = random.randint(0, 50)
    await append_scr(await msgformat(message, rng), message.id, True)
    if rng <= 3:
        await generate(message)

@client.event
async def on_typing(channel, user, when):
   if not client.suppress: print(color(f"{user.display_name} is typing in {channel.name}", fore=(137, 154, 196)))

@client.event
async def on_message_update(before, after):
    def tmp(labl, new):
        return color(f"{after.display_name} has changed their {labl} to {new}", fore=(137, 154, 196))
    if before.status != after.status: print(tmp("status", after.status))
    if before.activities != after.activities: print(tmp("activity", after.activites.name))
    if before.nickname != after.nickname: print(tmp("nickname", after.nickname))
    if before.roles != after.roles: print(f"{after.display_name}'s roles before:\n {0}\nafter:\{1}",before.roles, after.roles)

@client.event
async def on_user_update(before, after):
    def tmp(labl, new):
        return color(f"{after.display_name} has changed their {labl} to {new}", fore=(137, 154, 196))
    if before.username != after.username: print(tmp("username", after.username))

@client.event
async def on_guild_remove(guild):
    print(f"Bot was disconnected from {guild.name}")

@client.event
async def on_message_edit(before, after):
    for x in client.log:
        if after.id == x["id"]:
            dum = "(edited)"
            x["cont"] = f"{await msgformat(after)} {color (dum, fore=(74, 74, 74))}"
            await upd_scr()
            break

@client.event
async def on_message_delete(message):
    dele = None
    for x in range(len(client.log)):
        if client.log[x]['id'] == message.id:
            del client.log[x]
            break
    await upd_scr()

@client.event
async def on_member_join(member):
    await append_scr(color (f"{member.display_name}) joined the server.", fore=(60, 31, 128)), 0)

@client.event
async def on_member_remove(member):
    await append_scr(color(f"{member.display_name} left the server", fore=(235, 99, 99)))

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
    await append_scr(f"rng {rng}, which reffers to message: {message}", 0)
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
        print(0)
    elif reaction.me:
        await reaction.message.delete(delay=5)

    new = 1
    for x in client.log:
        if x["id"] == reaction.message.id: 
            new -= 1
            try:
                x["reaction"][reaction.emoji] += 1
            except:
                x["reaction"][reaction.emoji] = 1
    await upd_scr()

@client.event
async def on_reaction_remove(reaction, user):
    for x in client.log:
        if x["id"] == reaction.message.id:
            x["reaction"][reaction.emoji] -= 1
            if x["reaction"][reaction.emoji] == 0: x.pop(reaction)
    await upd_scr()


async def echo_server(reader, writer): #the start of hell
    data = ""
    writer.write("a\r\n".encode('utf-8'))
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
            try:
                if data[0] == "#":
                    out = []
                    for x in client.server.channels:
                        if data[1:] in x.name: out.append(x)
                        if data[1:] == x.name:
                            out = [x]
                            break
                    if len(out) == 1: 
                        client.channel = out[0]
                        await append_scr(f"message delivery channel switched to {client.channel}", 0)
                    elif len(out) > 1:
                        
                        writer.write(b"----------\n")
                        for x in out:
                            writer.write(f"{x}\r\n".encode('utf-8'))
                        writer.write(b"----------")
                        writer.write("Please specify what channel to go to\n".encode('utf-8'))
                    else:
                        writer.write("Channel not found, try again".encode('utf-8'))
                    
                elif data[0] == "$":
                    if data == "$": client.nick = "notepad.exe"
                    elif data == "$$":
                        if client.supress != True: 
                            client.supress = True
                            os.system("cls")
                        else: 
                            client.supress = False
                            print("Screen supression disabled")
                            await upd_scr()
                            
                    else: client.nick = data[1:]
                    if data != "$$":
                        await append_scr(f"nickname switched to {client.nick}", 0)
                        writer.write("Nickname changed\r\n".encode('utf-8'))
                elif data.startswith("e$"):
                    await client.lastmsg.edit(content=data[2:])
                    writer.write(b"Message edited.\r\n")
                elif data.startswith("d$"):
                    await client.lastmsg.delete()
                    writer.write(b"Message deleted.\r\n")
                elif data.startswith("ts$"):
                    x = await client.channel.send(content=client.user.mention)
                    print(x.content)
                    writer.write(b"0\r\n")
                
                else:
                    webh = discord.utils.find(lambda m: m.name == "notepad", await client.channel.webhooks())
                    if not webh: webh = await client.channel.create_webhook(name="notepad", reason="candy lol")
                    try:
                        file = discord.File('upload.png')
                    except:
                        file = None
                    client.lastmsg = await webh.send(data, username = client.nick, file=file, wait = True, avatar_url="https://cdn.discordapp.com/attachments/859869321592045599/861779701058764820/upload.png")
                #writer.write(data)
            except Exception as e:
                print(e)
                writer.write(b"you fool put actual text\r\n")
            finally:
                data = ""
                await writer.drain()  # Flow control, see later
    writer.close()
async def start_server(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()


async def msgformat(message, rng = None):
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
    
    retr = f'{bel}{rng}[{date} in #{color (message.channel, fore=(34, 245, 87))}] {dispn}: {message.content}{ath}'
    return retr
    
async def append_scr(disp, id:int, upd=True):
    client.log.append(
        {
            "cont": disp,
            "id": id,
            "reaction": {}
        }
    )
    if len(client.log) > 70:
        client.log.pop(0)
    if upd: await upd_scr()
    else:
        print("disp")

async def upd_scr():
    if client.supress != True:
        (os.system('cls'))
        for x in client.log:
            print(x["cont"])
            if len(x["reaction"]):
                #print("\n")
                for key, items in x["reaction"].items():
                    print(f"{key}({items})    ")


client.run(TOKEN)
#error: discord.notFound
