import discord
from discord.ext import commands, tasks
import os
import asyncio
from datetime import datetime as dt
from datetime import time as t
from reddit import *
from Question import *
from mongoDB import MongoDB
from cogs.news import top_news_from_world

# initiates Bot with prefix ('.')
client = commands.Bot(command_prefix='.')
mongoDB = MongoDB()

ACTIVITY_LIST_GENERAL = ['Smile often!', 'Az is dead!', 'Drink water!', 'Milica is a midget.',
                         'Spread love!', 'Stay positive!', 'Cenelia is handsome!', 'You are beautiful!', 'Believe in yourself!', 'Segment is a boomer!', 'Everything will be fine!', 'You can do it!', 'Be good to others!', 'Be good to yourself!']
ACTIVITY_LIST_MORNING = ['Good morning!', 'Have a nice day!',
                         'Hope you slept well!', 'Don\'t slack!', 'New day, new beginnings!']
ACTIVITY_LIST_EVENING = ['You deserve a rest!', 'Hope your day was good!',
                         'It\'s time to relax now!', 'Was your dinner good?']
ACTIVITY_LIST_NIGHT = ['Good night!', 'Why aren\'t you sleeping yet?',
                       'It\'s bed time!', 'Don\'t stay too long!', 'See you tomorrow!', 'Sleep tight!']

SLACKERS_CHANNEL_ID = 364712407601512450
slacker_channel = client.get_channel(SLACKERS_CHANNEL_ID)

"""
Checks if current time (UTC) is between given values.
params: begin_time and end_time are both in datetime format; therefore they should be initiated as ones
        e.g. is_time_between(time(4, 00), time(10,00)) (hh, mm)
returns: boolean
"""


def is_time_between(begin_time, end_time):
    check_time = dt.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:                                                           # if crosses midnight
        return check_time >= begin_time or check_time <= end_time

    """Checks if current time (UTC) is equal to given parameter.
    """


def is_time_equal(time):
    check_time = dt.utcnow().time()
    return time == check_time


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


async def main_loop(wait_time):
    while True:
        if is_time_between(t(5, 00), t(11, 00)):  # from 5 AM to 11 AM
            for activity in ACTIVITY_LIST_MORNING:
                await client.change_presence(activity=discord.Game(activity))
                await asyncio.sleep(wait_time)
        elif is_time_between(t(19, 00), t(0, 00)):  # from 19 to 24
            for activity in ACTIVITY_LIST_EVENING:
                await client.change_presence(activity=discord.Game(activity))
                await asyncio.sleep(wait_time)
        elif is_time_between(t(0, 00), t(5, 00)):  # from midnight to 5AM
            for activity in ACTIVITY_LIST_NIGHT:
                await client.change_presence(activity=discord.Game(activity))
                await asyncio.sleep(wait_time)
        else:
            for activity in ACTIVITY_LIST_GENERAL:  # from 11 AM to 19
                await client.change_presence(activity=discord.Game(activity))
                await asyncio.sleep(wait_time)


async def news_loop():
    while True:
        if is_time_equal(t(18, 30)):
            print("[LOOP] Sending top news.")
            embed_news = await top_news_from_world()
            await slacker_channel.send(embed=embed_news)


"""
'event' is a decorator that registers an event it listens to.
on_ready is called when client (bot) is done preparing the data received from Discord.
"""


@client.event
async def on_ready():
    # loops status_task in background
    client.loop.create_task(main_loop(30))
    client.loop.create_task(news_loop())
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
