import discord
from discord.ext import commands
import utils

class Useless(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def useless(self, ctx):
		if utils.get_setting(ctx.guild, "useless"):
			await ctx.send(embed = utils.embeds["useless"])
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Useless(client))