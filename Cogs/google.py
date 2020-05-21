import discord
from discord.ext import commands

from google import google
import utils

class Google(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx, *args):
        num_page = 1
        search_results = google.search(args[0], num_page)
        if len(args) >= 1:
            for result in search_results:
                await ctx.send(embed = discord.Embed(
                    title = "Google Search",
                    description = result.description,
                    color = utils.embed_color)
                    .set_footer(
                        text =  result.description.google_link,
                        icon_url = utils.icons["google"]))

def setup(client):
    client.add_cog(Google(client))