from Question import Question
import discord
from discord.ext import commands


class Trivia(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.question = Question(client)

    @commands.Cog.listener()
    async def on_ready(self):
        print('[COG] Trivia ready.')

    @commands.command()
    async def trivia(self, ctx):
        await self.question.ask_question()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.question is not None:
            if self.question.get_awaiting_answer():
                channel = message.channel
                if await self.question.check_answer(message, channel):
                    self.question = Question(self.client)


def setup(client):
    client.add_cog(Trivia(client))
