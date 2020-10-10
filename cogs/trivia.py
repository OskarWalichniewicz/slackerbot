from Question import Question
import discord
from discord.ext import commands


class Trivia(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia ready.')

    @commands.command()
    async def trivia(self, ctx):
        await question.ask_question()


def setup(client):
    client.add_cog(Trivia(client))
