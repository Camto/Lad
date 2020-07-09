import art
import discord
from discord.ext import commands

import utils


# Process dino related requests.
class Ascii(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ascii(self, ctx, *, arg):
        if utils.get_setting(ctx.guild.id, "ascii"):
            await ctx.send(f"```\n{art.text2art(arg)}\n```")
        else:
            await ctx.send(embed=utils.command_disabled)


def setup(client):
    client.add_cog(Ascii(client))