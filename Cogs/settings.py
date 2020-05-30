import discord
from discord.ext import commands

import utils

on_strs = ["yes", "y", "true", "t", "1", "enable", "on"]
off_strs = ["no", "n", "false", "f", "0", "disable", "off"]

insert_query = f"""
	insert into settings
		(guild_id, {",".join(list(map(str, utils.option_names)))})
	values
		(?, {",".join(list(map(
			lambda opt: str(utils.options[opt]["default"]),
			utils.option_names)))})
"""

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
					"select * from settings where guild_id = ?",
					(guild_id,))).fetchone()
				
				if not guild_in_db:
					await utils.db.execute(insert_query, (guild_id,))
					await utils.db.commit()
					print(f"Server {ctx.guild.name} ({guild_id}) has been added to the settings database.")
				
				# Actually change the options.
				
				option = args[0]
				val = args[1]
				if option in utils.option_names:
					type = utils.options[option]["type"]
					
					if type == "bool":
						if val.lower() in on_strs or val.lower() in off_strs:
							is_yes = val.lower() in on_strs
							val = 1 if is_yes else 0
							set_msg = f"Turned {option} {'on' if is_yes else 'off'}."
						else:
							return await ctx.send(embed = discord.Embed(
								description = f"{val} is not a valid value for {option}, use on or off.",
								color = utils.embed_color)
								.set_author(
									name = "Invalid Value",
									icon_url = utils.icons["settings"]))
					elif type == "integer":
						try:
							val = str(val)
							set_msg = f"Set {option} to {val}."
						except:
							return await ctx.send(embed = discord.Embed(
								description = f"{val} is not a valid value for {option}, use a whole number.",
								color = utils.embed_color)
								.set_author(
									name = "Invalid Value",
									icon_url = utils.icons["settings"]))
					elif type == "text":
						set_msg = f'Set {option} to "{val}".'
					
					await utils.db.execute(f"""
						update settings
						set {option} = ?
						where guild_id = ?""",
						(val, guild_id))
					await utils.db.commit()
					
					await ctx.send(embed = discord.Embed(
						description = set_msg,
						color = utils.embed_color)
						.set_author(
							name = "Changed Setting",
							icon_url = utils.icons["settings"]))
					
					if guild_id not in utils.settings:
						utils.settings[guild_id] = {}
					utils.settings[guild_id][option] = val
				else:
					await ctx.send(embed = discord.Embed(
						description = f"{option} is not an option that can be toggled.",
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