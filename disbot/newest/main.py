def main():
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
	GUILD = os.getenv('DISCORD_GUILD')

	bot = commands.Bot(command_prefix='a!', intents=intents) #initilizes the bot

	channel = bot.get_channel("825935386684686346") #log channel where everything is sent

	
	@commands.command()
	async def load(self, *, module): #a thing i copied thats supposed to display module errors but it doesnt work that well
		"""Loads a module."""
		try: 
			self.bot.load_extension(module)
		except Exception:
			e = discord.Embed(description=traceback.format_exc())

	@bot.event
	async def on_ready(): #initilization

	    guild = discord.utils.get(bot.guilds, name=GUILD) #gets the guild that i put in to kinda add some flavor text

	    print(
	    	f'{bot.user} is connected to the following guild:\n'
	        f'{guild.name}(id: {guild.id})'
	    )

	    


	    await bot.change_presence(activity=discord.Game(name='candycane\'s bot :)'), status=discord.Status.dnd) #:)

	@bot.event
	async def on_disconnect():

		await bot.change_presence(status=discord.Status.offline)
		print('so long gay bot!')


	@bot.command(name='reload', help='Reloads the python commands') #special command that accesses this repo and pulls/switches branches (this is why upd.py exists)
	async def relbot(ctx, state=0):
		bot = ctx.bot #re-attains the bot obj but i dont think i use it here oops
		channel = bot.get_channel(825935386684686346) #im not 10000% sure how namespace works here so just incase
		
		brn = "HEAD" #sets the branch to HEAD so the checkout command below doesn't error if a state isnt input
		if state == 1: brn = "master" # switches which branch is being checked out
		elif state == 2: brn = "discordbotnew3andknuckles"

		os.system(f"git checkout {brn}") #switch branch
		os.system(f"git pull origin") #and re pulls it

		print(f'[{ctx.guild.name}]: User [{ctx.author}] used [restart] command on state {state}') #log to the python file itself
		await channel.send(f'[{ctx.guild.name}]: User [{ctx.author}] used [restart] command on state {state}') #log to log channel
		await ctx.send(f'{ctx.author} reloaded the bot.') #flavor text sent to the channel that triggered it

		bot.reload_extension("upd") #reloads upd.py
		bot.reload_extension("misc") #reloads upd.py

	bot.load_extension("upd") #init load of upd.py
	bot.load_extension("misc") #init load of upd.py
	bot.run(TOKEN) #runs everything else

	

main() #runs everything else

#dont ask why everything is in a main func