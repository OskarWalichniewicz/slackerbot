import discord
from discord.ext import commands
from webscraping import *


class News(commands.Cog):

    COUNTRIES_CODES_DICT = {'rs': 'Serbia',
                            'it': 'Italy',
                            'nl': 'Netherlands',
                            'pl': 'Poland',
                            'ro': 'Romania'}

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] News ready.')

    @commands.command()
    async def news(self, ctx, *text):
        if len(text) > 1:  # if more than 1 word was typed after .news (e.g. .word bonobo bonobo)
            await ctx.send("stupid bonobo, it's .news (country_code), e.g. .news nl")
            return None

        text = text[0].lower()

        if len(text) != 2:  # if it has more than 2 letters
            await ctx.send("Dude that's not a country code I asked for.")
            return None

        # if its 2 letters but its not in dict
        elif len(text) == 2 and text not in self.COUNTRIES_CODES_DICT:
            await ctx.send("This country either doesn't exist, or we don't care, sorry.")
            return None

        else:  # is 2 letters and in dict
            if text == 'sr':
                text = 'rs'

            try:
                top_news_list = webscrap_top_news_from_country(text)

                embed_news = discord.Embed(
                    title='Top news from {}!'.format(
                        self.COUNTRIES_CODES_DICT[text]),
                    colour=discord.Color.orange()
                )

                for news in top_news_list:
                    embed_news.add_field(
                        name=news[0], value=news[1], inline=False)

                await ctx.send(embed=embed_news)

            except:
                print('[.NEWS] Error -> .news {} used'.format(text))


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

    embed_news.set_footer(
        text="For more news from your country, try .news (country_code)\nAvailable codes: rs, it, nl, pl, ro")

    return embed_news
