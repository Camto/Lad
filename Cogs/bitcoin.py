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
      request = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
      info = json.loads(request.text)
      await ctx.send(embed = discord.Embed(
        title = f":coin: 1 Bitcoin = {info['bpi']['USD']['rate']} USD",
        color = utils.embed_color)
        .set_footer(text = f"[{info['time']['updated']}] Disclaimer: This data was produced from the CoinDesk Bitcoin Price Index (USD)."))
    elif cmd[0].lower() == "history":
      today = datetime.date.today()
      week = today - datetime.timedelta(days=7)
      dates = []
      for date in range(8):
        dates.append(str(datetime.date.today() - datetime.timedelta(days=date)))    
      request = requests.get(f"https://api.coindesk.com/v1/bpi/historical/close.json?start={week}&end={today}")
      info = json.loads(request.text)
      await ctx.send(embed = discord.Embed(
        title = "Bitcoin price the last 7 days",
        description = f":coin: Today | ${info['bpi'][dates[0]]} \n\n :coin: {dates[1]} | ${info['bpi'][dates[1]]} \n\n :coin: {dates[2]} | ${info['bpi'][dates[2]]} \n\n :coin: {dates[3]} | ${info['bpi'][dates[3]]} \n\n :coin: {dates[4]} | ${info['bpi'][dates[4]]} \n\n :coin: {dates[5]} | ${info['bpi'][dates[5]]} \n\n :coin: {dates[6]} | ${info['bpi'][dates[6]]} \n\n :coin: {dates[7]} | ${info['bpi'][dates[7]]}",
        color = utils.embed_color)
        .set_footer(text = f"[{info['time']['updated']}] Disclaimer: This data was produced from the CoinDesk Bitcoin Price Index (USD)."))
    else:
      currency = cmd[0].upper()
      request = requests.get(f"https://api.coindesk.com/v1/bpi/currentprice/{urllib.parse.quote(currency, safe = '')}.json")
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