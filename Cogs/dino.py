import discord
from discord.ext import commands

import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import utils

dinos = utils.get_json("dinos")
dino_names = list(dinos.keys())

reload_emoji = utils.emojis["reload"]

# Process dino related requests.
class Dino(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def dino(self, ctx, *args):
		if utils.get_setting(ctx.guild.id, "dino"):
			if len(args) == 0:
				dino = random.choice(dino_names)
			else:
				dino = process.extractOne(args[0], dino_names)[0]
			
			if len(args) != 0:
				await ctx.send(embed = dino_to_embed(dino))
			else:
				reload_amount = 1
				
				msg = await ctx.send(embed =
					dino_to_embed(dino)
					.set_footer(text = f"#{reload_amount}"))
				
				await msg.add_reaction(reload_emoji)
				
				while True:
					try:
						reaction, user = await self.client.wait_for(
							"reaction_add",
							timeout = 60,
							check = lambda reaction, user:
								user == ctx.author and str(reaction.emoji) == reload_emoji)
					except asyncio.TimeoutError:
						break
					else:
						reload_amount += 1
						await msg.remove_reaction(reload_emoji, user)
						await msg.edit(embed =
							dino_to_embed(random.choice(dino_names))
							.set_footer(text = f"#{reload_amount}"))
		else:
			await ctx.send(embed = utils.command_disabled)

def dino_to_embed(dino):
	return (discord.Embed(
		description = dinos[dino],
		color = utils.embed_color)
		.set_author(
			name = dino.replace("_", " ").split("#")[-1],
			url = "https://en.wikipedia.org/wiki/" + dino,
			icon_url = random.choice(utils.icons["dinos"])))

def setup(client):
	client.add_cog(Dino(client))