import discord
from discord.ext import commands
import utils

import asyncio
import os
import random
import string

import requests
from PIL import Image
from requests.auth import HTTPBasicAuth

class Convert(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def convert(self, ctx, *args):
		if len(args) == 0 or len(args) == 1:
			await ctx.send(embed = utils.embeds["convert more info"])
		else:
			url = args[1]
			extension = args[0]
			temp_file = "".join(
				random.choice(string.ascii_lowercase)
				for _ in range(10))
			
			try:
				image_file = requests.get(url, allow_redirects = True)
				open(f"{temp_file}", "wb").write(image_file.content)

				try:
					im = Image.open(temp_file)
					im.save(f"{temp_file}.{extension}", quality = 100)
					nfile = discord.File(
						f"{temp_file}.{extension}", filename = f"Converted File.{extension}")
					await ctx.send(file = nfile, embed = utils.embeds["convert success"])
				except:
					await ctx.send(embed = utils.embeds["convert error converting"])
			except:
				await ctx.send(embed = utils.embeds["convert error downloading"])
			finally:
				if os.path.isfile(f"{temp_file}.{extension}"):
					os.remove(f"{temp_file}.{extension}")
				if os.path.isfile(temp_file):
					os.remove(temp_file)

def setup(client):
	client.add_cog(Convert(client))