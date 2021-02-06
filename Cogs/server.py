import discord
from discord.ext import commands
import utils

class Server(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def server(self, ctx):
		if utils.get_setting(ctx.guild.id, "server"):
			embed = (discord.Embed(
				title="Server information",
				color = utils.embed_color)
				.set_thumbnail(url = ctx.guild.icon_url)
				.set_footer(text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.avatar_url))
			
			fields = [
				("Owner", str(ctx.guild.owner)),
				("Region", ctx.guild.region),
				("Created at", ctx.guild.created_at.strftime("%d/%m/%Y")),
				("Members", str(ctx.guild.member_count)),
				("Boosters", str(ctx.guild.premium_subscription_count)),
				("Roles", len(ctx.guild.roles)),
				("Text channels", len(ctx.guild.text_channels)),
				("Voice channels", len(ctx.guild.voice_channels)),
				("Categories", len(ctx.guild.categories))]
			
			for name, value in fields:
				embed.add_field(name = name, value = value, inline = True)
			
			await ctx.send(embed = embed)
		else:
			await ctx.send(embed = utils.command_disabled)

def setup(client):
	client.add_cog(Server(client))