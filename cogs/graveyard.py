import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
import urllib.request
from github_integration import read_file
import contextlib
from mongoDB import MongoDB
import os


class Graveyard(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mongoDB = MongoDB()

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
        az_id = str(os.environ['AZ_DISCORD_ID'])
        query = {
            'discord_id': az_id
        }
        az = self.mongoDB.get_data(last_message, query)
        """
        {
            "_id":{"$oid":"5f8326bc278b5fa87391f0f2"},
            "discord_id":"329341017914605569",
            "year":"2020",
            "month":{"$numberInt":"10"},
            "day":{"$numberInt":"10"},
            "hour":{"$numberInt":"19"},
            "minute":{"$numberInt":"49"},
            "second":{"$numberInt":"20"}
        }
        """
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
