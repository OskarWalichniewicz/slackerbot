import discord
from discord.ext import commands
from word import *
from webscraping import *
from profanityfilter import ProfanityFilter

pf = ProfanityFilter()

"""
Checks if message author is not Awy by his ID.
returns boolean
"""


async def is_not_awy(ctx):
    return ctx.author.id != 245247289935921152


class Education(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Education ready.')

    @commands.command()
    async def rwiki(self, ctx):
        article_url, title, summary = webscrap_wikipedia()
        embed_wiki = discord.Embed(
            title=title, colour=discord.Color.green(), description=summary)
        embed_wiki.set_footer(
            text='Find out more here: {}'.format(article_url))
        await ctx.send(embed=embed_wiki)

    @commands.command()
    async def wiki(self, ctx, *, text):
        options = None
        try:
            article_url, title, summary = webscrap_wikipedia(text)
        except ValueError:
            options = webscrap_wikipedia(text)

        if options is not None:
            str_options = ""
            for option in options:
                str_options += option
                str_options += ", "
            await ctx.send("Did you mean: {}".format(str_options[:-2]))
            return 0

        if len(summary) > 2048:
            summary = summary[:2044]
            summary += "..."
        embed_wiki = discord.Embed(
            title=title, colour=discord.Color.green(), description=summary)
        embed_wiki.set_footer(
            text='Find out more here: {}'.format(article_url))
        await ctx.send(embed=embed_wiki)

    """
    When user calls word command with input (word),
    translates this word to all Slackers' languages (calling translate_word from word.py),
    searches for definitions (calling get_definitions from word.py)
    and embeds it.
    returns embed with searched word, definitions and translations to languages (as fields)
    """
    @commands.command()
    async def word(self, ctx, *text):
        try:
            if len(text) > 1:  # if more than 1 word was typed after .word (e.g. .word bonobo bonobo)
                await ctx.send("stupid bonobo, the command is called .word (singular) for a reason.")
                return None
            english_word = text[0]
            serbian_word_cyr, serbian_word_lat = translate_word(
                english_word, 'sr')
            serbian_word = str(serbian_word_cyr) + " / " + \
                str(serbian_word_lat)
            italian_word = translate_word(english_word, 'it')
            dutch_word = translate_word(english_word, 'nl')
            polish_word = translate_word(english_word, 'pl')
            romanian_word = translate_word(english_word, 'ro')

            def_string = get_definitions(english_word)

            if def_string == "":  # if there are no definitions to given word
                embed_word = discord.Embed(
                    title='{}'.format(english_word.upper()),
                    colour=discord.Color.orange()
                )
            else:
                embed_word = discord.Embed(
                    title='{}'.format(english_word.upper()),
                    description=def_string,
                    colour=discord.Color.orange()
                )

            embed_word.add_field(
                name=':flag_gb: English :flag_gb:', value=english_word, inline=False)
            embed_word.add_field(
                name=':flag_rs: Serbian :flag_rs:', value=serbian_word, inline=True)
            embed_word.add_field(
                name=':flag_it: Italian :flag_it:', value=italian_word, inline=False)
            embed_word.add_field(
                name=':flag_nl: Dutch :flag_nl:', value=dutch_word, inline=True)
            embed_word.add_field(
                name=':flag_pl: Polish :flag_pl:', value=polish_word, inline=False)
            embed_word.add_field(
                name=':flag_ro: Romanian :flag_ro:', value=romanian_word, inline=True)

            await ctx.send(embed=embed_word)

        except IndexError:  # If IndexError occurs
            print("[.WORD] IndexError")

    """
    Gets random word (calling get_random_word from word.py)
    rest as in @word command
    """
    @commands.command()
    async def rword(self, ctx):
        english_word = get_random_word()
        serbian_word_cyr, serbian_word_lat = translate_word(english_word, 'sr')
        serbian_word = str(serbian_word_cyr) + " / " + str(serbian_word_lat)
        italian_word = translate_word(english_word, 'it')
        dutch_word = translate_word(english_word, 'nl')
        polish_word = translate_word(english_word, 'pl')
        romanian_word = translate_word(english_word, 'ro')

        def_string = get_definitions(english_word)

        if def_string == "":
            embed_word = discord.Embed(
                title='{}'.format(english_word.upper()),
                colour=discord.Color.orange()
            )
        else:
            embed_word = discord.Embed(
                title='{}'.format(english_word.upper()),
                description=def_string,
                colour=discord.Color.orange()
            )

        embed_word.add_field(name=':flag_gb: English :flag_gb:',
                             value=english_word, inline=False)
        embed_word.add_field(name=':flag_rs: Serbian :flag_rs:',
                             value=serbian_word, inline=True)
        embed_word.add_field(name=':flag_it: Italian :flag_it:',
                             value=italian_word, inline=False)
        embed_word.add_field(name=':flag_nl: Dutch :flag_nl:',
                             value=dutch_word, inline=True)
        embed_word.add_field(name=':flag_pl: Polish :flag_pl:',
                             value=polish_word, inline=False)
        embed_word.add_field(name=':flag_ro: Romanian :flag_ro:',
                             value=romanian_word, inline=True)

        await ctx.send(embed=embed_word)

    """
    When user calls gimage command with input,
    it checks if the query is profanity (checked by ProfanityFilter), if its not
    calls webscrap_google_images (webscraping.py) passing user's query and 1 (so it returns only 1 image).
    returns image url (string)
    """
    @commands.command()
    async def gimage(self, ctx, *text):
        if pf.censor(str(text)) != str(text):
            await ctx.send('Slacker refuses to search for THAT. Please respect my poor eyes.')
            return None
        query = text
        img_url = webscrap_google_images(query, 1)
        for img in img_url:  # unwraps img_url (because it's a list)
            await ctx.send(img)

    """
    When user calls fact command,
    it calls webscrap_fact (webscraping.py),
    prettifies the output (sometimes it contains <em> </em>)
    and embeds it
    returns embed with fact (it's text) and an image.
    """
    @commands.command()
    async def fact(self, ctx):
        img_url, fact_descr = webscrap_fact()
        fact_descr = str(fact_descr).replace('<em>', '')
        fact_descr = fact_descr.replace('</em>', '')
        embed_fact = discord.Embed(
            title=fact_descr,
            colour=discord.Color.greyple()
        )
        embed_fact.set_image(url=img_url)
        await ctx.send(embed=embed_fact)

    """
    Called if CommandInvokeError occurs while calling fact command. (it sometimes happens, unknown reason)
    If it happens, it sends a message in the channel.
    """
    @fact.error
    async def fact_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Cene bugged me again, try one more time, please :feelsbadman:')


def setup(client):
    client.add_cog(Education(client))
