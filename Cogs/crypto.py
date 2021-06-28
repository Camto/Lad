import discord
from discord.ext import commands
import utils

import json
from requests import Request, Session

from datetime import datetime

class Crypto(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(aliases = ["cryptocurrency"])
	async def crypto(self, ctx, *cmd):
		if len(cmd) > 0:
			symbol = cmd[0].upper()
			url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
			parameters = {"symbol":symbol, "convert":"USD"}
			headers = {"Accepts":"application/json", "X-CMC_PRO_API_KEY":"b5943040-4be4-479b-b4d7-c6bceefcd8a9"}

			session = Session()
			session.headers.update(headers)

			response = session.get(url, params=parameters)
			# pprint.pprint(json.loads(response.text)["data"][symbol]["quote"]["USD"])
			info = json.loads(response.text)["data"][symbol]["quote"]["USD"]

			market_cap = str(info["market_cap"])
			percent_change_24h = str(info["percent_change_24h"])[0:4]
			price = str(info["price"])[0:8]
			name = str(json.loads(response.text)["data"][symbol]["slug"])

			embed=discord.Embed(
				title = f"1 {name.capitalize()} = ${price}",
				color = utils.embed_color).set_footer(text=datetime.now())

			fields = [
			("Market Cap", f"${market_cap}", False),
			("Percent change in the last 24 hours", f"{percent_change_24h}%", False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await ctx.send(embed=embed)

		else:
			await ctx.send(embed=discord.Embed(
				tite = "ERROR, please provide a valid cryptocurrency's symbol (for example, ``BTC`` or ``ETH``.",
				color = utils.embed_color))

def setup(client):
	client.add_cog(Crypto(client))