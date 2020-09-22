import discord
from discord.ext import commands
from reddit import *

class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Memes ready.')

    """
    """
    @commands.command()
    async def meme(self, ctx):
        title, upvotes, img = get_meme()
        embed_meme = discord.Embed(
                    title = title,
                    colour = discord.Color.blurple()
                )
        embed_meme.set_image(url = img)
        embed_meme.set_footer(text = "Upvotes: {}".format(upvotes))
        print('[COMMAND][MEME] {} memes left.'.format(str(len(memes))))
        await ctx.send(embed=embed_meme)

def setup(client):
    client.add_cog(Memes(client))