import discord
from discord.ext import commands

import utils
from random import randint  

class Roll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, *cmd):
        if len(cmd) == 0:
            await ctx.send(embed = discord.Embed(
                description = "Roll using DnD format (Example: 1d20)",
                color = utils.embed_color)
                .set_footer(text = f'Requested by {ctx.message.author}.'))

        def d(sides):
            return randint(1, sides)

        def roll(n, sides):
            return tuple(d(sides) for _ in range(n))

        amount, side = cmd[0].split("d")

        dice = roll(int(amount), int(side))

        try:
            await ctx.send(embed = discord.Embed(
                title = ":slot_machine: Rolling dice... :slot_machine:",
                description = f"Your destiny is... ``{dice, sum(dice)}``",
                color=utils.embed_color)
                .set_footer(text = f'Requested by {ctx.message.author}.'))
        except:
            await ctx.send(embed = discord.Embed(
                description = "Your input is too big to calculate",
                color = utils.embed_color)
                .set_footer(text = f'Requested by {ctx.message.author}.'))

def setup(client):
    client.add_cog(Roll(client))