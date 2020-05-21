import discord
from discord.ext import commands

import utils

# Change server settings.
class Settings(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(name = "settings")
	async def settings_cmd(self, ctx, *args):
		if ctx.message.author.guild_permissions.administrator:
			# If an option is being changed.
			
			if len(args) >= 2:
				guild_id = ctx.guild.id
				
				# Make sure server is in settings database.
				guild_in_db = await (await utils.db.execute(
					"SELECT * FROM settings WHERE guild_id = ?",
					(guild_id,))).fetchone()
				
				if not guild_in_db:
					await utils.db.execute("""
						INSERT INTO settings
							(guild_id, autoresponses, bible, dino, ping, say)
						VALUES
							(?, 1, 1, 1, 1, 1)""",
						(guild_id,))
					await utils.db.commit()
					print(f"Server {ctx.guild.name} ({guild_id}) has been added to the settings database.")
				
				# Actually change the options.
				
				if args[0] in utils.option_names:
					if args[1] == "on" or args[1] == "off":
						is_yes = args[1] == "on"
						
						await utils.db.execute(f"""
							UPDATE settings
							SET {args[0]} = ?
							WHERE guild_id = ?""",
							(1 if is_yes else 0, guild_id))
						await utils.db.commit()
						await ctx.send(embed = discord.Embed(
							description = f"Turned {args[0]} {'on' if is_yes else 'off'}.",
							color = utils.embed_color)
							.set_author(
								name = "Changed Setting",
								icon_url = utils.icons["settings"]))
						
						if guild_id not in utils.settings:
							utils.settings[guild_id] = {"autoresponses": 1}
						utils.settings[guild_id][args[0]] = 1 if is_yes else 0
					else:
						await ctx.send(embed = discord.Embed(
							description = f"{args[1]} is not a valid value, use on or off.",
							color = utils.embed_color)
							.set_author(
								name = "Invalid Value",
								icon_url = utils.icons["settings"]))
				else:
					await ctx.send(embed = discord.Embed(
						description = f"{args[0]} is not an option that can be toggled.",
						color = utils.embed_color)
						.set_author(
							name = "Invalid Option",
							icon_url = utils.icons["settings"]))
			else:
				await ctx.send(embed = discord.Embed(
					description = "Not enough arguments were given to change an option, for help with `l.settings`, please use `l.help settings`.",
					color = utils.embed_color)
					.set_author(
						name = "Not Enough Arguments",
						icon_url = utils.icons["settings"]))
		else:
			await ctx.send(embed = discord.Embed(
				description = "You're not an admin, you can't access the settings.",
				color = utils.embed_color)
				.set_author(
					name = "Denied Access",
					icon_url = utils.icons["settings"]))

def setup(client):
	client.add_cog(Settings(client))