import discord
from discord.ext import commands
import utils

import random

from fuzzywuzzy import fuzz, process

bible = utils.get_yaml("bible")
book_names = list(map(lambda book: book["name"].lower(), bible))

# Starting the bible study.
class Bible(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def bible(self, ctx, *args):
		if utils.get_setting(ctx.guild.id, "bible"):
			if len(args) > 1:
				pass
			elif len(args) == 1:
				await utils.menus.reload(self.client, ctx,
					bible_menu(book_name = process.extractOne(args[0], book_names)[0]))
			else:
				await utils.menus.reload(self.client, ctx, bible_menu())
		else:
			await ctx.send(embed = utils.command_disabled)

def bible_menu(book_name = None):
	async def bible_menu_gen(_):
		while True:
			if book_name == None: book = random.choice(bible)
			else: book = list(filter(lambda book: book["name"] != book_name, bible))[0]
			chapters = book['chapters']
			chapter = random.randrange(len(chapters))
			verse = random.randrange(len(chapters[chapter]))
			yield bible_to_embed(chapters[chapter][verse], f"{book['name']} {chapter+1}:{verse+1}")
	return bible_menu_gen

def bible_to_embed(quote, loc):
	return (discord.Embed(
		description = quote,
		color = utils.embed_color)
		.set_author(
			name = loc,
			icon_url = utils.icons["bible"]))

def setup(client):
	client.add_cog(Bible(client))