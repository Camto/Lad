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
		if utils.get_setting(ctx.guild, "feedback"):
			await self.channel.send(embed = discord.Embed(
				color = utils.embed_color)
				.add_field(name = "Feedback", value = arg, inline = False)
				.add_field(name = "Username", value = f"{ctx.author.name}#{ctx.author.discriminator}", inline = False)
				.add_field(name = "User ID", value = ctx.author.id, inline = False)
				.add_field(name = "Server ID", value = ctx.guild.id if ctx.guild else "DMs", inline = False)
				.add_field(name = "Respond to", value = f"{ctx.channel.id} {ctx.message.id}" if ctx.guild else "DMs", inline = False))
			await ctx.send("Feedback recieved!")
		else:
			await ctx.send(embed = utils.command_disabled)
	
	@commands.command()
	async def fb_respond(self, ctx, *, args):
		chnl_id, msg_id, content = args.lstrip().split(None, 2)
		chnl_id, msg_id = int(chnl_id), int(msg_id)
		msg = await self.client.get_channel(chnl_id).fetch_message(msg_id)
		await msg.reply(content)
		await ctx.send("Alright, sent response.")

def setup(client):
	client.add_cog(Feedback(client))