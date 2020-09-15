import discord
from discord.ext import commands
import os
import asyncio
from github_integration import *
from datetime import datetime, time

client = commands.Bot(command_prefix = '.')

def is_time_between(begin_time, end_time):
    check_time = datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:                                                           # if crosses midnight
        return check_time >= begin_time or check_time <= end_time

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

async def status_task(wait_time):
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
        await client.change_presence(activity=discord.Game('Segment is old'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Tesla was croatian'))
        await asyncio.sleep(wait_time)
        if is_time_between(time(4, 00), time(11, 00)):
            await client.change_presence(activity=discord.Game('Good Morning!'))
            await asyncio.sleep(wait_time)
        elif is_time_between(time(11, 00), time(17, 00)):
            await client.change_presence(activity=discord.Game('Good Afternoon!'))
            await asyncio.sleep(wait_time)
        elif is_time_between(time(17,00), time(22,00)):
            await client.change_presence(activity=discord.Game('Good Evening!'))
            await asyncio.sleep(wait_time)
        else:
            await client.change_presence(activity=discord.Game('Go to bed! :rage:'))
            await asyncio.sleep(wait_time)

@client.event
async def on_ready():
    client.loop.create_task(status_task(60))
    print("Bot ready")

@client.event
async def on_message(message):
    if message.author.id == int(os.environ['SEG_DISCORD_ID']):
        year = message.created_at.year
        month = message.created_at.month
        day = message.created_at.day
        hour = message.created_at.hour
        minute = message.created_at.minute
        second = message.created_at.second
        az_file_input = str(year) + "\n" + str(month) + "\n"+ str(day) + "\n"+ str(hour) + "\n" + str(minute) + "\n"+ str(second)
        save_to_github(az_file_input)

    await client.process_commands(message)

client.run(os.environ['DISCORD_TOKEN'])