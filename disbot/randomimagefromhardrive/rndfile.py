import re, os, time, sys

import discord, yaml, asyncio
from datetime import datetime as datetime
import random

from discord.ext import tasks



intents = discord.Intents.default() #sets up the intents obj
#intents.members = True #flips the member inperwhatever it is to true
TOKEN = None
cls = "\u001B[2J"

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

    client.cnl = client.get_channel(888953410034995211)

    load_img.start()

@tasks.loop(seconds=120)
async def load_img():


    print("load")
    nof = ("Downloads\\fnf", "Downloads\\friday", "Funkin", "weeb", "hilar", "FNFM", "preload", "DialogueModGB", "flixel", *["week" + str(x) for x in range(7)], 
    "funkin-windows-64bit", "export\\debug", "AppData", "export\\debug", "resourcepacks", "FTB", "parapparatingmod_v1_2_1_f11c3", 
    "Tahoma")
    image = random.choice( [f"{cur}\\{x}" for cur, dirs, files in os.walk("C:\\Users") for x in files if os.path.splitext(x)[1] in (
        ".jpeg", ".jpg", ".png", ".kra", ".kri", ".webp", ".mp4", ".gif"
        ) and not any([y in cur for y in nof])] )

    print(image)

    conf = await client.cnl.send(f"<@661044029110091776>\n{image}", file=discord.File(image))

    print(conf)
    try:
        await client.wait_for('raw_reaction_add', check=lambda m: m.message_id == conf.id, timeout=30.0)
        await client.get_channel(888954846370234368).send(re.sub(r"(C:\\Users\\).*?(\\.*)", r"\1\\[user]\2", f"{image}\n"), file=discord.File(image))
    except (asyncio.TimeoutError, discord.errors.HTTPException):
        print("didnt react in time")
        await client.cnl.send("ran out of time..", delete_after=30)
        pass

    try: await conf.delete()
    except: pass




client.run(TOKEN)



"""
imgs = []
for cur, dirs, files in os.walk("C:\\"):
    
    for x in files:
        if x[-4:] in (".jpg", "jpeg", ".png"):
            x = f"{cur}\\{x}"
            imgs.append(x)

print("\n")
print(len(imgs))"""