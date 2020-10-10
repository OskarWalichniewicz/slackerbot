import discord
from discord.ext import commands
from googletrans import Translator
from webscraping import *
import cyrtranslit


class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Translate ready.')

    @commands.command(aliases=['rs', 'sr'])
    async def serbian(self, ctx, *, text):
        outp_cyr = translator.translate(text, dest='sr').text
        outp_lat = cyrtranslit.to_latin(outp_cyr)
        await ctx.send(str(outp_cyr + "\n" + outp_lat))

    @commands.command(aliases=['en'])
    async def english(self, ctx, *, text):
        outp = translator.translate(text, dest='en').text
        await ctx.send(str(outp))

    @commands.command(aliases=['nl'])
    async def dutch(self, ctx, *, text):
        outp = translator.translate(text, dest='nl').text
        await ctx.send(str(outp))

    @commands.command(aliases=['it'])
    async def italian(self, ctx, *, text):
        outp = translator.translate(text, dest='it').text
        await ctx.send(str(outp))

    @commands.command(aliases=['pl'])
    async def polish(self, ctx, *, text):
        outp = translator.translate(text, dest='pl').text
        await ctx.send(str(outp))

    @commands.command(aliases=['ro'])
    async def romanian(self, ctx, *, text):
        outp = translator.translate(text, dest='ro').text
        await ctx.send(str(outp))

    @commands.command(aliases=['dym'])
    async def didyoumean(self, ctx, *, query):
        if " " in query:
            query.replace(" ", "+")
        didyoumean = webscrap_didyoumean(origin_language='auto', query=query)
        if didyoumean != "":
            await ctx.send("Did you mean: {}".format(didyoumean))
        else:
            await ctx.send("Looks fine to me.")


def setup(client):
    client.add_cog(Translate(client))


translator = Translator()
