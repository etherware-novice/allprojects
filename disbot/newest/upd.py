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

# todo: add self.log channel



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
		
		await self.log(ctx, "rng")

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
		
		await self.log(ctx, "dnd dice")


	@commands.Cog.listener()
	async def on_message(self, message):

		role1 = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'candycane', message.guild.roles)
		if role1 in message.author.roles or role2 in message.author.roles: await self.log(message, "weem")

		elif message.author != self.bot.user and "weem" in message.content:
			await message.delete()
			await message.channel.send(f"{message.author} has been weem blocked")
			await self.log(message, "weem", "the message was deleted")



	async def log(self, ctx, cmd, act = "nothing happened"):
		try:
			msg = f'[{ctx.guild}]: User [{ctx.author}] sent [{cmd}] in #{ctx.channel} and {act}'
		except:
			msg = f'[{ctx.guild.name}]: User [{ctx.author}] used [{cmd}] command in #{ctx.channel}'
		
		channel = self.bot.get_channel(825935386684686346)
		
		print(msg)
		await channel.send(msg)

def setup(bot):
	bot.add_cog(General(bot))
	



