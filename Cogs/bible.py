import discord
from discord.ext import commands

import random
import asyncio
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import utils

quotes = utils.get_yaml("bible quotes")

reload_emoji = utils.emojis["reload"]

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

			if len(args) != 0:
				await ctx.send(embed = bible_to_embed(quote))
			else:
				reload_amount = 1

				msg = await ctx.send(embed = 
					bible_to_embed(quote)
					.set_footer(text = f"#{reload_amount}"))

				await msg.add_reaction(reload_emoji)

				while True:
					try:
						reaction, user = await self.client.wait_for(
							"reaction_add",
							timeout = 60,
							check = lambda reaction, user:
								reaction.message.id == msg.id and
								user == ctx.author and
								str(reaction.emoji) == reload_emoji)
					except asyncio.TimeoutError:
						break
					else:
						reload_amount += 1
						await msg.remove_reaction(reload_emoji, user)
						await msg.edit(embed = 
							bible_to_embed(random.choice(quotes))
							.set_footer(text = f"#{reload_amount}"))
		else:
			await ctx.send(embed = utils.command_disabled)

def bible_to_embed(quote):
	return (discord.Embed(
		description = quote["text"],
		color = utils.embed_color)
		.set_author(
			name = quote["location"],
			icon_url = utils.icons["bible"]))

def setup(client):
	client.add_cog(Bible(client))