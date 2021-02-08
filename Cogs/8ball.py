import discord
from discord.ext import commands
import utils

import random
import asyncio

responses = list(map(
	lambda s: discord.Embed(description = s, color = utils.embed_color),
	[
		":smiley: It is certain.",
		":smiley: It is decidedly so.",
		":smiley: Without a doubt.",
		":smiley: Yes – definitely.",
		":smiley: You may rely on it.",
		":smiley: As I see it, yes.",
		":smiley: Most likely.",
		":smiley: Outlook good.",
		":smiley: Yes.",
		":smiley: Signs point to yes.",
		
		":woozy_face: Reply hazy, try again.",
		":woozy_face: Ask again later.",
		":woozy_face: Better not tell you now.",
		":woozy_face: Cannot predict now.",
		":woozy_face: Concentrate and ask again.",
		
		":no_entry_sign: Don't count on it.",
		":no_entry_sign: My reply is no.",
		":no_entry_sign: My sources say no.",
		":no_entry_sign: Outlook not so good.",
		":no_entry_sign: Very doubtful."
	]
))

class Cmd_8ball(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(name = "8ball")
	async def cmd_8ball(self, ctx, *_):
		if utils.get_setting(ctx.guild.id, "b"):
			async with ctx.typing():
				await ctx.send(":8ball: **Divining your fate...**")
				await asyncio.sleep(2)
				await ctx.send(embed = random.choice(responses))
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Cmd_8ball(client))