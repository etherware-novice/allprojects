#def timeup(format):
#	return datetime.now.strftime(format)

from discord.ext import commands
import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# todo: add log channel



class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print("abc")

	@commands.Cog.listener()
	async def on_member_join(self, member):
		print("tst")
		await member.send(
				f'Hi {member.name}, welcome to my test server!'
			)

	@commands.command(name='rng', help='Responds with a random number')
	#now = timeup("%H:%M")
	async def randreturn(self, ctx):
		response =  random.randint(0, 500)
		await ctx.send(response)
		#await ctx.send('new')
		await log(ctx, "rng")

	@commands.command(name='dndr', help="Returns a certain number of dice with modifiers")
	async def dnd(self, ctx, size:int, num:int, mod:int):
		dice = [random.randint(1, size) for _ in range(num)]

		numsum = 0
		for d in dice:
			numsum += d
		
		await ctx.send(dice)
		await ctx.send(f'{numsum} + {mod}')
		numsum += mod
		await ctx.send(numsum)
		await log(ctx, "dnd dice")


	@Bot.event
	async def on_message(ctx, message):

		if "weem" in message.content:
			await message.delete(message)
			await ctx.send(f"{message.author} has been weem blocked")
			await log(ctx, "anti weem (not command)")

def setup(bot):
	bot.add_cog(General(bot))

async def log(ctx, cmd):
	print(f'{[ctx.guild.name]}: User [{ctx.author}] used [{cmd}] command in #{ctx.channel}')
	
	bot = ctx.bot
	channel = bot.get_channel(825935386684686346)
	await channel.send(f'[{ctx.guild.name}]: User [{ctx.author}] used [{cmd}] command in #{ctx.channel}')
