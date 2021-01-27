import discord
from discord.ext import commands, tasks
import os
import asyncio
import datetime
from reddit import *
from Question import *
from mongoDB import MongoDB

# initiates Bot with prefix ('.')
client = commands.Bot(command_prefix='.')
mongoDB = MongoDB()

"""
Checks if current time (UTC) is between given values.
params: begin_time and end_time are both in datetime format; therefore they should be initiated as ones
        e.g. is_time_between(time(4, 00), time(10,00)) (hh, mm)
returns: boolean
"""


def is_time_between(begin_time, end_time):
    check_time = datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:                                                           # if crosses midnight
        return check_time >= begin_time or check_time <= end_time


"""
Adds Cogs functionality.
Loop goes through 'cogs' folder;
If file is in .py format it loads it, naming it same as file's name.
"""


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

"""
Changes Bot status (activity)
params: wait_time is a time that needs to pass before next activity loads (in seconds)
"""


async def status_task(wait_time):
    while True:
        await client.change_presence(activity=discord.Game('Smile often!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Az is dead!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Drink water!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Milica is a midget.'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Spread love!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Stay positive!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Cenelia is handsome!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('You are beautiful!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Believe in yourself!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Segment is a boomer!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Everything will be fine!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('You can do it!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Be good to others!'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Be good to yourself!'))
        await asyncio.sleep(wait_time)
        if is_time_between(datetime.time(4, 00), datetime.time(11, 00)):
            await client.change_presence(activity=discord.Game('Good Morning!'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('What an amazing day!'))
            await asyncio.sleep(wait_time)
        elif is_time_between(datetime.time(11, 00), datetime.time(17, 00)):
            await client.change_presence(activity=discord.Game('Good Afternoon!'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('Take a break!'))
            await asyncio.sleep(wait_time)
        elif is_time_between(datetime.time(17, 00), datetime.time(22, 00)):
            await client.change_presence(activity=discord.Game('Good Evening!'))
            await asyncio.sleep(wait_time)
        else:
            await client.change_presence(activity=discord.Game('Go to bed!'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('Tomorrow will be good day!'))
            await asyncio.sleep(wait_time)

"""
'event' is a decorator that registers an event it listens to.
on_ready is called when client (bot) is done preparing the data received from Discord.
"""


@client.event
async def on_ready():
    client.loop.create_task(status_task(60))  # loops status_task in background
    clean_removed_memes_loop.start()
    refresh_list_loop.start()
    print("[BOT] Client ready.")

"""
Every 10 hours calls clean_removed_memes_loop() from reddit.py
Used so memes_removed list doesn't get too big, affecting performance.
"""


@tasks.loop(hours=10)
async def clean_removed_memes_loop():
    clean_removed_memes(12)
    print("[LOOP] Cleaned removed memes list.")

"""
Every 2 hours calls remove_old_memes(x) from reddit.py and
populate_memes(y) from reddit.py
Used so memes in memes_list are fresh.
"""


@tasks.loop(hours=2)
async def refresh_list_loop():
    remove_old_memes(10)  # removes memes older than 10h from list
    populate_memes(200)  # populates reddit memes list up to len 100
    print("[LOOP] Removed old memes and repopulated memes list.")

"""
on_message is called when message is sent.
Case 1) If Azhanim wrote something it saves the time at which message was sent to github slackerbot_misc repository
        (calling save_to_github from github_intergration.py) in format (year\nmonth\nday\nhour\nminute\nsecond)
"""


@client.event
async def on_message(message):
    # Checks if message is sent by Azhanim (compares his ID to the from message).
    if message.author.id == int(os.environ['AZ_DISCORD_ID']):
        az_id = str(os.environ['AZ_DISCORD_ID'])
        query = {
            'discord_id': az_id
        }
        last_message_update = {
            'year': message.created_at.year,
            'month': message.created_at.month,
            'day': message.created_at.day,
            'hour': message.created_at.hour,
            'minute': message.created_at.minute,
            'second': message.created_at.second
        }
        await mongoDB.update_data(await mongoDB.open_last_message(), query, last_message_update)

    # this is necessary part of on_message().
    await client.process_commands(message)

# connects this file with Bot created at Discord Developer Portal by given token.
client.run(os.environ['DISCORD_TOKEN'])
