
import os
import discord
import random
from discord.ext import commands
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import traceback
from discord.ext import tasks
import json

class jsonfile(object):
	"""docstring for jsonfile"""

	def __init__(self, file:str = "0"): #file is an actual argument
		super(jsonfile, self).__init__() #idk what this does but i feel like it might break if i remove
		self.file = file #makes the argument file a class var

		if file == "0": #alternate option to make it not write to file and reset on shutdown
			self.data = {} #sets the data class var up

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

	def append(self, inp):
		self.data[len(self.data)] = inp
		self.update()

intents = discord.Intents.default() #sets up the intents obj
intents.members = True #flips the member inperwhatever it is to true

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #retrieves the stuff needed from a *hidden* env file yall aint gettin

bot = commands.Bot(command_prefix='am!', intents=intents) #initilizes the bot
#bot.obj = [] #initilizes list of games
bot.obj = jsonfile('games.json')


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
    


#the react-to-join section
@bot.event
async def on_reaction_add(reaction, user):
	y = {} #initilizes a dict
	for x in range(len(bot.obj.data)): #for every entry in bot.obj (counting 0 - num)
		y[bot.obj.data[x]] = bot.obj.data[x].latestmsg #store the key of the instance as the latest message of it

	if user != bot.user and reaction.emoji == u"\U0001F44D" and reaction.message in y.values(): #if not bot and reaction is thumbs up and the message is correct
		for key, value in y.items(): #for every single entry in the dictionary
			if reaction.message == value: #if the message is the same as the value
				obj = key #stores the correct instance into obj
		ctx = await bot.get_context(reaction.message) #obtains the ctx from the message sent
		await obj.add_user(ctx, user) #adds the user to the obj it belongs to


''' testing stuff
@bot.command(name='test')
async def react(ctx):
	bot.reactmsg = ctx.message
	bot.ogmsg = await ctx.send('reaction msg')
	await bot.ogmsg.add_reaction(u"\U0001F44D") #thumbs up


@bot.command(name='add')
async def add(ctx, game=0):
	game = bot.obj[game]
	await game.add_user(ctx, ctx.author)
'''

#initilizes a new instance of the game class
@bot.command(name='init') 
async def init(ctx, name, code):
	bot.obj.append(gameobj(ctx, name, code)) #appends an instance to bot.obj

''' another testing thing bc im lonely
@bot.command(name='fill')
async def fill(ctx):
	for x in {"user1#9833", "user2#2383", "user3#9742", "user4#8269", "user5#1048", "user6#7862", "user7#3452", "user8#3821", "user9#3490"}:
		await bot.obj[0].add_user(ctx, x)
'''


#listing command (both overall and individual)
@bot.command(name='list')
async def list(ctx, game = -1):

	try:
		msg = 'Game listing: \n\n' #nice little flavoring text

		if game == -1 and len(bot.obj.data) > 1: #if the game var was not provided and there is more than one instance
			for x in range(len(bot.obj.data)): #for the number of entries in bot.obj
				game = bot.obj.data[x] #stores the instance of the thing
				msg += f'<game {x}>, <name \'{game.name}\'>, <players {len(game.active)}/{len(game.wait)}>, <code \'{game.code}\'>\n' #flavor text and informacione
			await ctx.send(msg) #sends the message
		elif game == -1: #if there is only one instance and the game wasnt provided
			await bot.obj.data[0].statusmsg(ctx, 1) #just gets 0
		else:
			try:
				await bot.obj.data[game].statusmsg(ctx, 1) #gets the game input
			except:
				await ctx.send('Please send a valid game number') #if the game input was invalid
	except:
		ctx.send("Please initilize a game")

#change code funct
@bot.command(name='code')
async def chncode(ctx, game = -1, code:str = "error"):
	if game == -1 and len(bot.obj.data) > 1: ctx.send('Please specify a game') #if the game is left as default and there is more than one instance warn
	else:
		if game == -1: game = 0 #moves the default game int up one
		sudo = await chkrl(ctx, ctx.author)
		if ctx.author == bot.obj.data[game].host: sudo = 1
		if sudo == 1:
			bot.obj.data[game].code = code #sets the corresponding game's code
			bot.obj.update()
		else: await ctx.send('Sorry bud, you don\'t have the perms to do that')



#leave queue funct
@bot.command(name='leave')
async def leave(ctx, game = 0, member:discord.Member = None):
		if member == None: member = ctx.author
		if member != None:
			sudo = await chkrl(ctx, ctx.author)
			if ctx.author == bot.obj.data[game].host: sudo = 1
			if sudo == 1:
				try:
					await bot.obj.data[game].leave(ctx, member)
					await bot.obj.data[game].statusmsg(ctx)
				except Exception as e:
					print(e)
					await ctx.send('Whoops, that user isn\'t in that game')
			else:
				await ctx.send('Sorry bud, you don\'t have the perms to do that')
		elif game == -1: #very special case
			for x in bot.obj.data: #for every entry in bot.obj
				await x.leave(ctx, member) #runs leave in the instance
				await x.statusmsg(ctx, member) #updates the message
		else:
			await bot.obj.data[game].leave(ctx, member) #runs leave in the inst
			await bot.obj.data[game].statusmsg(ctx, member) #updates message

