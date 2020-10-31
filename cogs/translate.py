import discord
from discord.ext import commands
from googletrans import Translator
from webscraping import *
from word import *
import cyrtranslit


class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Translate ready.')

    @commands.command(aliases=['rs', 'sr'])
    async def serbian(self, ctx, *, text):
        translated_cyr, translated = translate_word(text, 'sr', 'auto')
        await ctx.send(str(translated_cyr + "\n" + translated))

    @commands.command(aliases=['en'])
    async def english(self, ctx, *, text):
        outp = translate_word(text, 'en', 'auto')
        await ctx.send(str(outp))

    @commands.command(aliases=['nl'])
    async def dutch(self, ctx, *, text):
        outp = translate_word(text, 'nl', 'auto')
        await ctx.send(str(outp))

    @commands.command(aliases=['it'])
    async def italian(self, ctx, *, text):
        outp = translate_word(text, 'it', 'auto')
        await ctx.send(str(outp))

    @commands.command(aliases=['pl'])
    async def polish(self, ctx, *, text):
        outp = translate_word(text, 'pl', 'auto')
        await ctx.send(str(outp))

    @commands.command(aliases=['ro'])
    async def romanian(self, ctx, *, text):
        outp = translate_word(text, 'ro', 'auto')
        await ctx.send(str(outp))

    @commands.command(aliases=['dym'])
    async def didyoumean(self, ctx, *, query):
        if " " in query:
            query.replace(" ", "+")
        didyoumean = webscrap_didyoumean(origin_language='en', query=query)
        if didyoumean != "":
            await ctx.send("Did you mean: {}".format(didyoumean))
        else:
            await ctx.send("Looks fine to me.")


def setup(client):
    client.add_cog(Translate(client))
