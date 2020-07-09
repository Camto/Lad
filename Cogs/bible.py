import asyncio
import random

import discord
from discord.ext import commands
from fuzzywuzzy import fuzz, process

import utils

quotes = utils.get_yaml("bible quotes")

reload_emoji = utils.emojis["reload"]

# Starting the bible study.
class Bible(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bible(self, ctx, *args):
        if utils.get_setting(ctx.guild.id, "bible"):
            if len(args) != 0:
                quote = process.extractOne(
                    args[0],
                    quotes,
                    scorer=fuzz.partial_token_sort_ratio)[0]
                await ctx.send(embed=bible_to_embed(quote))
            else:
                await utils.menus.reload(self.client, ctx, bible_menu)
        else:
            await ctx.send(embed=utils.command_disabled)


async def bible_menu(_):
    while True:
        yield bible_to_embed(random.choice(quotes))


def bible_to_embed(quote):
    return (discord.Embed(
            description=quote["text"],
            color=utils.embed_color)
            .set_author(
        name=quote["location"],
        icon_url=utils.icons["bible"]))


def setup(client):
    client.add_cog(Bible(client))