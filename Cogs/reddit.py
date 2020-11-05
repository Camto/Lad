import discord
from discord.ext import commands
import utils

import json
import urllib.parse

import requests

reload_emoji = utils.emojis["reload"]
next_emoji = utils.emojis["right pointer"]
prev_emoji = utils.emojis["left pointer"]
sorting_methods = ["hot", "new", "rising", "top", "controversial"]
top_sub_sorts = ["hour", "day", "week", "month", "year", "all"]

# Get Reddit posts and users.
class Reddit(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def reddit(self, ctx, *args):
		if utils.get_setting(ctx.guild.id, "reddit"):
			if len(args) >= 1:
				if args[0].startswith("r/"):
					await handle_sub(self, ctx, args)
				elif args[0].startswith("u/"):
					await handle_user(self, ctx, args)
				else:
					await ctx.send(embed = utils.embeds["reddit error"])
			else:
				await ctx.send(embed = utils.embeds["reddit error"])
		else:
			await ctx.send(embed = utils.embeds["command disabled"])

async def handle_sub(self, ctx, args):
	sub = args[0]
	
	if len(args) == 1 or args[1] == "random":
		async def menu_sub_random(_):
			while True:
				yield post_to_embed(get_random_post(sub))
		
		await utils.menus.reload(self.client, ctx, menu_sub_random)
	elif args[1] in sorting_methods:
		if args[1] != "top":
			# Sort by method other than top.
			n = int(args[2]) if len(args) >= 3 else 25
			posts = get_n_posts_by_sort(sub, n, args[1])
		elif len(args) >= 3 and args[2] in top_sub_sorts:
			# Sort by top of all time as the default for top.
			n = int(args[3]) if len(args) >= 4 else 25
			posts = get_n_posts_by_sort(sub, n, args[1], args[2])
		else:
			# Sort by top of all X.
			n = int(args[2]) if len(args) >= 3 else 25
			posts = get_n_posts_by_sort(sub, n, args[1])
		
		await menu_posts(self, ctx, posts[-n:])
	else:
		await ctx.send(embed = discord.Embed(
			description = f"Error, {args[1]} is not a sorting method this bot knows of. Use one of `hot`, `new`, `rising`, `top`, or `controversial` instead.",
			color = utils.embed_color)
			.set_author(
				name = "Invalid Sorting Method",
				icon_url = utils.icons["reddit"]))

async def handle_user(self, ctx, args):
	if len(args) == 1 or args[1] == "about":
		about = get_user_about(args[0][2:])
		
		if about["icon_img"] != "":
			profile_img = urllib.parse.urlparse(about["icon_img"])
			profile_img = f"{profile_img.scheme}://{profile_img.netloc}{profile_img.path}"
		else:
			profile_img = ""
		
		await ctx.send(embed = discord.Embed(
			description = about["subreddit"]["public_description"],
			color = utils.embed_color)
			.set_author(
				name = about["name"],
				icon_url = utils.icons["reddit"],
				url = f'https://www.reddit.com{about["subreddit"]["url"]}')
			.set_thumbnail(url = profile_img)
			.add_field(
				name = "Karma",
				value = about["link_karma"] + about["comment_karma"]))
	elif args[1] == "posts":
		sub = args[0] + "/submitted"
		
		if len(args) == 2:
			n = int(args[3]) if len(args) >= 4 else 25
			posts = get_n_posts_by_sort(sub, n, "new")
		elif args[2] != "top":
			# Sort by method other than top.
			n = int(args[3]) if len(args) >= 4 else 25
			posts = get_n_posts_by_sort(sub, n, args[2])
		elif len(args) >= 4 and args[3] in top_sub_sorts:
			# Sort by top of all time as the default for top.
			n = int(args[4]) if len(args) >= 5 else 25
			posts = get_n_posts_by_sort(sub, n, args[2], args[3])
		else:
			# Sort by top of all X.
			n = int(args[3]) if len(args) >= 4 else 25
			posts = get_n_posts_by_sort(sub, n, args[2])
		
		await menu_posts(self, ctx, posts[-n:])
	else:
		await ctx.send(embed = discord.Embed(
			description = f"``{args[1]}`` is not a property this bot knows how to get from Reddit users. Only `about` (the default) and `posts` work.",
			color = utils.embed_color)
			.set_author(
				name = "Can't get user property.",
				icon_url = utils.icons["reddit"]))

async def menu_posts(self, ctx, posts):
	async def menu_gen(_):
		yield len(posts)
		for post in posts:
			yield post_to_embed(post)
	await utils.menus.list(self.client, ctx, menu_gen)

def post_to_embed(post):
	embed = (discord.Embed(
		description = post["selftext"][:2000],
		color = utils.embed_color)
		.set_author(
			name = post["title"],
			icon_url = utils.icons["reddit"],
			url = f"https://www.reddit.com{post['permalink']}"))
	
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
	url = f"https://www.reddit.com/{urllib.parse.quote(sub, safe = '')}/random.json"
	post = json.loads(requests.get(url, headers = {"User-agent": "Ladbot"}).text)
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

def get_n_posts_by_sort(sub, n, sorting_method, top_sub_sort = "all"):
	if n > 100:
		return [{
			"title": "Error",
			"selftext": "Cannot fetch more than 100 posts.",
			"is_self": True,
			"permalink": ""
		}]
	
	if sub[:2] == "r/":
		url = f"https://www.reddit.com/{urllib.parse.quote(sub, safe = '')}/{sorting_method}.json?limit={n}"
	else:
		url = f"https://www.reddit.com/{urllib.parse.quote(sub, safe = '')}.json?sort={sorting_method}&limit={n}"
	if sorting_method == "top":
		url += f"&t={top_sub_sort}"
	
	posts = json.loads(requests.get(url, headers = {"User-agent": "Ladbot"}).text)
	
	if len(posts["data"]["children"]) != 0:
		return list(map(lambda post: post["data"], posts["data"]["children"]))
	else:
		return [{
			"title": "Error",
			"selftext": "There are no posts in that subreddit.",
			"is_self": True,
			"permalink": ""
		}]

def get_user_about(user):
	url = f"https://www.reddit.com/u/{urllib.parse.quote(user, safe = '')}/about.json"
	post = json.loads(requests.get(url, headers = {"User-agent": "Ladbot"}).text)
	if "error" not in post:
		return post["data"]
	else:
		print(post["error"])
		return {
			"name": "Error",
			"subreddit": {
				"public_description": "Failed to get user.",
				"url": ""
			},
			"icon_img": "",
			"link_karma": 0,
			"comment_karma": 0
		}

def setup(client):
	client.add_cog(Reddit(client))