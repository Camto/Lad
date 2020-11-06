import discord
from discord.ext import commands
import utils

import json

import yaml

on_strs = ["yes", "y", "true", "t", "1", "enable", "on"]
off_strs = ["no", "n", "false", "f", "0", "disable", "off"]

default_settings = {
	k: v["default"]
	for k, v in utils.options.items()}

# Change server settings.
class Settings(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(name = "settings")
	async def settings_cmd(self, ctx, *, args = ""):
		args = args.lstrip().split(None, 1)
		
		if ctx.message.author.guild_permissions.administrator:
			# If an option is being changed.
			
			if len(args) >= 2:
				guild_id = ctx.guild.id
				
				# Make sure server is in settings database.
				guild_in_db = await utils.db.fetch(
					"select * from settings where guild_id = $1",
					str(guild_id))
				
				if not guild_in_db:
					await utils.db.execute(f"""
						insert into settings
							(guild_id)
						values
							($1)""", str(guild_id))
					print(f"Server {ctx.guild.name} ({guild_id}) has been added to the settings database.")
				
				# Actually change the options.
				
				option = args[0]
				val = args[1]
				if option in utils.option_names:
					opt_type = utils.options[option]["type"]
					
					if opt_type == "bool":
						if val.lower() in on_strs or val.lower() in off_strs:
							val = val.lower() in on_strs
							set_msg = f"Turned {option} {'on' if val else 'off'}."
						else:
							return await ctx.send(embed = discord.Embed(
								description = f"{val} is not a valid value for {option}, use on or off.",
								color = utils.embed_color)
								.set_author(
									name = "Invalid Value",
									icon_url = utils.icons["settings"]))
					elif opt_type == "integer":
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
					elif opt_type == "text":
						set_msg = f'Set {option} to "{val}".'
					elif opt_type == "json":
						if val.startswith("```"): val = val[3:]
							if val.startswith("yaml"): val = val[4:]
							elif val.startswith("yml"): val = val[3:]
							if val.endswith("```"): val = val[:-3]
						
						try:
							val = yaml.safe_load(val)
						except:
							return await ctx.send(embed = discord.Embed(
								description = "The YAML sent wasn't valid.",
								color = utils.embed_color)
								.set_author(
									name = "Invalid Value",
									icon_url = utils.icons["settings"]))
						
						set_msg = f"Changed {option}."
					
					if opt_type == "json": db_val = json.dumps(val)
					else: db_val = val
					
					await utils.db.execute(f"""
						update settings
						set {option} = $1
						where guild_id = $2""",
						db_val, str(guild_id))
					
					await ctx.send(embed = discord.Embed(
						description = set_msg,
						color = utils.embed_color)
						.set_author(
							name = "Changed Setting",
							icon_url = utils.icons["settings"]))
					
					if guild_id not in utils.settings:
						utils.settings[guild_id] = default_settings
					utils.settings[guild_id][option] = val
				else:
					await ctx.send(embed = discord.Embed(
						description = f"{option} is not an option that can be toggled.",
						color = utils.embed_color)
						.set_author(
							name = "Invalid Option",
							icon_url = utils.icons["settings"]))
			else:
				await ctx.send(embed = utils.embeds["settings more args"])
		else:
			await ctx.send(embed = utils.embeds["settings not admin"])

def setup(client):
	client.add_cog(Settings(client))