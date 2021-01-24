import discord
from discord.ext import commands
import utils

# Set the bot's presence on startup.
class Feedback(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		self.channel = self.client.get_channel(int(utils.master_settings["feedback"]))
	
	@commands.command()
	async def feedback(self, ctx, *, arg):
		await self.channel.send(arg)
		await ctx.send("Feedback recieved!")

def setup(client):
	client.add_cog(Feedback(client))