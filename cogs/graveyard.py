import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
import urllib.request
from github_integration import read_file
import contextlib
from mongoDB import MongoDB


class Graveyard(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mongoDB = MongoDB()
        self.mongoDB.open_database("slacker_db")

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Graveyard ready.')

    """
    When az command is called,
    it opens (calls read_file from github_integration.py) az.txt file from slackerbot_misc repository and read its content line by line,
    creating variables (year, month, day, ...) and calculating difference between current time and time from file and sends it in discord message.
    returns how much time ago have az died (string)
    """
    @commands.command()
    async def az(self, ctx):
        lines = []
        x = read_file("az.txt", "OskarWalichniewicz/slackerbot_misc")
        x_iter = iter(x.splitlines())  # reads line by line
        for line in x_iter:
            lines.append(line.strip())  # appends line list

        az_date = datetime(int(lines[0]), int(lines[1]), int(lines[2]), int(
            lines[3]), int(lines[4]), int(lines[5]))  # creates datetime element

        curr_date = datetime.now()

        diff = curr_date - az_date  # calculate difference
        diff_days = diff.days
        diff_hours = (diff.seconds // 3600)
        diff_minutes = (diff.seconds // 60) % 60
        diff_seconds = diff.seconds - diff_hours * 3600 - diff_minutes * 60

        # if days are 0 it doesnt print days (cause its pointless) - visual thing
        if diff_days > 0:
            outp = "Az died {} days, {} hours, {} minutes, {} seconds ago".format(
                diff_days, diff_hours, diff_minutes, diff_seconds)
        else:
            if diff_hours > 0:
                outp = "Az died {} hours, {} minutes, {} seconds ago".format(
                    diff_hours, diff_minutes, diff_seconds)
            else:
                if diff_minutes > 0:
                    outp = "Az died {} minutes, {} seconds ago".format(
                        diff_minutes, diff_seconds)
                else:
                    if diff_seconds > 0:
                        outp = "Az died {} seconds ago".format(diff_seconds)

        # if days are plural - changes plural word to singular (words - word)
        if diff_days == 1:
            outp = outp.replace("days", "day")
        if diff_hours == 1:
            outp = outp.replace("hours", "hour")
        if diff_minutes == 1:
            outp = outp.replace("minutes", "minute")
        if diff_seconds == 1:
            outp = outp.replace("seconds", "second")

        await ctx.send(outp)

    @commands.command()
    async def az_2(self, ctx):
        self.mongoDB.open_collection('last_message')
        query = {
            'discord_id': str(os.environ['AZ_DISCORD_ID'])
        }
        az = self.mongoDB.get_document(query)
        az_date = datetime(
            int(az['year']),
            int(az['month']),
            int(az['day']),
            int(az['hour']),
            int(az['minute']),
            int(az['second']))

        diff_days, diff_hours, diff_minutes, diff_seconds = await self.calculate_difference(az_date)
        output = await self.prepare_string(diff_days, diff_hours, diff_minutes, diff_seconds)

        await ctx.send(output)

    async def calculate_difference(self, date):
        curr_date = datetime.now()
        diff = curr_date - date
        diff_days = diff.days
        diff_hours = (diff.seconds // 3600)
        diff_minutes = (diff.seconds // 60) % 60
        diff_seconds = diff.seconds - diff_hours * 3600 - diff_minutes * 60
        return diff_days, diff_hours, diff_minutes, diff_seconds

    async def prepare_string(self, diff_days, diff_hours, diff_minutes, diff_seconds):
        # if days are 0 it doesnt print days (cause its pointless) - visual thing
        if diff_days > 0:
            outp = "Az died {} days, {} hours, {} minutes, {} seconds ago".format(
                diff_days, diff_hours, diff_minutes, diff_seconds)
        else:
            if diff_hours > 0:
                outp = "Az died {} hours, {} minutes, {} seconds ago".format(
                    diff_hours, diff_minutes, diff_seconds)
            else:
                if diff_minutes > 0:
                    outp = "Az died {} minutes, {} seconds ago".format(
                        diff_minutes, diff_seconds)
                else:
                    if diff_seconds > 0:
                        outp = "Az died {} seconds ago".format(diff_seconds)

        # if days are plural - changes plural word to singular (words - word)
        if diff_days == 1:
            outp = outp.replace("days", "day")
        if diff_hours == 1:
            outp = outp.replace("hours", "hour")
        if diff_minutes == 1:
            outp = outp.replace("minutes", "minute")
        if diff_seconds == 1:
            outp = outp.replace("seconds", "second")

        return outp


def setup(client):
    client.add_cog(Graveyard(client))
