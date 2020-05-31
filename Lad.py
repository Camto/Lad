import discord
from discord.ext import commands

import sys
import os
import random
import json
import asyncio
import aiosqlite

sys.path.append(".")
import utils

client = commands.Bot(command_prefix = "l.")

client.remove_command("help")

@client.event
async def on_ready():
	activity = discord.Streaming(name = "l.help", url = "https://www.twitch.tv/jpvinnie")
	await client.change_presence(status = discord.Streaming, activity = activity)
	print(f"{client.user.name}#{client.user.discriminator} logged in!")

for filename in os.listdir("./Cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"Cogs.{filename[:-3]}")

async def start_bot():
	print(os.getenv("database_url"))
	# Start up settings database.
	utils.db = aiosqlite.connect("./settings.db")
	await utils.db.__aenter__()
	
	try: await utils.db.execute("""
		create table settings (
			guild_id text primary key)""")
	except: pass
	
	for option in utils.option_names:
		type = utils.options[option]["type"]
		default = utils.options[option]["default"]
		try: await utils.db.execute(f"""
			alter table settings
			add {option} {type} default {default}""")
		except: pass
	
	# Fetch settings.
	guilds = await (await utils.db.execute("select * from settings")).fetchall()
	for guild in guilds:
		guild_id = int(guild[0])
		utils.settings[guild_id] = {}
		for option in utils.option_names:
			column_num = utils.options[option]["column num"]
			utils.settings[guild_id][option] = guild[column_num]
	
	# Log the bot in.
	await client.start(os.getenv("token"))

loop = asyncio.get_event_loop()

try:
	loop.run_until_complete(start_bot())
except:
	loop.run_until_complete(utils.db.__aexit__(0, 0, 0))
	loop.run_until_complete(client.logout())
finally:
	loop.close()