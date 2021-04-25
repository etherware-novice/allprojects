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

file = 'ini.yaml'
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


bot = commands.Bot(command_prefix='am!', intents=intents) #initilizes the bot
bot.obj = [] #initilizes list of games
bot.file = file
bot.token = TOKEN

#flavorie text to make sure its working good
@bot.event
async def on_ready(): #initilization

    #guild = discord.utils.get(bot.guilds, name='bot tester') #gets the guild that i put in to kinda add some flavor text

	disp_guild = ''
	for x in bot.guilds:
		disp_guild += f'{x.name} ({x.member_count} members)\n'
		await x.me.edit(nick = 'the amogus bot')

	try:
		with open(bot.file.name) as file:
			tmp = yaml.safe_load(file)
			for no, x in tmp['game'].items():
				name = x['name']
				code = x['code']
				host = bot.get_user(x['host'])
				actw = {}
				for y in ['active', 'wait']:
					ln = []
					scr = x[y]
					for z in scr:
						ln.append(bot.get_user(z))
					actw[y] = ln

				bot.obj.append(gameobj(name, code, active=actw['active'], wait=actw['wait'], host=host))
			print('')
	except: print('')

	print(
		f'{bot.user} is connected to the following guilds:\n'
	    f'{disp_guild}'
    )

	await bot.change_presence(activity=discord.Game(name='candy\'s bot')) #:)
    



#the react-to-join section
@bot.listen('on_reaction_add')
async def addusr(reaction, user):
	y = {} #initilizes a dict
	for x in range(len(bot.obj)): #for every entry in bot.obj (counting 0 - num)
		y[bot.obj[x]] = bot.obj[x].latestmsg #store the key of the instance as the latest message of it

	if user != bot.user and reaction.emoji == u"\U0001F44D" and reaction.message in y.values(): #if not bot and reaction is thumbs up and the message is correct
		for key, value in y.items(): #for every single entry in the dictionary
			if reaction.message == value: #if the message is the same as the value
				obj = key #stores the correct instance into obj
		ctx = await bot.get_context(reaction.message) #obtains the ctx from the message sent
		await obj.add_user(ctx, user) #adds the user to the obj it belongs to


@bot.listen('on_reaction_remove')
async def reactrem(reaction, user):
	y = {} #initilizes a dict
	for x in range(len(bot.obj)): #for every entry in bot.obj (counting 0 - num)
		y[bot.obj[x]] = bot.obj[x].latestmsg #store the key of the instance as the latest message of it

	if user != bot.user and reaction.emoji == u"\U0001F44D" and reaction.message in y.values(): #if not bot and reaction is thumbs up and the message is correct
		for key, value in y.items(): #for every single entry in the dictionary
			if reaction.message == value: #if the message is the same as the value
				obj = key #stores the correct instance into obj
		ctx = await bot.get_context(reaction.message) #obtains the ctx from the message sent
		await obj.leave(ctx, user, hide=1) #adds the user to the obj it belongs to
		await obj.statusmsg(ctx)



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
	print(ctx.channel)
	bot.obj.append(gameobj(name, code, ctx)) #appends an instance to bot.obj
	file()

''' another testing thing bc im lonely'''
@bot.command(name='fill')
async def fill(ctx):
	for x in {"user1#9833", "user2#2383", "user3#9742", "user4#8269", "user5#1048", "user6#7862", "user7#3452", "user8#3821", "user9#3490"}:
		await bot.obj[0].add_user(ctx, x)



#listing command (both overall and individual)
@bot.command(name='list')
async def list(ctx, game = -1):

	try:
		msg = 'Game listing: \n\n' #nice little flavoring text

		if game == -1 and len(bot.obj) > 1: #if the game var was not provided and there is more than one instance
			for x in range(len(bot.obj)): #for the number of entries in bot.obj
				game = bot.obj[x] #stores the instance of the thing
				msg += f'<game {x}>, <name \'{game.name}\'>, <players {len(game.active)}/{len(game.wait)}>, <code \'{game.code}\'>\n' #flavor text and informacione
			await ctx.send(msg) #sends the message
		elif game == -1: #if there is only one instance and the game wasnt provided
			await bot.obj[0].statusmsg(ctx, 1) #just gets 0
			file()
		else:
			try:
				await bot.obj[game].statusmsg(ctx, 1) #gets the game input
			except:
				await ctx.send('Please send a valid game number') #if the game input was invalid
	except:
		await ctx.send("Please initilize a game")

