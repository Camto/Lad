import discord
from discord.ext import commands

import utils

# Show command descriptions.
class Help(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def help(self, ctx, *cmd):
		if len(cmd) == 0:
			await ctx.send(embed = discord.Embed(
			title = "Commands",
			description = "This bot's prefix is ``l.``",
			color = utils.embed_color)
			.set_footer(
				text = "https://github.com/Camto/Lad",
				icon_url = utils.icons["github"])
			.add_field(name = "help", value = "Show this message.", inline = False)
			.add_field(name = "ping", value = "Responds with pong.", inline = False)
			.add_field(name = "roll", value = "Roll a dice DnD style.", inline = False)
			.add_field(name = "say", value = "Make the bot say something.", inline = False)
			.add_field(name = "ascii", value = "Returns your message in ASCII art!", inline = False)
			.add_field(name = "reddit", value = "Sends a link to a random reddit post.", inline = False)
			.add_field(name = "search", value = "Get a list of Google search results.", inline = False)
			.add_field(name = "bible", value = "Returns a random bible verse. For verses do l.help bible", inline = False)
			.add_field(name = "bitcoin", value = "Get the current price of bitcoin with a wide range of currencies to choose from", inline = False)
			.add_field(name = "dino", value = "Use `l.dino` for a random dinosaur, `l.dino <dinosaur name here>` to find the dinosaur with that name.", inline = False))
		elif cmd[0] == "bible":
			await ctx.send(embed = discord.Embed(
			title = "To search type NUMBER first; followed by BOOK",
			color = utils.embed_color)
			.set_author(
				name = "Bible Help",
				icon_url = utils.icons["bible"])
			.add_field(name = "Matthew", value = "5:9 | 28:19 | 5:28 | 6:5 | 21:18-22 | 11:30 | 12:33 | 18:8 | 18:9", inline = False)
			.add_field(name = "Leviticus", value = "19:19 | 19:27 | 9:10 | 15:19-20 | 25:44-46 | 21:17-23", inline = False)
			.add_field(name = "Deuteronomy", value = "22:28-29 | 25:11-1 | 23:1 | 31:8 | 33:27 | 25:11-12", inline = False)
			.add_field(name = "Psalms", value = "23:1-6 | 46:1-3 | 9:9-10 | 34:10b | 32:7-8", inline = False)
			.add_field(name = "Exodus", value = "8:1-14 | 21:7-8 | 15:2 | 33:14 | 23:19", inline = False)
			.add_field(name = "Kings", value = "6:28-29 | 2:23-25 | 23:20-25", inline = False)
			.add_field(name = "John", value = "3:3 | 14:14 | 14:6 | 3:16", inline = False)
			.add_field(name = "Chronicles", value = "21:14-15 | 16:11", inline = False)
			.add_field(name = "Ephesians", value = "2:8 | 6:5 | 5:4", inline = False)
			.add_field(name = "Proverbs", value = "18:10 | 15:4", inline = False)
			.add_field(name = "Isaiah", value = "41:10 | 26:3-4", inline = False)
			.add_field(name = "Timothy", value = "6:6-9 | 3:16", inline = False)
			.add_field(name = "Luke", value = "16:18 | 3:11", inline = False)
			.add_field(name = "Peter", value = "5:8 | 2:18", inline = False)
			.add_field(name = "Numbers", value = "31:17-18", inline = False)
			.add_field(name = "Reverend", value = "21:8", inline = False)
			.add_field(name = "Nehemiah", value = "8:10", inline = False)
			.add_field(name = "Ezekiel", value = "47:11", inline = False)
			.add_field(name = "Hebrews", value = "12:1", inline = False)
			.add_field(name = "Romans", value = "3:23", inline = False)
			.add_field(name = "Genesis", value = "1:1", inline = False)
			.add_field(name = "Samuel", value = "6:19", inline = False))
		elif cmd[0] == "settings":
			option_list = "\n\n".join(map(
				lambda option: f"`{option[0]}`: {option[1]['descr']}",
				utils.options.items()))
			
			await ctx.send(embed = discord.Embed(
				description = f"""To change an option, use `l.settings <option name> <value>` <value> can be on or off.

	{option_list}""",
				color = utils.embed_color)
				.set_author(
					name = "Settings Help",
					icon_url = utils.icons["settings"]))

def setup(client):
	client.add_cog(Help(client))