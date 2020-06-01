import discord
from discord.ext import commands

import json

lad_id = 709644595104972890
embed_color = 0xe07bb8
global db
settings = {}

command_disabled = discord.Embed(
	title = "Command Disabled!",
	description = "This command was disabled in the settings by an admin.",
	color = embed_color)

def get_json(filename):
	file = open(f"./Data/{filename}.json", encoding = "utf-8")
	data = json.load(file)
	file.close()
	return data

options = get_json("options")
option_names = list(options.keys())
icons = get_json("icons")
emojis = get_json("emojis")

def get_setting(guild_id, option):
	if guild_id in settings:
		return settings[guild_id][option]
	else:
		return options[option]["default"]