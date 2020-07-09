import discord
from discord.ext import commands

import utils


# Process dino related requests.
class Say(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, *, arg="\u200b"):
        if utils.get_setting(ctx.guild.id, "say"):
            await ctx.send(arg)
            await ctx.message.delete()
        else:
            await ctx.send(embed=utils.command_disabled)


def setup(client):
    client.add_cog(Say(client))