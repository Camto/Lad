import discord
from discord.ext import commands

import asyncio
import json
import requests
import urllib.parse
import utils

reload_emoji = utils.emojis["reload"]

# Get Reddit posts and users.
class Reddit(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def reddit(self, ctx, *args):
		if len(args) >= 1:
			sub = args[0]
			reload_amount = 1
			
			msg = await ctx.send(embed =
				post_to_embed(get_random_post(sub))
				.set_footer(text = f"#{reload_amount}"))
			
			await msg.add_reaction(reload_emoji)
			
			while True:
				try:
					reaction, user = await self.client.wait_for(
						"reaction_add",
						timeout = 60,
						check = lambda reaction, user:
							reaction.message.id == msg.id and
							user == ctx.author and
							str(reaction.emoji) == reload_emoji)
				except asyncio.TimeoutError:
					break
				else:
					reload_amount += 1
					await msg.remove_reaction(reload_emoji, user)
					await msg.edit(embed =
						post_to_embed(get_random_post(sub))
						.set_footer(text = f"#{reload_amount}"))

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

def get_n_posts_in_cat(sub, n, cat):
	if n < 100:
		return {
			"title": "Error",
			"selftext": "Cannot fetch more than 100 posts.",
			"is_self": True,
			"permalink": ""
		}
	
	posts = json.loads(requests.get(
		f"https://www.reddit.com/r/{urllib.parse.quote(sub, safe = '')}/{cat}.json?limit={n}",
		headers = {"User-agent": "Ladbot"}).text)
	
	if "error" not in posts:
		return list(map(lambda post: post["data"], posts["data"]["children"]))
	else:
		print(posts["error"])
		return {
			"title": "Error",
			"selftext": "Failed to get posts.",
			"is_self": True,
			"permalink": ""
		}

def setup(client):
	client.add_cog(Reddit(client))