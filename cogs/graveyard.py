import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
import urllib.request
import contextlib

class Graveyard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Graveyard ready.')

    @commands.command()
    async def az(self, ctx):
        lines = []
        with contextlib.closing(urllib.request.urlopen('https://raw.githubusercontent.com/OskarWalichniewicz/slackerbot_misc/master/az.txt')) as x:
            for line in x:
                lines.append(line.decode('utf-8').strip())

        az_date = datetime(int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3]), int(lines[4]), int(lines[5]))

        curr_date = datetime.now()

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

def setup(client):
    client.add_cog(Graveyard(client))