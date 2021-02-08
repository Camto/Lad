import discord
from discord.ext import commands
import utils

import random
import asyncio

responses = list(map(
	discord.Embed.from_dict,
	utils.get_json("8ball")
))

class Cmd_8ball(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(name = "8ball")
	async def cmd_8ball(self, ctx, *_):
		if utils.get_setting(ctx.guild.id, "cmd_8ball"):
			async with ctx.typing():
				await ctx.send(":8ball: **Divining your fate...**")
				await asyncio.sleep(2)
				await ctx.send(embed = random.choice(responses))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Cmd_8ball(client))