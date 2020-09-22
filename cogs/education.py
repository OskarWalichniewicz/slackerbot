import discord
from discord.ext import commands
from word import *
from webscraping import *
from profanityfilter import ProfanityFilter

pf = ProfanityFilter()

async def is_not_awy(ctx): # checks if command caller is not Awy.
    return ctx.author.id != 245247289935921152

class Education(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Education ready.')

    @commands.command()
    async def word(self, ctx, *text):
        try:
            if len(text) > 1:
                await ctx.send("stupid bonobo, the command is called .word (singular) for a reason.")
                return None
            english_word = text[0]
            serbian_word_cyr, serbian_word_lat = translate_word(english_word, 'sr')
            serbian_word = str(serbian_word_cyr) + " / " + str(serbian_word_lat)
            italian_word = translate_word(english_word, 'it')
            dutch_word = translate_word(english_word, 'nl')
            polish_word = translate_word(english_word, 'pl')
            romanian_word = translate_word(english_word, 'ro')

            def_string = get_definitions(english_word)
            syn_string = get_synonyms(english_word)

            if def_string == "":
                embed_word = discord.Embed(
                    title = '{}'.format(english_word.upper()),
                    colour = discord.Color.orange()
                )
            else:
                embed_word = discord.Embed(
                    title = '{}'.format(english_word.upper()),
                    description = def_string,
                    colour = discord.Color.orange()
                )

            embed_word.add_field(name = ':flag_gb: English :flag_gb:', value = english_word, inline = False)
            embed_word.add_field(name = ':flag_rs: Serbian :flag_rs:', value = serbian_word, inline = True)
            embed_word.add_field(name = ':flag_it: Italian :flag_it:', value = italian_word, inline = False)
            embed_word.add_field(name = ':flag_nl: Dutch :flag_nl:', value = dutch_word, inline = True)
            embed_word.add_field(name = ':flag_pl: Polish :flag_pl:', value = polish_word, inline = False)
            embed_word.add_field(name = ':flag_ro: Romanian :flag_ro:', value = romanian_word, inline = True)

            footer = ""
            if syn_string != "":
                footer = "Synonyms: " + syn_string

            if footer != "":
                embed_word.set_footer(text = footer)

            await ctx.send(embed = embed_word)

        except IndexError: # If someone types something after .word
            print("[.WORD] IndexError")

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
        syn_string = get_synonyms(english_word)

        if def_string == "":
            embed_word = discord.Embed(
                title = '{}'.format(english_word.upper()),
                colour = discord.Color.orange()
            )
        else:
            embed_word = discord.Embed(
                title = '{}'.format(english_word.upper()),
                description = def_string,
                colour = discord.Color.orange()
            )

        embed_word.add_field(name = ':flag_gb: English :flag_gb:', value = english_word, inline = False)
        embed_word.add_field(name = ':flag_rs: Serbian :flag_rs:', value = serbian_word, inline = True)
        embed_word.add_field(name = ':flag_it: Italian :flag_it:', value = italian_word, inline = False)
        embed_word.add_field(name = ':flag_nl: Dutch :flag_nl:', value = dutch_word, inline = True)
        embed_word.add_field(name = ':flag_pl: Polish :flag_pl:', value = polish_word, inline = False)
        embed_word.add_field(name = ':flag_ro: Romanian :flag_ro:', value = romanian_word, inline = True)

        footer = ""
        if syn_string != "":
            footer = "Synonyms: " + syn_string

        if footer != "":
            embed_word.set_footer(text = footer)

        await ctx.send(embed = embed_word)

    @commands.command()
    @commands.check(is_not_awy)
    async def gimage(self, ctx, *text):
        if pf.censor(str(text)) != str(text):
            await ctx.send('Slacker refuses to search for THAT. Please respect my poor eyes.')
            return None
        query = text
        img_url = webscrap_google_images(query, 1)
        for img in img_url:
            await ctx.send(img)

    @commands.command()
    async def fact(self, ctx):
        img_url, fact_descr = webscrap_fact()
        fact_descr = str(fact_descr).replace('<em>', '')
        fact_descr = fact_descr.replace('</em>', '')
        embed_fact = discord.Embed(
                title = fact_descr,
                colour = discord.Color.orange()
            )
        embed_fact.set_image(url = img_url)
        await ctx.send(embed = embed_fact)

def setup(client):
    client.add_cog(Education(client))