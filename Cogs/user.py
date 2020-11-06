import discord
from discord.ext import commands
import utils

class User(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def user(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		
		embed = (discord.Embed(
			title = "User Info",
			color = utils.embed_color)
			.set_image(url = member.avatar_url))
		
		fields = [
			("ID", member.id),
			("Top role", member.top_role.mention),
			("Bot", member.bot),
			("Created At", member.created_at.strftime("%b. %d, %Y")),
			("Joined At", member.joined_at.strftime("%b. %d, %Y")),
			("Boosted", bool(member.premium_since))]
		
		for name, value in fields:
			embed.add_field(name = name, value = value, inline = True)
		
		await ctx.send(embed = embed)

def setup(client):
	client.add_cog(User(client))