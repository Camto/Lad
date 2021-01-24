import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import sys
import os
import asyncio
import asyncpg
import json
import aioconsole

sys.path.append(".")
import utils

client = commands.Bot(command_prefix = "l.", intents = discord.Intents().all())

client.remove_command("help")

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		await ctx.send(embed = utils.embeds["command not found"])

@client.event
async def on_ready():
	print(f"{client.user.name}#{client.user.discriminator} logged in!")

print("Loading cogs:")

for cog in utils.cogs_to_load:
	print(f"  Loading {cog}")
	client.load_extension(cog)

print("Done")

async def start_bot():	
	# Start up settings database.
	utils.db = await asyncpg.connect(utils.master_settings["database url"])
	
	await utils.db.execute("""
		create table if not exists settings (
			guild_id text primary key)""")
	
	for option in utils.option_names:
		type = utils.options[option]["type"]
		default = utils.options[option]["default"]
		await utils.db.execute(f"""
			alter table settings
			add column if not exists {option} {type}""")
	
	# Fetch settings.
	guilds = await utils.db.fetch("select * from settings")
	
	for guild in guilds:
		guild_id = int(guild["guild_id"])
		utils.settings[guild_id] = {}
		for option in utils.option_names:
			if option in guild and guild[option] is not None:
				val = guild[option]
				if utils.options[option]["type"] == "json":
					val = json.loads(val)
			else:
				val = utils.options[option]["default"]
			utils.settings[guild_id][option] = val
	
	# Log the bot in.
	await client.start(utils.master_settings["token"])

loop = asyncio.get_event_loop()

try:
	loop.run_until_complete(start_bot())
except Exception as err:
	print(err)
	loop.run_until_complete(client.logout())
finally:
	loop.close()