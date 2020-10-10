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
        question = Question(ctx)
        await question.ask_question()

    @commands.Cog.listener()
    async def on_message(self, message):
        if question is not None:
            if question.ongoing:
                await question.check_answer(message)


def setup(client):
    client.add_cog(Trivia(client))
