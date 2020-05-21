import discord
from discord.ext import commands

import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import utils

quotes = utils.get_json("bible quotes")

# Starting the bible study.
class Bible(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def bible(self, ctx, *args):
		if utils.get_setting(ctx.guild.id, "bible"):
			if len(args) == 0:
				quote = random.choice(quotes)
			else:
				quote = process.extractOne(
					args[0],
					quotes,
					scorer = fuzz.partial_token_sort_ratio)[0]

			await ctx.send(embed = discord.Embed(
				description = quote["text"],
				color = utils.embed_color)
				.set_author(
					name = quote["location"],
					icon_url = utils.icons["bible"]))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Bible(client))