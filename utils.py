import discord
from discord.ext import commands

import sys
import os
import asyncio
import json

master_settings = json.loads(os.getenv(f"LADBOT_{sys.argv[1]}"))
print(f"Loaded master settings: {', '.join(master_settings.keys())}")

global db
settings = {}

def get_json(filename):
	with open(f"./Data/{filename}.json", encoding = "utf-8") as stream:
		return json.load(stream)

embed_color = get_json("embed-color")
options = get_json("options")
option_names = list(options.keys())
icons = get_json("icons")
emojis = get_json("emojis")
embeds = my_dictionary = {
	k: discord.Embed.from_dict(v)
	for k, v in get_json("embeds").items()}

command_disabled = embeds["command disabled"]

def get_setting(guild, option):
	# Guild is None if it's a DM
	if guild and guild.id in settings:
		return settings[guild.id][option]
	else:
		return options[option]["default"]

chunks = lambda l, n: [l[i * n:(i + 1) * n] for i in range((len(l) + n - 1) // n)]

async def wait_for_response(client, channel, user, timeout = None):
	try:
		msg = await client.wait_for(
			"message",
			timeout = timeout,
			check = lambda msg:
				msg.channel == channel and
				msg.author == user)
		return msg
	except asyncio.TimeoutError:
		return None

async def menu(client, ctx, gen_):
	gen = gen_(ctx.author)
	
	embed, reactions = await gen.__anext__()
	msg = await ctx.send(embed = embed)
	for reaction in reactions:
		await msg.add_reaction(reaction)
	
	while True:
		try:
			reaction, user = await client.wait_for(
				"reaction_add",
				timeout = 60,
				check = lambda reaction, user:
					reaction.message.id == msg.id and
					user == ctx.author and
					str(reaction.emoji) in reactions)
		except asyncio.TimeoutError:
			break
		else:
			new_embed, new_reactions = await gen.asend(str(reaction.emoji))
			
			if new_embed != embed:
				await msg.edit(embed = new_embed)
				embed = new_embed
			# Try because we could be in a DM
			try:
				await msg.remove_reaction(str(reaction.emoji), user)
			except: pass
			
			if new_reactions != reactions:
				for reaction in reactions:
					try:
						await msg.remove_reaction(reaction, client.user)
					except: pass
				for reaction in new_reactions:
					await msg.add_reaction(reaction)
				reactions = new_reactions
	
	gen.aclose()

def reload_menu(gen_):
	async def inner(caller):
		gen = gen_(caller)
		reload_number = 1
		yield (
			prepend_footer_text(await gen.__anext__(), f"#{reload_number}"),
			[emojis["reload"]])
		while True:
			reload_number += 1
			yield (
				prepend_footer_text(await gen.__anext__(), f"#{reload_number}"),
				[emojis["reload"]])
		await gen.aclose()
	return inner

def list_menu(gen_):
	next_emoji = emojis["right pointer"]
	prev_emoji = emojis["left pointer"]
	
	async def inner(caller):
		gen = gen_(caller)
		idx = 0
		total_embeds = await gen.__anext__()
		
		embeds = [prepend_footer_text(
			await gen.__anext__(),
			f"{idx+1}/{total_embeds}")]
		
		dir = yield embeds[0], ([next_emoji] if total_embeds > 1 else [])
		
		while True:
			idx += 1 if dir == next_emoji else -1
			idx = min(max(idx, 0), total_embeds - 1)
			if len(embeds) <= idx:
				embeds.append(prepend_footer_text(
					await gen.__anext__(),
					f"{idx+1}/{total_embeds}"))
			
			if total_embeds == 1: reactions = []
			elif idx == 0: reactions = [next_emoji]
			elif idx == total_embeds - 1: reactions = [prev_emoji]
			else: reactions = [prev_emoji, next_emoji]
			
			dir = yield embeds[idx], reactions
	
	return inner

def prepend_footer_text(embed, text):
	if embed.footer.text == discord.Embed.Empty:
		embed.set_footer(text = text, icon_url = embed.footer.icon_url)
	else:
		embed.set_footer(
			text = f"{text} - {embed.footer.text}",
			icon_url = embed.footer.icon_url)
	return embed

class menus():
	menu = menu
	async def reload(client, ctx, gen):
		return await menu(client, ctx, reload_menu(gen))
	async def list(client, ctx, gen):
		return await menu(client, ctx, list_menu(gen))

cogs = sys.argv[2]
cogs_to_load = []
for cog in cogs.split(","):
	if cog == "all":
		for filename in os.listdir("./Cogs"):
			if filename.endswith(".py"):
				cogs_to_load.append(f"Cogs.{filename[:-3]}")
	elif cog[0] == "!":
		cogs_to_load.remove(f"Cogs.{cog[1:]}")
	else:
		cogs_to_load.append(f"Cogs.{cog}")