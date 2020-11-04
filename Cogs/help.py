import discord
from discord.ext import commands
import utils

import math

from fuzzywuzzy import fuzz, process

help = utils.get_yaml("help")

chunks = lambda l, n: [l[i * n:(i + 1) * n] for i in range((len(l) + n - 1) // n)]

# Show command descriptions.
class Help(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def help(self, ctx, *cmd):
		if len(cmd) == 0:
			
			async def help_menu(_):
				yield math.ceil(len(help) / 5)
				for chunk in chunks(help, 5):
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
			await ctx.send(embed = utils.embeds[f"{help_category} help"])

def setup(client):
	client.add_cog(Help(client))