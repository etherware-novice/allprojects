#def timeup(format):
#	return datetime.now.strftime(format)

def commands(client):
	import os
	import discord
	import random
	from datetime import datetime
	from dotenv import load_dotenv
#	intents = discord.Intents.default()
#	intents.members = True

	load_dotenv()
	TOKEN = os.getenv('DISCORD_TOKEN')
	GUILD = os.getenv('DISCORD_GUILD')

#	client = discord.Client(intents=intents)

	@client.event
	async def on_member_join(member):
		await member.create_dm()
		await member.dm_channel.send(
				f'Hi {member.name}, welcome to my test server!'
			)

	@client.event
	async def on_message(message):
		#now = timeup("%H:%M")
		if message.author == client.user:
			return

		if message.content == 'rng!':
			response = random.randint(0, 500)
			await message.channel.send(response)
			print(f'[now]: User [{message.author}] used [rng] command in  #{message.channel}')
