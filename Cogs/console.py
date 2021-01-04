import discord
from discord.ext import commands
import utils

import aioconsole

# The master console!
class Console(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		while True:
			cmd = await aioconsole.ainput()
			args = cmd.split()
			await self.client.get_channel(int(args[0])).send(" ".join(args[1:]))

def setup(client):
	client.add_cog(Console(client))