@bot.command(name='close')
async def close(ctx, game = -1):
	if game == -1:
		ctx.send('No game specified.')
	else:
		sudo = await chkrl(ctx, ctx.author)
		if ctx.author == bot.obj.data[game].host: sudo = 1
		if sudo == 1:
			try:
				bot.obj.data.pop(game)
				await ctx.send('Game successfully closed')
			except:
				await ctx.send('There was an error closing the game. Please check you are reffering to a valid game')
		else:
			await ctx.send('Sorry bud, you don\'t have the perms to do that')


class gameobj(object): #heres where like half the magic happens
	"""docstring for gameobj"""
	def __init__(self, ctx, name:str, code:str):
		super(gameobj, self).__init__()
		self.code = code #fils in all the default values
		self.active = []
		self.wait = []
		self.name = name
		self.host = ctx.author
		self.latestmsg = 0
		asyncio.ensure_future(self.statusmsg(ctx)) #triggers the status message

	#adds user
	async def add_user(self, ctx, user): 
		if user not in self.active and len(self.active) <= 9: #if the user isnt already in the list of active players and there is an empty spot
			self.active.append(user) #appends the user to the list
			await self.statusmsg(ctx) #updates info msg
		else: #no room in self.active or they're already in
			if user in self.active: msg = await ctx.send("You're already in the game") #if they're already in
			elif len(self.active) >= 9:  #if theres no room left
				msg = await ctx.send('There is no room left, adding you to the waiting list..') #msg letting you know
				self.wait.append(user) #adds the user to the waiting list
				await self.statusmsg(ctx) #updates the info msg
			await asyncio.sleep(3) #wait 3 seconds
			await msg.delete() #delete the status message


	#updates/creates new status message
	async def statusmsg(self, ctx, new:int = 0):
		try:
			msg = f'Host: {self.host} \nCode: {self.code} \nGame name: {self.name} \n\n' #header flavor text

			for x in range(10): #loops through below code 10 times
				try:
					if self.active[x].nick != None: nick = f'({self.active[x].nick}) '
					else: nick = ''
					msg += f'{x + 1}: {str(self.active[x])} {nick}\n' #if theres a user in the specific spot, print it
				except:
					msg += '[Empty] \n' #if the above fails due to index out of range, print empty

			if len(self.wait) > 0: #if theres ppl in the waiting list
				msg += '\n Waiting List \n' #seperator
				for x in range(len(self.wait)): #for the number of entries in the waiting list
					if self.active[x].nick != None: nick = f'({self.active[x].nick}) '
					else: nick = ''
					msg +=  f'{x + 1}: {str(self.wait[x])} {nick}\n' #adds the user to msg
					if x == 10: #10 entry limit
						msg += "...\n" #...

						break #breaks the for loop
				msg += "\n\n"


			msg += 'React with :thumbsup: to join!' #flavor texto

			#await bot.wait_until_ready() #something something keeps the loop from breaking
			
			try:
				if self.latestmsg and new == 0: await self.latestmsg.edit(content=msg) #if latestmsg exists and the flag isnt set, edit content
				else: raise Exception('expected manual exception, im too lazy to rewrite this code') #i just have this here so if new isnt 0 it cancels the try
			except Exception as e:
				print(e)
				self.latestmsg = await ctx.send(msg) #creates new message


			await self.latestmsg.add_reaction(u"\U0001F44D") #adds the thumbs up reaction

		except Exception as e:
			await ctx.send('There are no games running currently, run init to start one!') #hopefully this only triggers if there isnt an init for this instance
			await ctx.send(e)
	

	#leave funct
	async def leave(self, ctx, member = None):
		if member == None: member = ctx.author
		if member in self.active: #if the person leaving is in the active list
			self.active.remove(member) #removes from active list
			if len(self.wait) > 0: #if there are people waiting
				new = self.wait[0] #sets the first person in the waiting list to "new"
				self.wait.remove(new) #removes them from wait
				self.active.append(new) #adds to active
				await ctx.send(f'{new.mention}, {member.mention} has given you a spot!') #flavor text
			else: #if there is nobody waiting
				await ctx.send(f'{member.mention} has left the game') #simple 'has left' message
		elif member in self.wait: #if the person is in the waiting list
			self.wait.remove(member) #removes from waiting list
			await ctx.send(f'{member} has left the queue') #message of confirmation
		else:
			x = x 
			await ctx.send(f'You need to be in a queue to leave, {member}') #if the triggerer is not in any list, then just send back this
	

async def chkrl(ctx, user: discord.Member):
		modrl = [ #list of roles that are "elevated"
			742937828425465899
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