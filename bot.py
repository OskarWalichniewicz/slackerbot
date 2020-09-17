import discord
from discord.ext import commands
import os
import asyncio
from github_integration import *
from datetime import datetime, time

# initiates Bot with prefix ('.')
client = commands.Bot(command_prefix = '.')

"""
Checks if current time (UTC) is between given values.
params: begin_time and end_time are both in datetime format; therefore they should be initiated as ones
        e.g. is_time_between(time(4, 00), time(10,00))
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
        await client.change_presence(activity=discord.Game('Bobsy is being molested.'))
        await asyncio.sleep(wait_time)
        await client.change_presence(activity=discord.Game('Be good to others!'))
        await asyncio.sleep(wait_time)
        if is_time_between(time(4, 00), time(11, 00)):
            await client.change_presence(activity=discord.Game('Good Morning!'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('What an amazing day!'))
            await asyncio.sleep(wait_time)
        elif is_time_between(time(11, 00), time(17, 00)):
            await client.change_presence(activity=discord.Game('Good Afternoon!'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('Take a break!'))
            await asyncio.sleep(wait_time)
        elif is_time_between(time(17,00), time(22,00)):
            await client.change_presence(activity=discord.Game('Good Evening!'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('You should bath :worried:'))
            await asyncio.sleep(wait_time)
        else:
            await client.change_presence(activity=discord.Game('Go to bed! :rage:'))
            await asyncio.sleep(wait_time)
            await client.change_presence(activity=discord.Game('Tomorrow will be good day!'))
            await asyncio.sleep(wait_time)

"""
'event' is a decorator that registers an event it listens to.
on_ready is called when client (bot) is done preparing the data received from Discord.
"""
@client.event
async def on_ready():
    client.loop.create_task(status_task(60)) # loops status_task in background
    print("[BOT] Client ready.")

"""
on_message is called when message is sent.
"""
@client.event
async def on_message(message):
    if message.author.id == int(os.environ['AZ_DISCORD_ID']): # Checks if message is sent by Azhanim (compares his ID to the from message).
        year = message.created_at.year # message.created_at returns datetime
        month = message.created_at.month # assigning date elements to correspodning variables
        day = message.created_at.day
        hour = message.created_at.hour
        minute = message.created_at.minute
        second = message.created_at.second
        az_file_input = str(year) + "\n" + str(month) + "\n" + str(day) + "\n" + str(hour) + "\n" + str(minute) + "\n"+ str(second) # creates string, with each variable in new line
        save_to_github(az_file_input, "az.txt", "OskarWalichniewicz/slackerbot_misc", "Az sent message.") # calls save_to_github method from github_integration.py and passes previously created string; repository name and commit message

    await client.process_commands(message) # this is necessary part of on_message().

client.run(os.environ['DISCORD_TOKEN']) # connects this file with Bot created at Discord Developer Portal by given token.