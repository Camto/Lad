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
			await gen.asend(reaction.emoji)
			embed, new_reactions = await gen.__anext__()
			
			await msg.edit(embed = embed)
			await msg.remove_reaction(str(reaction.emoji), user)
			
			if new_reactions != None:
				for reaction in reactions:
					await msg.remove_reaction(reaction, client.user)
				for reaction in new_reactions:
					await msg.add_reaction(reaction)
				reactions = new_reactions
	
	gen.aclose()

class menus():
	menu = menu
