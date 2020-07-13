import discord
from discord.ext import commands
import utils

import json
import urllib

import requests

class Bitcoin(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def bitcoin(self, ctx, *cmd):
		if utils.get_setting(ctx.guild.id, "bitcoin"):
			if len(cmd) == 0:
				request = requests.get(
					"https://api.coindesk.com/v1/bpi/currentprice/USD.json")
				info = json.loads(request.text)
				await ctx.send(embed = discord.Embed(
					title = ":information_source: Info",
					description=f"Bitcoin price is: {info['bpi']['USD']['rate']} USD",
					color = utils.embed_color))
			else:
				currency = cmd[0].upper()
				request = requests.get(
					f"https://api.coindesk.com/v1/bpi/currentprice/{urllib.parse.quote(currency, safe = '')}.json")
				if request.status_code == 404:
					await ctx.send(embed = discord.Embed(
						title = ":anger: Error, currency not found",
						description = "Current list of currencies: [Official Website](https://www.coindesk.com/price/bitcoin)",
						color = utils.embed_color))
				elif request.status_code == 200:
					info = json.loads(request.text)
					await ctx.send(embed=discord.Embed(
						title = ":information_source: Info",
						description = f"Bitcoin price is: {info['bpi'][currency]['rate']} {currency}",
						color = utils.embed_color))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Bitcoin(client))