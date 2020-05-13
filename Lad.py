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

autoresponses = get_json("autoresponses.json")
quotes = get_json("bible quotes.json")

client = commands.Bot(command_prefix = "L.", description="tba")

@client.event
async def on_ready():
	activity = discord.Game(name="L.bible", type=3)
	await client.change_presence(status=discord.Status.online, activity=activity)
	print("Logged in")

# Ping command to check users ping 
@client.command()
async def ping(ctx):
	await ctx.send(f"Pong! Hey, {ctx.message.author.mention}, your ping is ``{round(client.latency * 1000)}`` ms")

# Starting the bible study
# Make the bot repeat something.
@client.command()
async def say(ctx, text):
	await ctx.send(text)

@client.command()
async def bible(ctx):
	await ctx.send(random.choice(quotes))

# Response system.
@client.event
async def on_message(msg):
	if msg.author.name != "Lad":
		content = msg.content
		
		if content.startswith("L."):
			await client.process_commands(msg)
			return
		
		text = "".join(content.split()).lower()
		for pair in autoresponses:
			for keyword in pair["keywords"]:
				if keyword in text:
					await msg.channel.send(random.choice(pair["responses"]))
					return

client.run(get_json("auth.json")["token"])