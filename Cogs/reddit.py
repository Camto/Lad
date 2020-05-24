import discord
from discord.ext import commands

import asyncio
import json
import requests
import urllib.parse
import utils

reload_emoji = "\U0001f504"

# Get Reddit posts and users.
class Reddit(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def reddit(self, ctx, *args):
		if len(args) >= 1:
			sub = args[0]
			
			msg = await ctx.send(embed =
				post_to_embed(get_random_post(sub)))
			
			await msg.add_reaction(reload_emoji)
			
			while True:
				try:
					reaction, user = await self.client.wait_for(
						"reaction_add",
						timeout = 60,
						check = lambda reaction, user:
							user == ctx.author and str(reaction.emoji) == reload_emoji)
				except asyncio.TimeoutError:
					break
				else:
					await msg.remove_reaction(reload_emoji, user)
					await msg.edit(embed =
						post_to_embed(get_random_post(sub)))

def post_to_embed(post):
	embed = (discord.Embed(
		description = post["selftext"][:2000],
		color = utils.embed_color)
		.set_author(
			name = post["title"],
			icon_url = utils.icons["reddit"],
			url = f'https://www.reddit.com{post["permalink"]}'))
	
	if not post["is_self"]:
		if "post_hint" in post:
			if post["post_hint"] == "image":
				embed.set_image(url = post["url"])
			elif (
				post["post_hint"] == "link" and
				post["thumbnail"] != "default"):
				embed.set_thumbnail(url = post["thumbnail"])
	
	return embed

def get_random_post(sub):
	post = json.loads(requests.get(
		f"https://www.reddit.com/r/{urllib.parse.quote(sub, safe = '')}/random.json",
		headers = {"User-agent": "Ladbot"}).text)
	if "error" not in post:
		if isinstance(post, list):
			post = post[0]
		return post["data"]["children"][0]["data"]
	else:
		print(post["error"])
		return {
			"title": "Error",
			"selftext": "Failed to get post.",
			"is_self": True,
			"permalink": ""
		}

def setup(client):
	client.add_cog(Reddit(client))