import asyncio
import os
import random
import string

import discord
import requests
from discord.ext import commands
from PIL import Image
from requests.auth import HTTPBasicAuth

import utils


class Convert(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def convert(self, ctx, *args):
        if len(args) == 0 or len(args) == 1:
            await ctx.send(embed=discord.Embed(
                title=":no_entry_sign: Error",
                description=f"Post an image in the chat, copy the link address (right click it) and `l.convert <extension> <link>`",
                color=utils.embed_color)
                .set_footer(text=f'Requested by {ctx.message.author}.'))
        else:
            url = args[1]
            extension = args[0]
            temp_file = ''.join(random.choice(string.ascii_lowercase)
                                for i in range(10))

            try:
                r = requests.get(url, allow_redirects=True)

                open(f'{temp_file}', 'wb').write(r.content)
                # await ctx.send(embed=discord.Embed(
                #    title=":white_check_mark: File Downloaded",
                #    color=utils.embed_color)
                #    .set_footer(text=f'Requested by {ctx.message.author}.'))
            except:
                await ctx.send(embed=discord.Embed(
                    title=":bangbang: Error while downloading file | Try another link",
                    color=utils.embed_color)
                    .set_footer(text=f'Requested by {ctx.message.author}.'))
            else:
                im = Image.open(temp_file)
                im.save(f'{temp_file}.{extension}', quality=100)
                nfile = discord.File(
                    f'{temp_file}.{extension}', filename=f"Converted File.{extension}")
                await ctx.send(file=nfile, embed=discord.Embed(
                    title=":white_check_mark: File Successfully Converted!",
                    color=utils.embed_color)
                    .set_footer(text=f'Requested by {ctx.message.author}.'))
            finally:
                if os.path.isfile(f'{temp_file}.{extension}'):
                    os.remove(f'{temp_file}.{extension}')
                if os.path.isfile(temp_file):
                    os.remove(temp_file)


def setup(client):
    client.add_cog(Convert(client))