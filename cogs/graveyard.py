import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
import urllib.request
from github_integration import read_file
import contextlib

class Graveyard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Graveyard ready.')

    """
    When az command is called,
    it opens (calls read_file from github_integration.py) az.txt file from slackerbot_misc repository and read its content line by line,
    creating variables (year, month, day, ...) and calculating difference between current time and time from file and sends it in discord message.
    """
    @commands.command()
    async def az(self, ctx):
        lines = []
        x = read_file("az.txt", "OskarWalichniewicz/slackerbot_misc")
        x_iter = iter(x.splitlines()) # reads line by line
        for line in x_iter:
            lines.append(line.strip()) # appends line list

        az_date = datetime(int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3]), int(lines[4]), int(lines[5])) # creates datetime element

        curr_date = datetime.now()

        diff = curr_date - az_date # calculate difference
        diff_days = diff.days
        diff_hours = (diff.seconds // 3600)
        diff_minutes = (diff.seconds // 60) % 60
        diff_seconds = diff.seconds - diff_hours * 3600 - diff_minutes * 60

        if diff_days > 0: # if days are 0 it doesnt print days (cause its pointless) - visual thing
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

        if diff_days == 1: # if days are plural - changes plural word to singular (words - word)
            outp = outp.replace("days", "day")
        if diff_hours == 1:
            outp = outp.replace("hours", "hour")
        if diff_minutes == 1:
            outp = outp.replace("minutes", "minute")
        if diff_seconds == 1:
            outp = outp.replace("seconds", "second")

        await ctx.send(outp)

def setup(client):
    client.add_cog(Graveyard(client))