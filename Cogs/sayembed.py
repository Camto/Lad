import discord
from discord.ext import commands
import utils

import json

utils.master_settings["admins"] = list(map(int, utils.master_settings["admins"]))

class Sayembed(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def sayembed(self, ctx, *, arg):
		if ctx.message.author.id in utils.master_settings["admins"]:
			await ctx.send(embed = discord.Embed.from_dict(json.loads(arg)))

def setup(client):
	client.add_cog(Sayembed(client))