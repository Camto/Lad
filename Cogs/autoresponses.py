import discord
from discord.ext import commands
import utils

import random

import art

# The autoresponse system.
class Autoresponses(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if (
				msg.author.id != self.client.user.id and
				utils.get_setting(msg.guild, "autoresponses") and
				not msg.content.startswith("l.")):
			text = msg.content.lower()
			for pair in utils.get_setting(msg.guild, "autoresponse_file"):
				for keyword in pair["keywords"]:
					if (
						keyword in text and
						abs(random.gauss(0, 1) < 1)):
						response = random.choice(pair["responses"])
						if response != "":
							return await msg.channel.send(response)

def setup(client):
	client.add_cog(Autoresponses(client))