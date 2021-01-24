import discord
from discord.ext import commands

import random

# Set the bot's presence on startup.
class Presence(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		await self.client.change_presence(
			status = discord.Streaming,
			activity = discord.Streaming(
				name = "l.help",
				url = f"https://www.twitch.tv/{random.choice(['jpvinnie', 'otomac'])}"))

def setup(client):
	client.add_cog(Presence(client))