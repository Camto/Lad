import discord
from discord.ext import commands
import utils

import random

# Secret command, never document anywhere.
class Embed(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def embed(self, ctx):
		await ctx.send(embed = random.choice(list(utils.embeds.values())))

def setup(client):
	client.add_cog(Embed(client))