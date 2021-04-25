#def timeup(format):
#	return datetime.now.strftime(format)

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

# todo: add self.log channel



class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



		#self.truth.start()


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
		await self.testmr.astim(ctx.author, 10) #the actual stuff
		await ctx.send(f'timer for {tm} seconds done') #flavor text



	#@commands.Cog.listener()
	#async def on_message(self, message):




	#integration ping blocker
	@commands.Cog.listener('on_message')
	async def wm_cool(self, message):
		user = message.author.id #whats the database saved as

		ctx = await self.bot.get_context(message)

		blockmsg = "weem" #the part to block
		limit = 5 #how many can be sent before it starts to act
		try:
			data = self.weemcnt.data[user] #retrieves the current count
		except: #if it doesnt exist yet
			self.weemcnt.data[user] = data = [] #sets both to a empty list

		try:
			sudo = await self.chkrl(ctx, message.author) #checks the users roles
			#sudo = 0

			if blockmsg in message.content and sudo != 1 and message.author != self.bot.user: #if the block word is in the message and its not privledged or a bot,
				try:
					if len(data) != 0: data.append(message) #if its not the first entry, add the message (so the first msg doesnt get del'd)
					else: data.append(0) #placeholder
					self.weemcnt.edit(user, data) #updates the obj with the list

					try: 
						self.weemcnt.timer[user] #if the timer var for this funct doesnt exist
					except:
						self.weemcnt.timer[user] = -1 #sets it to a placeholder (-1)

					if self.weemcnt.timer[user] < 0: #if the timer is -1 (none running)
						asyncio.ensure_future(self.weemcnt.astim(user, 30, [])) #asyncronously start a 30 second timer

					if len(data) >= limit: #if the number of messages exceeds the limit

						if len(data) == limit: #the first time this happens,
							for x in data:
								if x != 0: await x.delete() #delete all entries in the list if they arn't the placeholder (0)
						else:
							await message.delete() #simply delete the trigger message

						await self.log(message, f"{blockmsg} spam", f'was blocked for the next {self.weemcnt.timer[user]} seconds') #logs the event
						wrn = await message.channel.send(f'You are blocked from sending {blockmsg} for {self.weemcnt.timer[user]} seconds') #sends a message in the same channel and stores in var
						await asyncio.sleep(5) #wait 5 seconds
						await wrn.delete() #deletes the warn message

				except Exception as e:
					print(f'uh oh, something happened {e} - ')




		except Exception as e:
			print(e)
			if '@' in message.content: #checks if the @ sign is in the msg
				await message.delete() #delete
				await self.log(message, 'ping using the freaking tuppers', 'the message was deleted')

		await self.bot.process_commands(message)


	@commands.Cog.listener('on_message')
	async def noevery(self, message):
	    #ctx = await bot.get_context(message) #convinience but its probably not really neccesary
	   

	    if message.mention_everyone or len(message.mentions) >= 1 or len(message.role_mentions) >= 1: #if the message mentions everyone or it mentions a person/role:
	        def check(m):
	                return m == message and m.author.bot == False
	        
	        try:
	            await message.channel.trigger_typing() #starts the typing animation in the channel the message is from
	            msg = await self.bot.wait_for('message_delete', check=check, timeout=20) #watches for a message thats deleted that also has the ping (it times out in 20 seconds)
	            
	            await ctx.send(f'{msg.author.mention} has ghost pinged, smh \n\n Original Message: \n {discord.utils.escape_mentions(msg.content)}') #if the above check passes, send the info
	        except Exception as e:
	            print(e)
	            await asyncio.sleep(1)




# heres the manual utility commands used here

	@tasks.loop(seconds=600) #every 10 minutes
	async def truth(self): #just the truth man
		await self.bot.wait_until_ready() #something something keeps the loop from breaking
		me = self.bot.get_user(661044029110091776) #gets my main acct
		await me.send('you\'re useless dude') #dms the truth


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
			"candycane",
			830999252721074197
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
			await asyncio.sleep(1) #wait for one second but asyncronously

		self.timer[user] = -1 #sets the timer to -1 denoting its inactive
		self.edit(user, post) #edits the original message trigger author's entry to 0
		#return
	#async 	

#some boilerplate code that makes the cog functionable
def setup(bot):
	bot.add_cog(General(bot))
	



