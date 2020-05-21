import discord
from discord.ext import commands

import sys
import os
import random
import json
import asyncio

import aiosqlite
import art

sys.path.append(".")
import utils

autoresponses = utils.get_json("autoresponses")

command_disabled = discord.Embed(
	title = "Command disabled!",
	description = "This command was disabled in the settings by an admin.",
	color = utils.embed_color)

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

# Ping command to check users ping.
@client.command()
async def ping(ctx):
	if utils.get_setting(ctx.guild.id, "ping"):
		await ctx.send(embed = discord.Embed(
			title = "Pong!",
			description = f"Hey, {ctx.message.author.mention}. Current ping is: ``{round(client.latency * 1000)}`` ms.",
			color = utils.embed_color))
	else:
		await ctx.send(embed = command_disabled)

# The autoresponse system and relegating commands.
@client.event
async def on_message(msg):
	if msg.author.id != utils.lad_id:
		content = msg.content
		
		if content.startswith("l."):
			# The say command is actually here.
			if content.startswith("l.say"):
				if utils.get_setting(msg.guild.id, "say"):
					await msg.channel.send(content[5:].lstrip())
					return await msg.delete()
				else:
					await msg.channel.send(embed = command_disabled)
			elif content.startswith("l.ascii"):
				#if utils.get_setting(msg.guild.id, "ascii"):
					ascii_txt = art.text2art(content[7:].lstrip())
					await msg.channel.send(f"```\n{ascii_txt}\n```")
				#else: 
				#	await msg.channel.send(embed = command_disabled)
			else:
				return await client.process_commands(msg)
		
		if utils.get_setting(msg.guild.id, "autoresponses"):
			text = content.lower()
			for pair in autoresponses:
				for keyword in pair["keywords"]:
					if keyword in text:
						return await msg.channel.send(random.choice(pair["responses"]))

async def start_bot():
	# Start up settings database.
	utils.db = aiosqlite.connect("./settings.db")
	await utils.db.__aenter__()
	
	# Create settings table if it doesn't exist yet.
	
	has_created_settings = (
		await (await utils.db.execute("PRAGMA user_version")).fetchone())[0]
	
	if not has_created_settings:
		await utils.db.execute("""
			CREATE TABLE settings (
				guild_id TEXT PRIMARY KEY,
				autoresponses INTEGER,
				bible INTEGER,
				dino INTEGER,
				ping INTEGER,
				say INTEGER)""")
		await utils.db.execute("PRAGMA user_version = 1")
	
	# Fetch settings.
	guilds = await (await utils.db.execute("SELECT * FROM settings")).fetchall()
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