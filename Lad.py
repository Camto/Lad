import discord
from discord.ext import commands

import sys
import os
import random
import json
import asyncio

import aiosqlite
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import art

sys.path.append(".")
import utils

autoresponses = utils.get_json("autoresponses")
quotes = utils.get_json("bible quotes")

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

# Show command descriptions.
@client.command()
async def help(ctx, *cmd):
	if len(cmd) == 0:
		await ctx.send(embed = discord.Embed(
		title = "Commands",
		description = "This bot's prefix is ``l.``",
		color = utils.embed_color)
		.set_footer(
			text = "https://github.com/Camto/Lad",
			icon_url = utils.icons["github"])
		.add_field(name = "help", value = "Show this message.", inline = False)
		.add_field(name = "ping", value = "Responds with pong.", inline = False)
		.add_field(name = "say", value = "Make the bot say something.", inline = False)
		.add_field(name = "bible", value = "Returns a random bible verse. For verses do l.help bible", inline = False)
		.add_field(name = "dino", value = "Use `l.dino` for a random dinosaur, `l.dino <dinosaur name here>` to find the dinosaur with that name.", inline = False))
	elif cmd[0] == "bible":
		await ctx.send(embed = discord.Embed(
		title = "To search type NUMBER first; followed by BOOK",
		color = utils.embed_color)
		.set_author(
			name = "Bible Help",
			icon_url = utils.icons["bible"])
		.add_field(name = "Matthew", value = "5:9 | 28:19 | 5:28 | 6:5 | 21:18-22 | 11:30 | 12:33 | 18:8 | 18:9", inline = False)
		.add_field(name = "Leviticus", value = "19:19 | 19:27 | 9:10 | 15:19-20 | 25:44-46 | 21:17-23", inline = False)
		.add_field(name = "Deuteronomy", value = "22:28-29 | 25:11-1 | 23:1 | 31:8 | 33:27 | 25:11-12", inline = False)
		.add_field(name = "Psalms", value = "23:1-6 | 46:1-3 | 9:9-10 | 34:10b | 32:7-8", inline = False)
		.add_field(name = "Exodus", value = "8:1-14 | 21:7-8 | 15:2 | 33:14 | 23:19", inline = False)
		.add_field(name = "Kings", value = "6:28-29 | 2:23-25 | 23:20-25", inline = False)
		.add_field(name = "John", value = "3:3 | 14:14 | 14:6 | 3:16", inline = False)
		.add_field(name = "Chronicles", value = "21:14-15 | 16:11", inline = False)
		.add_field(name = "Ephesians", value = "2:8 | 6:5 | 5:4", inline = False)
		.add_field(name = "Proverbs", value = "18:10 | 15:4", inline = False)
		.add_field(name = "Isaiah", value = "41:10 | 26:3-4", inline = False)
		.add_field(name = "Timothy", value = "6:6-9 | 3:16", inline = False)
		.add_field(name = "Luke", value = "16:18 | 3:11", inline = False)
		.add_field(name = "Peter", value = "5:8 | 2:18", inline = False)
		.add_field(name = "Numbers", value = "31:17-18", inline = False)
		.add_field(name = "Reverend", value = "21:8", inline = False)
		.add_field(name = "Nehemiah", value = "8:10", inline = False)
		.add_field(name = "Ezekiel", value = "47:11", inline = False)
		.add_field(name = "Hebrews", value = "12:1", inline = False)
		.add_field(name = "Romans", value = "3:23", inline = False)
		.add_field(name = "Genesis", value = "1:1", inline = False)
		.add_field(name = "Samuel", value = "6:19", inline = False))
	elif cmd[0] == "settings":
		option_list = "\n\n".join(map(
			lambda option: f"`{option[0]}`: {option[1]}",
			utils.options.items()))
		
		await ctx.send(embed = discord.Embed(
			description = f"""To change an option, use `l.settings <option name> <value>` <value> can be on or off.

{option_list}""",
			color = utils.embed_color)
			.set_author(
				name = "Settings Help",
				icon_url = utils.icons["settings"]))

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

# Starting the bible study.
@client.command()
async def bible(ctx, *args):
	if utils.get_setting(ctx.guild.id, "bible"):
		if len(args) == 0:
			quote = random.choice(quotes)
		else:
			quote = process.extractOne(
				args[0],
				quotes,
				scorer = fuzz.partial_token_sort_ratio)[0]

		await ctx.send(embed = discord.Embed(
			description = quote["text"],
			color = utils.embed_color)
			.set_author(
				name = quote["location"],
				icon_url = utils.icons["bible"]))
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