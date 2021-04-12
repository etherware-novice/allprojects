import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import traceback
from discord.ext import tasks
intents = discord.Intents.default() #sets up the intents obj
intents.members = True #flips the member inperwhatever it is to true

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

bot = commands.Bot(command_prefix='am!', intents=intents) #initilizes the bot
bot.obj = []


#flavorie text to make sure its working good
@bot.event
async def on_ready(): #initilization

    guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

    print(discord.utils.get(bot.guilds))

    print(
    	f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    await bot.change_presence(activity=discord.Game(name='amogus bot :)')) #:)


@bot.event
async def on_reaction_add(reaction, user):
	if user != bot.user and reaction.emoji == u"\U0001F44D":
		msg = await reaction.message.channel.send(f'{user} reacted with :thumbsup:')
		await asyncio.sleep(5)
		await msg.delete()
		await bot.ogmsg.delete()
		await bot.reactmsg.delete()


@bot.command(name='test')
async def react(ctx):
	bot.reactmsg = ctx.message
	bot.ogmsg = await ctx.send('reaction msg')
	await bot.ogmsg.add_reaction(u"\U0001F44D") #thumbs up

@bot.command(name='add')
async def add(ctx):
	bot.obj[0].add_user(ctx.author)
	await bot.obj[0].statusmsg(ctx)

@bot.command(name='init')
async def init(ctx, name, code):
	bot.obj.append(gameobj(ctx, name, code))
	




class gameobj(object):
	"""docstring for gameobj"""
	def __init__(self, ctx, name:str, code:str):
		super(gameobj, self).__init__()
		self.code = code
		self.active = []
		self.wait = []
		self.name = name
		self.host = ctx.author
		print(self.host)
		asyncio.ensure_future(self.statusmsg(ctx))

	def add_user(self, user: discord.Member): #delete this, this will be replaced by reacting to statusmsg
		self.active.append(user)

	async def statusmsg(self, ctx):
		msg = f'Host: {self.host} \nCode: {self.code} \nGame name: {self.name} \n\n'

		for x in range(10):
			try:
				msg += f'{str(self.active[x])} \n'
			except:
				msg += '[Empty] \n'

		await ctx.send(msg)
		


bot.run(TOKEN) #runs everything else