import discord
from discord.ext import commands

class Other(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Other ready.')

    @commands.command(aliases = ['pp'])
    async def get_profile_pic(self, ctx, user: discord.User):
        await ctx.send(user.avatar_url)

def setup(client):
    client.add_cog(Other(client))