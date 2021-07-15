
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
from discord_slash import SlashCommand 

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

global multi, ovr
ovr = 0
multi = 1

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

    bot.exc = lambda n, e: f"ERROR ```{n[0].__name__}: [{e}] on line {n[2].tb_lineno}``` was thrown, talk to {bot.get_user(661044029110091776).mention}"



@bot.listen("on_message")
async def rand(message):
    if random.randint(0, 40) == 0: await random.choice(bot.gif).send(message)
    #elif message.content == "!whl": await bot.gif[0].send(message, True)
    elif message.content == "!ovr": await bot.gif[1].send(message, True)
    elif message.content == "!grt": await bot.gif[2].send(message, True)
    elif message.content == "!rnd": await random.choice(bot.gif).send(message)
    elif message.content == "!rns": await random.choice(bot.gif).send(message, True)
    if message.content == "!reload" and message.author.id == 661044029110091776:
        os.system(('git pull'))
        subprocess.call(['python3', 'main.py'])

@bot.command(name="whl")
async def choose(ctx, num:int):
    try:
        await bot.gif[num].send(ctx, True)
    except IndexError:
        await ctx.send("Put a correct wheel index (do w!help to see the wheels)")
    except Exception as e: await ctx.send(bot.exc(sys.exc_info(), e))

@bot.command(name="rnd")
async def rand(ctx, t = False):
    try:
        t = bool(t)
        await random.choice(bot.gif).send(ctx, t)
    except Exception as e: await ctx.send(bot.exc(sys.exc_info(), e))

@bot.command(name="list")
async def list(ctx):
    try:
        out = ""
        for x, y in enumerate(bot.gif):
            out += f"{x} - {y.desc}\n"
        await ctx.send(f"```{out}```")
    except Exception as e: await ctx.send(bot.exc(sys.exc_info(), e))


async def timer(mins, channel, target, message):
    #time.sleep(minutes * 60)

    print(f"Timer for {mins} mins")
    await asyncio.sleep(mins * 60 * multi)
    print("Timer up")
    await channel.send(f"{target.mention}, your curse [{message}] has been lifted!")

