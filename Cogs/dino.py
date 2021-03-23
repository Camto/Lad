import discord
from discord.ext import commands
import utils

import random

from fuzzywuzzy import fuzz, process

dinos = utils.get_json("dinos")
dino_names = list(dinos.keys())

# Process dino related requests.
class Dino(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def dino(self, ctx, *args):
		if utils.get_setting(ctx.guild, "dino"):
			if len(args) != 0:
				dino = process.extractOne(args[0], dino_names)[0]
				await ctx.send(embed = dino_to_embed(dino))
			else:
				await utils.menus.reload(self.client, ctx, dino_menu)
		else:
			await ctx.send(embed = utils.command_disabled)

async def dino_menu(_):
	while True:
		yield dino_to_embed(random.choice(dino_names))

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