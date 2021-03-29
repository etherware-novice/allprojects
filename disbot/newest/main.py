def main():
	import os

	import discord
	import random
	from discord.ext import commands
	import asyncio
	from datetime import datetime
	from dotenv import load_dotenv
	intents = discord.Intents.default()
	intents.members = True

	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	GUILD = os.getenv('DISCORD_GUILD')

	bot = commands.Bot(command_prefix='!')

	@bot.event
	async def on_ready():
	    
	    guild = discord.utils.get(bot.guilds, name=GUILD)

	    print(
	    	f'{bot.user} is connected to the following guild:\n'
	        f'{guild.name}(id: {guild.id})'
	    )

	    await bot.change_presence(activity=discord.Game(name='candycane\'s bot :)'))
	    


	@bot.command(name='reload', help='Reloads the python commands')
	async def relbot(ctx, state=0):
		brn = "HEAD"
		if state == 1: brn = "master"
		elif state == 2: brn = "discordbotnew3andknuckles"

		os.system(f"git checkout {brn}")
		os.system("git pull origin")
		print(f'[{ctx.guild.name}]: User [{ctx.author}] used [restart] command on state {state}')
		await ctx.send(f'{ctx.author} reloaded the bot.')
		bot.reload_extension("upd")

	bot.load_extension("upd")
	bot.run(TOKEN)
main()