import discord
from discord.ext import commands

"""
Sends screenshots to corresponding commands.
"""
class Memories(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Memories ready.')

    @commands.command()
    async def akcent(self, ctx):
        await ctx.send('https://prnt.sc/udv05c')

    @commands.command()
    async def stonelia(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/364712407601512450/709413405131407380/Screenshot_794.png?width=686&height=515 \n https://image.prntscr.com/image/pUq5QnZ9Ti_xDzfgi6oRkw.png ')

    @commands.command()
    async def stonement(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/364712407601512450/753284032036470824/unknown.png?width=728&height=515')

    @commands.command()
    async def pam(self, ctx):
        await ctx.send('https://media.discordapp.net/attachments/364712407601512450/752975692966264902/Screenshot_797.png?width=684&height=515')

    @commands.command()
    async def pupinka(self, ctx):
        await ctx.send('https://cdn.discordapp.com/attachments/364712407601512450/399218303739887617/WoWScrnShot_010618_160818.jpg')


def setup(client):
    client.add_cog(Memories(client))