import discord
from discord.ext import commands, tasks
import os
import asyncio
import datetime
from datetime import time as t
from datetime import timedelta
from reddit import *
from Question import *
from mongoDB import MongoDB
from cogs.news import top_news_from_world
from itertools import cycle

# initiates Bot with prefix ('.')
client = commands.Bot(command_prefix='.')
mongoDB = MongoDB()

"""
Lists of statuses (activities) that bot will have, depending on time of the day (all times in UTC, 24h format).
ACTIVITY_LIST_MORNING - 5 to 11
ACTIVITY_LIST_GENERAL - 11 to
ACTIVITY_LIST_EVENING - 19 to 24
ACTIVITY_LIST_NIGHT - 24 to 5
"""
ACTIVITY_LIST_GENERAL = ['Smile often!', 'Az is dead!', 'Drink water!', 'Milica is a midget.',
                         'Spread love!', 'Stay positive!', 'Cenelia is handsome!', 'You are beautiful!', 'Believe in yourself!', 'Segment is a boomer!', 'Everything will be fine!', 'You can do it!', 'Be good to others!', 'Be good to yourself!']
activity_list_general_cycle = cycle(ACTIVITY_LIST_GENERAL)
ACTIVITY_LIST_MORNING = ['Good morning!', 'Have a nice day!',
                         'Hope you slept well!', 'Don\'t slack!', 'New day, new beginnings!']
activity_list_morning_cycle = cycle(ACTIVITY_LIST_MORNING)
ACTIVITY_LIST_EVENING = ['You deserve a rest!', 'Hope your day was good!',
                         'It\'s time to relax now!', 'Was your dinner good?']
activity_list_evening_cycle = cycle(ACTIVITY_LIST_EVENING)
ACTIVITY_LIST_NIGHT = ['Good night!', 'Why aren\'t you sleeping yet?',
                       'It\'s bed time!', 'Don\'t stay too long!', 'See you tomorrow!', 'Sleep tight!']
activity_list_night_cycle = cycle(ACTIVITY_LIST_NIGHT)


def next_activity(cycle):
    return next(cycle)


"""
Main channel of bembem server, used for sending daily summary of news.
"""
SLACKERS_CHANNEL_ID = 364712407601512450

"""
Checks if current_time is between given values.
params: begin_time - current time is later than this
        end_time - current time is earlier than this
        current_time - all in datetime.datetime format -> (hh, mm)
returns: boolean
"""


def is_time_between(begin_time, end_time, current_time):
    if begin_time < end_time:
        return current_time >= begin_time and current_time <= end_time
    else:                                                           # if crosses midnight
        return current_time >= begin_time or current_time <= end_time


"""
Checks if current_time is equal to target_time
params: target_time - target time is equal to this
        current_time - all in datetime.datetime format -> (hh, mm)
returns: boolean
"""


def is_time_equal(target_time, current_time):
    return target_time == current_time


"""
Checks what time is it currently, and based on that makes actions.
1. If time is equal to 18 UTC - it sends message to bembem's main channel with summary of news (top_news_from_world())
2. It changes bot presence (activity) based on current time. (see ACTIVITY_LIST)

Uses: is_time_equal()
            top_news_from_world()
      is_time_between()
"""


async def change_activity(wait_time):
    now = dt.utcnow().time()  # current time

    if is_time_between(t(5, 00), t(11, 00), now):  # from 5 AM to 11 AM
        activity = next_activity(activity_list_morning_cycle)
    elif is_time_between(t(19, 00), t(0, 00), now):  # from 19 to 24
        activity = next_activity(activity_list_evening_cycle)
    elif is_time_between(t(0, 00), t(5, 00), now):  # from midnight to 5AM
        activity = next_activity(activity_list_night_cycle)
    else:
        activity = next_activity(activity_list_general_cycle)

    asyncio.sleep(wait_time)
    await client.change_presence(activity=discord.Game(activity))


async def calculate_time_difference(message_time):

    start_time = dt.utcnow().time()

    start_time_delta = datetime.timedelta(
        hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)

    schedule_delta = datetime.timedelta(
        hours=message_time.hour, minutes=message_time.minute, seconds=message_time.second)

    difference_delta = schedule_delta - now_delta
    return difference_delta.seconds


async def daily_news(time_delta, channel_id):
    channel_slackers = client.get_channel(channel_id)
    print("[LOOP] [DAILY_NEWS] {} seconds to message".format(time_delta))
    asyncio.sleep(time_delta)
    while True:
        embed_news = await top_news_from_world()
        await channel_slackers.send(embed=embed_news)
        asyncio.sleep(86400)
        print("[LOOP] [DAILY_NEWS] 86400 seconds to message")


async def main_loop(time_delta, channel_id):
    while True:
        await change_activity(30)
        await daily_news(time_delta, channel_id)

"""
Adds Cogs functionality.
Loop goes through 'cogs' folder;
If file is in .py format it loads it, naming it same as file's name.
"""


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


"""
'event' is a decorator that registers an event it listens to.
on_ready is called when client (bot) is done preparing the data received from Discord.
"""


@client.event
async def on_ready():
    time_difference = await calculate_time_difference(t(18, 00))

    client.loop.create_task(main_loop(time_difference, SLACKERS_CHANNEL_ID))

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
Case 1) If Azhanim (checks by ID) wrote something it queries the document with Az's ID and
        updates this document's time with time at which message was sent to mongoDB database.
        Document format:
            {'discord_id': [str],
             'year': [int],
             'month': [int],
             'day': [int],
             'hour': [int],
             'minute': [int],
             'second': [int]}
        Uses: update_data()
                  open_last_message() from mongoDB class.
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