#change code funct
@bot.command(name='code')
async def chncode(ctx, game = -1, code:str = "error"):
	if game == -1 and len(bot.obj) > 1: ctx.send('Please specify a game') #if the game is left as default and there is more than one instance warn
	else:
		if game == -1: game = 0 #moves the default game int up one
		sudo = await chkrl(ctx, ctx.author)
		if ctx.author == bot.obj[game].host: sudo = 1
		print(sudo)
		if sudo == 1:
			print('perms')
			bot.obj[game].code = code #sets the corresponding game's code
			await ctx.send(f'Game {game}\'s code was changed to {code}')

		else: await ctx.send('Sorry bud, you don\'t have the perms to do that')

@bot.command(name='chname')
async def chncode(ctx, game = -1, code:str = "null"):
	if game == -1 and len(bot.obj) > 1: ctx.send('Please specify a game') #if the game is left as default and there is more than one instance warn
	else:
		if game == -1: game = 0 #moves the default game int up one
		sudo = await chkrl(ctx, ctx.author)
		if ctx.author == bot.obj[game].host: sudo = 1
		if sudo == 1:
			bot.obj[game].name = code #sets the corresponding game's code
		else: await ctx.send('Sorry bud, you don\'t have the perms to do that')


@bot.command(name='ping')
async def ping(ctx, game = -1):
	msg = ''
	if game == -1 and len(bot.obj) > 1: ctx.send('Please specify a game')
	sudo = await chkrl(ctx, ctx.author)
	if ctx.author == bot.obj[game].host: sudo = 1
	if sudo == 1:
		png = []
		for x in bot.obj[game].active:
			png.append(x.mention)
		await ctx.send(", ".join(png))







#leave queue funct
@bot.command(name='leave')
async def leave(ctx, game = 0, member:discord.Member = None):
		if member != None:
			sudo = await chkrl(ctx, ctx.author)
			if ctx.author == bot.obj[game].host: sudo = 1
			if sudo == 1:
				try:
					await bot.obj[game].leave(ctx, member)
					await bot.obj[game].statusmsg(ctx)
				except Exception as e:
					print(e)
					await ctx.send('Whoops, that user isn\'t in that game')
			else:
				await ctx.send('Sorry bud, you don\'t have the perms to do that')
		elif game == -1: #very special case
			for x in bot.obj: #for every entry in bot.obj
				await x.leave(ctx, ctx.author) #runs leave in the instance
				await x.statusmsg(ctx, ctx.author) #updates the message
		else:
			await bot.obj[game].leave(ctx, ctx.author) #runs leave in the inst
			await bot.obj[game].statusmsg(ctx) #updates message

@bot.command(name='close')
async def close(ctx, game = -1):
	if game == -1:
		ctx.send('No game specified.')
	else:
		sudo = await chkrl(ctx, ctx.author)
		if ctx.author == bot.obj[game].host: sudo = 1
		if sudo == 1:
			try:
				bot.obj.pop(game)
				await ctx.send('Game successfully closed')
				file()
			except:
				await ctx.send('There was an error closing the game. Please check you are reffering to a valid game')
		else:
			await ctx.send('Sorry bud, you don\'t have the perms to do that')


