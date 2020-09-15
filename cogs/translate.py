import discord
from discord.ext import commands
from googletrans import Translator
import cyrtranslit

class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Translate ready.')

    @commands.command(aliases = ['serbian', 'rs', 'sr'])
    async def _serbian(self, ctx, *, text):
        outp_cyr = translator.translate(text, dest = 'sr').text
        outp_lat = cyrtranslit.to_latin(outp_cyr)
        await ctx.send(str(outp_cyr + "\n" + outp_lat))

    @commands.command(aliases = ['english', '.en'])
    async def _english(self, ctx, *, text):
        outp = translator.translate(text, dest = 'en').text
        await ctx.send(str(outp))

    @commands.command(aliases = ['dutch', '.nl'])
    async def _dutch(self, ctx, *, text):
        outp = translator.translate(text, dest = 'nl').text
        await ctx.send(str(outp))

    @commands.command(aliases = ['italian', '.it'])
    async def _italian(self, ctx, *, text):
        outp = translator.translate(text, dest = 'it').text
        await ctx.send(str(outp))

    @commands.command(aliases = ['polish', '.pl'])
    async def _polish(self, ctx, *, text):
        outp = translator.translate(text, dest = 'pl').text
        await ctx.send(str(outp))

    @commands.command(aliases = ['romanian', '.ro'])
    async def _romanian(self, ctx, *, text):
        outp = translator.translate(text, dest = 'ro').text
        await ctx.send(str(outp))

def setup(client):
    client.add_cog(Translate(client))

translator = Translator()
