import discord
from discord.ext import commands
import utils

class Feedback(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		self.channel = self.client.get_channel(int(utils.master_settings["feedback"]))
	
	@commands.command()
	async def feedback(self, ctx, *, arg):
		if utils.get_setting(ctx.guild.id, "feedback"):
			await self.channel.send(embed = discord.Embed(
				title = "Feedback",
				description = arg,
				color = utils.embed_color)
				.set_footer(text = f"Feedback submitted by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) in server {ctx.guild.name} ({ctx.guild.id})"))
			await ctx.send("Feedback recieved!")
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Feedback(client))