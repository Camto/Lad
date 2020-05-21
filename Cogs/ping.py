import discord
from discord.ext import commands

import utils

# Ping command to check users ping.
class Ping(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def ping(self, ctx):
		if utils.get_setting(ctx.guild.id, "ping"):
			await ctx.send(embed = discord.Embed(
				title = "Pong!",
				description = f"Hey, {ctx.message.author.mention}. Current ping is: ``{round(self.client.latency * 1000)}`` ms.",
				color = utils.embed_color))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Ping(client))