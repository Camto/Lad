import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import json

def get_json(filename):
	file = open(filename)
	data = json.load(file)
	file.close()
	return data

embed_color = 0xe07bb8
autoresponses = get_json("autoresponses.json")
quotes = get_json("bible quotes.json")

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
		.add_field(name = "say", value = "Make the bot say something.", inline = False))

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
		title = quote["location"],
		description = quote["text"],
		color = embed_color))

# Response system.
@client.event
async def on_message(msg):
	if msg.author.name != "Lad":
		content = msg.content
		
		if content.startswith("l."):
			# The say command is actually here.
			if content.startswith("l.say"):
				return await msg.channel.send(content[5:].lstrip())
			else:
				return await client.process_commands(msg)
		
		text = content.lower()
		for pair in autoresponses:
			for keyword in pair["keywords"]:
				if keyword in text:
					return await msg.channel.send(random.choice(pair["responses"]))

client.run(get_json("auth.json")["token"])