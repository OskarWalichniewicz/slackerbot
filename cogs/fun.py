import discord
from discord.ext import commands
from reddit import *
from webscraping import webscrap_joke


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Fun ready.')

    """
    When meme command is called,
    it calles get_meme command (from reddit.py)
    returns embed with meme title and an image.
    """
    @commands.command()
    async def meme(self, ctx):
        title, upvotes, img = get_meme()
        embed_meme = discord.Embed(
            title=title,
            colour=discord.Color.blurple()
        )
        embed_meme.set_image(url=img)
        embed_meme.set_footer(text="Upvotes: {}".format(upvotes))
        print('[COMMAND][MEME] {} memes left.'.format(str(len(memes))))
        await ctx.send(embed=embed_meme)

    """
    """
    @commands.command()
    async def joke(self, ctx):
        joke = webscrap_joke()
        await ctx.send(joke)


def setup(client):
    client.add_cog(Fun(client))