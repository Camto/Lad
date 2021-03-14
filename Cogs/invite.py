import discord
from discord.ext import commands
import utils

# Send invite link.
class Invite(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def invite(self, ctx):
		await ctx.send("https://discord.com/oauth2/authorize?client_id=709644595104972890&permissions=8&scope=bot")

def setup(client):
	client.add_cog(Invite(client))