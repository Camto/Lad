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
	
	@commands.command(aliases = ["btc"])
	async def bitcoin(self, ctx, *cmd):
		if utils.get_setting(ctx.guild, "bitcoin"):
			if len(cmd) == 0:
				request = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
				info = json.loads(request.text)
				
				await ctx.send(embed = discord.Embed(
					color = utils.embed_color)
					.set_author(
						name = f"1 BTC = {info['bpi']['USD']['rate']} USD",
						icon_url = utils.icons["bitcoin"]))
			elif cmd[0].lower() == "history" or " h ":
				today = datetime.date.today()
				week = today - datetime.timedelta(days = 7)
				dates = []
				# Current date -7 days in the past for a week.
				for date in range(8):
					dates.append(str(datetime.date.today() - datetime.timedelta(days = date)))		
				
				# Lucky the API request just so happens to have the same date formatting than datetime, use the previous list and dates.
				request = requests.get(f"https://api.coindesk.com/v1/bpi/historical/close.json?start={week}&end={today}")
				info = json.loads(request.text)
				fields = tuple((f"${info['bpi'][dates[i]]}", f"{dates[i]}") for i in range(1,8))
				
				embed = (discord.Embed(
					color = utils.embed_color)
					.set_author(
						name = "BTC to USD last week",
						icon_url = utils.icons["bitcoin"]))
				for name, value in fields:
					embed.add_field(name = name, value = value, inline = False)
				
				await ctx.send(embed = embed)
			else:
				currency = cmd[0].upper()
				request = requests.get(f"https://api.coindesk.com/v1/bpi/currentprice/{urllib.parse.quote(currency, safe = '')}.json")
				# When the currency doesn't exist
				if request.status_code == 404:
					await ctx.send(embed = utils.embeds["bitcoin error"])
				elif request.status_code == 200:
					info = json.loads(request.text)
					
					await ctx.send(embed = discord.Embed(
						color = utils.embed_color)
						.set_author(
							name = f"1 BTC = {info['bpi'][currency]['rate']} {currency}",
							icon_url = utils.icons["bitcoin"]))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Bitcoin(client))