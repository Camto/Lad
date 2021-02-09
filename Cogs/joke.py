import discord
from discord.ext import commands
import utils

import asyncio

class Joke(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def knockknock(self, ctx):
		channel = ctx.channel
		user = ctx.author
		
		await slow_send(channel, "Who's there?", 0.5)
		msg = await utils.wait_for_response(self.client, channel, user, 60)
		if msg is None:
			return await ctx.send("no person")
		
		await slow_send(channel, f"{msg.content} who?", 0.5)
		msg = await utils.wait_for_response(self.client, channel, user, 60)
		if msg is None:
			return await ctx.send("no punchline")
		
		await slow_send(channel, ":joy:", 0.5)

async def slow_send(channel, content, wait_time):
	async with channel.typing():
		await asyncio.sleep(wait_time)
		await channel.send(content)

def setup(client):
	client.add_cog(Joke(client))