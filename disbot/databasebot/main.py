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
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from dhooks import Webhook as dhook
import discordrp as cmd

bot = cmd.start('!')
bot.obj = {}

@bot.listen("on_ready")
async def init():

    await bot.change_presence(activity=discord.Game(name='> bootup successfull, waiting for commands...')) #:)

@bot.command(name='tst')
async def tst(ctx):
    #await cmd.wh(bot, ctx.channel.id, cn)
    test = dataobj(bot, ctx, "s", "ab")
    test.debug()
    #await ctx.send('word', embed=test.displ())

class dataobj(object):
    def __init__(self, bot, ctx, name:str, loc, **other):
        super(dataobj, self).__init__()
        self.name = name
        '''self.desc = ""
        self.loc = loc
        self.pwr = []
        self.other = other'''
        self.author = ctx.author
        self.bot = bot

        setu = asyncio.ensure_future(self.setup(ctx))
        while True:
            print(setu.result())
        #if setu.result() == -1: print(-1)



    async def setup(self, ctx):

        await ctx.send('Initilizing setupentr.exe', delete_after=2)
        await asyncio.sleep(2)
        await ctx.send('Running calibration tests', delete_after=0.5)
        await asyncio.sleep(0.5)
        await ctx.send('Initilizing user I/O', delete_after = 0.2)
        await asyncio.sleep(0.2)
        await ctx.send('Running final checks..', delete_after = 0.3)
        await asyncio.sleep(0.2)
        await ctx.send('Welcome \{USER.name.short} to the Super-Cal Database system. I will walk you through setting up a new entry.')
        try:
            a = await self.setupq(ctx, "First off, what do you want the description of your file to say?")
            b = await self.setupq(ctx, "Second, what location do you want to display on your file?")
        except Exception as e:
            #print(f"{type(e)}: {e}")
            #print(repr(e))
            #print(e.args[0])
            
            if e.args[0] == "User exited": await ctx.send('Understood, cancelling the entry..')
            else: await ctx.send(f"A critical error has occured in the program: ```{e}``` Please contact me (candycaneannihalator) about the error and I will try to fix it as best i can")
            return -1
        await ctx.send("Okay, everything is now set up. > Aborting setupentr.exe")
        await ctx.send(f"{a}\n{b}")

    async def setupq(self, ctx, question:str):
        await ctx.send(question)

        resp = ['Alright, adding to database..', 'Interesting.....', 'Oooh, I like that!', 'lol ok', 'entry.data updated, running next question..', "Got it, thanks", "Log attempt successful"]
        def check(m):
            return m.author == self.author and not m.author.bot

        msg = await self.bot.wait_for('message', check=check)
        if msg.content == "exit":
             raise Exception('User exited')
             print('usr exit')
        await ctx.send(random.choice(resp))
        return msg.content




    def displ(self):
        embed = discord.Embed(title=self.name, colour=discord.Colour(0x4ec228), url="https://discordapp.com", description="** **")        
        embed.set_author(name=self.author, url="https://discordapp.com", icon_url=self.author.avatar_url)
        
        embed.add_field(name="descr", value=f"```{self.desc}```")
        embed.add_field(name="loc", value=f"```{self.loc}```")

        e = ""
        for x in self.pwr:
            e += f"```{x}```"

        embed.add_field(name="pwr", value=e)
        
        for x, y in self.other.items():
            embed.add_field(name=x, value=f"```{y}```", inline=True)

        a = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
        e = ""
        y = 0
        for x in self.other.values():
            if y >= len(a):
                e += "..."
            e += f"{a[y]} {x}\n"
            y += 1

        embed.add_field(name="refrences", value=e)
        
        return embed
    
    def debug(self):
        self.desc = "placeholder desc for testing"
        self.loc = "somewheree"
        self.pwr = ['lorem ipsum dolor auodsnosadjaosndsauobcx;', 'eswnfueswjfijoeafdisadi873r934re9u1eeun19n']
        self.other = {"key1": "val1", "key2": "val2"}
bot.run(bot.token)