class gameobj(object): #heres where like half the magic happens
	"""docstring for gameobj"""
	def __init__(self, name:str, code:str, ctx = None, *, active = None, wait = None, host = None):
		super(gameobj, self).__init__()
		self.code = code #fils in all the default values
		self.active = []
		self.wait = []

		if active != None: self.active = active
		if wait != None: self.wait = wait
		if host != None: self.host = host
		self.name = name
		if host != None: self.host = host
		else: self.host = ctx.author
		self.latestmsg = 0
		if ctx != None: asyncio.ensure_future(self.statusmsg(ctx)) #triggers the status message

	#adds user
	async def add_user(self, ctx, user): 
		if user not in self.active and len(self.active) <= 9: #if the user isnt already in the list of active players and there is an empty spot
			self.active.append(user) #appends the user to the list
			await self.statusmsg(ctx) #updates info msg
			file()
		else: #no room in self.active or they're already in
			if user in self.active: msg = await ctx.send("You're already in the game") #if they're already in
			elif len(self.active) >= 9:  #if theres no room left
				msg = await ctx.send('There is no room left, adding you to the waiting list..') #msg letting you know
				self.wait.append(user) #adds the user to the waiting list
				await self.statusmsg(ctx) #updates the info msg
				file()
			await asyncio.sleep(3) #wait 3 seconds
			await msg.delete() #delete the status message


	#updates/creates new status message
	async def statusmsg(self, ctx, new:int = 0):
		try:
			msg = f'Host: {self.host} \nCode: {self.code} \nGame name: {self.name} \n\n' #header flavor text

			for x in range(10): #loops through below code 10 times
				try:
					try:
						if self.active[x].nick != None: nick = f'({self.active[x].nick}) '
						else: nick = ''
						msg += f'{x + 1}: {str(self.active[x])} {nick}\n' #if theres a user in the specific spot, print it
					except:
						msg += f'{x + 1}: {str(self.active[x])} \n' #filler characters dont get empties
				except:
					msg += '[Empty] \n' #if the above fails due to index out of range, print empty

			if len(self.wait) > 0: #if theres ppl in the waiting list
				msg += '\n Waiting List \n' #seperator
				for x in range(len(self.wait)): #for the number of entries in the waiting list
					try:
						if self.wait[x].nick != None: nick = f'({self.wait[x].nick}) '
						else: nick = ''
					except: nick = ''
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
				print(ctx.channel)
				self.latestmsg = await ctx.send(msg) #creates new message


			await self.latestmsg.add_reaction(u"\U0001F44D") #adds the thumbs up reaction

		except Exception as e:
			await ctx.send('There are no games running currently, run init to start one!') #hopefully this only triggers if there isnt an init for this instance
			await ctx.send(e)
	

	#leave funct
	async def leave(self, ctx, member = None, *, hide=0):
		if member == None: member = ctx.author
		if member in self.active: #if the person leaving is in the active list
			self.active.remove(member) #removes from active list
			if len(self.wait) > 0: #if there are people waiting
				new = self.wait[0] #sets the first person in the waiting list to "new"
				self.wait.remove(new) #removes them from wait
				self.active.append(new) #adds to active
				if hide == 0: await ctx.send(f'{new.mention}, {member.mention} has given you a spot!') #flavor text
				file()
			else: #if there is nobody waiting
				if hide == 0: await ctx.send(f'{member.mention} has left the game') #simple 'has left' message
				file()
		elif member in self.wait: #if the person is in the waiting list
			self.wait.remove(member) #removes from waiting list
			if hide == 0: await ctx.send(f'{member} has left the queue') #message of confirmation
			file()
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

def file():
	with io.open(bot.file.name, 'w', encoding='utf8') as outfile:
		#outfile = yaml.full_load(file)
		
		data = {"token": bot.token, 'game': {}}
		for x in range(len(bot.obj)):
			dataobj = bot.obj[x]
			loc = data['game'][x] = {}
			
			for y in ['name', 'code']:
				loc[str(y)] = getattr(dataobj, y)

			for y in ['active', 'wait']:
				ln = []
				for z in getattr(dataobj, y):
					ln.append(z.id)
				loc[y] = ln

			loc['host'] = dataobj.host.id


		print(data)
		yaml.dump(data, outfile)



bot.load_extension('jishaku')
bot.run(TOKEN) #runs everything else