import discord
from discord.ext import commands
import utils

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def user(self, ctx, member : discord.Member=None):
        if member is None:
            member = ctx.author

        fields = [("ID", member.id, True),
                ("Top role", member.top_role.mention, True),
                ("Bot", member.bot, True),
                ("Created At", member.created_at.strftime("%d/%m/%Y"), True),
                ("Joined At", member.joined_at.strftime("%d/%m/%Y"), True),
                ("Boosted", bool(member.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed = discord.Embed(
            title = "User Info",
            color = utils.embed_color).set_image(url=member.avatar_url))

def setup(client):
    client.add_cog(User(client))