import discord
from discord.ext import commands

import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import utils

dinos = utils.get_json("dinos")
dino_names = list(dinos.keys())

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
			
			await ctx.send(embed = discord.Embed(
				description = dinos[dino],
				color = utils.embed_color)
				.set_author(
					name = dino.replace("_", " ").split("#")[-1],
					url = "https://en.wikipedia.org/wiki/" + dino,
					icon_url = random.choice(utils.icons["dinos"])))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Dino(client))