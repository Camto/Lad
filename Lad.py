import discord
from discord.ext import commands
from discord.ext.commands import Bot

import random
import json
import asyncio
import aiosqlite
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

lad_id = 709644595104972890
embed_color = 0xe07bb8
settings = {}

def get_json(filename):
	file = open(f"./Data/{filename}.json", encoding = "utf-8")
	data = json.load(file)
	file.close()
	return data

options = get_json("options")
autoresponses = get_json("autoresponses")
icons = get_json("icons")
quotes = get_json("bible quotes")
dinos = get_json("dinos")
pars = get_json("pars")

client = commands.Bot(command_prefix = "l.")

client.remove_command("help")

@client.event
async def on_ready():
	activity = discord.Streaming(name = "l.help", url = "https://www.twitch.tv/jpvinnie")
	await client.change_presence(status = discord.Streaming, activity = activity)
	print(f"{client.user.name}#{client.user.discriminator} logged in!")

# Show command descriptions.
@client.command()
async def help(ctx, *cmd):
	if len(cmd) == 0:
		await ctx.send(embed = discord.Embed(
		title = "Commands",
		description = "This bot's prefix is ``l.``",
		color = embed_color)
		.add_field(name = "help", value = "Show this message.", inline = False)
		.add_field(name = "ping", value = "Responds with pong.", inline = False)
		.add_field(name = "say", value = "Make the bot say something.", inline = False)
		.add_field(name = "bible", value = "Returns a random bible verse. For verses do l.help bible", inline = False)
		.add_field(name = "dino", value = "Use `l.dino` for a random dinosaur, `l.dino <dinosaur name here>` to find the dinosaur with that name.", inline = False))
	elif cmd[0] == "bible":
		await ctx.send(embed = discord.Embed(
		title = "Bible Verses",
		color = embed_color)
		.set_author(
			name = "To search type NUMBER first; followed by BOOK",
			icon_url = icons["bible"])
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

# Ping command to check users ping.
@client.command()
async def ping(ctx):
	await ctx.send(embed = discord.Embed(
		title = "Pong!",
		description = f"Hey, {ctx.message.author.mention}. Current ping is: ``{round(client.latency * 1000)}`` ms.",
		color = embed_color))

# Starting the bible study.
@client.command()
async def bible(ctx, *args):
	if len(args) == 0:
		quote = random.choice(quotes)
	else:
		quote = process.extractOne(
			args[0],
			quotes,
			scorer = fuzz.partial_token_sort_ratio)[0]

	await ctx.send(embed = discord.Embed(
		description = quote["text"],
		color = embed_color)
		.set_author(
			name = quote["location"],
			icon_url = icons["bible"]))

# Process dino related requests.
@client.command()
async def dino(ctx, *args):
	if len(args) == 0:
		dino = random.choice(dinos)
	else:
		dino = process.extractOne(args[0], dinos)[0]
	
	await ctx.send(embed = discord.Embed(
		description = pars[dino],
		color = embed_color)
		.set_author(
			name = dino.replace("_", " "),
			url = "https://en.wikipedia.org/wiki/" + dino,
			icon_url = random.choice(icons["dinos"])))

# Change server settings.
@client.command()
async def settings(ctx, *args):
	if ctx.message.author.guild_permissions.administrator:
		# If an option is being changed.
		
		if len(args) >= 2:
			# Make sure server is in settings database.
			
			guild_in_db = await (await db.execute(
				"SELECT * FROM settings WHERE guild_id = ?",
				(ctx.guild.id,))).fetchone()
			
			if not guild_in_db:
				await db.execute("""
					INSERT INTO settings
						(guild_id, autoresponses)
					VALUES
						(?, 1)""",
					(ctx.guild.id,))
				await db.commit()
				print(f"Server {ctx.guild.name} ({ctx.guild.id}) has been added to the settings database.")
			
			# Actually change the options.
			
			if args[0] in options:
				if args[1] == "yes" or args[1] == "no":
					await db.execute(f"""
						UPDATE settings
						SET {args[0]} = ?
						WHERE guild_id = ?""",
						(1 if args[1] == "yes" else 0, ctx.guild.id))
					await db.commit()
					await ctx.send(embed = discord.Embed(
						description = f"Turned {args[0]} {'on' if args[1] == 'yes' else 'off'}.",
						color = embed_color))
				else:
					await ctx.send(embed = discord.Embed(
						description = f"{args[1]} is not a valid setting, use yes or no.",
						color = embed_color))
			else:
				await ctx.send(embed = discord.Embed(
					description = f"{args[0]} is not an option that can be toggled.",
					color = embed_color))
		else:
			await ctx.send(embed = discord.Embed(
				description = "Not enough arguments were given to change an option, for help with `l.settings`, please use `l.help settings`.",
				color = embed_color))
	else:
		await ctx.send(embed = discord.Embed(
			description = "You're not an admin, you can't change the settings.",
			color = embed_color))

# Response system.
@client.event
async def on_message(msg):
	if msg.author.id != lad_id:
		content = msg.content
		
		if content.startswith("l."):
			# The say command is actually here.
			if content.startswith("l.say"):
				await msg.channel.send(content[5:].lstrip())
				return await msg.delete()
			else:
				return await client.process_commands(msg)
		
		text = content.lower()
		for pair in autoresponses:
			for keyword in pair["keywords"]:
				if keyword in text:
					return await msg.channel.send(random.choice(pair["responses"]))

async def start_bot():
	global db
	db = aiosqlite.connect("./settings.db")
	await db.__aenter__()
	
	has_created_settings = (
		await (await db.execute("PRAGMA user_version")).fetchone())[0]
	
	if has_created_settings == 0:
		await db.execute("""
			CREATE TABLE settings (
				guild_id TEXT PRIMARY KEY,
				autoresponses INTEGER)""")
		await db.execute("PRAGMA user_version = 1")
	
	await client.start(get_json("auth")["token"])

loop = asyncio.get_event_loop()

try:
	loop.run_until_complete(start_bot())
except:
	loop.run_until_complete(db.__aexit__(0, 0, 0))
	loop.run_until_complete(client.logout())
finally:
	loop.close()