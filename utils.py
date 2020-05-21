import discord
from discord.ext import commands

import json

lad_id = 709644595104972890
embed_color = 0xe07bb8
global db
settings = {}

command_disabled = discord.Embed(
	title = "Command disabled!",
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

def get_setting(guild_id, setting):
	return guild_id not in settings or settings[guild_id][setting]