#def timeup(format):
#	return datetime.now.strftime(format)

from discord.ext import commands
import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
import json
from dotenv import load_dotenv

# todo: add self.log channel



class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		print("abc") #check to if the thing is starting up

		self.weemcnt = jsonfile('0') #json files used initilizer (look at jsonfile below for more info)
		self.testmr = jsonfile('ignore.json')
		self.mdb = jsonfile('msgwm.json')



	#simple dm user on join function
	@commands.Cog.listener() 
	async def on_member_join(self, member): #when a member joins:
		await member.send( #member.send is send a dm with this info
				f'Hi {member.name}, welcome to my test server!'
			)




	#random num generator
	@commands.command(name='rng', help='Responds with a random number')
	#now = timeup("%H:%M")
	async def randreturn(self, ctx): #function used here
		response =  random.randint(0, 500) #generates a number
		await ctx.send(response) #sends to the same channel the command was entered
		#await ctx.send('new')
		#await asyncio.ensure_future(self.testmr.astim(ctx, 15, 60)) #sets a timer for 15 minutes (15 seconds * 60)
		await self.log(ctx, "rng") #calls log func




	#a dnd dice generator
	@commands.command(name='dndr', help="Returns a certain number of dice with modifiers")
	async def dnd(self, ctx, size:int, num:int, mod:int):
		dice = [random.randint(1, size) for _ in range(num)] #i think this is getting the dice roll nums idk how this works

		numsum = 0
		for d in dice:
			numsum += d #adds up all the dice
		
		await ctx.send(dice) #neat little flavor text im proud of it
		await ctx.send(f'{numsum} + {mod}')
		numsum += mod
		await ctx.send(numsum)
		
		await self.log(ctx, "dnd dice") #logs it


	#tester using other user
	@commands.command(name='usr', help='testing a command with a separate user')
	async def usr(self, ctx, user: discord.Member):
		await ctx.send(await (self.chkrl(ctx, user))) #calls for checkrole function with input user
		await ctx.send(await (self.chkrl(ctx, ctx.message.author))) #call for checkrole func with the member who triggered 
		ctx.message.author = user



	




	#this was a testing program i just kinda left in to play with
	@commands.command(name='dbt', help='input a number to increase/decrease your individual database entry')
	async def dbe(self, ctx, mod:int): #function
		#usr = f"{ctx.author.display_name} - {ctx.author.discriminator}" #gets the name of the user in readabl
		usr = ctx.author.name

		try: num = self.mdb.data[usr] #attempts to retrieve the existing data
		except: num = 0 #fallback data/init num

		num += mod #modifies the number with the input 
		if num > 9999999999999999999999999999999999999999999999999999999999999999999: await ctx.send(f"{ctx.author}, the number is way too big") #hard limit instead of the bit limit
		else:
			await ctx.send(num) #returns num
			self.mdb.edit(usr, num) #modifies the user's databawse file
			await self.log(ctx, "mini database edit") #log log log

		#print(f'{ctx.author.id} ({ctx.author.display_name} - {ctx.author.discriminator})')




	#mini asyncronous timer test
	@commands.command(name='time', help='testing async timers')
	async def time(self, ctx, tm:int):
		await ctx.send(f'initilizing timer for {tm} seconds') #flavor text
		#await asyncio.ensure_future(self.testmr.astim(ctx, tm)) #the actual stuff
		await ctx.send(f'timer for {tm} seconds done') #flavor text



	#@commands.Cog.listener()
	#async def on_message(self, message):




	#integration ping blocker
	@commands.Cog.listener()
	async def on_message(self, message):
	#await self.chkrl(ctx, user)
	#weemcnt.data[user]
	#weemcnt.edit

		print('---------')
		#ctx = await self.bot.get_context(message)
		user = message.author.id
		try:
			data = self.weemcnt.data[user]
			print('data loaded good')
		except:
			self.weemcnt.data[user] = data = 0


		print(f'data - {data}')


		try:
			#sudo = await self.chkrl(ctx, message.author)
			sudo = 0

			print(f'sudo - {sudo}')

			print(self.weemcnt.data)

			if "a" in message.content and sudo != 1 and message.author != self.bot.user:

				try:
					print('weem')

					data += 1
					print(f'data inc - {data}')
					self.weemcnt.edit(user, data)
					print(f'db save - {self.weemcnt.data[user]}')


					try: 
						self.weemcnt.timer[user]
						print('timer var loaded')
					except:
						self.weemcnt.timer[user] = -1
						print('timer cvar created')

					print(f'timer - {self.weemcnt.timer}')

					if self.weemcnt.timer[user] < 0: 
						asyncio.ensure_future(self.weemcnt.astim(user, 30))
						print('timer trig')

					print(f'data right before check {data}')
					print(f'timer - {self.weemcnt.timer}')
					if data >= 5:

						print('extra')

						await message.delete()
						await message.channel.send(f'You are blocked from sending a for {self.weemcnt.timer[user]} seconds')
				except Exception as e:
					print(f'uh oh, something happened {e} - ')


		except:
			if '@' in message.content: #checks if the @ sign is in the msg
				await message.delete() #delete
				await self.log(message, 'ping using the freaking tuppers', 'the message was deleted')

		await self.bot.process_commands(message)


# heres the manual utility commands used here

	#log functs
	async def log(self, ctx, cmd, act = "nothing happened"):
		try:
			if ctx.me == 0: print('what is ctx me?') #checks if ctx.me exists which will always fail if <message> is used instead of <ctx>
			msg = f'[{ctx.guild.name}]: User [{ctx.author}] used [{cmd}] command in #{ctx.channel}' #sets the string to be logged
		except: #this will only be triggered if a messaege obj is imported
			msg = f'[{ctx.guild}]: User [{ctx.author}] sent [{cmd}] in #{ctx.channel} and {act}' #sets the string to be logged
                        
		
		channel = self.bot.get_channel(825935386684686346) #look i dont know how namespace works im just setting this var constantly
		
		print(msg) #outputs message to command line
		await channel.send(msg) #sends the log string to the log channel

	async def chkrl(self, ctx, user: discord.Member):
		modrl = [ #list of roles that are "elevated"
			"Admin",
			"candycane"
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


		return 0 #final fallback



#json file related class

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
		self.timer = {"null": 1} #initilizes the timer class var


	#overrides the json with input
	def write(self, input): 
		if self.file != "0": #checks if a file was input
			with open(self.file, "w") as file: #opens up the file for writing
				file.write(json.dumps(input, indent=4)) # formats and beautifies the JSON as a string and overwrites the file contents with it
		self.data = input #updates the data var to make sure its uptodate
		print(self.data)

	#local timer funct

	#editing function
	def edit(self, entry:str, inp):
		print(entry)
		print(inp)
		self.data[entry] = inp #replaces the <entry> with input
		print('zyx')
		self.update() #invokes write function

	#a simpler version of write that just writes the current state of data to the file
	def update(self):
		self.write(self.data) #write function invoked


	#@commands.Cog.listener()
	async def astim(self, user, time, multi = 1):
		time = time * multi #self-explanatory, added this so you dont have to calculate for minutes or hours and you can just change multi field
		
		
		for x in range(time, 0, -1): #for loop counting down
			self.timer[user] = x #updates the timer variable
			await asyncio.sleep(1) #wait for one second but asyncronously

		self.timer[user] = -1 #sets the timer to -1 denoting its inactive
		self.edit(user, 0) #edits the original message trigger author's entry to 0
		#return
	#async 	

#some boilerplate code that makes the cog functionable
def setup(bot):
	bot.add_cog(General(bot))
	



