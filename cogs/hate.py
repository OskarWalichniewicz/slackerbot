import discord
from discord.ext import commands

class Hate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ignios(self, ctx):
        await ctx.send('Fuck Ignios')

def setup(client):
    client.add_cog(Hate(client))