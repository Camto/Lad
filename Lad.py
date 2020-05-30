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
	# Start up settings database.
	utils.db = aiosqlite.connect("./settings.db")
	await utils.db.__aenter__()
	
	# Create settings table if it doesn't exist yet.
	
	has_created_settings = (
		await (await utils.db.execute("pragma user_version")).fetchone())[0]
	
	if not has_created_settings:
		await utils.db.execute("""
			create table settings (
				guild_id text primary key,
				autoresponses integer,
				bible integer,
				dino integer,
				ping integer,
				say integer)""")
		await utils.db.execute("pragma user_version = 1")
	
	# Fetch settings.
	guilds = await (await utils.db.execute("select * from settings")).fetchall()
	for guild in guilds:
		utils.settings[int(guild[0])] = {
			"autoresponses": guild[1],
			"bible": guild[2],
			"dino": guild[3],
			"ping": guild[4],
			"say": guild[5]
		}
	
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