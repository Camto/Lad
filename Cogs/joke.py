import discord
from discord.ext import commands
import utils

import asyncio
import random

responses = ["lol", "LMFAOOO", "jajaja", "xd", "XD", "lmfao", "LOL", "im dyingg", ":joy::joy::joy:", ":neutral_face:"]

class Joke(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def knockknock(self, ctx):
		if utils.get_setting(ctx.guild.id, "knockknock"):
			channel = ctx.channel
			user = ctx.author
			
			await slow_send(channel, "Who's there?", 0.5)
			msg = await utils.wait_for_response(self.client, channel, user, 60)
			if msg is None:
				return await ctx.send(random.choice(["Must've been the wind", "Guess there's nobody", "Eh, I'll just go back to bed"]))
			
			await slow_send(channel, f"{msg.content} who?", 0.5)
			msg = await utils.wait_for_response(self.client, channel, user, 60)
			if msg is None:
				return await ctx.send(random.choice(["Was there really no punchline?", "Huh, where'd you go?", "Oh well, I was hoping for a punchline."]))
			
			await slow_send(channel, ":joy:", 0.5)
		else:
			await ctx.send(embed = utils.command_disabled)
	
	@commands.command()
	async def laugh(self, ctx):
		if utils.get_setting(ctx.guild.id, "laugh"):
			await ctx.send(random.choice(responses))
		else:
			await ctx.send(embed = utils.command_disabled)
	
	@commands.command()
	async def luagh(self, ctx):
		await ctx.send(embed = discord.Embed(title = "Fuck you", color = utils.embed_color))

async def slow_send(channel, content, wait_time):
	async with channel.typing():
		await asyncio.sleep(wait_time)
		await channel.send(content)

def setup(client):
	client.add_cog(Joke(client))