import discord
from discord.ext import commands
import utils

class Avatar(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def avatar(self, ctx):
		await ctx.send(ctx.message.author.avatar_url)

def setup(client):
	client.add_cog(Avatar(client))