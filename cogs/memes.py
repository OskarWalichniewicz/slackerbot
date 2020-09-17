import discord
from discord.ext import commands
from webscraping import webscrap_9gag

class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Memes ready.')

    @commands.command(aliases = ['9gag'])
    async def _9gag(self, ctx, *text):
        title, post_url, gag_url = webscrap_9gag()
        _9gag_string = "title\n" + str(post_url)
        await ctx.send(_9gag_string)

def setup(client):
    client.add_cog(Memes(client))