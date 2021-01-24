import discord
from discord.ext import commands
import utils

utils.master_settings["admins"] = list(map(int, utils.master_settings["admins"]))

# Reload all cogs.
class Reload(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def reload(self, ctx):
		if ctx.author.id in utils.master_settings["admins"]:
			content = "Reloading cogs:"
			msg = await ctx.send(content)
			
			i = 0
			for cog in utils.cogs_to_load:
				self.client.unload_extension(cog)
				self.client.load_extension(cog)
				content += f"\n\u200b  Reloading {cog}"
				i += 1
				if i == 5:
					i = 0
					await msg.edit(content = content)
			
			content += "\nDone"
			await msg.edit(content = content)

def setup(client):
	client.add_cog(Reload(client))