class gifGen:
    def __init__(self, desc, gif:str = None, message:str = "", m_post:str = ""):
        self.gif = Image.open(gif) if gif != None else gif
        self.message = message
        self.m_post = m_post
        self.desc = desc
    

    def picoGen(self):
        font = ImageFont.truetype("PressStart2P-Regular.ttf", 48) #the ttf font used
        tmp = Image.open('temp.png') #opens the stream of the template

        with open("line.txt", "r") as f:
            prompts = f.read().splitlines() #gets lines from line.txt

        rng = random.randint(0, len(prompts) - 1)
        x = prompts[rng]

        #starts the image gener
        im = Image.new('RGBA', (632, 412), (255, 255, 255, 0)) #creates a transparant image
        d = ImageDraw.Draw(im) #gets drawing object out of the im object
        buffer = io.BytesIO() 
        wrapper = textwrap.TextWrapper(width=12) #gets a text wrapper with max length of 12 (basically an object to wrap text)
        x = wrapper.fill(text=x) #returns the string of x with \n to keep it in the textwrapper
        d.multiline_text((310, 190), x, font = font, anchor = "mm", align="center", fill = (61, 99, 196)) 

        tmp.paste(im, (154, 312), im) #puts the text image in the correct place on the template img
        
        tmp.save(buffer, format="PNG")
        buffer.seek(0)
        return [buffer, rng]
    def imageget(self):
        global trip
        buffer = io.BytesIO()
        rng = random.randint(0, self.gif.n_frames - 1)
        print(f"frame {rng}")
        self.gif.seek(rng)
        #self.gif.seek(13)
        self.gif.save(buffer, format="PNG")
        buffer.seek(0)
        return [buffer, rng]
    
    async def getTarget(self, message, reroll):
        if random.randint(0, 1):
            target = random.choice(
                [x.author async for x in message.channel.history(limit=30)]
            )
        else: target = message.author
        if reroll: target = message.author
        return target

    async def specframe(self, target, frame, *, message, vers = -1):
        defaul = 30
        global multi
        if vers:
            index = {
                1: {"timer": [60, "Caps Locks"]},
                3: {"timer": [defaul, "Tricky Impersonating"]},
                4: {"timer": [defaul, "3AM Challenge"]},
                5: {"multi": 10},
                7: {"timer": [defaul, "Light Mode"]},
                13: {"timer": [defaul, "Changed PFP"]},
                18: {"timer": [10, "Can't Speak"]},
                19: {"timer": [15, "Heckclown"]},
                24: {"timer": [60, "100% VOLUME"]},
                26: {"timer": [defaul, "Opposite Day"]},
                28: {"timer": [180, "Weeb Speak"]},
                29: {"timer": [120, "Beep Boop"]},
                30: {"timer": [10, "1 Handed"]},
                33: {"timer": [30, "F*King Swearing"]},
                34: {"timer": [defaul, "Reversed Keyboard"]},
                35: {"timer": [defaul, "DDoouubbllee TTeexxtt"]},
                37: {"timer": [5, "One Eye"]},
                38: {"timer": [15, "Top Row Letters"]},
                40: {"timer": [10, "Tricky Death"]},
                42: {"timer": [42, "No Discord"]},
                43: {"timer": [43, "Phone Screenshots"]},
                46: {"multi": 3},
                49: {"timer": [defaul, "Only Images"]}
            }
        elif vers == 0:
            index = {
                4: {"timer": [10, "Poison"]},
                6: {"timer": [10, "Leg Freeze"]},
                9: {"timer": [defaul, "Beep Boop!"]},
                15: {"timer": [defaul, "Tupper Dissapearing"]},
                17: {"effect": "nchn"},
                20: {"multi": 3},
                22: {"timer": {120, "Roblox Chat Filter"}},
                25: {"effect": "wheel"},
                40: {"effect": "rchn"},
                44: {"timer": [defaul, "Server Nick"]}
            }
        else: index ={1: []}
        try:
            iframe = index[frame]
        except:
            pass

        try:
            x = iframe["timer"]
            asyncio.create_task(timer(x[0], message.channel, target, x[1]))
        except: pass
        try:
            multi = iframe["multi"]
            return "multi"
        except: pass
        try:
            if iframe["effect"] == "nchn": return message.channel.category.text_channels[self.message.channel.position - 1].mention
            if iframe["effect"] == "rchn": return random.choice(message.guild.channels).mention
        except: pass

        return ""

    async def send(self, message, reroll = False, retr=False):
        global multi
        img, rng = await asyncio.get_running_loop().run_in_executor(None, (self.picoGen if self.gif == None else self.imageget))
        
        while True:
            target = await self.getTarget(message, reroll)
            if target.id == 449671019511283722 and rng == 2: pass
            else: break
        
        string = await self.specframe(target, rng, message=message, vers=(0 if self.gif == None else 1))

        img.seek(0)

        d_usr = target.display_name if target.bot else target.mention
        d_x = f" (x{multi})" if multi != 1 else ""
        if string == "multi": d_x = ""
        d_orig = f" caused by {message.author}" if message.author.id != target.id else ""
        d = f"{string}\n{d_usr}, {self.message}{d_x}{d_orig}{self.m_post}"
        if retr: return (d, discord.File(img, f"frame{rng}.png"))
        tmp = await message.channel.send(d, file=discord.File(img, f"frame{rng}.png"))

        if target == bot.user:
            await message.channel.send("Wait, thats me..", delete_after=6)
            await asyncio.sleep(1)
            await message.channel.send("Ok that one doesnt count-", delete_after=5)
            await asyncio.sleep(5)
            await tmp.delete()

        if multi != 1 and string != "multi": multi = 1

bot.gif = [gifGen("Tricky", "image0.gif", "Face the wheel of DOOOOOOOOM", "!!"), gifGen("Pico", message="you have been hit by pico's bad luck", m_post="..."), gifGen("grunt", "mc0.gif", "", "take...this? (uhm idk dm candy with your suggestions for the message that should go here)")]
opt = [create_choice(name=y.desc, value=str(x)) for x, y in enumerate(bot.gif)]

slash = SlashCommand(bot, sync_commands=True)
@slash.slash(name="wheel", description="loads a wheel in current channel", 
            options=[
               create_option(
                 name="whel",
                 description="the wheel to load.",
                 option_type=3,
                 required=True,
                 choices=opt
               )
             ], guild_ids=[867934020422475796])
async def loadwh(ctx, whel:str): # Defines a new "context" (ctx) command called "ping."
    try:
        await ctx.defer()
        whel = int(whel)
        disp, buffer = await bot.gif[whel].send(ctx, True, True)
        await ctx.send(disp, file=buffer, allowed_mentions=discord.AllowedMentions().all())
    except Exception as e:
        await ctx.send(bot.exc(sys.exc_info(), e))

@slash.slash(name="rndwheel", description="random wheel that will target anyone randomly using random.choice",
            options=[
                create_option(
                    name="self_target",
                    description="whether to target anyone or only self",
                    option_type=4,
                    required=False,
                    choices=[
                        create_choice(
                            name="True",
                            value=1
                        ),
                        create_choice(
                            name=False,
                            value=0
                        )
                    ]
                )
            ], guild_ids=[867934020422475796])
async def rndwheel(ctx, self_target:int = 1):
    try:
        print(self_target)
        disp, buffer = await random.choice(bot.gif).send(ctx, (True if self_target == 1 else False), True)
        await ctx.send(disp, file=buffer, allowed_mentions=discord.AllowedMentions().all())
    except Exception as e:
        await ctx.send(bot.exc(sys.exc_info(), e))


bot.run(TOKEN)
