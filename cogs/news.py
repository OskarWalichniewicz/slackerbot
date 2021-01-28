import discord
from discord.ext import commands
from webscraping import *


class News(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] News ready.')


def setup(client):
    client.add_cog(News(client))


async def top_news_from_world():
    top_news_list = webscrap_top_news()
    embed_news = discord.Embed(
        title='Top news from around the world!',
        colour=discord.Color.orange()
    )

    embed_names = [':flag_rs: Serbia :flag_rs:', ':flag_it: Italy :flag_it:',
                   ':flag_nl: Netherlands :flag_nl:', ':flag_pl: Poland :flag_pl:', ':flag_ro: Romania :flag_ro:']

    for i in range(len(embed_names)):
        embed_news.add_field(
            name=embed_names[i], value=top_news_list[i][0] + "\n" + top_news_list[i][1], inline=False)

    return embed_news
