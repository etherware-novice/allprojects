from discord.ext import commands
import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from discord.ext import tasks
import json
from dotenv import load_dotenv



class misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.data = jsonfile('catchlg.json')
		self.actmr = None


	@commands.group(pass_context=True)
	async def testg(ctx):
		await ctx.send('inv')
		if ctx.invoked_subcommand is None:
			await ctx.send('no')

	@testg.command(pass_context=True)
	async def group(ctx):
		await ctx.send('yes', delete_after=3)


	@commands.command(name='catch')
	async def check_catch(self, ctx, rng:int):


		print('double')

		try:
			cur = self.data.data[ctx.author.id]
		except:
			cur = 0
			self.data.edit(ctx.author.id, 0)

		if self.data.timer['active'] != -1 and not ctx.author.bot: #if theres an active thing going on rn 
			print(self.data.num)
			if rng == self.data.num:
				self.actmr.cancel() #stops the active timer
				print('starting cooldn')
				asyncio.ensure_future(self.data.astim('cooldn', 30, 1, -1)) #sets the cooldown
				self.data.edit(ctx.author.id, cur + 1)
				await ctx.send(f'Congratulations, {ctx.author.name}! Your score is now {self.data.data[ctx.author.id]}!', delete_after=5)
			else: await ctx.send(f'Sorry {ctx.author.name}, wrong number!', delete_after=5)
		else:
			await ctx.send(f'Sorry, {ctx.author.name}! There is no active event!', delete_after=5)


	@commands.Cog.listener('on_message')
	async def randspawn(self, message):
		#ng = random.randint(0, 20)
		ng = 1
		if ng == 0 and message.author.bot == False and self.data.timer['active'] == -1 and self.data.timer['cooldn'] == -1:
			self.data.num = random.randint(-999, 999)
			print(f'the return num{self.data.num}')
			self.actmr = asyncio.ensure_future(self.data.astim('active', 20, 1, -1))
			await message.channel.send(f'An event has started! Type a!catch {self.data.num} in the next 20 seconds to get a point!', delete_after=20)



class jsonfile(object):
	"""docstring for jsonfile"""

	def __init__(self, file:str = "0"): #file is an actual argument
		super(jsonfile, self).__init__() #idk what this does but i feel like it might break if i remove
		self.file = file #makes the argument file a class var

		if file == "0": #alternate option to make it not write to file and reset on shutdown
			self.data = {"null": 1} #sets the data class var up

		else: #if a file was input
			try: #attempts to load said file (will always fail if the file doesnt exist..yet)
				with open(self.file) as file: #attempts to load the file that was inputted
					self.data = json.load(file) # parses the JSON data in the file and returns a dictionary assigned to class var data
			except: #if the file doesnt exist yet
				try: 
					file = file.name #IODataWrapper preventer
				except:
					file = file #throwaway except function so that except runs something

					self.data = {"null": 1} #still makes sure data exists to not error out
					self.write(self.data) #invokes the local write function to write out the file
		self.timer = {"null": 1, "active": -1, "cooldn": -1} #initilizes the timer class var
		self.num = 0


	#overrides the json with input
	def write(self, input): 
		if self.file != "0": #checks if a file was input
			with open(self.file, "w") as file: #opens up the file for writing
				file.write(json.dumps(input, indent=4)) # formats and beautifies the JSON as a string and overwrites the file contents with it
		self.data = input #updates the data var to make sure its uptodate\

	#local timer funct

	#editing function
	def edit(self, entry:str, inp):
		self.data[entry] = inp #replaces the <entry> with input
		self.update() #invokes write function

	#a simpler version of write that just writes the current state of data to the file
	def update(self):
		self.write(self.data) #write function invoked


	#@commands.Cog.listener()
	async def astim(self, user, time, multi = 1, post = 0):
		time = time * multi #self-explanatory, added this so you dont have to calculate for minutes or hours and you can just change multi field
		
		
		for x in range(time, 0, -1): #for loop counting down
			self.timer[user] = x #updates the timer variable
			print(x)
			await asyncio.sleep(1) #wait for one second but asyncronously

		self.timer[user] = -1 #sets the timer to -1 denoting its inactive
		#self.edit(user, post) #edits the original message trigger author's entry to 0


#some boilerplate code that makes the cog functionable
def setup(bot):
	bot.add_cog(misc(bot))
	
