import random

import art
import discord
from discord.ext import commands

import utils


# The autoresponse system.
class On_Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if (
                msg.author.id != utils.lad_id and
                utils.get_setting(msg.guild.id, "autoresponses") and
                not msg.content.startswith("l.")):
            text = msg.content.lower()
            for pair in utils.get_setting(msg.guild.id, "autoresponse_file"):
                for keyword in pair["keywords"]:
                    if keyword in text:
                        return await msg.channel.send(random.choice(pair["responses"]))


def setup(client):
    client.add_cog(On_Message(client))