import discord
from discord.ext import commands
import utils

import math

from fuzzywuzzy import fuzz, process

help = utils.get_json("help")
for i in range(len(help)): help[i]["embed"] = discord.Embed.from_dict(help[i]["embed"])

# Show command descriptions.
class Help(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def help(self, ctx, *cmd):
		if len(cmd) == 0:
			
			async def help_menu(_):
				yield math.ceil(len(help) / 5)
				for chunk in utils.chunks(help, 5):
					help_embed = (discord.Embed(
						title = "Commands",
						description = "This bot's prefix is ``l.``",
						color = utils.embed_color)
						.set_footer(
							text = f"https://github.com/Camto/Lad - In {len(self.client.guilds)} servers!",
							icon_url = utils.icons["github"]))
					for cmd_help in chunk:
						help_embed.add_field(
							name = cmd_help["cmd"],
							value = cmd_help["msg"],
							inline = False)
					yield help_embed
			
			await utils.menus.list(self.client, ctx, help_menu)
		else:
			help_category = process.extractOne(cmd[0], list(map(lambda cmd: cmd["cmd"], help)))[0]
			await ctx.send(embed = list(filter(lambda cmd_help: cmd_help["cmd"] == help_category, help))[0]["embed"])

def setup(client):
	client.add_cog(Help(client))