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


bot = commands.Bot(command_prefix='!', intents=intents) #initilizes the bot]
bot.token = TOKEN

#flavorie text to make sure its working good
@bot.event
async def on_ready(): #initilization

    #guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    disp_guild = ''
    for x in bot.guilds:
        disp_guild += f'{x.name} ({x.member_count} members)\n'
        #await x.me.edit(nick = 'the amogus bot')

    print(
    	f'{bot.user} is connected to the following guilds:\n'
        f'{disp_guild}'
    )

    await bot.change_presence(activity=discord.Game(name='candy\'s bot')) #:)
    

@bot.listen('on_message')
async def checkin(message):
    suggestions = bot.get_channel(839881312306724904)
    if message.channel.id == suggestions.id and message.content[:2] == 's:' and not message.author.bot:
        await message.add_reaction(u"\U00002705") #adds the check up reaction
        await message.add_reaction(u"\U0000274c") # adds x
    pass

@bot.listen('on_reaction_add')
async def confirm(reaction, user):
    suggestions = bot.get_channel(839881312306724904)
    ctx = await bot.get_context(reaction.message)
    sudo = await chkrl(ctx, user)
    print(f"sudo: {sudo}")
    if reaction.emoji == u"\U00002705" and not user.bot and sudo == 1:
        print('check')
        if reaction.message.channel.id == 839881312306724904:
            print('suggest')
            embed = discord.Embed(title="Suggestion Entry", colour=discord.Colour(0x91a956), url="https://discordapp.com", description=f"```{reaction.message.content[3:]}```")

            embed.set_author(name=user, url="https://discordapp.com", icon_url=user.avatar_url)
            embed.set_footer(text=f"Original request by {reaction.message.author}", icon_url=user.avatar_url)

            embed.add_field(name="Press :white_check_mark: to delete the case", value="beep")

            #await suggestions.send(embed=embed)
            async with aiohttp.ClientSession() as session:
                webh = Webhook.from_url("https://canary.discord.com/api/webhooks/840003125594161152/8qkHB_l-hIdEdH2h_BQiE7lGkeMXk8qvtF3fg7DnXqVC1N64omrYIM5BAJceHgSrhPdN", adapter=AsyncWebhookAdapter(session))
                tmp = await webh.send(embed=embed, wait=True)
                tmpa = bot.get_channel(839968356253696072).get_partial_message(tmp.id)
                await tmpa.add_reaction(u"\U00002705")
            await reaction.message.delete()
            
        if reaction.message.channel.id == 839968356253696072:
            print('adsuggest')
            await reaction.message.delete()
    if reaction.emoji == u"\U0000274c" and reaction.message.channel.id == 839881312306724904 and not user.bot and sudo == 1:
        print('x')
        await reaction.message.delete()
        

async def chkrl(ctx, user: discord.Member):
		modrl = [ #list of roles that are "elevated"
			"Alpha",
            "mod pup",
            661044029110091776
		]
		blacklist = [ #list of member roles
			"User",
			"user",
			813469324328173608
		]


		for x in modrl:
			if isinstance(x, str): x = discord.utils.find(lambda r: r.name == x, ctx.guild.roles) #if its a string, use utils.find to get the role obj
			elif isinstance(x, int): x = ctx.guild.get_role(x) #if not string, but is an int, simply use get_role to get role obj
			if x in user.roles: return 1 #checks if the input user has the role from blacklist, if yes, returns -1
		for x in blacklist: #for every entry in blacklist
			if isinstance(x, str): x = discord.utils.find(lambda r: r.name == x, ctx.guild.roles) #if its a string, use utils.find to get the role obj
			elif isinstance(x, int): x = ctx.guild.get_role(x) #if not string, but is an int, simply use get_role to get role obj
			if x in user.roles: return -1 #checks if the input user has the role from blacklist, if yes, returns -1



bot.run(TOKEN) #runs everything else