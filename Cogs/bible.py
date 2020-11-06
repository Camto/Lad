import discord
from discord.ext import commands
import utils

import random

from fuzzywuzzy import fuzz, process

bible = utils.get_yaml("bible")

# Starting the bible study.
class Bible(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def bible(self, ctx, *args):
		if utils.get_setting(ctx.guild.id, "bible"):
			if len(args) > 0:
				pass#quote = process.extractOne(
				#	args[0],
				#	quotes,
				#	scorer = fuzz.partial_token_sort_ratio)[0]
				#await ctx.send(embed = bible_to_embed(quote))
			else:
				await utils.menus.reload(self.client, ctx, bible_menu)
		else:
			await ctx.send(embed = utils.command_disabled)

async def bible_menu(_):
	while True:
		book = random.choice(bible)
		chapters = book['chapters']
		chapter = random.randrange(len(chapters))
		verse = random.randrange(len(chapters[chapter]))
		yield bible_to_embed(chapters[chapter][verse], f"{book['name']} {chapter+1}:{verse+1}")

def bible_to_embed(quote, loc):
	return (discord.Embed(
		description = quote,
		color = utils.embed_color)
		.set_author(
			name = loc,
			icon_url = utils.icons["bible"]))

def setup(client):
	client.add_cog(Bible(client))