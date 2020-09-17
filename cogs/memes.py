# import discord
# from discord.ext import commands
# from webscraping import webscrap_9gag

# class Memes(commands.Cog):

#     def __init__(self, client):
#         self.client = client

#     @commands.Cog.listener()
#     async def on_ready(self):
#         print('[COG] Memes ready.')

#     @commands.command(aliases = ['9gag'])
#     async def _9gag(self, ctx, *text):
#         post_url, gag_url, title = webscrap_9gag()
#         embed_9gag = discord.Embed(
#                     title = str(title),
#                     colour = discord.Color.blue()
#                 )
#         embed_9gag.set_image(url = post_url)
#         await ctx.send(embed=embed_9gag)

# def setup(client):
#     client.add_cog(Memes(client))