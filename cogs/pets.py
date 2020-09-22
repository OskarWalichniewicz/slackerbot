import discord
from discord.ext import commands
import random
from webscraping import *

class Pets(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Pets ready.')

    @commands.command()
    async def nika(self, ctx):
        await ctx.send(get_picture(nika_list))

    @commands.command()
    async def dran(self, ctx):
        await ctx.send(get_picture(dran_list))

    @commands.command()
    async def franek(self, ctx):
        await ctx.send(get_picture(franek_list))

    @commands.command()
    async def shiba(self, ctx):
        await ctx.send(get_picture(shiba_list))

    @commands.command()
    async def cat(self, ctx):
        cat_img = webscrap_random_api('cat')
        await ctx.send(cat_img)

    @commands.command()
    async def panda(self, ctx):
        panda_img = webscrap_random_api('panda')
        await ctx.send(panda_img)

    @commands.command()
    async def rpanda(self, ctx):
        rpanda_img = webscrap_random_api('red_panda')
        await ctx.send(rpanda_img)

    @commands.command()
    async def fox(self, ctx):
        fox_img = webscrap_random_api('fox')
        await ctx.send(fox_img)

    @commands.command()
    async def koala(self, ctx):
        koala_img = webscrap_random_api('koala')
        await ctx.send(koala_img)

    @commands.command()
    async def dog(self, ctx):
        dog_img = webscrap_dog()
        await ctx.send(dog_img)

    @commands.command()
    async def duck(self, ctx):
        duck_img = webscrap_duck()
        await ctx.send(duck_img)

def setup(client):
    client.add_cog(Pets(client))

def get_picture(pic_list):
    rolled_picture = random.choice(pic_list)
    return rolled_picture

nika_list = ['https://cdn.discordapp.com/attachments/364712407601512450/754369363313819760/20200912_175256.jpg',
    'https://cdn.discordapp.com/attachments/364712407601512450/754369363532054538/20200912_175340.jpg',
    'https://media.discordapp.net/attachments/364712407601512450/754369363754090616/20200912_175350.jpg',
    'https://cdn.discordapp.com/attachments/364712407601512450/754369363942834216/20200912_175307.jpg',
    'https://media.discordapp.net/attachments/364712407601512450/754369364261863544/20200912_175318.jpg',
    'https://media.discordapp.net/attachments/364712407601512450/754369364496482334/20200912_175329.jpg']
dran_list = ['https://media.discordapp.net/attachments/364712407601512450/754368051431866378/image0.jpg',
    'https://media.discordapp.net/attachments/364712407601512450/754368473903267870/image0.jpg',
    'https://cdn.discordapp.com/attachments/364712407601512450/754368474792329216/image1.jpg']
franek_list = ['https://i.imgur.com/XB6Qptw.jpg',
    'https://i.imgur.com/F4GCJWf.jpg',
    'https://i.imgur.com/YoNbgR8.jpeg',
    'https://i.imgur.com/IJTAOJm.jpg',
    'https://i.imgur.com/CsJ3X2r.jpeg',
    'https://i.imgur.com/uFy1I1y.jpeg',
    'https://i.imgur.com/bn5eomm.jpg',
    'https://i.imgur.com/YQMyBRn.jpeg',
    'https://i.imgur.com/2dKCJAo.jpeg']
shiba_list = ['https://cdn.discordapp.com/attachments/364712407601512450/754369041975476304/IMG_20191225_142058.jpg']