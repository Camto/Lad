import discord
from discord.ext import commands

import json
import requests
import urllib.parse
import utils

# Get Reddit posts and users.
class Reddit(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def reddit(self, ctx, *args):
		if len(args) >= 1:
			post = json.loads(requests.get(
				f"https://www.reddit.com/r/{urllib.parse.quote(args[0], safe = '')}/random.json",
				headers = {"User-agent": "Ladbot"}).text)
			if "error" not in post:
				post = post[0]["data"]["children"][0]["data"]
				msg = await ctx.send(embed = post_to_embed(post))
			else:
				print(post["error"])

def post_to_embed(post):
	embed = (discord.Embed(
		description = post["selftext"],
		color = utils.embed_color)
		.set_author(
			name = post["title"],
			icon_url = utils.icons["reddit"],
			url = f'https://www.reddit.com{post["permalink"]}'))
	
	return embed

def setup(client):
	client.add_cog(Reddit(client))