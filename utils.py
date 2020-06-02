import discord
from discord.ext import commands

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