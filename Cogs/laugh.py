import discord
from discord.ext import commands
import utils
import random

responses = ["lol", "LMFAOOO", "jajaja", "xd", "XD", "lmfao", "LOL", "im dyingg", ":joy::joy::joy:", ":neutral_face:"]

class Laugh(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def laugh(self, ctx):
		if utils.get_setting(ctx.guild.id, "laugh"):
			await ctx.send(random.choice(responses))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Laugh(client))