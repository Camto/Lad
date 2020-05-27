import discord
from discord.ext import commands

import random
import art
import utils

autoresponses = utils.get_json("autoresponses")

# The autoresponse system and relegating commands.
class On_Message(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author.id != utils.lad_id:
			if utils.get_setting(msg.guild.id, "autoresponses"):
				text = msg.content.lower()
				for pair in autoresponses:
					for keyword in pair["keywords"]:
						if keyword in text:
							return await msg.channel.send(random.choice(pair["responses"]))

def setup(client):
	client.add_cog(On_Message(client))