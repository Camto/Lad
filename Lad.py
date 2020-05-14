import discord
from discord.ext import commands
from discord.ext.commands import Bot

import random
import json
from fuzzywuzzy import process

def get_json(filename):
	file = open("./Data/" + filename, encoding = "utf-8")
	data = json.load(file)
	file.close()
	return data

lad_id = 709644595104972890
embed_color = 0xe07bb8
bible_icon = "https://raw.githubusercontent.com/Camto/Lad/master/Images/bible.png"
autoresponses = get_json("autoresponses.json")
quotes = get_json("bible quotes.json")
dinos = get_json("dinos.json")
pars = get_json("pars.json")
to_wiki_link = lambda s: "https://en.wikipedia.org/wiki/" + s

client = commands.Bot(command_prefix = "l.")

client.remove_command("help")

@client.event
async def on_ready():
	activity = discord.Game(name = "l.help", type = 3)
	await client.change_presence(status = discord.Status.online, activity = activity)
	print("Logged in")

# Show command descriptions.
@client.command()
async def help(ctx):
	await ctx.send(embed = discord.Embed(
		title = "Commands",
		description = "This bot's prefix is ``l.``",
		color = embed_color)
		.add_field(name = "help", value = "Show this message.", inline = False)
		.add_field(name = "bible", value = "Returns a random bible verse.", inline = False)
		.add_field(name = "ping", value = "Responds with pong.", inline = False)
		.add_field(name = "say", value = "Make the bot say something.", inline = False)
		.add_field(name = "dino", value = "Use `l.dino` for a random dinosaur, `l.dino <dinosuar name here>` to find the dinosaur with that name.", inline = False))

# Ping command to check users ping.
@client.command()
async def ping(ctx):
	await ctx.send(embed = discord.Embed(
		title = "Pong!",
		description = f"Hey, {ctx.message.author.mention}, your ping is ``{round(client.latency * 1000)}`` ms.",
		color = embed_color))

# Starting the bible study.
@client.command()
async def bible(ctx):
	quote = random.choice(quotes)
	await ctx.send(embed = discord.Embed(
		description = quote["text"],
		color = embed_color)
		.set_author(
			name = quote["location"],
			icon_url = bible_icon))

# Process dino related requests.
@client.command()
async def dino(ctx, *args):
	if len(args) == 0:
		dino = random.choice(dinos)
	else:
		dino = process.extractOne(args[0], dinos)[0]
	
	await ctx.send(embed = discord.Embed(
		title = dino.replace("_", " "),
		url = to_wiki_link(dino),
		description = pars[dino],
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

client.run(get_json("auth.json")["token"])