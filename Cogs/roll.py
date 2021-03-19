import discord
from discord.ext import commands
import utils

from random import randint

class Roll(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(aliases=["r"])
	async def roll(self, ctx, *cmd):
		if utils.get_setting(ctx.guild.id, "roll"):
			try:
				amount, side = (
					map(int, cmd[0].split("d"))
					if "d" in cmd[0]
					else (1, int(cmd[0])))
				
				if amount > 10000 or side > 10000:
					return await ctx.send(embed = utils.embeds["roll error"])
				
				dice = [randint(1, side) for _ in range(amount)]
				str_dice = map(str, dice)
				final_dice = (
					f"{' + '.join(str_dice)} = {sum(dice)}"
					if amount > 1
					else str(sum(dice)))
				
				try:
					await ctx.send(embed = discord.Embed(
						title = ":game_die: Rolling dice...",
						description = f"Your destiny is... ``{final_dice}``",
						color = utils.embed_color).set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url))
				except:
					await ctx.send(embed = discord.Embed(
						title = ":game_die: Rolling dice...",
						description = f"Your destiny is... ``{sum(dice)}``",
						color = utils.embed_color)
						.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url))
			except:
				await ctx.send(embed = utils.embeds["roll more args"])
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Roll(client))