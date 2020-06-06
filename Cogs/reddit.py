import discord
from discord.ext import commands

import asyncio
import json
import requests
import urllib.parse
import utils

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
					await ctx.send(embed = discord.Embed(
						description = "Error, you did not provide a subreddit (starting with `r/`) or a user (starting with `u/`) You can use `l.help reddit` for help.",
						color = utils.embed_color)
						.set_author(
							name = "Wrong Arguments",
							icon_url = utils.icons["reddit"]))
		else:
			await ctx.send(embed = utils.command_disabled)

async def handle_sub(self, ctx, args):
	sub = args[0][2:]
	
	if len(args) == 1 or args[1] == "random":
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
	elif args[1] in sorting_methods:
		if args[1] != "top":
			posts = get_n_posts_by_sort(
				sub,
				int(args[2]) if len(args) >= 3 else 25,
				args[1])
		elif len(args) >= 3 and args[2] in top_sub_sorts:
			posts = get_n_posts_by_sort(
				sub,
				int(args[3]) if len(args) >= 4 else 25,
				args[1],
				args[2])
		else:
			posts = get_n_posts_by_sort(
				sub,
				int(args[2]) if len(args) >= 3 else 25,
				args[1])
		
		idx = 0
		total_posts = len(posts)
		
		posts_as_embeds = [
			post_to_embed(posts[0])
			.set_footer(text = f"{idx+1}/{total_posts}")]
		
		msg = await ctx.send(embed = posts_as_embeds[0])
		
		await msg.add_reaction(next_emoji)
		
		while True:
			try:
				reaction, user = await self.client.wait_for(
					"reaction_add",
					timeout = 60,
					check = lambda reaction, user:
						reaction.message.id == msg.id and
						user == ctx.author and
						(
							str(reaction.emoji) == next_emoji or
							str(reaction.emoji) == prev_emoji))
			except asyncio.TimeoutError:
				break
			else:
				idx += 1 if str(reaction.emoji) == next_emoji else -1
				idx = min(max(idx, 0), total_posts - 1)
				if len(posts_as_embeds) <= idx:
					posts_as_embeds.append(
						post_to_embed(posts[idx])
							.set_footer(text = f"{idx+1}/{total_posts}"))
				
				await msg.edit(embed = posts_as_embeds[idx])
				
				await msg.remove_reaction(str(reaction.emoji), user)
				
				if idx == 0:
					await msg.remove_reaction(prev_emoji, self.client.user)
					await msg.add_reaction(next_emoji)
				elif idx == total_posts - 1:
					await msg.remove_reaction(next_emoji, self.client.user)
					await msg.add_reaction(prev_emoji)
				elif idx == 1 and str(reaction.emoji) == next_emoji:
					await msg.remove_reaction(next_emoji, self.client.user)
					await msg.add_reaction(prev_emoji)
					await msg.add_reaction(next_emoji)
				elif idx == total_posts - 2 and str(reaction.emoji) == prev_emoji:
					await msg.add_reaction(next_emoji)
	else:
		await ctx.send(embed = discord.Embed(
			description = f"Error, {args[1]} is not a sorting method. Use one of `hot`, `new`, `rising`, `top`, or `controversial` instead.",
			color = utils.embed_color)
			.set_author(
				name = "Invalid Sorting Method",
				icon_url = utils.icons["reddit"]))

async def handle_user(self, ctx, args):
	about = get_user_about(args[0][2:])
	print(about)
	if about["icon_img"] != "":
		profile_img = urllib.parse.urlparse(about["icon_img"])
		profile_img = f"{profile_img.scheme}://{profile_img.netloc}{profile_img.path}"
	else:
		profile_img = ""
	print(profile_img)
	await ctx.send(embed = discord.Embed(
		description = about["subreddit"]["public_description"],
		color = utils.embed_color)
		.set_author(
			name = about["name"],
			icon_url = utils.icons["reddit"],
			url = f'https://www.reddit.com{about["subreddit"]["url"]}')
		.set_thumbnail(url = profile_img))

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
	url = f"https://www.reddit.com/r/{urllib.parse.quote(sub, safe = '')}/random.json"
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
	
	url = f"https://www.reddit.com/r/{urllib.parse.quote(sub, safe = '')}/{sorting_method}.json?limit={n}"
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
			"icon_img": ""
		}

def setup(client):
	client.add_cog(Reddit(client))