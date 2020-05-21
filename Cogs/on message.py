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
			content = msg.content
			
			if content.startswith("l."):
				# The say command is actually here.
				if content.startswith("l.say"):
					if utils.get_setting(msg.guild.id, "say"):
						await msg.channel.send(content[5:].lstrip())
						return await msg.delete()
					else:
						await msg.channel.send(embed = utils.command_disabled)
				elif content.startswith("l.ascii"):
					#if utils.get_setting(msg.guild.id, "ascii"):
						ascii_txt = art.text2art(content[7:].lstrip())
						await msg.channel.send(f"```\n{ascii_txt}\n```")
					#else: 
					#	await msg.channel.send(embed = utils.command_disabled)
			
			if utils.get_setting(msg.guild.id, "autoresponses"):
				text = content.lower()
				for pair in autoresponses:
					for keyword in pair["keywords"]:
						if keyword in text:
							return await msg.channel.send(random.choice(pair["responses"]))

def setup(client):
	client.add_cog(On_Message(client))