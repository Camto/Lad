import discord
from discord.ext import commands
import utils

# The master console!
class Console(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if (
				msg.channel.id == utils.master_settings["console"] and
				msg.author.id in utils.master_settings["admins"]):
			cmd = msg.content
			await run_cmd(self, msg, cmd)

async def run_cmd(self, msg, cmd):
	print(cmd)
	args = cmd.split()
	await self.client.get_channel(int(args[0])).send(args[1])

def setup(client):
	client.add_cog(Console(client))