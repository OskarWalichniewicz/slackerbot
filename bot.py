import discord
from discord.ext import commands
import os
import random


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot ready")

# @client.command()
# async def dran(ctx):
#     await ctx.send('Dran still does not have mats.')

@client.command()
async def awy(ctx):
    awyQuotes = ['MONSTRUJM',
    'biopolar or smth',
    'im such a god of english language',
    'sign of asking',
    'i am "CHAOTIC EVIL"',
    'i do not classify myserlf as good person',
    'she is prettending to be villian like i was to make that lesbo realise her true sexual envoirment',
    'why you  heff to be so mad at me all the time',
    'IM MMATURE',
    'i would gladly be  at the bottom if we talkin some bigass latina chick',
    'satan himself will get borred of trying to tourment me',
    'but you be pullin some Merlin shit summoning excalibuyrs worry not',
    'CENE YOU ARE MARIA TERESA',
    'well ye i cheated on her but like cmone she has allready girlfriend if i find another one to throw asidewhy shodln\'t i 2000 iq decision making']
    await ctx.send('Awy once said: "{}".'.format(random.choice(awyQuotes)))


client.run(os.environ['DISCORD_TOKEN']) #token