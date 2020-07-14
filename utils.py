import discord
from discord.ext import commands

import asyncio
import yaml

lad_id = 709644595104972890
embed_color = 0xe07bb8
global db
settings = {}

command_disabled = discord.Embed(
	title = "Command Disabled!",
	description = "This command was disabled in the settings by an admin.",
	color = embed_color)

def get_yaml(filename):
	with open(f"./Data/{filename}.yaml", encoding = "utf-8") as stream:
		return yaml.safe_load(stream)

options = get_yaml("options")
option_names = list(options.keys())
icons = get_yaml("icons")
emojis = get_yaml("emojis")

def get_setting(guild_id, option):
	if guild_id in settings:
		return settings[guild_id][option]
	else:
		return options[option]["default"]

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
			embed, new_reactions = await gen.asend(str(reaction.emoji))
			
			await msg.edit(embed = embed)
			await msg.remove_reaction(str(reaction.emoji), user)
			
			if new_reactions != None:
				for reaction in reactions:
					await msg.remove_reaction(reaction, client.user)
				for reaction in new_reactions:
					await msg.add_reaction(reaction)
				reactions = new_reactions
	
	gen.aclose()

def reload_menu(gen_):
	async def inner(caller):
		gen = gen_(caller)
		reload_number = 1
		yield (
			(await gen.__anext__()).set_footer(text = f"#{reload_number}"),
			[emojis["reload"]])
		while True:
			reload_number += 1
			yield (
				(await gen.__anext__()).set_footer(text = f"#{reload_number}"),
				None)
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
		
		dir = yield embeds[0], [next_emoji]
		
		while True:
			idx += 1 if dir == next_emoji else -1
			idx = min(max(idx, 0), total_embeds - 1)
			if len(embeds) <= idx:
				embeds.append(prepend_footer_text(
					await gen.__anext__(),
					f"{idx+1}/{total_embeds}"))
			
			reactions = None
			if idx == 0: reactions = [next_emoji]
			elif idx == total_embeds - 1: reactions = [prev_emoji]
			elif (
				idx == 1 and dir == next_emoji or
				idx == total_embeds - 2 and dir == prev_emoji):
				reactions = [prev_emoji, next_emoji]
			
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