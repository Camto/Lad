from random import randint

import discord
from discord.ext import commands

import utils

class Roll(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def roll(self, ctx, *cmd):
		try:
			amount, side = (
				map(int, cmd[0].split("d"))
				if "d" in cmd[0]
				else (1, int(cmd[0])))
			
			dice = tuple(randint(1, side) for _ in range(amount))
			str_dice = map(str, dice)
			final_dice = (
				f"{' + '.join(str_dice)} = {sum(dice)}"
				if amount > 1
				else str(sum(dice)))
			
			try:
				if sum(dice) >= 250000:
					await ctx.send(embed=discord.Embed(
						description="Your input is too big to calculate",
						color=utils.embed_color)
						.set_footer(text=f'Requested by {ctx.message.author}.'))
				else:
					await ctx.send(embed=discord.Embed(
						title=":game_die: Rolling dice...",
						description=f"Your destiny is... ``{final_dice}``",
						color=utils.embed_color)
						.set_footer(text=f'Requested by {ctx.message.author}.'))
			except:
				await ctx.send(embed=discord.Embed(
					description="Your input is too big to calculate",
					color=utils.embed_color)
					.set_footer(text=f'Requested by {ctx.message.author}.'))
		except:
			await ctx.send(embed=discord.Embed(
				description="Roll using DnD rules (Example: 1d20)",
				color=utils.embed_color)
				.set_footer(text=f'Requested by {ctx.message.author}.'))


def setup(client):
	client.add_cog(Roll(client))