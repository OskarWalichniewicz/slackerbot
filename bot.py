import discord
from discord.ext import commands
import os
from datetime import date, datetime, timedelta
from github import Github
import asyncio
from quotes import *

client = commands.Bot(command_prefix = '.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

def save_to_github(file_name):
    g = Github("OskarWalichniewicz", str(os.environ['GITHUB_PASSWORD']))
    repo = g.get_repo("OskarWalichniewicz/slackerbot")
    contents = repo.get_contents("variables.json")
    repo.update_file(contents.path, "az wrote something", file_name, contents.sha)

wait_time = 60 #how many seconds each status change
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('Milica is a midget'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Dran doesn\'t have mats'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Az is dead'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Cenelia is handsome'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Bobsy is being molested'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Awy is the wisest'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Akcent hates Cene'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Gazda likes Rasta'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Segment is old'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Tesla was croatian'))
        await asyncio.sleep(wait_time)

@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print("Bot ready")

@client.event
async def on_message(message):
    if message.author.id == int(os.environ['AZ_DISCORD_ID']):
        year = message.created_at.year
        month = message.created_at.month
        day = message.created_at.day
        hour = message.created_at.hour
        minute = message.created_at.minute
        second = message.created_at.second
        az_file_input = year + "\n" + month + "\n"+ day + "\n"+ hour + "\n" +minute + "\n"+ second
        az_file = open("az.txt", "w").close()
        az_file = open("az.txt", "w")
        az_file.write(az_file_input)
    if message.content == '.azsave' and message.author.id == 247438282424713216: # if Nefil writes .azsave it should save to github
        save_to_github(az_file_input)

    await client.process_commands(message)

@client.command()
async def awy(ctx):
    await ctx.send(get_quote(awy_list))

@client.command()
async def akcent(ctx):
    await ctx.send('https://prnt.sc/udv05c')

@client.command()
async def stonelia(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/709413405131407380/Screenshot_794.png?width=686&height=515 \n https://image.prntscr.com/image/pUq5QnZ9Ti_xDzfgi6oRkw.png ')

@client.command()
async def stonement(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/753284032036470824/unknown.png?width=728&height=515')

@client.command()
async def pam(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/752975692966264902/Screenshot_797.png?width=684&height=515')

@client.command()
async def dran(ctx):
    await ctx.send(get_quote(dran_list))

@client.command()
async def franek(ctx):
    await ctx.send(get_quote(franek_list))

@client.command()
async def shiba(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/364712407601512450/754369041975476304/IMG_20191225_142058.jpg')

@client.command()
async def nika(ctx):
    await ctx.send(get_quote(nika_list))

@client.command()
async def segment(ctx):
    await ctx.send(get_quote(segment_list))

@client.command()
async def ignios(ctx):
    await ctx.send('Fuck Ignios')

@client.command()
async def pupinka(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/364712407601512450/399218303739887617/WoWScrnShot_010618_160818.jpg')

@client.command()
async def cene(ctx):
    await ctx.send(get_quote(cene_list))

@client.command()
async def az(ctx):
    lines = []
    with open('az.txt') as f:
        lines = [line.rstrip() for line in f]
        az_date = datetime(int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3]), int(lines[4]), int(lines[5]))

    curr_date = datetime.now()
    print("Current time: " + str(curr_date))

    diff = curr_date - az_date
    diff_days = diff.days
    diff_hours = (diff.seconds // 3600)
    diff_minutes = (diff.seconds // 60) % 60
    diff_seconds = diff.seconds - diff_hours * 3600 - diff_minutes * 60

    if diff_days > 0:
        outp = "Az died {} days, {} hours, {} minutes, {} seconds ago".format(diff_days, diff_hours, diff_minutes, diff_seconds)
    else:
        if diff_hours > 0:
            outp = "Az died {} hours, {} minutes, {} seconds ago".format(diff_hours, diff_minutes, diff_seconds)
        else:
            if diff_minutes > 0:
                outp = "Az died {} minutes, {} seconds ago".format(diff_minutes, diff_seconds)
            else:
                if diff_seconds > 0:
                    outp = "Az died {} seconds ago".format(diff_seconds)


    if diff_days == 1:
        outp = outp.replace("days", "day")
    if diff_hours == 1:
        outp = outp.replace("hours", "hour")
    if diff_minutes == 1:
        outp = outp.replace("minutes", "minute")
    if diff_seconds == 1:
        outp = outp.replace("seconds", "second")

    await ctx.send(outp)


client.run(os.environ['DISCORD_TOKEN']) #token