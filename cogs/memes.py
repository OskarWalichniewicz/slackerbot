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
        embed_9gag = discord.Embed(
                title = title,
                description = post_url,
                colour = discord.Color.blue()
            )
        embed_9gag.set_footer(text = 'Link to gag: ' + str(gag_url))
        await ctx.send(embed=embed_9gag)

def setup(client):
    client.add_cog(Memes(client))