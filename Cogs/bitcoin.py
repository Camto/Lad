import discord
from discord.ext import commands
import utils

import json
import urllib

import requests

import datetime

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
					title = f":coin: 1 Bitcoin  = {info['bpi']['USD']['rate']} USD",
					color = utils.embed_color)
					.set_footer(text = f"[{info['time']['updated']}] Disclaimer: This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org"))
			else:
				currency = cmd[0].upper()
				request = requests.get(
					f"https://api.coindesk.com/v1/bpi/currentprice/{urllib.parse.quote(currency, safe = '')}.json")
				if request.status_code == 404:
					await ctx.send(embed = utils.embeds["bitcoin error"])
				elif request.status_code == 200:
					info = json.loads(request.text)
					await ctx.send(embed = discord.Embed(
						title = f":coin: 1 Bitcoin = {info['bpi'][currency]['rate']} {currency}",
						color = utils.embed_color)
						.set_footer(text = f"[{info['time']['updated']}] Disclaimer: This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org"))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Bitcoin(client))