import discord
from discord.ext import commands

import json
import utils
import aiohttp

class Bitcoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bitcoin(self, ctx, *cmd):
	    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
	    async with aiohttp.ClientSession() as session:  # Async HTTP request
		    raw_response = await session.get(url)
		    response = await raw_response.text()
		    response = json.loads(response)
		    currencies = ["USD","EUR","GBP"]
		    if len(cmd) == 0:
			    await ctx.send(embed = discord.Embed(
				    title = ':information_source: Info',
				    description = f"Current list of currencies", 
				    color=utils.embed_color)
				    .add_field(name = "USD", value = "United States Dollar", inline = False)
				    .add_field(name = "EUR", value = "Euro", inline = False)
				    .add_field(name = "GBP", value = "British Pound Sterling", inline = False))
		    elif cmd[0].upper() in currencies:
			    currency = cmd[0]
			    await ctx.send(embed = discord.Embed(
				    title = ':information_source: Info',
				    description = f"Bitcoin price is: ${response['bpi'][currency.upper()]['rate']} USD", 
				    color=utils.embed_color)
				    .set_footer(text = f"Requested by {ctx.message.author}."))
		    else:
			    await ctx.send(embed = discord.Embed(
				    title = ':anger: Error: Currency not found.', 
				    color=utils.embed_color)
				    .add_field(name = "USD", value = "United States Dollar", inline = False)
				    .add_field(name = "EUR", value = "Euro", inline = False)
				    .add_field(name = "GBP", value = "British Pound Sterling", inline = False))

def setup(client):
    client.add_cog(Bitcoin(client))