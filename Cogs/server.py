import discord
from discord.ext import commands
import utils

class Server(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def server(self, ctx):
		embed = (discord.Embed(
			title="Server information",
			color = utils.embed_color)
			.set_thumbnail(url = ctx.guild.icon_url))
		
		#statuses = [
		#	len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
		#	len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
		#	len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
		#	len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
		
		fields = [
			("ID", ctx.guild.id),
			("Owner", ctx.guild.owner),
			("Region", ctx.guild.region),
			("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")),
			("Members", len(ctx.guild.members)),
			("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members)))),
			("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members)))),
			("Banned members", len(await ctx.guild.bans())),
			# ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}"),
			("Text channels", len(ctx.guild.text_channels)),
			("Voice channels", len(ctx.guild.voice_channels)),
			("Categories", len(ctx.guild.categories)),
			("Roles", len(ctx.guild.roles)),
			("Invites", len(await ctx.guild.invites())),
			("\u200b", "\u200b")]
		
		for name, value in fields:
			print(f"Did field {name}")
			embed.add_field(name = name, value = value, inline = True)
		
		await ctx.send(embed = embed)

def setup(client):
	client.add_cog(Server(client))