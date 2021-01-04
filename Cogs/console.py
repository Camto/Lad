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
			cmd = ""
			last_line = await aioconsole.ainput()
			while last_line[0] == "#":
				cmd += last_line[1:] + "\n"
				last_line = await aioconsole.ainput()
			cmd += last_line
			
			await run_cmd(self.client, cmd)
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if (
				msg.channel.id == utils.master_settings["console"] and
				msg.author.id in utils.master_settings["admins"]):
			cmd = msg.content
			await run_cmd(self.client, cmd)

async def run_cmd(client, cmd):
	args = cmd.split()
	await client.get_channel(int(args[0])).send(" ".join(args[1:]))

def setup(client):
	client.add_cog(Console(client))